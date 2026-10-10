# GE19 D20R1 preregistration and claim freeze

- Immutable failure: original D20 exited during D17 H1 reconstruction at line 136. All original source and parent SHA checks passed. Never reclassify original D20 failure as PASS.
- Direct ground truth: D17 saved canonical y and X10 on original nodes reconstruct X10 at 2.4e-18 relative using the unchanged source-action Q and original Fourier k.
- Repair: replace the six-row unscaled pooled relative residual as an acceptance metric with the *original* Repair07 per-row `_constraint_backward_error` using the actual row-contribution magnitude. Keep the pooled number in JSON report-only. Retain D17 direct X10, reconstructed X10, canonical qslot and per-row backward gates at <= 1e-9. Log each before fail closed.
- Frozen physical computation: D17 numerical H1, D19R1 full original node bath, frozen Z11, original GE06 GE07 Lambda StageE GE05 M2 source families, frozen H3G M1 stale comparator.
- Not demonstrated: source-consistent new q20 and Z11, high-phase FD4-M2 control, original GE05 all-interval on-shell, all nonbath parent/constraint and boundary Ward, the full linear H4 operator, Z21 or lensing. No observational tuning. Original Repair37 SCIENCE_FAIL remains immutable.
