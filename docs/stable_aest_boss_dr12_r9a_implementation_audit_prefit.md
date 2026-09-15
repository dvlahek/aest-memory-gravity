# Stable AeST BOSS DR12 R9a — implementation audit before first fit

Date: 2026-09-15
Branch: `fullj-evolving-weyl-bridge`

Pre-fit science lock:

`63f4bea97c95a5627f659415f556636c1af21fad`

Implementation commits before any R9a memory-data fit:

- driver: `743c0d36d9abd546654c62c5e7169b58169bbbd6`;
- runner: `8decb976259916d052edf070e136771130cf6e04`.

The diff from the pre-fit lock through the runner commit contains only two new executable R9a files:

- `fullj_weyl/stable_aest_boss_dr12_r9a_growth_fixed_template.py`;
- `fullj_weyl/run_local_stable_aest_boss_dr12_r9a_growth_fixed_template.sh`.

No historical result, parent source, science threshold, tau grid, eta interval, or observational datum was modified.

The runner independently checks all frozen science/post-data commits with shell-level `git merge-base --is-ancestor` calls before building or fitting. The driver G1 independently repeats parent classification/provenance checks. The runner also contains a redundant Python anti-stale text-audit block; an unused helper list in that block does not weaken the shell ancestor checks or driver G1 and is non-gating redundancy, so no executable science repair is required.

## Frozen observational provenance

R9a retrieves a fresh checkout of `CobayaSampler/bao_data` at exact commit

`bb0c1c9009dc76d1391300e169e8df38fd1096db`

and verifies:

- `sdss_DR12Consensus_final.dat` SHA256 `eae45d2629dc1214b351716b3ff9a6f5a22f170b71e3d0e93aeeddc169d80e30`;
- `final_consensus_covtot_dM_Hz_fsig.txt` SHA256 `dea6d8d4893d2b84772f9b83d0653bf7d4ee81a0aeb63ce04859e20d0ad3a289`.

The BOSS growth likelihood uses the exact `f_sigma8` indices `[2,5,8]` and the corresponding full 3x3 marginal covariance submatrix. No diagonal covariance approximation is used.

## Frozen theory path

The runner creates a fresh disposable CLASS tree from frozen parent `e85808324f51fc694d12e3ed7439552a3c3f9540`, applies the certified stable-chi patch, neutralizes exactly one dormant historical external tangent hook, applies the certified R7a live/signed-eta diagnostic patch, and verifies zero R2d trace/replay hooks.

The 20 frozen theory runs are four tau values `10,5,2.5,1.25` times eta `0,+/-0.025,+/-0.05`, evaluated directly at BOSS redshifts `0.38,0.51,0.61`.

The data-preference quantities (`eta_hat`, Fisher sensitivity, Delta chi2, physical profile) have not been evaluated before this audit lock.
