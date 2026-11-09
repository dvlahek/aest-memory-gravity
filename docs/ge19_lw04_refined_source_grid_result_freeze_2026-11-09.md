# GE19 LW04 — completed original-model source-time-grid refinement

**Date:** 2026-11-09. **Frozen outcome:** `GE19_LW04_REFINED_SOURCE_GRID_AGREEMENT_PASS_LENSING_STILL_UNCERTIFIED`. **Pre-data froze before execution** at commit `afd9aae00700a8cabb1db0b2493f820720296a4c`. This is a numerically executed PASS for the **source-time grid refinement test** only; it is **not** a physical lensing, full LOS, nonlinear H4, or observational result.

## Evidence

Researcher submitted one local successful WSL batch, with exact filenames and cryptographic fingerprints; original bytes remain in local/conversation artifacts, rather than copied into Git:

| Source | SHA256 | Bytes |
|---|---|---:|
| `results/ge19_lw04_source_grid_refinement_20261109_zunionfix.json` | `6a1dfe9923daf385a9b78d0528eddeefd8442e0a28da9b60626814d30a435ac8` | 4,611 |
| `results/ge19_lw04_source_grid_refinement_20261109_zunionfix.npz` | `869502238bfc0cfdd7bcef0353b0d0b67051b79f1d5fb5b664d34c021b071106` | 1,234,814 |
| `results/ge19_lw04_source_grid_refinement_20261109_zunionfix.log` | `8edc7fba4517877a130e35eea2caebe2c73b2218d81d31abb720b3650dc0b3db` | 1,439 |

The complete three-CLASS-run log prints baseline, `+2.5` and `-2.5`, then ell=100/150/200/300 and final **PASS**. Parsed JSON agrees with log values. Independently read-only inspected the NPZ: it contains eight finite arrays, `W_refined_ell_{100,150,200,300}` and `TW_refined_ell_{100,150,200,300}`, each `(322,65)` float64. This is an output integrity check; the original `LW03` arrays used for differential comparisons are SHA-locked by the LW04 program.

Frozen parent files: LW01 JSON `ae49cb0d1e63d82080c092ca938beec4608afe2a0e30650b7d47b0513512014b`, LW01 NPZ `56172ff827d5314cbe066deaeec520f2062b4e4a646de7cb9fe509ae03c9dac9`; LW03 JSON `dcf057b8e51e4863f0c0765c11973de71db01240fce6421a691b3704869ae09d`, NPZ `f5b1334ab171e5e8df680ef6043969c91fbbafeb467bad8477d27ad4c94a0d53`. CLASS pinned HEAD `e85808324f51fc694d12e3ed7439552a3c3f9540`, no physical parameters changed. Original Drude force reused. Original `perturbations_sampling_stepsize=0.1` versus refined `0.025` is the sole intended numerical change.

## Outcome

**Native stored source-time grid grew from 24 to 89 points** (×3.7083); original source geometry `chi_s=5313.976587436474 Mpc` unchanged; max geometry relative error `1.328122282126371e-16`; exact CLASS Fourier k-prefix mismatch zero. All six global gates true: `all_ell_geometry`, `all_ell_source_resolution_checks`, `class_k_exact_prefix`, `fine_transfer_finite`, `source_chi_geometry`, `source_time_grid_increased`.

| ell | coarse original LW03 65-point ratio | LW04 refined 65-point ratio | W relative L2 | signed TW relative L2 | signed absolute-integral-normalized difference |
|---:|---:|---:|---:|---:|---:|
| 100 | +0.000298841034844 | +0.000299684770571 | 9.896924959e-6 | 0.0002385870265 | 0.0001419721795 |
| 150 | -0.012293429490432 | -0.012296198212980 | 1.025799187e-5 | 0.0003306260028 | 0.0001462029638 |
| 200 | +0.001323734141005 | +0.001324370623792 | 1.099768915e-5 | 0.0003093319420 | 0.0000967478359 |
| 300 | +0.001750524748284 | +0.001751361533712 | 1.019090482e-5 | 0.0004539161417 | 0.0000972632620 |

Primary `W` L2 differences all ~1e-5; signed derivative `TW` relative L2 differences <4.54e-4 (0.0454%); signed integral differences normalized against the LW03 integral of the **absolute derivative integrand** ~1e-4 (0.01%). These meet preregistered 1%, 1%, 5% numerical limits respectively. **These are not observed lensing percent changes.**

## Precise scientific implications

1. **Strong new control:** under the same cosmology, forcing, selected k/z paths and integrator tolerances, the Weyl transfer and its formal signed eta tangent are stable against the explicitly tested fourfold source-time sampling stepsize reduction in CLASS. This makes the sampled original native and offnative transfer results less likely to be a spurious consequence of the coarse original source-time sampling.
2. **LW03 radial FAIL preserved:** its 17/33/65 `chi` quadrature passes none of the preregistered composite ell gates; sign changes with quadrature at ell 100/200 remain a separate unresolved discretization issue. Refining the CLASS source time grid is NOT radial quadrature convergence.
3. **Finite-support limitation preserved:** only the original 0.03–0.20 h/Mpc, z=0.2–1.5 original window and per-ell truncated geometry were tested. The 65-point partial integrals (ell-dependent support) are NOT full line-of-sight observables and cannot be treated as measurements or significant predictions.
4. **No model identification:** this is an externally driven formal eta=0 tangent, not a finite physically calibrated coupling. A sufficiently flexible instantaneous gravity law can mimic one cosmological response history; a Nature-level observation would require distinctive cross-probe/multi-history evidence and physical competitor models.
5. **H4 unchanged:** original nonlinear Ward constraints and Z21 certification remain open; no earlier historical FAIL becomes PASS.

**Stop/go:** Close the LW04 source-time-grid diagnostic. The next *substantive* physics gate for Nature Astronomy is not another local source-time sweep. A separate, preregistered full-support **lensing forward operator** with independent radial integration convergence and physical normalization/units must be established first. Only afterward can DES Y3 or ACT DR6 observed bandpower residuals be evaluated for a hypothesis test. Treat any future full LOS solve as a distinct program with cost/stop gates, not a retroactive LW03 repair.

## Read-only LW03 LOS domain coverage diagnostic (not a signal fraction)

Using the unchanged LW03 NPZ `chi_ell_*` arrays, and `chi_s=5313.976587436474 Mpc` for the illustrative thin source plane at z=2, the **linear radial distance fraction** included by the ell-dependent original LW02/LW03/LW04 native support is:

| ell | low chi (Mpc) | high chi (Mpc) | retained chi-span / chi_s | excluded chi-span / chi_s |
|---:|---:|---:|---:|---:|
| 100 | 1035.782 | 4261.815 | 60.71% | 39.29% |
| 150 | 1282.872 | 4261.815 | 56.06% | 43.94% |
| 200 | 1786.006 | 4261.815 | 46.59% | 53.41% |
| 300 | 2292.615 | 4261.815 | 37.06% | 62.94% |

The included segments are not all `0<chi<chi_s` and their endpoints differ among ells. **These percentages quantify only unweighted comoving radial coverage, NOT the fraction of lensing power, derivative, observable significance or an upper bound on missing contributions.** The kernel, Weyl power, source selection, and low/high-k structure may weight the excluded segments very differently. The LW04 time-grid PASS is thus *strong evidence about one numerical axis* but does not support lifting the LOS stop-gate.
