import argparse
import json
from pathlib import Path
from .policy import load_rules
from .qc import validate
from .assets import load_manifest, validate_assets

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--rules-dir", required=True)
    parser.add_argument("--job", required=True)
    parser.add_argument("--assets-dir", required=True, help="Directory containing seven independent PNGs")
    parser.add_argument("--assets-manifest", required=True, help="JSON scene inspection manifest")
    args = parser.parse_args()
    try:
        hashes = load_rules(args.rules_dir)
        job = json.loads(Path(args.job).read_text(encoding="utf-8"))
        job["ruleset_hashes"] = hashes
        failures = validate(job)
        failures += validate_assets(args.assets_dir, load_manifest(args.assets_manifest))
    except (OSError, ValueError, TypeError) as exc:
        print("BLOCKED:", exc)
        return 2
    print(json.dumps({"status": "BLOCKED" if failures else "READY_FOR_HUMAN_REVIEW", "failures": failures, "ruleset_hashes": hashes, "publication_authorized": False}, indent=2))
    return 1 if failures else 0

if __name__ == "__main__":
    raise SystemExit(main())
