# Impact and Boundaries

## Metadata
- DocumentType: ImpactAndBoundaries
- DocumentId: IMPACT
- PlanName: reference-plan-example
- CreatedAt: 2026-07-17:14:53:04.486
- DocumentLanguage: en

## ImpactMap
| Path | SymbolOrContract | ChangeType | AffectedCallers | Evidence |
| --- | --- | --- | --- | --- |
| src/service/dispatch_registry.py | DispatchRegistry | create | src/service/entry.py | New explicit registry boundary required by D-001 |
| src/service/entry.py | handle_request | modify | public request entry callers | Entry flow must delegate selection through the registry |
| src/service/error_contract.py | normalize_dispatch_error | create | src/service/entry.py, handlers | Shared normalization point required by D-002 |
| tests/test_dispatch_flow.py | request and error contract assertions | modify | test suite | Existing caller-visible behavior must remain stable |

## StableBoundaries
- Public request payload shape stays unchanged.
- Public success and error envelopes stay unchanged.
- Handler business logic stays outside the registry and outside the error
  contract module.

## ProhibitedCrossBoundaryChanges
- No transport contract changes.
- No storage or schema changes.
- No plugin framework, reflection loader, or dynamic registration side channel.

## BoundaryAuditFindings
- The `architect-build` stage can identify every touched production and test path without guessing.
- The `architect-build` stage must preserve the public request payload and response envelopes while
  changing only the internal dispatch path.
- The only plausible over-boundary risk is an unexpected helper or fixture
  dependency outside the recorded task paths.

## BuildBlockingBoundaryGapsClosed
- The package records exact production and test paths per task.
- The package records preserved caller-visible contracts as stable boundaries.
- Every task records a numbered `1` / `2` cross-boundary approval path for real
  runtime overruns.
