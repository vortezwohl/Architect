# Task Catalog

## Metadata
- Document Type: Task Catalog
- Document ID: TASK-CATALOG
- Plan Name: reference-plan-example
- Created At: 2026-07-17:14:53:04.486
- Document Language: en

## Tasks
| Task ID | Execution Order | Path | Depends On | Source Design References | Summary |
| --- | --- | --- | --- | --- | --- |
| T-001 | 1 | 06-tasks/T-001-create-dispatch-registry.md | None | D-001 | Create the explicit dispatch registry boundary. |
| T-002 | 2 | 06-tasks/T-002-route-entry-through-registry.md | T-001 | D-001, D-002 | Route request entry through the registry and the shared error contract. |
| T-003 | 3 | 06-tasks/T-003-update-tests-for-dispatch-contract.md | T-001, T-002 | D-001, D-002 | Update tests to lock the dispatch and error contract behavior. |
