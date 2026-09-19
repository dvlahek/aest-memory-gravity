# NL1C7B6 — pre-data symbolic radial-reduction audit

## Status

Pre-data / pre-implementation preregistration.

NL1C7B6 is a new project-level analytic-representation track.

It is not B5a/B5b and it does not reopen either the Repair19c finite-difference Gauss-Newton sequence or the B5 conservative solver sequence.

Parent terminal B5 result:

`NL1C7B5_CONSERVATIVE_DIFFERENTIAL_CERTIFICATION_FAIL`.

Parent B5 Repair01 result-freeze commit:

`2a2739db609ffb58e899baa7308199fd8dbc528b`.

Parent result JSON SHA-256:

`bfeae8019b69f23e0fa659c6c3e0134353b85e0dcd67f0337c14d6f50b887c8d`.

Current history/README state records that no B5 solver-parameter follow-up is licensed.

## Purpose

The previous two-field construction attempts treated the exact Hamiltonian and radial-momentum constraints as large nonlinear residual systems.

NL1C7B6 asks a different question before any new numerical solve:

**Do the frozen action-derived spherical constraints admit an exact analytic reduction to a coupled first-order radial system for the same physical pair `(L,R_t)`?**

The audit is structural.

It does not integrate the reduced equations.

It does not construct a corrected state.

It does not run time evolution.

It does not change the physical ansatz.

## Frozen physics

Unchanged:

- eta=0;
- Simple source branch;
- beta=1;
- density-Q-completed state representation;
- same AeST coefficients and signs;
- same exact Q reconstruction;
- same matter/scalar/aether fields;
- same frozen areal-radius field `R(r)`;
- same frozen `L_t(r)`;
- only `L(r)` and `R_t(r)` remain candidate initial-data functions;
- historical exact differential certification threshold remains `1e-7`.

No additional physical field is introduced.

## Exact-Q substitution

The frozen exact-Q reconstruction is

`Q = cosh(u) p_t + sinh(u) phi_r/L`.

The Q target is frozen by the density-Q-completed state.

Therefore use exactly

`p_t = [Q_target - sinh(u) phi_r/L]/cosh(u)`.

Under this substitution define

`E = cosh(u) u_t + sinh(u)(L_t+u_r)/L`

and

`X = tanh(u) Q_target + phi_r/[cosh(u)L]`.

This substitution is an algebraic identity of the already frozen state representation, not a new approximation.

## Frozen action source dictionary

Reconstruct exactly the existing symbolic B4/Repair01 action terms:

- GR_kin;
- GR_curv_NL;
- GR_curv_Rr;
- GR_Nr_boundary;
- AeST_E2;
- AeST_EX;
- AeST_X2;

plus the already frozen j/J, K-sector, dust and background contributions.

The audit must derive structure from these existing expressions.

No equation may be inferred from the numerical residual alone.

## Structural target H

Write the continuous Hamiltonian constraint as

`H = S_H - d_r F_H = 0`.

The audit must verify symbolically that, after the exact-Q substitution:

1. `F_H` is independent of `L_r`, `R_t` and `R_{t,r}`;
2. all local Hamiltonian source terms are independent of `L_r` and `R_{t,r}`;
3. the only `R_t` dependence is the GR kinetic polynomial
   `2 L R_t^2 + 4 L_t R R_t`;
4. therefore the full continuous H constraint is exactly affine in `L_r`, quadratic in `R_t`, and independent of `R_{t,r}`.

The frozen Hamiltonian radial flux must reduce to

`F_H = 4 R R_r/L + 2 K_B R^2 cosh(u) E + 2 C R^2 cosh(u) X`.

The coefficient multiplying `L_r` in `H` must be verified exactly as

`A_H = [4 R R_r + 2 K_B R^2 cosh(u)sinh(u)(L_t+u_r) + 2 C R^2 phi_r]/L^2`.

Thus, away from coefficient zeros,

`L_r = -B_H/A_H`

where

`B_H = H evaluated at L_r=0`.

No quadratic branch choice is involved in this reduction because H is solved for `L_r`, not for `R_t`.

## Structural target M

Write the continuous radial-momentum constraint as

`M = S_M - d_r F_M = 0`.

The GR kinetic contribution must be verified exactly:

`S_M^GR = 4(L R_r R_t + L_r R R_t + L_t R R_r)`

and

`F_M^GR = 4 L R R_t`.

Therefore

`M_GR = 4 R L_t R_r - 4 L R R_{t,r}`.

The audit must verify symbolically that every non-GR frozen momentum term is independent of `R_t`.

Therefore the full continuous momentum constraint must be exactly affine in `R_{t,r}`, independent of algebraic `R_t`, and at most affine in `L_r`:

`M = -4 L R R_{t,r} + B_M(L,L_r; frozen fields)=0`.

Thus, away from the analytic center,

`R_{t,r}=B_M/(4 L R)`.

After substituting the Hamiltonian reduction for `L_r`, the constraints define a coupled first-order radial system for `(L,R_t)`.

## No hidden higher derivatives of solved fields

The audit must verify that:

- H contains no `L_{rr}`;
- H contains no `R_{t,r}`;
- M contains no `L_{rr}`;
- M contains no `R_{t,rr}`.

Derivatives of frozen fields such as `R_{rr}`, `u_{rr}`, `u_{t,r}`, `phi_{rr}` or `L_{t,r}` may appear and are allowed because those fields are not solved in NL1C7B6.

## Frozen parent coefficient audit

Use exactly the six lambda=1 canonical parent states:

- scales 5,10,20 h^-1 Mpc;
- Nr=256,512.

For every noncenter radial point compute:

- `A_H`;
- `A_M = 4 L R`.

Require:

1. both arrays finite;
2. no exact zero at any noncenter point;
3. constant sign separately for `A_H` and `A_M` on each case;
4. relative nondegeneracy
   `min(abs(A))/max(abs(A)) >= 1e-8`
   for each coefficient and each case.

The analytic center `r=0` is excluded only from this division test because `R(0)=0` makes both radial-system coefficients vanish there by regular spherical geometry.

No other radial point may be excluded.

## Center structure reporting

For each case report on the first eight noncenter nodes:

- `A_H/r`;
- `A_M/r`;
- minimum and maximum finite values;
- sign.

This is descriptive.

No center value is fitted.

No extrapolated boundary datum is introduced.

The purpose is to confirm that the coefficient degeneracy is the expected regular-center `O(r)` structure rather than an additional interior singularity.

## Boundary/gauge accounting

Repair18d1 certified

- `Y4=0`;
- `Qmean=0`

as deterministic transversality functionals for the two-dimensional null space of the discrete projection Jacobian.

NL1C7B6 must not silently reinterpret those functionals as physical radial boundary conditions.

The symbolic audit therefore only records the reduced-system order:

- two first-order unknown functions;
- two integration constants.

It also records the already existing physical boundary information:

- regular spherical center implies `R_t(0)=0`;
- the project evolution preregistration requires a regular asymptotic-background outer boundary.

The exact numerical boundary policy for a future reduced radial construction is **not** chosen in this audit.

A separate preregistration is required before any BVP/shooting/integration execution.

That preregistration must explicitly state how physical boundary conditions relate to or supersede the historical projection-only `Y4/Qmean` functionals.

## Gates

### B6_G1 — frozen provenance

Require exact B5 Repair01 frozen ancestry and exact imported source-code blobs.

### B6_G2 — exact-Q structural identities

Require symbolic equality of the frozen Q substitution and the stated reduced `E` and `X` forms.

### B6_G3 — Hamiltonian reduction identity

Require all Hamiltonian structural statements and the exact `A_H` formula to pass symbolically.

### B6_G4 — momentum reduction identity

Require exact GR cancellation and independence of all non-GR momentum terms from algebraic `R_t`.

Require the full coefficient of `R_{t,r}` to be exactly `-4LR`.

### B6_G5 — derivative order

Require no hidden second derivative of either solved field.

### B6_G6 — six-case coefficient nondegeneracy

Require the frozen parent coefficient audit to pass on all six cases under the fixed `1e-8` relative-nondegeneracy rule.

### B6_G7 — boundary/gauge claim boundary

Require that the audit makes no numerical boundary choice, no corrected-state construction and no evolution claim.

## Terminal classifications

Implementation/provenance failure:

`NL1C7B6_SYMBOLIC_REDUCTION_IMPLEMENTATION_FAIL`.

Symbolic structural failure:

`NL1C7B6_SYMBOLIC_RADIAL_REDUCTION_FAIL`.

Exact reduction holds but a parent coefficient is interior-degenerate under the frozen criterion:

`NL1C7B6_RADIAL_REDUCTION_COEFFICIENT_DEGENERACY`.

Full audit PASS:

`NL1C7B6_SYMBOLIC_RADIAL_REDUCTION_PASS`.

## Licensed continuation

Only

`NL1C7B6_SYMBOLIC_RADIAL_REDUCTION_PASS`

licenses a separately preregistered numerical construction of the reduced first-order radial system.

A PASS does not itself certify initial data.

A future construction must still be judged by the unchanged original B4 differential

`max epsilon_H <=1e-7`

and

`max epsilon_M <=1e-7`

on both Nr=256 and Nr=512.

No evolution or finite-eta claim is licensed by this audit alone.
