# GE19 Repair15 H3 initial shift/Noether compatibility audit lock

## Status

**DIAGNOSTIC IMPLEMENTATION LOCKED BEFORE REPAIR15 LOCAL RESULT**

Repair14 remains frozen as

`GE19_REPAIR14_SELF_CONSISTENT_REDUCED_H3_Z20_PARTICULAR_FAIL`.

Repair15 is diagnostic only and does not relabel Repair14 or certify Z20.

## Parent Repair14 freeze

Commit:

`7ba8b312f7dd8ca7035958be2abdf03df98a5bae`

File:

`docs/ge19_repair14_h3_z20_result_freeze.md`

Blob:

`58980049061a2a3161b56d00c734ee9fcd89c123`

Frozen Repair14 JSON:

- SHA-256 `741da95a0aaffa31e27f2b05d42b8a7f011574013de8639812e453d7b130fe57`
- bytes `697196`.

Frozen Repair14 NPZ:

- SHA-256 `b72626bd45b02b537d21f035fc8c746eb06eee669869c4aea921861328303c42`
- bytes `9467673`.

## Repair15 preregistration

Commit:

`576eca2dce3632037704f6c5f13f2c99a14ac87b`

File:

`ge19/repair15_predata_h3_initial_shift_noether_compatibility_audit.json`

Blob:

`eca7c1c6ac9a512b843753d78da41547ea88f112`

## Repair15 implementation

Commit:

`f3713fe784922d8def78ba1b7e8dc0bd7dc47d01`

File:

`ge19/repair15_h3_initial_shift_noether_compatibility_audit.py`

Blob:

`c366894df6642df07abd9e0b9b53d98f7181aee0`

The diagnostic:

- reconstructs the frozen Repair14 H3 source from the certified Repair13 Z10 parent;
- does not recompute H1;
- does not recompute a Z20 trajectory;
- retains the Repair13 reduced background and Repair14 Lambda c2 source;
- evaluates only the z=1.5 algebraic initial surface;
- keeps S20=u20=phi20=T20=0 and their cosmic-time derivatives zero;
- treats N20 and delta_varrho20 as the only algebraic unknowns.

## Initial compatibility system

The three tested equations are:

- lapse;
- dust density;
- shift.

For fixed zero dynamic values/derivatives they form a row-scaled 3x2 system for

`(N20, delta_varrho20)`.

Repair15 reports:

- current Repair14 lapse+density initialization and its independent shift residual;
- density+shift solve and independent lapse residual;
- lapse+shift solve and independent density residual;
- row-scaled 3x2 least-squares residual;
- left-null compatibility residual;
- coefficient and augmented ranks;
- singular values;
- anisotropy as an independent diagnostic.

The test is repeated over:

- C_min,C_star,C_max;
- beta0=1,0.5,0.1;
- m=1..40;
- Nt=64 and Nt=32 frozen Repair13 backgrounds.

## Frozen diagnostic threshold

Compatibility threshold:

`1e-6`.

Material-source floor relative to the global initial target maximum:

`1e-12`.

No Stage-B science threshold is changed.

## Frozen routing

Repair15 may return:

- `INITIAL_SOURCE_INCOMPATIBILITY`;
- `CURRENT_INITIAL_PARTITION_ONLY`;
- `INITIAL_SURFACE_CLOSE_PROPAGATION_DEFECT_REMAINS`;
- implementation-no-material-cases failure if applicable.

## Executable prelock audit

Workflow:

`.github/workflows/ge19-repair15-prelock-audit.yml`

Workflow blob:

`953ca958a67289bcca7dee9d1aa9b69da40f20b5`

GitHub Actions run:

`35600834919`

Job:

`106336279448`

Conclusion:

`success`

Terminal marker:

`GE19_REPAIR15_PRELOCK_AUDIT_PASS`

Synthetic compatible 3x2 control:

- least-squares residual `7.166458808248762e-16`;
- left-null residual `3.5254315917032006e-16`.

Synthetic incompatible 3x2 control:

- least-squares residual `0.18898223650461365`;
- left-null residual `0.18898223650461402`.

The prelock statically verifies that Repair15 does not invoke:

- `solve_case_canonical`;
- `_radau2_integrate_canonical`;
- `solve_reduced_h1_case_canonical`.

## Stop rule

Repair15 is attribution only.

No q20 and no H4/Z21 construction is licensed by this audit alone.

Any subsequent repair must be preregistered after the Repair15 result is frozen.

## Claim boundary

Repair15 can identify if the Repair14 failure is already an initial-surface second-order source/constraint incompatibility, a current initial-partition issue, or a propagation defect.

It cannot certify Z20 or nonlinear memory propagation.
