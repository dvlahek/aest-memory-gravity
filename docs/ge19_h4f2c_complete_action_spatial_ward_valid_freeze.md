# GE19 H4F2c — complete reduced action spatial covariance freeze

Classification:
`GE19_H4F2C_COMPLETE_REDUCED_ACTION_COVARIANCE_DERIVED_SIX_SOURCE_OPEN`.

The actual frozen GE06, GE07, GE05, Lambda and NL0C Y
action conventions and all earlier source-bound
Stage B/H4F1/H4F2a/H4F2b proofs were pinned
before this exact symbolic subset. This result
does not instantiate six mixed H4 source rows
or run a corrected-parent common-grid test.

## Provenance

- implementation:
  `ge19/h4f2c_complete_reduced_action_spatial_covariance.py`,
  blob `998e871c2398262c28442d0054b869d6ebdacfb4`;
- dedicated workflow:
  `.github/workflows/ge19-h4f2c-reduced-action-spatial-ward.yml`;
- successful run `36025455158`, job `107720721037`;
- marker `GE19_H4F2C_COMPLETE_REDUCED_ACTION_WARD_PASS`;
- artifact ID `10818368862`;
- JSON
  `results/ge19_h4f2c_complete_reduced_action_spatial_covariance.json`;
- JSON SHA-256
  `3fbee288b3cbd062b5b0a255712266f07b332a093c3bf47ef7a1455856bd121a`.

All source-file blob controls, actual-action text
bindings and exact density transformation gates pass.

## Derived action-level statement

For arbitrary infinitesimal spatial relabeling
`xi(t,x)`, the following frozen *reduced*
action densities each transform as
`delta L=partial_x(xi L)`:

- GE06 canonical Einstein ADM kinetic sector;
- GE06 plane integrated spatial-curvature
  terms `2 N R_x^2/L+4 N_x R R_x/L`;
- analytic AeST `KB E^2+2 C E X-C X^2+2 K(Q)`;
- NL0C nonanalytic `-C J(Y)` for
  both strict-sign branches of `|X|^3`,
  continuously at the zero-gradient set;
- GE07 dust with the correctly transforming
  scalar Lagrange multiplier varrho;
- each NL0B/GE05 longitudinal bath node
  `NLR^2[A(q)^2-(omega q-sqrt(w)X)^2]/4`;
- frozen `-6 rho_lambda NLR^2` Lambda density.

In the plane GR curvature term, `N_x`
and `R_x` transform as gradients of
spatial scalars; each complete curvature
term has weight one. The symbolic test
does not substitute spherical
`+2NL` into the plane action.

The independently pinned Stage D relative
Y-to-GE06 action factor is one. The
GE05-to-GE06 Euler-row factor two remains
a separate frozen residual normalization,
not an arbitrary action-sector fit.

Combined with H4F2b, this establishes the
*formal off-shell reduced spatial Ward
identity* for the sum of these action
sectors. It does **not** demonstrate that
the separately implemented GE19 H4 source
and its FD4/FD8 time derivatives represent
the exact mixed Euler coefficient on the
same corrected H3F/H3G parent.

## Exact remaining gate

Instantiate all **six** actual H4 mixed
source families with exact signed row
normalizations and the complete parent
Euler residuals, including the actual
frozen GE05 M1/M2 mappings, Y u+phi
Stage E source, Lambda and dust.
The signed H4F2b formal coefficient
must then be independently evaluated
on the common corrected-parent/time
representation. The original active
shift target remains 1e-6.

M1's frozen implementation uses only
`B20=X20-weighted_z20`, so the certified
H3G weighted projection is sufficient
for the **implemented M1 source**.
Bath node states are still required for
a complete off-shell bath-parent proof
and M2's first-order node evolution,
and must be rebuilt from the frozen
R1/GE05 equations where applicable.

No H4/Z21 state solve was carried out.
`Z21` remains NOT CERTIFIED and
lensing blocked.
