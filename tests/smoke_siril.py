"""Create a tiny Bayer FITS sequence and run the production Siril script."""

from __future__ import annotations

import argparse
import subprocess
import tempfile
from pathlib import Path

import numpy as np


def card(key: str, value=None) -> bytes:
    if value is None:
        text = key
    elif isinstance(value, bool):
        text = f"{key:<8}= {'T' if value else 'F':>20}"
    elif isinstance(value, str):
        text = f"{key:<8}= '{value}'"
    else:
        text = f"{key:<8}= {value:>20}"
    return text.ljust(80).encode("ascii")


def write_frame(path: Path, index: int) -> None:
    rng = np.random.default_rng(1000 + index)
    image = rng.normal(900, 8, (128, 128))
    yy, xx = np.mgrid[:128, :128]
    star_rng = np.random.default_rng(42)
    positions = star_rng.uniform(8, 120, (34, 2))
    brightness = star_rng.uniform(900, 3500, 34)
    # Integer motion keeps the Bayer phase stable while exercising registration.
    dx, dy = index // 4, index // 6
    for (x, y), peak in zip(positions, brightness, strict=True):
        image += peak * np.exp(-((xx - (x + dx)) ** 2 + (yy - (y + dy)) ** 2) / 2.2)
    pixels = np.clip(image, 0, 32000).astype(">i2")
    cards = [
        card("SIMPLE", True), card("BITPIX", 16), card("NAXIS", 2), card("NAXIS1", 128),
        card("NAXIS2", 128), card("BAYERPAT", "RGGB"), card("XBAYROFF", 0), card("YBAYROFF", 0),
        card("OBJECT", "SMOKE"), card("EXPTIME", 10.0), card("CCD-TEMP", 15.0),
        card("DATE-OBS", f"2026-08-27T02:00:{index:02d}"), card("END"),
    ]
    header = b"".join(cards).ljust(2880, b" ")
    payload = pixels.tobytes()
    path.write_bytes(header + payload + b"\0" * ((-len(payload)) % 2880))


def main() -> int:
    args = argparse.ArgumentParser()
    args.add_argument("--siril", type=Path, required=True)
    args.add_argument("--script", type=Path, required=True)
    options = args.parse_args()
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as temporary:
        work = Path(temporary); lights = work / "lights"; lights.mkdir()
        for index in range(12):
            write_frame(lights / f"smoke_{index:04d}.fit", index)
        command = [str(options.siril), "-d", str(work), "-s", str(options.script.resolve())]
        subprocess.run(command, check=True)
        result = work / "stack_linear.fit"
        if not result.exists() or result.stat().st_size < 2880:
            raise RuntimeError("Siril did not create stack_linear.fit")
        print(f"Siril smoke stack passed: {result.stat().st_size} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
