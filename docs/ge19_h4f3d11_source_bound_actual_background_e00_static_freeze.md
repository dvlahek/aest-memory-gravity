# GE19 H4F3d11 — source-bound original background Euler, preregistration and static freeze

**Current classification:**
`GE19_H4F3D11_SOURCE_BOUND_BACKGROUND_COMPILER_STATIC_PASS_ACTUAL_OPEN`.
The independently constructed physical runner passed **synthetic**
static regression. The original certified-parent *actual local*
background E00 arrays have **not** yet been executed or observed.

## Why this is the next physical step

Independently verified actual H4F3d10r1 preserved all 530
original D10 low-mode arrays bitwise, restored the complete
Nyquist `m41..64` archive and assembled the original
eight-field **known first-order** mixed nonbath contribution
`P_known-partial_chi(B_known)`. Its actual grid archive and
known signed parent/boundary diagnostic passed, but it did
not evaluate the missing original-action background terms

```text
P_background = sum_i E_i00 * F_i21,chi
B_background = L21*E_L00 - b21*E_b00
```

A numerical Friedmann identity by itself is not a
certificate for all eight exact original-action Euler
rows. H4F3d11 therefore evaluates `E_i00` on the *same*
frozen Repair13 `C_min,C_star,C_max x Nt128,Nt64`
physical backgrounds before any claim that a background
product or lower-action boundary may be eliminated.
The unknown `F21`, `L21` and `b21` are retained.

## Exact action-bound homogeneous inputs

The frozen original GE06 plane-symmetric Einstein+AeST
action `ge06/analytic_aest_directional_source_generator.py`
is independently loaded with the same frozen blob
`a7afe0035054a9dca55d74a6497c081422114b4c`.
Its **exact** 15 local action partial expressions,
not its first directional `c1` expressions, are
symbolically substituted at

```text
N=1; L=R=a; b=u=0; Lt=Rt=a*H; pt=Q0+Z0*Z_action;
Lx=Rx=bx=ut=ux=px=Nx=0.
```

The substitution `pt=Q0+Z0*Z_action` is made in
symbolic expressions **before** floating evaluation.
The exact original background formulas are audited:

```text
K=2*K2*Z0^2*(exp(Z_action^2)-1)
KQ=4*K2*Z0*Z_action*exp(Z_action^2)
Q=Q0+Z0*Z_action

pN_f=6*a*adot^2 + 2*a^3*(K-Q*KQ)
pL_f=-2*adot^2+2*a^2*K
pR_f=2*pL_f
pL_t=-4*a*adot
pR_t=-8*a*adot
pb_x=4*a^2*adot
pphi_t=2*a^3*KQ
all other homogeneous GE06 local partials = 0
```

The nonzero `pb_x` is preserved even though its
*homogeneous spatial derivative* vanishes.
The exact original GE07 minimally coupled dust
action `ge07/pressureless_matter_directional_source_generator.py`
(blob `cde8da77a80799cef00fc7c09c3633310fc9e3d4`)
gives `pN_f=-2*a^3*rho_b`,
`pT_t=2*a^3*rho_b=6*C`,
with `rho_b=3*C/a^3` and all other background
dust partials zero. The lapse, dust current and
density constraint remain separately recorded.
The original Lambda contribution is exactly
`(-6*rho_lambda*a^3,-6*rho_lambda*a^2,-12*rho_lambda*a^2)`
in `N,L,R`; original `rho_lambda_action`
comes from the *same* Repair13 physical parent.
The homogeneous zero-gradient NL0C/Y derivative
is zero by the frozen H4F3d8 symbolic zero-set
gate; its nonzero mixed H4 Y source is not deleted.

The exact source-bound compiler checks 15 original
GE06 and 7 original GE07 background partials
**symbolically** and has negative controls for
omitting the original nonzero shift momentum,
dropping the original scalar `Q*KQ` lapse
term and reversing the dust lapse sign.
The original `1e-12` comparator here is an
**internal numerical evaluation of expressions
already proved symbolically identical**, not a
physical background on-shell or H4 Ward threshold.

## Physical-grid archive and claim boundaries

The local runner stores the original physical
`H*FD4_ln(a)` and `H*FD8_ln(a)` temporal
derivatives **separately**, all eight
`N,L,R,b,u,phi,T,rho` original `E_i00`
arrays for six cases, all original action
currents/partials, original `a,H,Q,Z,K,KQ`,
dust, Lambda, Friedmann reconstruction,
and report-only absolute and natural-scale
residual norms and `rho_lambda` variation.
The scalar current and dust charge are also
checked as report-only original parent diagnostics.

`E_N/(6*a^3)=H^2-(Q*KQ-K)/3-C/a^3-rho_lambda`
is an independent analytic Friedmann formula.
`E_L,E_R` include the original time derivative
of their action momenta, not just the lapse
constraint. A varying interpolated
`rho_lambda_action` is measured and never
silently assumed constant. In particular
`E_R=2*E_L` is the homogeneous action
symmetry, but it is **not** an independent
on-shell error-budget certificate.

No source-matched physical smallness threshold
has been introduced. Actual background
`E_i00` residuals may be nonzero and are
archived with signs, both time stencils and
unmodified original nodes. The runner does
not solve or assume `F21`, `L21` or `b21`.

## Frozen code and static evidence

- Immutable predata:
  `ge19/h4f3d11_predata_actual_original_action_background_e00.json`,
  Git blob `deb4b35e6a147b48fe93d6c99d798572650000ac`.
- Exact original-action source compiler:
  `ge19/h4f3d11_source_bound_original_background_partials.py`,
  blob `1f085efec4ea64b42822ddeaac566f532d9dccf1`.
- Actual physical-grid evaluator:
  `ge19/h4f3d11_actual_original_action_background_e00.py`,
  blob `b162fad1db2a855917b5f8e29fce10c67d30737f`.
- No-overwrite local parent/code hash runner:
  `ge19/run_local_h4f3d11_actual_original_action_background_e00.sh`,
  blob `8c4f34ad79b347b3810093a1bba0b4129468f7fc`.
- Source compiler [static Actions 36189149840](https://github.com/dvlahek/aest-memory-gravity/actions/runs/36189149840)
  job `108249774292` **SUCCESS**,
  marker `GE19_H4F3D11_SOURCE_BOUND_BACKGROUND_COMPILER_STATIC_PASS_ACTUAL_OPEN`.
- Physical driver/runner [static Actions 36189465789](https://github.com/dvlahek/aest-memory-gravity/actions/runs/36189465789)
  job `108250800122` **SUCCESS**,
  marker `GE19_H4F3D11_PHYSICAL_DRIVER_STATIC_PASS_ACTUAL_BACKGROUND_OPEN`.

The first version of the source-test workflow,
[run 36189057213](https://github.com/dvlahek/aest-memory-gravity/actions/runs/36189057213),
failed before original-source import due to a
mistaken exact-string comparison against a
longer preregistered text entry. The separately
versioned `static-r1` workflow fixed only
that test-string check, preserving the original
failed workflow and all original physics source
blobs. It then passed all actual-source symbolic
and synthetic numerical regression checks.

## User-local actual physical execution

The user-local results directory, not Actions, holds
the original exact Repair13, H3F/H3G/Z11,
Repair26 and source/bath parents. The runner checks
their frozen locks plus **the unchanged actual
H4F3d10r1 physical JSON** SHA256
`69eabf101a6ec1939b32323e25b207dc419fad57eb5b2cef0858874a50cfa1d2`
and **NPZ** SHA256
`85c0fbd8b56037aae98615926b70bd60739a1af2fa1ff666ffc2e95485c2749b`.

```bash
cd ~/aest-memory-gravity
git checkout physics-first-gravitational-elasticity
git pull --ff-only
source .venv/bin/activate
set -o pipefail
bash ge19/run_local_h4f3d11_actual_original_action_background_e00.sh \
  2>&1 | tee results/ge19_H4F3D11_LOCAL_runner.log
echo "EXIT=${PIPESTATUS[0]}"
```

If successful, the new physical outputs are
`results/ge19_h4f3d11_actual_original_action_background_e00.json`,
`results/ge19_h4f3d11_actual_original_action_background_e00.npz`,
and `results/ge19_h4f3d11_actual_original_action_background_e00_FULL.log`.
Preserve all previous D10 and D10r1 artifacts unchanged.
The new physical outcome must be independently audited
before any actual-grid science classification.

**No actual original-parent E00 residual result yet;
no certified E00 on-shell gate; no numerical
E00*F21 or L21 action-background term;
no complete full all-sector H4 Ward,
no certified Z21 and no lensing.
Original Repair37 SCIENCE_FAIL immutable.
Original 2048 R1 bath nodes, active shift
1e-6 and time-order >=2.5 unchanged.**
