"""Load FAQ, regional job menus, and ZIP→region mappings from packaged assets."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

# After palm_beach_county and broward_county base layers, these override in order (last wins).
_CITY_OVERLAY_ORDER: tuple[str, ...] = (
    "delray_beach",
    "boynton_beach",
    "west_palm_beach",
    "boca_raton",
    "palm_beach_gardens",
)


@dataclass(frozen=True)
class KnowledgeBundle:
    faq_markdown: str
    regional_jobs: dict[str, dict[str, Any]]
    zip_to_region: dict[str, str]

    def job_types_for_region(self, region_id: str) -> list[str]:
        reg = self.regional_jobs.get(region_id) or {}
        raw = reg.get("job_types") or []
        if not isinstance(raw, list):
            return []
        return [str(x) for x in raw]

    def region_for_zip(self, zip_input: str) -> str | None:
        z = normalize_zip(zip_input)
        if z is None:
            return None
        return self.zip_to_region.get(z)


def normalize_zip(zip_input: str) -> str | None:
    digits = re.sub(r"\D", "", zip_input.strip())
    if len(digits) < 5:
        return None
    return digits[:5]


def _flatten_zip_regions(regions: dict[str, list[str]]) -> dict[str, str]:
    """Build zip5 → region_id with county base + Broward + city overlays."""
    out: dict[str, str] = {}
    pbc = regions.get("palm_beach_county") or []
    for z in pbc:
        z5 = normalize_zip(z)
        if z5:
            out[z5] = "palm_beach_county"
    broward = regions.get("broward_county") or []
    for z in broward:
        z5 = normalize_zip(z)
        if z5:
            out[z5] = "broward_county"
    for rid in _CITY_OVERLAY_ORDER:
        for z in regions.get(rid) or []:
            z5 = normalize_zip(z)
            if z5:
                out[z5] = rid
    return out


def load_serviceable_zips(path: Path) -> dict[str, str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    regions = data.get("regions")
    if not isinstance(regions, dict):
        msg = "serviceable_zips.json: missing object 'regions'"
        raise ValueError(msg)
    typed: dict[str, list[str]] = {}
    for k, v in regions.items():
        if not isinstance(k, str):
            continue
        if isinstance(v, list) and all(isinstance(x, str) for x in v):
            typed[k] = v
        else:
            msg = f"serviceable_zips.json: regions['{k}'] must be a list of strings"
            raise ValueError(msg)
    return _flatten_zip_regions(typed)


def load_regional_jobs(path: Path) -> dict[str, dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    regions = data.get("regions")
    if not isinstance(regions, dict):
        msg = "regional_jobs.json: missing object 'regions'"
        raise ValueError(msg)
    for rid, payload in regions.items():
        if not isinstance(rid, str) or not isinstance(payload, dict):
            msg = f"regional_jobs.json: bad entry for {rid!r}"
            raise ValueError(msg)
        jt = payload.get("job_types")
        if not isinstance(jt, list) or not all(isinstance(x, str) for x in jt):
            msg = f"regional_jobs.json: regions['{rid}'].job_types must be a list of strings"
            raise ValueError(msg)
    return regions  # type: ignore[return-value]


def load_faq(path: Path) -> str:
    return path.read_text(encoding="utf-8").strip()


def load_knowledge_dir(root: Path) -> KnowledgeBundle:
    faq = load_faq(root / "faq.md")
    regional = load_regional_jobs(root / "regional_jobs.json")
    zip_map = load_serviceable_zips(root / "serviceable_zips.json")
    return KnowledgeBundle(
        faq_markdown=faq,
        regional_jobs=regional,
        zip_to_region=zip_map,
    )
