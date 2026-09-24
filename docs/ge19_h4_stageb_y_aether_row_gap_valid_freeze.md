# GE19 H4 Stage B — frozen NL0C Y-sector variational source-row coverage gap

## Valid analytic classification

`GE19_H4_STAGEB_Y_AETHER_SOURCE_ROW_COVERAGE_GAP_CONFIRMED`.

This is an analytic action-to-implementation audit of the
**already frozen** NL0C and GE19 theory choices. It does not
change the model, add fitted source terms, perform an H4/Z21
numerical solve or retrospectively relabel historical science
artifacts.

Preregistration:

- file: `ge19/h4_structural_stage_b_y_variational_row_predata.json`;
- blob: `bb325a7b77be1b87b8d53c9f1462db479e36903d`.

Implementation:

- file: `ge19/h4_structural_stage_b_y_variational_row_audit.py`;
- blob: `a3a0973e973f552fabb40a3dff9dd612d47ed01a`.

GitHub Actions:

- run: `35980659010`;
- job: `107571474311`;
- conclusion: success;
- terminal marker:
  `GE19_H4_STAGEB_Y_VARIATIONAL_SOURCE_ROW_AUDIT_PASS`.

Successful frozen artifact:

- name: `ge19_h4_stageb_y_source_row_audit`;
- artifact ID: `10799504910`;
- JSON filename:
  `results/ge19_h4_stageb_y_variational_row_audit.json`;
- JSON SHA-256:
  `6f20168f0fff685d697ce5a981754513a5c8733067c22ffbbf55f2e904c1ac46`;
- JSON bytes: 6018.

All exact symbolic and pinned-source coverage gates passed.

## Action-derived finding

The frozen NL0C small-gradient action has a term proportional to

`L_Y = -lambda N L R^2 c_beta |X|^3`,

where `lambda=2-K_B`,
`c_beta=2/[3(1+beta)a0]`, and

`X = sinh(u)(phi_t-b phi_x)/N + cosh(u) phi_x/L`.

The frozen FLRW perturbation direction is

`g = Q u_1 + phi_{1,x}/a`,

with `X=epsilon g+O(epsilon^2)`.

The exact raw reduced action-density Euler coefficient for the
aether rapidity obeys, for `epsilon -> 0+`,

`E_u^(20) = -6 lambda c_beta a^3 Q |g|g`.

At the H4 eta-tangent level,

`E_u^(21,Y) = -12 lambda c_beta a^3 Q |g10|g11`,

where `g11=Q u11+phi11_x/a` and the notation denotes
the mixed second epsilon / first eta derivative of the Y-sector
residual, *before* applying the H4 RHS sign.

Both expressions are generically nonzero when Q and the
physical first-order gradient are nonzero.

The corresponding action-density scalar Euler **spatial flux**
coefficients are

`F_phi^(20) = +6 lambda c_beta a^2 |g|g`,

`F_phi^(21,Y) = +12 lambda c_beta a^2 |g10|g11`.

Here the scalar Euler residual includes `partial_x F_phi`.
The exact identity

`E_u^(2,Y) + a Q F_phi^(2,Y) = 0`

holds for the homogeneous FLRW factors in the reduced
longitudinal convention, including the eta-tangent coefficient.
The flux is continuous at `g=0` and its directional derivative
is `2|g|g11`, with zero value at the zero set.

All second-directional metric Y source coefficients vanish at
this perturbative order. This does **not** imply the aether
coefficient vanishes.

## Frozen H3/H4 source-row comparison

The frozen GE06 analytic generator explicitly excludes the
nonanalytic Y branch.

In the frozen H3 source constructor
`ge19/repair07_window_retarded_reduced_h3_z20_particular.py`:

`rhs[3] += -2.0*y`

with `ypiece[3]=-2.0*y`; there is no Y-dependent
`rhs[2]` or `ypiece[2]` contribution. Both the
reduced-H1 and alternate H3 source constructors have this
same scalar-only assignment.

In the frozen H4 source constructor
`ge19/repair37_cancellation_safe_fd8_h4_z21_reclosure.py`:

`main[3]=-2.0*fm`

for `2DY2`, with `main[2]` untouched and both
constraint rows set to zero.

The six-piece Repair37 source dictionary does not contain a
separate explicit Y aether piece.

**Therefore the explicit GE19 H3/H4 Y source rows do not
cover the nonzero aether Euler variation of the frozen
covariant Y action.**

This is a source-row coverage result, not an assertion that
the full H4 Noether identity was derived or tested.

## Important normalization boundary

The coefficient above is the **raw reduced
action-density Euler residual**. The historical
`y2_source` routine labels its returned scalar quantity a
physical-space divergence. Mapping the action-density
scalar flux to the raw GE06/GE19 scalar row requires an
independent measure and convention audit, including the
frozen GE06-to-GE05 factor-two dictionary.

Do not inject the formula above directly into a frozen
numerical source or choose its coefficient to reduce the
Repair37 shift residual.

## Consequences and next licensed action

- The previous Repair22 Z20 and Repair32B/32C reduced Z11
  certifications remain **unchanged as results of their
  preregistered implemented equations**. They must not be
  silently promoted to certifications of the complete
  variational NL0C H3/H4 system until its source dictionary
  is reconciled with the frozen action.
- Repair37 remains the immutable historical science FAIL.
- Repair38--Repair44 remain diagnostic-only.
- Do **not** run another interpolator/GE06 shift-row patch.

The next work is a separately pinned analytical
**action-density-to-GE19 source convention audit** for
both Y aether and scalar rows. It must explicitly determine
the volume factors and H3/H4 factor-two convention from the
frozen GE06 action and assembly. Then the full H4 Ward
identity can be revisited with an unambiguous, separately
versioned all-row source dictionary.

No H4/Z21 science reclosure or lensing is licensed.
