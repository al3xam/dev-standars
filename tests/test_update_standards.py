from __future__ import annotations

import importlib.util
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
UPDATER_PATH = REPOSITORY_ROOT / "scripts" / "update-standards.py"
SPEC = importlib.util.spec_from_file_location("update_standards", UPDATER_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("could not load update-standards.py")
UPDATER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(UPDATER)


class UpdateStandardsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory(prefix="update-standards-test-")
        self.root = Path(self.temporary_directory.name)
        self.source = self.root / "source"
        self.project = self.root / "project"
        self.source.mkdir()
        self.project.mkdir()
        self.write_source_file("README.md", "# Shared standards\nOriginal README.\n")
        self.write_source_file("GLOBAL.md", "# Global\nOriginal global rules.\n")
        self.write_source_file("git/WORKFLOW.md", "# Workflow\nOriginal workflow.\n")
        self.write_source_file("security/SECURITY.md", "# Security\nOriginal security rules.\n")
        self.write_source_file("testing/TESTING.md", "# Testing\nOriginal testing rules.\n")
        self.write_source_file("templates/project.yml", self.source_manifest("0.1.0"))
        self.write_source_file("scripts/create-project.sh", "#!/bin/sh\n")
        shutil.copy2(UPDATER_PATH, self.source / "scripts" / "update-standards.py")
        self.write_source_file(".github/prompts/updatestandards.prompt.md", "# Update prompt\n")

        UPDATER.build_candidate(self.source, "app", self.project)
        (self.project / ".dev-standards" / "project.yml").write_text(
            "schema_version: 1\n\n"
            "project:\n  name: test-app\n  type: app\n  components:\n    - web\n\n"
            "standards:\n  repository: \"example/dev-standards\"\n  version: \"0.1.0\"\n",
            encoding="utf-8",
        )
        UPDATER.write_baseline(
            self.project,
            self.project / ".dev-standards" / "managed-files.sha256",
        )

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def write_source_file(self, relative: str, content: str) -> None:
        path = self.source / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    @staticmethod
    def source_manifest(version: str) -> str:
        return (
            "schema_version: 1\n\n"
            "project:\n  name: standards-source\n  type: app\n  components: []\n\n"
            f"standards:\n  repository: \"example/dev-standards\"\n  version: \"{version}\"\n"
        )

    def run_updater(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(UPDATER_PATH), str(self.project), "--source", str(self.source), *arguments],
            capture_output=True,
            text=True,
            check=False,
        )

    def set_source_version(self, version: str) -> None:
        (self.source / "templates" / "project.yml").write_text(
            self.source_manifest(version),
            encoding="utf-8",
        )

    def test_noop_reports_current_version(self) -> None:
        result = self.run_updater()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Standards are up to date", result.stdout)

    def test_diff_only_does_not_write_and_apply_updates_manifest_and_baseline(self) -> None:
        global_path = self.source / "GLOBAL.md"
        global_path.write_text("# Global\nNew global rules.\n", encoding="utf-8")
        self.set_source_version("0.1.1")

        diff_result = self.run_updater()
        self.assertEqual(diff_result.returncode, 0, diff_result.stderr)
        self.assertIn("UPDATE", diff_result.stdout)
        self.assertIn("New global rules.", diff_result.stdout)
        installed_global = self.project / ".dev-standards" / "GLOBAL.md"
        self.assertNotIn("New global rules.", installed_global.read_text(encoding="utf-8"))

        apply_result = self.run_updater("--apply")
        self.assertEqual(apply_result.returncode, 0, apply_result.stderr)
        self.assertIn("New global rules.", installed_global.read_text(encoding="utf-8"))
        manifest = (self.project / ".dev-standards" / "project.yml").read_text(encoding="utf-8")
        self.assertIn('version: "0.1.1"', manifest)
        self.assertEqual(
            UPDATER.sha256(installed_global),
            UPDATER.load_baseline(self.project / ".dev-standards" / "managed-files.sha256")[
                ".dev-standards/GLOBAL.md"
            ],
        )

    def test_local_customization_aborts_whole_apply(self) -> None:
        installed_readme = self.project / ".dev-standards" / "README.md"
        installed_readme.write_text("# My local customization\n", encoding="utf-8")
        global_path = self.source / "GLOBAL.md"
        global_path.write_text("# Global\nUpstream update.\n", encoding="utf-8")
        (self.source / "README.md").write_text("# Shared standards\nUpstream README update.\n", encoding="utf-8")
        self.set_source_version("0.1.1")

        result = self.run_updater("--apply")
        self.assertEqual(result.returncode, 2)
        self.assertIn("locally modified managed file: .dev-standards/README.md", result.stdout)
        self.assertIn("My local customization", installed_readme.read_text(encoding="utf-8"))
        self.assertNotIn("Upstream update.", (self.project / ".dev-standards" / "GLOBAL.md").read_text(encoding="utf-8"))

    def test_apply_rejects_content_change_without_semver_bump(self) -> None:
        global_path = self.source / "GLOBAL.md"
        global_path.write_text("# Global\nUnreleased change.\n", encoding="utf-8")

        result = self.run_updater("--apply")
        self.assertEqual(result.returncode, 2)
        self.assertIn("without a version bump", result.stdout)
        self.assertNotIn("Unreleased change.", (self.project / ".dev-standards" / "GLOBAL.md").read_text(encoding="utf-8"))

    def test_downgrade_is_rejected(self) -> None:
        self.set_source_version("0.0.9")
        result = self.run_updater()
        self.assertEqual(result.returncode, 1)
        self.assertIn("downgrade refused", result.stderr)

    def test_missing_baseline_fails_without_changes(self) -> None:
        (self.project / ".dev-standards" / "managed-files.sha256").unlink()
        result = self.run_updater("--apply")
        self.assertEqual(result.returncode, 1)
        self.assertIn("no managed-file baseline", result.stderr)
        self.assertEqual(
            (self.project / ".dev-standards" / "GLOBAL.md").read_text(encoding="utf-8"),
            "# Global\nOriginal global rules.\n",
        )


if __name__ == "__main__":
    unittest.main()
