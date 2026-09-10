# D2C6F-R1 pre-data declaration — direct-bath gravitational-source convergence

Date: 2026-09-10

Parent D2C6F implementation head: `df953b9df86ee0b4d73d1691aa713535e27e57fa`.

Parent D2C6F historical result record: commit `0b7213a3c3e568dc0854fb1c1a33a055b746cb65`, classification `NL1C6D2C6F_FINITE_ETA_DIRECT_GRAVITATIONAL_SOURCE_FAIL`.

This follow-up is declared after the original F6 failure and before any D2C6F-R1 target result. The original FAIL is not changed.

## Scientific question

Determine whether the D2C6F F6 failure is caused by the previously compressed 39/47 bath representation when applied to quadratic direct metric-stress observables, or whether the direct gravitational source itself remains unconverged under an independent direct Drude quadrature.

No physics parameter is fitted or changed.

## Frozen physical scope

Retain exactly the D2C6F one-way direct gravitational-source construction from the NL0B/NL1C3B action. No metric/matter feedback is added here.

Freeze:

- `tau H0 = 1`;
- `eta = 0.125` only;
- the D2C6E/D2C6F background, CLASS histories, six seeded spatial modes/phases, periodic box and `z=6..0.2` checkpoint set;
- the same D2C6B nonlinear constitutive completion definitions;
- `Nx=128`, `Nstep=4096`;
- the exact D2C6F source definitions `S_Psi`, `S_Phi`, `S_b`, `S_shear`;
- the exact D2C6F spectral source comparison restricted to Fourier indices `n=0..32` and the symmetric relative-L2 normalization already frozen before D2C6F.

## Frozen member subset

The follow-up targets exactly the six members that failed the original F6 gate:

- `sigma=0`, `beta0=0.1`, `kind in {simple, exponential, sharp}`;
- `sigma=+1`, `beta0=0.1`, `kind in {simple, exponential, sharp}`.

No other completion member is part of the primary R1 gate.

## Independent direct Drude quadrature

Do not refit a compressed bath to D2C6F outputs.

Use the already-defined direct tan-Gauss-Legendre representation from `v019s/stable_bath.py`:

- Legendre nodes `z_i,w_i` on `[-1,1]`;
- `theta_i = pi(z_i+1)/4`;
- `omega_i tau = tan(theta_i)`;
- positive normalized weights `W_i = w_i/2`.

Freeze the direct quadrature sequence:

`N_bath = {128, 256, 512}`.

The `N=512` direct quadrature is the highest-order R1 reference. The earlier v0.19t program used the same direct-tan-GL construction as an independent continuum control; R1 does not use any D2C6F source result to choose these nodes or weights.

For diagnostic localization only, rerun the existing compressed orders `39` and `47` for the same six members and compare each with direct `N=512`. These compressed-vs-direct differences are not PASS/FAIL gates.

## Frozen gates

R1 PASS requires all of the following.

### R1 — provenance and exact coverage

- parent D2C6F implementation is an ancestor;
- parent FAIL-result record is an ancestor;
- this pre-data file is an ancestor;
- exactly six frozen members are evaluated at `eta=0.125`;
- direct orders are exactly `{128,256,512}`.

### R2 — direct quadrature identity

For each direct order:

- all frequencies are finite and strictly positive;
- all weights are finite and strictly positive;
- `abs(sum(weights)-1) <= 1e-12`.

### R3 — health and action identities

All direct-order trajectories must be finite and source-finite, retain the D2C6F scalar-current constraint `<=1e-10`, retain `min(1+j_eff)>0`, satisfy the completed-square energy identity `<=1e-12`, and have minimum completed-square energy `>=-1e-14`.

### R4 — direct source convergence

For every frozen member and each of `S_Psi`, `S_Phi`, `S_b`, `S_shear`, the direct `N=256` versus direct `N=512` source-signature relative L2 must satisfy

`<= 1e-2`.

This is the same numerical tolerance as the original D2C6F F6 source-convergence gate; the threshold is not relaxed.

### R5 — direct retained-trajectory convergence

For every frozen member, direct `N=256` versus direct `N=512` must satisfy

- canonical state relative L2 `<=1e-2`;
- `E` relative L2 `<=1e-2`.

### R6 — scope integrity

No source amplitude, source sign, completion ranking, eta scaling, Planck/ACT/SPT likelihood, metric feedback, or observational quantity is used as a PASS condition.

## Non-gating diagnostics

Report:

- direct `128 -> 256` and `256 -> 512` source differences by component/member;
- direct `128 -> 256` and `256 -> 512` state/E differences;
- compressed `39 -> direct512` and `47 -> direct512` source differences;
- which source component controls the maximum error;
- source RMS values at direct `N=512`;
- whether the direct sequence is numerically improving, as a diagnostic only.

No monotonic-convergence requirement is imposed because Gauss-Legendre quadratures are not nested.

## Classification and license

PASS label:

`NL1C6D2C6F_R1_DIRECT_BATH_SOURCE_CONVERGENCE_PASS`

FAIL label:

`NL1C6D2C6F_R1_DIRECT_BATH_SOURCE_CONVERGENCE_FAIL`

INCOMPLETE is reserved for technical execution failure before the frozen gate can be evaluated.

If and only if R1 passes, the next self-consistent weak-field feedback stage is licensed to use direct `N=256` as its primary bath and direct `N=512` as its bath-order control, under a new preregistration.

R1 does not license arbitrary-amplitude full nonlinear GR/AeST evolution or observational inference by itself.
