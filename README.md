# Messages of Hope production controller

Python foundation for the Messages of Hope 40-second TikTok reel workflow.

## Current capabilities
- Fail-closed loading of three authoritative Google Drive rules exported as UTF-8 text.
- SHA-256 rule provenance.
- Release manifest checks for 40 seconds, seven beats, both required hashtags, and human QC evidence.
- Manual GitHub Actions unit-test workflow (no scheduled trigger).
- No publishing, scheduling, asset generation, paid API usage, or automated Drive retrieval yet.

## Run tests
```sh
python -m unittest discover -s tests -v
```

## Dry-run QC
Place current exports in a local `rules/` folder with filenames:
`PROJECT_MANIFEST.txt`, `MASTER_PRODUCTION_SPEC.txt`, and `PRODUCTION_POLICY_CONFIG_JSON_v1.txt`.

```sh
python -m controller.cli --rules-dir rules --job release.json
```

This only reports `READY_FOR_HUMAN_REVIEW` or `BLOCKED`. A successful result does **not** authorize publishing. Finished reels must be previewed and explicitly approved by the user before any scheduling or publication.

## Next implementation phases
Authenticated Drive rule retrieval; complete ACTIVE ruleset loading and precedence checks; production job schema and topic bank; approved soundtrack selection; image/video and voiceover assembly; actual export-level mobile caption and audio QC; user preview and explicit release approval.

Never commit credentials, unpublished assets, private Drive content or API tokens. Keep GitHub Actions manual-only until the user requests scheduling.
