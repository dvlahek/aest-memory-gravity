# GE19 H4F2b — frozen signed mixed spatial Ward coefficient

Classification:
`GE19_H4F2B_SIGNED_MIXED_WARD_TEMPLATE_DERIVED_FULL_SOURCE_OPEN`.

This is an exact symbolic **formal coefficient** of the
full longitudinal spatial Ward identity on homogeneous,
eta-independent FLRW. It is not an instantiated
six-piece action-source identity or H4/Z21 certificate.

Implementation:
`ge19/h4f2b_signed_mixed_ward_template.py`,
blob `ab783ffe8242d8ff455647df8664a074f725ee81`.

Dedicated CI workflow:
`.github/workflows/ge19-h4f2b-signed-mixed-ward.yml`,
blob `de0f346f8580c66dacdf328ce675603e75dd5e92`.

GitHub Actions run `36019774035`, job
`107701407010`, conclusion `success`,
marker
`GE19_H4F2B_SIGNED_MIXED_WARD_TEMPLATE_PASS`.
Artifact ID `10816510514`.
JSON
`results/ge19_h4f2b_signed_mixed_ward_template.json`,
SHA-256
`7168fa81eeceab720d6fdb4e9d3e5ad1d4682fadcfac310ef147a72d182f7ebc`.

All exact symbolic gates passed, including derivative
factor-of-two, both first-order parent residual
products, GE19 isotropic/anisotropy projection
and the original RHS sign.

## Exact signed identity

For Euler residuals `E_i` of
`i=(N,L,R,b,u,phi,T,varrho,q_j)`,
with the scalar-longitudinal field transformations
from the frozen unreduced action, define

`W=sum_i E_i (F_i)_x - d_x(L E_L-b E_b) - d_t E_b=0`.

The actual mixed coefficient is the physical
directional derivative
`W21=d_eta d_epsilon^2 W|epsilon=eta=0`,
**not** an extra factorial-rescaled coefficient.

Under a spatially homogeneous, eta-independent FLRW
background with `F01=E01=0`, its exact symbolic
decomposition is

`W21=sum_i[E_i00 F_i21,x+2 E_i10 F_i11,x+2 E_i11 F_i10,x]-d_x B21-d_t E_b21=0`,

where

`B21=a E_L21+L21 E_L00+2 L10 E_L11+2 L11 E_L10-b21 E_b00-2 b10 E_b11-2 b11 E_b10`.

Every displayed parent residual is retained
off shell. The bath sum over nodes and dust
multiplier must be included in the full
action-derived instantiation.

The independent GE19 row projection is

`E_L=(E_iso+2 E_aniso)/3`.

With every displayed background/H1/Z11 Euler
residual set to zero, the conditional identity is

`-d_t E_b21-d_x(a E_L21)=0`.

If `E21=L21-S21` uses the unchanged
`LZ=-E_inhom` RHS convention, the source
contribution has the exact **plus** signs

`d_t S_b+(a/3)d_x(S_iso+2 S_aniso)`.

This alone is **not** an assertion that the
source term vanishes. That additionally
requires the *actual full action-derived*
six-piece nonlinear source and the linear
operator to obey the same Ward identity
under all stated parent on-shell and
regularity assumptions.

There is no independent direct `E20` product
in this formal mixed coefficient because the
background has no eta tangent; the corrected
H3F Z20/H3G q20 fields still enter `E21`
through its actual nonlinear source functional.
The eta-rescaled bath convention must be
handled separately at the action level.

## Open license

The real six H4 source pieces have NOT been
instantiated in the signed identity. The
corrected H3F/H3G parents have NOT been
evaluated on a common time representation.
No FD4/FD8 discrete Ward identity or
H4/Z21 solve was carried out.

NEXT: preregister and instantiate all six
source-row families and the exact associated
parent-residual/boundary dictionary. Do not
promote this formal template to full H4F2 PASS.

Z21 NOT CERTIFIED; lensing blocked.
