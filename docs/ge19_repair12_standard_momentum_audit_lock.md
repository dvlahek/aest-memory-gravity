# GE19 Repair12 remaining-standard-momentum audit lock

## Status

**DIAGNOSTIC IMPLEMENTATION LOCKED BEFORE REPAIR12 LOCAL RESULT**

Repair11 remains historically frozen as

`GE19_REPAIR11_LAMBDA_INCLUSIVE_REDUCED_H1_RECLOSURE_FAIL`.

Repair12 is diagnostic only and does not relabel Repair11.

## Parent Repair11 freeze

Commit:

`2943869fc88146176e62147bf7b4175d9216df41`

File:

`docs/ge19_repair11_lambda_h1_result_freeze.md`

Blob:

`a1b5c9a6e638305ecd0a9a16096b109befdd2dd3`

Frozen Repair11 JSON:

- SHA-256 `5283dd425864e8f6613678a1ad90a71e2d69243cbecd868685af45c52be077ab`
- bytes `67437`

Frozen Repair11 NPZ:

- SHA-256 `ed2431e59d89f820796f6e9b534b8ca19ae026ad55597302bf92ddb120dfec83`
- bytes `273299`

## Repair12 preregistration

Primary prereg commit:

`2f6e2b7da3d8e14b29a9f7998d30a6926aecf00e`

File:

`ge19/repair12_predata_remaining_standard_momentum_audit.json`

Blob:

`c5845dd439ad00e49cc0b06213b0c06a07b51247`

Metric/reproduction amendment commit:

`5a278b0ee78d6888a11eaa6ecd22cb1dcee9ec21`

File:

`ge19/repair12_predata_amendment01_metric_and_reproduction_lock.json`

Blob:

`fc5d084b85d12c35c3a7b44bb08f43c25a13ebff`

## Diagnostic implementation

Implementation commit:

`67af4ee595a298000aadee1d04820a9e9564431a`

File:

`ge19/repair12_remaining_standard_momentum_audit.py`

Blob:

`6861ada55e28e5834df30e192b404fb8b3e6322b`

Repair12 loads the frozen Repair11 trajectory and does not rerun the canonical dynamics.

For each frozen C, mode, grid and time node it evaluates:

- the frozen Repair11 Lambda-inclusive GE06 shift contribution;
- the frozen reduced-dust GE07 shift contribution;
- the full-standard CLASS momentum contribution in the same GE07 action normalization;
- the omitted momentum correction
  `Delta E_b = E_b^(full CLASS) - E_b^(reduced dust)`.

The exact diagnostic identity is checked numerically:

`r_full = r_dust + Delta E_b`.

## Metric contract

The current Repair11 science shift metric is reproduced using the unchanged componentwise backward-error definition.

The full-standard counterfactual uses the exact Repair08 pair metric:

`|E_b^(GE06)+E_b^(full CLASS)| / max(|E_b^(GE06)|, |E_b^(full CLASS)|, tiny)`.

Repair12 must reproduce the frozen Repair11 global shift maximum

`5.016294027155656e-5`

with relative error <= `1e-10` before any routing result is accepted.

## Executable prelock audit

Workflow:

`.github/workflows/ge19-repair12-prelock-audit.yml`

Workflow blob:

`c55b4b1ea9f5f46e12b5aa9e2ac713659e676718`

GitHub Actions run:

`35570277631`

Job:

`106240267998`

Conclusion:

`success`

Terminal marker:

`GE19_REPAIR12_PRELOCK_AUDIT_PASS`

The audit independently derived

`FULL_STANDARD_SHIFT_DERIVATION = -6*I*a**4*rho*theta/k`.

Metric falsification controls:

- exact cancellation -> `0.0`;
- same-sign equal contributions -> `2.0`.

The workflow also statically verifies that Repair12 does not call the canonical H1 solver, Radau integrator, or H3 matrix builder.

## Frozen routing

Repair12 may return only:

- `OMITTED_STANDARD_MOMENTUM_EXPLAINS_REMAINING_SHIFT` if the full-standard counterfactual max <= `1e-6`;
- `OMITTED_STANDARD_MOMENTUM_DOMINANT_WITH_CLASS_INTERPOLATION_FLOOR` if the improvement is >=10x and full-standard counterfactual max <= `1e-5`;
- `BACKGROUND_OR_REDUCED_DYNAMICS_REMAIN` otherwise;
- `REPAIR12_IMPLEMENTATION_REPRODUCTION_FAIL` if frozen Repair11 trajectory reproduction fails.

No threshold is relaxed.

## Claim boundary

Repair12 is only a diagnostic attribution test for the remaining Repair11 shift residual.

It does not certify Stage A, H3/Z20, finite eta, finite-amplitude nonlinear evolution, collapse, lensing or observational detection.
