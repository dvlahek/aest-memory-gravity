# GE19 H4 Stage E — valid versioned Y-only source-row implementation freeze

## Final classification and claim boundary

`GE19_H4_STAGEE_Y_SOURCE_ROW_DICTIONARY_IMPLEMENTATION_PASS`.

The preregistered standalone Y-only source module and its deterministic
source test passed, after repairing a first CI **preexecution import**
failure. The original preregistration, physics formulas, source
implementation and selftest gate definitions were not changed
between those attempts.

This is **not** a new parent Z20/q20 reclosure, a full Noether
identity, a H4/Z21 science result or lensing license.

## Frozen implementation and analytic parents

Preregistration:

`ge19/h4_stagee_predata_versioned_y_source_rows.json`

blob `e5ff7d12e963fa7487a1dff42ce06053f4b8d82e`.

Source module:

`ge19/h4_stagee_versioned_y_source_rows.py`

blob `282166ea5840d7fba4dbc328d40d7687afa6fa0f`.

Deterministic selftest:

`ge19/h4_stagee_versioned_y_source_selftest.py`

blob `05bbbb5d2dba2193adcbf468efc81eda6fb71ce6`.

Stage D common-action result:

`docs/ge19_h4_staged_common_y_action_rows_valid_freeze.md`

blob `7d140a608d91a39106c34565cd50e4aa729ec30b`.

Stage D local reproduction freeze:

`docs/ge19_h4_staged_local_analytic_reproduction_freeze.md`

blob `cb41f5633caaebf87924f464d509747ca7a7c4dc`.

## Historical first attempt

Run `35995106055`, commit
`8a405b6c16776016e735eb544214e8b59715f2f7`
stopped before source testing at

`ModuleNotFoundError: No module named 'ge19'`.

Immutable first-attempt classification:

`GE19_H4_STAGEE_FIRST_CI_PREEXECUTION_IMPORT_FAIL`.

Freeze:

`docs/ge19_h4_stagee_first_ci_import_failure_freeze.md`.

The sole fix was to invoke the unchanged selftest from the
repository root as

`python3 -m ge19.h4_stagee_versioned_y_source_selftest`.

No preregistered physics/numerics were changed.

## Valid audit provenance

- workflow:
  `.github/workflows/ge19-h4-stagee-versioned-y-rows.yml`;
- valid workflow commit:
  `512f07757d32229ec3acb289f21f3572ba0cd4c9`;
- run:
  `35995241998`;
- job:
  `107618483762`;
- conclusion:
  `success`;
- terminal marker:
  `GE19_H4_STAGEE_VERSIONED_Y_ROWS_PASS`.

Artifact:

- name: `ge19_h4_stagee_versioned_y_source_rows`;
- artifact ID: `10805856475`;
- JSON file:
  `results/ge19_h4_stagee_y_source_rows.json`;
- JSON bytes: `3371`;
- JSON SHA-256:
  `c3ff4cc18dc8c7a69ba661a68ea3de987818f1b9c1db3275b08f2976c385896e`.

## Frozen numerical source convention

The standalone module returns six GE19 main rows in exact order

`[N, L+R, u, phi, T, rho]`

and two constraint rows

`[shift, anisotropy]`.

Only the u and phi rows are nonzero for this Y-only source
at H3/H4, as derived from the NL0C covariant action.

With

`kappa=2(2-KB)/[(1+beta)a0]`,

`g10=Q u10+phi10_x/a`,

`g11=Q u11+phi11_x/a`,

the physical real-space nonlinear fluxes are

`f20=|g10|g10`,

`f21=2|g10|g11`.

Use the **same** 2/3 Fourier projection `P` on each
real-space flux before evaluating both source rows:

`S_u20=+2 a^3 Q kappa P(f20)`,

`S_phi20=-2 a^2 kappa partial_x P(f20)`,

`S_u21=+2 a^3 Q kappa P(f21)`,

`S_phi21=-2 a^2 kappa partial_x P(f21)`.

The spatial derivative is comoving `partial_x`; the
physical factor `1/a` has already been included in
`a^3(kappa/a)`. No additional division by
`a^3` is inserted.

The flux rule has a continuous directional derivative
at `g10=0` and is not replaced by a global quadratic
`F2` kernel.

## Passed audit controls

For each frozen co-primary `beta={1,0.5,0.1}`:

- finite and compatible inputs and exact source-row layout;
- zero non-Y main rows and zero both Y constraint rows;
- exact zero-set behavior of H4;
- H4 as the eta directional finite difference of H3
  within the preregistered tolerance;
- H3 scalar low-mode comparison against the unchanged
  Repair07 reduced `y2_source_from_reduced`, after the
  exact new `a^3` conversion;
- H4 scalar comparison against the unchanged Repair37
  `dy2_real` source, after the same `a^3` conversion;
- common projected flux and the preregistered 2/3
  high-mode projector;
- invalid coefficient, beta, grid and nonfinite input
  rejection.

The frozen external comparator functions were not patched;
only the selftest's temporary reduced-state adapter was
restored immediately after comparison. No parent solve ran.

## Next licensed work

Preregister the minimum separate corrected H3/Z20
science parent reclosure from this versioned Y source.
Determine the dependent q20 source/bath and time-control
reclosure that is required to remain consistent with the
changed Z20. Reassess reduced Z11 compatibility with the
unchanged eta=0 linear theory, without silently relabelling
historical Repair32B/32C.

Before any corrected science H4/Z21 run, derive/test the
complete all-sector H4 source/Noether compatibility on
a single parent/time representation. Do not restart
isolated GE06 shift-row patches.

The original Repair37 science FAIL and Repair38--44
diagnostics remain immutable. The original active shift
target `1e-6` is unchanged. Z21 remains NOT CERTIFIED
and lensing remains blocked.
