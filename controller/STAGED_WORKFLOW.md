# Message of Strength: staged production contract

**Global authority:** PROJECT_MANIFEST, MASTER_PRODUCTION_SPEC and PRODUCTION_POLICY_CONFIG_JSON_v1 apply at every stage. Stage-specific documents supplement them, never override them. Every source must be exported from the current authoritative Google Drive document as `rules/<DOCUMENT_NAME>.txt`. Hashes are checked at each stage. Drive retrieval is not automated by this repository.

Stages (in strict order):
1. **editorial** — TOPIC_DISCOVERY_RULESET, EDITORIAL_TONE_RULESET, MESSAGES_OF_HOPE_TOPIC_BANK. Output topic ID, originality evidence, script, seven beats.
2. **casting** — CHARACTER_CONTINUITY_RULESET. Consult `03_CHARACTERS/CHARACTER_SHEETS`; choose varied characters, lock their descriptions and mapping to beats. Do not use a generic default protagonist.
3. **artwork** — VISUAL_STYLE_RULESET, CHARACTER_CONTINUITY_RULESET. Seven scene briefs and **seven independent generation calls**; one scene per call, no embedded captions or collage.
4. **asset_qc** — VISUAL_STYLE_RULESET, CHARACTER_CONTINUITY_RULESET. Review every generated image before advancing. Reject and regenerate only failed beats. Attach seven-asset inspection manifest.
5. **assembly** — TYPOGRAPHY_AND_ON_SCREEN_COPY_RULESET. Only after asset QC: caption overlay, approved audio, 40-second MP4 and provenance.
6. **final_qc** — TYPOGRAPHY_AND_ON_SCREEN_COPY_RULESET. Inspect the actual exported MP4, phone overlay and mixed audio.
7. **approval** — Present the result for explicit user review. Never publish or schedule without subsequent explicit authorization.

Each stage in `pipeline.json` contains `status: "passed"`, `inspection_note`, `outputs` with fields defined in `controller/pipeline.py`, and `ruleset_hashes` for all its global + stage rules. The controller checks order, evidence fields and rule provenance. **It cannot prove a review happened or execute creative work**. Do not mark evidence as passed unless the work was actually done.

Run:
```sh
python -m unittest discover -s tests -v
python -m controller.cli --rules-dir rules --job release.json --assets-dir artwork --assets-manifest assets_manifest.json --pipeline pipeline.json --stage final_qc
```

A successful result means **READY_FOR_HUMAN_REVIEW**, never publication authorization. Stage validation is also available programmatically via `validate_pipeline(pipeline, stage, rules_dir)`; the release CLI always requires the seven assets and release manifest, so use the programmatic validator during early stages.

No image generation, Drive export, video assembly, scheduling or publishing is performed by this controller.
