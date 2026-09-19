# NL1C7B4 Repair19b1 — implementation lock

## Status

Locked after implementation and before any Repair19b1 execution.

Repair19b1 is a diagnostic certification repair only.

## Frozen Repair19b parent

- result-freeze commit:
  `cdc50f56d31f8a0007a80fe7fcaee98e687fe867`
- result-freeze blob:
  `49d50f2aa9f63484525d79729221e2389f3dacd6`
- Repair19b JSON SHA-256:
  `d177394b45e19ac2bca739d4ff256694c5df65e9331276e3c1b1466f4fbe5929`
- classification:
  `NL1C7B4_REPAIR19B_IMPLEMENTATION_FAIL`.

## Preregistration

- commit:
  `520f25bc3d8a71a96872b54fad669d8d72f88539`
- file:
  `docs/nl1c7b4_repair19b1_predata_orthonormal_direct_linear_feasibility.md`
- blob:
  `c20e87c3787d640a18262ba269b4fd957be130b4`.

## Implementation

- commit:
  `d5d23f7444a9e7df47fc056620be0e0d0541b396`
- file:
  `nl1c7b/initial_constraint_certification_repair19b1.py`
- blob:
  `11a14221a4d6d5d639781134b5e55233f863b799`.

## Frozen question

Only the preregistered orthonormal Y4=0/Qmean=0 representation is used for the science gate.

The chain basis is retained only as a conditioning control.

Repair19b1 tests residual-space linear feasibility and direct-vs-LSMR convergence, not physical correction-vector uniqueness.

## Frozen domain

Exactly:

- eta=0
- Y=Simple
- beta=1
- lambda=1
- scales=5,10,20 h^-1 Mpc
- Nr=256,512.

Total canonical cases: 6.

## Frozen Jacobian and bases

- same Repair19a/Repair19b parent state construction;
- same normalized residual;
- same Repair18a grouped two-point Jacobian;
- same Helmert orthonormal basis;
- no field added;
- no row or column removed.

## Frozen direct solvers

Both:

- SciPy LAPACK GELSD
- SciPy LAPACK GELSY

with

`cond=max(J_orth.shape)*eps_float64`.

Returned numerical rank is descriptive only.

## Frozen science gates

For all 12 direct orth solves:

- finite;
- relative residual <= `1e-6`;
- |Y4| <= `1e-12`;
- |Qmean| <= `1e-12`.

For all 12 direct-vs-frozen-LSMR comparisons:

- LSMR/direct relative-residual ratio >= `1e3`.

The full frozen Repair19b orth payload must reproduce to abs-or-rel `1e-12`.

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
  `b9b79d1fe12dff7b59d80260572129b746322412bf96ff214204f9651bd77761`
- Repair19b:
  `d177394b45e19ac2bca739d4ff256694c5df65e9331276e3c1b1466f4fbe5929`.

## Terminal classifications

- `NL1C7B4_REPAIR19B1_ORTHONORMAL_DIRECT_LINEAR_FEASIBILITY_LSMR_STAGNATION_PASS`
- `NL1C7B4_REPAIR19B1_ORTHONORMAL_DIRECT_LINEAR_INFEASIBILITY`
- `NL1C7B4_REPAIR19B1_LSMR_STAGNATION_NOT_ESTABLISHED`
- `NL1C7B4_REPAIR19B1_IMPLEMENTATION_FAIL`.

No solver, basis, threshold, parent, field, source, coefficient, sign, eta, branch, radial point set, or classification rule may change after the first Repair19b1 execution.
