# GE19 Repair44 GE06 shift-row0 versus anisotropy-row1 — implementation lock

## Status and scientific boundary

Repair44 is frozen before its first local execution.
It is diagnostic-only. Repair37 remains immutable science FAIL;
Repair38--Repair43 remain immutable diagnostics. No threshold, H4 source
physics, canonical operator, projected boundary, active mask, finite eta
assumption or observational input is changed.

Repair44 cannot certify Z21 or license lensing.

## Frozen Repair43 parent

Freeze:
`docs/ge19_repair43_valid_ge06_constraint_family_freeze.md`.

Freeze commit:
`91446ddb1987e834200204cb6d8c4f8c4008a5be`.

Freeze blob:
`2d3daec4c6f52d9d53071ee04fd8834825c2ce10`.

Frozen Repair43 classification:
`GE19_REPAIR43_QGE06_MAIN_CONSTRAINT_STAGE_SPLIT_COMPLETE`.

Frozen route:
`QGE06_CONSTRAINT_ROW_FIELD_CLOSER_TO_FULL`.

Frozen SHA-256:

- JSON/FULL:
  `559ae65ffc5d21433799e4e33aa6d91237a9aa41b9799463971bc45dabecae44`;
- NPZ:
  `d5c8c02c7f8272dc390ce9e4d2374a35b2ce1b14da5b60e69dc8366499bfe71c`;
- outer runner:
  `640c9f31959d4e5290a26c64e0dee2ec982866d942135e5261d3828ecc0afc13`.

## Preregistered contract

Preregistration:

`ge19/repair44_predata_qge06_shift_anisotropy_row_split.json`.

Prereg commit:
`3fa98dd405199cbb125c0fcc0f1c00f87b382430`.

Prereg blob:
`85b20ae36482cc343ce756c00970250ea51f1624`.

## Frozen implementation

Implementation:

`ge19/repair44_qge06_shift_anisotropy_row_split.py`.

Implementation commit:
`589859ac041c54e5702bf391e8623002d944a663`.

Implementation blob:
`3c734e55a8ac72874e78bd48b8fdd14112cd321f`.

The code uses only the exact frozen Repair41 direct382/763 GE06
constraint stage values and their saved frozen PCHIP counterparts.
It never interpolates direct target values, rebuilds the H4 sources,
changes projected p0 or changes the original factor-1 Nt128 Radau march.

The seven propagated variants are baseline, direct382/direct763 shift
row0-only, anisotropy row1-only and both constraint rows.

The BOTH correction must reproduce frozen Repair43 CONSTRAINT_ONLY
Z21 and active shift fields before interpretation.

The shift row0 correction does not enter the frozen canonical evolution
or algebraic elimination. Its exact Z21 equality with the baseline is
therefore an implementation gate, not an assumed scientific result.

The script stores all active shift fields, absolute residuals and actual
backward-error denominators and reports complex residual and source
displacement at the preregistered C_max/beta0=1/m8/time-index-3 hotspot.

The route is a preregistered comparison of the two single-row variants
against the full frozen Repair43 constraint-family field at direct382
and direct763, with no new numerical dominance threshold.

## Audits

Static implementation audit:
- run `35965264772`;
- conclusion: static audit was triggered on the implementation commit.
  Dedicated prelock below is the binding implementation audit.

Dedicated prelock:
- workflow commit `78fe09def03d16b2fa65d3bfc667a3b1b35aa463`;
- workflow blob `343354af896c612baf957bfd598b0efaa1150164`;
- run `35965318331`;
- job `107522493691`;
- conclusion `success`.

## Claim boundary

A valid Repair44 result localizes the mixed-source constraint-row response.
It cannot prove an error in GE06 physics, select an interpolant, relabel
previous repairs, certify Z21 or license lensing.
