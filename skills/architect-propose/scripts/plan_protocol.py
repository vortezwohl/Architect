"""Provide deterministic utilities for the Markdown-first Architect plan protocol.

The protocol keeps design and task intent in Markdown while reserving JSON for
mutable execution state. This module owns the deterministic concerns shared by
the plan creation, validation, and build-control commands.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import hashlib
import json
from pathlib import Path
import re
from typing import Iterable


PLAN_NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
DOCUMENT_ID_PATTERN = re.compile(r"^(?:PLAN|CONTEXT|DESIGN-CATALOG|IMPACT|TASK-CATALOG|VERIFICATION|EXECUTION-LOG|D-\d{3}|T-\d{3})$")
PLACEHOLDER_PATTERN = re.compile(r"\{\{(?:AGENT|GENERATED|RULE):[^}]+}}")
FIELD_PATTERN = re.compile(
    r"^- ([A-Za-z][A-Za-z0-9]*(?: [A-Za-z][A-Za-z0-9]*)*): (.+)$",
    re.MULTILINE,
)
SUSPICIOUS_TEXT_MARKERS = ("\ufffd", "????", "鈥", "锟", "蹇")
ROOT_DOCUMENTS = {
    "00-plan-manifest.md": ("Plan Manifest", "PLAN"),
    "01-context-and-contract.md": ("Context and Contract", "CONTEXT"),
    "02-design-catalog.md": ("Design Catalog", "DESIGN-CATALOG"),
    "04-impact-and-boundaries.md": ("Impact and Boundaries", "IMPACT"),
    "05-task-catalog.md": ("Task Catalog", "TASK-CATALOG"),
    "07-verification-plan.md": ("Verification Plan", "VERIFICATION"),
    "08-execution-log.md": ("Execution Log", "EXECUTION-LOG"),
}


class PlanProtocolError(ValueError):
    """Represent a deterministic plan protocol validation failure."""


@dataclass(frozen=True)
class DocumentMetadata:
    """Describe the fixed metadata stored in an Architect Markdown document.

    Args:
        document_type: Fixed English document type.
        document_id: Generated identifier for the document.
        plan_name: Generated plan name shared by the package.
        created_at: Generated local timestamp with millisecond precision.
        document_language: User-facing prose language tag.
    """

    document_type: str
    document_id: str
    plan_name: str
    created_at: str
    document_language: str


def current_timestamp() -> str:
    """Return the required local timestamp representation.

    Returns:
        A local timestamp formatted as ``YYYY-MM-DD:hh:mm:ss.sss``.
    """

    return datetime.now().strftime("%Y-%m-%d:%H:%M:%S.%f")[:-3]


def validate_plan_name(plan_name: str) -> None:
    """Validate a generated or requested plan name.

    Args:
        plan_name: Candidate lower-case kebab-case plan name.

    Raises:
        PlanProtocolError: Raised when the name is not valid kebab-case.
    """

    if not PLAN_NAME_PATTERN.fullmatch(plan_name):
        raise PlanProtocolError(
            "Plan Name must use lower-case kebab-case letters, numbers, and hyphens.",
        )


def read_utf8(path: Path) -> str:
    """Read one UTF-8 without BOM document and reject known corruption markers.

    Args:
        path: Text document path.

    Returns:
        Decoded document content.

    Raises:
        PlanProtocolError: Raised for invalid encoding, BOM, or suspicious text.
    """

    payload = path.read_bytes()
    if payload.startswith(b"\xef\xbb\xbf"):
        raise PlanProtocolError(f"UTF-8 BOM is forbidden: {path}")
    try:
        content = payload.decode("utf-8", errors="strict")
    except UnicodeDecodeError as error:
        raise PlanProtocolError(f"Invalid UTF-8 text: {path}") from error
    content = content.replace("\r\n", "\n").replace("\r", "\n")

    for marker in SUSPICIOUS_TEXT_MARKERS:
        if marker in content:
            raise PlanProtocolError(
                f"Suspicious encoding marker '{marker}' found in {path}",
            )
    return content


def write_utf8(path: Path, content: str) -> None:
    """Write one UTF-8 without BOM document with a final line ending.

    Args:
        path: Target document path.
        content: Complete text content to persist.
    """

    normalized = content.replace("\r\n", "\n").replace("\r", "\n")
    if not normalized.endswith("\n"):
        normalized += "\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(normalized, encoding="utf-8", newline="\n")


def replace_generated_fields(
    content: str,
    replacements: dict[str, str],
) -> str:
    """Replace deterministic template tokens without changing agent text.

    Args:
        content: Template or document text.
        replacements: Generated token names and replacement values.

    Returns:
        Document text with the specified generated tokens replaced.
    """

    for field_name, value in replacements.items():
        content = content.replace(f"{{{{GENERATED:{field_name}}}}}", value)
    return content


def parse_metadata(path: Path) -> DocumentMetadata:
    """Parse and validate the required fixed metadata fields in one document.

    Args:
        path: Markdown document path.

    Returns:
        Parsed document metadata.

    Raises:
        PlanProtocolError: Raised when a required field is absent or invalid.
    """

    # Strip metadata values so CRLF line endings do not leak `\r` into
    # deterministic identifiers such as PLAN, CONTEXT, D-001, or T-001.
    fields = {
        key: value.strip()
        for key, value in FIELD_PATTERN.findall(read_utf8(path))
    }
    required_fields = (
        "Document Type",
        "Document ID",
        "Plan Name",
        "Created At",
        "Document Language",
    )
    missing = [field_name for field_name in required_fields if field_name not in fields]
    if missing:
        raise PlanProtocolError(f"Missing metadata fields in {path}: {', '.join(missing)}")
    if not DOCUMENT_ID_PATTERN.fullmatch(fields["Document ID"]):
        raise PlanProtocolError(f"Invalid Document ID in {path}: {fields['Document ID']}")
    try:
        datetime.strptime(fields["Created At"], "%Y-%m-%d:%H:%M:%S.%f")
    except ValueError as error:
        raise PlanProtocolError(
            f"Created At must use YYYY-MM-DD:hh:mm:ss.sss in {path}",
        ) from error
    validate_plan_name(fields["Plan Name"])
    if not fields["Document Language"].strip():
        raise PlanProtocolError(f"Document Language must not be empty in {path}")
    return DocumentMetadata(
        document_type=fields["Document Type"],
        document_id=fields["Document ID"],
        plan_name=fields["Plan Name"],
        created_at=fields["Created At"],
        document_language=fields["Document Language"],
    )


def find_placeholders(path: Path) -> list[str]:
    """Return unresolved generated, agent, and rule placeholders in one document.

    Args:
        path: Markdown document path.

    Returns:
        Placeholder tokens that require resolution before `architect-build`.
    """

    return PLACEHOLDER_PATTERN.findall(read_utf8(path))


def markdown_documents(package_root: Path) -> list[Path]:
    """Return all plan Markdown documents in deterministic path order.

    Args:
        package_root: Plan package root.

    Returns:
        Sorted Markdown paths outside the mutable state directory.
    """

    return sorted(
        path
        for path in package_root.rglob("*.md")
        if ".state" not in path.parts
    )


def compute_plan_digest(package_root: Path) -> str:
    """Compute a stable digest for immutable plan documents.

    The execution log is intentionally excluded because the `architect-build`
    stage appends facts after
    the plan is sealed. The manifest digest field is normalized before hashing to
    avoid a self-referential digest.

    Args:
        package_root: Plan package root.

    Returns:
        Lower-case SHA-256 hexadecimal digest.
    """

    digest = hashlib.sha256()
    for path in markdown_documents(package_root):
        if path.name == "08-execution-log.md":
            continue
        relative_path = path.relative_to(package_root).as_posix()
        content = read_utf8(path)
        if path.name == "00-plan-manifest.md":
            content = re.sub(
                r"^- Plan Digest: .+$",
                "- Plan Digest: {{GENERATED:Plan Digest}}",
                content,
                flags=re.MULTILINE,
            )
        digest.update(relative_path.encode("utf-8"))
        digest.update(b"\0")
        digest.update(content.encode("utf-8"))
        digest.update(b"\0")
    return digest.hexdigest()


def load_state(package_root: Path) -> dict[str, object]:
    """Load the centralized mutable execution state.

    Args:
        package_root: Plan package root.

    Returns:
        Decoded state object.

    Raises:
        PlanProtocolError: Raised when the state file is absent or malformed.
    """

    state_path = package_root / ".state" / "execution-state.json"
    try:
        return json.loads(read_utf8(state_path))
    except json.JSONDecodeError as error:
        raise PlanProtocolError(f"Invalid execution state JSON: {state_path}") from error


def write_state(package_root: Path, state: dict[str, object]) -> None:
    """Persist centralized execution state with deterministic JSON formatting.

    Args:
        package_root: Plan package root.
        state: Complete state object to persist.
    """

    payload = json.dumps(state, ensure_ascii=False, indent=2, sort_keys=True)
    write_utf8(package_root / ".state" / "execution-state.json", payload)


def next_document_id(paths: Iterable[Path], prefix: str) -> str:
    """Allocate the first non-conflicting generated design or task identifier.

    Args:
        paths: Existing document paths.
        prefix: ``D`` for designs or ``T`` for tasks.

    Returns:
        The first unused three-digit identifier for the requested prefix.
    """

    used_ids = set()
    expression = re.compile(rf"^{re.escape(prefix)}-(\d{{3}})-")
    for path in paths:
        match = expression.match(path.name)
        if match:
            used_ids.add(int(match.group(1)))
    candidate = 1
    while candidate in used_ids:
        candidate += 1
    return f"{prefix}-{candidate:03d}"
