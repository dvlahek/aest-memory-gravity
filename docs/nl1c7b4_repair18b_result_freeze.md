# NL1C7B4 Repair18b — local result freeze

## Status

Frozen local WSL result from the first locked Repair18b execution.

Terminal classification:

`NL1C7B4_REPAIR18B_IMPLEMENTATION_FAIL`.

Execution HEAD:

`dde76bf195bc59fdbebb472e565e4bc8ce724cda`.

This is a local WSL result, not an official GitHub Actions run.

## Frozen output hashes

- result JSON:
  - bytes: `15558`
  - SHA-256:
    `cbb68157c2408d8d52c180586db0b7d6f007c584d48c5ffc8c8d272b74a6c855`
- evaluator log:
  - bytes: `16004`
  - SHA-256:
    `124797d841336f348f94ab057aed381d8f7e978a247be43104d1068b9c00a20d`
- local runner log:
  - bytes: `19025`
  - SHA-256:
    `8ffbbe6a302d7e5b980ae55304549f2d5137f35ecc5a54386a4773b40609987e`.

## Frozen classification reason

The result serialized:

- `finite_all = true`
- `structure_match_all = true`
- `full_rank_all = false`
- `provenance_ok = false`.

Because provenance is a mandatory implementation gate, the historical Repair18b result remains IMPLEMENTATION_FAIL and cannot be relabelled.

## Frozen scientific payload

Despite the implementation classification, the diagnostic payload is preserved exactly.

For all three scale-5/10/20 cases:

- sparse and dense 2-point Jacobians are identical to reported precision:
  `relative_Frobenius_sparse_vs_dense = 0.0`;
- deterministic operator-action differences are <= about `6.6e-10`;
- dense numerical rank is `508/510`;
- two singular directions fall below the frozen numerical-rank tolerance.

The minimum reported singular-value ratio is

`3.2080122441324997e-20`.

Thus the payload does not support a sparse-pattern mismatch.

## Linearized probe payload

The dense linear least-squares correction has no active bounds and drives the frozen linearized residual essentially to zero.

At alpha=1:

- scale 5:
  - H = `2.2075494135623804e-10`
  - M = `6.409137112485408e-3`
- scale 10:
  - H = `7.499680745150575e-10`
  - M = `2.721523091739074e-1`
- scale 20:
  - H = `1.7692173094108183e-10`
  - M = `1.5226865731462237e-2`.

This payload is diagnostic only because Repair18b failed its implementation provenance gate.

## Harness defect

The imported Repair01 function

`build_nonK()`

returns its exact symbolic dictionary identity as a Boolean.

Repair18b incorrectly required

`kidentity <= 1e-12`.

Because Python treats `True` numerically as `1`, this condition evaluates false even when the exact symbolic identity passes.

The correct Boolean test is

`bool(kidentity)`.

No input hash, physics term, Jacobian, residual, scale, field, threshold, or classification rule needs to change.

## Licensed continuation

A separately preregistered harness-only Repair18b1 may change only this provenance predicate from the invalid numerical comparison to the Boolean identity check.

Repair18b itself remains IMPLEMENTATION_FAIL.

Repair18b1 must reproduce the frozen Repair18b diagnostic payload before assigning the preregistered scientific diagnostic class.
