import unittest
from controller.pipeline import STAGES, stage_rules, validate_pipeline

def record(stage):
    from controller.pipeline import REQUIRED_OUTPUTS
    outputs = {key: "evidence" for key in REQUIRED_OUTPUTS[stage]}
    if stage == "editorial":
        outputs["beats"] = [{"beat": i} for i in range(1, 8)]
    if stage == "casting":
        outputs["characters"] = [{"id": "character_01"}]
    if stage == "artwork":
        outputs["scene_briefs"] = [{"beat": i} for i in range(1, 8)]
        outputs["generation_requests"] = [{"beat": i, "separate_request": True} for i in range(1, 8)]
    return {"status": "passed", "outputs": outputs, "inspection_note": "Evidence checked"}

class PipelineTests(unittest.TestCase):
    def test_stage_rule_scoping(self):
        self.assertIn("CHARACTER_CONTINUITY_RULESET", stage_rules("casting"))
        self.assertNotIn("TOPIC_DISCOVERY_RULESET", stage_rules("casting"))
        self.assertIn("PROJECT_MANIFEST", stage_rules("casting"))

    def test_missing_casting_blocks_artwork(self):
        stages = {"editorial": record("editorial"), "artwork": record("artwork")}
        self.assertIn("casting: not passed", validate_pipeline({"stages": stages}, "artwork"))

    def test_missing_independent_generation_blocks(self):
        stages = {stage: record(stage) for stage in STAGES[:3]}
        stages["artwork"]["outputs"]["generation_requests"][2]["separate_request"] = False
        self.assertIn("artwork: require seven separate generation requests", validate_pipeline({"stages": stages}, "artwork"))

    def test_valid_stage_sequence(self):
        stages = {stage: record(stage) for stage in STAGES}
        self.assertEqual(validate_pipeline({"stages": stages}, "approval"), [])

    def test_no_publication_permission_from_pipeline(self):
        stages = {stage: record(stage) for stage in STAGES}
        stages["approval"]["publication_authorized"] = True
        self.assertIn("approval: pipeline cannot authorize publication", validate_pipeline({"stages": stages}, "approval"))

if __name__ == "__main__":
    unittest.main()
