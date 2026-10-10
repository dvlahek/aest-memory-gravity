# GE19 D22A — physical preregistration, 27 September 2026

## Problem and immutable provenance
D21R1 corrected the original GE05 M2 scalar time-current but left the mixed H4 source with a *stale* H3G `B20`/M1 and a Z11 computed under frozen H3F H1/R1 bath. We must not label that source as an on-shell H4 parent. This D22A calculation targets only `C_star`, 128 original physical-action H3F knots, all original six first-order positive Fourier modes, original second-order modes 1..40, three fixed beta values, and all 2048 D19R1 bath nodes. All four actual D17/D19R1/D20R1/D21R1 JSON/NPZ pairs are SHA-locked, together with the original Repair26 trace, H3F, Repair32B/C and historical source Git blobs. Frozen Repair37 SCIENCE_FAIL remains immutable.

## Numerical definitions, no observational tuning
* Reconstruct H1 and the cosmic-time jets from D17 canonical y on the original 128 knots. Require D17 X10 identity and row-scaled algebraic backward consistency.
* Recompute `B10 = X10_D17 - sum_j w_j z10_D19R1,j`. Do not repropagate or interpolate frozen R1 bath. Require full-node-to-weighted D19R1 replay.
* Map `-2 M1_GE05` into the original GE06 residual convention with Repair32B's exact factor 2; solve Z11 with the *frozen R2 eta dynamic boundary* archived by Repair32B. The old algebraic initial state is source-dependent and must not be reused as the new one.
* Recompute the action-completed-Y H3F source on D17 H1, including GE06/GE07/Lambda, at Nx1024 and Nx2048. New Z20 uses the actual-source projected momentum boundary from frozen Repair18, **not** the old p0 or an arbitrary homogeneous solution. Integrate the inherited canonical Radau scheme with the action continuation for H,Q,Z from D17; restore callbacks and caches in `finally`.
* Predetermined numerical monitors: linear 1e-8, shift/anisotropy 1e-6, source Nx1024/2048 5e-4, initial/boundary 1e-8. Changes relative to frozen H3F/Repair32B are report-only, **not** new tunable thresholds.

## Claim boundary
Output arrays `Z11_D17_D19_candidate_primary` and `Z20_D17_H3F_candidate_primary` are **single-cohort numerical candidates**, not certified true continuum original-action parents. `X20_D17_Z20_primary_NOT_B20` is only a *drive*, not a physical `B20` response. Recompute q20 from the new Z20 and D19 bath in the following D22B calculation, including a phase-resolved test of the original GE05 q20 quadratic current before accepting its weighted projection. Only then can M1 be rebuilt. No original GE05 all-interval on-shell certificate, full parent/boundary/operator H4 Ward, Z21 solve, lensing or observation tuning is claimed. Never edit the frozen source modules or overwrite prior result files.
