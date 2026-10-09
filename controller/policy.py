import hashlib
import json
from pathlib import Path

REQUIRED = ("PROJECT_MANIFEST", "MASTER_PRODUCTION_SPEC", "PRODUCTION_POLICY_CONFIG_JSON_v1")

def load_rules(folder):
    root = Path(folder)
    hashes = {}
    for name in REQUIRED:
        path = root / (name + ".txt")
        data = path.read_bytes()
        if not data.strip():
            raise ValueError("Empty rule: " + name)
        hashes[name] = hashlib.sha256(data).hexdigest()
    config = json.loads((root / (REQUIRED[2] + ".txt")).read_text(encoding="utf-8-sig"))
    if config.get("status") != "ACTIVE" or config.get("workflow", {}).get("require_explicit_publication_approval") is not True:
        raise ValueError("Inactive or unsafe production policy")
    return hashes
