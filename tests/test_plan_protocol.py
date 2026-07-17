"""Verify deterministic Markdown-first plan creation, sealing, and recovery."""

from __future__ import annotations

import sys
from pathlib import Path
import tempfile
import unittest


SCRIPTS_ROOT = (
    Path(__file__).resolve().parents[1]
    / "skills"
    / "architect-propose"
    / "scripts"
)
sys.path.insert(0, str(SCRIPTS_ROOT))

import build_control
import make_plan
import plan_control
from plan_protocol import PlanProtocolError, read_utf8, write_utf8
from validate_plan import validate_package


def replace_agent_tokens(content: str, replacements: dict[str, str]) -> str:
    """Replace agent placeholders in a fixture with evidence-backed sample text.

    Args:
        content: Template-derived fixture content.
        replacements: Explicit token values required by the fixture.

    Returns:
        Filled fixture content.
    """

    for token, value in replacements.items():
        content = content.replace(f"{{{{AGENT:{token}}}}}", value)
    return content


class PlanProtocolTests(unittest.TestCase):
    """Exercise the deterministic package lifecycle using isolated Git worktrees."""

    def create_filled_plan(self) -> tuple[tempfile.TemporaryDirectory[str], Path, Path]:
        """Create one complete, sealable Chinese-language plan fixture.

        Returns:
            Temporary directory handle, repository root, and package root.
        """

        temporary_directory = tempfile.TemporaryDirectory()
        repo_root = Path(temporary_directory.name)
        (repo_root / ".git").mkdir()
        write_utf8(repo_root / "allowed.txt", "before")
        write_utf8(repo_root / "stable.txt", "stable")
        _, package = make_plan.create_plan(repo_root, "payment-state", "zh-Hans")
        design_path = plan_control.add_document(package, "design", "payment-state")
        task_path = plan_control.add_document(package, "task", "change-payment-state")

        root_replacements = {
            "Objective": "集中支付状态迁移。",
            "NonGoals": "不改变外部支付接口。",
            "ApprovedDesignBundle": "DesignIds: D-001\n- ApprovalEvidence: 用户在展示后的下一轮未拒绝该设计。\n- BundleSummary: 支付状态迁移设计已锁定。",
            "BuildEntryConditions": "现有状态文件存在且工作区独占。",
            "ObservedFacts": "状态由多个调用方直接写入。",
            "Assumptions": "没有未记录的状态消费者。",
            "CompatibilityIntent": "允许有意的内部重构。",
            "PreservedContracts": "保留支付结果字段。",
            "ExplicitlyBreakableContracts": "允许内部状态帮助函数变更。",
            "StopConditions": "发现新状态所有者时返回 Design。",
            "DesignIds": "D-001",
            "ApprovalEvidence": "用户在展示后的下一轮未拒绝 D-001。",
            "BundleDigest": "recorded-bundle",
            "DesignId": "D-001",
            "CanonicalConcept": "Finite State Machine",
            "DesignDigest": "recorded-design",
            "TaskId": "T-001",
            "DependsOn": "None",
            "DesignRefs": "D-001",
            "Summary": "集中状态转换。",
            "Path": "allowed.txt",
            "SymbolOrContract": "payment_state",
            "ChangeType": "modify",
            "AffectedCallers": "PaymentHandler",
            "Evidence": "repository inspection",
            "StableBoundaries": "Payment result fields remain stable.",
            "ProhibitedCrossBoundaryChanges": "Do not edit external API handlers.",
            "Category": "normal",
            "Scenario": "状态转换成功。",
            "CommandOrProcedure": "python -m unittest",
            "ExpectedResult": "通过。",
            "TaskIds": "T-001",
            "CompatibilityMigrationConcurrencyAndRollback": "验证回退不会修改稳定文件。",
        }
        for filename in (
            "00-plan-manifest.md",
            "01-context-and-contract.md",
            "02-design-catalog.md",
            "04-impact-and-boundaries.md",
            "05-task-catalog.md",
            "07-verification-plan.md",
        ):
            path = package / filename
            replacements = dict(root_replacements)
            if filename == "02-design-catalog.md":
                replacements["Path"] = "03-designs/D-001-payment-state.md"
            if filename == "05-task-catalog.md":
                replacements["Path"] = "06-tasks/T-001-change-payment-state.md"
            write_utf8(path, replace_agent_tokens(read_utf8(path), replacements))

        design_replacements = {
            "CanonicalName": "Finite State Machine",
            "Category": "Architectural Concept",
            "Reference": "https://martinfowler.com/eaaDev/EventSourcing.html",
            "Intent": "集中支付状态迁移。",
            "StableCoreAndVariation": "支付结果保持稳定，状态转换集中。",
            "Rationale": "避免多个调用方直接写状态。",
            "Alternatives": "拒绝在调用方保留条件分支。",
            "DesignBoundaries": "PaymentStateMachine owns all transitions.",
            "Counterexamples": "没有显式状态模型时不使用状态机。",
            "AntiPatterns": "禁止 Handler 直接写支付状态。",
        }
        design_content = replace_agent_tokens(read_utf8(design_path), design_replacements)
        design_content = design_content.replace("{{RULE:MUST_DO}}", "状态迁移只能由 PaymentStateMachine 执行。")
        design_content = design_content.replace("{{RULE:MUST_NOT_DO}}", "Handler 不得直接写支付状态。")
        write_utf8(design_path, design_content)

        task_replacements = {
            "DesignRefs": "D-001",
            "RuleRefs": "R-D001-001, R-D001-N001",
            "ProhibitedNewConcepts": "不得引入事件总线。",
            "Preconditions": "D-001 已获得批准。",
            "Path": "allowed.txt",
            "Symbol": "payment_state",
            "Operation": "modify",
            "AllowedDesignChange": "将状态写入集中到状态机。",
            "ExplicitlyOutOfScope": "stable.txt 和其他调用方。",
            "AtomicStep": "仅修改 allowed.txt 中的状态写入。",
            "ScopeCheckAndBreachRecovery": "越界后完整回退当前任务检查点。",
            "VerificationCommand": "python -m unittest",
            "ExpectedResult": "通过。",
            "CompletionCondition": "范围检查和实际验证都已记录。",
        }
        task_content = replace_agent_tokens(read_utf8(task_path), task_replacements)
        task_content = task_content.replace("{{RULE:MUST_DO}}", "只修改状态所有者。")
        task_content = task_content.replace("{{RULE:MUST_NOT_DO}}", "不得修改 stable.txt。")
        write_utf8(task_path, task_content)
        plan_control.seal_plan(package)
        return temporary_directory, repo_root, package

    def test_sealed_plan_validates(self) -> None:
        """A complete fixture must satisfy every static package validation gate."""

        temporary_directory, _, package = self.create_filled_plan()
        self.addCleanup(temporary_directory.cleanup)
        self.assertEqual(validate_package(package), [])

    def test_encoding_markers_fail_closed(self) -> None:
        """Known replacement markers must prevent a corrupted plan from validating."""

        temporary_directory, _, package = self.create_filled_plan()
        self.addCleanup(temporary_directory.cleanup)
        manifest_path = package / "00-plan-manifest.md"
        write_utf8(manifest_path, read_utf8(manifest_path) + "\n????\n")
        errors = validate_package(package)
        self.assertTrue(any("Suspicious encoding marker" in error for error in errors))

    def test_unknown_design_rule_fails_closed(self) -> None:
        """A task cannot cite a design rule that was never approved or generated."""

        temporary_directory, _, package = self.create_filled_plan()
        self.addCleanup(temporary_directory.cleanup)
        task_path = package / "06-tasks" / "T-001-change-payment-state.md"
        content = read_utf8(task_path).replace("R-D001-001", "R-D999-001")
        write_utf8(task_path, content)
        plan_control.seal_plan(package)
        errors = validate_package(package)
        self.assertTrue(any("unknown design rules" in error for error in errors))

    def test_declared_bundle_designs_fail_closed(self) -> None:
        """The approved bundle must declare exactly the design documents that exist."""

        temporary_directory, _, package = self.create_filled_plan()
        self.addCleanup(temporary_directory.cleanup)
        catalog_path = package / "02-design-catalog.md"
        content = read_utf8(catalog_path).replace("- DesignIds: D-001", "- DesignIds: D-999", 1)
        write_utf8(catalog_path, content)
        plan_control.seal_plan(package)
        errors = validate_package(package)
        self.assertTrue(any("ApprovedDesignBundle DesignIds reference unknown designs" in error for error in errors))

    def test_scope_breach_restores_complete_task_checkpoint(self) -> None:
        """A boundary breach must restore both allowed and unexpected source edits."""

        temporary_directory, repo_root, package = self.create_filled_plan()
        self.addCleanup(temporary_directory.cleanup)
        build_control.start_task(repo_root, package, "T-001")
        write_utf8(repo_root / "allowed.txt", "changed")
        self.assertEqual(
            build_control.check_scope(repo_root, package, "T-001"),
            {"allowed.txt"},
        )
        write_utf8(repo_root / "unexpected.txt", "unexpected")
        with self.assertRaises(PlanProtocolError):
            build_control.check_scope(repo_root, package, "T-001")
        self.assertEqual(read_utf8(repo_root / "allowed.txt"), "before\n")
        self.assertFalse((repo_root / "unexpected.txt").exists())

    def test_static_plan_drift_rolls_back_active_task(self) -> None:
        """Changing a sealed task document must invalidate and roll back its attempt."""

        temporary_directory, repo_root, package = self.create_filled_plan()
        self.addCleanup(temporary_directory.cleanup)
        build_control.start_task(repo_root, package, "T-001")
        write_utf8(repo_root / "allowed.txt", "changed")
        task_path = package / "06-tasks" / "T-001-change-payment-state.md"
        write_utf8(task_path, read_utf8(task_path) + "\nUnapproved change.\n")
        with self.assertRaises(PlanProtocolError):
            build_control.check_scope(repo_root, package, "T-001")
        self.assertEqual(read_utf8(repo_root / "allowed.txt"), "before\n")


if __name__ == "__main__":
    unittest.main()
