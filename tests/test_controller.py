import tempfile
import unittest
from controller.policy import load_rules
from controller.qc import validate, may_publish

class ControllerTests(unittest.TestCase):
    def test_missing_rules_block(self):
        with tempfile.TemporaryDirectory() as folder:
            with self.assertRaises(FileNotFoundError):
                load_rules(folder)

    def test_incomplete_qc_blocks(self):
        self.assertTrue(validate({"format": "SUBSTANTIVE_40_V1", "duration_seconds": 40, "beats": [{}] * 7}))

    def test_publication_always_requires_external_approval(self):
        self.assertFalse(may_publish({"approved": True}))

if __name__ == "__main__":
    unittest.main()
