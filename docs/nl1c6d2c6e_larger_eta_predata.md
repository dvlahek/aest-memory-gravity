# NL1C6D2C6E pre-data declaration: larger-amplitude retained finite-eta scan

Date: 2026-09-10
Branch: `v053-exp-normalization-corrected`

## Parent certification

This stage is licensed only by the successful preregistered D2C6D retained finite-positive-eta run:

- parent workflow run: `34507347610`
- parent implementation/workflow head: `0e596eb342e56fae56287017876fb2ee07c4c2b4`
- parent classification: `NL1C6D2C6D_FINITE_POSITIVE_ETA_RETAINED_SCALAR_CURRENT_PASS`
- parent result: all D1--D8 true; 81/81 primary trajectories healthy; `LARGER_AMPLITUDE_RETAINED_ETA_STEP_LICENSED=True`.

This declaration is committed before any D2C6E numerical output is generated.

## Scientific question

D2C6E asks how far the already certified retained scalar-current finite-memory continuation can be increased in physical positive memory coupling before numerical/physical health or convergence is lost, and where measurable departure from the eta=0 tangent approximation begins.

It is not a search for a preferred sign, amplitude, or observational signal. No result-dependent change to eta values, ensemble membership, gates, resolutions, or completion functions is allowed on the result commit.

## Frozen model scope

The model and all non-memory parameters remain exactly those of D2C6C R7 / D2C6D:

- same corrected AeST background and CLASS v3.3.4 baseline,
- `K_B=0.0665`, `K2=9500`, `Q0=1e-4 Mpc^-1`, `Z0=1e-17 Mpc^-1`, `a0=1.2e-10 m/s^2`,
- same six Fourier modes and nine redshift checkpoints,
- same 27 nonlinear scalar-current completion members (`sigma in {-1,0,+1}`, `kind in {simple,exponential,sharp}`, `beta0 in {1,0.5,0.1}`),
- same derivative-bounded completion and `epsilon_mix=0.25`,
- same stable canonical variables and elliptic reconstruction,
- same Drude memory with `tau H0=1`, primary order 39 and control order 47,
- same exact `bath_advance` propagator and modewise regular full prehistory,
- external metric/matter sector remains frozen as in the certified R6/R7 tangent comparison,
- no memory background correction,
- no direct nonlinear memory Einstein stress,
- no nonlinear matter evolution,
- no observational likelihood.

Accordingly, a PASS here certifies only the retained scalar-current finite-memory model. It does not certify full nonlinear AeST+memory or an observational detection.

## Physical eta ladder

The co-primary larger-amplitude ladder is frozen to the next three dyadic values above the D2C6D maximum:

- `eta1 = 1/32 = 0.03125`,
- `eta2 = 1/16 = 0.0625`,
- `eta3 = 1/8  = 0.125`.

All three are physical positive eta values. There is no signed-lambda reinterpretation.

The previous certified maximum `eta=1/64=0.015625` is provenance only and is not re-fit or used to alter the new ladder after results are seen.

## Primary trajectories

All 27 nonlinear completion members are run at all three eta values at:

- `Nx=128`,
- `nstep=4096`,
- memory order 39.

Thus the exact co-primary coverage is 27 x 3 = 81 trajectories.

Each finite-eta run is evolved as a difference state `d = y_eta - y_0` together with the eta=0 base trajectory. The bath is driven by the actual finite-eta `chi_eta`, so the finite-memory feedback is nonlinear through the current state rather than frozen to the eta=0 source.

## Numerical controls at eta = 1/8

For every one of the 27 completion members, the largest eta is rerun with:

- bath-order control: order 47, `Nx=128`, `nstep=4096`,
- time control: order 39, `Nx=128`, `nstep=8192`,
- spatial control: order 39, `Nx=256`, `nstep=4096`.

Control trajectories must also remain finite, satisfy the same constraint threshold, and retain `min(1+j_eff)>0`. This is intentionally conservative and is declared before output.

## Frozen gates

The scientific PASS requires all of the following.

### E1 -- provenance and exact coverage

- parent D2C6D provenance matches the frozen parent identifiers,
- exactly 27 unique completion members are present,
- exactly 81 primary finite-eta trajectories are evaluated.

### E2 -- finite-eta source identity

Using the same deterministic source-identity audit as D2C6D at `eta=1/8`:

- elliptic reconstruction relative L2 <= `1e-10`,
- canonical source-increment relative L2 <= `1e-10`.

### E3 -- all primary and control trajectories healthy

For every primary and numerical-control trajectory:

- all evolved quantities finite,
- full canonical constraint residual <= `1e-10`,
- `min(1+j_eff) > 0`.

### E4 -- bath-order convergence at eta=1/8

Maximum displacement-field relative L2 difference between order 39 and order 47 across all 27 members and canonical displacement fields <= `1e-2`.

### E5 -- time convergence at eta=1/8

Maximum displacement-field relative L2 difference between 4096-step and 8192-step runs across all 27 members <= `2e-3`.

### E6 -- spatial convergence at eta=1/8

Maximum displacement-field relative L2 difference between `Nx=128` and spectrally resampled `Nx=256` runs across all 27 members <= `5e-3`.

### E7 -- scope clean

The result must explicitly state that it is retained scalar-current only and does not license a full nonlinear/observational claim.

There is deliberately no gate on response sign, response amplitude, monotonicity, tangent linearity, or the presence/absence of a nonlinear turnover.

## Predeclared non-gating nonlinearity diagnostics

For each completion member, eta, and each of `alpha`, `E`, and `chi`, report:

1. tangent remainder
   `R_tan(eta) = ||Delta y_eta - eta v0|| / (|eta| ||v0||)`,
   where `v0` is the already certified eta=0 tangent from D2C6C R7;
2. signed tangent projection divided by eta;
3. dyadic response-quotient change
   `||Delta y_eta1/eta1 - Delta y_eta2/eta2|| / ||Delta y_eta2/eta2||`
   and the analogous eta2--eta3 quantity;
4. displacement norms.

For descriptive interpretation only, the first eta at which `R_tan` exceeds 1% is called the onset of visible nonlinearity for that member/field; 5% is called strong departure from the tangent approximation. These thresholds do not affect PASS/FAIL.

## Outcome labels

PASS:
`NL1C6D2C6E_LARGER_ETA_RETAINED_SCALAR_CURRENT_PASS`

FAIL:
`NL1C6D2C6E_LARGER_ETA_RETAINED_SCALAR_CURRENT_FAIL`

Technical incomplete:
`NL1C6D2C6E_LARGER_ETA_RETAINED_SCALAR_CURRENT_INCOMPLETE`

A PASS licenses a separately preregistered still-larger retained-eta continuation. It does not license full nonlinear AeST+memory or an observational step.
