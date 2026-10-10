# Archive policy

This directory is for superseded summaries and implementation-era notes that are useful for provenance but are not part of the active scientific route.

## Rules

- Historical science FAILs, diagnostic FAILs and implementation failures are never deleted from git history or relabelled.
- Active code and frozen science artifacts are not moved merely to make the tree look cleaner.
- Files are archived only when they are superseded as navigation/documentation and are not required by active imports, runners, hash locks or provenance checks.
- Git history remains the authoritative record of prior file locations and contents.
- The active recovery point is `docs/CURRENT_GE19_STATUS.md`.
- The current persistent history supplement is `docs/ge19_history_2026-10-10.md`.

## Archived in this cleanup

- `THEORY_v018.md` -> `docs/archive/THEORY_v018.md`

`THEORY_v018.md` describes the old v0.18 CLASS source-integration gate. It remains scientifically useful as historical context but is no longer an active top-level theory document.

## Intentionally not archived

The numerous GE19 repair scripts, preregistration JSON files and result-freeze documents remain in place because many are part of explicit SHA/provenance chains. Moving or deleting them would create unnecessary risk and does not improve the active science route.
