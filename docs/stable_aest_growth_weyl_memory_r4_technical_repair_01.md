# Stable AeST growth–Weyl memory R4 — technical repair 01

Date: 2026-09-14
Branch: `fullj-evolving-weyl-bridge`

## Status before repair

The first R4 attempt stopped after:

- `STABLE_AEST_GROWTH_WEYL_MEMORY_R4_IMPORT_PASS`
- `STABLE_AEST_GROWTH_WEYL_MEMORY_R4_SCIENCE_LOCK_PASS`
- `STABLE_AEST_GROWTH_WEYL_MEMORY_R4_PARENT_PASS`
- `STABLE_AEST_GROWTH_WEYL_MEMORY_R4_OLD_PROVENANCE_PASS`

and before `STABLE_AEST_GROWTH_WEYL_MEMORY_R4_SINGLE_CHANNEL_SOURCE_PASS`, before CLASS was built for R4, and before any R4 eta=0/0.005/0.01 science run was executed.

Therefore no R4 science classification exists from this attempt and the preregistration remains unchanged.

## Technical cause

The R4 runner reused the shared local directory

`.local/class_corrected_e8580832_densek64_stablechi`

and additionally required that this source contain zero occurrences of `aest_tangent_external_force`. The shared local directory is a cache used by earlier development/diagnostic workflows and can retain diagnostic source modifications from an older local run while still carrying the stable-chi marker. R3 direct finite-eta physics does not activate diagnostic forcing environments, but R4 intentionally audits source topology and must not rely on mutable shared-cache cleanliness.

## Locked repair

R4 will instead create a fresh disposable CLASS source tree from the frozen parent `e85808324f51fc694d12e3ed7439552a3c3f9540`, verify the frozen `aest_memory.c` SHA, and apply only `apply_aest_stable_chi_residual_patch.py`.

The fresh R4 source must then satisfy exactly the preregistered topology:

- stable-chi marker present;
- `chi = Q*s` source present;
- one physical `Bchi_aest *= pba->aest_eta` multiplication;
- one physical `E_rhs_aest -= 0.5*Q_aest*Bchi_aest` closure;
- zero `aest_tangent_external_force` occurrences.

No physical equation, eta value, tau, bath order, k anchor, redshift, observable, R4 metric, threshold, or classification rule is changed.
