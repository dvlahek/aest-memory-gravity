# GE19 — G1 single-pass executed: exact surrogate bridge PASS, physical G1 OPEN

**Date:** 2026-11-08.  
**Branch:** `physics-first-gravitational-elasticity`.  
**Executable:** `ge19/h4f3d_g1_single_pass_physical_parent_evidence.py`, frozen source commits `706f7c3` + `636a3d0`.  
**User-local executed artifacts (provided 2026-11-08):**
- `results/ge19_g1_single_pass_20261108.json` (9,386 bytes), SHA-256 **`3eb405722e06ffdd8f03adbae21db977cf4cec46dbad3c067346b089dfd6d37e`**.
- `results/ge19_g1_single_pass_20261108.log` (749 bytes), SHA-256 **`334648ae5f85f453d20eb9709be3e925e5c96b0fffec480b80406eaf557a3e92`**.
- Report exact classification: `GE19_G1_SINGLE_PASS_EXACT_X10_HERMITE_SURROGATE_BOUND_G1_CONTINUOUS_OPEN`.
- Both immutable source-array SHA-256 inputs D17 `cd3bcf8cf5ac9ab14385baa4d90bd53400daae9f2bb89d4d22bfa2a581846359`, H3F `90840755fa9febb1d8cb84609d9e58f67dec2a0a01cd6bf8e47685b45caa4542` match the original locks. G1B and G1C2 report SHA locks also match.

## Exact-rational result for the *two declared Hermite polynomials only*

The saved-float piecewise cubic-Hermite `X10` representations (coarse H3F source-endpoint jets and fine D17 original-action dense endpoint jets) were compared using exact rational Bernstein coefficients over all 508 fine intervals, for primary C_star six modes. The strict upper bound on `sup_x |X10_H3F_coarse_Hermite - X10_D17_fine_Hermite|` is:

| Mode m | exact-input `Linf_x` upper bound, absolute native X10 units |
|---:|---:|
| 3 | 6.460707774282417714e-12 |
| 5 | 3.9580114079203204033e-11 |
| 8 | 1.25376616470704956652e-10 |
| 10 | 2.19538507617993983453e-10 |
| 15 | 6.6627777387999329845e-10 |
| 20 | 8.74300760404109153277e-10 |

**Worst of six: `8.74300760404109153277e-10`**. On **every mode**, the largest Bernstein control is `B3` at fine interval `507`, i.e. the **last endpoint**. Consequently there is no larger Bernstein *upper bound* away from endpoints for these two surrogate polynomials; this does NOT prove the interior true error is zero or that the H4 source uses either interpolation.

Source-endpoint `X10` mismatch at m20 (in old G1C2) was `8.743007604041092e-10`; its close value here is consistent with the last-endpoint dominance, not an independent H4 science gate. The exact rational bound applies only when treating stored binary64 data as exact inputs to ideal cubic polynomials; no floating roundoff or ODE source enclosure was certified by this calculation.

## Relevant earlier scientific evidence, still in declared scope only

- Prior G1B H3F-versus-Repair22 H1/H1dot nodal source identity: **14/14 exact** on Nt128/Nt64, C_min/C_star/C_max.
- Prior G1C2 physical `(S,u,phi,T)`, `X10`, `X10_x` node differences: worst relative L2 `2.083331381227907e-6`, `2.083498430076084e-6`, `1.0971121105527938e-6`, all 6 Cstar primary modes.
- Five local original D47 R5g8 continuous H1 primary/`C_star`, 256-subinterval certificates for modes `3,5,8,10,15` are hash/provenance-and-flag verified; **m20** exact-path report is `MISSING`, not a demonstrated science failure or a claim that D47 has never run. No D47 certificates for `C_min`/`C_max` or `Nt64` can be inferred.
- D55CR11F original `GE05_bath_onshell_certified=true`, `continuous_X10_certified=true`, `continuum_bath_quadrature_certified=true` PASS in its frozen own scope, immutable JSON SHA `3b1165a0fd55d55eebf6409d2b37502ee3037eeb0b4246255d00da3fd4373c63`; its physical transfer to the **actual H4F3B** batch/interval is not proven here.
- Repair32C original artifact-only `Z11_certified=true` PASS, immutable SHA `037314effa33c5bfaf51f6f3c72459de43cb486c6ef5e9a94f5b1984a68611b9`; **not** all-interval Euler (E_{i11}) enclosure.
- H4F3B original corrected six-source scoped PASS, immutable SHA `1ec88fd3fd6b81bf30614b0cb78d722a02dd4f745e1f22cb9b8f956a44bac6c1`.
- Actual action-derived 16/16 canonical continuum linear Ward operator already proved; no reason to repeat Cmat or H4 source-only replay.

## Precise physics decision — no more representation microsweeps

**Closed:** source-bound G1B nodal lineage and this **exact-input global polynomial representation difference theorem** for Cstar m3/5/8/10/15/20. The mathematical upper bound is *absolute native X10*, not an H4 shift error. All provided NPZ/report SHA locks matched.

**Not closed:** an original-action **continuous all-H4-cohort** H1/Z11/GE05 Euler residual enclosure; true D47 interval certificate transport from its *specified* nominal/absolute norm to the actual H4 parent representation and source interpolation (which H4F3B constructs from H3F arrays on the two frozen grids); lower-parent boundary trace and correct mixed Ward discrepancy bound; the independently prelocked D9/D12R3 physical FD4/FD8/roundoff `B_total`. G1 report explicitly has `G1_PHYSICAL_CLOSED=false`, `G3_physical_D9_B_total_frozen=false`, `full_H4_Ward_certified=false`, `Z21_certified=false`, `lensing_licensed=false`.

**Next scientifically necessary route:** stop repeating ancestry, X10 nodal, or polynomial bridge tests. With all original physical source weights frozen, establish a common-norm source **error-transfer theorem** from (1) original-action interval H1 bound to actual H4 sampled and reconstructed H1 (including the stored D17/H3F representation discrepancy and nominal identity), (2) original-action continuous Z11 Euler residual interval enclosure, (3) GE05 actual q10 mode/full-cohort D55 applicability and bath-node error, (4) lower-boundary cross terms. Source operations in H4F3B include bilinear GE06/GE07/Lambda, scalar+aether Stage E Y, and M1/M2, and source dependence should be controlled with actual operator/Bilinear functional norms; simply adding unrelated relative error percentages is invalid.

Recovery of old D47 m20 file should be a **file search only**; don't run a new 508-step arbitrary-precision m20 job unless no original cert exists and a complete physical G1 proof actually requires it. If original D47 physical enclosures are too coarse, frame an explicit new bounded method rather than retroactively weakening the H4 1e-6 shift tolerance or G3 preregistration.

**Next execution gating decision:** prioritize one **actual physical source-operator/parent interval-error certification** with all prerequisites in the same norm and original action. The original G1C2 and G1 single-pass reports should now be considered *completed evidence*, not reasons to launch further small abstract audits.

No observational tuning; old H4/Repair37 science FAILs preserved.
