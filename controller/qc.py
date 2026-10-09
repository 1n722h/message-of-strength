def validate(job):
    errors = []
    if job.get("format") != "SUBSTANTIVE_40_V1":
        errors.append("Wrong format")
    if abs(job.get("duration_seconds", 0) - 40) > 1 / 30:
        errors.append("Wrong duration")
    if len(job.get("beats", [])) != 7:
        errors.append("Expected seven beats")
    desc = job.get("description", "")
    for tag in ("#hopecore", "#fyp"):
        if desc.count(tag) != 1:
            errors.append("Missing or repeated " + tag)
    for gate in ("export_visually_inspected", "mobile_caption_overlay_checked", "audio_listened", "music_provenance_checked", "topic_originality_checked"):
        if job.get("qc", {}).get(gate) is not True:
            errors.append("QC evidence missing: " + gate)
    if not job.get("ruleset_hashes"):
        errors.append("Ruleset hashes missing")
    return errors

def may_publish(job):
    # Publishing is not implemented. Approval requires a separate explicit user action.
    return False
