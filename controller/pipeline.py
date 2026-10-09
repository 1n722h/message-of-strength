"""Fail-closed stage transitions for Message of Strength.

A producer supplies actual stage artifacts and inspection evidence. This module
does not generate content or claim that a visual review took place.
"""
import hashlib
import json
from pathlib import Path

STAGES = ("editorial", "casting", "artwork", "asset_qc", "assembly", "final_qc", "approval")
RULES = {
    "editorial": ("TOPIC_DISCOVERY_RULESET", "EDITORIAL_TONE_RULESET", "MESSAGES_OF_HOPE_TOPIC_BANK"),
    "casting": ("CHARACTER_CONTINUITY_RULESET",),
    "artwork": ("VISUAL_STYLE_RULESET", "CHARACTER_CONTINUITY_RULESET"),
    "asset_qc": ("VISUAL_STYLE_RULESET", "CHARACTER_CONTINUITY_RULESET"),
    "assembly": ("TYPOGRAPHY_AND_ON_SCREEN_COPY_RULESET",),
    "final_qc": ("TYPOGRAPHY_AND_ON_SCREEN_COPY_RULESET",),
    "approval": (),
}
GLOBAL = ("PROJECT_MANIFEST", "MASTER_PRODUCTION_SPEC", "PRODUCTION_POLICY_CONFIG_JSON_v1")
REQUIRED_OUTPUTS = {
    "editorial": ("topic_id", "originality_note", "script", "beats"),
    "casting": ("characters", "casting_variety_note", "beat_cast"),
    "artwork": ("scene_briefs", "character_lock", "generation_requests"),
    "asset_qc": ("assets_manifest",),
    "assembly": ("video_path", "music_source", "captions_path"),
    "final_qc": ("video_inspection_note", "audio_inspection_note", "mobile_overlay_note"),
    "approval": ("review_package",),
}


def stage_rules(stage):
    if stage not in STAGES:
        raise ValueError("Unknown stage: " + str(stage))
    return GLOBAL + RULES[stage]


def validate_pipeline(pipeline, stage, rules_dir=None):
    """Require all earlier stages complete and stage-specific output evidence."""
    if stage not in STAGES:
        return ["Unknown stage"]
    errors = []
    if not isinstance(pipeline, dict) or not isinstance(pipeline.get("stages"), dict):
        return ["Missing pipeline stage records"]
    records = pipeline["stages"]
    for name in STAGES[:STAGES.index(stage) + 1]:
        record = records.get(name)
        if not isinstance(record, dict) or record.get("status") != "passed":
            errors.append(name + ": not passed")
            continue
        outputs = record.get("outputs")
        if not isinstance(outputs, dict):
            errors.append(name + ": outputs missing")
            continue
        for field in REQUIRED_OUTPUTS[name]:
            if not outputs.get(field):
                errors.append(name + ": missing " + field)
        if not isinstance(record.get("inspection_note"), str) or not record["inspection_note"].strip():
            errors.append(name + ": missing review note")
        if name == "artwork":
            requests = outputs.get("generation_requests")
            if not isinstance(requests, list) or len(requests) != 7 or any(
                not isinstance(x, dict) or x.get("beat") != i or x.get("separate_request") is not True
                for i, x in enumerate(requests, 1)
            ):
                errors.append("artwork: require seven separate generation requests")
            briefs = outputs.get("scene_briefs")
            if not isinstance(briefs, list) or len(briefs) != 7:
                errors.append("artwork: require seven scene briefs")
        if name == "casting":
            if not isinstance(outputs.get("characters"), list) or not outputs["characters"]:
                errors.append("casting: require character records")
        if name == "editorial":
            if not isinstance(outputs.get("beats"), list) or len(outputs["beats"]) != 7:
                errors.append("editorial: require seven beats")
        if name == "approval" and record.get("publication_authorized") is True:
            errors.append("approval: pipeline cannot authorize publication")
        if rules_dir is not None:
            hashes = record.get("ruleset_hashes")
            if not isinstance(hashes, dict):
                errors.append(name + ": ruleset hashes missing")
            else:
                for rule in stage_rules(name):
                    path = Path(rules_dir) / (rule + ".txt")
                    try:
                        actual = hashlib.sha256(path.read_bytes()).hexdigest()
                        if hashes.get(rule) != actual:
                            errors.append(name + ": missing/stale rule " + rule)
                    except OSError:
                        errors.append(name + ": missing rule file " + rule)
    return errors


def load_pipeline(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))
