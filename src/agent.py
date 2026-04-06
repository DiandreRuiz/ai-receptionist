import logging
from pathlib import Path

from dotenv import load_dotenv
from livekit import rtc
from livekit.agents import (
    Agent,
    AgentServer,
    AgentSession,
    JobContext,
    JobProcess,
    RunContext,
    cli,
    function_tool,
    inference,
    room_io,
)
from livekit.plugins import noise_cancellation, silero
from livekit.plugins.turn_detector.multilingual import MultilingualModel

from knowledge.loaders import KnowledgeBundle, load_knowledge_dir

logger = logging.getLogger("agent")

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


class Assistant(Agent):
    def __init__(self, knowledge: KnowledgeBundle | None = None) -> None:
        kb = knowledge or load_knowledge_dir(KNOWLEDGE_DIR)
        super().__init__(instructions=build_system_instructions(kb))
        self._knowledge = kb

    async def on_enter(self) -> None:
        self.session.generate_reply(instructions=INBOUND_GREETING_INSTRUCTIONS)

    @function_tool
    async def lookup_customer(
        self,
        context: RunContext,
        customer_name: str,
        address: str | None = None,
        phone: str | None = None,
    ) -> str:
        """Search for an existing customer record (demo mock).

        Args:
            customer_name: The customer's full name.
            address: Service or mailing address if known.
            phone: Phone number if known.
        """
        logger.info(
            "lookup_customer name=%s address=%s phone=%s",
            customer_name,
            address,
            phone,
        )
        return (
            "No matching customer record found (demo). "
            "Proceed as a new customer and capture their details."
        )

    @function_tool
    async def get_bookable_jobs(self, context: RunContext, zip_code: str) -> str:
        """Return bookable job types for the caller's five-digit service ZIP.

        Args:
            zip_code: U.S. ZIP code for the job location (five digits, optional ZIP+4).
        """
        region_id = self._knowledge.region_for_zip(zip_code)
        if region_id is None:
            return (
                "ZIP code is outside SK Quality Roofing's served areas for this demo. "
                "Do not book; politely explain they are outside the service area."
            )
        meta = self._knowledge.regional_jobs.get(region_id) or {}
        label = meta.get("label") or region_id.replace("_", " ").title()
        jobs = self._knowledge.job_types_for_region(region_id)
        lines = ", ".join(jobs)
        return (
            f"Region: {label} ({region_id}). Bookable job types for this ZIP: {lines}."
        )

    @function_tool
    async def book_appointment(
        self,
        context: RunContext,
        customer_name: str,
        address: str,
        phone: str,
        job_type: str,
        issue_description: str,
        scheduled_date: str,
        scheduled_time_window: str,
        email: str | None = None,
        insurance_claim_number: str | None = None,
        notes: str | None = None,
    ) -> str:
        """Create a new appointment (demo mock).

        Args:
            customer_name: Full name of the customer.
            address: Service address for the appointment.
            phone: Callback number.
            job_type: Job category matching get_bookable_jobs.
            issue_description: Plain-language summary for the crew.
            scheduled_date: Selected appointment date.
            scheduled_time_window: Selected window, e.g. morning or nine to eleven A M.
            email: Optional email.
            insurance_claim_number: Optional claim number.
            notes: Optional extra notes.
        """
        logger.info(
            "book_appointment demo name=%s job_type=%s date=%s",
            customer_name,
            job_type,
            scheduled_date,
        )
        _ = (email, insurance_claim_number, notes, issue_description, phone, address)
        return (
            "Appointment confirmed (demo). Reference ST-DEMO-1001. "
            f"{scheduled_date}, {scheduled_time_window}."
        )


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
