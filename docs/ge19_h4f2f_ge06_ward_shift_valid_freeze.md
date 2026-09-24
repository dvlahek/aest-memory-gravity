# GE19 H4F2f — valid frozen GE06 coframe Ward and independent shift mixed-source subset

## Classification and precise scope

`GE19_H4F2F_GE06_SPATIAL_WARD_SHIFT_SOURCE_SUBSET_PASS`.

The dedicated GitHub Actions execution has completed with a
successful outcome. Frozen GE06 Einstein/analytic AeST
plane-symmetric coframe invariants and action density obey
the exact reduced spatial Ward transformation. Both actual
independent-shift action partials `b_f` and `b_x`
satisfy the exact mixed physical epsilon²/eta coefficient,
half-gradient polarization, reversed-direction symmetry,
and original GE19 `-2 Q_cross` RHS convention.
The actual frozen generator's numeric source controls pass.

This is **GE06 action and independent shift-source subset
only**. It does not certify the six-piece all-sector
H4 source/parent Noether identity, corrected H3F/H3G
common-grid H4 source assembly, Z21 or lensing.

## Exact frozen inputs and successful CI

- preregistration:
  `ge19/h4f2f_predata_ge06_shift_ward_mixed_source.json`,
  blob `551294c5763b086919c9f27076a922c29ca953e5`;
- valid implementation:
  `ge19/h4f2f_ge06_shift_ward_mixed_source_audit.py`,
  blob `49e7546e5ccb76d27436486f8baddd2a4d17956e`;
- valid workflow:
  `.github/workflows/ge19-h4f2f-ge06-ward-shift.yml`,
  blob `17415c334d93d1e46374eca02eb9beb9e184bc11`;
- successful execution commit:
  `5f5d14d332b6d1da4b86d95d53ec4767df0029ad`;
- run: `36037212512`;
- job: `107760180126`;
- conclusion: `success`;
- terminal marker:
  `GE19_H4F2F_GE06_SHIFT_ACTION_SUBSET_PASS`;
- artifact ID: `10825093346`;
- JSON:
  `results/ge19_h4f2f_ge06_shift_ward_mixed_source.json`;
- JSON bytes: `4200`;
- JSON SHA-256:
  `b6aca9808ae36eaebea2356c0f3443e571e6ede8a4c0436be7cd80bf2bc3eb40`.

The JSON's `all_subset_gates_pass` is true. All
frozen source blobs, ten explicit unreduced
coframe-jet/Ward geometry gates, GE06 source
action bindings and both independent-shift
symbolic gates are true.

Actual frozen-generator direct/polarized numeric
source errors:

- `b_f`: relative L2 `0.0`;
- `b_x`: relative L2
  `1.6592729300491167e-16`.

Both pass the original `1e-9` source-only
numerical threshold, without fitting or
threshold adjustment.

## Historical failed CI provenance (immutable)

The first run `36030973726` failed at a
half/full epsilon²/eta source gate defined
incorrectly in the *audit*, not in the
frozen GE06 action. Its original result
is frozen in
`docs/ge19_h4f2f_first_ci_half_derivative_gate_failure_freeze.md`.

An intermediate `36031713914` stopped at
its old code-blob lock before source execution.

Run `36031753394` had every named exact
symbolic and numerical gate true but used
the invalid aggregate
`all(all(g.values()) for g in numeric.values())`.
The legitimate `b_f=0.0` numerical error
converted to Boolean `False`.
Its raw FAIL and 4195-byte JSON are frozen in
`docs/ge19_h4f2f_second_ci_numeric_truthiness_failure_freeze.md`.

The corrected source-audit script in
`36036837437` generated the valid 4200-byte
PASS JSON with the exact same SHA-256 as
the ultimately successful run; the workflow
itself repeated the old zero-error Boolean
aggregation in its post-audit assertion.
Its failing workflow outcome and valid
script result are frozen separately in
`docs/ge19_h4f2f_third_ci_workflow_numeric_truthiness_failure_freeze.md`.

The successful `36037212512` workflow
fixes **only** that post-audit numeric
assertion, checking named Boolean gates
separately from actual relative L2 values
against the unchanged threshold.
The frozen preregistration, physical
source equations, actual GE06/GE07/GE05
generators and legacy science results
remain untouched.

## Next necessary H4 work

Combine H4F2a–f's validated restricted
action-source subsets into one **separately
preregistered, complete signed all-sector
mixed H4 Ward/source-parent dictionary**
with the actual GE06, GE07, Lambda,
Stage E Y, GE05 M1 and GE05 M2 all-row
contributions, complete bath/dust parent
Euler residuals and corrected H3F/H3G,
H1 and Z11 parents.

The formal H4F2b Ward template cannot be
declared zero from separate partial
source identities. Its complete signed
parent-equation and boundary terms must
be explicitly checked on the common
corrected parent/time representation
before any new H4/Z21 state solve.

Original Repair37 remains historical
science FAIL, Repair38–44 diagnostics
remain immutable and the original active
shift threshold remains `1e-6`.
**Z21 NOT CERTIFIED; lensing blocked.**
