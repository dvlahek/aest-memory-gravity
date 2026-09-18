# NL1C7B4 Repair19a — pre-data gauge-fixed reduced-coordinate conditioning audit

## Status

Pre-data / pre-run diagnostic preregistration.

Repair19 is frozen as

`NL1C7B4_REPAIR19_GAUGE_FIXED_EXACT_NONLINEAR_CONSTRAINT_FAIL`

at result-freeze commit

`f42b238052d9db58f8eecf7098bd83c231863612`.

Frozen Repair19 result JSON:

- bytes: `67179`
- SHA-256:
  `ccf4a362f6a8a791f681d565881ff5728520752b1cbd93d72024b0919e1fe879`.

Repair19a is diagnostic only.

## Scientific question

Did Repair19 fail because the fixed chain reduced coordinates are numerically ill-conditioned for nonlinear least-squares, or does the same gauge-fixed physical subspace already fail at the linearized level?

Repair19a must not change the physical projection pair, the certified Y4/Qmean conditions, any source term, or the historical `1e-7` nonlinear threshold.

## Frozen domain

Use only the lambda=1 canonical cases:

- eta=0
- Y=Simple
- beta=1
- scales=5,10,20 h^-1 Mpc
- Nr=256,512.

Total cases: 6.

The parent state and exact residual are exactly those of Repair19 before projection.

## Two coordinate bases for the same constrained subspace

Let `m=Nr-1`.

### Frozen Repair19 chain basis

Use exactly the Repair19 basis:

- Y4 block: three first-difference columns over first four y_L nodes plus identity on nodes 5..m;
- Qmean block: path-incidence first-difference basis over q_Rt.

Denote this basis `B_chain`.

### Orthonormal Helmert basis

Construct `B_orth` spanning exactly the same subspace.

For the first four y_L coordinates use the three standard Helmert contrast columns, each normalized and mutually orthogonal. Nodes 5..m retain identity columns.

For q_Rt use the standard m-dimensional Helmert contrast basis with m-1 orthonormal mean-zero columns.

Thus require

- `B_orth^T B_orth = I`;
- `G B_orth = 0`;
- column count = `2m-2`.

No state solve is allowed in Repair19a.

## Basis-conditioning diagnostics

Report for both grids:

- analytic/spectral condition number of `B_chain`;
- condition number of `B_orth`;
- smallest and largest singular values of both bases.

For the path-incidence q block the chain singular values may be evaluated analytically as

`2 sin(k pi/(2m)), k=1,...,m-1`.

For the first-four y block use the exact numerical 4x3 singular values.

No conditioning threshold is used for terminal classification.

## Frozen full physical Jacobian

For each of the six lambda=1 cases define the full physical coordinate residual

`F(x)=[N_H/D_H^p,N_M/D_M^p]`

with x=(y_L,q_Rt), exactly as Repair18a/Repair19.

Compute the full sparse/grouped 2-point Jacobian at x=0 using the frozen Repair18a half-band-16 pattern.

No reduced-coordinate finite differences are used in this diagnostic.

Form

- `J_chain = J_x B_chain`
- `J_orth = J_x B_orth`.

Because the two bases span the same constrained physical subspace, the two reduced maps must represent the same physical linear correction space.

## Linearized least-squares probe

For each basis and each case solve

`min ||F0 + J_red dz||_2`

with SciPy `lsmr`:

- atol=1e-12
- btol=1e-12
- conlim=1e16
- maxiter=10000.

Transform to the physical correction

`dx=B dz`.

Report:

- initial residual L2;
- final linear residual L2;
- relative final residual;
- LSMR stop code and iterations;
- estimated condition number;
- `||dx||_2`;
- maximum |y_L| and |q_Rt|;
- physical difference between the chain and orth solutions after both are computed.

No nonlinear state is accepted or written.

## Exact nonlinear alpha probes

For the orthonormal-basis linearized physical correction only, evaluate the exact nonlinear residual at fixed amplitudes

`alpha={1,1/2,1/4,1/8}`.

Report exact moving-denominator:

- max epsilon_H
- max epsilon_M
- normalized residual L2.

These probes are descriptive only.

They test if a direction that solves the gauge-fixed linearized problem also reduces the exact nonlinear residual before a new nonlinear solver is attempted.

## Gates

### R19A_G1 — exact frozen provenance

Require exact frozen Repair19 hash/classification/gates and all frozen Repair19 parents.

Repair19 itself must remain science FAIL.

### R19A_G2 — exact same constrained subspace

For both grids require:

- chain and orth bases have shape `(2m,2m-2)`;
- both have full column rank analytically;
- `||G B_chain||_F <=1e-12`;
- `||G B_orth||_F <=1e-12`;
- `||B_orth^T B_orth-I||_F <=1e-12`.

### R19A_G3 — exact parent reproduction

For all six cases reproduce Repair19 lambda=1 parent H/M values to abs-or-rel `1e-12`.

### R19A_G4 — finite Jacobian and linear probes

Require all six full grouped Jacobians, both reduced maps, and both LSMR solutions finite.

### R19A_G5 — gauge-fixed linear feasibility

For both coordinate bases and all six cases require

`||F0+J_red dz||_2 / max(||F0||_2,tiny) <= 1e-6`.

This threshold tests linearized feasibility only.

It does not alter the historical nonlinear constraint threshold.

### R19A_G6 — physical-coordinate agreement

For every case require the chain and orth linearized physical corrections to agree to

`||dx_chain-dx_orth||_2 / max(||dx_chain||_2,||dx_orth||_2,tiny) <= 1e-5`.

This verifies that coordinate conditioning does not change the physical linear least-squares solution.

### R19A_G7 — complete nonlinear alpha probe

Require all 24 orth-basis exact nonlinear alpha probes finite with exact Q reconstruction error <=1e-12.

No H/M pass threshold is imposed on these probes.

### R19A_G8 — claim boundary

Repair19a must not:

- modify or write a state artifact;
- run nonlinear least-squares;
- add a physical field;
- change Y4/Qmean;
- change any source, coefficient, sign, eta, branch, radial point set, or historical threshold;
- remove a failed case;
- run time evolution;
- make an observational claim;
- relabel Repair19.

## Terminal classifications

If all eight gates pass:

`NL1C7B4_REPAIR19A_GAUGE_FIXED_LINEAR_CONDITIONING_CHARACTERIZED`.

Otherwise:

`NL1C7B4_REPAIR19A_IMPLEMENTATION_FAIL`.

## Interpretation boundary

Repair19a does not certify nonlinear closure.

If both bases solve the same gauge-fixed linear problem but the chain basis is substantially more ill-conditioned, a later preregistered nonlinear solver may switch coordinates while keeping exactly the same physical Y4/Qmean subspace.

If the gauge-fixed linear problem itself is not feasible, the next step must revisit the physical constraint-completion ansatz rather than the nonlinear optimizer.
