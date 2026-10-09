import hashlib
import struct
import tempfile
import unittest
from pathlib import Path
from controller.policy import load_rules
from controller.qc import validate, may_publish
from controller.assets import validate_assets, EXPECTED

def png_bytes(width=1080, height=1920, marker=b""):
    # Header-only fixtures test metadata; not a substitute for full PNG decode/visual QC.
    return b"\x89PNG\r\n\x1a\n" + struct.pack(">I", 13) + b"IHDR" + struct.pack(">II", width, height) + b"\x08\x06\x00\x00\x00" + marker

class ControllerTests(unittest.TestCase):
    def test_missing_rules_block(self):
        with tempfile.TemporaryDirectory() as folder:
            with self.assertRaises(FileNotFoundError):
                load_rules(folder)

    def test_incomplete_qc_blocks(self):
        self.assertTrue(validate({"format": "SUBSTANTIVE_40_V1", "duration_seconds": 40, "beats": [{}] * 7}))

    def test_publication_always_requires_external_approval(self):
        self.assertFalse(may_publish({"approved": True}))

    def fixtures(self, folder):
        scenes = []
        for i, filename in enumerate(EXPECTED):
            data = png_bytes(marker=bytes([i]))
            (Path(folder) / filename).write_bytes(data)
            scenes.append({"filename": filename, "sha256": hashlib.sha256(data).hexdigest(),
                           "visually_inspected": True, "single_scene_confirmed": True,
                           "no_embedded_text_confirmed": True, "no_collage_confirmed": True,
                           "continuity_checked": True, "inspection_note": "Scene individually inspected"})
        return {"scenes": scenes}

    def test_seven_independent_assets_pass_structural_gate(self):
        with tempfile.TemporaryDirectory() as folder:
            manifest = self.fixtures(folder)
            self.assertEqual(validate_assets(folder, manifest), [])

    def test_combined_scene_or_missing_file_blocks(self):
        with tempfile.TemporaryDirectory() as folder:
            manifest = self.fixtures(folder)
            (Path(folder) / "beat_04.png").unlink()
            self.assertTrue(validate_assets(folder, manifest))

    def test_duplicate_images_block(self):
        with tempfile.TemporaryDirectory() as folder:
            manifest = self.fixtures(folder)
            data = (Path(folder) / "beat_01.png").read_bytes()
            (Path(folder) / "beat_02.png").write_bytes(data)
            manifest["scenes"][1]["sha256"] = hashlib.sha256(data).hexdigest()
            self.assertIn("Seven distinct image hashes required", validate_assets(folder, manifest))

    def test_collage_not_inspected_blocks(self):
        with tempfile.TemporaryDirectory() as folder:
            manifest = self.fixtures(folder)
            manifest["scenes"][3]["no_collage_confirmed"] = False
            self.assertTrue(validate_assets(folder, manifest))

    def test_wrong_dimensions_block(self):
        with tempfile.TemporaryDirectory() as folder:
            manifest = self.fixtures(folder)
            data = png_bytes(width=720, height=1280, marker=b"3")
            (Path(folder) / "beat_04.png").write_bytes(data)
            manifest["scenes"][3]["sha256"] = hashlib.sha256(data).hexdigest()
            self.assertTrue(validate_assets(folder, manifest))

if __name__ == "__main__":
    unittest.main()
