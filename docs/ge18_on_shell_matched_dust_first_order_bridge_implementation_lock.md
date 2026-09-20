# GE18 on-shell matched-dust first-order bridge — implementation lock

## Status

Implementation locked before the first GE18 result.

GE18 uses only the already completed local GE15 R1 outputs. It does not run CLASS.

## Purpose

The reduced H3 matter sector must be an actual solution of the linear pressureless equations before its quadratic GE07 source can be used.

GE18 therefore does not algebraically relabel the full standard CLASS sector as dust.

It constructs a new pressureless first-order state on the frozen GE15 metric and initializes that state by matching the full standard-sector absolute density and momentum at the upper edge of the frozen window.

## Dependencies

- `GE15_CANCELLATION_FREE_S_STATE_PRECISION_CLOSURE_PASS`;
- `GE16_LATE_TIME_STANDARD_MATTER_RESIDUAL_DIAGNOSTIC_PASS`;
- `GE17_LATE_TIME_STANDARD_BACKGROUND_DUST_DIAGNOSTIC_PASS`.

## Frozen local GE15 inputs

Required files:

- `results/ge15_R1_dense_accepted_step_trace.dat`;
- `results/ge15_R1_cli_background.dat`;
- `results/ge15_R1_cli_perturbations_k0_s.dat` through
  `ge15_R1_cli_perturbations_k5_s.dat`;
- `results/ge15_cancellation_free_s_state_precision_closure.json`.

The dense-trace SHA-256 must match the value recorded inside the GE15 PASS JSON.

The raw CLASS perturbation files are independently cross-checked against the dense trace using the frozen GE09/GE15 trace-control routine.

## Frozen standard-sector reconstruction

Using the raw CLASS species outputs,

`delta rho_std =
 rho_g delta_g
 +rho_b delta_b
 +rho_ur delta_ur
 +rho_ncdm delta_ncdm`.

`momentum_std =
 (4/3 rho_g) theta_g
 +rho_b theta_b
 +(4/3 rho_ur) theta_ur
 +(rho_ncdm+p_ncdm) theta_ncdm`.

The patched CLASS CDM slot is AeST effective dark and is excluded.

## Frozen reduced dust backgrounds

CLASS-density units:

- `C_min=2.566238549760586e-9`;
- `C_star=2.568543329983919e-9`;
- `C_max=2.5714842087496506e-9`.

For each case,

`rho_d=C/a^3`.

No additional background parameter is introduced.

## Frozen dust evolution

In pinned CLASS Newtonian-gauge conventions,

`delta_d'=-theta_d+3 phi'`;

`theta_d'=-(aH)theta_d+k^2 psi`.

The independent variable used numerically is `ln(a)`.

At

`a=1/(1+1.5)`,

for each k mode and each frozen C value, choose

`rho_d delta_d = delta rho_std`

and

`rho_d theta_d = momentum_std`.

After the initial match, the dust state evolves only with the exact pressureless equations above.

## Frozen GE07 variable map

CLASS background density convention is `(8 pi G/3) rho`.

GE07 uses

`varrho=8 pi G rho_phys`.

Therefore

`varrho_bar = 3 rho_d = 3 C/a^3`;

`delta varrho = 3 rho_d delta_d`.

For one real Fourier cosine mode,

`T_1=a theta_d/k^2`;

`delta T_t = psi`;

`delta T_x = -a theta_d/k`

on the sine phase.

The identity

`dot T_1=psi`

follows exactly from the frozen dust Euler equation.

No independent matter mode or coupling coefficient is added.

## Frozen numerical controls

Primary:

- DOP853;
- `rtol=1e-11`;
- `atol=1e-13`.

Control:

- DOP853;
- `rtol=2e-12`;
- `atol=2e-14`.

Require:

- primary/control absolute-density global relative L2 <= `1e-8`;
- primary/control momentum global relative L2 <= `1e-8`;
- initial absolute-density match relative error <= `1e-10`;
- initial absolute-momentum match relative error <= `1e-10`;
- `dot T_1=psi` abs-or-rel error <= `1e-9`;
- all outputs finite.

## No model-error acceptance gate

The difference between the on-shell reduced dust state and the full standard CLASS state is reported but does not determine GE18 PASS/FAIL.

That error must later propagate through the reduced-H3 Z20 matter envelope.

## Terminal classifications

Pass:

`GE18_ON_SHELL_MATCHED_DUST_FIRST_ORDER_BRIDGE_PASS`.

Fail:

`GE18_ON_SHELL_MATCHED_DUST_FIRST_ORDER_BRIDGE_FAIL`.

## Claim boundary

A PASS certifies:

- an internally consistent pressureless first-order standard-matter surrogate;
- the exact map from that surrogate into the GE07 directional variables;
- readiness of the reduced matter input for a later reduced-H3 Z20 solve.

It does not:

- declare the full standard sector exactly pressureless;
- relabel GE08;
- certify a full-species second-order CLASS solution;
- introduce finite eta;
- by itself establish a nonlinear observable.
