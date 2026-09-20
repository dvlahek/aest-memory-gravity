# GE09 dense accepted-step local-jet bridge — implementation lock

## Status

Implementation locked before first GE09 execution.

## Preregistration

Commit:

`823ffd1a9da8e103e4568044f0f3ceb29c374aac`.

File:

`ge09/predata_dense_accepted_step_local_jet_bridge.json`.

Frozen blob:

`239a0296a25b3740e67c02759c1998560c37de4f`.

## Diagnostic trace patch

Commit:

`9dbda17590c99b5880ef94da149053cdbf038e15`.

File:

`ge09/apply_dense_accepted_step_trace_patch.py`.

Frozen blob:

`23b0cd22ebab499aee0ce03e6b3b678fe727ef55`.

The patch only adds a diagnostic trace inside
`perturbations_print_variables()`.

It does not modify any perturbation/background equation, source table or
solver tolerance.

## Audit implementation

Commit:

`0f73c284178c420df22d2368391e69d47fc7e69f`.

File:

`ge09/dense_accepted_step_local_jet_bridge.py`.

Frozen blob:

`ce12da94c81ec006cdc9097272e0407879977b78`.

## Successful-step semantics

Pinned NDF15 performs a fresh

`perturbations_derivs(tnew,ynew,f0)`

immediately before

`perturbations_print_variables(tnew,ynew,f0)`

at every successful integration endpoint.

Hence the GE09 dense trace carries physical RHS derivatives, not interpolating
polynomial derivatives.

## Frozen common-time representation

Window:

`0.2 <= z <= 1.5`.

Common coordinate:

`ln(a)`.

Nodes:

`64`.

Primary:

all successful accepted-step endpoints.

Control:

every second successful accepted endpoint for each k, with first/last retained.

Derivative-aware fields:

- phi;
- delta_dark;
- theta_dark;
- alpha_aest;
- E_aest.

Interpolation:

`CubicHermiteSpline`

with

`dF/dln(a) = F_prime/(aH)`.

Algebraic/background fields use

`PchipInterpolator`.

No off-window extrapolation is allowed.

## Complete GE06 local jet

The frozen directional entries are

`N,L,R,b,u,Lt,Lx,Rt,Rx,bx,ut,ux,pt,px,Nx`.

Spatial derivatives use analytic Fourier multipliers on the already frozen
NL1C4 six-mode representative.

No finite-difference spatial derivative is used.

## Frozen controls

Require:

- diagnostic trace versus CLASS `get_perturbations()` <= `1e-12` abs-or-rel;
- >= 16 successful endpoints per k inside the window;
- exactly 64 common nodes;
- primary representation versus GE08 accepted source-grid state <= `1e-4`;
- primary versus every-second-endpoint control:
  - global relative L2 <= `5e-4`;
  - pointwise abs-or-rel <= `2e-3`;
- closed scalar `pt` versus independent product-rule expression <= `1e-12`;
- all complete-jet entries finite.

## Classification

All gates pass:

`GE09_DENSE_ACCEPTED_STEP_LOCAL_JET_BRIDGE_PASS`.

Otherwise:

`GE09_DENSE_ACCEPTED_STEP_LOCAL_JET_BRIDGE_FAIL`.

## Project boundary

A PASS certifies only the complete first-order local-jet representation needed
by GE06.

GE08 Repair01 exact standard-matter incompleteness remains active.

Therefore GE09 never licenses a Z20 solve by itself.
