# GE19 Repair21 on-shell H1 parent + matched-shift audit lock

## Status

**DIAGNOSTIC IMPLEMENTATION LOCKED BEFORE REPAIR21 LOCAL RESULT**

Repair20 remains frozen with route

`ACTIVE_SHIFT_PROPAGATION_ISSUE_REMAINS`.

Repair21 is diagnostic only. It does not relabel Repair19/20 and does not certify Z20.

## Parent Repair20 freeze

Commit:

`317b4219f6630b0c1f0f15081e8db62e6470a47c`

File:

`docs/ge19_repair20_shift_time_resolution_result_freeze.md`

Blob:

`34ee88238837e5b661d7f633b6df6df2e6c3662a`

Frozen Repair20 JSON/NPZ:

- JSON SHA-256 `5f1dc8e48963c6403f142958c8ce34ab1457953b47868d1a65317655cd0644eb`;
- NPZ SHA-256 `99937112b889bc556ada756bc7b4e834991a6019596fdbc353a40294ad3968a6`.

## Repair21 preregistration

Commit:

`434dc92f0f59e34d84ca730ea041edecb004271c`

File:

`ge19/repair21_predata_on_shell_h1_parent_matched_shift_audit.json`

Blob:

`2d1925a043348422693e0e66edb5a73e5e9daebc`

## Repair21 implementation

Commit:

`9d75bd9a457a2d54089286e3fc6ff5a3c84a3aa0`

File:

`ge19/repair21_on_shell_h1_parent_matched_shift_audit.py`

Blob:

`73e7fa0f5b3a58f0462308bf11d2a53b7616abfb`

## Frozen scientific question

Repair20 used separately PCHIP-interpolated frozen Repair13 Nt64 arrays for

- Z10;
- Z10dot

on Nt128.

That construction reproduces the original Nt64 nodes but does not guarantee that inserted Nt128 midpoint values satisfy the exact first-order canonical equations and Noether identities.

Repair21 asks if the unresolved active H3 shift defect persists when the H1 parent is solved **on shell** independently at Nt64 and Nt128.

## Frozen H1 parent construction

For Nt64 and Nt128:

- same Repair13 self-consistent reduced AeST+dust+Lambda background;
- same GE15/GE18 reference first-order initial data;
- same Repair11 Lambda c1 operator;
- same Repair07 `solve_reduced_h1_case_canonical`;
- no PCHIP H1 parent in the main science path.

Nt64 must reproduce the frozen Repair13 Nt64 H1 state and derivative.

The old Repair20 PCHIP parent is retained only as an explicit counterfactual diagnostic.

## Frozen H1 gates

- Nt64 Z10 reproduction <= `1e-12`;
- Nt64 Z10dot reproduction <= `1e-12`;
- H1 linear residual <= `1e-8`;
- H1 shift <= `1e-6`;
- H1 anisotropy <= `1e-6`;
- H1 initial dynamic match <= `1e-10`;
- H1 Nt64/Nt128 state relative L2 <= `5e-3`;
- finite outputs.

## Frozen H3 construction

On the new on-shell H1 parents:

- same Repair14 GE06+GE07+Lambda c2+Y2 source;
- same Repair18 q0=0 projected-p0 boundary;
- same Repair07 two-stage Radau IIA canonical march;
- same original shift metric;
- same original `1e-6` shift threshold;
- same linear/aniso thresholds.

No source formula, sign, component order, normalization or boundary rule changes.

## Frozen matched-grid diagnostic

Common comparison grid:

`Nt128 ln(a)`.

For each fixed C,beta,m:

- PCHIP-interpolate the Nt64 shift metric to the Nt128 x-grid;
- define active/near-null mask only from the Nt128 on-shell natural shift scale;
- evaluate both Nt64-interpolated and Nt128 metrics on that identical active mask.

Report:

- matched active Linf at Nt64 and Nt128;
- matched active RMS/L2 at Nt64 and Nt128;
- observed orders
  `log(e64/e128)/log(h64/h128)`;
- Nt128 near-null absolute residual / S_ref;
- worst Nt128 active sample.

This removes the Repair20 defect in which different global worst samples were used at each resolution.

## Frozen diagnostic gates

Positive routing additionally requires:

- Nt128 active Linf <= `1e-6`;
- matched active Linf order >= `2.5`;
- matched active L2 order >= `2.5`;
- Nt64/Nt128 H3 state relative L2 <= `5e-3`;
- H3 linear residual <= `1e-8`;
- H3 anisotropy <= `1e-6`;
- Repair18 boundary p0 reproduction <= `1e-12`;
- Nt128 near-null abs residual / S_ref <= `1000 eps`;
- finite outputs.

## Frozen routing

Only:

- `INTERPOLATED_H1_PARENT_DEFECT_CONFIRMED`;
- `ACTIVE_SHIFT_ISSUE_PERSISTS_ON_ON_SHELL_PARENT`;
- `IMPLEMENTATION_FAIL`.

Even positive routing does not certify Z20 and does not relabel Repair19/20.

## Prelock history

Initial dedicated prelock run:

`35633948401`

conclusion:

`failure`.

The failure was audit-only: the workflow contained an incorrect expected Repair13 source-file blob hash.

No Repair21 science code, preregistered formula, gate or routing changed.

Audit-only provenance fix commit:

`9a23dedaad79887b0f1626541031e0b650743197`.

Final dedicated prelock run:

`35634051163`

job:

`106446967082`

conclusion:

`success`.

Terminal marker:

`GE19_REPAIR21_PRELOCK_AUDIT_PASS`.

Synthetic matched-grid order:

`3.0`.

Frozen source blobs reproduced:

- Repair07: `e34d28a2062c748f48bc82fa928844b02631de25`;
- Repair13: `362d63d03d7b850fceae393f535353ded79aeea7`;
- Repair14: `06c5ced952c2370cfa4aaadb6ef8f72d2d7221de`;
- Repair18: `c7b3a5c689bd78a65a8150c26e1fbfae108cb580`.

## Stop rule

No Z20 certification.

No q20, H4 or Z21.

No shift threshold relaxation.

No observational bridge.

## Claim boundary

Repair21 may determine if the Repair20 unresolved active shift residual is an off-shell H1-parent interpolation artifact. It does not change the physical model or any historical science classification.
