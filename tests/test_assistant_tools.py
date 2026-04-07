"""Deterministic tests for Assistant tool stubs (no LLM)."""

from pathlib import Path
from unittest.mock import MagicMock

import pytest

from agent import Assistant
from knowledge.loaders import load_knowledge_dir

KNOWLEDGE_ROOT = Path(__file__).resolve().parent.parent / "src" / "knowledge"


@pytest.fixture
def knowledge():
    return load_knowledge_dir(KNOWLEDGE_ROOT)


@pytest.fixture
def assistant(knowledge):
    return Assistant(knowledge=knowledge)


@pytest.mark.asyncio
async def test_lookup_customer_returns_not_found(assistant: Assistant) -> None:
    ctx = MagicMock()
    out = await assistant.lookup_customer(
        ctx, customer_name="Jane Doe", address="1 Main St", phone="555-0100"
    )
    assert "No matching customer record found" in out
    assert "demo" not in out.lower()
    assert "new customer" in out.lower()


@pytest.mark.asyncio
async def test_get_bookable_jobs_served_zip_plus_four(assistant: Assistant) -> None:
    ctx = MagicMock()
    out = await assistant.get_bookable_jobs(ctx, "33445-1234")
    assert "Delray Beach" in out or "delray" in out.lower()
    assert "Roof Repair" in out
    assert "Roof Installation" in out


@pytest.mark.asyncio
async def test_get_bookable_jobs_palm_beach_gardens_two_types(
    assistant: Assistant,
) -> None:
    ctx = MagicMock()
    out = await assistant.get_bookable_jobs(ctx, "33410")
    assert "Palm Beach Gardens" in out
    assert "Roof Repair" in out
    assert "Roof Installation" in out
    assert "Roof Inspection" not in out


@pytest.mark.asyncio
async def test_get_bookable_jobs_outside_service_area(assistant: Assistant) -> None:
    ctx = MagicMock()
    out = await assistant.get_bookable_jobs(ctx, "90210")
    assert "outside" in out.lower()
    assert "Do not book" in out


@pytest.mark.asyncio
async def test_book_appointment_returns_confirmation(assistant: Assistant) -> None:
    ctx = MagicMock()
    out = await assistant.book_appointment(
        ctx,
        customer_name="Pat Lee",
        address="10 Ocean Dr, Delray Beach FL 33483",
        phone="555-0199",
        job_type="Roof Inspection",
        issue_description="Annual check",
        scheduled_date="Wednesday April 9 2026",
        scheduled_time_window="9 to 11 AM",
    )
    assert "SK-4821" in out
    assert "April" in out
    assert "9" in out and "11" in out


@pytest.mark.asyncio
async def test_cancel_appointment_returns_confirmation(assistant: Assistant) -> None:
    ctx = MagicMock()
    out = await assistant.cancel_appointment(
        ctx,
        customer_name="Pat Lee",
        phone="555-0199",
        confirmation_reference="SK-4821",
        scheduled_date="Wednesday April 9 2026",
        scheduled_time_window="9 to 11 AM",
        reason="Travel conflict",
    )
    assert "SK-C9088" in out
    assert "Pat Lee" in out
    assert "removed" in out.lower() or "cancel" in out.lower()


@pytest.mark.asyncio
async def test_reschedule_appointment_returns_confirmation(assistant: Assistant) -> None:
    ctx = MagicMock()
    out = await assistant.reschedule_appointment(
        ctx,
        customer_name="Pat Lee",
        phone="555-0199",
        original_scheduled_date="Wednesday April 9 2026",
        original_time_window="9 AM to 11 AM",
        new_scheduled_date="Friday April 11 2026",
        new_time_window="1 PM to 3 PM",
        confirmation_reference="SK-4821",
    )
    assert "SK-R7703" in out
    assert "April 9" in out or "April" in out
    assert "April 11" in out or "Moved" in out
