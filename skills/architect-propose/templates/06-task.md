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

## FunctionalBoundary
- TargetFunctionality: {{AGENT:TargetFunctionality}}
- ProtectedRelatedFunctionality: {{AGENT:ProtectedRelatedFunctionality}}
- ExplicitNonGoals: {{AGENT:ExplicitNonGoals}}
- CompatibilityObligations: {{AGENT:CompatibilityObligations}}
- HardStopCondition: {{AGENT:HardStopCondition}}

## CodeImpactScope
| ExpectedPath | SymbolOrArea | ExpectedChange | EvidenceOrReason |
| --- | --- | --- | --- |
| {{AGENT:ExpectedPath}} | {{AGENT:SymbolOrArea}} | {{AGENT:ExpectedChange}} | {{AGENT:EvidenceOrReason}} |

## ImpactScopeAdaptationRules
- CoverageIntent: {{AGENT:CoverageIntent}}
- AdaptiveExpansionRule: {{AGENT:AdaptiveExpansionRule}}
- AssessmentAndLogRequirement: {{AGENT:AssessmentAndLogRequirement}}

## MUST DO
- {{RULE:MUST_DO}}

## MUST NOT DO
- {{RULE:MUST_NOT_DO}}

## AtomicSteps
1. {{AGENT:AtomicStep}}

## FunctionalBoundaryEscalation
- TriggerCondition: {{AGENT:TriggerCondition}}
- RequiredAnalysis: {{AGENT:RequiredAnalysis}}
- Recommendation: {{AGENT:Recommendation}}
- ApprovalQuestion: {{AGENT:ApprovalQuestion}}
- DecisionScope: {{AGENT:DecisionScope}}
- RecordRequirement: {{AGENT:RecordRequirement}}

### DecisionOptions
| Number | Path | FunctionalImpact | CompatibilityImpact | Verification |
| --- | --- | --- | --- | --- |
| {{AGENT:Number}} | {{AGENT:Path}} | {{AGENT:FunctionalImpact}} | {{AGENT:CompatibilityImpact}} | {{AGENT:Verification}} |
| {{AGENT:Number}} | {{AGENT:Path}} | {{AGENT:FunctionalImpact}} | {{AGENT:CompatibilityImpact}} | {{AGENT:Verification}} |

## TaskDeclaredExecutionResults
- CommandOrProcedure: {{AGENT:ExecutionResultCommandOrProcedure}}
- ExpectedRecordedResult: {{AGENT:ExpectedRecordedResult}}

## CompletionCondition
{{AGENT:CompletionCondition}}
