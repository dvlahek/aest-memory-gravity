# GE19 H4F3d1 — valid frozen canonical linear-operator Ward compiler

## Result

**Classification:** `GE19_H4F3D1_CANONICAL_OPERATOR_WARD_COMPILER_PASS`.

This is the **first restricted analytic/engineering implementation
gate** under the independently preregistered integrated H4F3d
actual corrected-parent Ward structural test. It proves the
signed frozen GE19 canonical *linear-operator row dictionary*
and tests its FD4 physical-time implementation with nontrivial
manufactured complex polynomial matrices and state vectors.

It is **not** the full H4F3d Noether structural PASS.
It does not evaluate actual H4F3b source NPZ, actual
H1/Z11/H3F/H3G parents, all signed parent Euler residuals
or boundary terms. It does not solve Z21 or license lensing.

## Preregistered source and exact immutable audit

- predata:
  `ge19/h4f3d1_predata_frozen_canonical_operator_ward.json`;
  blob `4577de495692ecbe4c07d1156ffab2abfc99e96d`;
- code:
  `ge19/h4f3d1_frozen_canonical_operator_ward.py`;
  blob `60786ac14c9478801c5df9ccf458ead9a34ac827`;
- dedicated GitHub workflow:
  `.github/workflows/ge19-h4f3d1-canonical-operator-ward.yml`;
  blob `99d47d088f4b621b9b36959244856f0b84e8c812`;
- valid workflow run `36102755011`;
  job `107968605067`;
  conclusion `success`;
  marker `GE19_H4F3D1_CANONICAL_OPERATOR_WARD_COMPILER_PASS`;
- uploaded CI artifact ID `10849404814`;
- JSON: `results/ge19_h4f3d1_canonical_operator_ward.json`;
  4239 bytes;
  SHA-256
  `f87f77dc02ccef3862c539a4e14aa5f67b78a2c68fbb5592fb9df71a979919e6`.

All pinned Git blobs, original 16-row Cmat source semantics,
symbolic iso/aniso/Euler-momentum projection, RHS sign
and both manufactured Nt64/Nt128 FD4/negative-control
cohorts passed without changing any historical file.

## Exact original canonical operator extraction

For the frozen unconstrained local first-order matrix
`Cmat[16,10]` acting on

`w=(N,dr,S,u,phi,T,Sdot,udot,phidot,Tdot)`,

the source-bound row ordering is:

- `Cmat[6]w`: isotropic L+R **nonderivative** Euler row;
- `(Cmat[12]+Cmat[13])w`: anisotropic
  L-R/2 nonderivative Euler row;
- `Cmat[14]w=p_L`: original GE06 L momentum;
- `Cmat[15]w=p_R`: original GE06 R momentum;
- `(Cmat[10]+Cmat[11])w`: independent
  GE06+GE07 shift Euler row.

The independent complete L Euler row is

`E_L=[Cmat[6]+2(Cmat[12]+Cmat[13])]w/3
       - d_t(Cmat[14]w)`.

In particular the derivative must act on the
**product** `Cmat(x)w(x)`, not only on the state.
The independent shift Euler row is

`E_b=(Cmat[10]+Cmat[11])w`.

On the original uniform `x=ln(a)` grid the
canonical operator contribution to the mixed
spatial Ward equation is

`W_op=-H FD4_x(E_b)-ik a E_L`.

These definitions preserve the exact
`E_L=(E_iso+2 E_aniso)/3` projection
and use `d_t=H FD4_x`. The original
H4F3b six-source contribution must be
combined later with its separately pinned
FD8/FD4 source-sector derivatives and
the complete signed parent Euler/boundary terms.

## Controls and unresolved physics

Independent manufactured complex polynomial Cmat
and w fields were used at Nt64 and Nt128, with
the exact frozen FD4 stencil including endpoints.
They retain `p_S=p_L+p_R`. The compiled
operator was checked against independently
differentiated **degree-four products**;
wrong momentum omission, wrong isotropic-only
L row and omission of `d_t Cmat` were required
to disagree. Neither `W_op` nor the
source Ward term was required to vanish.

The result is an operator *compiler* and a
necessary implementation check. It does not
establish physical linear Ward zero on an
actual certified background and cannot substitute
for a full off-shell action/parent residual
identity.

## Next one integrated H4F3d structural gate

The first full actual-source H4F3d test must
supply exact frozen H4F3b source JSON/NPZ,
the original certified H1/Z11/H3F Z20/H3G
q20 and Repair26 R1 bath parent data on the
same physical Nt128/Nt64 grid. It must derive
the signed complete parent Euler/boundary
terms **before** testing any physical
source+operator residual, and preregister
a structural truncation tolerance from the
FD4/FD8 operators, not from the previously
reported source-only Ward magnitude.

The original active H4 shift threshold `1e-6`
and matched temporal order `>=2.5`
remain unchanged for any later separately
preregistered Z21 science attempt.
Repair37 stays historical SCIENCE_FAIL;
Repair38–44 remain diagnostics.

**Full H4 Noether NOT CERTIFIED;
Z21 NOT CERTIFIED; lensing blocked.**
