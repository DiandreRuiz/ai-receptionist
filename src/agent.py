from pathlib import Path

from dotenv import load_dotenv
from livekit import rtc
from livekit.agents import (
    Agent,
    AgentServer,
    AgentSession,
    JobContext,
    JobProcess,
    cli,
    inference,
    room_io,
)
from livekit.plugins import noise_cancellation, silero
from livekit.plugins.turn_detector.multilingual import MultilingualModel

from knowledge.loaders import KnowledgeBundle, load_knowledge_dir
from tools import ReceptionistTools

load_dotenv(".env.local")

PROMPTS_DIR = Path(__file__).parent / "prompts"
SYSTEM_PROMPT_PATH = PROMPTS_DIR / "receptionist_system_prompt.md"
INBOUND_GREETING_PATH = PROMPTS_DIR / "greeting.md"
KNOWLEDGE_DIR = Path(__file__).resolve().parent / "knowledge"

INBOUND_GREETING_INSTRUCTIONS = INBOUND_GREETING_PATH.read_text()


def build_system_instructions(knowledge: KnowledgeBundle) -> str:
    base = SYSTEM_PROMPT_PATH.read_text()
    return (
        f"{base.rstrip()}\n\n---\n\n"
        f"# Approved FAQ (verbatim when it matches)\n\n{knowledge.faq_markdown}"
    )


class Assistant(ReceptionistTools, Agent):
    def __init__(self, knowledge: KnowledgeBundle | None = None) -> None:
        kb = knowledge or load_knowledge_dir(KNOWLEDGE_DIR)
        super().__init__(instructions=build_system_instructions(kb))
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

    session = AgentSession(
        stt=inference.STT(model="deepgram/nova-3", language="multi"),
        llm=inference.LLM(model="openai/gpt-4o"),
        tts=inference.TTS(
            model="cartesia/sonic-3", voice="9626c31c-bec5-4cca-baa8-f8ba9e84c8bc"
        ),
        turn_detection=MultilingualModel(),
        vad=ctx.proc.userdata["vad"],
        preemptive_generation=True,
    )

    await session.start(
        agent=Assistant(knowledge=knowledge),
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
