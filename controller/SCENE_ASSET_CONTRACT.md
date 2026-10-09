# Seven-beat independent asset contract (ACTIVE for manual testing)

Generate **one image per invocation**, never a whole-reel storyboard, contact sheet, comic page or collage. Each request must reference only one beat's setting, subject, action and emotional purpose. Do not include captions, speech bubbles, letters, logos, watermarks, borders, panels or split screens. Use original adult graphic-novel style from ACTIVE Drive rules. Preserve established character traits across beats.

1. Select original topic after checking topic bank and recent production history.
2. Write seven distinct scene briefs and caption/timing records; timing sums to 40 seconds.
3. Generate `beat_01.png` alone, inspect it, then generate `beat_02.png` alone, etc. Preserve originals; never crop seven panels out of a single composite image.
4. Deliver exactly seven standalone 1080x1920 PNG assets `beat_01.png` through `beat_07.png`.
5. Before assembly, visually inspect **each individual image** for single-scene composition, no collage, no embedded readable text, continuity and framing. Document a genuine, scene-specific `inspection_note` and set evidence flags only after inspection. Do not infer inspection from filename or image hash.
6. Create `assets_manifest.json` with `scenes` ordered 01–07. Every scene: `filename`, file-content `sha256`, `visually_inspected`, `single_scene_confirmed`, `no_embedded_text_confirmed`, `no_collage_confirmed`, `continuity_checked`, `inspection_note`.
7. Run `python -m controller.cli --rules-dir rules --job release.json --assets-dir artwork --assets-manifest assets_manifest.json` before considering a package ready for human review.
8. Reject failures, regenerate only the failed scene, re-inspect and re-run checks. Video assembly must not begin until all seven scene assets pass. Final exported-video inspection and TikTok UI overlay inspection remain mandatory separately.

**Limits:** The controller checks filenames, PNG signature/IHDR dimensions, SHA-256 uniqueness and recorded visual attestations. It does **not** itself understand image contents, prove the PNG fully decodes, or prove that a human/vision model truly inspected the images. A trusted production reviewer must perform the visual checks; never fabricate evidence. This controller never publishes or schedules anything.
