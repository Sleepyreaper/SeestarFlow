from __future__ import annotations

import csv
import hashlib
import json
import os
import re
import shlex
import shutil
import sqlite3
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from .fits import measure_quality, read_header, read_image


FITS_EXTENSIONS = {".fit", ".fits", ".fts"}


def slug(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9._-]+", "-", value.strip()).strip("-")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _init_db(path: Path) -> sqlite3.Connection:
    connection = sqlite3.connect(path)
    connection.executescript(
        """
        CREATE TABLE IF NOT EXISTS sessions (
          id TEXT PRIMARY KEY, target TEXT, site TEXT, filter_name TEXT,
          mount TEXT, session_path TEXT, created_utc TEXT
        );
        CREATE TABLE IF NOT EXISTS frames (
          hash TEXT PRIMARY KEY, session_id TEXT, filename TEXT, source TEXT,
          date_obs TEXT, exposure REAL, temperature REAL, header_json TEXT,
          FOREIGN KEY(session_id) REFERENCES sessions(id)
        );
        """
    )
    return connection


def discover_frames(source: Path) -> list[Path]:
    candidates = [p for p in source.rglob("*") if p.is_file() and p.suffix.lower() in FITS_EXTENSIONS]
    subframes = [p for p in candidates if any(part.lower().endswith("_sub") for part in p.parts)]
    return sorted(subframes or candidates)


def ingest(
    source: Path,
    library: Path,
    target: str,
    site: str,
    filter_name: str,
    mount: str,
    identity: dict | None = None,
) -> Path:
    frames = discover_frames(source)
    if not frames:
        raise ValueError(f"No FITS frames found below {source}")
    first_header, _ = read_header(frames[0])
    date = str(first_header.get("DATE-OBS", datetime.now().date().isoformat()))[:10]
    session_id = "_".join(map(slug, (date, site, filter_name, mount)))
    session = library / slug(target.upper()) / session_id
    lights = session / "originals"
    lights.mkdir(parents=True, exist_ok=True)
    connection = _init_db(library / "catalog.db")
    connection.execute(
        "INSERT OR IGNORE INTO sessions VALUES (?,?,?,?,?,?,?)",
        (session_id + "_" + slug(target.upper()), target.upper(), site, filter_name, mount, str(session), datetime.now(timezone.utc).isoformat()),
    )
    copied = []
    for frame in frames:
        header, _ = read_header(frame)
        if int(header.get("STACKCNT", 1) or 1) > 1:
            continue
        digest = sha256(frame)
        name = frame.name
        destination = lights / name
        if destination.exists() and sha256(destination) != digest:
            destination = lights / f"{frame.stem}_{digest[:8]}{frame.suffix.lower()}"
        if not destination.exists():
            # Originals must be independent of the source device. A hard link
            # here would allow a later source-side edit to alter the archive.
            shutil.copy2(frame, destination)
            if sha256(destination) != digest:
                destination.unlink(missing_ok=True)
                raise OSError(f"Hash verification failed while copying {frame}")
        connection.execute(
            "INSERT OR IGNORE INTO frames VALUES (?,?,?,?,?,?,?,?)",
            (digest, session_id + "_" + slug(target.upper()), destination.name, str(frame), str(header.get("DATE-OBS", "")),
             float(header.get("EXPTIME", 0) or 0), float(header.get("CCD-TEMP", 0) or 0), json.dumps(header, default=str)),
        )
        copied.append({"file": destination.name, "sha256": digest, "source": str(frame), "header": header})
    connection.commit()
    connection.close()
    public_identity = {
        key: value for key, value in (identity or {}).items()
        if key in {"creator", "copyright_notice", "public_contact"} and value
    }
    manifest = {
        "schema": 2, "target": target.upper(), "site": site, "filter": filter_name, "mount": mount,
        "session_id": session_id, "created_utc": datetime.now(timezone.utc).isoformat(), "frames": copied,
        "identity": public_identity,
    }
    (session / "manifest.json").write_text(json.dumps(manifest, indent=2, default=str), encoding="utf-8")
    return session


def analyze(session: Path, thresholds: dict) -> list[dict]:
    rows = []
    for frame in sorted((session / "originals").iterdir()):
        if frame.suffix.lower() not in FITS_EXTENSIONS:
            continue
        try:
            _, image = read_image(frame)
            quality = measure_quality(image)
            row = {"filename": frame.name, **quality.serializable()}
        except Exception as exc:
            row = {"filename": frame.name, "background": 0, "noise_mad": 0, "star_count": 0,
                   "fwhm_px": 99, "ellipticity": 1, "saturation_fraction": 1, "score": 0,
                   "accepted": False, "reason": f"read-error: {exc}"}
        rows.append(row)
    valid = [r for r in rows if not str(r["reason"]).startswith("read-error")]
    if valid:
        med_fwhm = sorted(r["fwhm_px"] for r in valid)[len(valid) // 2]
        med_bg = sorted(r["background"] for r in valid)[len(valid) // 2]
        for row in valid:
            reasons = []
            if row["star_count"] < thresholds["min_stars"]: reasons.append("few-stars")
            if row["ellipticity"] > thresholds["max_ellipticity"]: reasons.append("trailed")
            if row["fwhm_px"] > med_fwhm * thresholds["max_fwhm_ratio"]: reasons.append("soft-focus")
            if med_bg and row["background"] > med_bg * thresholds["max_background_ratio"]: reasons.append("bright-background")
            row["score"] = round(100.0 * min(1.0, med_fwhm / max(row["fwhm_px"], 1e-6))
                                 * max(0.0, 1.0 - row["ellipticity"]), 2)
            row["accepted"] = not reasons
            row["reason"] = ",".join(reasons)
    fields = ["filename", "background", "noise_mad", "star_count", "fwhm_px", "ellipticity",
              "saturation_fraction", "score", "accepted", "reason"]
    with (session / "quality.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader(); writer.writerows(rows)
    (session / "approved.lst").write_text("\n".join(r["filename"] for r in rows if r["accepted"]) + "\n", encoding="utf-8")
    return rows


def stage(session: Path) -> Path:
    approved_path = session / "approved.lst"
    if not approved_path.exists():
        raise ValueError("Run analyze before stack")
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    work = session / "products" / run_id
    lights = work / "lights"
    lights.mkdir(parents=True)
    for name in approved_path.read_text(encoding="utf-8").splitlines():
        source = session / "originals" / name
        destination = lights / name
        try:
            os.link(source, destination)
        except OSError:
            shutil.copy2(source, destination)
    shutil.copy2(Path(__file__).resolve().parent / "assets" / "SeestarFlow_Preprocess.ssf", work)
    return work


def find_executable(configured: str, names: tuple[str, ...]) -> str | None:
    if configured:
        try:
            if Path(configured).exists():
                return configured
        except OSError:
            # A managed execution sandbox may block probing an otherwise valid
            # per-user installation. The native user process can still run it.
            if Path(configured).is_absolute():
                return configured
    for name in names:
        found = shutil.which(name)
        if found:
            return found
    return None


def stack(session: Path, siril_path: str, dry_run: bool = False) -> tuple[Path, list[str]]:
    work = stage(session)
    executable = find_executable(siril_path, ("siril-cli.exe", "siril-cli", "siril.exe", "siril"))
    command = [executable or "siril-cli", "-d", str(work), "-s", str(work / "SeestarFlow_Preprocess.ssf")]
    if not dry_run:
        if not executable:
            raise FileNotFoundError("Siril was not found. Install it or set tools.siril in config.toml")
        subprocess.run(command, check=True)
        sequence = work / "process" / "r_pp_light_.seq"
        registered = selected = None
        if sequence.exists():
            for line in sequence.read_text(encoding="utf-8", errors="replace").splitlines():
                if line.startswith("S "):
                    fields = shlex.split(line)
                    if len(fields) >= 5:
                        registered = int(fields[3])
                        selected = int(fields[4])
                    break
        input_frames = sum(1 for path in (work / "lights").iterdir() if path.suffix.lower() in FITS_EXTENSIONS)
        report = {
            "schema": 1,
            "input_frames": input_frames,
            "registered_frames": registered,
            "stacked_frames": selected,
            "registration_yield": round(registered / input_frames, 4) if registered is not None and input_frames else None,
            "stack_linear": str(work / "stack_linear.fit"),
            "created_utc": datetime.now(timezone.utc).isoformat(),
        }
        (work / "stack_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    return work, command


def linear_process(
    stack_path: Path,
    graxpert_path: str,
    grax_denoise: bool = False,
    dry_run: bool = False,
) -> tuple[Path, list[list[str]]]:
    """Correct gradients and optionally denoise with GraXpert.

    The paid branch normally leaves denoising disabled here so the same pixels
    are not denoised again by NoiseXTerminator.  ``grax_denoise`` is intended
    for the all-free branch.
    """
    executable = find_executable(graxpert_path, ("GraXpert.exe", "GraXpert-win64.exe", "graxpert"))
    output_dir = stack_path.parent / "linear"
    output_dir.mkdir(exist_ok=True)
    gradient_stem = output_dir / "gradient_corrected"
    denoised_stem = output_dir / "linear_denoised"
    commands = [
        [executable or "GraXpert", str(stack_path), "-cli", "-cmd", "background-extraction",
         "-correction", "Subtraction", "-smoothing", "0.2", "-bg", "-output", str(gradient_stem)],
    ]
    if grax_denoise:
        commands.append(
            [executable or "GraXpert", str(gradient_stem.with_suffix(".fits")), "-cli", "-cmd", "denoising",
             "-strength", "0.4", "-batch_size", "4", "-output", str(denoised_stem)]
        )
    recipe = {
        "schema": 1, "input": str(stack_path), "input_sha256": sha256(stack_path),
        "stage": "linear", "commands": commands, "created_utc": datetime.now(timezone.utc).isoformat(),
        "graxpert_denoise": grax_denoise,
        "handoff": str((denoised_stem if grax_denoise else gradient_stem).with_suffix(".fits")),
        "notes": "Inspect the saved background model before accepting this result. Do not use GraXpert denoise before NoiseXTerminator.",
    }
    (output_dir / "recipe.json").write_text(json.dumps(recipe, indent=2), encoding="utf-8")
    if not dry_run:
        if not executable:
            raise FileNotFoundError("GraXpert was not found. Install it or set tools.graxpert in config.toml")
        for command in commands:
            subprocess.run(command, check=True)
    return output_dir, commands


def premium_process(
    linear_path: Path,
    rc_astro_path: str,
    kind: str,
    star_separate: bool = False,
    dry_run: bool = False,
) -> tuple[Path, list[list[str]]]:
    """Apply the licensed NXT/SXT linear workflow and record exact commands.

    GradientXTerminator and StarShrink are Photoshop plug-ins and therefore
    remain documented human decision gates. BlurXTerminator is a separate
    license and is intentionally not assumed here.
    """
    executable = find_executable(rc_astro_path, ("rc-astro.exe", "rc-astro"))
    output_dir = linear_path.parent / "rcastro"
    output_dir.mkdir(exist_ok=True)
    guidance = {
        "cluster": "Keep stars intact unless a deliberate diagnostic requires separation.",
        "galaxy": "Inspect the core, H-II knots, and compact background galaxies after SXT.",
        "nebula": "Star separation is usually useful; stretch the object and stars independently.",
    }
    commands: list[list[str]] = []
    denoise_input = linear_path
    if star_separate:
        starless = output_dir / "starless_linear.fit"
        commands.append([
            executable or "rc-astro", "sxt", str(linear_path), "-o", str(starless),
            "--stars", "--unscreen=false",
        ])
        denoise_input = starless
    nxt = output_dir / ("starless_nxt_linear.fit" if star_separate else "nxt_linear.fit")
    commands.append([executable or "rc-astro", "nxt", str(denoise_input), "-o", str(nxt)])
    recipe = {
        "schema": 2,
        "input": str(linear_path),
        "input_sha256": sha256(linear_path),
        "stage": "rcastro-linear",
        "kind": kind,
        "star_separate": star_separate,
        "commands": commands,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "notes": (
            "NoiseXTerminator runs exactly once with its current defaults. "
            "When requested, StarXTerminator runs first on linear data with Unscreen disabled. "
            f"{guidance[kind]} Inspect every result at 100%."
        ),
        "photoshop_handoff": (
            "Use GradientXTerminator only as the chosen gradient owner or a proved residual pass; "
            "use masked StarShrink only after recombination when stars overwhelm a non-stellar subject."
        ),
    }
    (output_dir / "recipe.json").write_text(json.dumps(recipe, indent=2), encoding="utf-8")
    if not dry_run:
        if not executable:
            raise FileNotFoundError("RC Astro was not found. Install it or set tools.rc_astro in config.toml")
        for command in commands:
            subprocess.run(command, check=True)
    return output_dir, commands


def estimate_storage(
    exposure_seconds: float,
    hours: float,
    frame_bytes: int = 16_594_560,
    working_overhead: float = 1.25,
) -> dict:
    """Estimate continuous S50 Pro telephoto FITS storage.

    ``frame_bytes`` is the measured size of an early 2160 x 3840 S50 Pro
    telephoto FITS subframe. Monday's commissioning run should replace it with
    the size actually produced by the owner's firmware and capture mode.
    """
    if exposure_seconds <= 0 or hours <= 0 or frame_bytes <= 0 or working_overhead < 1:
        raise ValueError("exposure, hours, frame bytes, and overhead must be positive; overhead must be >= 1")
    frames = int(hours * 3600 // exposure_seconds)
    raw_bytes = frames * frame_bytes
    return {
        "exposure_seconds": exposure_seconds,
        "hours": hours,
        "frames": frames,
        "frame_bytes": frame_bytes,
        "raw_gb": round(raw_bytes / 1_000_000_000, 2),
        "raw_gib": round(raw_bytes / 1024**3, 2),
        "recommended_free_gb": round(raw_bytes * working_overhead / 1_000_000_000, 2),
        "working_overhead": working_overhead,
        "assumption": "continuous telephoto FITS capture; excludes rejected-frame gaps, wide-camera data, previews, and video",
    }


def record_release(
    file_path: Path,
    manifest_path: Path,
    target: str,
    variant: str,
    destination: str = "",
    notes: str = "",
    identity: dict | None = None,
) -> dict:
    """Append an immutable-file fingerprint to a JSONL release ledger."""
    if not file_path.is_file():
        raise FileNotFoundError(file_path)
    allowed = {"proof", "portfolio", "print", "archive"}
    if variant not in allowed:
        raise ValueError(f"variant must be one of {sorted(allowed)}")
    public_identity = {
        key: value for key, value in (identity or {}).items()
        if key in {"creator", "copyright_notice", "public_contact"} and value
    }
    entry = {
        "schema": 1,
        "recorded_utc": datetime.now(timezone.utc).isoformat(),
        "target": target.upper(),
        "variant": variant,
        "filename": file_path.name,
        "path": str(file_path.resolve()),
        "bytes": file_path.stat().st_size,
        "sha256": sha256(file_path),
        "destination": destination,
        "notes": notes,
        "identity": public_identity,
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    with manifest_path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return entry
