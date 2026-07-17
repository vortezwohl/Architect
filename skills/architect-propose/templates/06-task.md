# Task: {{GENERATED:DocumentId}}-{{GENERATED:Slug}}

## Metadata
- DocumentType: Task
- DocumentId: {{GENERATED:DocumentId}}
- PlanName: {{GENERATED:PlanName}}
- CreatedAt: {{GENERATED:CreatedAt}}
- DocumentLanguage: {{GENERATED:DocumentLanguage}}

## DesignSources
- SubdesignRefs: {{AGENT:SubdesignRefs}}
- RuleRefs: {{AGENT:RuleRefs}}
- ProhibitedNewConcepts: {{AGENT:ProhibitedNewConcepts}}

## Preconditions
{{AGENT:Preconditions}}

## ExactChangeBoundary
| Path | Symbol | Operation | AllowedImplementationDetail |
| --- | --- | --- | --- |
| {{AGENT:Path}} | {{AGENT:Symbol}} | {{AGENT:Operation}} | {{AGENT:AllowedImplementationDetail}} |

## ExplicitlyOutOfScope
{{AGENT:ExplicitlyOutOfScope}}

## MUST DO
- {{RULE:MUST_DO}}

## MUST NOT DO
- {{RULE:MUST_NOT_DO}}

## AtomicSteps
1. {{AGENT:AtomicStep}}

## ExecutionBoundaryRules
{{AGENT:ExecutionBoundaryRules}}

## TaskDeclaredExecutionResults
- CommandOrProcedure: {{AGENT:ExecutionResultCommandOrProcedure}}
- ExpectedRecordedResult: {{AGENT:ExpectedRecordedResult}}

## CompletionCondition
{{AGENT:CompletionCondition}}
