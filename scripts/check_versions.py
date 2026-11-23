#!/usr/bin/env python3
"""Version check for tripmate-docs.

Compares every Markdown document changed on this branch with the same
document on the base branch (normally the tip of origin/main) and fails
when, for any document with a `**Version:**` header:

- the new version is not the next one after the base version
  (1.5 -> 1.6, or 1.9 -> 2.0);
- the last row of its Version History table is not the new version;
- the version tag of the new version already exists.

A document that is new on this branch needs a history row for its
version and a free tag. Documents without a `**Version:**` header
(README.md, CLAUDE.md) are skipped.

Usage: python3 scripts/check_versions.py [--base origin/main]
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import PurePosixPath

VERSION_RE = re.compile(r"^\*\*Version:\*\*\s*(\d+)\.(\d+)", re.MULTILINE)
HISTORY_ROW_RE = re.compile(r"^\|\s*(\d+\.\d+)\s*\|\s*\d{4}-\d{2}-\d{2}\s*\|", re.MULTILINE)


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], check=True, capture_output=True, text=True
    ).stdout


def parse_version(text: str) -> tuple[int, int] | None:
    match = VERSION_RE.search(text)
    return (int(match.group(1)), int(match.group(2))) if match else None


def last_history_version(text: str) -> str | None:
    rows = HISTORY_ROW_RE.findall(text)
    return rows[-1] if rows else None


def is_next(base: tuple[int, int], new: tuple[int, int]) -> bool:
    return new == (base[0], base[1] + 1) or new == (base[0] + 1, 0)


def tag_name(path: str, version: str) -> str:
    p = PurePosixPath(path)
    if path == "prd.md":
        return f"v{version}"
    if path == "product-workflow.md":
        return f"workflow-v{version}"
    if p.name == "spec.md" and p.parent.parent.name == "specs":
        return f"{p.parent.name}-spec-v{version}"
    return f"{p.stem.lower()}-v{version}"


def fmt(version: tuple[int, int]) -> str:
    return f"{version[0]}.{version[1]}"


def check_document(
    path: str, base_text: str | None, head_text: str, tags: set[str]
) -> list[str]:
    errors: list[str] = []
    head = parse_version(head_text)
    base = parse_version(base_text) if base_text is not None else None
    if head is None:
        if base is not None:
            errors.append(f"{path}: the **Version:** header was removed")
        return errors
    if base is not None and not is_next(base, head):
        errors.append(
            f"{path}: version {fmt(head)} is not the next one after "
            f"{fmt(base)} on the base branch; rebase on main and take the next version"
        )
    last = last_history_version(head_text)
    if last != fmt(head):
        errors.append(
            f"{path}: the last Version History row is {last or 'missing'}, "
            f"expected {fmt(head)}"
        )
    tag = tag_name(path, fmt(head))
    if base != head and tag in tags:
        errors.append(f"{path}: tag {tag} already exists; take the next version")
    return errors


def changed_documents(base: str) -> list[str]:
    out = git("diff", "--name-only", "--diff-filter=AMR", f"{base}...HEAD", "--", "*.md")
    return [line for line in out.splitlines() if line]


def base_text(base: str, path: str) -> str | None:
    try:
        return git("show", f"{base}:{path}")
    except subprocess.CalledProcessError:
        return None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--base", default="origin/main")
    args = parser.parse_args(argv)

    tags = set(git("tag", "--list").split())
    errors: list[str] = []
    for path in changed_documents(args.base):
        with open(path, encoding="utf-8") as f:
            head_text = f.read()
        errors += check_document(path, base_text(args.base, path), head_text, tags)

    for error in errors:
        print(f"::error::{error}" if "GITHUB_ACTIONS" in os.environ else error)
    if not errors:
        print("Version check passed.")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
