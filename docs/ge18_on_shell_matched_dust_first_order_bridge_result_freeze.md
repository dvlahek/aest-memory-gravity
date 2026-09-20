# GE18 on-shell matched-dust first-order bridge — result freeze

## Status

Historical first GE18 local execution is frozen as

`GE18_ON_SHELL_MATCHED_DUST_FIRST_ORDER_BRIDGE_FAIL`.

This classification is immutable.

The failure is narrow: one implementation-added cross-file interpolation gate failed. The on-shell dust construction itself passed all preregistered numerical controls.

## Execution provenance

The local runner lock audit passed and all required frozen GE15 local inputs were present.

Relevant repository runner commit:

`f819fa1c3edd8ace2d05ecf7a316d1c8e2e4d3ac`.

Uploaded result files supplied after execution:

- JSON SHA-256:
  `b75de90d001ba229f1970fff38a3dc69e874da734b80e68f5b1844a139bfdde9`;
- NPZ SHA-256:
  `b6ccaf2257fbb09df701c43bc9a593a3f68238826277a510a0b3b531ea9fa6fe`;
- full log SHA-256:
  `b75de90d001ba229f1970fff38a3dc69e874da734b80e68f5b1844a139bfdde9`;
- runner log SHA-256:
  `cf1e18917f0ac75fcb1d73ca438fd747c7d8fec369f128d913fbd7616351d577`.

The JSON and full log are byte-identical because the script prints the JSON payload directly.

## Passed core provenance controls

- parent GE15 classification:
  `GE15_CANCELLATION_FREE_S_STATE_PRECISION_CLOSURE_PASS`;
- R1 dense trace SHA matched the value frozen by GE15 exactly;
- dense accepted-step trace versus raw CLASS perturbation output:
  abs-or-rel maximum `0.0`;
- requested-k relative miss gate passed.

Therefore the frozen metric perturbation trace and raw CLASS perturbation files are provenance-consistent at their native common points.

## Passed on-shell dust controls

Primary/control DOP853 convergence:

- absolute-density global relative L2 maximum:
  `7.73203670933738e-9`;
- momentum global relative L2 maximum:
  `7.774364641179449e-9`.

Both pass the frozen `1e-8` limits.

The initial absolute density match passes the frozen `1e-10` limit.

The initial absolute momentum match passes the frozen `1e-10` limit.

The exact GE07 dust-potential identity gives

`max abs-or-rel(dot(T1),psi)=8.326672684688674e-17`

against the frozen `1e-9` limit.

All outputs are finite.

## Failed gate

The only failed gate is

`metric_and_background_cross_file_abs_or_rel_le_1e8`.

Observed maximum:

`7.590304690330285e-8`.

This gate was not one of the frozen numerical controls in the GE18 preregistration. It was added during implementation as an extra sanity check.

The implementation evaluates the dense trace on the 64 common `ln(a)` nodes using the frozen GE09 Hermite/PCHIP state representation, while it independently PCHIP-interpolates the raw CLASS mode files and background file onto those same nodes.

Thus the failed quantity mixes:

1. a native provenance comparison, which already passes exactly with error `0.0`; and
2. a comparison of two different interpolation representations away from their common native points.

It cannot be interpreted as a physical inconsistency or a failure of the on-shell dust equations.

The historical GE18 classification nevertheless remains FAIL.

## Descriptive reduced-matter model error

No model-error acceptance gate was preregistered.

For the central `C_star` dust model versus the full standard CLASS sector:

- density global relative L2:
  `1.3765302104657398e-3`;
- density pointwise relative maximum:
  `5.069139301271249e-3`;
- momentum global relative L2:
  `6.891936293682233e-3`;
- momentum pointwise relative maximum:
  `1.778016087606809e-2`.

The mismatch is exactly zero at the matching surface `z=1.5` by construction and grows smoothly toward `z=0.2`.

At `z=0.2` across the six frozen k modes:

- density global relative L2:
  `4.823418757097107e-3`;
- momentum global relative L2:
  `1.6806577682240635e-2`.

The error also grows smoothly with k. This is consistent with the reduced pressureless model omitting the small but finite standard radiation/neutrino stress documented by GE16/GE17.

## GE17 background envelope propagated into GE18

Relative to the central dust result:

- `C_min` density global L2 shift:
  `4.3793528365838954e-5`;
- `C_max` density global L2 shift:
  `5.58765717440552e-5`;
- `C_min` momentum global L2 shift:
  `2.1965036600727895e-4`;
- `C_max` momentum global L2 shift:
  `2.8020843420250804e-4`.

Therefore the dominant first-order reduced-matter discrepancy is the dynamical pressureless approximation relative to full standard matter, not the GE17 `C_min/C_max` background-normalization envelope.

## Licensed repair

Exactly one GE18 Repair01 is licensed.

Repair01 may:

- keep the native dense-trace SHA gate;
- keep the exact native dense-trace versus raw CLASS perturbation control;
- keep every preregistered dust integrator/matching/GE07-map gate unchanged;
- retain the 64-node cross-interpolation mismatch only as a descriptive diagnostic.

Repair01 may not:

- relax any preregistered numerical threshold;
- add a model-error acceptance threshold;
- change the dust equations;
- change `C_min,C_star,C_max`;
- change the initial matching surface or matching prescription;
- alter the GE07 map;
- relabel historical GE18.

## Claim boundary

This result does not yet license reduced-H3 Z20 because the executed historical classification is FAIL.

A separately locked GE18 Repair01 must execute and pass first.
