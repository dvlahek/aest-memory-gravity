# Stable AeST growth–Weyl memory R4 — technical repair 03

Date: 2026-09-14
Branch: `fullj-evolving-weyl-bridge`

This note is a pre-result implementation repair checkpoint. No R4 science result exists yet.

The third R4 attempt passed the preregistration lock, parent lock, frozen CLASS provenance, stable-chi source patch, diagnostic-hook neutralization, single-channel source audit, CLASS build, and `R4_DIRECT_FINITE_ETA_PASS`. It then failed before completing the first physical run with

`AttributeError: module 'fullj_weyl.stable_aest_growth_weyl_memory_r3_scale_generality' has no attribute 'classy_h'`.

Cause: the R4 driver imported the R3 module and attempted to call the helper functions `classy_h`, `k_h_from_transfer`, and `interp_transfer_field` through `r3`. These helpers are defined in `stable_aest_growth_weyl_memory_r2.py`; R3 uses R2 internally but does not re-export those symbols.

Allowed repair: import `stable_aest_growth_weyl_memory_r2` directly in the R4 driver and replace only the three helper calls `r3.classy_h`, `r3.k_h_from_transfer`, and `r3.interp_transfer_field` by their `r2` equivalents.

No source equation, physical memory parameter, anchor, eta value, observable definition, threshold, gate, classification priority, or preregistered interpretation is changed. The failed attempt produced no completed R4 cell and has no science classification.
