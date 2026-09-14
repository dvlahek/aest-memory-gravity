# Stable AeST growth–Weyl memory R2b — pre-result technical repair 3

Date: 2026-09-14
Branch: `fullj-evolving-weyl-bridge`

## Status before repair

The R2b preregistration remains locked at

    fc118356ea77be3b81854a95992a89ff7a1630bc

and the R2a post-data parent remains

    bbcf1e8e88743fb63ebe9b7e8da1202b8d3438dc.

The first two attempted R2b executions failed before any forcing trace or signed lambda science probe was produced. The third attempted execution also failed before any forcing trace or lambda probe.

The third failure occurred inside `apply_stable_aest_r2b_variational_patch.py` while locating the insertion point inside `perturbations_sources()`. The patcher searched for two textual variants of the line assigning `a2`. More than one such assignment exists in the function, so the safety guard raised

    RuntimeError: multiple a2 source-grid anchors found

before modifying the temporary R2b CLASS source.

Therefore no R2b scientific gate has been evaluated and no R2b scientific classification exists yet.

## Allowed repair

This repair is purely structural. It may only make the insertion point unambiguous inside the already preregistered native CLASS source-grid function.

The trace insertion will be anchored to the local sequence beginning with

    a = ppw->pvecback[pba->index_bg_a];

inside `perturbations_sources()`, then to the first following `a2 = ...;` assignment in that same local block. This identifies the source-grid background setup without choosing among unrelated later `a2` assignments.

The diagnostic external-force hook remains attached to the existing AeST `E` derivative. The exact physical memory closure, stable residual state `s`, `chi=Q*s`, tau H0=10, memory order 20, physical eta=0, lambda set, observables, redshift grid, anchors, thresholds, gates and classification logic remain unchanged.

No scientific result may be reclassified because of this repair.
