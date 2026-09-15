"""Plan equal-integration selections from explicitly reviewed capture blocks.

This measures acquisition yield, not image quality. Siril integration and matched
linear-image measurements remain required before declaring an exposure winner.
"""
from __future__ import annotations

import csv
import json
import math
from collections import defaultdict
from pathlib import Path

from .fits import read_header
from .pipeline import sha256


def _resolve(base: Path, value: str) -> Path:
    path = Path(value)
    return (path if path.is_absolute() else base / path).resolve()


def _evenly_spaced(items: list, count: int) -> list:
    # Deterministic selection across the entire time span, without brightness bias.
    return [items[min(len(items) - 1, int((i + 0.5) * len(items) / count))]
            for i in range(count)] if count else []


def compare_captures(spec_path: Path, output: Path) -> dict:
    if output.exists():
        raise FileExistsError("Use a new report folder; existing comparisons are preserved")
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    blocks = spec["blocks"]
    if len(blocks) < 2:
        raise ValueError("Supply at least two capture blocks")
    groups = defaultdict(list)
    rows, warnings, seen, signatures, ids = [], set(), set(), set(), set()
    for block in blocks:
        block_id = str(block["id"])
        if block_id in ids:
            raise ValueError("Duplicate block id")
        ids.add(block_id)
        exposure = float(block["exposure_seconds"])
        wall = float(block["wall_seconds"])
        mount = block["mount"]
        if exposure not in {10, 20, 30, 60} or mount not in {"eq", "altaz"}:
            raise ValueError("Expected 10/20/30/60 seconds and eq/altaz")
        if not math.isfinite(wall) or wall <= 0 or (mount == "altaz" and exposure == 60):
            raise ValueError("Invalid duration or 60-second Alt-Az block")
        source = _resolve(spec_path.parent, block["source"])
        approved = _resolve(spec_path.parent, block["approved_list"])
        approved_names = approved.read_text(encoding="utf-8").splitlines()
        approved_names = [name.strip() for name in approved_names if name.strip()]
        if len(approved_names) != len(set(approved_names)):
            raise ValueError("Duplicate filename in approved list")
        frames = sorted(p for p in source.iterdir()
                        if p.is_file() and p.suffix.lower() in {".fit", ".fits", ".fts"})
        names = {p.name for p in frames}
        if set(approved_names) - names:
            raise ValueError(f"Approved list references missing files in {block_id}")
        accepted = []
        total_bytes = 0
        for frame in frames:
            header, offset = read_header(frame)
            if int(header.get("STACKCNT", 1)) != 1 or int(header.get("NAXIS", 0)) != 2:
                raise ValueError(f"Expected individual 2-D sub, found master/layout: {frame.name}")
            if not math.isclose(float(header.get("EXPTIME", -1)), exposure):
                raise ValueError(f"Exposure mismatch: {frame.name}")
            dims = (int(header["NAXIS1"]), int(header["NAXIS2"]))
            bitpix = int(header["BITPIX"])
            if bitpix not in {8, 16, 32, -32, -64} or min(dims) <= 0:
                raise ValueError(f"Unsupported pixels: {frame.name}")
            size = frame.stat().st_size
            if size < offset + math.prod(dims) * abs(bitpix) // 8:
                raise ValueError(f"Truncated FITS: {frame.name}")
            signature = []
            for key in ("OBJECT", "FILTER", "INSTRUME", "GAIN", "FOCALLEN", "BAYERPAT"):
                value = header.get(key)
                if value is None:
                    warnings.add(f"Missing {key}: check capture log before claiming matched conditions")
                signature.append(str(value).strip().upper())
            signatures.add((*signature, *dims, bitpix))
            mode = header.get("EQMODE")
            if mode is None:
                warnings.add("EQMODE missing: mount labels rely on the observer's log")
            elif str(mode).upper() not in {"0", "1", "FALSE", "TRUE"}:
                raise ValueError(f"Unknown EQMODE: {frame.name}")
            elif (str(mode).upper() in {"1", "TRUE"}) != (mount == "eq"):
                raise ValueError(f"Mount/header mismatch: {frame.name}")
            digest = sha256(frame)
            if digest in seen:
                raise ValueError(f"Duplicate photons across blocks: {frame.name}")
            seen.add(digest)
            total_bytes += size
            if frame.name in approved_names:
                if not header.get("DATE-OBS"):
                    warnings.add("DATE-OBS missing: selection order uses filenames; verify block chronology")
                accepted.append({"path": str(frame), "sha256": digest,
                                 "date_obs": str(header.get("DATE-OBS", "")),
                                 "block": block_id})
        if len(frames) * exposure > wall + 1e-6:
            raise ValueError(f"Saved integration exceeds logged clock time in {block_id}")
        key = f"{mount}_{int(exposure)}s"
        groups[key].extend(accepted)
        rows.append({"block": block_id, "group": key, "exposure_seconds": exposure,
                     "wall_seconds": wall, "saved_frames": len(frames),
                     "qa_frames": len(accepted), "qa_seconds": len(accepted) * exposure,
                     "saved_bytes": total_bytes})
    if len(signatures) != 1:
        raise ValueError("Target/filter/camera/gain/geometry differs: use a separate experiment")
    if len(groups) < 2:
        raise ValueError("Need at least two mount/exposure combinations")
    exposures = {row["group"]: int(row["exposure_seconds"]) for row in rows}
    quantum = math.lcm(*exposures.values())
    common = int(min(len(frames) * exposures[key] for key, frames in groups.items()) // quantum) * quantum
    if common == 0:
        raise ValueError("Insufficient QA-approved integration for an equal-time pair")
    summaries, selections = [], {}
    for key, frames in sorted(groups.items()):
        relevant = [row for row in rows if row["group"] == key]
        wall = sum(row["wall_seconds"] for row in relevant)
        saved = sum(row["saved_frames"] for row in relevant)
        seconds = len(frames) * exposures[key]
        frames.sort(key=lambda frame: (frame["date_obs"], frame["path"]))
        selections[key] = {
            "all_qa_approved": frames,
            "equal_integration": _evenly_spaced(frames, common // exposures[key]),
        }
        summaries.append({"group": key, "wall_seconds": wall, "saved_frames": saved,
                          "qa_frames": len(frames), "qa_seconds": seconds,
                          "qa_retention_of_saved": len(frames) / saved if saved else None,
                          "qa_minutes_per_clock_hour": seconds / wall * 60,
                          "saved_bytes": sum(row["saved_bytes"] for row in relevant)})
    if len({item["wall_seconds"] for item in summaries}) != 1:
        warnings.add("Group clock times differ: throughput is normalized; image stacks are not equal-clock")
    report = {"schema": 1, "status": "selection-ready; final-stack image comparison pending",
              "equal_input_integration_seconds": common, "groups": summaries,
              "blocks": rows, "warnings": sorted(warnings), "selections": selections,
              "limitations": ["QA approval is not Siril registration or integration acceptance.",
                              "Saved files may omit camera-rejected frames; no attempted-frame rejection rate inferred.",
                              "No image-quality or signal-to-noise winner is inferred from throughput.",
                              "Recheck equal integration after final Siril rejection."]}
    output.mkdir(parents=True, exist_ok=False)
    (output / "report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    with (output / "throughput.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(summaries[0]))
        writer.writeheader()
        writer.writerows(summaries)
    for key, selection in selections.items():
        for label, frames in selection.items():
            (output / f"{key}_{label}.lst").write_text(
                "\n".join(frame["path"] for frame in frames) + "\n", encoding="utf-8")
    return report
