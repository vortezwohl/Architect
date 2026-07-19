# Impact and Boundaries

## Metadata
- DocumentType: ImpactAndBoundaries
- DocumentId: IMPACT
- PlanName: restore-multilingual-github-stars-badge
- CreatedAt: 2026-07-19:17:35:20.192
- DocumentLanguage: en

## ImpactMap
| Path | SymbolOrContract | ChangeType | AffectedCallers | Evidence |
| --- | --- | --- | --- | --- |
| README.md | Third top-level badge | modify | GitHub README readers and stargazers link users | Historical line in commit 3d7d667; current line at README.md:13 |
| i18n/README_zh-hans.md | Third top-level badge | modify | Simplified Chinese README readers and stargazers link users | Historical line in commit 3d7d667; current line at i18n/README_zh-hans.md:13 |
| i18n/README_zh-hant.md | Third top-level badge | modify | Traditional Chinese README readers and stargazers link users | Historical line in commit 3d7d667; current line at i18n/README_zh-hant.md:13 |
| i18n/README_ja-jp.md | Third top-level badge | modify | Japanese README readers and stargazers link users | Historical line in commit 3d7d667; current line at i18n/README_ja-jp.md:13 |

## StableBoundaries
- Badge order and the first two badges remain unchanged.
- All README prose, navigation, wordmark references, installation commands,
  and language-specific content remain unchanged.
- The external badge semantic is identical across all four files.

## ProhibitedCrossBoundaryChanges
- No application code, tests, runtime configuration, plugin metadata, assets,
  or files outside the four README paths.
- No repository URL migration, branding change, link normalization, or
  additional localization synchronization.
