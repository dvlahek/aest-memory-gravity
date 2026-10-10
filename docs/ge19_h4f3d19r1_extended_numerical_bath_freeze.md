# GE19 D19R1 numerical reclosure — preregistration and claim boundary

## Scientific and implementation decision

The original D19 offline replication unexpectedly differed from immutable D16R1 because an independently copied overdamped Repair24 step omitted `exp(lambda1 * dt)` and `exp(lambda2 * dt)` in the new velocity. This was NOT a change to original Repair24 or D16R1. Restoring both factors replayed all D16R1 full bath nodes with exactly zero relative difference for `z` and `v` and reproduced weighted outputs to machine precision. The broken offline result remains a failed diagnostic and is not a valid numerical parent.

With the corrected source step, physical H1 drive at original source-action dense D17 grid and physical clock produce a true remaining numerical diagnostic: D19 sampled GE05 residual at 64 original steps ~0.003156, while the preregistered acceptance is <=0.001. D19R1 is an additive, source-locked extension of the grid to 64,128,256 original steps. All six numerical thresholds from the original D19 are unchanged. 128-vs-256 is the decisive refinement comparison. No a posteriori tuning of thresholds or physics is allowed.

## Source and parent scope

Cstar, primary Nt128, Nq2048, original six positive modes and their +/- reality partners. D17 dense source-action H1 X/X_x, D15a continuous original-action H/Hx, D16R1 frozen Repair26 boundary and archive, original Repair24 step, original GE05 source and original signed convolution. 16-point Gauss quadrature computes each exact physical-action substep clock. `v=dz/ds` is continuous through all substeps and frozen original knots. Source files/parent results and trace are SHA-locked, outputs have D19R1-only names, `unzip -n`, no overwrite. Progress is printed throughout WSL runs.

`Rs=3(tau H-heff)v+r^2(Xlin-X_D17)` and signed W are sampled at fixed x fractions 0.4/0.6 of each original H3F interval. This is a finite-step sampled numerical check, not an all-interval error certificate; D17 true original continuous H1 error remains unenclosed. Passing does NOT license original GE05 all-interval first-order bath on-shell, original full H4 Ward, rebuilt q20/Z11, Z21 or lensing. Original Repair37 SCIENCE_FAIL is immutable.

An optional *independent accelerated* pilot, not the pinned source runner, observed 256-substep sampled residual ~0.000196. The actual local source runner has not yet produced D19R1 science results. The user's final result must be checked against actual source JSON/NPZ and all frozen gates.
