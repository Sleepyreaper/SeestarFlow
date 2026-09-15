from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

from .config import ROOT, load_config, resolve_library
from .pipeline import (
    analyze,
    estimate_storage,
    find_executable,
    ingest,
    linear_process,
    premium_process,
    record_release,
    stack,
)
from .workflow_sheet import build_workflow_sheet
from .capture_compare import compare_captures


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(prog="seestarflow")
    root.add_argument("--config", type=Path, default=ROOT / "config.toml")
    commands = root.add_subparsers(dest="command", required=True)
    commands.add_parser("doctor")
    compare = commands.add_parser("capture-compare")
    compare.add_argument("--spec", type=Path, required=True)
    compare.add_argument("--output", type=Path, required=True)
    add = commands.add_parser("ingest")
    add.add_argument("--source", type=Path, required=True)
    add.add_argument("--target", required=True)
    add.add_argument("--site", required=True, help="A short site label, for example backyard or dark-site")
    add.add_argument("--filter", choices=("broadband", "dualband"), required=True)
    add.add_argument("--mount", choices=("altaz", "eq", "unknown"), required=True)
    qa = commands.add_parser("analyze")
    qa.add_argument("--session", type=Path, required=True)
    run = commands.add_parser("stack")
    run.add_argument("--session", type=Path, required=True)
    run.add_argument("--dry-run", action="store_true")
    linear = commands.add_parser("linear")
    linear.add_argument("--stack", type=Path, required=True)
    linear.add_argument(
        "--grax-denoise", action="store_true",
        help="Use GraXpert denoise for the free branch; leave off before NoiseXTerminator",
    )
    linear.add_argument("--dry-run", action="store_true")
    premium = commands.add_parser(
        "premium",
        help="Run licensed NXT once and optional early SXT; Photoshop GXT/StarShrink remain manual gates",
    )
    premium.add_argument("--linear", type=Path, required=True)
    premium.add_argument("--kind", choices=("cluster", "galaxy", "nebula"), required=True)
    premium.add_argument("--star-separate", action="store_true")
    premium.add_argument("--dry-run", action="store_true")
    storage = commands.add_parser("storage")
    storage.add_argument("--exposure", type=float, required=True, help="Exposure length in seconds")
    storage.add_argument("--hours", type=float, required=True)
    storage.add_argument("--frame-bytes", type=int, default=16_594_560)
    storage.add_argument("--overhead", type=float, default=1.25)
    sheet = commands.add_parser("workflow-sheet")
    sheet.add_argument("--spec", type=Path, required=True)
    sheet.add_argument("--output", type=Path)
    release = commands.add_parser("release")
    release.add_argument("--file", type=Path, required=True)
    release.add_argument("--target", required=True)
    release.add_argument("--variant", choices=("proof", "portfolio", "print", "archive"), required=True)
    release.add_argument("--destination", default="", help="Publication URL, print lab, client, or archive label")
    release.add_argument("--notes", default="")
    release.add_argument("--manifest", type=Path)
    return root


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    config = load_config(args.config)
    if args.command == "capture-compare":
        report = compare_captures(args.spec.resolve(), args.output.resolve())
        print(json.dumps({key: value for key, value in report.items() if key != "selections"}, indent=2))
        return 0
    if args.command == "doctor":
        report = {
            "library": str(resolve_library(config)),
            "siril": find_executable(config["tools"].get("siril", ""), ("siril-cli.exe", "siril-cli", "siril.exe", "siril")),
            "graxpert": find_executable(config["tools"].get("graxpert", ""), ("GraXpert-win64.exe", "graxpert.exe", "graxpert")),
            "rc_astro": find_executable(config["tools"].get("rc_astro", ""), ("rc-astro.exe", "rc-astro")),
            "photoshop": find_executable(config["tools"].get("photoshop", ""), ("Photoshop.exe",)),
            "pixinsight": find_executable(config["tools"].get("pixinsight", ""), ("PixInsight.exe", "PixInsight")),
            "identity_configured": bool(config.get("identity", {}).get("creator") and config.get("identity", {}).get("copyright_notice")),
            "free_gb": round(shutil.disk_usage(ROOT).free / 1024**3, 1),
        }
        print(json.dumps(report, indent=2)); return 0
    if args.command == "ingest":
        result = ingest(
            args.source, resolve_library(config), args.target, args.site, args.filter, args.mount,
            config.get("identity", {}),
        )
        print(result); return 0
    if args.command == "analyze":
        rows = analyze(args.session.resolve(), config["quality"])
        accepted = sum(bool(row["accepted"]) for row in rows)
        print(f"Accepted {accepted}/{len(rows)} frames; report: {args.session / 'quality.csv'}"); return 0
    if args.command == "stack":
        work, command = stack(args.session.resolve(), config["tools"].get("siril", ""), args.dry_run)
        print(f"Work directory: {work}\nCommand: {' '.join(command)}"); return 0
    if args.command == "linear":
        output, commands = linear_process(
            args.stack.resolve(), config["tools"].get("graxpert", ""), args.grax_denoise, args.dry_run,
        )
        print(f"Output directory: {output}")
        for command in commands: print("Command:", " ".join(command))
        return 0
    if args.command == "storage":
        print(json.dumps(estimate_storage(args.exposure, args.hours, args.frame_bytes, args.overhead), indent=2))
        return 0
    if args.command == "workflow-sheet":
        print(build_workflow_sheet(args.spec.resolve(), args.output.resolve() if args.output else None))
        return 0
    if args.command == "release":
        manifest = args.manifest.resolve() if args.manifest else resolve_library(config) / "release-manifest.jsonl"
        entry = record_release(
            args.file.resolve(), manifest, args.target, args.variant, args.destination, args.notes,
            config.get("identity", {}),
        )
        print(json.dumps(entry, indent=2, ensure_ascii=False))
        return 0
    if args.command == "premium":
        output, commands = premium_process(
            args.linear.resolve(), config["tools"].get("rc_astro", ""), args.kind,
            args.star_separate, args.dry_run,
        )
        print(f"Output directory: {output}")
        for command in commands: print("Command:", " ".join(command))
        return 0
    return 2
