"""Tests for check.py: python3 -m unittest discover scripts"""

import hashlib
import subprocess
import tempfile
import unittest
from pathlib import Path

from check import check

STEP = b"ISO-10303-21;\nEND-ISO-10303-21;\n"


def readme(digest: str) -> str:
    return (
        "# Bracket\n\n- Author: A. Person\n- Made with: SolidCraft 1.0, AP242\n"
        f"- Size: 1 body, 12 faces\n- SHA-256: {digest}\n"
    )


class CheckTest(unittest.TestCase):
    def setUp(self):
        self._dir = tempfile.TemporaryDirectory()
        self.root = Path(self._dir.name)
        subprocess.run(["git", "init", "-q"], cwd=self.root, check=True)
        self.write("README.md", "# Models\n")
        self.write("step/README.md", "# STEP\n")

    def tearDown(self):
        self._dir.cleanup()

    def write(self, rel: str, content):
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(content, str):
            path.write_text(content)
        else:
            path.write_bytes(content)
        subprocess.run(["git", "add", rel], cwd=self.root, check=True)

    def errors(self):
        return check(self.root)

    def test_a_complete_model_passes(self):
        self.write("step/bracket/bracket.step", STEP)
        self.write("step/bracket/README.md", readme(hashlib.sha256(STEP).hexdigest()))
        self.assertEqual(self.errors(), [])

    def test_a_wrong_sha256_fails(self):
        self.write("step/bracket/bracket.step", STEP)
        self.write("step/bracket/README.md", readme("0" * 64))
        self.assertTrue(any("SHA-256" in e for e in self.errors()))

    def test_a_model_without_readme_fails(self):
        self.write("step/bracket/bracket.step", STEP)
        self.assertTrue(any("no README.md" in e for e in self.errors()))

    def test_a_native_cad_file_fails(self):
        self.write("step/bracket/bracket.sldprt", b"x")
        self.write("step/bracket/README.md", readme("0" * 64))
        self.assertTrue(any("accepts" in e for e in self.errors()))

    def test_an_unknown_folder_fails(self):
        self.write("parasolid/bracket/bracket.x_t", b"x")
        self.assertTrue(any("not a format folder" in e for e in self.errors()))

    def test_upper_case_names_fail(self):
        self.write("step/Bracket/Bracket.STEP", STEP)
        self.write("step/Bracket/README.md", readme(hashlib.sha256(STEP).hexdigest()))
        self.assertTrue(any("lower case" in e for e in self.errors()))

    def test_results_need_a_dated_name(self):
        self.write("results/my-results.md", "# x\n")
        self.assertTrue(any("results/" in e for e in self.errors()))
        self.write("results/2026-10-20-jdoe-freecad.md", "# x\n")
        self.assertEqual(len(self.errors()), 1)


if __name__ == "__main__":
    unittest.main()
