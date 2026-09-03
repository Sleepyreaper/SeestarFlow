from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

from .config import ROOT, load_config, resolve_library
from .pipeline import analyze, find_executable, ingest, linear_process, premium_process, stack


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(prog="seestarflow")
    root.add_argument("--config", type=Path, default=ROOT / "config.toml")
    commands = root.add_subparsers(dest="command", required=True)
    commands.add_parser("doctor")
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
    linear.add_argument("--dry-run", action="store_true")
    premium = commands.add_parser("premium")
    premium.add_argument("--linear", type=Path, required=True)
    premium.add_argument("--kind", choices=("cluster", "galaxy", "nebula"), required=True)
    premium.add_argument("--star-separate", action="store_true")
    premium.add_argument("--dry-run", action="store_true")
    return root


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    config = load_config(args.config)
    if args.command == "doctor":
        report = {
            "library": str(resolve_library(config)),
            "siril": find_executable(config["tools"].get("siril", ""), ("siril-cli.exe", "siril-cli", "siril.exe", "siril")),
            "graxpert": find_executable(config["tools"].get("graxpert", ""), ("GraXpert-win64.exe", "graxpert.exe", "graxpert")),
            "rc_astro": find_executable(config["tools"].get("rc_astro", ""), ("rc-astro.exe", "rc-astro")),
            "pixinsight": find_executable(config["tools"].get("pixinsight", ""), ("PixInsight.exe", "PixInsight")),
            "free_gb": round(shutil.disk_usage(ROOT).free / 1024**3, 1),
        }
        print(json.dumps(report, indent=2)); return 0
    if args.command == "ingest":
        result = ingest(args.source, resolve_library(config), args.target, args.site, args.filter, args.mount)
        print(result); return 0
    if args.command == "analyze":
        rows = analyze(args.session.resolve(), config["quality"])
        accepted = sum(bool(row["accepted"]) for row in rows)
        print(f"Accepted {accepted}/{len(rows)} frames; report: {args.session / 'quality.csv'}"); return 0
    if args.command == "stack":
        work, command = stack(args.session.resolve(), config["tools"].get("siril", ""), args.dry_run)
        print(f"Work directory: {work}\nCommand: {' '.join(command)}"); return 0
    if args.command == "linear":
        output, commands = linear_process(args.stack.resolve(), config["tools"].get("graxpert", ""), args.dry_run)
        print(f"Output directory: {output}")
        for command in commands: print("Command:", " ".join(command))
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
