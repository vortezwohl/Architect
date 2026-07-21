# Task: T-003-update-tests-for-dispatch-contract

## Metadata
- Document Type: Task
- Document ID: T-003
- Plan Name: reference-plan-example
- Created At: 2026-07-17:14:53:04.486
- Document Language: en

## Design Sources
- Source Design References: D-001, D-002
- Design Rule References: R-D001-001, R-D002-001, R-D002-002, R-D002-N001, R-D002-N002
- Prohibited New Concepts: No test-only dispatch behavior or public error variant.

## Preconditions
- T-001 and T-002 have completed and preserve caller-visible behavior.

## Functional Boundary
- Requested Functionality: Prove deterministic registry routing and preserved public
  request and error behavior.
- Protected Functionality: Production behavior, public contract assertions,
  and the existing test harness semantics remain unchanged.
- Explicit Non-Goals: New production behavior and a new test framework are outside
  this task.
- Compatibility Guarantees: Tests continue to assert existing caller-visible
  success and error behavior.
- Mandatory Stop Condition: Stop if required coverage needs production behavior changes
  or a protected contract relaxation.

## Code Impact Scope
| Likely Code Location | Relevant Symbol or Area | Expected Work | Evidence or Rationale |
| --- | --- | --- | --- |
| tests/test_dispatch_flow.py | request/error assertions | Update contract coverage | D-002 requires stable external failures. |
| tests/test_dispatch_registry.py | lookup coverage | Add focused selection tests | D-001 requires deterministic registry selection. |

## Impact Scope Expansion Procedure
- Initial Scope Rationale: Cover request-flow and registry behavior with the existing test facilities.
- Scope Expansion Decision Rule: Add a fixture or helper only after confirming it does
  not alter production behavior or test-harness semantics.
- Required Assessment and Record: Record every adaptation, its evidence, and the
  boundary-preservation verification.

## MUST DO
- M-T003-001: Add focused coverage for the registry boundary.
- M-T003-002: Preserve caller-visible success and error assertions in updated tests.

## MUST NOT DO
- N-T003-001: Do not rewrite tests to assert only internal details.
- N-T003-002: Do not remove caller-visible error contract assertions.

## Atomic Steps
1. Update request-flow tests without relaxing public assertions.
2. Add focused deterministic registry lookup coverage.

## Functional Boundary Conflict Protocol
- Escalation Trigger: Proving the dispatch contract requires changing protected test semantics, existing fixtures, or a stated non-goal.
- Required Conflict Analysis: Identify the missing proof, current fixture behavior, and the smallest test-only alternatives. Compare focused contract tests, a compatibility fixture, and an approved expectation change.
- Recommended Option: `2`
- Recommendation Rationale: Focused contract tests provide the required proof without changing protected test semantics or fixtures.
- Decision Prompt: Reply with `1` to stop and preserve current coverage, `2` to add focused contract tests, `3` to approve a compatibility fixture, or `4` to approve the described test-semantics change.
- Decision Limit: This decision covers only the demonstrated verification conflict and its minimum necessary implementation scope.
- Required Decision Record: Record the selected option, the missing proof, actual affected tests, and verification outcome in execution state and log.

### Resolution Options
| Number | Resolution Path | Effect on Requested Functionality | Effect on Protected Functionality | Compatibility Consequences | Required Verification |
| --- | --- | --- | --- | --- | --- |
| 1 | Stop this task and preserve current coverage. | The new dispatch contract remains unproven. | Existing tests and fixture semantics remain unchanged. | No behavior or fixture compatibility change. | Confirm that no test behavior was changed. |
| 2 | Add focused dispatch-contract tests. | Proves the requested dispatch behavior. | Preserves existing test semantics and fixtures. | Existing coverage remains valid. | Run focused contract checks and the full relevant suite. |
| 3 | Add the smallest compatibility fixture for both paths. | Proves both contract paths. | Preserves current fixtures while adding a controlled alternate setup. | Existing fixtures remain valid; one new compatibility fixture is maintained. | Verify both fixture modes and regression coverage. |
| 4 | Change the described test semantics after approval. | Can prove the requested behavior under revised expectations. | Changes protected test semantics. | Existing expectations or fixtures may need migration. | Verify the explicitly approved revised test contract. |

## Required Verification Evidence
- Verification Procedure: Run dispatch-related request, error, and registry tests.
- Required Evidence: Tests prove deterministic selection and preserved
  caller-visible behavior.

## Completion Criteria
Coverage proves the approved target functionality without changing protected behavior.
