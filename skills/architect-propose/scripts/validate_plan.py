"""Validate a sealed Markdown-first Architect plan package before Build.

Validation is intentionally fail-closed. It verifies deterministic structure,
English metadata fields, cross-document references, centralized execution state,
and encoding safety before Build can consume any agent-authored package content.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import re

from plan_protocol import (
    ROOT_DOCUMENTS,
    PlanProtocolError,
    compute_plan_digest,
    find_placeholders,
    load_state,
    parse_metadata,
    read_utf8,
)


DESIGN_FILE_PATTERN = re.compile(r"^(D-\d{3})-[a-z0-9]+(?:-[a-z0-9]+)*\.md$")
TASK_FILE_PATTERN = re.compile(r"^(T-\d{3})-[a-z0-9]+(?:-[a-z0-9]+)*\.md$")
DESIGN_RULE_PATTERN = re.compile(r"^- R-D\d{3}(?:-N\d{3}|-\d{3}): .+$", re.MULTILINE)
TASK_MUST_DO_PATTERN = re.compile(r"^- M-T\d{3}-\d{3}: .+$", re.MULTILINE)
TASK_MUST_NOT_PATTERN = re.compile(r"^- N-T\d{3}-\d{3}: .+$", re.MULTILINE)
RULE_REFERENCE_PATTERN = re.compile(r"R-D\d{3}(?:-N\d{3}|-\d{3})")
TASK_RULE_PATTERN = re.compile(r"[MN]-T\d{3}-\d{3}")
BUNDLE_DESIGN_ID_PATTERN = re.compile(r"^D-\d{3}$")


def validate_required_headings(path: Path, headings: tuple[str, ...]) -> list[str]:
    """Return missing fixed English headings for one plan document.

    Args:
        path: Markdown document to inspect.
        headings: Required heading strings.

    Returns:
        Validation errors for absent headings.
    """

    content = read_utf8(path)
    return [
        f"Missing heading '{heading}' in {path.relative_to(path.parents[1])}"
        for heading in headings
        if heading not in content
    ]


def table_rows(content: str, heading: str) -> list[list[str]]:
    """Parse non-header Markdown table rows in one fixed plan section.

    Args:
        content: Complete Markdown document content.
        heading: Exact section heading that owns the table.

    Returns:
        Parsed table cells without header or separator rows.
    """

    lines = content.splitlines()
    collecting = False
    rows: list[list[str]] = []
    for line in lines:
        if line == heading:
            collecting = True
            continue
        if collecting and line.startswith("## "):
            break
        if not collecting or not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if not cells or cells[0] in {"DesignId", "SubdesignId", "TaskId", "---"}:
            continue
        if set(cells[0]) == {"-"}:
            continue
        rows.append(cells)
    return rows


def section_fields(content: str, heading: str) -> dict[str, str]:
    """Parse bullet-style ``- Key: Value`` fields under one exact section heading.

    Args:
        content: Complete Markdown document content.
        heading: Exact section heading that owns the bullet fields.

    Returns:
        Parsed field mapping. Wrapped continuation lines are folded into the
        previous field value with spaces.
    """

    lines = content.splitlines()
    collecting = False
    current_key: str | None = None
    fields: dict[str, str] = {}
    for line in lines:
        if line == heading:
            collecting = True
            continue
        if collecting and line.startswith("## "):
            break
        if not collecting:
            continue
        if line.startswith("- "):
            payload = line[2:]
            if ": " not in payload:
                current_key = None
                continue
            key, value = payload.split(": ", 1)
            fields[key.strip()] = value.strip()
            current_key = key.strip()
            continue
        if current_key and line.startswith("  "):
            fields[current_key] = f"{fields[current_key]} {line.strip()}".strip()
    return fields


def validate_package(package_root: Path) -> list[str]:
    """Validate one complete plan package without changing its contents.

    Args:
        package_root: Selected plan package root.

    Returns:
        Validation error messages. An empty list means the package is buildable.
    """

    errors: list[str] = []
    manifest_path = package_root / "00-plan-manifest.md"
    if not manifest_path.is_file():
        return [f"Missing required document: {manifest_path.name}"]
    try:
        manifest = parse_metadata(manifest_path)
    except PlanProtocolError as error:
        return [str(error)]

    for filename, (document_type, document_id) in ROOT_DOCUMENTS.items():
        path = package_root / filename
        if not path.is_file():
            errors.append(f"Missing required document: {filename}")
            continue
        try:
            metadata = parse_metadata(path)
            if metadata.document_type != document_type:
                errors.append(f"Invalid DocumentType in {filename}")
            if metadata.document_id != document_id:
                errors.append(f"Invalid DocumentId in {filename}")
            if metadata.plan_name != manifest.plan_name:
                errors.append(f"PlanName mismatch in {filename}")
            if metadata.document_language != manifest.document_language:
                errors.append(f"DocumentLanguage mismatch in {filename}")
            if path.name != "08-execution-log.md" and find_placeholders(path):
                errors.append(f"Unresolved placeholders in {filename}")
        except PlanProtocolError as error:
            errors.append(str(error))

    design_directory = package_root / "03-designs"
    task_directory = package_root / "06-tasks"
    if not design_directory.is_dir():
        errors.append("Missing required directory: 03-designs")
    if not task_directory.is_dir():
        errors.append("Missing required directory: 06-tasks")
    design_paths = sorted(design_directory.glob("*.md")) if design_directory.is_dir() else []
    task_paths = sorted(task_directory.glob("*.md")) if task_directory.is_dir() else []
    if not design_paths:
        errors.append("Plan must contain at least one design document.")
    if not task_paths:
        errors.append("Plan must contain at least one task document.")

    try:
        design_catalog = read_utf8(package_root / "02-design-catalog.md")
        task_catalog = read_utf8(package_root / "05-task-catalog.md")
    except (OSError, PlanProtocolError) as error:
        return errors + [str(error)]
    approved_bundle_fields = section_fields(
        design_catalog,
        "## ApprovedDesignBundle",
    )
    required_bundle_fields = ("DesignIds", "ApprovalEvidence", "BundleDigest")
    missing_bundle_fields = [
        field_name
        for field_name in required_bundle_fields
        if not approved_bundle_fields.get(field_name, "").strip()
    ]
    if missing_bundle_fields:
        errors.append(
            "ApprovedDesignBundle is missing required fields: "
            f"{', '.join(missing_bundle_fields)}",
        )
    declared_design_ids = {
        item.strip()
        for item in approved_bundle_fields.get("DesignIds", "").split(",")
        if item.strip()
    }
    invalid_declared_design_ids = {
        design_id
        for design_id in declared_design_ids
        if not BUNDLE_DESIGN_ID_PATTERN.fullmatch(design_id)
    }
    if invalid_declared_design_ids:
        errors.append(
            "ApprovedDesignBundle contains invalid DesignIds: "
            f"{', '.join(sorted(invalid_declared_design_ids))}",
        )
    design_catalog_rows = {
        row[0]: row
        for row in table_rows(design_catalog, "## Designs")
        if len(row) == 4
    }
    task_catalog_rows = {
        row[0]: row
        for row in table_rows(task_catalog, "## Tasks")
        if len(row) == 6
    }
    design_ids: set[str] = set()
    design_rule_ids: set[str] = set()
    rule_owners: dict[str, str] = {}
    task_ids: set[str] = set()
    for path in design_paths:
        match = DESIGN_FILE_PATTERN.fullmatch(path.name)
        if not match:
            errors.append(f"Invalid design filename: {path.name}")
            continue
        design_id = match.group(1)
        design_ids.add(design_id)
        try:
            metadata = parse_metadata(path)
            if metadata.document_type != "Design" or metadata.document_id != design_id:
                errors.append(f"Design metadata mismatch: {path.name}")
            if metadata.plan_name != manifest.plan_name:
                errors.append(f"PlanName mismatch: {path.name}")
            if find_placeholders(path):
                errors.append(f"Unresolved placeholders in {path.name}")
            errors.extend(
                validate_required_headings(
                    path,
                    (
                        "## Concept",
                        "## Counterexamples",
                        "## AntiPatterns",
                        "### MUST DO",
                        "### MUST NOT DO",
                    ),
                ),
            )
            content = read_utf8(path)
            if not DESIGN_RULE_PATTERN.search(content):
                errors.append(f"Missing generated design rule in {path.name}")
            expected_rule_prefix = f"R-{design_id.replace('-', '')}"
            for rule_id in RULE_REFERENCE_PATTERN.findall(content):
                if not rule_id.startswith(expected_rule_prefix):
                    errors.append(
                        f"Design rule does not belong to {design_id} in {path.name}: "
                        f"{rule_id}",
                    )
                design_rule_ids.add(rule_id)
                rule_owners[rule_id] = design_id
            catalog_row = design_catalog_rows.get(design_id)
            if catalog_row is None:
                errors.append(f"Design catalog does not reference {path.name}")
            elif catalog_row[1] != path.relative_to(package_root).as_posix():
                errors.append(f"Design catalog path mismatch for {design_id}")
            elif not catalog_row[3].strip():
                errors.append(f"Design catalog is missing DesignDigest for {design_id}")
            if design_id not in design_catalog or path.relative_to(package_root).as_posix() not in design_catalog:
                errors.append(f"Design catalog does not reference {path.name}")
        except PlanProtocolError as error:
            errors.append(str(error))

    catalog_design_ids = set(design_catalog_rows)
    extra_catalog_designs = catalog_design_ids - design_ids
    if extra_catalog_designs:
        errors.append(
            "Design catalog references design files that do not exist: "
            f"{', '.join(sorted(extra_catalog_designs))}",
        )
    missing_catalog_designs = design_ids - catalog_design_ids
    if missing_catalog_designs:
        errors.append(
            "Design catalog is missing design rows for: "
            f"{', '.join(sorted(missing_catalog_designs))}",
        )
    if declared_design_ids != design_ids:
        missing_from_bundle = design_ids - declared_design_ids
        extra_in_bundle = declared_design_ids - design_ids
        if missing_from_bundle:
            errors.append(
                "ApprovedDesignBundle DesignIds are missing design documents for: "
                f"{', '.join(sorted(missing_from_bundle))}",
            )
        if extra_in_bundle:
            errors.append(
                "ApprovedDesignBundle DesignIds reference unknown designs: "
                f"{', '.join(sorted(extra_in_bundle))}",
            )

    for path in task_paths:
        match = TASK_FILE_PATTERN.fullmatch(path.name)
        if not match:
            errors.append(f"Invalid task filename: {path.name}")
            continue
        task_id = match.group(1)
        task_ids.add(task_id)
        try:
            metadata = parse_metadata(path)
            if metadata.document_type != "Task" or metadata.document_id != task_id:
                errors.append(f"Task metadata mismatch: {path.name}")
            if metadata.plan_name != manifest.plan_name:
                errors.append(f"PlanName mismatch: {path.name}")
            if find_placeholders(path):
                errors.append(f"Unresolved placeholders in {path.name}")
            errors.extend(
                validate_required_headings(
                    path,
                    (
                        "## DesignSources",
                        "## ExactChangeBoundary",
                        "## MUST DO",
                        "## MUST NOT DO",
                        "## ExecutionBoundaryRules",
                        "## TaskDeclaredExecutionResults",
                    ),
                ),
            )
            content = read_utf8(path)
            if not TASK_MUST_DO_PATTERN.search(content):
                errors.append(f"Missing generated MUST DO rule in {path.name}")
            if not TASK_MUST_NOT_PATTERN.search(content):
                errors.append(f"Missing generated MUST NOT DO rule in {path.name}")
            expected_task_rule_prefixes = (f"M-{task_id.replace('-', '')}", f"N-{task_id.replace('-', '')}")
            for rule_id in TASK_RULE_PATTERN.findall(content):
                if not rule_id.startswith(expected_task_rule_prefixes):
                    errors.append(
                        f"Task rule does not belong to {task_id} in {path.name}: {rule_id}",
                    )
            references: set[str] = set()
            if not re.search(r"^- SubdesignRefs: D-\d{3}(?:, D-\d{3})*$", content, re.MULTILINE):
                errors.append(f"Invalid SubdesignRefs in {path.name}")
            else:
                design_reference_line = re.search(
                    r"^- SubdesignRefs: (.+)$",
                    content,
                    re.MULTILINE,
                )
                if design_reference_line:
                    references = {
                        item.strip()
                        for item in design_reference_line.group(1).split(",")
                    }
                    unknown_designs = references - design_ids
                    if unknown_designs:
                        errors.append(
                            f"Task references unknown subdesigns in {path.name}: "
                            f"{', '.join(sorted(unknown_designs))}",
                        )
            rule_reference_line = re.search(
                r"^- RuleRefs: (.+)$",
                content,
                re.MULTILINE,
            )
            if not rule_reference_line:
                errors.append(f"Missing RuleRefs in {path.name}")
            else:
                rule_references = {
                    item.strip()
                    for item in rule_reference_line.group(1).split(",")
                }
                unknown_rules = rule_references - design_rule_ids
                if unknown_rules:
                    errors.append(
                        f"Task references unknown design rules in {path.name}: "
                        f"{', '.join(sorted(unknown_rules))}",
                    )
                unrelated_rules = {
                    rule_id
                    for rule_id in rule_references
                    if rule_owners.get(rule_id) not in references
                }
                if unrelated_rules:
                    errors.append(
                        f"Task references rules outside SubdesignRefs in {path.name}: "
                        f"{', '.join(sorted(unrelated_rules))}",
                    )
            if not re.search(r"^\| [^|]+ \| [^|]+ \| (?:create|modify|delete) \| [^|]+ \|$", content, re.MULTILINE):
                errors.append(f"Missing exact path/symbol/operation boundary in {path.name}")
            catalog_row = task_catalog_rows.get(task_id)
            if catalog_row is None:
                errors.append(f"Task catalog does not reference {path.name}")
            elif catalog_row[2] != path.relative_to(package_root).as_posix():
                errors.append(f"Task catalog path mismatch for {task_id}")
        except PlanProtocolError as error:
            errors.append(str(error))

    try:
        state = load_state(package_root)
        if state.get("PlanDigest") != compute_plan_digest(package_root):
            errors.append("Execution state PlanDigest does not match immutable documents.")
        tasks = state.get("Tasks")
        if not isinstance(tasks, dict) or set(tasks) != task_ids:
            errors.append("Execution state Tasks do not exactly match task documents.")
    except PlanProtocolError as error:
        errors.append(str(error))

    manifest_content = read_utf8(manifest_path)
    match = re.search(r"^- PlanDigest: ([0-9a-f]{64})$", manifest_content, re.MULTILINE)
    if not match:
        errors.append("PlanManifest must contain a sealed SHA-256 PlanDigest.")
    elif match.group(1) != compute_plan_digest(package_root):
        errors.append("PlanManifest PlanDigest does not match immutable documents.")
    return errors


def main() -> int:
    """Parse arguments, print all validation failures, and return an exit status.

    Returns:
        Process exit status.
    """

    parser = argparse.ArgumentParser(
        description="Validate a sealed Markdown-first Architect plan package.",
    )
    parser.add_argument("--repo-root", required=True, type=Path)
    parser.add_argument("--plan", required=True)
    arguments = parser.parse_args()
    package_root = arguments.repo_root.resolve() / ".architect" / arguments.plan
    try:
        errors = validate_package(package_root)
    except (OSError, PlanProtocolError) as error:
        errors = [str(error)]
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"VALID: {package_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
