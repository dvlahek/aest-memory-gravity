# NL1C7B6 — symbolic radial-reduction result freeze

## Status

Frozen first locked NL1C7B6 execution.

Terminal classification:

`NL1C7B6_SYMBOLIC_RADIAL_REDUCTION_PASS`.

Science return code:

`SCIENCE_RC=0`.

Execution HEAD:

`64c3324841015f45c79abc8680cb63cef15f7316`.

The run began with:

`NL1C7B6_SYMBOLIC_RADIAL_REDUCTION_LOCK_PASS`.

This is a structural analytic PASS. It licenses a separately preregistered numerical construction of the reduced radial system. It does not itself certify initial data or license evolution.

## Frozen output hashes

Result JSON:

- bytes: `15425`
- SHA-256:
  `ed1efdac5dee72d8c57cbda23d074213babd15fdf3bc7adc18e61789f862e635`.

Evaluator log:

- bytes: `15871`
- SHA-256:
  `c02cbca48db44b9807852eef7b98404d07b148b64b2dbf9011cd5984cf140592`.

Full runner log:

- bytes: `21616`
- SHA-256:
  `52cdce4a0847cae3fd7f4cfc10ecfe1603016285f91664af59384674bd1c2101`.

No corrected-state NPZ was constructed by this audit.

## Gate result

All seven gates PASS:

- B6_G1 frozen provenance;
- B6_G2 exact-Q structural identities;
- B6_G3 Hamiltonian reduction identity;
- B6_G4 momentum reduction identity;
- B6_G5 derivative order;
- B6_G6 six-case coefficient nondegeneracy;
- B6_G7 boundary/gauge claim boundary.

Parent H/M reproduction is exact in all six canonical cases.

## Exact structural result

After the frozen exact-Q substitution

`p_t=[Q_target-sinh(u) phi_r/L]/cosh(u)`,

the frozen aether variables reduce to

`E=cosh(u)u_t+sinh(u)(L_t+u_r)/L`

and

`X=tanh(u)Q_target+phi_r/[cosh(u)L]`.

The Hamiltonian radial flux is exactly

`F_H=4 R R_r/L + 2 K_B R^2 cosh(u) E + 2 C R^2 cosh(u) X`.

The Hamiltonian constraint is:

- affine in `L_r`;
- quadratic in algebraic `R_t`;
- independent of `R_{t,r}`;
- free of second derivatives of solved fields.

Its solved-field derivative coefficient is

`A_H=[4 R R_r + 2 K_B R^2 cosh(u)sinh(u)(L_t+u_r) + 2 C R^2 phi_r]/L^2`.

Thus, away from the regular center,

`L_r=-B_H/A_H`.

The GR radial-momentum terms satisfy exactly

`S_M^GR=4(L R_r R_t + L_r R R_t + L_t R R_r)`

and

`F_M^GR=4 L R R_t`.

Their exact combination is

`M_GR=4 R L_t R_r - 4 L R R_{t,r}`.

All non-GR frozen momentum sectors are independent of algebraic `R_t`.

Therefore the full momentum constraint is affine in `R_{t,r}` with coefficient

`-4 L R`

and, after substituting the Hamiltonian expression for `L_r`,

`R_{t,r}=B_M/(4LR)`.

Hence the exact frozen H/M constraints define a coupled first-order radial system for the same physical pair `(L,R_t)`.

## Six-case coefficient audit

All six lambda=1 canonical parent cases pass the frozen nondegeneracy test.

For every noncenter point:

- `A_H` is finite;
- `A_H` is strictly positive;
- `A_H` has no interior zero;
- `4LR` is finite;
- `4LR` is strictly positive;
- `4LR` has no interior zero.

The minimum-to-maximum absolute coefficient ratios are approximately:

- Nr=256: `3.92157e-3`;
- Nr=512: `1.95695e-3`;

for both coefficient families, far above the frozen `1e-8` threshold.

## Regular-center structure

The first eight noncenter nodes show the expected regular spherical scaling.

Across all scales and both resolutions:

`A_H/r ≈ 4`

to approximately parts in `1e-6` or better.

Similarly,

`A_M/r = (4LR)/r ≈ 1.6000e-3`.

Thus both coefficients vanish linearly at the analytic center, with finite nonzero ratios to `r`.

There is no detected additional interior singularity or sign change.

This strongly supports treating the center by analytic regularity rather than by coefficient division at `r=0`.

## Boundary/gauge accounting

The reduced system contains:

- two first-order unknown functions: `L(r)` and `R_t(r)`;
- two integration constants.

The audit records:

- regular-center condition `R_t(0)=0`;
- existing project requirement of a regular asymptotic-background outer boundary.

It intentionally does not choose the numerical boundary policy.

The historical `Y4=0` and `Qmean=0` conditions remain Repair18d1 projection-nullspace transversality functionals. They are not reinterpreted as physical radial boundary conditions.

A separate preregistration is required before any radial integration, shooting or BVP solve.

## Scientific interpretation

This PASS changes the numerical problem qualitatively.

The exact constraint system does not need to be posed as a large nonlinear least-squares minimization over all radial nodes.

It admits an exact first-order radial reduction for the same frozen two-field physical ansatz.

The previous Repair19c and B5 failures therefore do not imply that the two-field ansatz lacks an exact solution. They show that two residual-minimization constructions failed to find one.

NL1C7B6 provides a mathematically cleaner route: solve the constraint equations as radial differential equations.

## Licensed continuation

A separately preregistered reduced-radial numerical construction is now licensed.

That construction must:

- preserve the same frozen physics;
- keep only `(L,R_t)` adjustable;
- impose a physically explicit regular-center/asymptotic-background boundary policy before execution;
- use the exact reduced first-order equations, not a residual-minimization surrogate;
- retain the original B4 differential evaluator as the final independent certification;
- require
  `max epsilon_H <= 1e-7`
  and
  `max epsilon_M <= 1e-7`
  on Nr=256 and Nr=512;
- write a corrected-state NPZ only on full certification.

Eta=0 short-time evolution remains unlicensed until that independent differential certification passes.
