from __future__ import annotations

import math
from dataclasses import dataclass, asdict
from pathlib import Path

import numpy as np


BLOCK = 2880


def _value(text: str):
    value = text.split("/", 1)[0].strip()
    if value.startswith("'"):
        return value.strip(" '")
    if value in {"T", "F"}:
        return value == "T"
    try:
        return float(value.replace("D", "E")) if any(c in value for c in ".ED") else int(value)
    except ValueError:
        return value


def read_header(path: Path) -> tuple[dict, int]:
    header: dict[str, object] = {}
    consumed = 0
    with path.open("rb") as handle:
        ended = False
        while not ended:
            block = handle.read(BLOCK)
            if len(block) != BLOCK:
                raise ValueError(f"Incomplete FITS header: {path}")
            consumed += BLOCK
            for start in range(0, BLOCK, 80):
                card = block[start : start + 80].decode("ascii", errors="replace")
                key = card[:8].strip()
                if key == "END":
                    ended = True
                    break
                if key and card[8:10] == "= ":
                    header[key] = _value(card[10:])
    return header, consumed


def read_image(path: Path, max_side: int = 1200) -> tuple[dict, np.ndarray]:
    header, offset = read_header(path)
    bitpix = int(header.get("BITPIX", 0))
    naxis = int(header.get("NAXIS", 0))
    dims = [int(header[f"NAXIS{i}"]) for i in range(1, naxis + 1)]
    dtypes = {8: ">u1", 16: ">i2", 32: ">i4", -32: ">f4", -64: ">f8"}
    if bitpix not in dtypes or naxis not in {2, 3}:
        raise ValueError(f"Unsupported FITS layout BITPIX={bitpix}, NAXIS={naxis}: {path}")
    count = math.prod(dims)
    with path.open("rb") as handle:
        handle.seek(offset)
        data = np.fromfile(handle, dtype=np.dtype(dtypes[bitpix]), count=count)
    if data.size != count:
        raise ValueError(f"Incomplete FITS pixels: {path}")
    data = data.reshape(tuple(reversed(dims))).astype(np.float32)
    data = data * float(header.get("BSCALE", 1.0)) + float(header.get("BZERO", 0.0))
    if data.ndim == 3:
        data = np.median(data, axis=0)
    stride = max(1, math.ceil(max(data.shape) / max_side))
    return header, data[::stride, ::stride]


@dataclass
class Quality:
    background: float
    noise_mad: float
    star_count: int
    fwhm_px: float
    ellipticity: float
    saturation_fraction: float
    score: float = 0.0
    accepted: bool = True
    reason: str = ""

    def serializable(self) -> dict:
        return asdict(self)


def measure_quality(image: np.ndarray) -> Quality:
    finite = image[np.isfinite(image)]
    if finite.size < 100:
        raise ValueError("Not enough finite pixels")
    background = float(np.median(finite))
    mad = float(np.median(np.abs(finite - background)))
    noise = max(1e-6, 1.4826 * mad)
    threshold = background + 7.0 * noise
    core = image[1:-1, 1:-1]
    peaks = core > threshold
    for dy, dx in ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)):
        peaks &= core >= np.roll(np.roll(core, dy, axis=0), dx, axis=1)
    coords = np.argwhere(peaks)
    if len(coords) > 300:
        brightness = core[coords[:, 0], coords[:, 1]]
        coords = coords[np.argsort(brightness)[-300:]]

    fwhms: list[float] = []
    ellipticities: list[float] = []
    for y0, x0 in coords:
        y, x = int(y0 + 1), int(x0 + 1)
        if y < 4 or x < 4 or y + 4 >= image.shape[0] or x + 4 >= image.shape[1]:
            continue
        patch = np.maximum(image[y - 3 : y + 4, x - 3 : x + 4] - background, 0)
        total = float(patch.sum())
        if total <= 0:
            continue
        yy, xx = np.mgrid[-3:4, -3:4]
        mx = float((patch * xx).sum() / total)
        my = float((patch * yy).sum() / total)
        vx = float((patch * (xx - mx) ** 2).sum() / total)
        vy = float((patch * (yy - my) ** 2).sum() / total)
        major, minor = max(vx, vy), min(vx, vy)
        if 0.04 < major < 9.0:
            fwhms.append(2.355 * math.sqrt((vx + vy) / 2.0))
            ellipticities.append(1.0 - math.sqrt(max(minor, 0.0) / major))
    high = float(np.percentile(finite, 99.999))
    saturation = float(np.mean(finite >= high)) if high > background else 0.0
    return Quality(
        background=background,
        noise_mad=noise,
        star_count=len(fwhms),
        fwhm_px=float(np.median(fwhms)) if fwhms else 99.0,
        ellipticity=float(np.median(ellipticities)) if ellipticities else 1.0,
        saturation_fraction=saturation,
    )
