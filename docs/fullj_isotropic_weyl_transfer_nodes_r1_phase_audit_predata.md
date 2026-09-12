# Full-J isotropic Weyl transfer nodes R1 — zero-safe phase audit pre-data declaration

## Status

This audit is preregistered after the historical transfer-node milestone returned

`FULLJ_ISOTROPIC_WEYL_TRANSFER_NODES_FAIL`

solely because G4 used the pointwise ratio `|Im T|/|T|`, whose maximum occurs near a real-transfer zero crossing.

The historical FAIL remains unchanged. This R1 audit does not modify the original G4 threshold or reclassify the original run.

## Required ancestry

- original transfer predata: `b02960733256e27d4c1883a30031392c68a5cf74`
- original transfer implementation: `9e78fb19e0aa7a554bd7a60b0cde18ff5c13fa80`
- original transfer runner: `a4e26d29b4a8b6ceba67151aabe01db74406a93f`
- historical transfer FAIL result lock: `b7bb0aef90ec935821f4dc1a63db0d79966a15f8`

The local input is the completed original JSON:

`results/fullj_isotropic_weyl_transfer_nodes.json`.

No CLASS run, nonlinear trajectory rerun, interpolation, fitting, or parameter change is permitted.

## Frozen question

Determine if the failed pointwise G4 is caused by an ill-conditioned local normalization near a transfer zero while the actual quadrature leakage remains negligible for the transfer and power nodes.

Let

`T = Re(T) + i Im(T)`

for the stored six-mode transfer nodes, and `T_single` for the stored single-mode nodes.

## Zero-safe diagnostics

### 1. Global quadrature norm

Define

`eps_Q_global = ||Im T||_2 / ||T||_2`

across all 54 `(k,z)` nodes, and analogously `eps_Q_single` from the stored single-mode transfer nodes.

This remains well-conditioned when an individual real transfer crosses zero because the denominator is the full grid norm.

### 2. Absolute quadrature leakage

Define

`Q_abs_max = max |Im T|`

and the analogous single-mode quantity.

The transfer is dimensionless, so this is a direct absolute numerical leakage diagnostic.

### 3. Real-projection power contamination

Define nodewise

`Delta_complex = P_R * |T|^2`

and

`Delta_real = P_R * Re(T)^2`.

Measure

`eps_power_max = max |Delta_complex-Delta_real| / max(Delta_complex,tiny)`.

This directly tests if the quadrature component matters for the physical power nodes.

### 4. Historical non-phase gate lock

The original completed JSON must show exactly one failed gate, G4. G1–G3 and G5–G9 must all remain true.

## Frozen gates

### R1-G1 — provenance and historical-state lock

All required commits are ancestors of HEAD. The local original JSON must have classification

`FULLJ_ISOTROPIC_WEYL_TRANSFER_NODES_FAIL`

and exactly G4 false with all other original gates true.

### R1-G2 — global zero-safe phase consistency

Use the original phase threshold unchanged:

- `eps_Q_global <= 1e-8`
- `eps_Q_single <= 1e-8`.

### R1-G3 — absolute quadrature leakage

Again use the same numerical scale `1e-8` without fitting:

- `max |Im T| <= 1e-8`
- `max |Im T_single| <= 1e-8`.

### R1-G4 — physical power contamination

Require

`eps_power_max <= 1e-12`.

This matches the existing algebraic power-node precision gate.

### R1-G5 — retained independent validations

The stored original summary must still satisfy the original preregistered non-phase limits:

- separability median <= `5e-4`, max <= `5e-3`
- off-target leakage max <= `5e-3`
- amplitude-homogeneity median <= `5e-4`, max <= `5e-3`
- Gaussian reconstruction median <= `5e-3`, max <= `2e-2`
- power identity residual <= `1e-12`.

No value is recomputed with a fitted phase or adjusted transfer.

## Classification

PASS:

`FULLJ_ISOTROPIC_WEYL_TRANSFER_NODES_R1_PHASE_AUDIT_PASS`

FAIL:

`FULLJ_ISOTROPIC_WEYL_TRANSFER_NODES_R1_PHASE_AUDIT_FAIL`

INCOMPLETE:

`FULLJ_ISOTROPIC_WEYL_TRANSFER_NODES_R1_PHASE_AUDIT_INCOMPLETE`

## Licensing rule

Only if all R1 gates pass may the stored physical transfer be projected to its real part and the already constructed six discrete nodes be licensed:

- `THREE_D_ISOTROPIC_WEYL_TRANSFER_NODES_LICENSED=True`
- `THREE_D_ISOTROPIC_WEYL_POWER_NODES_LICENSED=True`.

Even after PASS:

- `THREE_D_CONTINUOUS_WEYL_POWER_LICENSED=False`
- `EVOLVING_WEYL_POWER_LICENSED=False`
- `ACT_LIKELIHOOD_LICENSED=False`
- `OBSERVATIONAL_CLAIM_LICENSED=False`.

The next milestone after PASS remains a separately preregistered dense-k radial extension/convergence audit.
