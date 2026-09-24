# GE19 Repair42 valid diagnostic — direct target H4 propagation above science target

## Frozen classification and route

Repair42 completed as a valid diagnostic, with classification

`GE19_REPAIR42_DIRECT_TARGET_H4_PROPAGATION_DIAGNOSTIC_COMPLETE`.

The preregistered route is

`DIRECT_TARGET_CORRECTION_ABOVE_SCIENCE_TARGET`.

All implementation gates pass. This is **not** a science H4/Z21 reclosure.
Repair37 remains the immutable historical science FAIL. Repair38--Repair42
remain diagnostic-only. Z21 is not certified and lensing remains blocked.

## Frozen user-supplied artifacts

- JSON: 6426 bytes, SHA-256
  `4a211581a77c1ad00e14cc398ca7a19b12642f3f3e35b416314d6721f5f81e25`;
- NPZ: 41367682 bytes, SHA-256
  `a60515f3d92bbd388fd2fadae6cf2dd07f3ee68e8690b07632bbe5091e9013c5`;
- FULL: 6426 bytes, SHA-256
  `4a211581a77c1ad00e14cc398ca7a19b12642f3f3e35b416314d6721f5f81e25`;
- outer runner: 11002 bytes, SHA-256
  `855067c5f733374d98a97e5013c0f23ea1cfbcb1f62494a596beab9768cbcf9c`.

Terminal marker: `GE19_REPAIR42_DIAGNOSTIC_COMPLETE`.

## Frozen reproduction

- generated stage x versus Repair41 stored stage x: exactly `0.0`;
- Repair41 saved PCHIP target versus Repair37 PCHIP: relative L2 `0.0`;
- frozen Repair37 baseline Z21 reproduction: relative L2 `0.0`;
- frozen Repair37 baseline shift-metric reproduction: relative L2 `0.0`;
- projected p0 exact;
- frozen active sample count: `23850`;
- all outputs finite;
- unchanged science target: `1e-6`.

## Frozen direct-target propagation

| Variant | Active Linf | Active RMS |
|---|---:|---:|
| PCHIP baseline | 1.1749387207106255e-6 | 1.0515104304068532e-6 |
| direct382 M1 only | 1.174938735937822e-6 | 1.051510440409759e-6 |
| direct382 Q_GE06 only | 4.755180483851141e-4 | 3.33685344785325e-5 |
| direct382 both | 4.755180486721134e-4 | 3.3368534572853516e-5 |
| direct763 M1 only | 1.1749387364482247e-6 | 1.051510440651074e-6 |
| direct763 Q_GE06 only | 1.4187840843421127e-4 | 1.7528307562583297e-5 |
| direct763 both | 1.4187840851992924e-4 | 1.752830758224085e-5 |

Both combined direct corrections remain above `1e-6`.
M1-only is essentially neutral for the shift metric. The increase follows
Q_GE06.

The absolute shift residual maxima do not increase with the direct Q_GE06
correction: baseline `3.2233694490020835e-10`, direct382 both
`1.0078526038795732e-10`, direct763 both
`1.1338576958899654e-10`. Thus the larger normalized shift metric
cannot be described as a corresponding increase in the global absolute
residual maximum.

## Post-freeze NPZ localization

These analyses use only the emitted frozen Repair37, Repair41 and Repair42
NPZs. They do not alter the Repair42 route or gates.

The active Linf hotspot occurs for Fourier mode `m=8`, near the left edge
of the window, at Nt128 time index `it=3`,
`ln(a)=-0.8989528773447014`, in each of C_min, C_star and C_max.
The same site appears for all beta columns within floating precision.

For C_max, beta0, mode 8, it=3:

- frozen Repair37 shift scale:
  `4.457554307372833e-12`;
- frozen Repair37 absolute shift residual:
  `3.3883333250150448e-18`;
- frozen Repair37 shift metric:
  `7.601328197865615e-7`;
- frozen Repair41 Q_GE06 constraint row0 PCHIP magnitude:
  `4.1330133389195965e-12`;
- direct382-minus-PCHIP Q_GE06 constraint row0 magnitude:
  `2.1600003821566376e-15`;
- this delta divided by the frozen shift scale:
  `4.845707383943654e-4`;
- resulting direct382 BOTH metric at this site:
  `4.755180486721134e-4`;
- direct763-minus-PCHIP Q_GE06 constraint row0 magnitude:
  `7.310994371678159e-16`;
- this delta divided by frozen shift scale:
  `1.640135793653868e-4`;
- resulting direct763 BOTH metric at this site:
  `1.4187840851992924e-4`.

This near equality between the normalized constraint-source displacement and
the observed normalized shift defect makes the Q_GE06 constraint row,
specifically its first source component, the immediate localization target.

The tiny *global* Repair41 Nt382-versus-Nt763 source relative L2 does not
certify the Q_GE06 constraint row to `1e-6` of the much smaller, local
shift-equation scale. The direct382 and direct763 hotspot defects differ by
more than a factor of three even though the full direct target references
satisfied their inherited relative-L2 parent gates.

The current evidence is consistent with a mixed-representation, constraint
source-compatibility defect caused by patching only selected direct fine-grid
H4 pieces into the frozen coarse-grid PCHIP total. It does not yet prove
that other physical source pieces are erroneous or that the underlying
equations fail.

## Next licensed localization

Repair43 should be preregistered as a **diagnostic-only Q_GE06
main-versus-constraint stage-correction decomposition**:

- freeze all Repair37/Repair41/Repair42 parent artifacts;
- preserve the original factor-1 canonical propagation, projected p0,
  active mask and `1e-6` target;
- compare PCHIP baseline, direct382/direct763 Q_GE06 main-only,
  constraint-only and main+constraint corrections;
- reproduce the frozen Repair42 Q_GE06-only variants exactly before
  interpreting the split;
- store not only normalized shift metric, but absolute shift residual
  and its actual backward-error denominator at every original Nt128 node;
- inspect the registered C_max/beta0/m8/it3 hotspot and the full active
  field without changing the active mask;
- distinguish a source-row compatibility defect from changes in the
  canonical propagated state.

Repair43 must not relabel Repair42, change source physics, relax thresholds,
certify Z21 or license lensing.
