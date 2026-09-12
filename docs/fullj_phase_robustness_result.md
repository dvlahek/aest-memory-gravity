# Full-J finite phase-robustness result

## Classification

`FULLJ_PHASE_ROBUSTNESS_PASS`

This document locks the one-shot finite phase-robustness test of the previously certified full-J local response operator. No further phase-count ladder is preregistered.

## Frozen scope

- Physical eta: `0`.
- Static/fixed-a nonlinear full-J snapshots only.
- Three new deterministic phase realizations: `phase_A`, `phase_B`, `phase_C`.
- Redshifts: `z={0.25,0.5,1.0}`.
- Nine co-primary full-J branches per redshift and phase realization: three interpolation kinds times `beta0={1,0.5,0.1}`.
- Thirteen Fourier modes per background.
- New nonlinear backgrounds: `81`.
- New tangent solves: `1053`.
- The original locked phase realization was not counted in the new gate.

## Final numerical result

All `81/81` new backgrounds completed and all `81/81` retained the preregistered local diagonal UV condition.

Diagonal high-k slopes across the 81 new backgrounds:

- minimum: `-2.069654785715396`
- median: `-2.0031800518464413`
- maximum: `-1.936767488911733`

Thus every new phase realization remains consistent with an approximately `k^-2` local high-k response and all satisfy the frozen `s_diag <= -1` gate.

Numerical controls:

- maximum source-amplitude regression relative error: `7.934752809006791e-15`
- maximum R1 relative L2 over the 81 records: `3.1101600054239727e-13`
- maximum R2 relative L2 over the 81 records: `1.9915572400418388e-10`
- maximum tangent relative residual over the 81 records: `9.963842308707554e-11`

These remain comfortably inside the frozen gates `R1<=1e-10`, `R2<=1e-8`, source-amplitude regression `<=1e-12`, and tangent residual `<=1e-8`.

## Phase-robust node-coupling result

At the preregistered node diagnostic `z=0.25`, `k_out=0.6 Mpc^-1`, all `27/27` new phase x branch cases satisfy the off-diagonal-majority criterion. The preregistered requirement was only `>=21/27`.

Frozen-source-shape full-to-diagonal Weyl-power ratio across those 27 new cases:

- minimum: `4110.295471495011`
- median: `10387.849269462577`
- maximum: `24898.23614409879`

Off-diagonal fraction:

- minimum: `0.9997567084880065`
- median: `0.9999037336821068`
- maximum: `0.9999598365123452`

Therefore the source-node/mode-coupling interpretation is not an artifact of the original spatial phase realization. In this finite preregistered phase quartet (original locked realization plus three new realizations), the local diagonal UV response remains stable while the node output remains overwhelmingly off-diagonal.

## Interpretation

The combined static full-J evidence now supports the following restricted statement:

1. The local diagonal full-J response is UV-regular and remains approximately `k^-2` across interpolation family, beta0, redshift, and the finite preregistered phase set.
2. Large raw scalar ratios `|Phi_k|/|S_k|` near source nodes are not local UV divergences. They arise because nonlinear mode coupling remains strong when the direct source Fourier coefficient is small.
3. A scalar transfer function `T(k,z)` is therefore not an adequate representation of the tested nonlinear full-J response near source nodes; the local response is operator-valued.

## Scope boundary

This result is **not** an evolving-FLRW Weyl-power calculation and does not license ACT lensing or any observational claim.

- `EVOLVING_FLRW_WEYL_POWER_LICENSED=False`
- `ACT_LIKELIHOOD_LICENSED=False`
- `OBSERVATIONAL_CLAIM_LICENSED=False`

The next physical step must address the evolving FLRW Weyl response `W=Phi+Psi` with the action-derived metric/matter constraints. The static identity `W=2 Phi` must not be promoted to evolving FLRW without that calculation.

Historical results remain unchanged.