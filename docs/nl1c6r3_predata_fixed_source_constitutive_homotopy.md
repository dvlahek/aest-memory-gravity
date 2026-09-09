# NL1C6R3 predata — fixed-source constitutive homotopy repair

Status: **PREREGISTERED BEFORE NL1C6R3 FIELD RESULTS**.

Frozen test label:

**NL1C6R3_PREDATA_FIXED_SOURCE_CONSTITUTIVE_HOMOTOPY**

## Motivation fixed before data

NL1C6R2 (`34351229257`) completed technically but was scientifically classified

**NL1C6R2_FULL_J_BARYONIC_RECLOSURE_FAIL**.

Its artifact `results_bundle_nl1c6r2_pseudo_arclength_repair` has ID `10108738796` and SHA256 `74fd5007cb12413baf1011de155b23437f3bbd1db140bfbd472af6a81c47d9cb`. The immutable result document is `docs/nl1c6r2_pseudo_arclength_repair_result.md`.

R2 established that pseudo-arclength can enter and follow the zero-source-connected full-J branch through a fold, but all nine co-primary interpolation/beta branches terminate numerically on the first native slice near positive source amplitudes of order `3e-7`--`7e-7`, with the arclength step driven to about `1e-10`. This is many orders of magnitude below the physical source amplitude `lambda=1`.

The observed scale is consistent with a true near-singular Helmholtz/Jacobian regime. For locally constant `A_eff=j+x dj/dx`, the Fourier-space field Jacobian contains the factor

`-A_eff k_phys^2 + mu^2 (1+A_eff)`.

Therefore another attempt to push the same zero-source source-amplitude branch with smaller `ds`, more Newton iterations, or a looser physical gate is not an admissible repair.

NL1C6R3 instead asks a different numerical existence question at the **full physical baryonic source**: can the unchanged full-J endpoint equation be reached continuously from either of two exact constitutive anchors while keeping the source amplitude fixed at one?

## Physics frozen unchanged

NL1C6R3 MUST use the same NL1C5B baryon-source artifact and the same endpoint physical equations, constants, source convention, interpolation functions, co-primary branches, periodic box, physical-coordinate derivatives, resolutions, and physical acceptance gates as NL1C6/NL1C6R/NL1C6R2.

Frozen inputs and constants include:

- NL1C5B artifact ID `10101422385`;
- NL1C5B artifact SHA256 `0ab60cbc32210ad3fb75c881f91a9db11148280e9223ea644680ed8cdfbaa590`;
- `K_B=0.0665`, `K2=9500`, `Q0=1e-4 Mpc^-1`;
- `mu^2=9.826739074217741e-05 Mpc^-2`;
- `a0=1.2e-10 m s^-2`;
- beta0 co-primary values `{1.0,0.5,0.1}`;
- interpolation families `{simple, exponential, sharp}`;
- baryons only in the field source;
- `Nx=256` primary and `Nx=512` resolution control;
- all 24 native CLASS times for the primary trajectory;
- the eight native evaluation times in `0.2 <= z <= 1.5` for resolution and branch controls;
- `physical_eta=0`; no retarded-memory forcing, no matter re-evolution, no observational likelihood.

At the physical endpoint theta=1 the equation is exactly the original NL1C6 full-J baryonic equation. No endpoint source amplitude, physical parameter, residual gate, resolution gate, or branch-selection gate may be changed.

## Fixed-source constitutive anchors

For a given full physical right-hand side `rhs`, interpolation `j_full(x)`, and beta0, two deterministic homotopies are co-primary numerical routes.

### S: screened/high-gradient anchor

`j_S(theta,x) = (1-theta)/beta0 + theta j_full(x)`.

At `theta=0` this is exactly `j=1/beta0`. The initial field is the existing analytic high-gradient baryonic Helmholtz solution already validated by the NL1C6 regression. At `theta=1`, `j_S=j_full`.

Holding chi fixed,

`d j_S / d theta = j_full - 1/beta0`.

The chi-Jacobian coefficient is

`A_eff,S = (1-theta)/beta0 + theta (j_full + x dj_full/dx)`.

### M: mass-dominated anchor

`j_M(theta,x) = theta j_full(x)`.

At `theta=0`, the nonlinear divergence term vanishes and the exact zero-mean anchor is

`chi = rhs/mu^2`.

At `theta=1`, `j_M=j_full`.

Holding chi fixed,

`d j_M / d theta = j_full`.

The chi-Jacobian coefficient is

`A_eff,M = theta (j_full + x dj_full/dx)`.

Both routes therefore terminate at exactly the same physical endpoint equation. They are numerical continuation coordinates only and are not alternate physical models.

## Frozen seed selection

For each independently recovered snapshot and each anchor route, theta=0 is the exact analytic anchor. A second residual-valid point is selected deterministically by trying, in this fixed order,

`theta1 in {2^-8, 2^-10, 2^-12, 2^-14, 2^-16, 2^-18, 2^-20, 2^-22, 2^-24, 2^-26, 2^-28, 2^-30}`.

The first candidate in this ordered list that converges under the frozen fixed-theta Newton tolerance is used. No candidate may be inserted, deleted, or reordered after results are seen. Failure of all candidates is a route failure.

## Frozen pseudo-arclength coordinate

Continuation is performed in the augmented state `(y,theta)`, where

`y = chi/chi_scale`,

and

`chi_scale = max(rms(chi_anchor), ||rhs||_2/(mu^2 sqrt(n)), 1e-300)`.

The field inner product is `mean(y1*y2)` and the theta coordinate uses the ordinary scalar product. Tangent orientation is kept continuous by non-negative overlap with the preceding tangent. Folds in theta are allowed.

Predictor/corrector continuation uses:

- initial `ds=1e-2`;
- minimum `ds=1e-8`;
- maximum `ds=1e-1`;
- maximum `1200` accepted arclength points per route;
- augmented Newton maximum `40` iterations;
- augmented residual tolerance `2e-10` for both normalized field residual and arclength constraint;
- deterministic backtracking `alpha=2^-m`, `m=0,...,40`, accepting only strict decrease of the combined augmented residual;
- on failed corrector, reject the predictor and retry with `ds -> ds/2`;
- after convergence in at most 4 Newton iterations, `ds -> min(1.5 ds,ds_max)`;
- 5--8 iterations: keep `ds`;
- more than 8 iterations: `ds -> max(0.7 ds,ds_min)`;
- route failure if the next step falls below `ds_min`;
- route failure if `|theta|>2` before the first positive theta=1 crossing.

When consecutive accepted points first bracket theta=1, their fields are linearly interpolated in theta and corrected at exact theta=1 by the unchanged full-J fixed-source Newton solve. Only an exact theta=1 state satisfying the frozen solver tolerance is an endpoint candidate.

## Frozen bordered augmented preconditioner

R2 used a block-diagonal augmented preconditioner. R3 replaces only that numerical component by a bordered preconditioner that retains the parameter/field coupling.

For the normalized augmented Newton system

`[ A  b ; t_y^T  t_theta ] [dy,dtheta]^T = [r,gamma]^T`,

let `M` be the existing Fourier approximation to the inverse field Jacobian in the same physical state. Define

`z = M_A r`, `w = M_A b`,

where `M_A` includes the frozen rhs/chi normalization used by the augmented field equation. Then

`den = t_theta - <t_y,w>`,

`dtheta = (gamma - <t_y,z>)/den`,

`dy = z - w dtheta`.

This bordered action is used as the GMRES preconditioner. If `den` is non-finite or has absolute value below `1e-12`, the preconditioner deterministically falls back to the R2 block-diagonal action for that application; this fallback changes no physical residual or acceptance gate.

Frozen augmented GMRES settings:

- `rtol=1e-10`, `atol=0`;
- restart `min(100,n+1)`;
- `maxiter=600`.

The theta column is evaluated analytically from the constitutive formulas above; finite-difference parameter columns are forbidden.

## Fixed-theta and endpoint Newton settings

All fixed-theta seed solves and exact theta=1 endpoint corrections use analytic JVPs and the existing Fourier field preconditioner with:

- maximum Newton iterations `80`;
- relative residual tolerance `2e-10` against `||rhs||_2`;
- GMRES `rtol=1e-8`, `atol=0`, restart `min(80,n)`, `maxiter=300`;
- deterministic backtracking `alpha=2^-m`, `m=0,...,40`;
- strict residual decrease.

## Primary endpoint and branch rule

For every independently recovered snapshot both S and M anchor routes are attempted.

- If neither route reaches a residual-valid theta=1 endpoint, the snapshot fails.
- If exactly one route reaches theta=1, that endpoint is the primary candidate.
- If both reach theta=1 and their low-mode chi difference is `<=1e-4`, the screened-anchor endpoint is used as the deterministic primary candidate and the two routes are classified as numerically consistent.
- If both reach theta=1 and their low-mode chi difference is `>1e-4`, the snapshot is flagged as a residual-valid multibranch case. The screened route is retained only as a deterministic reporting reference; the test cannot be classified PASS.

For later native times, first attempt the unchanged exact full-J fixed-source Newton solve from the preceding accepted native-time field. On failure, recover that snapshot with both frozen constitutive anchor routes above. Independent S/M anchor checks are additionally required at the eight native evaluation times even when direct time continuation succeeds, so a second endpoint branch reachable through a constitutive anchor cannot be hidden by the direct solver.

For `Nx=512` evaluation controls, first attempt fixed-source Newton from the spectrally resampled `Nx=256` primary field. If it fails, use the same dual-anchor recovery. The endpoint physical equation remains unchanged.

## Physical gates unchanged

NL1C6R3 inherits the NL1C6 physical gates without relaxation:

- G1 input/source identity: PASS required;
- G2 high-gradient analytic regression: maximum error `<=1e-10`;
- G3 every primary endpoint solution converged and finite;
- G3 `R1_relative_L2 <= 1e-10`;
- G3 `R2_relative_L2 <= 1e-8`;
- G4 maximum `Nx=256` versus `Nx=512` discrepancy `<=5e-3`;
- G5 no distinct residual-valid root with low-mode chi difference `>1e-4`.

The S/M dual-anchor comparison is part of G5 in addition to the historical deterministic high-gradient and mass-dominated direct-start controls.

## Frozen classifications

If G1--G4 pass and G5 finds no distinct residual-valid endpoint root:

**NL1C6R3_FULL_J_BARYONIC_RECLOSURE_PASS**

If G1--G4 pass but either S/M anchor comparison or the historical alternate-start control finds a distinct residual-valid endpoint root:

**NL1C6R3_FULL_J_MULTIBRANCH_REQUIRES_BOUNDARY_SELECTION**

Otherwise:

**NL1C6R3_FULL_J_BARYONIC_RECLOSURE_FAIL**

## Continuation rule

Only `NL1C6R3_FULL_J_BARYONIC_RECLOSURE_PASS` permits the next eta=0 retarded-memory source/tangent test on the full reclosed native-time chi trajectory.

A numerical FAIL remains a numerical result and may not be reinterpreted as evidence that the full-J endpoint equation has no physical solution. A residual-valid MULTIBRANCH result is a physical branch-selection issue and may not be repaired by selecting the favorable branch.

If both fixed-source constitutive anchors systematically fail to reach theta=1 despite the bordered pseudo-arclength repair, the next scientific step is to reconsider the static-snapshot branch-selection assumption and test dynamical field evolution rather than continue an open-ended sequence of static solver-tolerance relaxations.
