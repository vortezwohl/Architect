# Task: T-001-create-dispatch-registry

## Metadata
- Document Type: Task
- Document ID: T-001
- Plan Name: reference-plan-example
- Created At: 2026-07-17:14:53:04.486
- Document Language: en

## Design Sources
- Source Design References: D-001
- Design Rule References: R-D001-001, R-D001-002, R-D001-N001, R-D001-N002
- Prohibited New Concepts: No plugin framework, reflection-based discovery, or
  duplicate branch-owned dispatch table.

## Preconditions
- D-001 is approved and no registry module exists yet.

## Functional Boundary
- Requested Functionality: Create one explicit registry that owns handler selection.
- Protected Functionality: Request parsing, handler business rules, and
  public request and error behavior remain unchanged.
- Explicit Non-Goals: Request entry rewiring, runtime plugins, and transport
  changes are outside this task.
- Compatibility Guarantees: Existing callers observe no public behavior change.
- Mandatory Stop Condition: Stop if registry creation requires changing protected
  behavior or adding a prohibited runtime extension mechanism.

## Code Impact Scope
| Likely Code Location | Relevant Symbol or Area | Expected Work | Evidence or Rationale |
| --- | --- | --- | --- |
| src/service/dispatch_registry.py | DispatchRegistry | Add registry and lookup | D-001 assigns selection ownership here. |

## Impact Scope Expansion Procedure
- Initial Scope Rationale: Cover the new registry module and likely focused test helpers.
- Scope Expansion Decision Rule: Add a necessary helper or fixture only after confirming
  it preserves the functional boundary and is the smallest viable choice.
- Required Assessment and Record: Record the evidence, alternatives, affected
  locations, and verification for every impact-scope adaptation.

## MUST DO
- M-T001-001: Create one explicit registry module that owns handler selection.
- M-T001-002: Keep the registration surface readable and static in repository code.

## MUST NOT DO
- N-T001-001: Do not add reflection, plugin loading, or import side effects.
- N-T001-002: Do not duplicate registry decisions inside the old entry branch flow.

## Atomic Steps
1. Create the registry data structure and deterministic selection logic.
2. Keep request entry wiring unchanged until T-002.

## Functional Boundary Conflict Protocol
- Escalation Trigger: Building the registry requires either changing the current request or error behavior, or introducing the prohibited runtime extension mechanism.
- Required Conflict Analysis: Compare an explicit static registry, a protected-behavior change, and a compatibility adapter. Identify the affected callers, error behavior, and the minimum code impact scope for each path.
- Recommended Option: `3`
- Recommendation Rationale: A bounded compatibility adapter can introduce explicit dispatch ownership while preserving the protected request and error behavior.
- Decision Prompt: Reply with `1` to stop and preserve protected behavior, `2` to approve the described behavior change, or `3` to approve the compatibility adapter.
- Decision Limit: This decision covers only the registry-creation conflict and its minimum necessary implementation scope.
- Required Decision Record: Record the selected option, the evidence considered, the actual affected code, the resulting behavior, and the verification outcome in execution state and log.

### Resolution Options
| Number | Resolution Path | Effect on Requested Functionality | Effect on Protected Functionality | Compatibility Consequences | Required Verification |
| --- | --- | --- | --- | --- | --- |
| 1 | Stop this task and keep the current dispatch behavior. | The requested registry remains unimplemented. | Protected request parsing and error behavior remain unchanged. | No caller-visible change. | Confirm that no implementation change was applied. |
| 2 | Change the protected request or error behavior as described. | The registry can be introduced directly. | Changes protected behavior. | Existing callers may observe the new behavior. | Verify the explicitly approved request and error contract. |
| 3 | Add the smallest compatibility adapter around the explicit registry. | Implements explicit handler selection. | Preserves protected request parsing and error behavior. | Existing callers retain current behavior while new dispatch ownership is introduced internally. | Verify registry selection plus both existing request and error paths. |

## Required Verification Evidence
- Verification Procedure: Inspect registry selection and its focused checks.
- Required Evidence: Selection is explicit and deterministic without
  reflection-based discovery.

## Completion Criteria
The registry owns handler selection while protected functionality is unchanged.
