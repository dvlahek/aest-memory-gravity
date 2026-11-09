# GE19 LW03 — frozen local result: source-time native closure PASS, radial projection FAIL

**Date:** 2026-11-09. **Result status:** `GE19_LW03_SOURCE_TIME_OPERATOR_OR_RADIAL_QUADRATURE_FAIL`. This is a completed three-CLASS-run numerical **FAIL** of the original frozen LW03 composite gates, not a crash or an implementation exception.

## Submitted evidence

The user supplied three exact local artifacts from the single `_kprefixfix` WSL execution (source artifacts remain on the researcher's local system, rather than copied into Git):
- `results/ge19_lw03_source_time_closure_20261109_kprefixfix.json`, SHA-256 `dcf057b8e51e4863f0c0765c11973de71db01240fce6421a691b3704869ae09d`;
- `results/ge19_lw03_source_time_closure_20261109_kprefixfix.log`, SHA-256 `b438e8e3835cda914b4eb7a59dc2b94626aa8d81c0ede3c7e952a15adcfaed9e`;
- `results/ge19_lw03_source_time_closure_20261109_kprefixfix.npz`, SHA-256 `f5b1334ab171e5e8df680ef6043969c91fbbafeb467bad8477d27ad4c94a0d53`.

The original frozen predata git blob remains `f66323370f526faa3e4587795d91e72d4bd68c0b`. Original source constraints: `KB=0.0665`, `tauH0=10`, `p=0`, CLASS HEAD `e85808324f51fc694d12e3ed7439552a3c3f9540`; only baseline, +2.5, -2.5 runs; no observational fit, no H4.

## Exactly what passed

`get_transfer(z)` evaluated the signed Weyl source-time operator at 262 unique source redshifts inside the original, ell-specific LW02 windows. Native CLASS Fourier-grid k-prefix check `0.0`, original source-plane and comoving background geometry mismatch `0.0`, archived LW01 native-time baseline W relative L2 difference `6.216583398058324e-15`, same **lambda=2.5** signed tangent relative L2 difference `2.2563377946040432e-14`. All transfer values finite. **The source operator agrees with the native LW01 state at the original nodes essentially at machine precision**. This is a robust additional numerical cross-check and does not promote LW02.

## Exactly what failed

Locked radial signed-derivative quadrature thresholds: `17→33 relative error/abs-derivative integral <=0.02`, `33→65 <=0.005`, and same nonzero sign across 17, 33, 65. All four eligible ells had `quadrature_gate=false`; ell=500 had only two native z nodes and remained excluded.

| ell | original LW02 signed ratio | LW03 17 nodes | 33 nodes | 65 nodes | 17→33 abs-weighted error | 33→65 abs-weighted error |
|--:|--:|--:|--:|--:|--:|--:|
| 100 | -0.007596365936 | -0.005256399905 | -0.001338774320 | +0.000298841035 | 0.62380170 | 0.27990332 |
| 150 | -0.019510092135 | -0.013547381335 | -0.012530474787 | -0.012293429490 | 0.06700297 | 0.00585552 |
| 200 | -0.002674807885 | -0.000426598538 | +0.002055944652 | +0.001323734141 | 0.41643022 | 0.12010702 |
| 300 | -0.001645935053 | +0.001790948355 | +0.002345913722 | +0.001750524748 | 0.05864027 | 0.07454947 |

`ell=100,200`: even the sign criterion fails. `ell=150`: 33→65 is 0.00586, above preregistered 0.005, and 17→33 is 0.067, above 0.02. `ell=300`: both error gates fail despite consistent positive sign. **No postrun tolerance changes or cherry-picking**.

## Read-only independent audit using the submitted NPZ

Original archive k nodes selected by mask: 322 in `0.03≤k_h≤0.20`; original LW02 CLASS `chi_s=5313.976587436474 Mpc`; exact frozen `h=0.673324639084866`, `A_s=2.1308864352626987e-9`, `n_s=0.9666229454895277`. At each of the submitted 65 `chi` points, interpolate `W(chi,k)` and `T_W=dW/deta` **only over log native k** to `k=(ell+0.5)/chi`. Form
```text
Pprim(k)=(2π²/k³) A_s(k/0.05)^(n_s-1)
G(chi)=4[(chi_s-chi)/(chi_s chi)]²/chi²
B(chi)=G Pprim W²
S(chi)=2G Pprim W T_W
```
and independently trapezoid `B`, `S`. Recovered the original reported four 65-node signed ratios at absolute discrepancy `<8e-17` using only uploaded LW01/LW02/LW03 arrays.

Along the `k(chi)` lensing sampling path, `T_W` was positive at **all 65 sampled points for each of the four multipoles**, while `W` changed sign 3, 1, 3, 1 times at ell 100,150,200,300 respectively. The resulting signed-derivative cancellation ratio `|∫S|/∫|S|` at 65 nodes was **0.05033, 0.67753, 0.20683, 0.21962**. In particular ell100's net derivative is only ~5% of the accumulated absolute signed contributions. This explains heightened sensitivity to the radial discretization. The sampled W zero crossings and cancellation are numerical diagnostics only, not physics-confirmed oscillation modes.

PCHIP reintegration using the 65 existing S and B samples is not independent perturbation-evolution information; no physical sign assertion can follow from dense interpolation alone.

## Frozen scientific decision

- **LW01 numerical PASS stands**: nonzero signed native Weyl tangent of externally driven linear AeST/positive-Drude memory model. Parent model unchanged.
- **LW03 source-time cross-closure PASS** at original native time nodes. The complete LW03 preregistered protocol **FAIL** due radial quadrature.
- Physical `C_ell^kappakappa` **sign and amplitude NOT certified**, `full_lensing_spectrum_certified=false`, `observational_detection=false`, H4 Ward and Z21 not certified.
- No more ad hoc 17/33/65-to-higher quadrature refinement is scientifically sufficient: evaluating the same CLASS interpolation operator more densely does not certify its independent time resolution, nor account for the missing line of sight, edge support, source distribution, gauge/physics consistency, finite eta and external observational sensitivity.
- **Stop boundary:** treat LW01 transfer-tangent as the achieved theoretical result. A separate lensing-physics continuation should first freeze a genuinely **independent source-time resolution plus extended k,z line-of-sight completeness** test, with a bounded computational cost and no parameter tuning, rather than simply repeating LW03 or tightening numerical tolerances after seeing these failures.
