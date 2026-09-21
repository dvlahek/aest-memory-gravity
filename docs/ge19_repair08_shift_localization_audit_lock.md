# GE19 Repair08 shift-localization audit implementation lock

## Status

**DIAGNOSTIC IMPLEMENTATION LOCKED BEFORE REPAIR08 RESULT**

Repair07 remains historically frozen as

`GE19_REPAIR07_WINDOW_RETARDED_REDUCED_H3_Z20_PARTICULAR_FAIL`.

## Parent Repair07 freeze

Commit:

`8295046a26979b4045a39b8010f892d100d7a7c5`

File:

`docs/ge19_repair07_reduced_h1_result_freeze.md`

Blob:

`8146ba26f0d147ba62315faaf5fb03156564d738`

Frozen Repair07 science JSON SHA-256:

`f27d31b637332bd043ebabdcc47a18e1126f05065aea2cca794ac8e0f2b2e894`.

## Repair08 preregistration

Commit:

`30b2672dd26ae164cd5a3363c5f12f5936e4545a`

File:

`ge19/repair08_predata_shift_constraint_localization_audit.json`

Blob:

`7f584923203d371c344d9d6825a2f925069f6a28`

## Diagnostic implementation

Implementation commit:

`9c481e42f09e810afbf551ee8a8450c05da581fd`

File:

`ge19/repair08_shift_constraint_localization_audit.py`

Blob:

`6bf737ff455e54295dc099df933b99e1f1a64141`

The implementation is diagnostic only.

It does not modify Repair07, GE06, GE07, GE15, GE18, the DAE partition, Radau, any sign, any threshold, the background, C values, or the Stage-A/Stage-B science logic.

## Executable prelock audit

Workflow:

`.github/workflows/ge19-repair08-prelock-audit.yml`

Blob:

`2b8a83fa17fdc1018dd1fb8105e151fa6c500705`

Run:

`35562966270`

Job:

`106219192505`

Conclusion:

`success`

Markers:

- `GE19_REPAIR08_PRELOCK_AUDIT_PASS`
- `GE19_REPAIR08_PREREG_AUDIT_PASS`

The audit derives directly from the frozen GE07 action:

`GE07_LINEAR_SHIFT = -2*aa**3*dTx*rhob`

and therefore the equivalent full-standard CLASS momentum contribution is

`FULL_STANDARD_EQUIVALENT_SHIFT = -6*I*aa**4*mom/k`.

No sign or normalization in that comparison is manually tuned after seeing Repair08 data.

## Frozen diagnostic questions

Repair08 must report, for every C case and each frozen first-order mode:

1. the shift residual on the prescribed initial surface before propagation;
2. the shift residual of the frozen mixed GE15+GE18 reduced-dust reference across the window;
3. the shift residual of the internally evolved Repair07 canonical state across the window;
4. the cancellation of the GE15 gravitational+AeST shift piece against the exact full-standard CLASS momentum contribution;
5. hypothetical T/matter-sign and AeST scalar-phi sign flips, diagnostics only;
6. the first redshift at which the canonical trajectory crosses the unchanged `1e-6` shift gate.

## Interpretation

If the initial surface already fails, the next repair must target a mapping/constraint compatibility issue.

If the initial surface passes and the trajectory later fails, the next repair must target propagation/background consistency, not the initial GE15/GE18 sign convention.

If the full-standard CLASS momentum cancels the GE15 gravitational+AeST piece but the reduced-dust bridge does not, the defect is localized to the reduced-matter/background replacement rather than GE06.

No H3/Z20 construction is permitted by Repair08.
