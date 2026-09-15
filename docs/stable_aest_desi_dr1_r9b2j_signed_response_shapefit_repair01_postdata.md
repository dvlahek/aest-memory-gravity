# Stable AeST DESI DR1 R9b2j signed-response ShapeFit Repair01 — postdata freeze

## Frozen result

The first completed Repair01 invocation is classified

`STABLE_AEST_DESI_DR1_R9B2J_CROSS_OPERATOR_FAIL`.

This is the R9b2j scientific/numerical result. The earlier exit-143 invocation remains a technical non-result and is not reclassified.

Repair01 completed all twenty `(tau, eta)` CLASS cases with process isolation/checkpointing. Stage A completed; DESI data and the likelihood projection were not evaluated because the preregistered cross-operator gate failed.

## Frozen gates

- J1 provenance: PASS
- J2 common bounded native grid: PASS
- J3 eta=0 closure and tau invariance: PASS
- J4 signed-response integration-resolution convergence: PASS
- J5 epsilon consistency: PASS
- J6 linear-vs-PCHIP signed-response operator agreement: FAIL

The thresholds remain the preregistered `E <= 0.05`, `C >= 0.995`. They are not relaxed postdata.

## Frozen diagnostics

The native source grid is common and healthy, with 108 retained nodes spanning approximately `1.0494678329e-4 <= k_h <= 4.1823019354`.

Value-level eta=0 closure remains healthy:

- max relative `sigma8_dd` closure: `0.004281014344273224`
- max relative `f` closure: `0.0012638368549621388`

Eta=0 tau variation is negligible:

- `f`: `4.403917722396233e-10`
- `sigma8_dd`: `5.326722844947505e-10`
- `sigma8_tt`: `9.387830934074604e-10`

The linear signed-response integral is internally converged: 4096-to-8192 differences are about `1.4e-5` in relative vector norm and 8192-to-16384 differences about `2.5e-6`, with cosines effectively one.

Both interpolation operators are independently epsilon-stable. Across the four tau values, the 8192-node linear operator has primary/control `E` from about `3.3e-6` to `9.5e-4`, while PCHIP has `E` from about `4.0e-6` to `1.31e-3`; all corresponding cosines are effectively one.

However, linear and PCHIP signed-response tangents remain materially different at both epsilon values. Across tau, the cross-operator mismatch is approximately `E = 0.3216--0.3223`, `C = 0.9804--0.9806`. The mismatch is therefore not caused by finite-difference epsilon or by the 4096/8192/16384 integration grid. It is localized to reconstruction of the signed response between the 108 actual CLASS transfer nodes.

## Frozen artifacts

- Repair01 result JSON SHA256: `e61b05279e0b2cb58c12a66cc0455f4c894ba5be2ec7d656be13cf6b8cf8c602`
- Repair01 science log SHA256: `735c93724fc4567f2c6c51c533ae2c72ca42037de725cfd6122d358d2f1b9b96`

## Authorized next step

No operator may be selected postdata and J6 may not be removed or weakened.

The only authorized next diagnostic is an actual CLASS native-k-density convergence test. It must change the solver's real transfer sampling, not merely add interpolation/integration nodes. The historical corrected-CLASS dense settings are `k_per_decade_for_pk = 80` and `k_per_decade_for_bao = 560`; these values may be used as the first dense tier. A second, independently preregistered denser tier may be used to establish convergence.

DESI ShapeFit data remain blocked until the signed-response operator ambiguity is resolved under actual solver-node refinement. If the ambiguity persists under native-k refinement, the direct-velocity ShapeFit observable remains numerically unresolved and no DESI projection is licensed from this chain.
