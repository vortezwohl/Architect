# Task: T-001-restore-multilingual-github-stars-badge

## Metadata
- DocumentType: Task
- DocumentId: T-001
- PlanName: restore-multilingual-github-stars-badge
- CreatedAt: 2026-07-19:17:35:20.192
- DocumentLanguage: en

## DesignSources
- SubdesignRefs: D-001
- RuleRefs: R-D001-001, R-D001-002, R-D001-N001, R-D001-N002
- ProhibitedNewConcepts: No README generator, template layer, repository URL
  migration, branding change, or unrelated localization synchronization.

## Preconditions
- D-001 is approved and recorded in this plan.
- The current four target lines still use the Architect Repo / open repo badge.
- The historical target line is confirmed from commit 3d7d667.
- Build has authorization to modify only the four README files in this task.

## ExactChangeBoundary
| Path | Symbol | Operation | AllowedImplementationDetail |
| --- | --- | --- | --- |
| README.md | Third top-level badge at line 13 | modify | Replace only the current Architect Repo badge with the exact historical GitHub Stars badge line. |
| i18n/README_zh-hans.md | Third top-level badge at line 13 | modify | Replace only the current Architect Repo badge with the exact historical GitHub Stars badge line. |
| i18n/README_zh-hant.md | Third top-level badge at line 13 | modify | Replace only the current Architect Repo badge with the exact historical GitHub Stars badge line. |
| i18n/README_ja-jp.md | Third top-level badge at line 13 | modify | Replace only the current Architect Repo badge with the exact historical GitHub Stars badge line. |

## ExplicitlyOutOfScope
- Do not modify any other README line or any file outside the four listed
  Markdown files.
- Do not change badge order, workflow badge, license badge, wordmark, prose,
  navigation, installation commands, or repository metadata.
- Do not add or modify tests, scripts, dependencies, or generated assets.

## MUST DO
- M-T001-001: Replace all four target lines with the exact historical GitHub Stars badge.
- M-T001-002: Run every verification command declared by this task and record observed results.

## MUST NOT DO
- N-T001-001: Do not leave any Architect Repo / open repo badge in the four target positions.
- N-T001-002: Do not change any content outside the four approved target lines.

## AtomicSteps
1. Replace the third badge line in each of the four approved README paths
   with the exact historical GitHub Stars line from commit 3d7d667.
2. Inspect all four target lines and compare their badge image and target URLs.
3. Inspect the bounded Git diff and run the encoding and whitespace checks.
4. Record the observed commands, results, and any remaining risk in task
   state and the execution log.

## ExecutionBoundaryRules
- Only the four target lines may be edited.
- If any additional change appears necessary, stop the task and report the
  boundary conflict instead of expanding scope.
- Do not replace the historical Agent-Architect URLs with a newer URL during
  this task; that would be a new compatibility decision.

## TaskDeclaredExecutionResults
- CommandOrProcedure: Inspect all four target lines, compare them to commit
  3d7d667, inspect the four-file diff, run git diff --check, and verify that
  the files have no UTF-8 BOM.
- ExpectedRecordedResult: All four exact historical badge lines are present;
  only the four approved lines changed; whitespace and encoding checks pass.

## CompletionCondition
The four README files contain the exact historical GitHub Stars badge line,
the bounded diff contains no unrelated changes, and all declared verification
commands have factual recorded results.
