# GE19 — action-quarter candidate finite-eta native-transfer result: first interpretation and physics stop

**2026-11-10. Original researcher WSL PASS — one fixed, post-selection numerical diagnostic only.**  
**Classification:** \`ACTION_QUARTER_FIXED_ETA_NATIVE_TRANSFER_PASS_PHYSICAL_ETA_WEYL_AND_DES_BLOCK\`.  
**Important:** no new CLASS job or observational fit was performed in this closeout. This is interpretation of the uploaded JSON and runner log; the results are **not** independent validations of the physical action-to-CLASS map.

## 1. Exact original WSL provenance and archiving

The following ORIGINAL user-provided bytes are archived unchanged in the dedicated action-quarter candidate GitHub branch and subsequently fetched with matching Git blobs:

| Evidence | SHA-256 | Git blob | Status |
|---|---|---|---|
| \`ge19/candidates/evidence/ge19_action_quarter_finite_eta_r1_runner.log\` | \`1f599799d371f87665cb2544ef29b7c670cf51c3d660bb7860d5a26f5ae09eba\` | \`b282a34ec5843528039b78ee2efb2e5db768c015\` | Actual current **PASS** |
| \`ge19/candidates/evidence/fixed_eta_transfer_diagnostic_20261110_r1.json\` | \`f54da0f1894b187deff3bdd3627bd115b586b77abc65ae314f3570873945f7c4\` | \`dbb29f08a66235c3be996db9d1e76cf5acabdfda\` | Actual current **PASS**, 147 native k points |
| \`ge19/candidates/evidence/ge19_action_quarter_preflight_old_argument_error.log\` | \`e7ea5b74ef75800ff1b7bb34067199ebeadf28920ba0f72409c835d2b313e7e9\` | \`cfce2d4065f4681bc2ec3f78f2d194b238cfad17\` | **Historical preflight argparser error** fixed in commit \`ec6adbdeccbaa083e1d0874bc420d3d6102fa4cf\`; NOT current physics failure |

Runner reports \`FINTE_ETA_SOURCE_PREFLIGHT_PASS\` (actual spelling \`FINITE_ETA\`), \`RUN_PASS candidate_eta0\`, \`RUN_PASS candidate_eta001\`, \`RUN_PASS historical_eta001\`, and \`FINITE_ETA_TRANSFER_DIAGNOSTIC_PASS 147\`; no full physical observer ready. Historical source SHA-256 \`276646d913348824bddf9e24138e4213ecc3fb8b605d21525bf9280474dbca80\` and candidate C source SHA-256 \`75bf9fe85f2aae85031edc109e131c6b5d1745dca8497300237e16e57c99f883\` match frozen source evidence. The prior \(\eta=0\) full background/matter P(k) byte-identity test remains PASS.

## 2. Actual measured differences from the diagnostic JSON, without embellishment

Frozen AeST Exp cosmology; \(\eta=0\) candidate and \(\eta=0.01\) candidate and historical half-source code; one \(z_{\rm pk}=0.5\), and 147 native transfer k samples. Weyl definition \(W=(\Phi+\Psi)/2\). Density column identified as **\`d_m\`** by the uploaded manifest (not \`d_tot\`).

Every \`half_minus_quarter_scaled_by_baseline\` value below is

\[
\frac{\max_k |T^{\rm historic}_{\eta=.01}(k)-T^{\rm candidate}_{\eta=.01}(k)|}
{\max_k|T^{\rm candidate}_{\eta=0}(k)|}
\]

(or the analogous P(k) column); it is **not** \(\max_k|\Delta T/T|\), an instrument forecast or a fractional comparison at fixed k.

| Quantity | Half vs quarter, max / max-baseline | Percent of max-baseline |
|---|---:|---:|
| Native \`d_m\` transfer | \(3.3597544509917483\times10^{-6}\) | \(0.0003359754450991748\%\) |
| Native \(\Phi\) transfer | \(5.790854076422126\times10^{-7}\) | \(0.00005790854076422126\%\) |
| Native \(\Psi\) transfer | \(5.793162813301304\times10^{-7}\) | \(0.00005793162813301304\%\) |
| \(W=(\Phi+\Psi)/2\) transfer | \(5.792008214664641\times10^{-7}\) | \(0.0000579200821466464\%\) |
| **\`density_W\` (transfer product)** | \(5.71012563979103\times10^{-6}\) | \(0.000571012563979103\%\) |
| Native matter \(P(k)\) at fixed z | \(4.36057507849327\times10^{-6}\) | \(0.000436057507849327\%\) |

For the quarter candidate **versus its own eta=0 baseline**, the maximum-baseline-normalized differences are \(3.482423051083672\times10^{-7}\) (W), \(7.939157405801136\times10^{-6}\) (\(d_m\)), and \(6.973721845075122\times10^{-6}\) (\(d_m W\) transfer product).

In particular:
- It is **proven that the two implemented CLASS paths produce distinguishable numerical arrays** for this input in the generated output, and both code paths finish without a reported error.
- It is **not** proven that those differences exceed a controlled discretization/solver/CLASS time-approximation error. The one-point z and max-normalized JSON are inadequate for a convergence or signed-shape judgment.
- The magnitudes are small. **No survey signal-to-noise can be inferred** from these percentages. They are not upper bounds on the projected DES \(\gamma_t\) difference because projection weights, possible sign reversals, bias, nuisance fits and z-dependence have not been evaluated.
- \`density_W\` is \(T_{d_m}(k)W(k)\) in native CLASS conventions; it is **not** the physically calibrated \(P_{\delta W}(k,z)\), which requires primordial normalization and the appropriate transfer/cross-power conventions.
- Old frozen \(\gamma=1/2\) remains **conditionally inconsistent with the original reduced action/CLASS dictionary** as shown in LW33. A finite output difference cannot substitute for full original action-to-CLASS proof.

## 3. Physics decision now — no more runs merely to collect PASS labels

**Evidence-based result:** the separately versioned \(\gamma=1/4\) source builds, has exact \(\eta=0\) equivalence to old code, and generates a nonzero but very small distinct native matter and Weyl transfer at the single positive \(\eta=0.01\) test.

**Production/observation:** \`PHYSICS_BLOCK\`. Complete action-to-CLASS mapping and Einstein constraint propagation, causal auxiliary initialization diagnostics, numerical resolution and physical eta-normalized matter–Weyl cross transfer are still unproven. No observed DES shear likelihood has been run. This does **not** disprove the theory or validate the historical half-source.

**Next zero-new-simulation data action:** inspect the *already generated* \`results/ge19_action_quarter_finite_eta_r1/native_transfer_comparison.npz\`: explicitly preserve sign and k support of \(\Delta\Phi(k),\Delta\Psi(k),\Delta d_m(k)\); check whether the quarter-vs-half difference is smooth, sign-changing, and located in DES-supported k. This may be done without rerunning CLASS. The current user upload did not include the NPZ; **do not invent its contents** or assert per-k conclusions. If arrays show only numerical noise or physically negligible signal, stop observational optimism rather than adding amplitude scans. If they show a coherent supported transfer pattern, the next physical gating task remains the **existing** P0 issue: complete constraint propagation / covariant source-to-CLASS justification, then one nuisance-marginal forecast before real DES comparison.

**No new LW phases, no blind parameter sweeps, no GitHub Actions, and no claimed gravitational-memory detection.**

## Linked original files

- [Fixed positive-eta JSON](../ge19/candidates/evidence/fixed_eta_transfer_diagnostic_20261110_r1.json)
- [Fixed positive-eta runner log](../ge19/candidates/evidence/ge19_action_quarter_finite_eta_r1_runner.log)
- [Historical preflight argument error](../ge19/candidates/evidence/ge19_action_quarter_preflight_old_argument_error.log)
- [Physics acceptance gate](ge19_physics_acceptance_decision_action_to_CLASS_2026-11-10.md), maintained as BLOCK
