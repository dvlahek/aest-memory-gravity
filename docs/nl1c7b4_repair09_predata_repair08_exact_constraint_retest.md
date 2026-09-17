# NL1C7B4 Repair09 — exact nonlinear B4 retest on certified Repair08 state

## Status

Locked before implementation.

Repair09 is licensed only by the frozen Repair08 result at commit `6a8812f9b8d9f4fa373212376b6c01b4649076aa`, classification `NL1C7A_REPAIR08_IDENTITY_PRESERVING_SCALAR_REPRESENTATION_CERTIFIED`.

Repair09 answers one question only: after replacing the historical cancellation-sensitive scalar representation by the certified identity-preserving Repair08 representation, do the frozen raw eta=0 B4 Hamiltonian and radial-momentum constraints satisfy the original B4 tolerance?

It is not a finite-eta test, nonlinear evolution test, observable test, or parameter fit.

## Frozen inputs

Primary certified state input:

- `results/nl1c7a_repair08_identity_preserving_primary_states.npz`;
- SHA-256 `4639f3b5c0afcddb2f98c8b9f6a9dbbf8661dac685b12d235c09075a106dafa7`;
- size `103024` bytes;
- Repair08 result JSON SHA-256 `054851decab71e79a05aca2bc9fb287bb1239c8fb425989f40920004c3d88453`.

Retained dense trace and coverage are the same frozen Repair01 inputs used by Repair08:

- dense trace artifact `10469031693`, SHA-256 `193325536405f9a21a238f5fbe71a772d2484a096dcbfec3d6007e825cc38f70`;
- exact 128 native k modes;
- `a_i=0.02`;
- scales `[5,10,20] h^-1 Mpc`.

The dense trace may be used only to recover the already frozen background quantities and to construct the 512-point radial control from the same certified Repair08 continuous Fourier representation. It may not be used to replace or alter the primary 256-point NPZ state.

## Frozen code semantics

Repair09 inherits the exact nonlinear raw-constraint dictionary from `nl1c7b/initial_constraint_certification_repair02.py` unchanged in physics content:

- exact nonlinear `Q` dictionary completion;
- exact Exp `K(Q)` sector;
- frozen non-K variational terms;
- frozen dust and standard-background terms;
- `Y` families `Simple`, `Exponential`, `Sharp`;
- `beta0 = 1.0, 0.5, 0.1`.

Repair09 inherits the identity-preserving scalar reconstruction from `nl1c7a/evaluate_identity_preserving_repair08.py` only for the radial-resolution control.

No coefficient, sign, source, branch, scale, point, radial interval, or normalization may be selected after execution.

## Frozen thresholds

The original B4 raw-constraint limit is retained exactly:

- `max epsilon_H <= 1e-7`;
- `max epsilon_M <= 1e-7`.

The exact nonlinear Q-dictionary preservation limit remains `1e-12`.

The historical Repair02 two-grid RMS control is retained exactly: for each scale/Y/beta case, the ratio between 256- and 512-point RMS residuals must be finite and <= `2.0` for both H and M.

No Repair05/06 `1e-5` linear-interface threshold is a Repair09 PASS criterion. Linear-interface values may be reported only as diagnostics.

## State use

### Primary Nr=256 state

For each scale 5, 10, 20, Repair09 must load the state arrays directly from the certified Repair08 NPZ. The primary B4 constraint evaluation must use these arrays and must not reconstruct or project them.

### Nr=512 control state

The 512-point state is a radial-resolution control of the same continuous Repair08 representation. It must be built with the frozen Repair08 canonical scalar transfer

`PCHIP(log(a), a Q theta_A/k^2)`

formed on the native time grid before interpolation, with all non-scalar fields from the frozen C7A constructor.

Before using the 512 control, the same reconstruction path at Nr=256 must reproduce every array in the certified Repair08 NPZ to relative L2 <= `1e-12`. This is an implementation/provenance gate, not a fit.

## Exact nonlinear Q dictionary

For each state, define the frozen target

`Q_target = Q_bg + delta Q`.

As in Repair02, recover the coordinate-time scalar derivative algebraically as

`phi_t = (Q_target - sinh(u) phi_r/L) / cosh(u)`

so that

`Q_exact = cosh(u) phi_t + sinh(u) phi_r/L`.

Require max normalized `Q_exact-Q_target <= 1e-12`.

This is the already frozen dictionary completion. It is not a constraint projection and does not modify the certified physical `Q_target`.

## Repair09 gates

### R9_G1 — exact Repair08 provenance

Require the exact Repair08 NPZ SHA-256, exact Repair08 result classification, all ten Repair08 gates true, correct metadata, 128 k modes, and frozen dense-trace coverage.

### R9_G2 — Repair08 state-anchor reproduction

Reconstruct the Repair08 Nr=256 representation through the locked continuous representation path and require every state array to reproduce the certified NPZ to relative L2 <= `1e-12`. The actual primary constraint calculation still uses the arrays loaded from the NPZ.

### R9_G3 — exact nonlinear dictionary

Require the frozen Q dictionary identity, max normalized Q error <= `1e-12`, finite Exp-sector quantities, and no clipping or linearization.

### R9_G4 — original raw B4 constraints

Evaluate all 54 frozen cases: 3 scales x 2 radial resolutions x 3 Y families x 3 beta values.

PASS requires every case to satisfy both

`max epsilon_H <= 1e-7`

and

`max epsilon_M <= 1e-7`

over all non-center radial points exactly as in the frozen Repair02 definition.

No tail, zero crossing, small-denominator point, Y family, beta value, scale, or radial point may be removed.

### R9_G5 — two-grid control

For all 27 matched scale/Y/beta cases, require the historical 256/512 RMS ratio <= 2.0 for H and M.

### R9_G6 — claim boundary

Require: no state projection, no coefficient fitting, no source insertion, no sign change, no K clipping, no Q linearization, no radial point removal, no threshold change, no nonlinear evolution, and no finite eta.

## Terminal classifications

Allowed terminal classes are:

- `NL1C7B4_REPAIR09_REPAIR08_EXACT_NONLINEAR_CONSTRAINT_PASS`;
- `NL1C7B4_REPAIR09_REPAIR08_RAW_CONSTRAINT_FAIL`;
- `NL1C7B4_REPAIR09_IMPLEMENTATION_FAIL`.

A PASS means only that the certified Repair08 eta=0 initial data satisfy the frozen B4 raw initial constraints under the original `1e-7` criterion and two-grid control. It licenses a separately preregistered short-time eta=0 evolution test. It does not imply finite-eta viability or observational detection.

A FAIL after R9_G1-R9_G3 pass means the historical scalar-representation artifact has been removed but a genuine remaining raw-constraint/model-interface mismatch persists. Historical B4/R05/R06 failures remain historical and are not rewritten.