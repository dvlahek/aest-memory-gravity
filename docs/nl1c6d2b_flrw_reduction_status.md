# NL1C6D2B nonlinear FLRW reduction status

This note records the derivation boundary used by the preregistered
`NL1C6D2B_FLRW_SOURCE_GRAVITY_COUPLING_AUDIT`.

## Established before D2B

The repository has already certified the following ingredients.

1. `NL1C6D1A_LONGITUDINAL_WEAKFIELD_REDUCTION_AUDIT_PASS` establishes the
   1D longitudinal weak-field canonical relations, the exact inactivity of the
   transverse curl sector in the repository geometry, the full-J static
   reduction, and the published Minkowski tracking-mode dispersion.

2. `NL1C6D1B_LINEAR_SCALAR_MODE_REGRESSION_PASS` independently verifies the
   propagating scalar-mode dispersion numerically.

3. `NL1C6D1CDE_CONSTRAINT_QS_REGRESSION_PASS` verifies the linear constraints,
   the fixed-a quasistatic full-J identity, and the high-gradient regression.

4. `NL1C6D2A_BARYON_MATTER_SECTOR_AUDIT_PASS` establishes the frozen CLASS
   baryon density/velocity history and the Newtonian-gauge continuity
   convention
   `delta_b' + theta_b - 3 phi' = 0`.

5. The frozen CLASS AeST bridge evolves the homogeneous Exp background and the
   linear Newtonian-gauge AeST perturbation state. Its effective dark component
   contributes to the same CLASS stress-energy sums used by the metric
   constraints.

## Exact CLASS conventions retained in D2B

For the frozen Newtonian-gauge implementation,

```text
metric_continuity = -3 phi'
metric_euler      = k^2 psi
```

and the metric constraints are

```text
phi' = -Hconf psi + (3/2) a^2/k^2 sum_s[(rho_s+p_s) theta_s]

psi  = phi - (9/2) a^2/k^2 sum_s[(rho_s+p_s) shear_s].
```

The AeST effective-dark component uses the frozen `delta_cdm`/`theta_cdm`
slots when `aest_enabled=yes`; this is a repository convention, not a new
D2B reinterpretation.

## Missing action-derived object

What is **not** yet established is an explicit scalar-longitudinal weak-field
FLRW reduction of the same AeST action that simultaneously retains

- the nonlinear spatial `J(Y)` sector used by R3/D1A;
- all FLRW scale-factor and conformal-Hubble coefficients;
- the nondynamical lapse/shift constraints;
- a canonical or equivalent first-order time-dependent state; and
- the matter density and momentum sources in those same reduced variables.

The frozen CLASS bridge is a linear FLRW implementation. D1A is a
nonlinear-spatial weak-field/Minkowski reduction whose zero-time-derivative
limit gives R3. Combining the temporal coefficients of the former with the
nonlinear `J(Y)` operator of the latter without deriving the combination from
the action would be a new theory choice.

Therefore D2B must not introduce, by analogy, terms such as `2 H chi'`,
`3 H chi'`, a guessed time-dependent `P_alpha` source law, or any damping
coefficient intended to select a static branch.

## D2B interpretation rule

The local D2B audit evaluates every frozen identity and CLASS convention that
can be checked independently. A contradiction is a D2B `FAIL`.

If those checks pass but the nonlinear FLRW reduction above remains absent,
the correct preregistered classification is

```text
NL1C6D2B_FLRW_SOURCE_GRAVITY_COUPLING_AUDIT_INCOMPLETE
```

This means that the covariant theory has not been rejected. It means only that
the bridge required to define the nonlinear cosmological branch-evolution
experiment has not yet been derived without an additional theory choice.

A D2B `INCOMPLETE` does not permit D2 nonlinear branch evolution and does not
permit NL1C7 causal-memory science runs.
