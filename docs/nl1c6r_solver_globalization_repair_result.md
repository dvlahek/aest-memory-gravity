# NL1C6R result — deterministic globalization repair

Final preregistered classification:

**NL1C6R_FULL_J_BARYONIC_RECLOSURE_FAIL**

This is a **numerical continuation failure**, not evidence that the published full-J baryonic quasistatic field system has no physical solution.

Historical NL1C6 result remains unchanged: `NL1C6_FULL_J_BARYONIC_RECLOSURE_FAIL`.

NL1C6R predata commit: `f7666cbb7b12b84fca26d934ab81bc5fc9020745`.

Scientific repair implementation commit: `c1897b252a6a5c5f3013233e049b5c5e34f2858f`.

Import-path technical fix commit: `3ecc576b27dd1451987f5747d2698eebbf9503cc`.

Final workflow/logging commit: `ff0c75595c69ae8b7a966df4958755a32c3a9593`.

Final GitHub Actions run: `34346655008` — technical SUCCESS with honest scientific FAIL classification.

Artifact: `results_bundle_nl1c6r_solver_globalization_repair`, ID `10103396065`, SHA256 `6233521bf8e5f6af7a7587ba03f081159a3b725aae5dea9cdb52696fb5eefdb9`.

The main numerical step ran from `2026-09-09T11:38:56Z` to `2026-09-09T12:19:04Z` (about 40 min 8 s).

No observational data, finite physical eta, memory source, or matter re-evolution was used.

## Controls that passed

- NL1C5B baryon-source artifact identity: PASS.
- Requested native k-mode identity: PASS, maximum relative miss `0.0`.
- Frozen high-gradient analytic regression: PASS for every beta0 and every evaluation snapshot.
- Maximum high-gradient regression error: `1.5679255329173794e-14`.
- No distinct residual-valid alternate root was found before the primary continuation failed.

The high-gradient control again strongly constrains the implementation signs, `1+beta0` factors, physical-coordinate Laplacian, baryonic source normalization, and `Phi=tildePhi+chi` reconstruction.

## What NL1C6R repaired

NL1C6R changed only numerical globalization:

- source homotopy refined to `lambda = 2^-24, 2^-23, ..., 2^-1, 1`;
- deterministic Newton backtracking extended to `alpha = 2^-m`, `m=0,...,40`;
- Newton maximum increased to 60 iterations;
- the same analytic JVP, Fourier preconditioner, physical equations, source, branches, and final physical gates were retained.

This repair successfully crossed the exact first point where NL1C6 had failed.

For example, for Simple with `beta0=1` at `z=6`, the first four source amplitudes converged:

- `lambda=2^-24`: relative residual `2.8373621138701177e-13`;
- `lambda=2^-23`: `5.07409242197527e-13`;
- `lambda=2^-22`: `1.267722424852895e-16`;
- `lambda=2^-21`: `7.559215084200435e-12`.

The next step, `lambda=2^-20 = 9.5367431640625e-7`, reached the 60-iteration limit with relative residual `0.04207572781686791`.

## Failure pattern

All nine co-primary branches enter the full-J branch at very small source amplitude but fail while continuing toward larger lambda on the first native slice `z=6.000000000000045`.

The approximate first failed homotopy scales are systematic in beta0 and largely insensitive to interpolation family:

- `beta0=0.1`: failure around `lambda=2^-23`, residual about `1.6e-3`;
- `beta0=0.5`: failure around `lambda=2^-21`, residual about `4.5e-2` to `1.08e-1`;
- `beta0=1.0`: failure around `lambda=2^-20`, residual about `3.46e-2` to `4.21e-2`.

Simple, Exponential, and Sharp show the same qualitative transition. This is inconsistent with a random interpolation-specific coding error and instead indicates that fixed-parameter source continuation is approaching a nearly singular/fold region of the nonlinear field branch.

The linearized full-J operator has the schematic Fourier stiffness

`-A_eff k_phys^2 + mu^2 (1 + A_eff)`

with `A_eff = j + x dj/dx`. Starting from the zero-source mass-dominated branch, increasing source amplitude drives `A_eff` upward and can make a sourced mode nearly singular before the physical `lambda=1` state is reached. Ordinary lambda-homotopy then becomes ill-conditioned even when the connected nonlinear branch continues through a fold.

## Consequence

NL1C6R remains an immutable FAIL under its preregistered numerical prescription. It establishes two useful facts:

1. the full-J branch can be entered from the zero-source state;
2. ordinary source-amplitude continuation is not a reliable branch parameter through the observed near-singular regime.

The next solver repair must therefore keep all physical equations and gates frozen while replacing fixed-lambda continuation by a deterministic **pseudo-arclength continuation in `(chi, lambda)`**, allowing the connected zero-source branch to be followed through folds without assuming that lambda is locally monotonic.

Only a residual-valid physical `lambda=1` trajectory permits the next eta=0 retarded-memory source/tangent test.
