import argparse
import json
from pathlib import Path
from .policy import load_rules
from .qc import validate

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--rules-dir", required=True)
    parser.add_argument("--job", required=True)
    args = parser.parse_args()
    try:
        hashes = load_rules(args.rules_dir)
        job = json.loads(Path(args.job).read_text(encoding="utf-8"))
        job["ruleset_hashes"] = hashes
        failures = validate(job)
    except (OSError, ValueError) as exc:
        print("BLOCKED:", exc)
        return 2
    print(json.dumps({"status": "BLOCKED" if failures else "READY_FOR_HUMAN_REVIEW", "failures": failures, "ruleset_hashes": hashes, "publication_authorized": False}, indent=2))
    return 1 if failures else 0

if __name__ == "__main__":
    raise SystemExit(main())
