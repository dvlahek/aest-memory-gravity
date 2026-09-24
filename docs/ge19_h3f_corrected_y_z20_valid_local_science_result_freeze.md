# GE19 H3F — valid local action-completed Y Z20 science result freeze

## Classification and exact scope

**`GE19_H3F_CORRECTED_Y_H3_Z20_CERTIFIED`**.

The first separately versioned H3F science execution passed
every preregistered gate, with local terminal marker
`GE19_H3F_NEW_Z20_SCIENCE_PASS`. This certifies only the
low-mode, finite-window, constraint-controlled reduced
H3/Z20 particular computed with the action-completed
NL0C Y aether + scalar raw RHS and unchanged frozen
GE06, GE07 and Lambda non-Y terms.

It does **not** certify a homogeneous/primordial
second-order solution, full species, the new q20 bath,
full all-sector H4 Noether compatibility, H4/Z21,
finite physical eta, lensing or observations.

The prior H3F preregistration, source-adapter implementation,
science code and fixed thresholds were unchanged during
the reported local science execution. Historical
Repair22/27/32 certifications remain their own results.
Repair37 remains historical science FAIL.
Repair38--44 remain diagnostic-only.

## Local result provenance

The user supplied all four exact output files and the
terminal log. Uploaded paths have copy-suffixes on
some names but hashes identify the original local
runner outputs. Their bytes and SHA-256 were
independently verified from uploaded files.

| Result | Bytes | SHA-256 |
|---|---:|---|
| `results/ge19_h3f_corrected_y_z20_science_reclosure.json` | 414800 | `0616188d2bb7a6c09b2b56433a1f8a1860f360b2e54d2cb84e1ae214a407866b` |
| `results/ge19_h3f_corrected_y_z20_science_reclosure_FULL.log` | 414800 | `0616188d2bb7a6c09b2b56433a1f8a1860f360b2e54d2cb84e1ae214a407866b` |
| `results/ge19_h3f_corrected_y_z20_science_reclosure.npz` | 14181793 | `90840755fa9febb1d8cb84609d9e58f67dec2a0a01cd6bf8e47685b45caa4542` |
| `results/ge19_H3F_LOCAL_runner.log` | 9844 | `c38599aba33efdee9106f7f6ce198701201da543f43a6ade72dbe7d798be4bf2` |

The JSON and inner FULL log are byte-identical. The
NPZ contains 62 fields, all finite, including the
complete `(beta=3,m=40,state=6,Nt=128)` primary
Z20 cohorts, boundary p0, source and shift controls.
The runner records all three preexecution markers
`GE19_H3F_LOCK_PASS`,
`GE19_H3F_LOCAL_PREEXECUTION_AUDIT_PASS`,
`GE19_H3F_FROZEN_PARENTS_PASS`.

## Parent/adapter controls

- Old-Y-disabled baseline replay reproduced the exact
  original Repair22 Z20 and projected p0 with reported
  maximum relative L2 differences 0.0 and 0.0.
- The frozen Stage E source-result SHA is
  `c3ff4cc18dc8c7a69ba661a68ea3de987818f1b9c1db3275b08f2976c385896e`.
- The prior scalar-only Y source was **replaced**, not
  added to the new u+phi rows.
- Recomputed source-aware p0 reproduction relative L2:
  `0.0`. Old Repair18 p0 difference is report-only,
  max `3.473886544805647e-16`.
- Initial projected constraint scaled residual:
  `2.482534153108436e-16`. Lapse and shift
  backward error maxima are `2.639992134386278e-16`
  and `3.321187887383499e-16`; projected and
  augmented ranks equal 2.

## Frozen science metrics (unchanged thresholds)

- H1 Nt64 old-parent reproduction: state and
  derivative relative L2 maxima both `0.0`.
- H1 linear residual `4.3389056048311334e-16`;
  H1 shift backward error `6.370007701051935e-08`.
- H3 main RHS source-spatial Nx1024/Nx2048
  low-mode relative L2 `1.396725754522341e-12`
  against `5e-4`.
- H3 Nt64/Nt128 state relative L2
  `1.5208749234474405e-05`
  against `5e-3`.
- H3 linear-system residual `2.1791561708741177e-13`
  against `1e-8`; anisotropy
  backward error `6.391121604651976e-16`
  against `1e-6`.

**Active shift**, with the originally frozen
near-null/active split:

- Nt128 active L-infinity
  `8.067171756100188e-07` against **unrelaxed**
  `1e-6`;
- matched Nt64 active L-infinity
  `7.796430200329358e-06`;
- matched L-infinity order
  `3.2357755676907107` against `>=2.5`;
- matched L2 order
  `3.1225511608309504` against `>=2.5`;
- active samples `24057`, near-null samples
  `22023`;
- near-null absolute residual over S_ref
  `9.599035641086836e-15` against
  `1000*eps(float64)`.

The legacy *all-row* shift metrics `1.983174285151758`
(primary) and `1.8946211278683025` (control)
are report-only historical diagnostics. They are
not interchangeable with the preregistered
active/near-null cancellation-safe certification
metric. Their values were not hidden or removed.

Worst active sample:
`C_star, beta0=0.1, m=6, Nt128 index 29,
ln(a)=-0.7486914714227706`, with
absolute residual `1.0183081980627736e-16`
and scale `1.2622864974862537e-10`.

All individual science gates report true; failed
gate list is empty. All stored NPZ arrays are finite.

## Next physics route

Preregister and independently execute a **new
corrected-Y q20 reconstruction**, changing the
Z20 parent from historical Repair22 to this
H3F certified Z20. Retain the frozen Repair26 R1
cancellation-free first-order full-history bath,
the unchanged Repair24/27 normalized bath
equations, `z20(a0)=0`, `dz20/dxi(a0)=0`,
original spatial/time/quadrature grids and gates.
The old Repair27 numerical q20 array is an
independent comparator only, never automatically
a parent for the new corrected-Y Z20.

Before any corrected H4/Z21 science reclosure,
derive and test complete **all-sector** H4
source/Noether compatibility on one consistent
corrected parent/time representation. Stage E
Y-only source-row PASS does not by itself
establish full H4 compatibility.

**Z21 remains NOT CERTIFIED. Lensing remains blocked.**
