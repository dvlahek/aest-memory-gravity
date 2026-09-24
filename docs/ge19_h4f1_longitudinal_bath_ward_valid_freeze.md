# GE19 H4F1 — exact longitudinal bath covector spatial Ward result

## Classification and strictly limited scope

`GE19_H4F1_LONGITUDINAL_BATH_WARD_COVARIANCE_DERIVED`.

This is a valid **restricted analytic** spatial-diffeomorphism
result for the frozen NL0B/NL1C3B scalar-longitudinal memory
reduction. It supplies a previously open transformation
obligation to the eventual complete H4 Ward/Noether audit.

It is **not** the full mixed H4 source/parent residual identity,
a common-grid H4 source compatibility test, a numerical Z21
reclosure or a lensing result. The original Repair37 science
FAIL and Repair38--44 diagnostics remain unchanged.

## Frozen inputs and successful execution

Preregistration:
`ge19/h4f1_predata_longitudinal_bath_spatial_ward.json`,
blob `7f26852707ba5b722adf0c934003b2cc5cccb24b`.

Analytic implementation:
`ge19/h4f1_longitudinal_bath_spatial_ward_audit.py`,
blob `a3f0b8e2d466a6421b9292ea841e0508854fe023`.

Dedicated GitHub Actions workflow:
`.github/workflows/ge19-h4f1-bath-spatial-ward.yml`,
blob `36b68f837e6e45cb4eb13963f7e2340c77343ffe`.

Valid execution:
- run `36017517915`;
- job `107693741610`;
- conclusion `success`;
- marker `GE19_H4F1_LONGITUDINAL_BATH_WARD_AUDIT_PASS`;
- artifact ID `10814799107`;
- JSON `results/ge19_h4f1_longitudinal_bath_spatial_ward.json`;
- JSON SHA-256
  `105797e68ebb50a2b9b9cbdb78434f48a9d6f0c387bfc9fd1bbff86b7af7ef8c`.

All frozen blob and source-action bindings, and every exact
symbolic reduced spatial-relabeling gate passed.

## Actual derived transformations

Use the frozen 3+1 longitudinal coframe

`theta^0=Ndt, theta^1=L(dx+b dt)`,

`A=cosh(u)e_0+sinh(u)e_1`,

`s=sinh(u)e_0+cosh(u)e_1`.

The frozen covariant bath is a covector with
`U_{j mu}=q_j s_mu`. Its exact longitudinal
coordinate components are

`U_t=q[-N sinh(u)+L b cosh(u)]`,

`U_x=q L cosh(u)`.

For arbitrary infinitesimal spatial
`xi(t,x)`, the exact component tests prove

`delta U_t=xi U_{t,x}+U_x xi_t`,

`delta U_x=xi U_{x,x}+U_x xi_x`,

with the compatible longitudinal coefficient
transforming as the **spatial scalar**

`delta q=xi q_x`.

This scalar rule is derived from the covariant
`U=q s` construction and the coframe; it is
not an independent gauge transformation
imposed on an unrelated bath variable.

The aether's coordinate components transform
as a vector and obey `A^mu U_mu=0`
identically. Both

`A(q)=cosh(u)(q_t-b q_x)/N+sinh(u)q_x/L`

and

`X_phi=sinh(u)(phi_t-b phi_x)/N+cosh(u)phi_x/L`

are exact spatial scalars.

The GE05 per-node longitudinal density

`L_mem=NLR^2/4[(Aq)^2-(omega q-sqrt(w) X_phi)^2]`

therefore satisfies exactly

`delta L_mem=partial_x(xi L_mem)`

for arbitrary `xi(t,x)` including
`xi_t` and `xi_x`. This is an action-level
spatial Ward primitive and fixes the reduced
bath scalar Euler contribution `E_q q_x`
in the formal Ward identity.

## Open obligations and next gate

This result does not establish arbitrary
transverse bath perturbation transformations,
the distribution of all H4 parent-equation
residuals, the mixed H4 source coefficient,
a single common corrected-parent/time
realization, or discrete FD4/FD8 Noether
consistency.

The next analytic task is to derive the
**complete signed all-sector mixed H4 Ward
identity**, retaining GE06/GE07/Lambda,
the action-derived Stage E Y aether+scalar
mixed source, GE05 M1/M2 and the complete
bath, H1/H2/H3 parent residual terms.
A valid full analytic source identity is
needed before any common-grid structural
source evaluation and well before a new
Z21 science run.

The corrected H3F Z20/H3G q20 parents
remain certified only within their
frozen scopes. Existing reduced Z11
is the separately frozen linear tangent.
**Z21 remains NOT CERTIFIED and lensing blocked.**
