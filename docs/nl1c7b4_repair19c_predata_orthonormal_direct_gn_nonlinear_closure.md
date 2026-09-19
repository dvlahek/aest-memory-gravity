# NL1C7B4 Repair19c — pre-data orthonormal direct Gauss-Newton nonlinear closure

## Status

Pre-data / pre-run preregistration.

Repair19b1 is frozen as

`NL1C7B4_REPAIR19B1_ORTHONORMAL_DIRECT_LINEAR_FEASIBILITY_LSMR_STAGNATION_PASS`

at result-freeze commit

`5f33dd543f9b722438faa9659858be942287f14f`.

Frozen Repair19b1 result JSON:

- bytes: `36865`
- SHA-256:
  `33774c721bfd15c1c2f6b776408b3fc4623e3720f9199aa04fc43e8415be1a26`.

Repair19c is the first nonlinear solve licensed by that PASS.

## Scientific question

Can the same physical `(L,R_t)` correction pair, restricted to the same exact `Y4=0` and `Qmean=0` subspace, close the exact nonlinear eta=0 B4 Hamiltonian and momentum constraints when the nonlinear iteration uses the certified orthonormal coordinates and a deterministic direct rank-revealing Gauss-Newton step?

No new physical variable is introduced.

## Frozen parent and state map

Parent state:

- Repair15a density-Q completed state;
- exact same Repair16/R18/R19 reconstruction for Nr=256 and Nr=512.

Projection variables remain exactly:

- `L = L_parent * exp(y_L)`
- `R_t = R_t,parent + q_Rt * (a H R_s)`.

All nonprojection fields are bitwise frozen.

## Frozen constrained coordinates

Use exactly the Repair19a/Repair19b1 orthonormal Helmert basis `B_orth`.

Physical correction:

`x=(y_L,q_Rt)=B_orth z`.

This enforces exactly:

- `Y4 = 0`
- `Qmean = 0`.

No chain-basis nonlinear solve is permitted.

## Frozen virtual-amplitude domain

Use the same virtual perturbation path as Repair19:

`lambda = {1, 1/2, 1/4, 1/8}`.

Canonical solve branch:

- Y=Simple
- beta=1.

Scales:

- 5, 10, 20 h^-1 Mpc.

Grids:

- Nr=256,512.

Total nonlinear solves: 24.

## Frozen nonlinear residual

For each virtual parent state, define the solve residual exactly as Repair19:

`F(x)=[N_H/D_H^p, N_M/D_M^p]`

over non-center points, with denominators frozen from that virtual parent state.

Final certification always uses the exact moving-denominator nonlinear B4 epsilon from the solved state.

Historical exact closure threshold remains:

`epsilon_H <= 1e-7`
and
`epsilon_M <= 1e-7`.

No residual rescaling or threshold relaxation is allowed.

## Frozen Jacobian

At every nonlinear iteration:

1. evaluate the full physical-coordinate residual at current `x`;
2. compute the same SciPy grouped sparse two-point finite-difference Jacobian in physical `x=(y_L,q_Rt)` coordinates with the frozen Repair18a half-band-16 sparsity pattern;
3. form algebraically
   `J_orth = J_x B_orth`.

No reduced-coordinate finite-difference rule is introduced.

## Frozen direct Gauss-Newton step

At every iteration solve

`min ||J_orth dz + F||_2`

with

- `scipy.linalg.lstsq`
- LAPACK driver `gelsy`
- `cond=max(J_orth.shape)*eps_float64`
- `check_finite=True`.

GELSY is selected before the nonlinear run because the frozen Repair19b1 payload showed direct residual-space feasibility in all six lambda=1 cases and GELSY retained the full reduced rank in all six, including the two Nr=512 cases in which GELSD dropped one weak direction.

Returned numerical rank during nonlinear iterations is recorded but is not itself a pass criterion.

No LSMR, TRF, Levenberg-Marquardt, multistart, pseudorandom perturbation, or alternate driver fallback is allowed.

## Frozen globalization

Start every solve from

`z=0`.

Use deterministic backtracking over

`alpha = 1, 1/2, 1/4, 1/8, 1/16, 1/32, 1/64, 1/128`.

Objective:

`phi = 0.5 ||F||_2^2`.

A trial step is accepted only if:

1. all trial quantities are finite;
2. `max|y_L| <= 0.5`;
3. `max|q_Rt| <= 0.5`;
4. Armijo decrease holds:
   `phi_trial <= phi * (1 - 1e-4 alpha)`.

Use at most 12 accepted Gauss-Newton iterations.

If no backtracking amplitude is accepted, the solve fails.

No trust-region or regularization parameter is introduced.

## Frozen stopping rule

After the initial state and after every accepted step, evaluate the exact nonlinear moving-denominator constraints.

A solve is successful only if all are simultaneously true:

- finite state;
- `L>0`;
- exact-Q reconstruction error <= `1e-12`;
- `|Y4| <= 1e-12`;
- `|Qmean| <= 1e-12`;
- `max|y_L| <= 0.5`;
- `max|q_Rt| <= 0.5`;
- `max epsilon_H <= 1e-7`;
- `max epsilon_M <= 1e-7`;
- all frozen nonprojection fields remain bitwise unchanged.

No success declaration is permitted from objective decrease alone.

## First-step reproduction control

For each lambda=1 scale/grid case, the first GELSY linearized step at z=0 must reproduce the corresponding frozen Repair19b1 GELSY payload to abs-or-rel `1e-10` for:

- returned rank;
- predicted relative linear residual;
- max |y_L|;
- max |q_Rt|.

This verifies that Repair19c begins from the certified direct linear step.

## Correction scaling

For each scale/grid pair compute the final physical correction norm exactly as Repair18/19:

`C=sqrt(mean[(delta L/a)^2]+mean[(delta R_t/(a H R_s))^2])`.

As in Repair19, gate only the adjacent slopes

- lambda 1/2 -> 1/4
- lambda 1/4 -> 1/8

with

`1.8 <= log2(C_a/C_b) <= 2.2`.

The lambda 1 -> 1/2 slope is reported but not gated.

## Two-grid correction control

At lambda=1 require for every scale:

`max(C_256,C_512)/min(C_256,C_512) <= 2`.

## All-branch exact retest

Only after a lambda=1 canonical solved state passes the exact canonical nonlinear closure, retest that same state under all frozen source-dictionary branches:

- Y in {Simple, Exponential, Sharp}
- beta in {1, 0.5, 0.1}.

Across 3 scales x 2 grids x 9 branches = 54 retests, require:

- finite;
- max epsilon_H <= 1e-7;
- max epsilon_M <= 1e-7.

No branch-specific refit is permitted.

## Output state artifact

Write a new Repair19c NPZ only if all science and integrity gates before artifact validation pass.

The NPZ contains only the six lambda=1 solved physical states.

It must identify:

- Repair19b1 parent hash;
- Repair15a state hash;
- exact selected gauge `Y4=0,Qmean=0`;
- solver `orthonormal direct GELSY Gauss-Newton`.

If any preceding gate fails, no Repair19c state NPZ may remain.

## Gates

### R19C_G1 — exact frozen provenance

Require exact Repair19b1 PASS hash/classification/gates and all inherited parent hashes.

### R19C_G2 — orthonormal constrained basis

Require exact frozen orth basis reproduction at Nr=256 and 512, including gauge annihilation and orthonormality <=1e-12.

### R19C_G3 — exact parent reproduction

For all six lambda=1 parent cases reproduce Repair16 canonical pre-projection H/M values to abs-or-rel 1e-12.

### R19C_G4 — certified first-step reproduction

Require all six lambda=1 first direct GELSY steps to reproduce the frozen Repair19b1 GELSY linear payload under the rule above.

### R19C_G5 — exact canonical nonlinear closure

Require all 24 virtual-amplitude canonical nonlinear solves to satisfy the frozen exact stopping rule and historical `1e-7` H/M threshold.

### R19C_G6 — second-order correction scaling

Require the two gated small-lambda correction slopes for every scale/grid pair to lie in [1.8,2.2].

### R19C_G7 — two-grid correction amplitude

Require every lambda=1 symmetric two-grid correction ratio <=2.

### R19C_G8 — all-branch lambda=1 exact closure

Require all 54 frozen branch retests to satisfy the historical `1e-7` H/M threshold with no refit.

### R19C_G9 — field-freeze invariant

Require bitwise equality for every nonprojection field for all 24 canonical solved states.

### R19C_G10 — output integrity

If G1-G9 pass, require the newly written NPZ to reproduce all six lambda=1 solved states and metadata exactly.

If any of G1-G9 fails, require that no NPZ is present.

### R19C_G11 — claim boundary

Repair19c must not:

- add a physical field;
- modify Q, alpha, phi, matter variables, source dictionaries, coefficients, or signs;
- change eta from zero;
- change branch definitions;
- remove radial points or cases;
- change the historical 1e-7 threshold;
- use branch-specific fitting;
- run time evolution;
- make an observational claim;
- relabel any earlier repair.

## Terminal classifications

If G1-G4, G9, G10, or G11 fail:

`NL1C7B4_REPAIR19C_IMPLEMENTATION_FAIL`.

Else if G5 fails:

`NL1C7B4_REPAIR19C_ORTHONORMAL_DIRECT_GN_NONLINEAR_CLOSURE_FAIL`.

Else if G6 fails:

`NL1C7B4_REPAIR19C_CORRECTION_SCALING_FAIL`.

Else if G7 fails:

`NL1C7B4_REPAIR19C_TWO_GRID_CONTROL_FAIL`.

Else if G8 fails:

`NL1C7B4_REPAIR19C_CANONICAL_PASS_BRANCH_RETEST_FAIL`.

Else:

`NL1C7B4_REPAIR19C_ORTHONORMAL_DIRECT_GN_EXACT_NONLINEAR_CONSTRAINT_PASS`.

## Interpretation boundary

A PASS certifies an exact eta=0 nonlinear initial-state projection for the frozen `(L,R_t)` correction pair across the virtual-amplitude path, both grids, and all source-dictionary retests.

It does not certify short-time nonlinear evolution or any finite-eta or observational result.

Only after a PASS and result freeze may short-time eta=0 evolution be preregistered.
