"""Latency checks: local instruction assembly vs. pipeline metrics (LLM TTFT).

Local tests are deterministic. The async test calls the hosted inference API
(same stack as other ``test_agent`` / ``test_faq_utterances`` LLM tests).
"""

from __future__ import annotations

import time

import pytest
from livekit.agents import Agent, AgentSession, inference, llm

from agent import KNOWLEDGE_DIR, build_system_instructions
from knowledge.loaders import load_knowledge_dir

# Generous ceilings for cold CI / slow disks.
_LOAD_KNOWLEDGE_MAX_S = 3.0
_BUILD_INSTRUCTIONS_MAX_S = 5.0

# Upper bound for LLM time-to-first-token in tests (network variance); not a production SLO.
_LLM_TTFT_TEST_MAX_S = 90.0


class _InstructionsOnlyAssistant(Agent):
    """Full system instructions, no tools, no ``on_enter`` greeting — one assistant reply per run."""

    def __init__(self) -> None:
        kb = load_knowledge_dir(KNOWLEDGE_DIR)
        super().__init__(instructions=build_system_instructions(kb))


def _llm() -> llm.LLM:
    return inference.LLM(model="openai/gpt-4.1-mini")


def test_load_knowledge_dir_completes_within_budget() -> None:
    t0 = time.perf_counter()
    load_knowledge_dir(KNOWLEDGE_DIR)
    assert time.perf_counter() - t0 < _LOAD_KNOWLEDGE_MAX_S


def test_build_system_instructions_completes_within_budget() -> None:
    kb = load_knowledge_dir(KNOWLEDGE_DIR)
    t0 = time.perf_counter()
    build_system_instructions(kb)
    assert time.perf_counter() - t0 < _BUILD_INSTRUCTIONS_MAX_S


@pytest.mark.asyncio
async def test_text_session_records_llm_ttft_for_assistant_reply() -> None:
    """LiveKit records ``llm_node_ttft`` on assistant ``ChatMessage.metrics`` (see MetricsReport)."""
    async with (
        _llm() as llm_model,
        AgentSession(llm=llm_model) as session,
    ):
        await session.start(_InstructionsOnlyAssistant())
        result = await session.run(
            user_input='Reply with exactly the word "ok" and nothing else.',
        )
        await result

    assistant_msgs = [
        e.item
        for e in result.events
        if e.type == "message" and e.item.role == "assistant"
    ]
    assert assistant_msgs, "expected at least one assistant message"

    metrics = assistant_msgs[-1].metrics
    assert metrics is not None, "assistant message should carry a metrics dict"
    ttft = metrics.get("llm_node_ttft")
    assert ttft is not None, "expected llm_node_ttft on assistant message"
    assert isinstance(ttft, int | float)
    assert 0.0 < ttft < _LLM_TTFT_TEST_MAX_S
