# Task: {{GENERATED:DocumentId}}-{{GENERATED:Slug}}

## Metadata
- DocumentType: Task
- DocumentId: {{GENERATED:DocumentId}}
- PlanName: {{GENERATED:PlanName}}
- CreatedAt: {{GENERATED:CreatedAt}}
- DocumentLanguage: {{GENERATED:DocumentLanguage}}

## DesignSources
- DesignRefs: {{AGENT:DesignRefs}}
- RuleRefs: {{AGENT:RuleRefs}}
- ProhibitedNewConcepts: {{AGENT:ProhibitedNewConcepts}}

## Preconditions
{{AGENT:Preconditions}}

## ExactChangeBoundary
| Path | Symbol | Operation | AllowedDesignChange |
| --- | --- | --- | --- |
| {{AGENT:Path}} | {{AGENT:Symbol}} | {{AGENT:Operation}} | {{AGENT:AllowedDesignChange}} |

## ExplicitlyOutOfScope
{{AGENT:ExplicitlyOutOfScope}}

## MUST DO
- {{RULE:MUST_DO}}

## MUST NOT DO
- {{RULE:MUST_NOT_DO}}

## AtomicSteps
1. {{AGENT:AtomicStep}}

## ScopeCheckAndBreachRecovery
{{AGENT:ScopeCheckAndBreachRecovery}}

## LocalVerification
- Command: {{AGENT:VerificationCommand}}
- ExpectedResult: {{AGENT:ExpectedResult}}

## CompletionCondition
{{AGENT:CompletionCondition}}
