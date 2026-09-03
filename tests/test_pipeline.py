import struct
import tempfile
import unittest
from pathlib import Path

import numpy as np

from seestarflow.fits import measure_quality, read_header, read_image
from seestarflow.pipeline import ingest


def card(key, value=None):
    if value is None:
        text = key
    elif isinstance(value, str):
        text = f"{key:<8}= '{value}'"
    else:
        text = f"{key:<8}= {value:>20}"
    return text.ljust(80).encode("ascii")


def write_fits(path: Path):
    header = b"".join([
        card("SIMPLE", "T"), card("BITPIX", 16), card("NAXIS", 2), card("NAXIS1", 64),
        card("NAXIS2", 64), card("OBJECT", "M31"), card("DATE-OBS", "2026-08-27T02:00:00"),
        card("EXPTIME", 10.0), card("END")
    ]).ljust(2880, b" ")
    image = np.full((64, 64), 1000, dtype=">i2")
    for y, x in ((12, 12), (25, 20), (40, 44), (50, 15)):
        image[y, x] = 8000
        image[y-1:y+2, x-1:x+2] += 1500
    payload = image.tobytes()
    path.write_bytes(header + payload + b"\0" * ((-len(payload)) % 2880))


class PipelineTests(unittest.TestCase):
    def test_fits_and_ingest(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); source = root / "M31_sub"; source.mkdir()
            frame = source / "frame-0001.fit"; write_fits(frame)
            header, _ = read_header(frame)
            self.assertEqual(header["OBJECT"], "M31")
            _, image = read_image(frame)
            self.assertEqual(image.shape, (64, 64))
            quality = measure_quality(image)
            self.assertGreaterEqual(quality.star_count, 1)
            session = ingest(source, root / "library", "M31", "backyard", "broadband", "altaz")
            self.assertTrue((session / "manifest.json").exists())
            archived = session / "originals" / frame.name
            before = archived.read_bytes()
            frame.write_bytes(b"source changed after ingest")
            self.assertEqual(archived.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
