"""
LLM judge tests: caller questions aligned to headings in src/knowledge/faq.md.

Each test asserts the assistant conveys the approved FAQ facts (spoken form OK).
"""

import pytest
from livekit.agents import AgentSession, inference, llm

from agent import Assistant


def _llm() -> llm.LLM:
    return inference.LLM(model="openai/gpt-4.1-mini")


@pytest.mark.asyncio
async def test_faq_contractor_services_scope() -> None:
    async with (
        _llm() as llm,
        AgentSession(llm=llm) as session,
    ):
        await session.start(Assistant())
        result = await session.run(
            user_input="In general, what does a roofing contractor help homeowners with?"
        )
        await (
            result.expect.next_event()
            .is_message(role="assistant")
            .judge(
                llm,
                intent="""
                The answer follows the approved FAQ idea that contractors handle
                roof installation, repair, maintenance, and inspection, and may
                mention common materials such as asphalt shingles, metal, tile,
                or flat systems. It may mention replacements or emergency work.
                """,
            )
        )
        result.expect.no_more_events()


@pytest.mark.asyncio
async def test_faq_roof_installation_steps() -> None:
    async with (
        _llm() as llm,
        AgentSession(llm=llm) as session,
    ):
        await session.start(Assistant())
        result = await session.run(
            user_input="What is usually involved in a roof installation project?"
        )
        await (
            result.expect.next_event()
            .is_message(role="assistant")
            .judge(
                llm,
                intent="""
                The answer matches the FAQ: removing old roofing when needed,
                deck repairs, underlayment, new roof covering, flashing and
                ventilation, and sealing for leaks—depending on material and home.
                """,
            )
        )
        result.expect.no_more_events()


@pytest.mark.asyncio
async def test_faq_how_to_choose_contractor() -> None:
    async with (
        _llm() as llm,
        AgentSession(llm=llm) as session,
    ):
        await session.start(Assistant())
        result = await session.run(
            user_input="How should I go about choosing a roofing contractor?"
        )
        await (
            result.expect.next_event()
            .is_message(role="assistant")
            .judge(
                llm,
                intent="""
                The answer aligns with the FAQ: look for experience, licensing
                and insurance, reviews, references, written estimates, comparing
                more than one quote, and reading the contract before signing.
                """,
            )
        )
        result.expect.no_more_events()


@pytest.mark.asyncio
async def test_faq_sk_licensed_florida_no_unsolicited_license_number() -> None:
    async with (
        _llm() as llm,
        AgentSession(llm=llm) as session,
    ):
        await session.start(Assistant())
        result = await session.run(
            user_input="Is SK Quality Roofing a licensed roofing contractor?"
        )
        await (
            result.expect.next_event()
            .is_message(role="assistant")
            .judge(
                llm,
                intent="""
                The answer confirms SK is licensed and insured in Florida (or
                equivalent wording per FAQ). The caller did not ask for a
                license number, so the response must NOT read a long numeric
                license string aloud.
                """,
            )
        )
        result.expect.no_more_events()


@pytest.mark.asyncio
async def test_faq_inspection_frequency() -> None:
    async with (
        _llm() as llm,
        AgentSession(llm=llm) as session,
    ):
        await session.start(Assistant())
        result = await session.run(
            user_input="How often should I have my roof inspected?"
        )
        await (
            result.expect.next_event()
            .is_message(role="assistant")
            .judge(
                llm,
                intent="""
                The answer matches the FAQ: many professionals suggest about once
                a year and after major storms, and that regular checks catch
                small problems early.
                """,
            )
        )
        result.expect.no_more_events()


@pytest.mark.asyncio
async def test_faq_signs_roof_needs_repair() -> None:
    async with (
        _llm() as llm,
        AgentSession(llm=llm) as session,
    ):
        await session.start(Assistant())
        result = await session.run(
            user_input="What are some warning signs that my roof might need repairs?"
        )
        await (
            result.expect.next_event()
            .is_message(role="assistant")
            .judge(
                llm,
                intent="""
                The answer includes several FAQ themes: missing or damaged
                shingles, ceiling stains or leaks, sagging, higher energy bills,
                wear around chimneys or vents, and that a professional should
                take a look.
                """,
            )
        )
        result.expect.no_more_events()


@pytest.mark.asyncio
async def test_faq_replacement_cost_education_not_quote() -> None:
    async with (
        _llm() as llm,
        AgentSession(llm=llm) as session,
    ):
        await session.start(Assistant())
        result = await session.run(
            user_input="Roughly how much does a typical home roof replacement cost?"
        )
        await (
            result.expect.next_event()
            .is_message(role="assistant")
            .judge(
                llm,
                intent="""
                The answer matches the FAQ: a wide national range often around
                five thousand to fifteen thousand dollars or more depending on
                factors, framed as general education—not the caller's price.
                It should steer them to a free on-site estimate from SK for
                their specific roof.
                """,
            )
        )
        result.expect.no_more_events()


@pytest.mark.asyncio
async def test_faq_diy_roof_repair_risk() -> None:
    async with (
        _llm() as llm,
        AgentSession(llm=llm) as session,
    ):
        await session.start(Assistant())
        result = await session.run(user_input="Can I safely do roof repairs myself?")
        await (
            result.expect.next_event()
            .is_message(role="assistant")
            .judge(
                llm,
                intent="""
                The answer matches the FAQ: small tasks might be possible for
                some people, but roofing is dangerous and mistakes can worsen
                problems; most work should be done by a qualified professional.
                """,
            )
        )
        result.expect.no_more_events()


@pytest.mark.asyncio
async def test_faq_roof_lifespan_by_material() -> None:
    async with (
        _llm() as llm,
        AgentSession(llm=llm) as session,
    ):
        await session.start(Assistant())
        result = await session.run(
            user_input="How long do different kinds of roofs usually last?"
        )
        await (
            result.expect.next_event()
            .is_message(role="assistant")
            .judge(
                llm,
                intent="""
                The answer matches the FAQ: lifespan depends on material and
                quality; asphalt shingles often roughly twenty to thirty years,
                metal often lasts decades longer, tile can last around fifty
                years or more with care, and maintenance matters.
                """,
            )
        )
        result.expect.no_more_events()


@pytest.mark.asyncio
async def test_faq_florida_common_materials() -> None:
    async with (
        _llm() as llm,
        AgentSession(llm=llm) as session,
    ):
        await session.start(Assistant())
        result = await session.run(
            user_input="What roofing materials are common on Florida homes?"
        )
        await (
            result.expect.next_event()
            .is_message(role="assistant")
            .judge(
                llm,
                intent="""
                The answer matches the FAQ: asphalt shingles, tile, and metal
                are common; flat or low-slope areas may use membranes suited to
                the climate; an estimator can recommend for wind, sun, and
                humidity.
                """,
            )
        )
        result.expect.no_more_events()


@pytest.mark.asyncio
async def test_faq_storm_damage_get_checked() -> None:
    async with (
        _llm() as llm,
        AgentSession(llm=llm) as session,
    ):
        await session.start(Assistant())
        result = await session.run(
            user_input="After a bad storm, should I worry if I do not see damage from the ground?"
        )
        await (
            result.expect.next_event()
            .is_message(role="assistant")
            .judge(
                llm,
                intent="""
                The answer matches the FAQ core: after bad weather it is smart to
                have the roof checked even without obvious ground-level damage
                (hidden issues may exist). It should encourage a professional
                inspection rather than the homeowner climbing on the roof, or
                mention documenting what you see safely from the ground—at
                least one of those safety themes should appear.
                """,
            )
        )
        result.expect.no_more_events()


@pytest.mark.asyncio
async def test_faq_insurance_coverage_only_insurer_confirms() -> None:
    async with (
        _llm() as llm,
        AgentSession(llm=llm) as session,
    ):
        await session.start(Assistant())
        result = await session.run(
            user_input="Does homeowners insurance usually cover storm damage to the roof?"
        )
        await (
            result.expect.next_event()
            .is_message(role="assistant")
            .judge(
                llm,
                intent="""
                The answer matches the FAQ: only their insurance company can
                confirm coverage; the agent may mention noting a claim number and
                scheduling an inspection to document conditions. It must NOT
                guarantee coverage or act as an insurance advisor.
                """,
            )
        )
        result.expect.no_more_events()


@pytest.mark.asyncio
async def test_faq_reduce_leaks_maintenance() -> None:
    async with (
        _llm() as llm,
        AgentSession(llm=llm) as session,
    ):
        await session.start(Assistant())
        result = await session.run(
            user_input="What can homeowners do to help reduce the chance of roof leaks?"
        )
        await (
            result.expect.next_event()
            .is_message(role="assistant")
            .judge(
                llm,
                intent="""
                The answer matches the FAQ: keep gutters clear, fix flashing
                promptly, address missing or lifted shingles, and if water is
                entering the home treat it as urgent and get professional help.
                """,
            )
        )
        result.expect.no_more_events()


@pytest.mark.asyncio
async def test_faq_metal_roofing_benefits() -> None:
    async with (
        _llm() as llm,
        AgentSession(llm=llm) as session,
    ):
        await session.start(Assistant())
        result = await session.run(
            user_input="What are the benefits of metal roofing for a house?"
        )
        await (
            result.expect.next_event()
            .is_message(role="assistant")
            .judge(
                llm,
                intent="""
                The answer matches the FAQ: metal can be durable and long-lasting
                and may perform well in harsh weather; whether it is right
                depends on structure, style, and budget, and an on-site visit
                is the right place to decide—not a hard sell for metal.
                """,
            )
        )
        result.expect.no_more_events()


@pytest.mark.asyncio
async def test_faq_florida_roof_installation_typical_duration() -> None:
    async with (
        _llm() as llm,
        AgentSession(llm=llm) as session,
    ):
        await session.start(Assistant())
        result = await session.run(
            user_input="If I'm in Florida, roughly how many days does a normal house roof installation usually take?"
        )
        await (
            result.expect.next_event()
            .is_message(role="assistant")
            .judge(
                llm,
                intent="""
                The answer reflects the FAQ: often on the order of about two to
                five days for a typical home, with weather and extra repairs as
                factors that can extend it. It should stay general—not a promise
                for this caller's job.
                """,
            )
        )
        result.expect.no_more_events()


@pytest.mark.asyncio
async def test_faq_flat_roof_drainage_focus() -> None:
    async with (
        _llm() as llm,
        AgentSession(llm=llm) as session,
    ):
        await session.start(Assistant())
        result = await session.run(
            user_input="What is the big thing to get right with a flat roof in Florida when it rains a lot?"
        )
        await (
            result.expect.next_event()
            .is_message(role="assistant")
            .judge(
                llm,
                intent="""
                The answer matches the FAQ theme: drainage is critical—water does
                not shed like a steep roof; keeping drains, scuppers, or gutters
                clear and proper installation matters; ponding or failed seams
                increase risk. It should not guarantee the caller's roof type.
                """,
            )
        )
        result.expect.no_more_events()


@pytest.mark.asyncio
async def test_faq_metal_roof_noise_and_lightning_myths() -> None:
    async with (
        _llm() as llm,
        AgentSession(llm=llm) as session,
    ):
        await session.start(Assistant())
        result = await session.run(
            user_input="I'm worried metal roofing will be super loud in the rain and attract lightning—is that true?"
        )
        await (
            result.expect.next_event()
            .is_message(role="assistant")
            .judge(
                llm,
                intent="""
                The answer should debunk the lightning myth: metal does not
                attract lightning. For rain noise, it should reflect the FAQ idea
                that with proper decking and insulation or underlayment, modern
                metal roofs are usually not noticeably louder than other roofs.
                """,
            )
        )
        result.expect.no_more_events()


@pytest.mark.asyncio
async def test_faq_delray_office_address_hours_no_phone() -> None:
    async with (
        _llm() as llm,
        AgentSession(llm=llm) as session,
    ):
        await session.start(Assistant())
        result = await session.run(
            user_input="What's the address of your Delray Beach office and what are your hours there?"
        )
        await (
            result.expect.next_event()
            .is_message(role="assistant")
            .judge(
                llm,
                intent="""
                The answer includes the FAQ facts: roughly 772 SW 17th Avenue
                (or Southwest Seventeenth Avenue), Delray Beach, Florida 33444,
                and that the office is open twenty-four hours or around the
                clock. It must NOT give a telephone number (none is in the FAQ).
                """,
            )
        )
        result.expect.no_more_events()
