# NL1C7B4 Repair02 result freeze — exact nonlinear dictionary completion

Status: **POST-DATA / FROZEN**

Official run: `35216284867`

Head SHA: `2791ba272e8a587bfe2ead747b54596631527627`

Artifact: `10495377062`

Artifact SHA256: `f74795d3c57ba6f307655b1ec15513b57babc7eadbe0c81c4f62bf1949643d49`

Science classification:

`NL1C7B4_REPAIR02_DICTIONARY_COMPLETED_RAW_CONSTRAINT_FAIL`

## What passed

- exact C7A state reproduction: max relative L2 error `0.0` against the official retained primary-state NPZ;
- symbolic Exp K(Q) dictionary identity: PASS;
- R2-G1 exact target preservation: PASS, max normalized Q-target error `0.0`;
- R2-G2 unique algebraic first-order-preserving completion: PASS;
- R2-G3 Exp-domain restoration: PASS;
- R2-G5 two-grid control and no case selection: PASS for all 27 grid pairs;
- all action terms are finite away from the analytically excluded center;
- no Q linearization, K clipping, amplitude/phase fit, constraint projection, Y-branch selection, or scale selection was used.

The exact completion changes only `phidot` according to the preregistered algebraic inversion

`phidot_completed = [Q_target - sinh(u) phi_r/L] / cosh(u)`.

The largest completion relative L2 correction is about `2.50e-5`; the exact completed Exp coordinate remains finite with max `|Z| = 5.549704644025342`.

## What failed

The unchanged B4 raw-constraint gate remains above the frozen `1e-7` threshold in all `54/54` co-primary cases.

Global maxima:

- Hamiltonian: `max epsilon_H = 7.427971317516522e-05`;
- radial momentum: `max epsilon_M = 0.9999999999945085`;
- number of constraint-passing cases: `0/54`.

Representative two-grid behavior is highly stable. For example at `R_sigma=5 h^-1 Mpc`, RMS grid ratios are approximately `1.00019` for Hamiltonian and `1.00086` for momentum. Therefore the failure is not removed by doubling the radial resolution.

The Y interpolation family and beta0 do not materially change the reported residuals. This indicates that the remaining failure is not a post-result Y-branch choice problem.

## Interpretation boundary

Repair02 successfully removes the previous nonlinear Q-dictionary/Exp-domain pathology. The remaining raw-constraint failure is therefore a separate closure problem.

This result does **not** authorize a short nonlinear evolution or long collapse run.

Before modifying any state field or adding any radial source, the next checkpoint must localize the remaining Hamiltonian and momentum residual term-by-term using the same frozen action and the same completed Repair02 state.
