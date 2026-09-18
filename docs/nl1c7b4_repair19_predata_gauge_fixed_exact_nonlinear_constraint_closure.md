# NL1C7B4 Repair19 — pre-data gauge-fixed exact nonlinear constraint closure

## Status

Pre-data / pre-run science preregistration.

Repair18d1 is frozen as

`NL1C7B4_REPAIR18D1_NULLSPACE_TRANSVERSALITY_AUDIT_PASS`

at result-freeze commit

`814450553dc9680f13f329cb6e578350498163aa`.

Frozen Repair18d1 result JSON:

- SHA-256:
  `21d5be34660f0054bd8550908f300de64ec1ec9e8f81e0f150c7c1540e3bf04c`.

Repair19 is the first post-localization nonlinear closure test allowed to impose the certified null-space conditions.

## Scientific question

Does the frozen Repair15a first-order eta=0 state admit a small, second-order, grid-stable exact nonlinear completion in the physical projection pair

- `L(r)`
- `R_t(r)`

after removing the two certified local null directions with the Repair18d1-selected conditions

- `Y4=0`
- `Qmean=0`?

A PASS must satisfy the unchanged historical exact nonlinear B4 threshold

`max epsilon_H <= 1e-7`

and

`max epsilon_M <= 1e-7`.

No threshold relaxation is permitted.

## Frozen parent state

Use the certified Repair15a density-Q-completed state.

Primary Nr=256 state:

- loaded directly from the frozen Repair15a NPZ.

Nr=512 state:

- reconstructed exactly with the frozen Repair16 procedure from the same Repair15a representation.

No B4 residual may be used to alter any parent field before the Repair19 projection.

## Physical projection

Only two physical fields may change:

- `L_minus_a`
- `Rdot_minus_aHr`.

All other state fields remain bitwise frozen.

Use the Repair18a coordinate definitions:

`L = L_p exp(y_L)`

and

`R_t = R_{t,p} + q_Rt (a H R_s)`,

with

`R_s = scale/h`.

Center corrections remain exactly zero.

## Exact gauge/regularity conditions

Repair18d1 certified the pair `Y4+Qmean`.

Repair19 imposes them exactly, not through penalty residuals.

### Y4

`Y4=0` means

`y_L[1]+y_L[2]+y_L[3]+y_L[4]=0`

over the first four non-center radial coordinates.

### Qmean

`Qmean=0` means

`sum_{i=1}^{m} q_Rt[i]=0`

over all non-center coordinates.

Because the Repair18d1 functionals were normalized, zero of the normalized functional is exactly equivalent to zero of these sums.

## Reduced-coordinate parametrization

Let `m=Nr-1`.

Construct an explicit sparse linear map

`x = B z`

from `2m-2` reduced coordinates to the full `2m` coordinate vector

`x=[y_L,q_Rt]`.

### y_L block

Use `m-1` reduced coordinates.

For the first four nodes use the local chain basis:

- column 1: `(+1,-1,0,0)`
- column 2: `(0,+1,-1,0)`
- column 3: `(0,0,+1,-1)`.

For nodes 5 through m use identity columns.

This spans exactly the subspace with first-four-node sum zero.

### q_Rt block

Use `m-1` reduced coordinates and the local first-difference chain:

- `q_1=z_1`
- `q_i=z_i-z_{i-1}` for `2<=i<=m-1`
- `q_m=-z_{m-1}`.

This spans exactly the mean-zero q_Rt subspace.

The reduced basis is fixed before the run and may not be changed.

## Reduced-basis checks

For both Nr=256 and Nr=512 require:

- shape `(2m,2m-2)`;
- finite sparse entries;
- full column rank `2m-2`;
- `||G B||_F <= 1e-12`, where G contains the normalized Y4 and Qmean rows;
- every reduced basis column has finite nonzero norm.

## Frozen nonlinear solver

For each scale/grid/lambda solve in reduced coordinates z.

Exact residual:

`F(z)=[N_H/D_H^p,N_M/D_M^p]`

on all non-center radial points, where:

- the numerator is the exact nonlinear frozen 11-source constraint numerator of the projected state;
- `D_H^p,D_M^p` are frozen from the unprojected parent at that same lambda before the solve.

Solver:

- `scipy.optimize.least_squares`
- method: `trf`
- Jacobian: `2-point`
- reduced sparse Jacobian pattern obtained structurally from
  `Repair18a_jac_pattern @ |B|`
- zero reduced-coordinate initial condition
- `x_scale='jac'`
- `ftol=1e-12`
- `xtol=1e-12`
- `gtol=1e-12`
- `max_nfev=400`
- no multistart
- no continuation between lambda values.

No explicit optimizer bounds are imposed in reduced coordinates because the exact null-space basis mixes physical coordinates.

Instead, every final full physical coordinate must satisfy the unchanged safety box

- `max |y_L| <= 0.5`
- `max |q_Rt| <= 0.5`.

A bound violation is a science FAIL.

## Frozen amplitude path

For every scale/grid solve independently at

- lambda = 1
- lambda = 1/2
- lambda = 1/4
- lambda = 1/8.

Scales:

- 5
- 10
- 20 h^-1 Mpc.

Grids:

- Nr=256
- Nr=512.

Total canonical solves:

`3 x 2 x 4 = 24`.

Canonical solve branch:

- Y = `Simple`
- beta = `1.0`.

## Exact canonical closure

For every one of the 24 canonical solves require:

- finite solver output;
- `L>0`;
- exact Q reconstruction normalized error <= `1e-12`;
- exact gauge residual `|Y4| <= 1e-12`;
- exact gauge residual `|Qmean| <= 1e-12`;
- full physical coordinate safety box respected;
- final moving-denominator exact nonlinear
  `max epsilon_H <= 1e-7`;
- final moving-denominator exact nonlinear
  `max epsilon_M <= 1e-7`.

The frozen parent-denominator least-squares residual is only the solver objective. It is not the PASS criterion.

## Second-order correction scaling

Use the same physical correction norm as Repair18/18a:

`C(lambda)=sqrt(mean[(delta L/a)^2] + mean[(delta R_t/(a H R_s))^2])`.

For each scale/grid compute adjacent log2 slopes.

Gate only:

- `1/2 -> 1/4`
- `1/4 -> 1/8`.

Require both in

`[1.8,2.2]`.

The `1 -> 1/2` slope is diagnostic only.

## Two-grid correction control

At lambda=1 require for every scale:

`max(C256,C512)/min(C256,C512) <= 2.0`.

Also report the exact post-projection H/M epsilon ratios across grids, but do not add a new threshold beyond both grids independently satisfying `1e-7`.

## All-branch lambda=1 retest

After solving the canonical Simple/beta=1 state independently on each scale/grid, evaluate that same projected state under every frozen historical branch:

Y:

- Simple
- Exponential
- Sharp

beta:

- 1.0
- 0.5
- 0.1.

This gives:

`3 scales x 2 grids x 3 Y x 3 beta = 54`

exact nonlinear lambda=1 cases.

Require all 54 to satisfy the unchanged historical threshold:

- max epsilon_H <= `1e-7`
- max epsilon_M <= `1e-7`.

No branch-specific refit or re-solve is allowed.

## Field-freeze invariant

For all 24 solved states require bitwise equality of every parent state field except:

- `L_minus_a`
- `Rdot_minus_aHr`.

## Output state artifact

Only if all science gates through the 54-case all-branch retest pass, write:

`results/nl1c7b4_repair19_gauge_fixed_exact_nonlinear_states.npz`.

The NPZ must contain lambda=1 projected states for all six scale/grid combinations.

Each stored state must include every state array required by the frozen exact evaluator plus metadata identifying:

- scale
- Nr
- selected conditions `Y4=0,Qmean=0`
- Repair18d1 JSON SHA-256
- Repair15a NPZ SHA-256.

If any science gate fails, the official Repair19 NPZ must not be written.

## Gates

### R19_G1 — exact frozen provenance

Require exact frozen hashes/classes/gates for Repair15a, Repair16, Repair17, Repair18, Repair18a, Repair18b1, Repair18c, Repair18d, and Repair18d1.

Require Repair18d1 selected candidate exactly:

`Y4+Qmean`.

### R19_G2 — exact reduced-basis construction

Require all reduced-basis checks at both grids.

### R19_G3 — unprojected parent reproduction

At lambda=1 reproduce the frozen Repair16 canonical Simple/beta=1 max-epsilon H/M values for all six scale/grid parent states to absolute-or-relative `1e-12`.

### R19_G4 — canonical gauge-fixed exact nonlinear closure

All 24 canonical solves satisfy every exact closure, gauge, positivity, Q, and safety-box requirement.

### R19_G5 — second-order correction scaling

All six scale/grid paths pass the frozen `[1.8,2.2]` gated slopes.

### R19_G6 — two-grid correction-amplitude control

All three lambda=1 scale pairs satisfy ratio <=2.0.

### R19_G7 — all-branch exact nonlinear closure

All 54 lambda=1 historical Y/beta cases satisfy both exact nonlinear `1e-7` constraints.

### R19_G8 — field-freeze invariant

Only L and R_t projection fields change.

### R19_G9 — output artifact integrity

If and only if G1-G8 pass:

- NPZ exists and is non-empty;
- exactly six scale/grid states are present;
- metadata are complete and match the frozen parent hashes/selected conditions;
- all arrays finite.

If G1-G8 do not all pass, require that the official NPZ does not exist.

### R19_G10 — claim boundary

Repair19 must not:

- change any source, coefficient, or sign;
- change any historical threshold;
- remove radial points;
- linearize Q;
- clip K;
- change eta from zero;
- solve branch-specific states;
- use multistart;
- use continuation between lambdas;
- alter Repair15a or any historical artifact;
- run nonlinear time evolution;
- make an observational claim.

## Terminal classifications

PASS:

`NL1C7B4_REPAIR19_GAUGE_FIXED_EXACT_NONLINEAR_CONSTRAINT_PASS`

Science FAIL:

`NL1C7B4_REPAIR19_GAUGE_FIXED_EXACT_NONLINEAR_CONSTRAINT_FAIL`

Implementation FAIL:

`NL1C7B4_REPAIR19_IMPLEMENTATION_FAIL`.

## Interpretation boundary

A PASS certifies an eta=0 initial state that:

- preserves the certified first-order Repair15a content;
- adds a small second-order nonlinear completion;
- removes the certified two-dimensional local null freedom with the independently selected Y4/Qmean conditions;
- satisfies the original exact nonlinear B4 threshold on all 54 historical branch/grid/scale cases.

Only after this PASS may the projected state be used for preregistered short-time nonlinear eta=0 evolution.
