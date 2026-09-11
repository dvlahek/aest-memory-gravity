# D2C6F-R2 result — action-consistent vector-phase direct memory stress

Date: 2026-09-11

Final classification:

`NL1C6D2C6F_R2_VECTOR_PHASE_DIRECT_SOURCE_PASS`

This result supersedes only the feedback license attached to the old-phase D2C6F-R1 reconstruction. The historical D2C6F FAIL and D2C6F-R1 PASS remain unchanged in the record.

## What R2 established

R2 corrected the local-vector reconstruction used by the direct memory stress from the positive spectral operator `|d_x| z_j` to the action-consistent signed derivative

`q_{j,x} = sqrt(w_j)/omega_j * d_x z_j`.

The local vector-phase identity passed with large margin:

- signed-gradient relative error: `7.628783208651e-15`;
- completed-square alignment residual: `2.170100946342e-15`;
- derivative bridge residual: `2.236512400012e-15`;
- old `|d_x|` forensic residual: `1.414213562373`.

The action finite-difference audit also passed:

- maximum metric-source finite-difference relative error: `2.594848457787e-10`.

All 27 direct-256 primary trajectories at `eta=0.125` were healthy, with retained scalar-current constraints at approximately `1e-15` to `1e-14`, positive `min(1+j_eff)`, and completed-square energy identities at approximately `1e-17`.

All preregistered convergence gates passed with very large margin:

- worst direct-256 versus direct-512 source/state control: `1.106970184749e-07` (gate `1e-2`);
- worst time control: `6.383582828297e-07` (gate `2e-3`);
- worst space control: `1.568535e-06` (gate `5e-3`).

The corrected source differs materially from the historical old-phase reconstruction. For the three frozen forensic sentinels the corrected-versus-old relative differences are order unity; the momentum-source difference is approximately `1.78193` in all three cases. The phase repair therefore changes the physical direct-stress prediction and was not a cosmetic numerical adjustment.

## Important non-gating physics diagnostic

R2 also projected the corrected direct memory stress one way through the preregistered Newtonian-gauge metric constraints. This projection was deliberately non-gating.

The largest reported one-way response is

- member: `sigma=-1|kind=simple|beta0=1`;
- checkpoint index: `8` (`z=0.2` in the frozen checkpoint ordering);
- `delta_phi_rms = 1.144427845661e8`;
- `delta_psi_rms = 3.289431912549e8`;
- `delta_weyl_rms = 2.145004066887e8`.

Even at the first `z=6` checkpoint, the same one-way diagnostic gives `delta_psi_rms` of order unity for the primary trajectories.

These amplitudes are far outside the weak-field regime. They do **not** invalidate the R2 source-convergence PASS because source amplitude was intentionally not a gate. They do mean that a self-consistent feedback run at `eta=0.125` would not be a controlled weak-field continuation of the present derivation.

## Interpretation

The correct project state after R2 is therefore:

1. the direct memory stress is now action-consistent and numerically converged;
2. the retained finite-memory trajectory certification remains intact;
3. a separately preregistered metric-feedback stage is formally re-licensed;
4. however, `eta=0.125` must **not** be used as the first feedback amplitude because the one-way metric response already leaves the weak-field domain by many orders of magnitude;
5. the next step must determine the small-eta weak-field admissibility scale from the independently certified eta=0 trajectory and the corrected direct stress before closing the feedback loop.

`OBSERVATIONAL_STEP_LICENSED=False` remains unchanged.
