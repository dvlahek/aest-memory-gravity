# GE19 Repair25 first-order bath boundary dictionary audit — result freeze

## Status

First valid Repair25 science audit completed successfully as a diagnostic execution.

Terminal classification:

`GE19_REPAIR25_FIRST_ORDER_BATH_BOUNDARY_DICTIONARY_AUDIT_COMPLETE`.

Frozen route:

`LEGACY_V077_BOUNDARY_TRACE_INCOMPATIBLE_GE15_CERTIFIED`.

Science exit:

`0`.

Repair25 remains diagnostic only.

## Frozen output provenance

Result JSON:

`results/ge19_repair25_first_order_bath_boundary_dictionary_audit.json`.

SHA-256:

`ccf30e5d706f91c023e31526a9ae66154ecadbfa15e3f90a5239824ad74c7a05`.

Bytes:

`64000`.

FULL science log:

`results/ge19_repair25_first_order_bath_boundary_dictionary_audit_FULL.log`.

SHA-256:

`ccf30e5d706f91c023e31526a9ae66154ecadbfa15e3f90a5239824ad74c7a05`.

Bytes:

`64000`.

Locked runner SHA-256 reported by the execution:

`64100b1960050ecb194579357db3d383866a068788523dd3f159558a7087280b`.

Runner bytes:

`8168`.

The execution consumed the frozen Repair24, Repair22, Repair13, GE15 and v0.77 inputs and passed every runner-level provenance audit before science.

## Exact a=0.4 dictionary closure

GE15 algebraic reference:

- X versus grad(chi)/a relative L2:
  `6.961752470055609e-17`;
- pointwise abs-or-rel:
  `1.8940232492426095e-21`.

Reduced GE19 / Repair22 on-shell X10 versus GE15:

- relative L2 max:
  `7.819918013124737e-17`;
- pointwise abs-or-rel max:
  `1.8940232492426095e-21`.

Q dictionary closure:

- Q_action versus GE15 relative max:
  `1.1102230246251565e-16`;
- v0.77 Q_trace versus GE15 relative L2:
  `1.1065592085855149e-16`;
- v0.77 Q_trace pointwise abs-or-rel:
  `1.3552527156068805e-20`.

Therefore GE15, Repair22/GE19 and the Q trace agree to numerical precision on the frozen initial surface.

## v0.77 amplitude incompatibility

At a=0.4 the direct v0.77 chi/a versus GE15 chi/a mismatch is:

- global relative L2:
  `0.9999998670367867`;
- pointwise abs-or-rel:
  `0.9999999460419693`.

The six positive-mode v0.77/GE15 amplitude ratios are approximately:

- k_h=0.03: `64266.179725142996`;
- k_h=0.05: `11778726.049248401`;
- k_h=0.08: `18532922.462558754`;
- k_h=0.10: `11751838.221065594`;
- k_h=0.15: `6528855.307426735`;
- k_h=0.20: `3247319.67226704`.

Their complex ratio phases are zero to floating-point accuracy.

Thus the mismatch is not a phase/sign error. It is a strongly mode-dependent amplitude normalization mismatch.

## Common-window shape audit

Common overlap:

- a in `[0.4, 0.8333333333333334]`;
- 128 nodes.

Direct v0.77 versus GE15:

- relative L2:
  `0.9999998669793289`;
- pointwise abs-or-rel:
  `0.9999999460679324`.

A single global real scale does not close the mismatch:

- best scale:
  `5256501.110338989`;
- post-fit relative L2:
  `0.5484311025444283`.

A single global complex scale also does not close it:

- magnitude:
  `4909668.237732929`;
- phase:
  `9.033633411337888e-18`;
- post-fit relative L2:
  `0.46599450356276223`.

In contrast, fitting one independent real scale per k mode gives:

- post-fit relative L2 between
  `0.00030118201657457184`
  and
  `0.00030346193149017757`;
- temporal-shape cosine between
  `0.9999999539554272`
  and
  `0.9999999546446953`.

Therefore each mode has essentially the same temporal shape in v0.77 and GE15, but a different mode-dependent amplitude normalization.

## Frozen convention-factor audit

No tested simple convention factor closes the discrepancy.

Among the tested forms, `1/k` gives the smallest report-only post-fit residual after allowing an additional complex scalar:

`0.25783615676918054`.

The next closest tested forms are:

- `a/k`: `0.28507333879516455`;
- `a/(i k)`: `0.2850733387951646`.

These are far above the frozen `1e-3` compatibility scale.

No candidate factor is adopted.

The reported log-log k slope of independent per-mode scales,

`1.5955181856084877`,

is descriptive only and is not a licensed normalization law because the six scale factors are non-monotonic.

## Frozen gate result

PASS:

- Q_action versus GE15;
- GE15 algebraic identity;
- Repair22 X10 versus GE15;
- all per-mode temporal-shape cosines >= 0.9999.

FAIL / incompatible:

- direct v0.77 versus GE15 compatibility;
- single best global scale closure.

This uniquely selects:

`LEGACY_V077_BOUNDARY_TRACE_INCOMPATIBLE_GE15_CERTIFIED`.

## Scientific conclusion

Repair24's unique X10 bridge failure did not expose an inconsistency in the certified GE15 first-order AeST state or in the Repair22/GE19 on-shell H1 dictionary.

GE15 and Repair22/GE19 agree to machine precision.

The historical v0.77 boundary trace carries a different mode-dependent amplitude normalization while preserving essentially the same per-mode time dependence and phase.

Therefore the next valid task is not a q20 rerun and not a fitted rescaling.

The next task must derive the legacy v0.77 mode-amplitude normalization from its generating construction and certify the exact map into the GE15/GE19 convention before q20 is reconstructed.

## Stop boundary

- `q20_rerun_performed = false`;
- q20 remains not certified;
- no fitted normalization is adopted;
- H4/Z21 remains unlicensed.

Repair24 remains a historical FAIL and is not relabelled.
