# NL1C6D2B predata — FLRW source/gravity coupling audit

Status: **PREREGISTERED BEFORE NL1C6D2B COUPLED-GRAVITY RESULTS**.

Frozen label:

```text
NL1C6D2B_PREDATA_FLRW_SOURCE_GRAVITY_COUPLING_AUDIT
```

## Motivation

The chain entering this phase is

```text
NL1C6R3_FULL_J_BARYONIC_RECLOSURE_FAIL
NL1C6D1_DYNAMICAL_FORMULATION_AUDIT_PASS
NL1C6D2A_BARYON_MATTER_SECTOR_AUDIT_PASS
```

R3 is a numerical/static-snapshot failure, not a physical exclusion. D1 establishes the nonlinear-spatial longitudinal weak-field AeST gravitational reduction and its exact static full-J limit in the repository's 1D geometry. D2A establishes a same-model CLASS baryon density/velocity history satisfying the Newtonian-gauge continuity equation.

The remaining prerequisite before nonlinear cosmological branch evolution is to couple the D1 gravitational sector to the D2A time-dependent FLRW matter sector without inventing expansion, momentum-source, or damping terms.

NL1C6D2B is therefore a **formulation audit**, not yet the nonlinear branch-selection science run.

## Authoritative inputs

Retain exactly:

- `K_B = 0.0665`;
- `K2 = 9500`;
- `Q0 = 1e-4 Mpc^-1`;
- `beta0 in {1.0,0.5,0.1}`;
- `lambda_s = 1/beta0`;
- `mu^2 = 2 K2 Q0^2/(2-K_B)`;
- the Simple/Exponential/Sharp full-J interpolation functions already frozen in R3;
- the same Exp AeST homogeneous cosmology and CLASS commit `e85808324f51fc694d12e3ed7439552a3c3f9540`;
- the D2A matter fields `d_b`, `t_b`, `phi`, `psi` on the exact frozen native grid;
- the retained v0.77 memory-off AeST trace `(k,tau,a,H/H0,chi,Q)` where required for an independent linear cosmological regression.

No finite physical eta and no observational likelihood enters D2B.

## Background and time coordinate

The target background is spatially flat FLRW with the same background solution used by the frozen CLASS AeST model. The primary time variable is conformal time `tau` for comparison with CLASS. Any cosmic-time form must be related by `dt = a d tau` explicitly.

The reduction must retain the longitudinal 1D geometry used by the nonlinear repository calculations. The known 1D curl-null result remains valid, but it does not justify dropping FLRW expansion terms.

## Matter normalization

The baryon perturbation source used by R3 is frozen as

```text
S_b(a,x) = (3/2) (100/c)^2 omega_b a^-3 delta_b(a,x)
```

in `Mpc^-2`, equivalently `4 pi G_N delta rho_b/c^2` in the repository convention.

D2B must show algebraically that the time-dependent matter source entering the coupled AeST constraint/evolution equations uses this same normalization. `d_b` may not be rescaled to make a coupled equation pass.

The D2A velocity divergence `t_b` must enter through the action-derived matter momentum/continuity structure. It may not be used merely as an empirical correction to constraint drift.

## Prohibited shortcuts

D2B fails or is classified incomplete if the implementation requires any of the following without derivation from the covariant/3+1 theory:

- adding `3H`, `2H`, or any other Hubble-friction term by analogy;
- promoting the fixed-source D1A equation `dot(P_alpha)=0` to a guessed time-dependent source law;
- differentiating the Hamiltonian constraint and treating the resulting identity as an independent matter-coupling equation unless equivalence to the pre-gauge-fixing momentum equation is demonstrated;
- inserting CLASS `d_b(t)` directly into the static R3 residual at every time and calling that dynamical evolution;
- using Newton, pseudo-time, source homotopy, arclength, or constitutive homotopy as physical time;
- initializing from a favorable R3 static root;
- tuning friction/damping to force settling;
- changing the frozen full-J interpolation functions or physical parameters.

## B1 — FLRW longitudinal derivation

Starting from the same AeST covariant/3+1 action underlying D1A, derive the scalar-longitudinal weak-field equations on the frozen spatially flat FLRW background while retaining the nonlinear spatial `J(Y)` term.

The derivation must identify:

- the metric scalar variables and gauge;
- the longitudinal aether/scalar variables;
- the nondynamical lapse/shift constraints;
- the canonical momenta or equivalent first-order state;
- the matter density and momentum source terms;
- every factor of `a`, `H`, or conformal Hubble rate `mathcal H`;
- the exact mapping to repository `Phi`, `tildePhi`, `chi` in the fixed-a weak-field limit.

Every time-dependent coefficient must be traceable to the action or an exact change of time/variables.

## B2 — D1A zero-expansion regression

Taking

```text
a -> constant
H -> 0
```

with a time-independent dust source must recover the already certified D1A equations and canonical relations.

Frozen numerical/algebraic gate:

```text
max normalized discrepancy <= 1e-12.
```

## B3 — exact fixed-a quasistatic full-J regression

Setting all physical time derivatives to zero at an arbitrary fixed scale factor must reproduce the R3 equations exactly:

```text
Phi = tildePhi + chi
lap_phys(tildePhi) + mu^2 Phi = 4 pi G_N rho_b/(1+beta0)
lap_phys(tildePhi) = div_phys[j(x) grad_phys chi]
```

with

```text
x = c^2 |grad_phys chi|/(a0 Mpc_in_metres).
```

Required manufactured-state discrepancy:

```text
<= 1e-12.
```

This gate is intentionally redundant with D1D but now tests the FLRW-derived system after all scale-factor factors are included.

## B4 — linear cosmological regression against frozen CLASS AeST

Linearize the derived FLRW system about the exact frozen homogeneous AeST background and remove the nonlinear finite-gradient terms in the appropriate small-amplitude limit.

For the six frozen modes

```text
{0.03,0.05,0.08,0.10,0.15,0.20} h/Mpc
```

compare the derived linear evolution/constraint residuals with the same CLASS model used to create the retained v0.77 trace and D2A matter block.

Primary fields available for cross-checking are

```text
a(tau), H(tau), chi(tau), Q(tau), phi(tau), psi(tau), d_b(tau), t_b(tau).
```

The exact regression statistic must be frozen in the implementation before the first D2B residual is inspected. The target tolerance is

```text
max normalized equation residual <= 2e-3
```

for finite-difference/interpolation residuals on the common dense history, with an independent native/dense closure target

```text
<= 2e-4.
```

A tighter result is reported but the preregistered gates are not changed after output.

## B5 — matter continuity/momentum consistency

The coupled gravitational constraints and matter equations must imply the D2A Newtonian-gauge baryon continuity relation

```text
delta_b' + theta_b - 3 phi' = 0
```

without an empirical constraint projection.

The matter momentum term sourcing the gravitational longitudinal system must be shown to be the same `theta_b`/momentum convention exported by CLASS. A sign or factor-of-a ambiguity is a FAIL/INCOMPLETE result, not a tunable convention after output.

## B6 — constraint propagation

Construct deterministic linear initial data from the frozen CLASS trajectory. The retained gravitational constraints must propagate over `0.2 <= z <= 6` with maximum normalized residual

```text
<= 2e-3
```

using no empirical post-step projection. Exact algebraic solution of nondynamical constraints is allowed.

## B7 — no artificial branch selection

D2B may validate the coupled time-dependent equations but must not yet use full nonlinear source amplitude to decide which R3 branch is physically selected.

No D2B output may be interpreted as memory survival, a finite-eta effect, or an observational result.

## Frozen classifications

All B1-B7 requirements close without a new physical function or fitted coefficient:

```text
NL1C6D2B_FLRW_SOURCE_GRAVITY_COUPLING_AUDIT_PASS
```

The derived equations contradict a frozen identity or regression gate:

```text
NL1C6D2B_FLRW_SOURCE_GRAVITY_COUPLING_AUDIT_FAIL
```

The covariant theory remains viable but a required FLRW longitudinal reduction, momentum-source mapping, or CLASS variable mapping cannot be established without an additional theory choice:

```text
NL1C6D2B_FLRW_SOURCE_GRAVITY_COUPLING_AUDIT_INCOMPLETE
```

## Continuation rule

Only a D2B PASS permits preregistration of the nonlinear physical branch-evolution run. That subsequent run must freeze initial data, time stepping, constraint handling, sharp-kink treatment, resolution controls, and branch/settling classifications before inspecting the nonlinear trajectory.

NL1C7 causal-memory response remains blocked until the nonlinear full-J evolution itself passes its own preregistered gates.
