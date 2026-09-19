# NL1C7B4 Repair19b — implementation lock

## Status

Locked after implementation and before any Repair19b execution.

Repair19b is a direct linear diagnostic only.

## Frozen Repair19a parent

- result-freeze commit:
  `e8f6e93f17066cbfb2355dc64f5b36e91a06f527`
- result-freeze blob:
  `c448606fec79ad8cbf3b42b5853d60763fff4c94`
- Repair19a JSON SHA-256:
  `b9b79d1fe12dff7b59d80260572129b746322412bf96ff214204f9651bd77761`
- classification:
  `NL1C7B4_REPAIR19A_GAUGE_FIXED_LINEAR_INFEASIBILITY`.

## Preregistration

- commit:
  `b79ecb52840c304abb5b915766f23785db0c3adc`
- file:
  `docs/nl1c7b4_repair19b_predata_direct_reduced_linear_feasibility_audit.md`
- blob:
  `89f7656ad93939d2db6a926267700bb39f3ef4b3`.

## Implementation

- commit:
  `af80efab750c3fbd83bce47947fd5843c544cf0f`
- file:
  `nl1c7b/initial_constraint_certification_repair19b.py`
- blob:
  `862bb139ea9ff9f85907b0457119ad2916660278`.

## Frozen domain

Exactly six canonical lambda=1 cases:

- eta=0
- Y=Simple
- beta=1
- scale=5,10,20 h^-1 Mpc
- Nr=256,512.

## Frozen linear system

For each case:

1. reproduce the Repair19a parent state and normalized residual;
2. recompute the same grouped two-point full physical Jacobian with the frozen Repair18a half-band-16 sparsity pattern;
3. form the same two reduced matrices:
   - chain basis;
   - orthonormal Helmert basis;
4. densify only the reduced matrices;
5. solve by deterministic direct LAPACK least squares.

No nonlinear state is constructed.

## Frozen direct solvers

Primary:

- `scipy.linalg.lstsq`
- LAPACK `gelsd`
- `cond=max(shape)*eps_float64`.

Independent cross-check:

- `scipy.linalg.lstsq`
- LAPACK `gelsy`
- same cond.

## Frozen thresholds

- linear feasibility:
  `relative residual <=1e-6`
- chain-vs-orth physical correction:
  `<=1e-8`
- GELSD-vs-GELSY physical correction:
  `<=1e-8`
- exact gauge residual:
  `<=1e-12`
- frozen LSMR/direct residual ratio:
  `>=1e3`.

No historical nonlinear threshold is altered.

## Frozen parent hashes

- Repair15a JSON:
  `596c7b13c4683840bcf40f6850356e179e77f873c3a3b42ba0b54730ae80811d`
- Repair15a NPZ:
  `997d0033eeed1f3e60c1907c7938a0ea87a1cf38de6ab860340bd003d18d6e6e`
- Repair16:
  `a225f435ef61eaf33a1b4466eea678b23d1a221a537589bd8e2b0717ed66335b`
- Repair17:
  `09750aeb9fdce7bbbbe148c8478b9af5067a72ab20a1e48171f5a9e3a1d4b82e`
- Repair18:
  `8f8b6ce1316bd5cad3442ebd0cba692e4d4c82060685da083517b990cac36922`
- Repair18a:
  `29a81013b42ebe22989ca1a00b48bb2bb33447677bb77db6aefee298c7159782`
- Repair18b:
  `cbb68157c2408d8d52c180586db0b7d6f007c584d48c5ffc8c8d272b74a6c855`
- Repair18b1:
  `8e0d796e0368372d0b4cf75a075fba12ebde154b651d74929e745118c1ca6dab`
- Repair18c:
  `d49600f8b27536aeb0dca28d1d777d09439a376241c7f8f93b74e754c502e24b`
- Repair18d:
  `adc1410d50118c8080c1f84e5733cb09e5ff7d8f51a4937f1e306a96fe416def`
- Repair18d1:
  `21d5be34660f0054bd8550908f300de64ec1ec9e8f81e0f150c7c1540e3bf04c`
- Repair19:
  `ccf4a362f6a8a791f681d565881ff5728520752b1cbd93d72024b0919e1fe879`
- Repair19a:
  `b9b79d1fe12dff7b59d80260572129b746322412bf96ff214204f9651bd77761`.

## Terminal classes

- `NL1C7B4_REPAIR19B_LSMR_STAGNATION_IDENTIFIED`
- `NL1C7B4_REPAIR19B_DIRECT_LINEAR_INFEASIBILITY`
- `NL1C7B4_REPAIR19B_DIRECT_SOLVER_COORDINATE_DISAGREEMENT`
- `NL1C7B4_REPAIR19B_LSMR_STAGNATION_NOT_ESTABLISHED`
- `NL1C7B4_REPAIR19B_IMPLEMENTATION_FAIL`.

No basis, field, residual, Jacobian rule, solver driver, cutoff, threshold, source, coefficient, sign, eta, branch, radial point set, or historical artifact may change after the first Repair19b execution.
