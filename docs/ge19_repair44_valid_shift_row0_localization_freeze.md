# GE19 Repair44 valid diagnostic — independent GE06 shift-source row localization

## Classification and immutable route

Repair44 completed as a valid **diagnostic-only** result:

`GE19_REPAIR44_QGE06_SHIFT_ANISOTROPY_ROW_SPLIT_COMPLETE`.

The frozen preregistered route is:

`QGE06_SHIFT_ROW0_FIELD_CLOSER_TO_FULL`.

All 13 implementation gates passed. The original Repair37 science FAIL
remains immutable. Repair38--Repair44 are diagnostics only. Neither
window-local particular Z21 nor lensing is certified by this result.

## Exact frozen local artifacts

- JSON: 13943 bytes; SHA-256
  `4f59f9a1aac21b267a00f75c5d5f0a0f791cfc20a4825f78b433729a4c50d435`.
- NPZ: 37706449 bytes; SHA-256
  `951694b7d83cdef312b766945b1f8a9844d1d6dd3a875929c5befc834c87f051`.
- FULL log: 13943 bytes; SHA-256
  `4f59f9a1aac21b267a00f75c5d5f0a0f791cfc20a4825f78b433729a4c50d435`.
- Outer runner log: 24242 bytes; SHA-256
  `ba532ceda0cb8b3fc7ba79699d49b95c3b1517061243500efc7257475dd77103`.

Terminal marker:
`GE19_REPAIR44_DIAGNOSTIC_COMPLETE`.

## Frozen integrity controls

- generated factor-1 stage coordinates versus saved Repair41 stages: 0.0;
- saved Repair41 target PCHIP versus Repair37: relative L2 0.0;
- PCHIP baseline Z21 and shift versus Repair43: relative L2 0.0;
- direct382/direct763 BOTH constraint-row Z21 and shift versus frozen
  Repair43 CONSTRAINT_ONLY: relative L2 0.0;
- shift-row0-only Z21 versus PCHIP baseline: **exact equality** for both
  direct382 and direct763, maximum absolute difference 0.0;
- projected p0 unchanged, active mask unchanged, active sample count 23850,
  all outputs finite;
- no science threshold relaxation, no observational inputs.

## Preregistered full-active-field attribution

| Direct resolution | Row0-only to full RMS | Row1-only to full RMS | Closer single-row field |
|---|---:|---:|---|
| Nt382 | 1.330579226777027e-5 | 3.1819579585608295e-5 | SHIFT_ROW0_ONLY |
| Nt763 | 3.2855892593937466e-5 | 3.7920942725665424e-5 | SHIFT_ROW0_ONLY |

The preregistered route selects shift-row0-only for both resolutions.
This is a closer-field statement, **not** a claim that row1 is negligible:
row1-only changes the canonical/algebraic reconstruction, with reported
full-Z21 relative L2 changes 1.3694392289496816e-14 (Nt382) and
4.4327374499077066e-14 (Nt763).

## Frozen active shift metrics

| Variant | Active Linf |
|---|---:|
| PCHIP baseline | 1.1749387207106255e-6 |
| direct382 shift row0 only | 4.838106055745792e-4 |
| direct382 anisotropy row1 only | 3.109549229010864e-5 |
| direct382 both constraint rows | 4.720762493838458e-4 |
| direct763 shift row0 only | 1.6325344654560058e-4 |
| direct763 anisotropy row1 only | 7.541666375800236e-5 |
| direct763 both constraint rows | 1.340570409265403e-4 |

No variant meets the frozen 1e-6 science target.

## Registered C_max / beta0=1 / m=8 / it=3 hotspot

The immutable hotspot is ln(a) = -0.8989528773447014.
Frozen Repair37 backward-error scale:
`4.457554307372833e-12`.

For shift source row0 alone:

- direct382-minus-PCHIP source delta magnitude:
  `2.1600003821566376e-15`;
- direct763-minus-PCHIP source delta magnitude:
  `7.310994371678159e-16`;
- normalized to the frozen local shift scale:
  `4.845707383943654e-4` and `1.640135793653868e-4`.

The registered complex identity closes exactly at this sample, for both
resolutions:

`shift_residual(row0_only) - shift_residual(baseline) = - delta_shift_source_row0`.

Reported complex identity absolute defect is 0.0.
The row0-only canonical Z21 state is identical to baseline, as predicted by
the frozen operator. Thus the extra shift residual follows directly from
changing the independent source right-hand side without changing the
canonical solution.

The hotspot residual identity is a **property of this selective source
intervention**, not an independent proof that the native fine-grid GE06
source, the GE06 physics, or the full H4 equations are inconsistent.

## Scientific interpretation and stop boundary

Repair44 localizes the major mixed-representation discrepancy to
the independent GE06 shift-source row0. The tested intervention
changes only that row's RHS while retaining the frozen coarse PCHIP
state and non-target source pieces. Therefore a large resulting
constraint residual is algebraically expected. Further single-row
source patches would not establish a consistent physical H4 solution.

The remaining necessary question is **full-source constraint/Noether
compatibility on one common parent/time representation**, with the
unchanged projected p0 rule and the actual original 1e-6 backward-error
target. No observational tuning and no adjustment of an isolated
source row to make the residual small.

Recommended next phase:

1. freeze Repair44 and explicitly stop the isolated source/interpolator
   repair sequence;
2. perform a source-level analytical compatibility audit of the
   entire H4 shift/anisotropy/main-source dictionary and its Noether
   relation on a common parent/time representation;
3. only if that audit passes, preregister one integrated science H4/Z21
   reclosure with independent time control;
4. if it fails, correct the identified source/constraint derivation
   through a separate physical/theoretical revision without relabeling
   historical results.

Repair44 does not license a new partial H4 stage-correction "repair",
Z21 certification or lensing.
