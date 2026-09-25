# GE19 H4F3d5 — valid normalized bath Euler residual compiler

## Classification and scope

`GE19_H4F3D5_NORMALIZED_BATH_PARENT_RESIDUAL_COMPILER_PASS`.

The frozen GE05 per-node action, original first-order Euler current,
normalized `z=omega q/sqrt(w)` convention, and physical eta-rescaled
H4 mixed bath Ward coefficient have been checked independently.
The compiler passed its two deterministic manufactured time-grid
FD4/kinematic/sign tests on GitHub Actions.

This is **not** an actual physical-parent H4 Ward/Noether residual
evaluation, a new H4/Z21 solve or a lensing result. The deliberately
manufactured test fields are not a substitute for the original
H1/Z11/H3F/H3G/Repair26 R1 arrays.

## Immutable provenance

- preregistration:
  `ge19/h4f3d5_predata_normalized_bath_parent_residual_compiler.json`,
  blob `6b7519b48ace8900c8a2879f13c70db3524b366e`;
- valid source:
  `ge19/h4f3d5_normalized_bath_parent_residual_compiler.py`,
  blob `62cbd02902ccb514c535213ff9801a9abcd46ffb`;
- dedicated workflow:
  `.github/workflows/ge19-h4f3d5-normalized-bath-euler.yml`,
  blob `c3b14955a1287158d76ca47ad9b80e733d785c97`;
- successful execution commit `5d0495640d6c5fb926d2e15118a90d11df110980`;
- GitHub Actions run `36126850777`, job `108044837991`,
  conclusion `success`;
- terminal marker:
  `GE19_H4F3D5_NORMALIZED_BATH_EULER_COMPILER_PASS`;
- result JSON:
  `results/ge19_h4f3d5_normalized_bath_parent_residual_compiler.json`,
  6089 bytes, SHA-256
  `f7538b77475c0dbcab57f331770a75643216d2d3c5966e41396fded0d7b41df4`;
- artifact `ge19_h4f3d5_normalized_bath_euler_compiler`,
  ID `10860371141`.

All exact frozen blob checks, action/sign checks and every preregistered
manufactured Nt64/Nt128 test gate passed. No old source or science
threshold was altered.

## Derived normalized first-order bath Euler residual

With `omega_j=r_j/tau`, `w_j>0`,
`z_j=omega_j q_j/sqrt(w_j)`, and
`v_j=tau H d_xi z_j`, where `xi=ln(a)`,
the exact GE05 raw first-order Euler residual is

`R_z,j10=H D_xi[a^3 v_j/tau]+a^3 omega_j^2(z_j-X10)`,

`E_q,j10,GE05=-sqrt(w_j)/(2 omega_j) R_z,j10`.

The physical eta-regularized, GE06-normalized mixed H4 bath Ward
parent is **`+4 sum_j E_q,j10 q_j10,x`**. Its algebraic
per-node *mode-coefficient product* is
`-2(w_j/omega_j^2)R_z,j10(ik)z_j10`.
Physical Fourier coefficients of this product require the
corresponding real-space convolution; multiplying equal-k mode
coefficients is not that convolution.

Both finite-grid manufactured cases use 5 positive bath nodes,
modes 3/5/8, Nt64/Nt128, a degree-four polynomial current,
the original fourth-order time derivative including boundary
stencils, an independently determined drive with analytically
zero first-order bath Euler residual, and negative tests for
omitting H and reversing the Euler sign.

These tests certify **only** normalization, analytic sign and
manufactured FD4 consistency. They do not show that
`E_q,j10` vanishes on the user's saved physical first-order
bath trajectory.

## Remaining physical H4F3d gate

Under existing
`ge19/h4f3d_predata_actual_operator_all_parent_ward_closure.json`,
evaluate the exact normalized per-node bath Euler residual
and all other signed parent Euler/boundary terms independently
on the **same original physical Nt128/Nt64 parent grids**
as the valid H4F3b six-piece source. Add them to the original
canonical full-product FD4 operator Ward and the separately
frozen source-family FD8/FD4 Ward. Derive and prelock the
structural numerical error budget before examining the
combined physical residual.

The genuine H4F3b source binary and original certified
Repair32B Z11 NPZ are not automatically present in the
Actions checkout. The manufactured H4F3d5 result cannot
replace them. Their exact SHA-256-locked original files
must be accessible to any genuine physical integration.

Historical Repair37 remains SCIENCE_FAIL. Full physical
all-parent H4 structural Noether PASS has **not** been
obtained. `Z21` is NOT CERTIFIED and lensing is blocked.
