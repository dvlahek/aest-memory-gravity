# GE19 Repair43 valid diagnostic — GE06 constraint-family shift sensitivity freeze

## Status

Repair43 completed successfully as a diagnostic-only result.

Classification:
`GE19_REPAIR43_QGE06_MAIN_CONSTRAINT_STAGE_SPLIT_COMPLETE`.

Preregistered route:
`QGE06_CONSTRAINT_ROW_FIELD_CLOSER_TO_FULL`.

All implementation gates pass. The frozen Repair37 PCHIP baseline and the
Repair42 Q_GE06-only direct382 and direct763 variants reproduce exactly in
both Z21 and active shift metric. No previous repair is relabelled.

Repair43 does not certify Z21, perform a science H4 reclosure or license
lensing.

## Immutable local outputs

- JSON: 9916 bytes, SHA-256
  `559ae65ffc5d21433799e4e33aa6d91237a9aa41b9799463971bc45dabecae44`;
- NPZ: 37722392 bytes, SHA-256
  `d5c8c02c7f8272dc390ce9e4d2374a35b2ce1b14da5b60e69dc8366499bfe71c`;
- FULL: 9916 bytes, SHA-256
  `559ae65ffc5d21433799e4e33aa6d91237a9aa41b9799463971bc45dabecae44`;
- outer runner: 17374 bytes, SHA-256
  `640c9f31959d4e5290a26c64e0dee2ec982866d942135e5261d3828ecc0afc13`.

Terminal marker:
`GE19_REPAIR43_DIAGNOSTIC_COMPLETE`.

## Frozen reproduction and active mask

- generated stage x versus Repair41: `0.0`;
- saved Repair41 PCHIP versus Repair37 PCHIP target: `0.0`;
- PCHIP Z21 and shift reproduction versus Repair42: `0.0`;
- direct382/763 GE06 BOTH Z21 and shift reproduction versus Repair42
  GE06-only: `0.0`;
- projected p0 exact;
- active sample count: 23850;
- all outputs finite.

The active-shift science target remains `1e-6` and is not relaxed.

## Frozen GE06 source-family results

| Variant | Active shift Linf | Active shift RMS |
|---|---:|---:|
| PCHIP baseline | 1.1749387207106255e-6 | 1.0515104304068532e-6 |
| direct382 main only | 8.00104907644944e-6 | 4.65152573801425e-6 |
| direct382 constraint family only | 4.720762493838458e-4 | 3.212863248349017e-5 |
| direct382 main plus constraint | 4.755180483851141e-4 | 3.33685344785325e-5 |
| direct763 main only | 1.9125499500968034e-5 | 1.1687276396418912e-5 |
| direct763 constraint family only | 1.340570409265403e-4 | 1.560705065451567e-5 |
| direct763 main plus constraint | 1.4187840843421127e-4 | 1.7528307562583297e-5 |

For direct382, the frozen active-field RMS difference from full GE06 is
`3.5053044897295815e-6` for constraint-family-only versus
`3.224425545693223e-5` for main-only.

For direct763 the corresponding differences are
`8.50429000256443e-6` versus `1.5351581497083544e-5`.

The constraint *family* is therefore closer to the full GE06 field at both
resolutions. This is not yet a result about either constraint row
individually.

## Frozen hotspot

Registered sample: C_max, beta0=1, Fourier m=8, Nt128 time index 3,
`ln(a)=-0.8989528773447014`.

Frozen Repair37 actual shift backward-error scale:
`4.457554307372833e-12`.

At this sample:

- baseline shift metric:
  `7.601328197865615e-7`;
- direct382 main-only:
  `2.6830674373598384e-6`;
- direct382 constraint-family-only:
  `4.720762493838458e-4`;
- direct382 both:
  `4.755180483851141e-4`;
- direct763 main-only:
  `7.061924922843726e-6`;
- direct763 constraint-family-only:
  `1.340570409265403e-4`;
- direct763 both:
  `1.4187840843421127e-4`.

The Q_GE06 direct-minus-PCHIP first constraint row0 source difference is
`2.1600003821566376e-15` for direct382, i.e.
`4.845707383943654e-4` of the frozen shift scale.

For direct763 it is `7.310994371678159e-16`, i.e.
`1.640135793653868e-4` of the scale.

The normalized source displacement closely tracks the shift spike. This
is not sufficient to prove which of the two constraint-source rows is
responsible because Repair43's CONSTRAINT_ONLY variant changed both rows.

## Structural operator interpretation

In the unchanged Repair07 canonical operator, the two constraint-source
rows are shift (combined source index 6) and anisotropy (index 7).
The operator uses the anisotropy source (index 7) in algebraic elimination,
while the independent shift-source row (index 6) is a separate constraint
check, not used to drive the canonical evolution.

Thus the Repair43 constraint-family intervention conflates two mechanisms:

1. a direct change of the independent shift constraint right-hand side;
2. an anisotropy-source change that can alter reconstructed variables and
   the propagation.

It is premature to label the GE06 physics, other H4 pieces, or the
normalization as erroneous based only on the mixed-representation
constraint-family-only spike.

## Next licensed step

A separately preregistered Repair44 diagnostic-only GE06
shift-row-versus-anisotropy-row source-stage split.

Requirements:

- use the exact frozen Repair37 PCHIP H4 baseline, Repair41 direct382/763
  GE06 stage arrays and Repair43 output;
- preserve frozen projected p0, factor-1 Radau, H4 canonical operator,
  active mask and original `1e-6` target;
- propagate PCHIP baseline, row0-only, row1-only and both GE06 constraint
  corrections for direct382 and direct763;
- reproduce exactly frozen Repair43 constraint-family-only Z21 and shift
  fields before interpreting the split;
- report unchanged source-node and hotspot controls, full active fields,
  actual absolute shift residual and backward-error denominator;
- check that row0-only leaves the propagated canonical state unchanged as
  predicted by the frozen operator;
- use no newly fitted offset, threshold or observational input.

Repair44 remains diagnostic-only and cannot certify Z21 or license lensing.
