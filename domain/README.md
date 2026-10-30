# Historical physics domain package

This directory preserves the May 2026 domain inputs for the separate
[D-ND_LAB engine](https://github.com/GrazianoGuiducci/D-ND_LAB). Its original
context, assertions, seed tensions, category mapping and falsification record
remain unchanged. They are historical sources, not the current regenerative
Lab's prompt, active memory or newly validated scientific claims.

The current Lab is developed in MM-DND and exposed at
[d-nd.com/ai-lab](https://d-nd.com/ai-lab). The repository
[README](../README.md) and [architecture](../docs/ARCHITECTURE.md) explain that
Lab; `physics_lab/` supplies its public offline reader.

The former “Phase 0 — placeholder” description is superseded by this explicit
historical status. The original version remains in Git history at
`cca0794984f1e613c42c4a43bd960a1853b95231`.

For an engine installation, use D-ND_LAB's own shipped `domains/physics/`
directory. For a separately selected historical reconstruction of this
package, read [compatibility and layout](../docs/DND_LAB_COMPATIBILITY.md).
Cloning this whole repository directly as an engine domain does not place
`config.json` at the path expected by that loader.
