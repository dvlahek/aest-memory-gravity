# GE19 H4F2a — frozen off-shell GE07 dust spatial Ward subset

Classification: `GE19_H4F2A_DUST_OFFSHELL_WARD_DERIVED`.

This is a source-bound symbolic **subset** of preregistered H4F2,
not a complete mixed H4 source/parent Noether identity and not
a numerical H4/Z21 solve.

Frozen implementation:
`ge19/h4f2a_dust_offshell_ward.py`,
blob `ea347bb1631901efd11929127ca5b485a99dd062`.

Dedicated CI workflow:
`.github/workflows/ge19-h4f2a-dust-ward.yml`,
blob `40c203c8d852e1e0ec0f7b040989edd6743c8c82`.

Valid GitHub Actions run `36019565065`, job
`107700697230`, conclusion `success`, marker
`GE19_H4F2A_DUST_OFFSHELL_WARD_PASS`.
Artifact ID `10815444480`.
JSON `results/ge19_h4f2a_dust_offshell_ward.json`,
SHA-256
`3154412e7e1e337d7efe2797498b56b58b0438c1c6fcd6c03c2629a591437259`.

All frozen source and actual GE07 action bindings and exact
off-shell spatial-covariance gates passed.

## Derived transformation

The frozen minimally coupled dust action is

`L_d=N L R^2 varrho [((T_t-b T_x)/N)^2-(T_x/L)^2-1]`.

For arbitrary `xi(t,x)`, the dust potential T and
multiplier varrho are spatial scalars:
`delta T=xi T_x`,
`delta varrho=xi varrho_x`.
Then W and V are spatial scalars and the entire
dust Lagrangian transforms as a spatial density,

`delta L_d=partial_x(xi L_d)`,

**off shell**; the dust normalization constraint
need not be imposed for this identity.

Treating varrho instead as a weight-one spatial density
gives the exact extra off-shell term
`xi_x L_d`. This is generally nonzero.
It vanishes on the dust constraint shell, so using
an on-shell-only check would conceal the wrong
off-shell transformation.

The formal Ward identity consequently contains
the signed dust parent terms
`E_T T_x+E_varrho varrho_x` under the frozen
Euler sign convention. This does not determine
the complete six-piece H4 source.

NEXT: combine this bound dust result with H4F1
bath covariance and the separately frozen H4F2b
signed mixed-coefficient template. All remaining
actual action-derived H4 source and parent-residual
coefficients must be independently instantiated.

`Z21` remains NOT CERTIFIED; lensing blocked.
