#!/usr/bin/env python3
"""Token counts for the assembled system instructions (OpenAI gpt-4o tokenizer).

Production LLM in src/agent.py: inference.LLM(model="openai/gpt-4o").
Uses tiktoken's encoding for gpt-4o (o200k_base). Counts are for the **system**
instruction string from build_system_instructions only—each user/assistant turn
adds more. LiveKit also attaches **tool schemas** (not counted here); expect a
few hundred extra tokens for those.

Run from repo root:  uv run python scripts/count_prompt_tokens.py
"""

from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import tiktoken

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from agent import (  # noqa: E402
    KNOWLEDGE_DIR,
    SYSTEM_PROMPT_PATH,
    _inbound_line_body,
    _session_clock_body,
    build_system_instructions,
)
from knowledge.loaders import load_knowledge_dir  # noqa: E402

MODEL_LABEL = "openai/gpt-4o"
ENCODING = tiktoken.encoding_for_model("gpt-4o")


def _tok(s: str) -> int:
    return len(ENCODING.encode(s))


def main() -> None:
    kb = load_knowledge_dir(KNOWLEDGE_DIR)
    fixed = datetime(2026, 4, 6, 14, 30, tzinfo=ZoneInfo("America/New_York"))
    session_clock_tz = ZoneInfo("America/New_York")

    base = SYSTEM_PROMPT_PATH.read_text(encoding="utf-8").rstrip()
    clock_body = _session_clock_body(fixed, session_clock_tz)
    line_no = _inbound_line_body(None)
    line_yes = _inbound_line_body("+15615551234")
    faq = kb.faq_markdown.strip()
    cartesia = kb.cartesia_tts_best_practices_markdown.strip()

    full_no = build_system_instructions(kb, caller_phone=None, session_started_at=fixed)
    full_yes = build_system_instructions(
        kb, caller_phone="+15615551234", session_started_at=fixed
    )

    # Monolith map, ## A-D headings, and assembly --- dividers (not split out; base .md has its own --- lines).
    assembly_overhead = (
        _tok(full_no)
        - _tok(base)
        - _tok(line_no)
        - _tok(clock_body)
        - _tok(faq)
        - _tok(cartesia)
    )

    print(f"Tokenizer: tiktoken for {MODEL_LABEL} ({ENCODING.name})")
    print()
    print(f"{'Component':<44} {'tokens':>10}")
    print(f"{'receptionist_system_prompt.md':<44} {_tok(base):>10,}")
    print(f"{'faq.md (block C body)':<44} {_tok(faq):>10,}")
    print(f"{'cartesia_tts_best_practices.md (block D)':<44} {_tok(cartesia):>10,}")
    print(f"{'Session clock body (block B)':<44} {_tok(clock_body):>10,}")
    print(f"{'Inbound line — no caller ID (block A)':<44} {_tok(line_no):>10,}")
    print(f"{'Inbound line — +1 sample SIP (block A)':<44} {_tok(line_yes):>10,}")
    print(f"{'Index + block headings + assembly dividers':<44} {assembly_overhead:>10,}")
    print()
    print("Full system instructions (matches build_system_instructions):")
    print(f"  {'No caller_id':<22} {_tok(full_no):>10,} tokens")
    print(f"  {'With sample SIP':<22} {_tok(full_yes):>10,} tokens")
    print()
    print("gpt-4o context window (typical): 128,000 tokens combined input+output.")
    print(
        "Add: user/assistant history, audio-derived text, and tool definitions per request."
    )

    tools_src = (SRC / "tools.py").read_text(encoding="utf-8")
    print()
    print(
        f"For scale: tokenizing all of src/tools.py as raw text = {_tok(tools_src):,} tokens "
        "(API tool JSON is related but not identical)."
    )


if __name__ == "__main__":
    main()
