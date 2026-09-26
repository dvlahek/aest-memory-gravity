# GE19 H4F3d11 — actual original-source background E00 independent physical archive freeze

**Physical classification:**
`GE19_H4F3D11_ACTUAL_BACKGROUND_E00_ARRAYS_DIAGNOSTIC_PASS_ONSHELL_OPEN`.

**Independent uploaded-artifact classification:**
`GE19_H4F3D11_ACTUAL_ORIGINAL_SOURCE_BACKGROUND_E00_INDEPENDENT_ARCHIVE_AND_DERIVATIVE_DIAGNOSTIC_PASS_ONSHELL_OPEN`.

This stage has evaluated the actual frozen original GE06/GE07/Lambda
**homogeneous nonbath** background Euler `E_i00` for all eight
`N,L,R,b,u,phi,T,rho` action fields, all original
`C_min,C_star,C_max x Nt128,Nt64` physical grids and
original `H*FD4_ln(a)` and `H*FD8_ln(a)` divergences separately.
It did not evaluate the original `E_i00 F_i21,chi`
mixed term, the original `L21 E_L00-b21 E_b00`
background action boundary, complete GE05 bath
background Euler or the integrated full H4 Ward.

## Uploaded physical bytes independently audited

| Original user-local artifact | SHA256 | Bytes |
| --- | --- | ---: |
| `ge19_h4f3d11_actual_original_action_background_e00.json` | `d62436b12bb5e5d9b7cbf1ea24abd0e6c06ac3ff1bfd43a41556aef284e3d3df` | 49826 |
| `ge19_h4f3d11_actual_original_action_background_e00.npz` | `7679dc6765b87c0b1294b3915d0d1305e4fa59ac86a18d75621d5bf85c616229` | 358182 |
| `ge19_h4f3d11_actual_original_action_background_e00_FULL.log` | `d62436b12bb5e5d9b7cbf1ea24abd0e6c06ac3ff1bfd43a41556aef284e3d3df` | 49826 |
| `ge19_H4F3D11_LOCAL_runner.log` | `5d8f7f5cc306cce969ad498aa86db0737246e5055415c3d372ece6bd109537e9` | 2167 |

JSON and FULL log are **byte-identical**. All original
runner-reported file hashes and byte lengths match actual uploads;
the terminal runner marker agrees with the JSON classification.
The runner reported original code/predata/physical-parent SHA PASS.
The JSON reaffirms original Repair13 NPZ SHA256
`011c0ae54fd21d70c0e2c695ce62e7b74a3c5529a07c9023c882a447d5b40ca3`,
original passed D10r1 actual JSON SHA256
`69eabf101a6ec1939b32323e25b207dc419fad57eb5b2cef0858874a50cfa1d2`,
and original passed D10r1 NPZ SHA256
`85c0fbd8b56037aae98615926b70bd60739a1af2fa1ff666ffc2e95485c2749b`.
Historical raw H3F/H3G/Repair13/Z11/Repair26 inputs were
verified by the **user-local original runner**, not independently
reintegrated from uploaded raw physical parent bytes.

The NPZ has **578 finite numerical arrays**: 96 arrays for each
of six `C/Nt` cases plus the two original x clocks;
289 arrays of length 128 and 289 of length 64.
Every original case is present, with both time schemes and all
eight distinct background Euler rows. All 96 actual `E_i00`
arrays were independently reassembled exactly from the
signed archived source components.
All 48 archived GE06 `pLt,pRt,phi_t` and GE07
`pT_t` original FD4/FD8 temporal divergences were
independently reconstructed **exactly** from the
original frozen differentiation coefficients.

The source compiler's original GE06 15 and GE07 7
background action-partial symbolic gates PASS.
Independent numerical action-partial reconstruction
from archived original Repair13 `a,H,Q,K,KQ,rho_dust`
agrees to a maximum `3.7032e-15` relative.
Here the **original model normalization matters**:
Repair13 `rho_dust_action=C/a^3` is the Friedmann
density, while original GE07 uses the matter-action
`varrho_b=3*C/a^3`. Thus the original action gives
`pN_f^dust=-6*C`, `pT_t^dust=6*C`;
no factor of three was added to or removed from
the action or original physical outputs.

## Actual physical C_star / Nt128 example

| Original Euler row or source diagnostic | FD4 original-grid L2 | FD8 original-grid L2 |
| --- | ---: | ---: |
| `E_N00` | 2.940830783e-21 | 2.940830783e-21 |
| `E_L00` | 1.544185613e-15 | 5.807162290e-20 |
| `E_R00` | 3.088371226e-15 | 1.161432458e-19 |
| `E_phi00` | 1.980739816e-18 | 1.470005387e-17 |
| `E_T00` | 4.281972018e-25 | 1.775348380e-24 |
| `E_b00,E_u00,E_rho00` | exactly 0 | exactly 0 |

The original `E_L00` relative to the natural sum of its
GE06/GE07/Lambda Euler component L2 scales is
`4.2164e-10` on FD4 and `1.5857e-14` on FD8,
**report-only**. All six original `E_R00=2E_L00`
arrays are exactly reproduced as stored. The original
homogeneous GE06 `p_bx00` shift momentum is
nonzero (C_star/Nt128 norm `0.00360704`),
but its homogeneous spatial derivative vanishes.
Do not drop the local momentum before
checking the physical spatial action boundary.

The source report's `natural_relative=1` for
the scalar and dust-potential rows is a tautology
of the original per-row natural-scale definition:
those fields have only **one** saved temporal
divergence component in the background. It is NOT
physical evidence of a 100% violation. When normalized
to the relevant nonzero original background
`phi_t` and `T_t` current L2 norms, the actual
largest scalar residual ratios are about
`2.18e-16` (FD4) and `1.62e-15` (FD8)
over all six cases. The FD8 scalar residual can
grow relative to FD4 because of cancellation
when differentiating an almost-constant
charge at machine precision.

## Independently localized original-grid temporal defect

The frozen exact homogeneous action and the
frozen Repair13 scalar/dust/Friedmann identities give
a *conditional analytic nonbath continuum reduction*:

```text
H^2 = (Q*KQ-K)/3 + C/a^3 + rho_lambda
dH^2/dln(a) = -Q*KQ - 3*C/a^3   [constant rho_lambda]
p_Lt = -4*a^2*H
-d_t(p_Lt) = 8*a^2*H^2 + 2*a^2*dH^2/dln(a)
E_L00 = 2*a^2*(3*H^2+dH^2/dln(a)+K-3*rho_lambda) = 0
E_R00 = 2*E_L00 = 0
E_phi00 = -2*d_t(a^3*KQ) = 0
E_T00 = -6*d_t(C) = 0
```

Those equalities apply **only** under the original
homogeneous nonbath action and exact scalar/dust
conservation plus frozen constant-Lambda Friedmann
model. No GE05 memory-bath Euler has been
proved zero in this step.
All six actual uploaded `rho_lambda_action`
grids are exactly constant. The archive's
`a^3 KQ` varies by at most `1.0843e-19`
around `0.0004007778406741802`, consistent
with float64 stable-action charge reconstruction.

On all six original actual backgrounds, independently
replacing only the `p_Lt` finite difference with
the exact analytic time derivative gives
`||E_L00^analytic||_2 <= 4.961e-22`.
The actual original archived discrete-minus-analytic
Euler difference agrees with the explicit
finite-difference `p_Lt` derivative defect
to within `6.484e-23` L2.
Thus the much larger original FD4 metric-pressure
residual is specifically an original **temporal
discretization defect**, not evidence for an extra
nonbath continuum force. This is an independent
algebraic recomposition from the *uploaded original
physical background and frozen source partials*,
not a second independent original H3F/H3G solve.

No numerical science-smallness threshold was
chosen from these outputs. Full high-derivative
FD4/FD8 error certification on the original
active H4 window remains OPEN; any product
`E_i00*F_i21,chi` needs actual original
`F_i21` and a bound on the relevant discretization
defect before it can be suppressed in the
numerical Ward identity.

## Immutable project boundaries and next route

Machine-readable independent actual audit:
`ge19/h4f3d11_actual_original_background_e00_independent_archive_audit.json`
Git blob `c3f238c2914ff18e43030ec31a3debb0edab81f1`.

The original failed D10 result and original
Repair37 SCIENCE_FAIL stay immutable.
The original `2048` R1 bath nodes, shift
`1e-6`, time-order requirement `>=2.5`,
and all frozen source parameters are unchanged.

**Current outcome: original physical E00-array
diagnostic PASS; analytic original homogeneous
nonbath cancellation derived conditionally;
no actual full covariant E00 on-shell gate,
no GE05 bath background on-shell certificate,
no `E00 F21,chi` product, no
`L21 E_L00-b21 E_b00` evaluation,
no complete original integrated H4 Noether,
no certified window-local particular Z21
and no lensing.**

Next source-first step: preregister an independent
symbolic exact original-action homogeneous
nonbath background cancellation and an actual
original `F21`-dependent discrete defect bound;
then restore all full GE05 bath/action boundaries
and actual original full H4 Ward. Do not
use observables to tune the theory.
