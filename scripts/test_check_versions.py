"""Tests for check_versions.py. Run: python3 -m unittest discover -s scripts"""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_versions as cv  # noqa: E402


def doc(version: str, history: list[str] | None = None) -> str:
    rows = history if history is not None else [version]
    table = "\n".join(f"| {v} | 2026-11-23 | Change {v}. |" for v in rows)
    return (
        f"# Doc\n\n**Version:** {version}\\\n\nBody.\n\n## Version History\n\n"
        f"| Version | Date | Changes |\n|---------|------|---------|\n{table}\n"
    )


class UnitTests(unittest.TestCase):
    def test_next_minor_and_major(self):
        self.assertTrue(cv.is_next((1, 5), (1, 6)))
        self.assertTrue(cv.is_next((1, 9), (2, 0)))
        self.assertTrue(cv.is_next((1, 9), (1, 10)))
        self.assertFalse(cv.is_next((1, 5), (1, 5)))
        self.assertFalse(cv.is_next((1, 5), (1, 7)))
        self.assertFalse(cv.is_next((1, 6), (1, 5)))

    def test_tag_names(self):
        self.assertEqual(cv.tag_name("prd.md", "1.6"), "v1.6")
        self.assertEqual(cv.tag_name("product-workflow.md", "2.1"), "workflow-v2.1")
        self.assertEqual(
            cv.tag_name("docs/specs/epic-11/spec.md", "1.6"), "epic-11-spec-v1.6"
        )
        self.assertEqual(
            cv.tag_name("docs/development-flow.md", "1.9"), "development-flow-v1.9"
        )
        self.assertEqual(cv.tag_name("GLOSSARY.md", "1.9"), "glossary-v1.9")

    def test_valid_bump_passes(self):
        self.assertEqual(
            cv.check_document("a.md", doc("1.5"), doc("1.6", ["1.5", "1.6"]), set()), []
        )

    def test_same_version_fails(self):
        errors = cv.check_document("a.md", doc("1.5"), doc("1.5") + "more", set())
        self.assertTrue(any("not the next one" in e for e in errors))

    def test_other_machine_merged_first_fails(self):
        # main is already at 1.6; this branch also wrote 1.6 from 1.5
        errors = cv.check_document(
            "a.md", doc("1.6", ["1.5", "1.6"]), doc("1.6", ["1.5", "1.6"]) + "x", set()
        )
        self.assertTrue(any("not the next one" in e for e in errors))

    def test_skipped_version_fails(self):
        errors = cv.check_document("a.md", doc("1.5"), doc("1.7", ["1.5", "1.7"]), set())
        self.assertTrue(any("not the next one" in e for e in errors))

    def test_missing_history_row_fails(self):
        errors = cv.check_document("a.md", doc("1.5"), doc("1.6", ["1.5"]), set())
        self.assertTrue(any("Version History" in e for e in errors))

    def test_existing_tag_fails(self):
        errors = cv.check_document(
            "a.md", doc("1.5"), doc("1.6", ["1.5", "1.6"]), {"a-v1.6"}
        )
        self.assertTrue(any("already exists" in e for e in errors))

    def test_removed_header_fails(self):
        errors = cv.check_document("a.md", doc("1.5"), "# Doc\n", set())
        self.assertTrue(any("removed" in e for e in errors))

    def test_new_document_needs_history_row(self):
        self.assertEqual(cv.check_document("new.md", None, doc("1.0"), set()), [])
        errors = cv.check_document("new.md", None, doc("1.0", []), set())
        self.assertTrue(errors)

    def test_document_without_header_is_skipped(self):
        self.assertEqual(cv.check_document("README.md", "# R\n", "# R2\n", set()), [])


class GitTests(unittest.TestCase):
    """Runs main() in a throwaway repository with a base branch."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.cwd = os.getcwd()
        os.chdir(self.tmp.name)
        for cmd in (
            ["init", "-q", "-b", "main"],
            ["config", "user.email", "t@example.com"],
            ["config", "user.name", "t"],
        ):
            subprocess.run(["git", *cmd], check=True)
        Path("a.md").write_text(doc("1.5"))
        Path("README.md").write_text("# R\n")
        self.commit("base")
        subprocess.run(["git", "checkout", "-q", "-b", "work"], check=True)

    def tearDown(self):
        os.chdir(self.cwd)
        self.tmp.cleanup()

    def commit(self, msg: str):
        subprocess.run(["git", "add", "-A"], check=True)
        subprocess.run(["git", "commit", "-q", "-m", msg], check=True)

    def test_bump_passes(self):
        Path("a.md").write_text(doc("1.6", ["1.5", "1.6"]))
        Path("README.md").write_text("# R changed\n")
        self.commit("bump")
        self.assertEqual(cv.main(["--base", "main"]), 0)

    def test_race_with_main_fails(self):
        Path("a.md").write_text(doc("1.6", ["1.5", "1.6"]) + "mine\n")
        self.commit("mine")
        subprocess.run(["git", "checkout", "-q", "main"], check=True)
        Path("a.md").write_text(doc("1.6", ["1.5", "1.6"]) + "theirs\n")
        self.commit("theirs")
        subprocess.run(["git", "checkout", "-q", "work"], check=True)
        self.assertEqual(cv.main(["--base", "main"]), 1)


if __name__ == "__main__":
    unittest.main()
