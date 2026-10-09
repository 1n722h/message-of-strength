"""Fail-closed seven-scene asset gate. No image generation or publication here."""
import hashlib
import json
import re
import struct
from pathlib import Path

EXPECTED = [f"beat_{i:02d}.png" for i in range(1, 8)]
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def validate_assets(directory, manifest):
    """Return failures; visual attestations must come from an actual inspection."""
    failures = []
    root = Path(directory)
    if not isinstance(manifest, dict) or not isinstance(manifest.get("scenes"), list):
        return ["Missing scenes manifest"]
    scenes = manifest["scenes"]
    if len(scenes) != 7:
        failures.append("Expected exactly seven scene records")
    filenames = [s.get("filename") if isinstance(s, dict) else None for s in scenes]
    if filenames != EXPECTED:
        failures.append("Scene filenames/order must be beat_01.png through beat_07.png")
    if not root.is_dir():
        return failures + ["Asset directory missing"]
    actual = sorted(p.name for p in root.glob("beat_*.png") if p.is_file())
    if actual != EXPECTED:
        failures.append("Exactly seven numbered PNG assets required")
    digests = []
    for expected, scene in zip(EXPECTED, scenes):
        if not isinstance(scene, dict) or scene.get("filename") != expected:
            failures.append("Malformed scene record: " + expected)
            continue
        path = root / expected
        try:
            with path.open("rb") as handle:
                header = handle.read(24)
                if header[:8] != PNG_SIGNATURE or header[12:16] != b"IHDR":
                    raise ValueError("invalid PNG header")
                width, height = struct.unpack(">II", header[16:24])
                if (width, height) != (1080, 1920):
                    failures.append(f"{expected}: expected 1080x1920, got {width}x{height}")
                handle.seek(0)
                digest = hashlib.file_digest(handle, "sha256").hexdigest()
                digests.append(digest)
                if scene.get("sha256") != digest:
                    failures.append(expected + ": missing/mismatched SHA-256")
        except (OSError, ValueError, struct.error) as exc:
            failures.append(f"{expected}: unreadable asset ({exc})")
        for gate in ("visually_inspected", "single_scene_confirmed", "no_embedded_text_confirmed", "no_collage_confirmed", "continuity_checked"):
            if scene.get(gate) is not True:
                failures.append(f"{expected}: missing visual evidence {gate}")
        if not isinstance(scene.get("inspection_note"), str) or not scene["inspection_note"].strip():
            failures.append(expected + ": missing inspection note")
    if len(digests) != 7 or len(set(digests)) != 7:
        failures.append("Seven distinct image hashes required")
    return failures


def load_manifest(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))
