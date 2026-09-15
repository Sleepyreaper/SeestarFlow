import json
import contextlib
import io
import tempfile
import unittest
from pathlib import Path

from seestarflow.capture_compare import compare_captures
from seestarflow.cli import main


def write_sub(path, exposure, sequence, **overrides):
    header = {"SIMPLE": True, "BITPIX": 16, "NAXIS": 2, "NAXIS1": 4, "NAXIS2": 4,
              "EXPTIME": exposure, "EQMODE": 1, "OBJECT": "M31", "FILTER": "IRCUT",
              "INSTRUME": "TEST", "GAIN": 80, "FOCALLEN": 260, "BAYERPAT": "RGGB",
              "SEQID": sequence, "DATE-OBS": f"2026-09-20T01:{sequence:02}:00"}
    header.update(overrides)
    cards = []
    for key, value in header.items():
        literal = f"'{value}'" if isinstance(value, str) else str(value)
        cards.append(f"{key:<8}= {literal}".ljust(80))
    payload = ("".join(cards) + "END".ljust(80)).encode().ljust(2880, b" ")
    path.write_bytes(payload + bytes(2880))


class CaptureCompareTests(unittest.TestCase):
    def fixture(self, root):
        blocks = []
        for index, (exposure, count) in enumerate(((30, 8), (60, 3))):
            folder = root / str(exposure)
            folder.mkdir()
            names = []
            for n in range(count):
                name = f"{n:03}.fit"
                write_sub(folder / name, exposure, index * 10 + n)
                names.append(name)
            (folder / "approved.lst").write_text("\n".join(names))
            blocks.append({"id": str(exposure), "source": str(exposure),
                           "approved_list": f"{exposure}/approved.lst", "mount": "eq",
                           "exposure_seconds": exposure, "wall_seconds": 300})
        spec = root / "experiment.json"
        spec.write_text(json.dumps({"blocks": blocks}))
        return spec

    def test_equal_time_and_clock_yield_have_separate_meanings(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            report = compare_captures(self.fixture(root), root / "report")
            self.assertEqual(report["equal_input_integration_seconds"], 180)
            self.assertEqual(len(report["selections"]["eq_30s"]["equal_integration"]), 6)
            self.assertEqual(len(report["selections"]["eq_60s"]["equal_integration"]), 3)
            self.assertEqual(report["groups"][0]["qa_minutes_per_clock_hour"], 48)
            self.assertEqual(report["groups"][1]["qa_minutes_per_clock_hour"], 36)
            self.assertIn("pending", report["status"])
            self.assertTrue((root / "report/throughput.csv").exists())

    def test_rejects_mislabeled_data(self):
        cases = ({"EXPTIME": 10}, {"EQMODE": 0}, {"STACKCNT": 50},
                 {"NAXIS": 3}, {"FILTER": "LP"}, {"GAIN": 90})
        for change in cases:
            with self.subTest(change=change), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                spec = self.fixture(root)
                write_sub(root / "60/000.fit", 60, 10, **change)
                with self.assertRaises(ValueError):
                    compare_captures(spec, root / "report")
                self.assertFalse((root / "report").exists())

    def test_duplicate_photons_and_truncated_file(self):
        for truncated in (False, True):
            with self.subTest(truncated=truncated), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                spec = self.fixture(root)
                source = root / "30/000.fit"
                (root / "30/001.fit").write_bytes(source.read_bytes()[:2880] if truncated else source.read_bytes())
                with self.assertRaises(ValueError):
                    compare_captures(spec, root / "report")

    def test_does_not_count_unapproved_frames_as_accepted(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            spec = self.fixture(root)
            (root / "30/approved.lst").write_text("000.fit\n001.fit\n")
            report = compare_captures(spec, root / "report")
            self.assertEqual(report["equal_input_integration_seconds"], 60)
            self.assertEqual(report["groups"][0]["qa_retention_of_saved"], 0.25)

    def test_rejects_bad_clock_or_missing_selection(self):
        for case in ("clock", "missing", "empty"):
            with self.subTest(case=case), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                spec = self.fixture(root)
                if case == "clock":
                    data = json.loads(spec.read_text())
                    data["blocks"][0]["wall_seconds"] = 30
                    spec.write_text(json.dumps(data))
                else:
                    (root / "30/approved.lst").write_text("absent.fit" if case == "missing" else "")
                with self.assertRaises(ValueError):
                    compare_captures(spec, root / "report")

    def test_cli_and_existing_report_protection(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            spec = self.fixture(root)
            with contextlib.redirect_stdout(io.StringIO()) as stdout:
                result = main(["capture-compare", "--spec", str(spec), "--output", str(root / "report")])
            self.assertEqual(result, 0)
            self.assertEqual(json.loads(stdout.getvalue())["equal_input_integration_seconds"], 180)
            before = (root / "report/report.json").read_bytes()
            with self.assertRaises(FileExistsError):
                compare_captures(spec, root / "report")
            self.assertEqual((root / "report/report.json").read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
