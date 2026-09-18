# NL1C7B4 Repair18b — implementation lock

## Status

Locked after Repair18b implementation and before any Repair18b execution.

Repair18b is diagnostic only.

## Frozen parent results

Repair18a result freeze:

- commit:
  `8cfce926a9075d77dd73c5bb5242c9d3e26b74ad`
- file:
  `docs/nl1c7b4_repair18a_result_freeze.md`
- blob:
  `21f12cdf27abc560812dabb1c6b1a3b9e41e14f5`
- Repair18a JSON SHA-256:
  `29a81013b42ebe22989ca1a00b48bb2bb33447677bb77db6aefee298c7159782`.

Repair18 and Repair18a remain FAIL and cannot be relabelled.

## Preregistration

- commit:
  `ff79eb82b14ff2c86a2d02c3b05fc60937a7801d`
- file:
  `docs/nl1c7b4_repair18b_predata_jacobian_fidelity_diagnostic.md`
- blob:
  `24e23e90c930895c9ff4da44e7a3a8c6efa98e70`.

## Implementation

Final pre-run evaluator:

- implementation commit:
  `bca4eabea8c8e1a0e6e8a88999567776096b5c3b`
- file:
  `nl1c7b/initial_constraint_certification_repair18b.py`
- blob:
  `9beb762d33d4026a446a1a19363e79087b5a6525`.

The post-implementation edit before this lock only replaced non-finite JSON sentinels by serializable `null` values. No diagnostic formula, threshold, domain, or classification logic changed.

## Frozen domain

- eta = 0
- canonical Y = Simple
- beta = 1
- lambda = 1
- Nr = 256
- scales = 5, 10, 20 h^-1 Mpc
- projection pair = `(L,R_t)`
- solver coordinates = `(y_L,q_Rt)`
- all non-projection fields frozen.

## Frozen Jacobian comparison

At x=0 compare:

1. dense/unstructured SciPy `2-point` numerical Jacobian;
2. sparse/grouped SciPy `2-point` numerical Jacobian using the frozen Repair18a half-band-16 pattern.

Both use the same SciPy default relative-step rule.

Frozen structure-match threshold:

`||J_sparse-J_dense||_F / ||J_dense||_F <= 1e-6`.

The threshold is diagnostic only and does not modify any historical physics gate.

## Frozen local-rank diagnostic

For the dense Jacobian report:

- largest singular value;
- smallest singular value;
- ratio;
- numerical rank with
  `tol=sigma_max*max(shape)*eps_float64`.

Full column rank is required only for the descriptive
`FULL_RANK_JACOBIAN_DIAGNOSTIC_PASS` outcome.

## Frozen linearized feasibility probe

For every scale solve

`min ||F(0)+J_dense dx||_2`

with SciPy `lsq_linear`:

- method = trf
- tol = 1e-12
- max_iter = 500
- bounds = [-0.5,0.5] on every solver coordinate.

Evaluate the exact nonlinear residual for all preregistered amplitudes

`alpha={1,1/2,1/4,1/8}`.

No alpha may be selected after the run.

## Frozen imported blobs

- Repair18a evaluator:
  `767199e8ab620f5d6dabd50d0efde9828f22048b`
- Repair16 evaluator:
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

## Frozen input hashes

Repair15a JSON:
`596c7b13c4683840bcf40f6850356e179e77f873c3a3b42ba0b54730ae80811d`

Repair15a NPZ:
`997d0033eeed1f3e60c1907c7938a0ea87a1cf38de6ab860340bd003d18d6e6e`

Repair16 JSON:
`a225f435ef61eaf33a1b4466eea678b23d1a221a537589bd8e2b0717ed66335b`

Repair17 JSON:
`09750aeb9fdce7bbbbe148c8478b9af5067a72ab20a1e48171f5a9e3a1d4b82e`

Repair18 JSON:
`8f8b6ce1316bd5cad3442ebd0cba692e4d4c82060685da083517b990cac36922`

Repair18a JSON:
`29a81013b42ebe22989ca1a00b48bb2bb33447677bb77db6aefee298c7159782`

## Terminal classes

- `NL1C7B4_REPAIR18B_SPARSE_JACOBIAN_STRUCTURE_MISMATCH`
- `NL1C7B4_REPAIR18B_LOCAL_PROJECTION_RANK_DEFICIENCY`
- `NL1C7B4_REPAIR18B_FULL_RANK_JACOBIAN_DIAGNOSTIC_PASS`
- `NL1C7B4_REPAIR18B_IMPLEMENTATION_FAIL`.

No diagnostic threshold, Jacobian method, field set, scale, grid, alpha, or parent artifact may change after the first Repair18b execution.
