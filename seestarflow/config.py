from __future__ import annotations

import tomllib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_config(path: Path | None = None) -> dict:
    config_path = path or ROOT / "config.toml"
    with config_path.open("rb") as handle:
        return tomllib.load(handle)


def resolve_library(config: dict) -> Path:
    value = Path(config["paths"]["library"])
    return value if value.is_absolute() else ROOT / value
