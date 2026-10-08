#!/usr/bin/env python3
"""Compare or update a project's installed development standards."""

from __future__ import annotations

import argparse
import difflib
import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path, PurePosixPath

MANIFEST_PATH = Path(".dev-standards/project.yml")
BASELINE_PATH = Path(".dev-standards/managed-files.sha256")


def fail(message: str, exit_code: int = 1) -> None:
    print(f"Error: {message}", file=sys.stderr)
    raise SystemExit(exit_code)


def read_simple_field(text: str, section: str, field: str) -> str:
    section_match = re.search(rf"(?m)^{re.escape(section)}:\s*\n((?:^[ \t]+.*\n?)*)", text)
    if not section_match:
        fail(f"missing '{section}' section in project manifest")
    match = re.search(
        rf"(?m)^  {re.escape(field)}:\s*['\"]?([^\s'\"#]+)",
        section_match.group(1),
    )
    if not match:
        fail(f"missing '{field}' in '{section}' section")
    return match.group(1)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_semver(value: str, label: str) -> tuple[int, int, int]:
    match = re.fullmatch(r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)", value)
    if not match:
        fail(f"{label} must use a stable SemVer version (MAJOR.MINOR.PATCH): {value}")
    return tuple(int(part) for part in match.groups())


def load_baseline(path: Path) -> dict[str, str]:
    if not path.is_file():
        fail(
            "no managed-file baseline found; this project must be created or "
            "adopted with a generator that records managed-files.sha256"
        )
    entries: dict[str, str] = {}
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        parts = line.split("  ", 1)
        if len(parts) != 2 or not re.fullmatch(r"[0-9a-f]{64}", parts[0]):
            fail(f"invalid baseline entry at {path}:{line_number}")
        relative = PurePosixPath(parts[1])
        if relative.is_absolute() or ".." in relative.parts:
            fail(f"unsafe path in managed-file baseline: {parts[1]}")
        entries[relative.as_posix()] = parts[0]
    return entries


def find_gh() -> str | None:
    executable = shutil.which("gh")
    if executable:
        return executable
    for candidate in ("/opt/homebrew/bin/gh", "/usr/local/bin/gh"):
        if Path(candidate).is_executable():
            return candidate
    return None


def clone_source(repository: str, destination: Path) -> None:
    gh = find_gh()
    if not gh:
        fail("GitHub CLI is required to fetch standards; pass --source for a local copy")
    auth = subprocess.run([gh, "auth", "status"], capture_output=True, text=True)
    if auth.returncode:
        fail("authenticate GitHub CLI with 'gh auth login' or pass --source")
    result = subprocess.run([gh, "repo", "clone", repository, str(destination), "--", "--depth=1"])
    if result.returncode:
        fail(f"could not clone standards repository {repository}")


def add_tree(source: Path, target_root: Path, source_relative: str, target_relative: str) -> None:
    source_path = source / source_relative
    if not source_path.exists():
        return
    target_path = target_root / target_relative
    if source_path.is_dir():
        for file_path in source_path.rglob("*"):
            if file_path.is_file():
                relative = file_path.relative_to(source_path)
                target = target_path / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(file_path, target)
    elif source_path.is_file():
        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_path, target_path)


def build_candidate(source: Path, project_type: str, target_root: Path) -> None:
    mappings = [
        ("README.md", ".dev-standards/README.md"),
        ("GLOBAL.md", ".dev-standards/GLOBAL.md"),
        ("git", ".dev-standards/git"),
        ("security", ".dev-standards/security"),
        ("testing", ".dev-standards/testing"),
        ("templates", ".dev-standards/templates"),
        ("scripts/create-project.sh", ".dev-standards/scripts/create-project.sh"),
        ("scripts/update-standards.py", ".dev-standards/scripts/update-standards.py"),
        (".github/prompts", ".github/prompts"),
    ]
    if project_type == "prestashop":
        mappings.append(("prestashop", ".dev-standards/prestashop"))
    for source_relative, target_relative in mappings:
        add_tree(source, target_root, source_relative, target_relative)


def indexed_files(root: Path) -> dict[str, Path]:
    files: dict[str, Path] = {}
    for base in (root / ".dev-standards", root / ".github/prompts"):
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if not path.is_file():
                continue
            relative = path.relative_to(root).as_posix()
            if relative in {MANIFEST_PATH.as_posix(), BASELINE_PATH.as_posix()}:
                continue
            files[relative] = path
    return files


def update_manifest(path: Path, repository: str, version: str) -> None:
    lines = path.read_text(encoding="utf-8").splitlines()
    try:
        section_index = lines.index("standards:")
    except ValueError:
        fail("project manifest has no standards section")

    section_end = section_index + 1
    while section_end < len(lines) and (not lines[section_end] or lines[section_end][0].isspace()):
        section_end += 1

    repository_found = False
    version_found = False
    for index in range(section_index + 1, section_end):
        if lines[index].startswith("  repository:"):
            lines[index] = f'  repository: "{repository}"'
            repository_found = True
        elif lines[index].startswith("  version:"):
            lines[index] = f'  version: "{version}"'
            version_found = True
    if not repository_found:
        lines.insert(section_index + 1, f'  repository: "{repository}"')
    if not version_found:
        lines.insert(section_index + 2 if not repository_found else section_index + 1, f'  version: "{version}"')
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_baseline(root: Path, destination: Path) -> None:
    files = indexed_files(root)
    lines = [f"{sha256(path)}  {relative}" for relative, path in sorted(files.items())]
    destination.write_text("\n".join(lines) + "\n", encoding="utf-8")


def diff_text(local_path: Path, incoming_path: Path, relative: str) -> str:
    try:
        local_lines = local_path.read_text(encoding="utf-8").splitlines(keepends=True)
        incoming_lines = incoming_path.read_text(encoding="utf-8").splitlines(keepends=True)
    except UnicodeDecodeError:
        return f"Binary file changed: {relative}\n"
    return "".join(
        difflib.unified_diff(
            local_lines,
            incoming_lines,
            fromfile=f"installed/{relative}",
            tofile=f"available/{relative}",
        )
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Compare installed standards; use --apply only after reviewing the diff."
    )
    parser.add_argument("project", nargs="?", default=".", help="project directory (default: current directory)")
    parser.add_argument("--source", help="local standards repository; defaults to the repository in project.yml")
    parser.add_argument("--apply", action="store_true", help="apply changes after conflict checks")
    args = parser.parse_args()

    project = Path(args.project).expanduser().resolve()
    manifest_path = project / MANIFEST_PATH
    if not manifest_path.is_file():
        fail(f"not a standards-enabled project: {project}")

    project_manifest = manifest_path.read_text(encoding="utf-8")
    repository = read_simple_field(project_manifest, "standards", "repository")
    installed_version = read_simple_field(project_manifest, "standards", "version")
    project_type = read_simple_field(project_manifest, "project", "type")
    installed_semver = parse_semver(installed_version, "installed standards version")
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository):
        fail(f"invalid standards repository in project manifest: {repository}")

    baseline = load_baseline(project / BASELINE_PATH)
    with tempfile.TemporaryDirectory(prefix="dev-standards-update-") as temporary_directory:
        temporary_root = Path(temporary_directory)
        if args.source:
            source = Path(args.source).expanduser().resolve()
            if not source.is_dir():
                fail(f"standards source is not a directory: {source}")
        else:
            source = temporary_root / "source"
            clone_source(repository, source)

        source_template = source / "templates/project.yml"
        if not source_template.is_file():
            fail(f"source is missing templates/project.yml: {source}")
        source_manifest = source_template.read_text(encoding="utf-8")
        latest_version = read_simple_field(source_manifest, "standards", "version")
        latest_semver = parse_semver(latest_version, "available standards version")
        if latest_semver < installed_semver:
            fail(f"standards downgrade refused: installed {installed_version}, available {latest_version}")
        candidate_root = temporary_root / "candidate"
        candidate_root.mkdir()
        build_candidate(source, project_type, candidate_root)
        candidate_files = indexed_files(candidate_root)

        changes: list[tuple[str, str, Path | None]] = []
        conflicts: list[str] = []
        all_paths = sorted(set(baseline) | set(candidate_files))
        for relative in all_paths:
            installed_path = project / relative
            expected_hash = baseline.get(relative)
            incoming_path = candidate_files.get(relative)
            installed_exists = installed_path.is_file()

            if expected_hash is not None:
                if not installed_exists:
                    conflicts.append(f"missing managed file: {relative}")
                    continue
                if sha256(installed_path) != expected_hash:
                    conflicts.append(f"locally modified managed file: {relative}")
                    continue
                if incoming_path is None:
                    changes.append(("delete", relative, None))
                elif sha256(installed_path) != sha256(incoming_path):
                    changes.append(("update", relative, incoming_path))
            elif incoming_path is not None:
                if installed_exists:
                    conflicts.append(f"new standard conflicts with existing local file: {relative}")
                else:
                    changes.append(("add", relative, incoming_path))

        print(f"Project: {project}")
        print(f"Standards repository: {repository}")
        print(f"Installed version: {installed_version}")
        print(f"Available version: {latest_version}")

        if conflicts:
            print("\nConflicts detected; no files will be changed:")
            for conflict in conflicts:
                print(f"  CONFLICT {conflict}")
                relative = conflict.split(": ", 1)[-1]
                installed_path = project / relative
                incoming_path = candidate_files.get(relative)
                if installed_path.is_file() and incoming_path is not None:
                    text_diff = diff_text(installed_path, incoming_path, relative)
                    if text_diff:
                        print(text_diff, end="")
            return 2

        if not changes:
            if latest_semver == installed_semver:
                print("\nStandards are up to date; no file changes detected.")
            else:
                print("\nNo managed file changes detected; only the standards version will advance.")
        else:
            print("\nProposed changes:")
            for operation, relative, incoming_path in changes:
                print(f"  {operation.upper():6} {relative}")
                installed_path = project / relative
                if operation == "update" and incoming_path is not None:
                    text_diff = diff_text(installed_path, incoming_path, relative)
                    if text_diff:
                        print(text_diff, end="")

        if changes and latest_semver == installed_semver:
            print(
                "\nUpstream content changed without a version bump. Update "
                "templates/project.yml before applying these standards."
            )
            if args.apply:
                return 2

        if not args.apply:
            print("\nNo files changed. Review the diff, then rerun with --apply to update.")
            return 0

        for operation, relative, incoming_path in changes:
            installed_path = project / relative
            if operation == "delete":
                installed_path.unlink()
            elif incoming_path is not None:
                installed_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(incoming_path, installed_path)

        update_manifest(manifest_path, repository, latest_version)
        write_baseline(project, project / BASELINE_PATH)
        print(f"\nStandards updated to {latest_version}. No commit or push was created.")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
