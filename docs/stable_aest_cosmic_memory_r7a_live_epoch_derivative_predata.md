# Stable AeST cosmic-memory R7a — live physical epoch derivative pre-data declaration

Date: 2026-09-15
Branch: `fullj-evolving-weyl-bridge`

## Purpose

R7 completed with the formal classification

`STABLE_AEST_COSMIC_MEMORY_R7_PHYSICAL_BRIDGE_FAIL`.

Its epoch-table reconstruction was internally accurate, but the frozen full-history replay tangent did not reproduce the direct physical R5b `effective_f_sigma8` derivative within the preregistered physical-bridge bound. R7a therefore removes force-table trace/replay transport entirely.

R7a asks the same causal question by a different first-order construction:

> Which cosmic redshift windows contribute to the direct physical observable derivative at eta=0 when the memory feedback is activated only inside that window?

R7a is not a re-run or reclassification of R7. R7 remains a completed historical FAIL.

## Frozen parents

R7a is preregistered after, and must lock:

1. R7 post-data checkpoint `cf0132f7877160948e1ba4670eda19750d82159b`, whose classification is exactly `STABLE_AEST_COSMIC_MEMORY_R7_PHYSICAL_BRIDGE_FAIL`;
2. R5b post-data checkpoint `3242335ece23fbeb743f075a1df1aa70acaab211`, whose classification is exactly `STABLE_AEST_OBSERVABLE_PROJECTION_R5B_DERIVATIVE_ZERO_CERTIFIED`.

The frozen R5b files remain:

- `results/stable_aest_observable_projection_r5b_derivative_zero.json`, SHA-256 `26ce723e2b7b783fcd19765c9c7f01b6101992a3f09e6ee321299bf148259ca9`;
- `results/stable_aest_observable_projection_r5b_derivative_zero.npz`, SHA-256 `a88f99254bc1a7393e40691d5dc539bb1e1648eae1b892e43b63f593f8e367e1`.

No historical classification may be changed by R7a.

## Mathematical construction

The physical memory feedback entering the stable-AeST E equation is proportional to

`eta * B_chi,raw(y_eta)`.

At eta=0,

`d/deta [ eta B_chi,raw(y_eta) ]|_0 = B_chi,raw(y_0)`.

Therefore the first-order derivative can be additively decomposed by multiplying only the physical feedback coefficient by complementary cosmic-time windows while leaving the bath states and all other equations live and self-consistent.

For a window `W_i(a)` define the diagnostic physical family

`eta * W_i(a) * B_chi,raw`.

The bath equations are not windowed or reset. The window acts only on the physical feedback from the already evolving memory bath into the E equation.

At eta=0 the tangent source is

`W_i(a) B_chi,raw(y_0)`,

so the sum of the four window derivatives must equal the full derivative because the windows form a partition of unity.

This construction does not require an external tangent hook, a frozen forcing table, interpolation in `(k,tau)`, or averaging repeated adaptive ODE evaluations.

## Frozen model and observables

Use the same physical/numerical regime as R5b and R7:

- frozen CLASS parent head `e85808324f51fc694d12e3ed7439552a3c3f9540`;
- certified stable `chi = Q s` residual dynamics;
- `tau H0 = 10`;
- memory order `20`;
- `tol_perturbations_integration = 3e-8`;
- no Halofit/nonlinear correction;
- canonical initialization anchor `k_h = 0.165` only for the frozen R5b initialization setup;
- `sigma8(z)` at `z = [0.2, 0.5, 1.0, 1.5, 2.0]`;
- CLASS `effective_f_sigma8(z)` on the same redshift grid;
- linear `C_L^{kappa kappa}`, `L=40,...,2000`, from raw CLASS `pp` using `[(L(L+1)/2)^2] C_L^{phiphi}`.

The parameter/output construction must otherwise match R5b.

## Disposable source topology

R7a must be built from a fresh copy of the same frozen CLASS parent. Apply the certified stable-chi patch, then neutralize exactly one dormant historical external variational forcing hook in the disposable source, as in R5b.

The final R7a source must contain:

- stable `chi = Q s` dynamics;
- exactly one physical memory closure `E_rhs_aest -= 0.5*Q_aest*Bchi_aest;`;
- exactly one physical eta multiplier, modified only by the R7a live epoch weight;
- zero `aest_tangent_external_force` calls in `perturbations_derivs`;
- zero R2d force-trace calls in `perturbations_derivs`;
- one R7a epoch-window helper.

The R7a helper may select one of five modes from a run-level environment variable:

- `full`;
- `ancient`;
- `intermediate`;
- `recent_structure`;
- `late`.

Any missing or unknown mode must fail closed rather than silently selecting a science window.

Each CLASS run must be a separate Python process so any cached environment selection is process-local.

## Frozen cosmic windows

Using the instantaneous CLASS scale factor `a`, define `z = 1/a - 1` and the same windows as R7:

- `ancient`: `z >= 10`;
- `intermediate`: `2 <= z < 10`;
- `recent_structure`: `0.5 <= z < 2`;
- `late`: `z < 0.5`.

For every finite positive `a`, exactly one of the four science windows must have weight one and the others zero. The `full` mode has weight one at all times.

No boundary may be changed after results are seen.

## Physical central derivatives

Primary derivative amplitude:

`epsilon = 0.025`.

For the full mode run

- eta = `+0.025`, `-0.025`.

For each of the four epoch modes run

- eta = `+0.025`, `-0.025`.

Also run the full mode at

- eta = `+0.05`, `-0.05`

as a first-order amplitude control.

Run one full-mode eta=0 baseline.

Total planned cosmology runs: 13.

For observable `X`, define

`T_X^full(eps) = [X_full(+eps)-X_full(-eps)] / [2 eps X_0]`,

and for epoch `i`

`T_X^i = [X_i(+0.025)-X_i(-0.025)] / [0.05 X_0]`.

Define

`T_X^sum = sum_i T_X^i`.

The signed negative-eta branch is a derivative diagnostic around eta=0. It is not interpreted as a separately physical cosmology.

## Epoch contribution metrics

Only if all certification gates pass, report for each observable vector:

1. signed projection fraction `p_i = (T_i dot T_full)/(T_full dot T_full)`;
2. norm share `||T_i|| / sum_j ||T_j||`;
3. cosine between `T_i` and the full tangent;
4. raw tangent norm.

For `sigma8` and `f sigma8`, also report signed epoch fractions at z=0.2.

Signed fractions may be negative and must not be clipped, renormalized into probabilities, or described as fractions of stored energy.

No condition is imposed on which epoch dominates.

## Gates

### R7A-G1 provenance and parent lock

PASS iff:

- the R7 post-data and R5b post-data commits above are ancestors of HEAD;
- the R7 classification is exactly `STABLE_AEST_COSMIC_MEMORY_R7_PHYSICAL_BRIDGE_FAIL`;
- the frozen R5b JSON/NPZ SHA-256 values match;
- the R5b classification is exactly `STABLE_AEST_OBSERVABLE_PROJECTION_R5B_DERIVATIVE_ZERO_CERTIFIED` with all R5b gates true.

### R7A-G2 live physical source topology

PASS iff the fresh disposable source satisfies all source-topology requirements above, has exactly one live R7a epoch helper, zero external replay hooks, and zero R2d trace hooks in `perturbations_derivs`.

### R7A-G3 finite physical runs and baseline identity

PASS iff all 13 runs complete with finite `sigma8`, `effective_f_sigma8`, and `C_L^{kappa kappa}`, with positive `sigma8` and `C_L^{kappa kappa}`, and the eta-zero R7a baseline reproduces the frozen R5b eta-zero baseline for all three observables to relative L2 `<=1e-10` and cosine `>=0.999999999`.

### R7A-G4 full central-derivative amplitude consistency

Compare the full-mode central tangents at epsilon=0.025 and epsilon=0.05.

PASS iff for each of `sigma8`, `f sigma8`, and `C_L^{kappa kappa}`:

- relative L2 difference `<=0.05`;
- cosine `>=0.995`.

### R7A-G5 direct physical bridge to R5b

Compare the R7a full-mode epsilon=0.025 central tangent with the frozen R5b eta=0.01 forward derivative-at-zero tangent.

PASS iff for all three observables:

- relative L2 difference `<=0.10`;
- cosine `>=0.995`.

This gate is deliberately the same normalization/shape bridge requirement that R7 failed, but R7a obtains the tangent directly from the live physical memory term instead of a transported force table.

### R7A-G6 live epoch reconstruction

Compare `T_X^sum` with `T_X^full(0.025)`.

PASS iff for all three observables:

- relative L2 difference `<=0.02`;
- cosine `>=0.999`.

No epoch-dominance threshold is permitted.

## Classification priority

1. `STABLE_AEST_COSMIC_MEMORY_R7A_INCOMPLETE`
2. `STABLE_AEST_COSMIC_MEMORY_R7A_PARENT_PROVENANCE_FAIL`
3. `STABLE_AEST_COSMIC_MEMORY_R7A_SOURCE_TOPOLOGY_FAIL`
4. `STABLE_AEST_COSMIC_MEMORY_R7A_RUN_FAIL`
5. `STABLE_AEST_COSMIC_MEMORY_R7A_CENTRAL_DERIVATIVE_FAIL`
6. `STABLE_AEST_COSMIC_MEMORY_R7A_PHYSICAL_BRIDGE_FAIL`
7. `STABLE_AEST_COSMIC_MEMORY_R7A_EPOCH_RECONSTRUCTION_FAIL`
8. if G1-G6 all pass: `STABLE_AEST_COSMIC_MEMORY_R7A_LIVE_LOOKBACK_DECOMPOSITION_CERTIFIED`.

## Claim discipline

A PASS licenses only that, in the frozen stable-AeST `tau H0=10` regime, the direct physical first-order observable derivative at eta=0 can be decomposed into the four predeclared redshift windows using a live physical feedback mask, with the summed epoch derivatives reconstructing the full direct derivative within preregistered tolerances.

A PASS may license reporting the measured epoch contributions as properties of this tested model/regime.

R7a does not license:

- observational detection;
- an eta or tau constraint;
- universality over other tau values;
- irreversible/permanent spacetime memory;
- a claim that gravity remembers the entire age of the Universe in an observationally measurable sense;
- any epoch-dominance statement not directly supported by the certified measured fractions.

A separate preregistered tau scan remains necessary for relaxation-time generality.
