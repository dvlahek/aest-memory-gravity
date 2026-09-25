# GE19 H4F3d6 — valid normalized bath Euler/Ward compiler, actual inputs pending

## Result and exact claim boundary

Classification:
`GE19_H4F3D6_BATH_CONVOLUTION_COMPILER_PASS_ACTUAL_OPEN`.

This is a valid **manufactured analytic/numerical implementation result**
for the independent, signed GE05 first-order per-node bath Euler
contribution to the physical mixed H4 Ward identity. It is NOT the
actual corrected-parent bath Ward result, full all-sector H4
Noether certificate, H4/Z21 science reclosure or lensing result.

The first **physical** H4F3d6 execution has not been performed.
The original certified local H4F3b six-piece NPZ and Repair32B
Z11 binary are not in GitHub Actions checkout. No fabricated
or manufactured parent replaces those files in the physical run.

## Frozen source and successful CI

Predata:
`ge19/h4f3d6_predata_actual_normalized_bath_parent_ward.json`,
blob `d283086a6ae95efd184db570d6c2f9a8aa32ac7c`.

Implementation:
`ge19/h4f3d6_actual_normalized_bath_parent_ward.py`,
blob `0419145499f5f44e06ba0c96f779c2a604e84ce7`.

Dedicated workflow:
`.github/workflows/ge19-h4f3d6-bath-parent-ward.yml`,
blob `ec0d9c94eaa6295ed46eb858b62a278ec05e8c02`.

Successful workflow:
- run `36127944207`;
- job `108048299004`;
- conclusion `success`;
- marker `GE19_H4F3D6_BATH_CONVOLUTION_COMPILER_PASS_ACTUAL_OPEN`;
- artifact `ge19_h4f3d6_manufactured_bath_ward`;
- artifact ID `10860163241`;
- result JSON SHA-256
  `db6eb2effc711c2c83ebeff6bbeae5e64c295e160505174d657ec676e2f8ad9f`.

Exact pinned-source and manufactured Nt64/Nt128 gates passed.
The script tests the original FD4 current, plus and negative
complex-conjugate Fourier harmonics, independent real-space
FFT of the **physical product** and a deliberately wrong
spatial-gradient negative control. A same-mode product
without convolution is explicitly not accepted.

## Action-normalized physical expression

The exact frozen GE05 first-order normalized per-node bath
Euler residual is

`R_zj10 = H D4_x(a^3 v_j10/tau)
          +a^3 omega_j^2(z_j10-X10)`,

`E_qj10,GE05 = -sqrt(w_j)/(2 omega_j) R_zj10`,

`q_j10,x = sqrt(w_j)/omega_j * (ik) z_j10`.

The physical eta-regularized mixed Ward bath parent term is

`W_bath = +4 sum_j E_qj10,GE05 q_j10,x`.

To obtain the actual mode coefficient, both positive
original modes `m=(3,5,8,10,15,20)` and the
conjugate negative harmonics are included before
summing all spatial cross-products at `m=0..40`.
The physical input is the **frozen Repair26 R1**
full-history first-order per-node bath, reconstructed
using the unchanged Repair24 propagator on the
on-shell certified H3F H1 and exact common
H4F3b Nt128/Nt64 `x=ln(a)` grid.

The physical script checks hashes for the
existing actual H4F3b source JSON/NPZ,
H3F Z20, H3G q20, original certified Z11,
Repair13 background, Repair26 R1 trace and
frozen source implementations before
producing any new result. The H3G stored
weighted z10 is an independent check of
the reconstructed per-node first-order bath.

## Source comparison and structural limitations

The exact stored H4F3b physical source Ward is
read without recalculation, correction or fitting.
The script saves the per-C,Nt bath parent Ward
and all 18 per-C,beta,Nt
`W_source+W_bath` arrays for inspection.

**No physical smallness/zero gate** is imposed
on the source-only or source+bath term. The
complete nonbath background/H1/Z11 Euler
parent contributions, action boundary and
independent canonical operator Ward still
must be instantiated and evaluated on the
same actual grid. A structural FD4/FD8
error budget remains to be derived and
preregistered before the integrated test.

Even a valid future physical H4F3d6
bath-subset PASS will not certify the
full Noether identity or permit a
new Z21 solve on its own.

Historical Repair37 science FAIL and
Repair38--44 diagnostics remain immutable.
Original active shift 1e-6 and
matched-order >=2.5 are unchanged.

**Full all-sector H4 Noether NOT CERTIFIED;
Z21 NOT CERTIFIED; lensing blocked.**
