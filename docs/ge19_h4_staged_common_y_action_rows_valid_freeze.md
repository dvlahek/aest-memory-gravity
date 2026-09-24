# GE19 H4 structural Stage D — common GR-normalized Y action and complete Y-only source rows

## Classification

`GE19_H4_STAGED_COMMON_GR_NORMALIZATION_AND_Y_ROWS_DERIVED`.

This is a valid action-level analytic result, not a numerical H3/H4/Z21
solve and not a complete all-sector H4 Noether certificate.

The Stage C local audit was reproduced byte-identically and frozen in
`docs/ge19_h4_stagec_local_analytic_reproduction_freeze.md`.

## Immutable inputs and execution

Predata:
`ge19/h4_structural_stage_d_predata_global_y_normalization.json`,
blob `764d064c76d44bc597ab6c4f96044ba2a90433a5`.

Implementation:
`ge19/h4_structural_stage_d_common_action_y_rows.py`,
blob `162357ce845a93982b46aef7d839a7171964b47e`.

Successful dedicated GitHub Actions audit:

- workflow: `.github/workflows/ge19-h4-staged-common-y-action.yml`;
- run: `35984187949`;
- job: `107582874421`;
- conclusion: `success`;
- terminal marker: `GE19_H4_STAGED_COMMON_Y_ACTION_AUDIT_PASS`;
- artifact name: `ge19_h4_staged_common_y_action_rows`;
- artifact ID: `10800569833`;
- JSON file:
  `results/ge19_h4_staged_common_y_action_rows.json`;
- JSON bytes: `4876`;
- JSON SHA-256:
  `2d900249d1e030a9b11b2b3d3e4b65ada8cbfb39a119b40ac0aba3ce10380d11`.

All pinned-source and exact symbolic action, GR, Y-row and eta-tangent
gates passed. No fitted coefficient or new theory choice was introduced.

## Independent common-action normalization

The frozen NL0C covariant action specifies the Y sector with the
common Einstein-Hilbert prefactor:

`S_J = -1/(16 pi Gtilde) integral sqrt(-g) (2-KB) J(Y)`.

The frozen NL1C6 complete ungauged spherical action contains

`N L R^2[KB E^2+2 C E X-C X^2+2 K(Q)-C J(Y)]`

inside the same `lag=grav+aest+mem` sum, with `C=2-KB`.

The frozen GE06 plane-symmetric memory-off action contains the same
analytic AeST bracket with `-C J(Y)` omitted, in the
single `lag=grav+aest` sum.

Under exact invariant naming, the AeST action difference is
precisely

`L_NL1C6,AeST - L_GE06,AeST = -N L R^2 C J(Y)`.

The spherical GR source differs from plane GE06 GR only by the
expected unit-sphere curvature term `+2 N L`. Both GR kinetic
actions have exactly the canonical Einstein-Hilbert ADM combination

`K_ij K^ij-K^2 = -4 kL kR-2 kR^2`.

Therefore the NL0C Y sector and GE06 GR+analytic AeST sector use
the same GR-normalized action convention: the extra relative
NL0C-to-GE06 raw action factor is **1**.

This conclusion is grounded in the common frozen action and
canonical EH term, not fitted to Repair37 source residuals.

## Derived Y-only Euler/source dictionary

On the frozen zero-gradient FLRW background define

`g = Q u10 + phi10_x/a`,
`kappa = 2(2-KB)/[(1+beta)a0]`.

The directional branch is `epsilon -> 0+`. The continuous
nonanalytic flux is `|g|g`, with directional derivative
`D(|g|g)[h]=2|g|h`, including `g=0`.

At H3 (second physical epsilon derivative), the exact raw
action-density Euler Y rows are

`E_phi,Y^(20) = 2 a^3 (kappa/a) partial_x(|g|g)`,

`E_u,Y^(20) = -2 a^3 Q kappa |g|g`.

Their corresponding compatible GE19 RHS contributions, with
the unchanged `L Z20 = -E^(20)` convention, are

`S_phi,Y^(20) = -2 a^3 (kappa/a) partial_x(|g|g)`,

`S_u,Y^(20) = +2 a^3 Q kappa |g|g`.

The original frozen H3 source inserts
`S_phi,Y^(20)=-2 y2_code`, with
`y2_code=(kappa/a)partial_x(|g|g)`, and has no Y aether
row. It thus differs from the common raw variational dictionary
in both its volume factor and source-row coverage.

For the mixed H4 eta-tangent, with background Q and beta unchanged
under eta at eta=0, let
`g10=Q u10+phi10_x/a` and
`g11=Q u11+phi11_x/a`. Then the exact
Y-only raw RHS coefficients are

`S_phi,Y^(21) = -4 a^3 (kappa/a) partial_x(|g10|g11)`,

`S_u,Y^(21) = +4 a^3 Q kappa |g10|g11`.

The original H4 `2DY2` source inserts only scalar
`-2 dy2_code` and does not include these full raw
action-density rows.

At this perturbative order, the Y-sector metric and independent
shift source rows vanish. The independent GE06 shift-constraint
problem in Repair37--44 is not therefore resolved by declaring
a direct new Y shift source.

## Claim and integration boundary

This audit settles the common relative action prefactor and
derives the **Y-sector-only** source rows. It does not derive the
complete H4 Noether identity including GE05 memory, GE07 dust,
GE06 analytic nonlinearities, Lambda and all on-shell parent
residual terms. It does not imply that the corrected parent state
will meet the original 1e-6 shift gate.

Do not edit or relabel historical H3, Repair22/27/32, Repair37
or Repair38--44 outputs. The previous certifications are for
their preregistered implemented equations.

Next licensed step: freeze a separately versioned, independently
testable *complete Y scalar+aether source dictionary*, then
preregister a new H3 Z20 parent reclosure and dependent q20 controls
as required. Preserve unchanged H2 Z11 conventions and assess
their compatibility independently before the new H4 solve.
Only after parent and full-source structural gates pass may
a separately preregistered science H4/Z21 reclosure proceed.

Window-local particular Z21 remains NOT CERTIFIED.
Lensing remains blocked.
