# NL1C6D2AC pre-data: corrected baryon matter-sector audit

## Purpose

Re-run the historical D2A baryon matter-sector validation for the corrected Exp-normalization model, using only the newly frozen corrected baryonic source certified by `NL1C5BC_CORRECTED_BARYON_SOURCE_FREEZE_PASS`.

Historical `NL1C6D2A_BARYON_MATTER_SECTOR_AUDIT_PASS` remains unchanged and is not used as a PASS gate for the corrected model.

## Frozen model and inputs

- Branch: `v053-exp-normalization-corrected`.
- CLASS commit: `e85808324f51fc694d12e3ed7439552a3c3f9540`.
- Corrected Exp normalization certified by `NL1C6D2N_EXP_NORMALIZATION_AUDIT_PASS`.
- Corrected CLASS baseline certified by `NL1C6D2N_CORRECTED_CLASS_BASELINE_R1_PASS`.
- Corrected baryon source certified by `NL1C5BC_CORRECTED_BARYON_SOURCE_FREEZE_PASS`.
- Memory disabled, `eta=0`, no likelihood and no cosmological refit.
- Requested modes: `k_h=[0.03,0.05,0.08,0.10,0.15,0.20] h/Mpc`.

The workflow must regenerate the corrected NL1C5BC source in the same isolated corrected CLASS environment before running this audit. No historical source NPZ may be substituted.

## Gates

### A1 corrected source identity

Fresh corrected CLASS `d_b`, `d_m`, `k_h`, and `z` must match the regenerated corrected NL1C5BC frozen block:

- `k_h` relative maximum mismatch <= `1e-12`;
- `z` absolute maximum mismatch <= `1e-12`;
- `d_b` relative L2 <= `1e-10`;
- `d_m` relative L2 <= `1e-10`;
- all `d_b`, `t_b`, and `d_m` values finite;
- all six requested `k_h` values hit to relative miss <= `1e-12`.

### A2 Newtonian-gauge baryon continuity

On dense CLASS histories, use

`delta_b' + theta_b - 3 phi' = 0`.

If CLASS does not directly expose `phi_prime`, derive it only from a cubic spline of the dense CLASS `phi(tau)` history, as in historical D2A. Drop two edge points inside the audit window and require at least 20 interior samples per mode.

For each of the six modes in `0.2 <= z <= 6`, require normalized L2 residual <= `2e-3`. The maximum over modes is the gate quantity.

### A3 dense/native closure

Interpolate each dense CLASS `delta_b(z)` and `theta_b(z)` history onto the native transfer redshift samples for the corresponding requested mode. Require, for every mode:

- `d_b` relative L2 <= `2e-4`;
- `t_b` relative L2 <= `2e-4`.

### A4 conventions and scope

Record explicitly that CLASS `theta_b` is used as the Newtonian-gauge velocity divergence in the continuity equation above, with no added scale-factor redefinition.

No nonlinear full-J field evolution, branch selection, memory forcing, finite eta, observational likelihood, or cosmological refit is permitted in D2AC.

## Classification

PASS only if A1-A4 are satisfied:

`NL1C6D2AC_CORRECTED_BARYON_MATTER_SECTOR_AUDIT_PASS`

otherwise:

`NL1C6D2AC_CORRECTED_BARYON_MATTER_SECTOR_AUDIT_FAIL`

A PASS licenses the corrected-model source-dependent full-J static/reclosure gate. It does not by itself authorize nonlinear cosmological branch evolution, memory likelihood claims, or NL1C7.
