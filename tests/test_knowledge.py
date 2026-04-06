"""Unit tests for knowledge loaders and ZIP→region resolution."""

from pathlib import Path

from knowledge.loaders import load_knowledge_dir, normalize_zip

KNOWLEDGE_ROOT = Path(__file__).resolve().parent.parent / "src" / "knowledge"


def test_normalize_zip_strips_zip_plus_four() -> None:
    assert normalize_zip("33445-1234") == "33445"
    assert normalize_zip("  33445  ") == "33445"


def test_normalize_zip_rejects_short() -> None:
    assert normalize_zip("1234") is None
    assert normalize_zip("abcd") is None


def test_region_delray_zip() -> None:
    kb = load_knowledge_dir(KNOWLEDGE_ROOT)
    assert kb.region_for_zip("33444") == "delray_beach"


def test_region_palm_beach_gardens_zip() -> None:
    kb = load_knowledge_dir(KNOWLEDGE_ROOT)
    assert kb.region_for_zip("33410") == "palm_beach_gardens"


def test_region_broward_zip() -> None:
    kb = load_knowledge_dir(KNOWLEDGE_ROOT)
    assert kb.region_for_zip("33301") == "broward_county"


def test_border_zip_deerfield_broward_wins() -> None:
    kb = load_knowledge_dir(KNOWLEDGE_ROOT)
    assert kb.region_for_zip("33441") == "broward_county"


def test_palm_beach_gardens_two_job_types_only() -> None:
    kb = load_knowledge_dir(KNOWLEDGE_ROOT)
    jobs = kb.job_types_for_region("palm_beach_gardens")
    assert jobs == ["Roof Repair", "Roof Installation"]


def test_unknown_zip_not_served() -> None:
    kb = load_knowledge_dir(KNOWLEDGE_ROOT)
    assert kb.region_for_zip("90210") is None


def test_cartesia_tts_best_practices_packaged() -> None:
    kb = load_knowledge_dir(KNOWLEDGE_ROOT)
    text = kb.cartesia_tts_best_practices_markdown
    assert "Sonic-3" in text
    assert "MM/DD/YYYY" in text
