import struct
import tempfile
import unittest
from pathlib import Path

import numpy as np

from seestarflow.fits import measure_quality, read_header, read_image
from seestarflow.pipeline import estimate_storage, ingest, linear_process, premium_process, record_release


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

    def test_storage_estimate_uses_measured_s50_pro_frame_size(self):
        result = estimate_storage(10, 8)
        self.assertEqual(result["frames"], 2880)
        self.assertEqual(result["raw_gb"], 47.79)
        self.assertGreater(result["recommended_free_gb"], result["raw_gb"])

    def test_paid_branch_does_not_double_denoise(self):
        with tempfile.TemporaryDirectory() as temp:
            stack = Path(temp) / "stack.fit"
            stack.write_bytes(b"test linear master")
            _, grax_commands = linear_process(stack, "", dry_run=True)
            self.assertEqual(len(grax_commands), 1)
            self.assertEqual(grax_commands[0][4], "background-extraction")

            _, paid_commands = premium_process(stack, "", "nebula", star_separate=True, dry_run=True)
            self.assertIn("--sharpen-stars", paid_commands[0])
            self.assertIn("--sharpen-nonstellar", paid_commands[0])
            self.assertIn("--denoise", paid_commands[1])
            self.assertNotIn("--unscreen", paid_commands[2])

    def test_free_branch_can_request_graxpert_denoise(self):
        with tempfile.TemporaryDirectory() as temp:
            stack = Path(temp) / "stack.fit"
            stack.write_bytes(b"test linear master")
            _, commands = linear_process(stack, "", grax_denoise=True, dry_run=True)
            self.assertEqual(len(commands), 2)
            self.assertEqual(commands[1][4], "denoising")

    def test_release_ledger_hashes_exact_export(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            export = root / "m27-portfolio.jpg"
            export.write_bytes(b"exact release bytes")
            manifest = root / "release-manifest.jsonl"
            entry = record_release(
                export, manifest, "M27", "portfolio", "https://example.test/m27", identity={
                    "creator": "Example Photographer",
                    "copyright_notice": "Copyright Example Photographer",
                    "private_field": "must-not-leak",
                },
            )
            self.assertEqual(entry["target"], "M27")
            self.assertEqual(entry["identity"]["creator"], "Example Photographer")
            self.assertNotIn("private_field", entry["identity"])
            saved = manifest.read_text(encoding="utf-8")
            self.assertIn(entry["sha256"], saved)


if __name__ == "__main__":
    unittest.main()
