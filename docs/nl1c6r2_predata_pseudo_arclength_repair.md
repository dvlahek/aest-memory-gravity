# NL1C6R2 predata — pseudo-arclength continuation repair

Status: **PREREGISTERED BEFORE NL1C6R2 FIELD RESULTS**.

Frozen test label:

**NL1C6R2_PREDATA_PSEUDO_ARCLENGTH_REPAIR**

## Motivation fixed before data

NL1C6R (`34346655008`) was a technical-success / scientific-FAIL run. It established that the full-J branch can be entered at very small source amplitude, but ordinary fixed-parameter source homotopy stalls on the first native slice while approaching a nearly singular nonlinear regime. The failure is systematic across all three interpolation families and all three beta0 values.

NL1C6R is immutable and remains classified

**NL1C6R_FULL_J_BARYONIC_RECLOSURE_FAIL**.

Its final artifact is `results_bundle_nl1c6r_solver_globalization_repair`, ID `10103396065`, SHA256 `6233521bf8e5f6af7a7587ba03f081159a3b725aae5dea9cdb52696fb5eefdb9`.

The observed fixed-lambda failure is consistent with the linearized full-J stiffness approaching a sourced Helmholtz singularity,

`-A_eff k_phys^2 + mu^2 (1 + A_eff)`, with `A_eff = j + x dj/dx`,

so lambda need not remain a good local parameter even if the connected nonlinear branch continues. The declared repair therefore changes only the numerical continuation coordinate.

## Physics frozen unchanged

NL1C6R2 MUST use the same NL1C5B baryon-source artifact and the same physical equations, constants, source convention, interpolation functions, co-primary branches, periodic box, physical-coordinate derivatives, resolutions, and physical acceptance gates as NL1C6/NL1C6R.

In particular:

- input baryon artifact ID `10101422385`;
- input baryon artifact SHA256 `0ab60cbc32210ad3fb75c881f91a9db11148280e9223ea644680ed8cdfbaa590`;
- `K_B=0.0665`, `K2=9500`, `Q0=1e-4 Mpc^-1`;
- `mu^2=9.826739074217741e-05 Mpc^-2`;
- `a0=1.2e-10 m s^-2`;
- beta0 co-primary values `{1.0,0.5,0.1}`;
- interpolation families `{simple, exponential, sharp}`;
- `Nx=256` primary and `Nx=512` resolution control;
- all 24 native CLASS times for the primary trajectory;
- the eight native evaluation times in `0.2 <= z <= 1.5` for resolution/branch controls;
- baryons only in the field source;
- `physical_eta=0` and no memory forcing;
- no matter re-evolution, observational data, or likelihood.

No physical equation, interpolation, source amplitude, beta0, resolution, residual gate, or branch-selection gate may be changed in NL1C6R2.

## Frozen branch-selection principle

The physical snapshot used by this repair is the solution on the nonlinear branch **continuously connected to the homogeneous zero-source state** as the source-amplitude parameter lambda is introduced.

Ordinary lambda-homotopy assumes lambda is locally monotonic. NL1C6R2 instead follows the same connected branch by pseudo-arclength continuation in the augmented state `(chi, lambda)`. A fold in lambda is therefore allowed. The algorithm may not jump to an independently seeded root merely because it is easier to solve.

The first positive crossing of `lambda=1` reached while following the oriented zero-source-connected branch is the primary candidate for that snapshot. The candidate must then satisfy the unchanged physical residual gates at exactly `lambda=1`.

## Frozen scaling

For each snapshot and branch, let `rhs` be the full physical `lambda=1` right-hand side and `n` the grid size.

Define

`rhs_scale = ||rhs||_2`

and

`chi_scale = rhs_scale / (mu^2 sqrt(n))`.

Pseudo-arclength is performed in the dimensionless state

`y = chi / chi_scale`.

The arclength inner product is

`<dy1,dy2> = mean(dy1*dy2)`

for the field component plus the ordinary scalar product for lambda.

This scaling is frozen before the NL1C6R2 result and is not tuned branch by branch.

## Frozen initial points

The first snapshot of any independently continued solve starts from two residual-valid fixed-lambda points on the mass-dominated zero-source branch:

- `lambda0 = 2^-34`;
- `lambda1 = 2^-33`.

They are solved in increasing lambda order, starting from `chi=0` and then from the preceding converged state.

Both seed points must satisfy the numerical Newton tolerance. Failure of either seed is an NL1C6R2 solver failure; the seed amplitudes may not be changed after seeing the result.

## Frozen pseudo-arclength predictor/corrector

From two accepted points, the secant in `(y,lambda)` defines the oriented unit tangent. Tangent orientation is kept continuous by requiring non-negative inner product with the previous tangent.

Predictor:

`(y_pred,lambda_pred) = (y,lambda) + ds * tangent`.

Corrector solves the augmented system consisting of:

1. the unchanged physical full-J residual `F(chi,lambda) = 0`, where the baryonic source is multiplied by lambda;
2. the pseudo-arclength hyperplane through the predictor, orthogonal to the frozen predictor tangent.

The field Jacobian-vector product remains the analytic NL1C6 Jacobian. The lambda column is exactly `-rhs`. The augmented Newton step is solved by GMRES on the full `(n+1)` linear operator, not by a Schur complement requiring inversion of the potentially singular fixed-lambda field Jacobian.

The block preconditioner uses the existing Fourier field preconditioner for the field block and identity for the scalar arclength block.

Frozen augmented GMRES settings:

- `rtol=1e-9`;
- `atol=0`;
- restart `min(100,n+1)`;
- `maxiter=400`.

Frozen corrector limits:

- maximum augmented Newton iterations per predictor: `24`;
- deterministic backtracking `alpha=2^-m`, `m=0,...,24`;
- accept only a finite trial with strictly smaller combined augmented residual norm.

## Frozen arclength step control

- initial `ds = 2e-8`;
- minimum `ds = 1e-10`;
- maximum `ds = 0.10`;
- if a corrector converges in at most 4 Newton iterations, next `ds = min(1.5 ds, ds_max)`;
- if it converges in 5--8 iterations, keep `ds`;
- if it converges in more than 8 iterations, next `ds = max(0.7 ds, ds_min)`;
- on corrector failure, reject the predictor and retry from the last accepted point with `ds -> ds/2`;
- failure with the next step below `ds_min` is a solver failure;
- maximum accepted pseudo-arclength points per independently continued snapshot: `800`;
- terminate with solver failure if `|lambda| > 2` before a physical `lambda=1` crossing is obtained.

These controls are global and identical for all interpolation/beta/resolution branches.

## Exact lambda=1 correction

When two consecutive accepted arclength points first bracket `lambda=1`, linearly interpolate their fields in lambda and use that state as the initial value for an exact fixed-`lambda=1` Newton correction.

Frozen fixed-lambda Newton settings are the NL1C6R analytic JVP and Fourier preconditioner with:

- maximum Newton iterations `80`;
- Newton tolerance `2e-10` relative to `||rhs||_2`;
- GMRES `rtol=1e-8`, `atol=0`, restart `min(80,n)`, `maxiter=240`;
- backtracking `alpha=2^-m`, `m=0,...,40`;
- strict residual decrease.

Only a converged exact `lambda=1` state is passed to the unchanged NL1C6 physical diagnostics.

## Native-time continuation

For each `(interpolation,beta0)` primary branch:

1. obtain the highest-redshift native snapshot by the frozen pseudo-arclength method above;
2. for each later native time, first attempt the unchanged fixed-`lambda=1` Newton solve from the preceding accepted native-time field;
3. if that direct time continuation fails, independently recover the current snapshot by the same frozen zero-source-connected pseudo-arclength method above.

This fallback preserves the same branch-selection rule without modifying the source or physics.

For `Nx=512` resolution controls, first attempt fixed-`lambda=1` Newton from the spectrally resampled `Nx=256` primary solution. If it fails, use the same frozen pseudo-arclength recovery at `Nx=512`.

## Physical gates unchanged

NL1C6R2 inherits the NL1C6 gates without relaxation:

- G1 input/source identity: PASS required;
- G2 high-gradient analytic regression: maximum error `<=1e-10`;
- G3 every primary solution converged and finite;
- G3 `R1_relative_L2 <= 1e-10`;
- G3 `R2_relative_L2 <= 1e-8`;
- G4 maximum `Nx=256` versus `Nx=512` discrepancy `<=5e-3`;
- G5 no distinct residual-valid alternate root with low-mode chi difference `>1e-4`.

The alternate deterministic high-gradient and mass-dominated starts remain unchanged and are not used to replace the pseudo-arclength primary branch.

## Frozen classifications

If G1--G4 pass and G5 finds no distinct residual-valid root:

**NL1C6R2_FULL_J_BARYONIC_RECLOSURE_PASS**

If G1--G4 pass but G5 finds a distinct residual-valid root:

**NL1C6R2_FULL_J_MULTIBRANCH_REQUIRES_BOUNDARY_SELECTION**

Otherwise:

**NL1C6R2_FULL_J_BARYONIC_RECLOSURE_FAIL**

## Continuation rule

Only `NL1C6R2_FULL_J_BARYONIC_RECLOSURE_PASS` permits the next eta=0 retarded-memory source/tangent test on the full reclosed native-time chi trajectory.

A FAIL caused by inability to traverse the augmented continuation remains a numerical result and must not be reinterpreted as evidence that the physical full-J field equations lack a solution. A residual-valid multibranch result is a physical branch-selection issue and must not be repaired by solver tuning.
