# NL1C7B4 Repair19 — implementation lock

## Status

Locked after implementation and before any Repair19 execution.

Repair19 is the first gauge-fixed exact nonlinear closure test after the independently certified Repair18d1 transversality result.

## Frozen Repair18d1 parent

- result-freeze commit:
  `814450553dc9680f13f329cb6e578350498163aa`
- result-freeze blob:
  `a72bd095fbb2f66bb3e398a379f847634aace3b4`
- Repair18d1 JSON SHA-256:
  `21d5be34660f0054bd8550908f300de64ec1ec9e8f81e0f150c7c1540e3bf04c`
- classification:
  `NL1C7B4_REPAIR18D1_NULLSPACE_TRANSVERSALITY_AUDIT_PASS`
- certified selected pair:
  `Y4+Qmean`.

## Preregistration

- commit:
  `167eb24812d539dd273e6a5185d11c6402477940`
- file:
  `docs/nl1c7b4_repair19_predata_gauge_fixed_exact_nonlinear_constraint_closure.md`
- blob:
  `f9c3ccfc78c671d9459bad56b466c5f04d839f2c`.

## Implementation

- commit:
  `9a7b5eb21f54603e157098e9dc62abbb5ea1ad03`
- file:
  `nl1c7b/initial_constraint_certification_repair19.py`
- blob:
  `2532094b518dfc2990fa0d77d8123d793b0107b3`.

## Exact reduced parametrization

The full correction vector is

`x=[y_L,q_Rt]`.

Repair19 solves in a fixed sparse reduced basis

`x=Bz`

with two coordinates removed exactly.

The basis enforces, to floating-point roundoff:

- `Y4=0`
- `Qmean=0`.

No gauge penalty residual is used.

The y_L constrained block uses the local chain basis on the first four non-center nodes.

The q_Rt constrained block uses the path-incidence/first-difference basis whose vectors have exactly zero global sum.

## Frozen nonlinear solver

- SciPy `least_squares`
- method `trf`
- finite difference `2-point`
- reduced sparse Jacobian structure obtained from the frozen Repair18a full sparsity pattern and the fixed basis B
- zero initial reduced coordinates
- `x_scale='jac'`
- `ftol=1e-12`
- `xtol=1e-12`
- `gtol=1e-12`
- `max_nfev=400`
- no multistart
- no lambda continuation
- no branch-specific state solve.

No explicit optimizer bounds are applied in reduced coordinates.

Every final full coordinate must satisfy the hard safety gate

- `max |y_L| <= 0.5`
- `max |q_Rt| <= 0.5`.

## Frozen science domain

Canonical solve:

- eta=0
- Y=Simple
- beta=1
- lambda=1,1/2,1/4,1/8
- scales=5,10,20 h^-1 Mpc
- Nr=256,512
- total canonical solves=24.

All-branch lambda=1 retest:

- Y=Simple,Exponential,Sharp
- beta=1,0.5,0.1
- scales=5,10,20
- Nr=256,512
- total exact historical cases=54.

Historical exact nonlinear threshold remains:

`max epsilon_H <= 1e-7`

and

`max epsilon_M <= 1e-7`.

## Frozen state-output rule

The official output

`results/nl1c7b4_repair19_gauge_fixed_exact_nonlinear_states.npz`

may be written only if all pre-output science/implementation gates pass, including all 54 historical branch cases.

If any pre-output science gate fails, the official NPZ must not exist.

## Frozen imported evaluator blobs

- Repair18a exact nonlinear source evaluator:
  `767199e8ab620f5d6dabd50d0efde9828f22048b`
- Repair16 parent-state construction/reproduction:
  `fbd7d24f748fc398638d4eea4b7707801161e52a`
- Repair01 source dictionary:
  `253a0ae2a19a597f06358704ea276c9005973af3`
- Repair09 exact helpers:
  `0cd67cecfbd590cb8819ad37314dc5b49047bc93`
- base B4:
  `8559120dc273be3174eca130ca313ed6ff5acb25`
- Repair08:
  `94fb3f42a7c819b0525860f7344d5dbaff93da19`
- C7A reconstruction:
  `ff383c1ddc2cb2a684e2b5dd11fde0ae811e4fac`.

## Frozen parent result hashes

- Repair15a:
  `596c7b13c4683840bcf40f6850356e179e77f873c3a3b42ba0b54730ae80811d`
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
  `21d5be34660f0054bd8550908f300de64ec1ec9e8f81e0f150c7c1540e3bf04c`.

## Terminal classifications

- `NL1C7B4_REPAIR19_GAUGE_FIXED_EXACT_NONLINEAR_CONSTRAINT_PASS`
- `NL1C7B4_REPAIR19_GAUGE_FIXED_EXACT_NONLINEAR_CONSTRAINT_FAIL`
- `NL1C7B4_REPAIR19_IMPLEMENTATION_FAIL`.

No solver tolerance, basis, candidate condition, branch, field, threshold, source, coefficient, sign, point set, eta value, or output rule may change after the first Repair19 execution.
