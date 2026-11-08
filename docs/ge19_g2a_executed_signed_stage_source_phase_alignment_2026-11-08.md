# GE19 G2A — signed stage source recovery executed; nearly common amplitude change, not full Ward

**Date:** 2026-11-08. **Frozen branch:** `physics-first-gravitational-elasticity`. **Status:** executed source reconstruction; full original H4 Ward remains **OPEN** and original frozen active shift remains **FAIL**.

## Actual uploaded outputs, verified

- `ge19_g2a_Cstar_allmodes_signed_h4_stage_source.json`: SHA256 `742b94f6156271a01f533e5a71e5065fe160c4c83ff5d71249c6664916e5f95d`.
- `ge19_g2a_Cstar_allmodes_signed_h4_stage_source.log`: SHA256 `8957a9310a06867dc206bdabf11fbc3c4fa580ff573dc2f280fb2e6d7058c2f0`.
- `ge19_g2a_Cstar_allmodes_signed_h4_stage_source.npz`: SHA256 `3075dea41e508c713b4a125d8d58979371aabb982c1fe83520c30fa60dc70723`.
- All four local original parent SHA-256 locks passed at the actual G2A run (original R37 NPZ, Cr12u NPZ, Cr12abR2 NPZ and original Cr12abR2 Python). Verified each recovered NPZ array finite with correct axes: 3 beta × 40 modes × 6 original main rows or 2 constraint rows × 255 source points (initial node x0 plus exactly 254 original Radau stage points). Exact first-node R37-source preservation and exact original node-right-stage coordinates validated. Original independently regrouped five-piece hotspot source crosscheck equals **0.0** in stored complex arithmetic.
- Program outcome: `GE19_G2A_ORIGINAL_SIGNED_H4_STAGE_FORCING_RECOVERED_FULL_PARENT_WARD_OPEN`. Source **only**: no original canonical Euler residual phase, no full parent Ward, no Z21 or lensing.

## Critical original Cstar/m40/beta-index1/time-node24 actual numbers

At `x=-0.7775878956385266`, original right Radau stage index47, G2A source index48:

```text
original Repair37 shift RHS =  8.661891918697527e-08 -1.4555159074168087e-07 i
final Cr12abR2 shift RHS =    8.661918844036937e-08 -1.4555204318625260e-07 i
delta FINAL-OLD RHS =        2.6925339409804516e-13 -4.5244457172596325e-13 i
|delta RHS| =               5.2650116877135950e-13
delta RHS / old RHS =       ~3.1084824941243590e-06 +1e-15 i
frozen original raw |Eb| =   2.7770076323913147e-13
frozen original Eb scale =   2.2807278924536992e-07
frozen active normalized =  1.2175970845008160e-06 (FAIL, threshold 1e-6)
```

The ratio `|delta RHS|/|Eb| ≈1.896` compares different physical quantities: signed source perturbation to unsigned final Euler residual. It is **not** an error decomposition, no inferred phase of Eb, no proof that a 3.1-ppm normalization should be applied to the action.

At x24 among the **21 modes** with `|original shift source|>1e-14`, `Re(deltaS/S)` runs from `3.108482494124359e-6` to `3.1120648024201222e-6` and `max|Im(deltaS/S)|≈9.454818182952093e-11`. The full-domain complex projection of deltaS onto original signed shift S captures **99.6215940685% of deltaS energy**, with fitted complex coefficient `~7.66993337705e-6 -1.45818458635e-13 i`. This is a **nearly phase-preserving, common-amplitude change in the stored RHS**, not proof of a new universal physical factor. Original and final complex shift sources are bitwise beta-independent at all 255 points.

## Component responsibility for the **stage source** correction only

The actual original Cr12abR2 Python defines `historical_M2_constraint_stage` by evaluating the original Repair37 piece-specific PCHIP at the same stage points. So using its stored `historical_M2` and `sub48_M2` gives an exact source-side additive decomposition of the complex `delta RHS` at x24/m40:

```text
delta_M2 shift RHS =     -1.5698832778442723e-15 +2.6379803853998880e-15 i
|delta_M2| =             3.069767746884057e-15
delta_other source RHS = +2.7082327737588943e-13 -4.5508255211136310e-13 i
|delta_other| =          5.295709365182435e-13
delta_M2/delta_total =  -0.0058305050946945705 +1.81e-11 i
```

Thus at this single mode/time, the fine48 **M2 re-evaluation contributes just ~0.583% of the overall stage-source amplitude change, and is almost antiparallel**; the combined remaining Q6/Q7/Lambda/DY2 stage-source replacements dominate this signed **source difference**. This **does not mean M2, or those other sectors, make the same fractional contribution to the propagated H4 residual**, which requires the entire action-constrained linear response and parent state.

## Stop criterion for source-only numerical diagnostics

Do not relaunch the old frozen H4 repair campaign, vary beta, or tune any source weight by the observed source ratio. Finite stage values (not an independently certified common differentiable continuous forcing) plus unsigned stored `|Eb|` cannot reconstruct the original complex signed `Eb`, physical longitudinal `EL`, full first-order-parent `R_parent` and original lower-boundary `B_parent`. Hence no actual original mixed-action Noether transport test from this bundle alone.

Only credible next *physics* route: independent common-physical-clock variation/Noether accounting for all original first-order parents and action boundary/interface terms, followed, **if original canonical stages / full signed Euler data are recovered or transparently reproduced**, by one signed integrated-Ward test with unchanged D9/D12R3 FD4/FD8 and roundoff budget. Otherwise report the identifiability gap, not a fabricated PASS. Original D55Cr11f GE05 Cstar six-mode H-channel PASS, Cr12abR2 IMPLEMENTATION_FAIL and active H4 shift SCIENCE FAIL, and Cr12ad frozen-physics closeout all remain unchanged.

Separate **reproducible read-only audit files** (created in chat container; not WSL source replacement):
`GE19_G2A_SIGNED_STAGE_SOURCE_AUDIT_20261108.json` SHA `0dbbde8d15796b2ebb2a47e6e3ac9e2ab9bf9a5c10b9e7c70e7dabc679fbba18`;
`GE19_G2A_SIGNED_STAGE_SOURCE_AUDIT_20261108.md` SHA `65e806949a451a22ce2ba71dea15b4c59a5b1f5f88eccefecf79cfc44a077e1a`.
