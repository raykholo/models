#!/usr/bin/env python3
"""Checks the repository against the rules in README.md.

Every model sits in <format>/<model>/ beside a README.md that names the SHA-256 of each of its
files; file types match their folder; names are lower case with hyphens; no file is over 50 MB;
results follow results/README.md. Standard library only. Exit status 1 lists every violation.
"""

import hashlib
import re
import subprocess
import sys
from pathlib import Path

MAX_BYTES = 50 * 1024 * 1024
TEXTURES = {".png", ".jpg", ".jpeg", ".ktx2"}

# File types each format folder accepts, besides each model's README.md.
FORMATS = {
    "step": {".step", ".stp"},
    "iges": {".iges", ".igs"},
    "3mf": {".3mf"},
    "stl": {".stl"},
    "obj": {".obj", ".mtl"} | TEXTURES,
    "gltf": {".gltf", ".glb", ".bin"} | TEXTURES,
    "ply": {".ply"},
}

# Companion files (materials, buffers, textures) need no SHA-256 of their own in the README.
COMPANIONS = {".mtl", ".bin"} | TEXTURES

ROOT_FILES = {"README.md", "LICENSE", "DISCLAIMER.md", ".gitignore"}
ROOT_DIRS = set(FORMATS) | {"results", "scripts", ".github"}
NAME = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
RESULT = re.compile(r"^\d{4}-\d{2}-\d{2}-[a-z0-9]+(-[a-z0-9]+)*\.md$")
REQUIRED_FIELDS = ("Author", "Made with", "Size", "SHA-256")


def tracked_files(root: Path) -> list[Path]:
    out = subprocess.run(
        ["git", "ls-files", "-z"], cwd=root, capture_output=True, check=True
    ).stdout
    return [Path(p) for p in out.decode().split("\0") if p]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def check(root: Path) -> list[str]:
    errors = []
    models: dict[Path, list[Path]] = {}

    for rel in tracked_files(root):
        parts = rel.parts
        size = (root / rel).stat().st_size
        if size > MAX_BYTES:
            errors.append(f"{rel}: {size / 2**20:.1f} MB, over the 50 MB limit")

        if len(parts) == 1:
            if rel.name not in ROOT_FILES:
                errors.append(f"{rel}: not expected at the repository root")
            continue
        top = parts[0]
        if top not in ROOT_DIRS:
            errors.append(f"{rel}: {top}/ is not a format folder (see README.md, Formats)")
            continue
        if top in {"scripts", ".github"}:
            continue
        if top == "results":
            if len(parts) != 2 or not (
                rel.name in {"README.md", "TEMPLATE.md"} or RESULT.match(rel.name)
            ):
                errors.append(
                    f"{rel}: results are named results/<yyyy-mm-dd>-<handle>-<software>.md"
                )
            continue

        # A format folder: its README.md, or <format>/<model>/<file>.
        if len(parts) == 2:
            if rel.name != "README.md":
                errors.append(f"{rel}: models go in their own folder, {top}/<model>/")
            continue
        if len(parts) != 3:
            errors.append(f"{rel}: models are one level deep, {top}/<model>/<file>")
            continue
        model = parts[1]
        if not NAME.match(model):
            errors.append(f"{top}/{model}/: names are lower case with hyphens")
        if rel.name == "README.md":
            models.setdefault(rel.parent, [])
            continue
        if not NAME.match(rel.stem) or rel.suffix != rel.suffix.lower():
            errors.append(f"{rel}: names are lower case with hyphens")
        if rel.suffix.lower() not in FORMATS[top]:
            allowed = ", ".join(sorted(FORMATS[top]))
            errors.append(f"{rel}: {top}/ accepts {allowed}")
        models.setdefault(rel.parent, []).append(rel)

    for folder, files in sorted(models.items()):
        readme = root / folder / "README.md"
        if not readme.is_file():
            errors.append(f"{folder}/: no README.md (see README.md, Adding a model)")
            continue
        primary = [f for f in files if f.suffix.lower() not in COMPANIONS]
        if not primary:
            errors.append(f"{folder}/: a README.md but no model file")
        text = readme.read_text(encoding="utf-8")
        for field in REQUIRED_FIELDS:
            if field.lower() not in text.lower():
                errors.append(f"{folder}/README.md: missing {field}")
        for rel in primary:
            digest = sha256(root / rel)
            if digest not in text.lower():
                errors.append(f"{folder}/README.md: does not give {rel.name}'s SHA-256 {digest}")

    return errors


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent
    errors = check(root)
    for e in errors:
        print(f"error: {e}")
    if errors:
        print(f"{len(errors)} problem(s); the rules are in README.md.")
        return 1
    print("ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
