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

# Business-local “today” for scheduling copy (South Florida).
SESSION_CLOCK_TZ = ZoneInfo("America/New_York")

INBOUND_GREETING_INSTRUCTIONS = INBOUND_GREETING_PATH.read_text()


def _session_clock_context(when: datetime) -> str:
    """Human + ISO lines for the LLM; fixed at job start."""
    local = (
        when.astimezone(SESSION_CLOCK_TZ)
        if when.tzinfo
        else when.replace(tzinfo=SESSION_CLOCK_TZ)
    )
    spoken = local.strftime("%A, %B %d, %Y at %I:%M %p %Z")
    return (
        "# Session clock (reference for scheduling)\n\n"
        f"**Local time when this session started** ({SESSION_CLOCK_TZ.key}): **{spoken}** "
        f"(ISO: {local.isoformat(timespec='seconds')}).\n\n"
        "Treat this as **today** when proposing appointment dates, interpreting phrases like "
        "**“tomorrow”** or **“next week,”** and staying consistent within the call. "
        "This timestamp is from session start, not updated every minute."
    )


def build_system_instructions(
    knowledge: KnowledgeBundle,
    *,
    caller_phone: str | None = None,
    session_started_at: datetime | None = None,
) -> str:
    base = SYSTEM_PROMPT_PATH.read_text()
    if caller_phone:
        line_ctx = (
            "# Inbound line (session fact)\n\n"
            f"The caller ID on this inbound line is **{caller_phone}** (from SIP). "
            "You may read it back digit-by-digit when confirming the callback number, "
            "following the Cartesia spelling-out guidance below. "
            "If the caller says it is wrong, use the number they give instead."
        )
    else:
        line_ctx = (
            "# Inbound line (session fact)\n\n"
            "You do **not** have this caller's phone number on this connection "
            "(e.g. console test, web client, or hidden caller ID per trunk/dispatch rules). "
            "Do **not** say you can see their number or read digits back unless they spoke a number. "
            "Still ask **“Is this the best number to contact you on?”** as in your booking rules."
        )
    clock = session_started_at or datetime.now(SESSION_CLOCK_TZ)
    clock_ctx = _session_clock_context(clock)
    return (
        f"{base.rstrip()}\n\n---\n\n"
        f"{line_ctx}\n\n"
        f"---\n\n"
        f"{clock_ctx}\n\n"
        f"---\n\n"
        f"# Approved FAQ (verbatim when it matches)\n\n{knowledge.faq_markdown}\n\n"
        f"---\n\n"
        f"# Cartesia Sonic-3 TTS (format assistant text for synthesis)\n\n"
        f"{knowledge.cartesia_tts_best_practices_markdown}"
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
        turn_handling=TurnHandlingOptions(turn_detection=EnglishModel()),
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
