# GE11 Repair01 precision-key binding — result freeze

## Status

Frozen first science-reaching GE11 Repair01 execution.

Terminal classification:

`GE11_REPAIR01_DENSE_LOCAL_JET_FIXED_REFINEMENT_FAIL`.

Historical classifications remain unchanged:

- `GE09_DENSE_ACCEPTED_STEP_LOCAL_JET_BRIDGE_FAIL`;
- `GE11_DENSE_LOCAL_JET_FIXED_REFINEMENT_FAIL`.

GitHub Actions run:

`35497478790`.

Execution HEAD:

`ef5d8909ba5df78bd744c466df8e6d90234fcfdc`.

Artifact:

- ID: `10600652596`;
- name: `results_bundle_ge11_repair01_precision_key_binding`;
- size: `459195734` bytes;
- ZIP SHA-256:
  `b35a3a0c8bbd22483bd04c006b20ceb97d3c7f263e178382026cba2983628ecc`.

## Precision binding

The repaired runtime provenance gates pass:

- active pinned-CLASS precision keys present;
- obsolete singular keys absent from both Repair01 precision files;
- R1 and R2 dense accepted-step traces have different hashes.

Dense trace hashes:

- R1:
  `c50aae91fee94f00e1cbb5bd3c4d9352f15d892e91b230fad690f06c43e25fbd`;
- R2:
  `5a9480f69744db59ab8ca7fbdef56398c5fe38493730976d92b25873f46379b1`.

Therefore the corrected R1/R2 precision parameters genuinely reached the pinned CLASS runtime.

## R1 result

Accepted points per k in the frozen window:

`{49,49,49,49,49,58}`.

Maximum ln(a) gaps:

`{0.0159294,0.0159902,0.0160953,0.0160171,0.0158100,0.0156856}`.

Source-grid validation maximum:

`1.8417064525777546e-6`

against the frozen `1e-4` limit.

The previous GE09 `delta_dark` mismatch is no longer dominant:

`delta_dark = 3.6727326412949733e-9`.

Primary/decimated complete-jet controls:

- global relative-L2 maximum:
  `2.741562317126901e-6`;
- pointwise abs-or-rel maximum:
  `3.482707541498957e-6`.

All frozen R1 single-level gates pass.

## R2 result

Accepted points per k:

`{54,55,55,56,55,59}`.

Maximum ln(a) gaps:

`{0.0142764,0.0142672,0.0140930,0.0141183,0.0142083,0.0139054}`.

Source-grid validation maximum:

`1.29585287056976e-6`.

`delta_dark = 1.3060535846881182e-9`.

Primary/decimated complete-jet controls:

- global relative-L2 maximum:
  `1.3556879527450145e-6`;
- pointwise abs-or-rel maximum:
  `2.7947850632538266e-6`.

All frozen R2 single-level gates pass.

## Failed refinement gate

The R1 and R2 complete jets are not mutually converged.

Frozen cross-level limits:

- global relative L2 <= `5e-4`;
- pointwise abs-or-rel <= `2e-3`.

Observed maxima:

- global relative L2:
  `0.45886068704381233`;
- pointwise abs-or-rel:
  `0.7829092344800966`.

Both cross-level gates fail by large margins.

Largest cross-level channels:

- `u`: global `0.4588606665`, pointwise `0.7829090407`;
- `ut`: global `0.4588606870`, pointwise `0.7829092345`;
- `ux`: global `0.4532668449`, pointwise `0.7829090407`;
- `pt`: global `0.1706062311`;
- `px`: global `0.1839330823`;
- `Lt=Rt`: global `0.0262145608`;
- `Lx=Rx`: global `0.0187977308`;
- `Nx`: global `0.0147403696`.

Metric state channels themselves differ much less:

- `N`: global `0.00428111`;
- `L=R`: global `0.00544709`.

## Scientific interpretation

Repair01 resolves the historical source-grid interpolation failure.

The corrected precision levels show that:

1. the accepted-step representation becomes substantially denser;
2. source-grid validation improves by roughly two orders of magnitude;
3. internal primary/decimated interpolation controls become extremely small;
4. nevertheless the physical/local-jet state changes materially from R1 to R2.

Therefore the remaining bottleneck is not the historical `delta_dark` source-grid interpolation error.

It is cross-precision convergence of the underlying AeST/aether/scalar state, especially the channels feeding `u,ut,ux,pt,px`.

The complete GE06 local jet is not certified.

## Project boundary

Do not:

- relax the R1/R2 cross-level gates;
- select R2 alone because its single-level gates pass;
- add an unpreregistered R3 sequence;
- proceed to `Z20`;
- infer that the large `u` discrepancy is physical rather than numerical.

A separately preregistered diagnostic may compare the underlying native R1/R2 state channels before the GE06 jet mapping and localize the discrepancy among:

- `alpha_aest`;
- `E_aest`;
- `theta_dark`;
- `chi`;
- `phi,psi`;
- physical RHS derivatives;
- normalization/dictionary operations.

Such a diagnostic must use only the frozen Repair01 artifact and cannot change either precision level or the interpolation representation.
