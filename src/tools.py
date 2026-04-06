"""Demo receptionist function tools (ServiceTitan-shaped stubs)."""

from __future__ import annotations

import logging

from livekit.agents import RunContext, function_tool

logger = logging.getLogger(__name__)


class ReceptionistTools:
    """Mixin providing @function_tool methods; expects ``_knowledge`` on the agent instance."""

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
