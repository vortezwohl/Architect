# Task: T-002-route-entry-through-registry

## Metadata
- Document Type: Task
- Document ID: T-002
- Plan Name: reference-plan-example
- Created At: 2026-07-17:14:53:04.486
- Document Language: en

## Design Sources
- Source Design References: D-001, D-002
- Design Rule References: R-D001-001, R-D001-N001, R-D002-001, R-D002-002, R-D002-N001, R-D002-N002
- Prohibited New Concepts: No transport contract, branch-specific error envelope,
  or alternate dispatch path beside the registry.

## Preconditions
- T-001 has completed and D-001 and D-002 remain approved.

## Functional Boundary
- Requested Functionality: Route request entry through the registry and one error
  normalization point.
- Protected Functionality: Public request fields, handler business rules,
  error envelope, storage, deployment, and transport behavior remain unchanged.
- Explicit Non-Goals: New request fields, storage changes, and test rewrites are
  outside this task.
- Compatibility Guarantees: Existing callers receive the same successful and
  failed response semantics.
- Mandatory Stop Condition: Stop if registry routing or normalization cannot preserve
  the existing public contract.

## Code Impact Scope
| Likely Code Location | Relevant Symbol or Area | Expected Work | Evidence or Rationale |
| --- | --- | --- | --- |
| src/service/entry.py | handle_request | Route through registry | D-001 moves selection ownership. |
| src/service/error_contract.py | normalize_dispatch_error | Add normalization | D-002 freezes outward failures. |

## Impact Scope Expansion Procedure
- Initial Scope Rationale: Cover entry wiring, normalization, and any direct contract test
  helper needed to prove preserved behavior.
- Scope Expansion Decision Rule: Expand only after assessing callers and protected
  behavior, then choose the smallest viable implementation.
- Required Assessment and Record: Record each adaptation with alternatives,
  affected code, functional-boundary check, and verification.

## MUST DO
- M-T002-001: Delegate handler selection to the registry created in T-001.
- M-T002-002: Normalize failures through one shared error contract before returning.

## MUST NOT DO
- N-T002-001: Do not leave a second dispatch branch structure active beside the registry.
- N-T002-002: Do not leak raw internal exceptions to callers.

## Atomic Steps
1. Route handler selection through the registry.
2. Normalize outward failures through one shared point.
3. Remove redundant branch-owned dispatch logic while preserving public behavior.

## Functional Boundary Conflict Protocol
- Escalation Trigger: Routing entry through the registry would change the current public request or error envelope unless an adapter can preserve it.
- Required Conflict Analysis: Trace the entry callers and error normalization path. Compare retaining the current entry flow with a scoped adapter, and identify the evidence that the adapter preserves the protected contract.
- Recommended Option: `2`
- Recommendation Rationale: A narrow adapter can delegate selection to the registry while retaining the existing public request and error envelope.
- Decision Prompt: Reply with `1` to stop and preserve the current contract, or `2` to approve the scoped adapter.
- Decision Limit: This decision covers only the entry-routing conflict and its minimum necessary implementation scope.
- Required Decision Record: Record the selected option, the protected contract evidence, actual affected code, and verification outcome in execution state and log.

### Resolution Options
| Number | Resolution Path | Effect on Requested Functionality | Effect on Protected Functionality | Compatibility Consequences | Required Verification |
| --- | --- | --- | --- | --- | --- |
| 1 | Stop this task and retain the current entry flow. | Registry routing remains incomplete. | Public request and error behavior remain unchanged. | No caller-visible change. | Confirm that no routing change was applied. |
| 2 | Add the smallest entry adapter that delegates to the registry. | Completes registry routing. | Preserves the public request fields and error envelope. | Existing callers retain current success and failure behavior. | Verify successful requests, normalized failures, and focused regression coverage. |

## Required Verification Evidence
- Verification Procedure: Inspect routing and error normalization with contract checks.
- Required Evidence: Entry routes through the registry and outward errors
  preserve the existing envelope.

## Completion Criteria
Entry delegates dispatch and preserves caller-visible success and error behavior.
