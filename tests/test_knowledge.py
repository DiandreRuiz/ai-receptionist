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
    assert jobs == ["Roof Repair", "Roof Replacement"]


def test_unknown_zip_not_served() -> None:
    kb = load_knowledge_dir(KNOWLEDGE_ROOT)
    assert kb.region_for_zip("90210") is None


def test_cartesia_tts_best_practices_packaged() -> None:
    kb = load_knowledge_dir(KNOWLEDGE_ROOT)
    text = kb.cartesia_tts_best_practices_markdown
    assert "Sonic-3" in text
    assert "MM/DD/YYYY" in text


def test_faq_includes_topic_group_sections() -> None:
    kb = load_knowledge_dir(KNOWLEDGE_ROOT)
    text = kb.faq_markdown
    assert "# Roof Installation" in text
    assert "# Roof Repair" in text
    assert "# Roof Inspection" in text
    assert "# Roof Replacement" in text
    assert "# Metal Roof Installation & Repair" in text
    assert "# Flat Roof Installation & Repair" in text


def test_faq_includes_delray_office_facts_no_phone() -> None:
    kb = load_knowledge_dir(KNOWLEDGE_ROOT)
    text = kb.faq_markdown
    assert "772 SW 17th Avenue" in text
    assert "Delray Beach, FL 33444" in text
    assert "Open 24 hours" in text
    assert "CCC1336888" in text
    assert "CCC1329590" in text
    assert "783-5251" not in text
    assert "(561)" not in text
