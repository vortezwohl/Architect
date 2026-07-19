# Subdesign: D-001-restore-multilingual-github-stars-badge

## Metadata
- DocumentType: Design
- DocumentId: D-001
- PlanName: restore-multilingual-github-stars-badge
- CreatedAt: 2026-07-19:17:35:20.192
- DocumentLanguage: en

## Concept
- CanonicalName: Documentation Consistency Restoration
- Category: Documentation consistency and bounded change
- Reference: references/source-article.md Sections 2 and 5; Keim and Koziolek, Towards Consistency Checking Between Software Architecture and Informal Documentation, DOI 10.1109/icsa-c.2019.00052; Liu, Noei, and Lyons, How ReadMe files are structured in open source Java projects, DOI 10.1016/j.infsof.2022.106924

## Intent
- Restore the historical GitHub Stars badge and its /stargazers target at the
  third badge position in README.md and all three localized README files.

## StableCoreAndVariation
- Stable core: the four README documents, their badge order, all other badges,
  the wordmark, navigation, translated prose, and current file encoding.
- Actual variation: each language file has its own translated content and
  relative asset paths, but the restored third badge has one shared public
  meaning and one shared external target.
- Ownership: each Markdown file owns its own static badge line; no generator
  or shared runtime component exists.

## Rationale
- Restore the exact four historical lines directly. This is the globally best
  supported design because repository history proves the intended content, the
  user confirmed the compatibility boundary, and the change does not require a
  new abstraction. The direct four-line restoration is easier to review and
  verify than introducing a documentation generation layer.

## Alternatives
- Restore only the English README: rejected because the supported language
  views would expose inconsistent top-level product signals.
- Keep Architect Repo / open repo: rejected because it does not preserve the
  confirmed historical badge contract.
- Add a README generator or shared template: rejected because the repository
  has no established generation pipeline and four static line edits are fully
  reviewable without new maintenance cost.

## DesignBoundaries
- The only editable content is line 13 in README.md and line 13 in each of
  i18n/README_zh-hans.md, i18n/README_zh-hant.md, and i18n/README_ja-jp.md.
- The restored image URL is exactly
  https://img.shields.io/github/stars/vortezwohl/Agent-Architect?style=flat-square&label=Stars.
- The restored target URL is exactly
  https://github.com/vortezwohl/Agent-Architect/stargazers.
- No assets, code, tests, navigation, prose, or other links are in scope.

## Counterexamples
- If the repository is formally renamed or moved in the future, the historical
  Agent-Architect stargazers URL may need a new compatibility decision.
- If shields.io is unavailable, the badge may fail to render; this plan does
  not redesign external badge hosting.

## AntiPatterns
- Replacing every GitHub link instead of the four approved badge lines.
- Updating only the English README.
- Combining this restoration with branding, navigation, or localization work.
- Introducing a generator, template layer, or dependency for four static lines.

## Rules

### MUST DO
- R-D001-001: Restore the exact historical GitHub Stars badge line in all four approved README files.
- R-D001-002: Validate that only the four approved third-badge lines changed and that all four files remain UTF-8 without BOM.

### MUST NOT DO
- R-D001-N001: Do not modify any README content outside the four approved badge lines.
- R-D001-N002: Do not introduce a generator, template layer, dependency, or unrelated repository URL change.
