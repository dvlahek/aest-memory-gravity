# Full-J isotropic Weyl transfer nodes — result

## Classification

The preregistered transfer-node milestone completed and returned

`FULLJ_ISOTROPIC_WEYL_TRANSFER_NODES_FAIL`.

The failure is narrow: G4 (pointwise transfer-phase consistency) failed, while G1–G3 and G5–G9 passed.

## Frozen-gate outcome

- G1 provenance/setup: PASS
- G2 finite/constraint health: PASS
- G3 initial corrected-CLASS normalization: PASS
- G4 transfer phase consistency: FAIL
- G5 single-mode separability: PASS
- G6 off-target leakage: PASS
- G7 amplitude homogeneity: PASS
- G8 Gaussian ensemble reconstruction: PASS
- G9 discrete power-node sanity: PASS

Summary metrics:

- initial CLASS max relative error: `7.55876668127277e-15`
- pointwise phase metric max `|Im T|/|T|`: `6.748959021664703e-08`
- separability median: `2.948772885461996e-10`
- separability maximum: `1.0487263309295026e-06`
- off-target leakage maximum: `7.451381233238023e-12`
- amplitude-homogeneity median: `3.7771933443955484e-10`
- amplitude-homogeneity maximum: `2.6170804943117027e-06`
- Gaussian ratio reconstruction median: `4.89389762837665e-11`
- Gaussian ratio reconstruction maximum: `1.7807695548234596e-08`
- power identity residual: `7.174174695641998e-18`

The six-mode metric constraints remain at machine precision and all single-mode/amplitude-control trajectories are finite.

## Diagnosis

The maximum G4 ratio occurs at the near-zero transfer cell `n=10, z=0.2`:

- `Re T = 0.006174491143802195`
- `Im T = -4.167138770915273e-10`

The absolute quadrature component is therefore tiny, but the preregistered local denominator `|T|` is also small because the real transfer is close to a zero crossing. This makes the pointwise relative phase metric poorly conditioned at that cell.

This diagnosis does not alter the historical classification. The original milestone remains FAIL and its G4 threshold is not relaxed post hoc.

The other independent checks strongly indicate that the transfer construction itself is numerically stable: the six-mode/single-mode difference remains <= `1.0487263309295026e-06`, amplitude homogeneity <= `2.6170804943117027e-06`, and the transfer nodes reconstruct the independently locked 32-realization Gaussian nonlinear/CLASS ratios to <= `1.7807695548234596e-08`.

## Scope

Because the original preregistered G4 failed:

- `THREE_D_ISOTROPIC_WEYL_TRANSFER_NODES_LICENSED=False`
- `THREE_D_ISOTROPIC_WEYL_POWER_NODES_LICENSED=False`
- `THREE_D_CONTINUOUS_WEYL_POWER_LICENSED=False`
- `EVOLVING_WEYL_POWER_LICENSED=False`
- `ACT_LIKELIHOOD_LICENSED=False`
- `OBSERVATIONAL_CLAIM_LICENSED=False`

A separate post-failure, preregistered zero-safe phase audit is required before any node license can be reconsidered.
