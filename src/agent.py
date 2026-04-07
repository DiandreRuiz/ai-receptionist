from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from dotenv import load_dotenv
from livekit import rtc
from livekit.agents import (
    Agent,
    AgentServer,
    AgentSession,
    JobContext,
    JobProcess,
    TurnHandlingOptions,
    cli,
    inference,
    room_io,
)
from livekit.agents.beta.tools import EndCallTool
from livekit.plugins import noise_cancellation, silero
from livekit.plugins.turn_detector.english import EnglishModel

from knowledge.loaders import KnowledgeBundle, load_knowledge_dir
from tools import ReceptionistTools

load_dotenv(".env.local")

PROMPTS_DIR = Path(__file__).parent / "prompts"
SYSTEM_PROMPT_PATH = PROMPTS_DIR / "receptionist_system_prompt.md"
INBOUND_GREETING_PATH = PROMPTS_DIR / "greeting.md"
KNOWLEDGE_DIR = Path(__file__).resolve().parent / "knowledge"

INBOUND_GREETING_INSTRUCTIONS = INBOUND_GREETING_PATH.read_text()

# Turn handling: ``endpointing.min_delay`` = minimum silence (seconds) after speech
# before the user's turn is considered complete. SDK default is 0.5; slightly
# higher reduces the agent jumping in during short pauses or trailing thought.
# See ``EndpointingOptions`` in livekit.agents.voice.turn.
_USER_TURN_MIN_SILENCE_S = 0.75


def _session_clock_body(when: datetime, tz: ZoneInfo) -> str:
    """Human + ISO lines for the LLM; fixed at job start (body only — heading added in build)."""
    local = when.astimezone(tz) if when.tzinfo else when.replace(tzinfo=tz)
    spoken = local.strftime("%A, %B %d, %Y at %I:%M %p %Z")
    return (
        f"**Local time when this session started** ({tz.key}): **{spoken}** "
        f"(ISO: {local.isoformat(timespec='seconds')}).\n\n"
        "Treat this as **today** when proposing appointment dates, interpreting phrases like "
        "**“tomorrow”** or **“next week,”** and staying consistent within the call. "
        "This timestamp is from session start, not updated every minute."
    )


def _inbound_line_body(caller_phone: str | None) -> str:
    """SIP / console caller-ID facts (body only — heading added in build)."""
    if caller_phone:
        return (
            f"The caller ID on this inbound line is **{caller_phone}** (from SIP). "
            "You may read it back digit-by-digit when confirming the callback number, "
            "following the **Cartesia** guidance in **block D** below. "
            "If the caller says it is wrong, use the number they give instead."
        )
    return (
        "You do **not** have this caller's phone number on this connection "
        "(e.g. console test, web client, or hidden caller ID per trunk/dispatch rules). "
        "Do **not** say you can see their number or read digits back unless they spoke a number. "
        "Still ask **“Is this the best number to contact you on?”** as in your booking rules."
    )


def build_system_instructions(
    knowledge: KnowledgeBundle,
    *,
    caller_phone: str | None = None,
    session_started_at: datetime | None = None,
) -> str:
    # Prompt-assembly constants (kept inside this function; not module globals).
    instruction_divider = "\n\n---\n\n"
    appended_blocks_index = """# Appended: session facts and knowledge bases

**Single merged system message — distinct blocks below.** Scan this index first; **do not** mix up roles (FAQ facts vs. TTS formatting vs. session facts).

- **Block A — Inbound line:** Whether you have the caller's number on **this** connection (SIP).
- **Block B — Session clock:** Fixed **today** for **this call** when interpreting *tomorrow*, *next week*, and appointment dates.
- **Block C — Approved FAQ:** **Consult before** answering general roofing or SK questions; approved facts live here.
- **Block D — Cartesia Sonic-3 TTS:** Rules for **formatting written assistant text** for the voice engine **only** — not facts to read as company policy unless they duplicate the FAQ.
"""
    # Business-local "today" for scheduling copy (South Florida).
    session_clock_tz = ZoneInfo("America/New_York")

    base = SYSTEM_PROMPT_PATH.read_text()
    line_body = _inbound_line_body(caller_phone)
    clock = session_started_at or datetime.now(session_clock_tz)
    clock_body = _session_clock_body(clock, session_clock_tz)
    return (
        f"{base.rstrip()}{instruction_divider}"
        f"{appended_blocks_index.strip()}{instruction_divider}"
        f"## A. Inbound line (this session only)\n\n{line_body}{instruction_divider}"
        f"## B. Session clock (scheduling anchor for this call)\n\n{clock_body}{instruction_divider}"
        f"## C. Approved FAQ (verbatim when it matches)\n\n{knowledge.faq_markdown.strip()}"
        f"{instruction_divider}"
        f"## D. Cartesia Sonic-3 TTS (assistant text formatting for synthesis)\n\n"
        f"{knowledge.cartesia_tts_best_practices_markdown.strip()}"
    )


def _sip_caller_phone_from_room(room: rtc.Room) -> str | None:
    for p in room.remote_participants.values():
        if p.kind != rtc.ParticipantKind.PARTICIPANT_KIND_SIP:
            continue
        raw = p.attributes.get("sip.phoneNumber")
        if raw:
            return str(raw).strip()
    return None


class Assistant(ReceptionistTools, Agent):
    def __init__(
        self,
        knowledge: KnowledgeBundle | None = None,
        *,
        with_end_call_tool: bool = False,
        caller_phone: str | None = None,
        session_started_at: datetime | None = None,
    ) -> None:
        kb = knowledge or load_knowledge_dir(KNOWLEDGE_DIR)
        hangup_tools = [EndCallTool()] if with_end_call_tool else []
        super().__init__(
            instructions=build_system_instructions(
                kb,
                caller_phone=caller_phone,
                session_started_at=session_started_at,
            ),
            tools=hangup_tools,
        )
        self._knowledge = kb

    async def on_enter(self) -> None:
        self.session.generate_reply(instructions=INBOUND_GREETING_INSTRUCTIONS)


server = AgentServer()


def prewarm(proc: JobProcess):
    proc.userdata["vad"] = silero.VAD.load()
    proc.userdata["knowledge"] = load_knowledge_dir(KNOWLEDGE_DIR)


server.setup_fnc = prewarm


@server.rtc_session(agent_name="ai-receptionist-agent")
async def agent(ctx: JobContext):
    ctx.log_context_fields = {
        "room": ctx.room.name,
    }

    knowledge: KnowledgeBundle = ctx.proc.userdata["knowledge"]

    # SIP is usually already on ctx.room when the job runs; if not, prompts handle missing ID.
    caller_phone = _sip_caller_phone_from_room(ctx.room)

    session = AgentSession(
        stt=inference.STT(model="deepgram/nova-3", language="en"),
        llm=inference.LLM(model="openai/gpt-4o"),
        tts=inference.TTS(
            model="cartesia/sonic-3",
            voice="9626c31c-bec5-4cca-baa8-f8ba9e84c8bc",
        ),
        turn_handling=TurnHandlingOptions(
            turn_detection=EnglishModel(),
            endpointing={"min_delay": _USER_TURN_MIN_SILENCE_S},
        ),
        vad=ctx.proc.userdata["vad"],
        # Speculative LLM/TTS before end-of-turn; improves latency (see LiveKit session docs).
        preemptive_generation=True,
    )

    await session.start(
        agent=Assistant(
            knowledge=knowledge,
            with_end_call_tool=True,
            caller_phone=caller_phone,
        ),
        room=ctx.room,
        room_options=room_io.RoomOptions(
            audio_input=room_io.AudioInputOptions(
                noise_cancellation=lambda params: (
                    noise_cancellation.BVCTelephony()
                    if params.participant.kind
                    == rtc.ParticipantKind.PARTICIPANT_KIND_SIP
                    else noise_cancellation.BVC()
                ),
            ),
        ),
    )
    await ctx.connect()


if __name__ == "__main__":
    cli.run_app(server)
