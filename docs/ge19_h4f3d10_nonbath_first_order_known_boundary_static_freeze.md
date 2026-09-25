# GE19 H4F3d10 — frozen ACTUAL first-order nonbath Euler and known lower-boundary local runner

## Scientific scope and current classification

**Classification: `GE19_H4F3D10_STATIC_ASSEMBLY_PASS_ACTUAL_PHYSICAL_OPEN`.**

Following the actual physical H4F3d7r1 original R1 interval-ODE versus
sampled-FD4 diagnostic PASS, H4F3d10 is a separate versioned,
physics-first **actual-parent executable** for the eight nonbath
fields `N,L,R,b,u,phi,T,rho`. It uses exact original corrected
H3F H1 and certified Repair32B/32C Z11 parents on the same
Repair13 `Nt=128,64`, `C_min,C_star,C_max` grids.

The first-order field Euler rows use unchanged source-bound
GE06 stable-Z analytic c1 action partials, original GE07 dust c1,
and exact linearization of original Lambda
`-6*rho_lambda_action*N*L*R**2`. Original physical-time
`H*FD4_ln(a)` and `H*FD8_ln(a)` divergences are retained as
**separate report-only diagnostic arrays**. Spatial
`partial_chi` uses the original frozen spectral derivative,
not `partial_ln(a)`. Original six positive real modes
`3,5,8,10,15,20` enter the original `Nx=128` polynomial
grid, and signed Fourier products are retained through `m=40`.

The only computed mixed parent/boundary here is the exact
source-bound known first-order part:

```text
P_known = sum_i 2*(E_i10 * F_i11,chi + E_i11 * F_i10,chi)
B_known = 2*L10*E_L11 + 2*L11*E_L10
        - 2*b10*E_b11 - 2*b11*E_b10
W_known = P_known - partial_chi(B_known)
```

The original reduced first-order parent has `b10=b11=0`,
but the negative sign and both shift cross terms remain
explicitly implemented and were exercised with nonzero
synthetic shift fields in CI. The analytic first-order
NL0C/Y flux derivative at the exact homogeneous zero-gradient
background is zero, as separately proved by frozen H4F3d8.
The genuinely nonzero mixed physical H4 Y source is
**not deleted**.

**Unresolved exact terms are preserved:**

```text
P_background = sum_i E_i00 * F_i21,chi
B_background = L21*E_L00 - b21*E_b00
```

The full mixed nonbath contribution still requires
`P_background - partial_chi(B_background)`.
The new code does not assume or assert `E_i00=0`
numerically from cosmological intuition. It does not
have certified Z21/F21, so it cannot evaluate those
terms or the complete H4 Noether identity.

## Versioned exact provenance and PASS

- Preregistration `ge19/h4f3d10_predata_actual_nonbath_first_order_known_boundary.json`,
  blob `7aafe872f32057ab46ed99650b3df1803050077e`.
  The `1e-12` FFT comparison is exclusively an
  *archive/synthetic internal assembly check*, **not**
  a newly fitted physical Ward or on-shell gate.
- Original physical-input preflight:
  `ge19/h4f3d10_actual_nonbath_first_order_known_boundary.py`,
  blob `c570546caa301ec6899b4e669b663726fd4fdc2f`.
- Frozen GE06/GE07/Lambda first-order physical local partials:
  `ge19/h4f3d10_nonbath_first_order_local_partials.py`,
  blob `4c3968d7186e27f15b10992198d7bccedf207bfb`.
- Independently assembled signed parent/boundary:
  `ge19/h4f3d10_known_parent_boundary_assembly.py`,
  blob `d3a43a0ebbd78e03f2313592bdb1455977cb1d1c`.
- Versioned six-case local physical driver:
  `ge19/h4f3d10_physical_main.py`,
  blob `1eec8381ba107a02ba3dc41bfd18fcc7e12d224e`.
- No-overwrite/isolated-working-directory runner:
  `ge19/run_local_h4f3d10_actual_nonbath_first_order_known_boundary.sh`,
  blob `4c873192001a1fd8f3652a9e47ec13c11d999199`.
- Regression workflow
  `.github/workflows/ge19-h4f3d10-nonbath-static.yml`,
  blob `ac6f5151128b5fdaf265b3bceaa107ffa9dbf920`.
- [Actions 36161122686](https://github.com/dvlahek/aest-memory-gravity/actions/runs/36161122686),
  job `108157660938`, completed **success**.
  This verifies original frozen Git blobs, source syntax,
  runner isolation, no overwrite, eight signed fields,
  Fourier reconstruction, both original time-scheme labels,
  exact known-boundary sign and explicit wrong-shift-sign
  negative control, on independent **synthetic** fields.
  It has not evaluated actual physical parent NPZs.

The frozen H4F3d7r1 original physical JSON
SHA-256 `031229d570d29ae9c4ea0ab8e25222d94e9cda4520c991cd203e9d7b97e01dc9`,
NPZ SHA-256
`4f011c96c2c11165df6332eafc459c5d2c5e7bc5164a436bde3d1563696f0e13`,
H4F3b/H4F3d6 and original Repair26 full R1 trace
are all required in their previously frozen exact bytes.
The original H3F/H3G, Repair32B/32C, Repair13 and
dense-background SHA gates are delegated to
`s.frozen_inputs` under the same original frozen code.
The new runner additionally checks original r7/r11/r13/r14/r24
implementation blobs before the first historical import.

## Local PHYSICAL run and result boundary

Only the user's original local checkout has all original
certified parents. The run is not substitutable by a
GitHub Actions manufactured fixture.

```bash
cd ~/aest-memory-gravity
git checkout physics-first-gravitational-elasticity
git pull --ff-only
source .venv/bin/activate
set -o pipefail
bash ge19/run_local_h4f3d10_actual_nonbath_first_order_known_boundary.sh \
  2>&1 | tee results/ge19_H4F3D10_LOCAL_runner.log
echo "EXIT=${PIPESTATUS[0]}"
```

If successful, the distinct physical outputs will be
`results/ge19_h4f3d10_actual_nonbath_first_order_known_boundary.json`,
the companion `.npz`,
and `_FULL.log`. They must be independently checked before
freezing any **actual** H4F3d10 diagnostic.

**No full actual all-sector H4 Ward/Noether PASS.
No physical FD4/FD8 full error budget.
No newly asserted bath-on-shell condition.
No Z21 certification; lensing blocked.**
The original Repair37 SCIENCE_FAIL, original
2048-node R1 bath, active shift `1e-6`
and matched time order `>=2.5` remain unchanged.
