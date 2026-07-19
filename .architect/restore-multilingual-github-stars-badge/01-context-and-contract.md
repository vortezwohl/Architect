# Context and Contract

## Metadata
- DocumentType: ContextAndContract
- DocumentId: CONTEXT
- PlanName: restore-multilingual-github-stars-badge
- CreatedAt: 2026-07-19:17:35:20.192
- DocumentLanguage: en

## ObservedFacts
- The repository is a documentation-led plugin repository with one English
  README and three localized README files.
- The affected entry points are the third badge lines in README.md and the
  three files under i18n/.
- The current behavior owner is the static Markdown badge line in each file.
- GitHub renders the Markdown, shields.io renders the badge image, and the
  badge link points readers to the repository stargazers page.
- Commit 3d7d667 contains the same historical GitHub Stars badge line in all
  four files; the current Architect Repo badge replaced it in commit 3ffda33.
- No dedicated README badge test was found in the repository test tree.

## ApprovedInputLimits
- Use only the approved D-001 design and the four identified README paths.
- Restore the exact historical badge URL and target URL from commit 3d7d667.
- Do not infer or add any unrelated README synchronization work.

## CompatibilityIntent
- Preserve the historical public README badge contract across every supported
  language while preserving all current unrelated README content.

## PreservedContracts
- The third badge remains in the same position in all four README files.
- The badge label is GitHub Stars and the image URL uses the repository's
  github/stars endpoint with style=flat-square&label=Stars.
- The badge target remains the repository's /stargazers page.
- The workflow badge, license badge, wordmark, navigation, prose, and file
  encoding remain unchanged.

## ExplicitlyBreakableContracts
- None approved. This is a compatibility restoration only.

## ExecutionConstraints
- Build must edit only the four exact badge lines.
- Build must validate the exact historical line in every language file.
- Build must record observed verification results in task state and the
  execution log; no result may be claimed without command evidence.
