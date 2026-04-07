"""Receptionist function tools (ServiceTitan-shaped stubs for development)."""

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
        """Search for an existing customer record.

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
            "No matching customer record found. "
            "Proceed as a new customer and capture their details. "
            "Do not state that we are treating this as a new customer."
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
                "ZIP code is outside SK Quality Roofing's served areas. "
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
        """Create a new appointment in scheduling.

        Args:
            customer_name: Full name of the customer.
            address: Service address for the appointment.
            phone: Confirmed callback number (caller's line or alternate they gave).
            job_type: Job category matching get_bookable_jobs.
            issue_description: Plain-language summary for the crew.
            scheduled_date: Selected date including weekday when possible (e.g. Wednesday April 5 2026).
            scheduled_time_window: Selected window, e.g. nine A M to eleven A M.
            email: Not collected from callers; pass None.
            insurance_claim_number: Optional claim number.
            notes: Optional extra notes.
        """
        logger.info(
            "book_appointment name=%s job_type=%s date=%s",
            customer_name,
            job_type,
            scheduled_date,
        )
        _ = (email, insurance_claim_number, notes, issue_description, phone, address)
        return (
            "Appointment confirmed. Confirmation reference SK-4821. "
            f"{scheduled_date}, {scheduled_time_window}."
        )

    @function_tool
    async def cancel_appointment(
        self,
        context: RunContext,
        customer_name: str,
        phone: str,
        scheduled_date: str,
        scheduled_time_window: str,
        confirmation_reference: str | None = None,
        reason: str | None = None,
    ) -> str:
        """Cancel an existing scheduled visit (stub: always succeeds).

        Demo: the assistant always passes the fixed "tomorrow" slot it stated aloud
        (roof repair, nine A M to eleven A M)—never values collected from the caller.
        """
        logger.info(
            "cancel_appointment name=%s phone=%s ref=%s date=%s",
            customer_name,
            phone,
            confirmation_reference,
            scheduled_date,
        )
        _ = (reason, scheduled_date, scheduled_time_window)
        ref = confirmation_reference or "on file"
        return (
            "Cancellation confirmed. Reference SK-C9088. "
            f"The roof repair visit for {customer_name} on {scheduled_date}, "
            f"{scheduled_time_window}, has been removed from the schedule "
            f"(confirmation {ref})."
        )

    @function_tool
    async def reschedule_appointment(
        self,
        context: RunContext,
        customer_name: str,
        phone: str,
        original_scheduled_date: str,
        original_time_window: str,
        new_scheduled_date: str,
        new_time_window: str,
        confirmation_reference: str | None = None,
        address: str | None = None,
        notes: str | None = None,
    ) -> str:
        """Reschedule an existing visit to a new date and window (stub: always succeeds).

        Demo: original_* must always be the assistant's fixed "tomorrow" roof-repair
        slot (nine A M to eleven A M) that was stated aloud—not caller-supplied times.
        """
        logger.info(
            "reschedule_appointment name=%s orig=%s new=%s",
            customer_name,
            original_scheduled_date,
            new_scheduled_date,
        )
        _ = (address, notes, confirmation_reference)
        return (
            "Reschedule confirmed. Reference SK-R7703. "
            f"Roof repair moved from {original_scheduled_date}, {original_time_window} "
            f"to {new_scheduled_date}, {new_time_window}."
        )
