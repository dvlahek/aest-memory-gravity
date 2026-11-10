# GE19 — native \(\Delta W(k)\) and \(\Delta d_m(k)\) at fixed positive eta: physical interpretation and stop

**Date:** 2026-11-10. **Input:** original researcher uploaded \`native_transfer_comparison.npz\`, 21,851 bytes, SHA-256 \`ca63e13a49b3b104fd65c06314a21d86734983a74e7427188cdeeb03bf9a85c5\`. **This input binary itself has not been pushed to GitHub; preserve local WSL original.** Its structure and values were directly read with NumPy and the calculations independently reproduced from its 16 finite float64 arrays. The separate [source-verified numeric summary](../ge19/candidates/evidence/ge19_native_transfer_npz_signed_shape_20261110.json) is available in the repository. This work **did not** invoke CLASS, modify any model parameter, inspect DES residuals, or run a new numerics campaign.

## Fixed inputs and distinction between a code difference and physical prediction

The saved arrays are from the original historical \(\gamma=1/2\) versus separately copied candidate \(\gamma=1/4\), both at fixed \(\eta=0.01\), frozen Exp cosmology and \(z=0.5\), with the candidate \(\eta=0\) baseline. The density transfer is explicitly labeled **\`d_m\`**, not \`d_tot\`. The 147 common original \(k\) nodes cover \(1.04974\times10^{-5}\) through \(0.304857\,h/{\rm Mpc}\). The previously screened DES *native k support only*, \(0.03 \le k\le0.2\,h/{\rm Mpc}\), contains 49 nodes, \(k=0.03015307\) to \(0.19784731\).

Define the actual **finite implemented difference**

\[
\Delta T(k)=T_{\rm historical,\,\gamma=1/2;\,\eta=.01}(k)-
             T_{\rm candidate,\,\gamma=1/4;\,\eta=.01}(k).
\]

The plotted quantity is \(10^6\Delta T(k)/\max_{\text{all }147\,k}|T_{\rm candidate,\eta=0}(k)|\), **not** pointwise \(\Delta T(k)/T(k)\), a derivative \(dT/d\eta\) or a DES \(\Delta\gamma_t\).

## Exact read-only calculations for \(0.03\le k\le0.2\,h/\mathrm{Mpc}\)

| Measured property (49 k nodes) | \(W=(\Phi+\Psi)/2\) | \(d_m\) |
|---|---:|---:|
| \(\max_k|\Delta T(k)|\) | \(3.159558091825332\times10^{-7}\) | \(0.019479727044199535\) |
| \(k\) of largest difference | \(0.06887276322009737\,h/{\rm Mpc}\) | same |
| \(\max|\Delta T|/\max_{\rm all}|T_0|\) | \(5.792008214664641\times10^{-7}\) | \(1.0229141494283504\times10^{-6}\) |
| Positive / negative \(\Delta T\) samples | 27 / 22 | 26 / 23 |
| Sign flips between adjacent \(k\) nodes | **26/48** | **22/48** |
| Median pointwise \(|\Delta T(k)/T_0(k)|\) | \(1.0785883724083863\times10^{-7}\) | \(6.57755951768846\times10^{-8}\) |
| Residual \(||\Delta T-aT_0||_2/||\Delta T||_2\) after best scalar amplitude \(a\) | **0.9503005849** | **0.9996658567** |
| Cosine of historical-vs-baseline and candidate-vs-baseline responses | **−0.0553993027** | **−0.1989131154** |
| \(||[T_h-T_0]-2[T_q-T_0]||_2/||T_h-T_0||_2\) | **1.3739827576** | **1.7704231830** |

At the largest \(|\Delta W|\) sample, \(k=0.0688727632\), the immediate neighboring \(\Delta W\) values are approximately \(-1.53146\times10^{-7}\) at \(k=0.06631181\), \(-3.15956\times10^{-7}\) at \(k=0.06887276\), then \(-1.51036\times10^{-8}\) at \(k=0.07142937\). The corresponding \(\Delta d_m\) values are \(+0.0113061\), \(+0.0194797\), then \(-0.00047645\): pronounced localized structure, not a slowly varying rescaling.

The added changes in the two metric potentials nearly coincide: \(\max_{\rm window}|\Delta\Phi-\Delta\Psi|\approx4.9960\times10^{-16}\) (difference of *source changes*, not the total \(\Phi-\Psi\)). This is consistent with an absence of new linear anisotropic-stress increment in the restricted model, **not** proof of all-sector physical gauge or constraint closure.

## Interpretation — not an instrumental sensitivity estimate

1. **No coherent sign-definite transfer memory signal was resolved.** The finite \(\eta\) code difference exists but is small and sign-oscillatory at neighboring k nodes. A low-order amplitude-only fit leaves 95% of the difference vector's L2 norm for W and 99.97% for \(d_m\); this rules out an *amplitude-only description of the generated difference*, but **does not** establish a physically distinctive scale-dependent memory signal.
2. **Source-normalization scaling not shown.** If the coupled model were in the strict small-\(\eta\) linear-response regime, \(\gamma=1/2\) versus \(\gamma=1/4\) would lead to approximately doubled deviations from the same \(\eta=0\) baseline. The large \(\|S_h-2S_q\|/\|S_h\|\) values (137% W, 177% \(d_m\) in this finite-sample norm) **do not support that simple expectation**. This could arise from numerical solver/precision effects, a failure to be in the perturbative regime, or another unverified code/initial-state condition. **This calculation cannot identify the cause.**
3. **Do not label fluctuations "numerical noise" as a proved diagnosis.** Oscillatory transfer spectra can have legitimate scale structure; this single \(z,\eta\) run contains no source/solver-resolution comparison or independent physical benchmark. There is insufficient evidence to certify the signed differences as physical or numerically converged.
4. **DES scope not certified.** Mere overlap with the original k interval at one redshift is not the DES GGL angular/LOS operator. The input has no calibrated \(P_{\delta W}\), source redshift kernels, galaxy bias/IA/photo-z nuisance marginalization, covariance or observed \(\gamma_t\). No \(\sigma_\eta\), signal-to-noise ratio, observational significance, or memory discovery follows.
5. **Scientific recommendation:** halt further unconstrained CLASS amplitude sweeps. Preserve the exact quarter-source normalization theorem in the analytic restricted sector and continue the **existing** physics P0 acceptance task if pursuing detection. If a full source-to-Weyl physical bridge is later independently established, one justified targeted numerical-error qualification (not a sweep for a preferred signal) can check whether this jagged response survives. Until then, classify **\`SHAPE_UNRESOLVED/PHYSICS_BLOCK\`**.

## Frozen evidence and ancillary visualization

- Original signed arrays on researcher's machine: \`results/ge19_action_quarter_finite_eta_r1/native_transfer_comparison.npz\` (SHA above), not yet GitHub-binary-archived.
- Original actual positive-eta result already archived in [fixed transfer JSON](../ge19/candidates/evidence/fixed_eta_transfer_diagnostic_20261110_r1.json) and [runner log](../ge19/candidates/evidence/ge19_action_quarter_finite_eta_r1_runner.log).
- Read-only analysis snapshot: [summary JSON](../ge19/candidates/evidence/ge19_native_transfer_npz_signed_shape_20261110.json). Local charts were generated for \(W(k)\) and \(d_m(k)\) without further CLASS runs; the graphical files remain in the conversation artifacts, not claimed as GitHub-archived.
- Original observational selection: [LW20 GGL plan](ge19_lw20_des_y3_ggl_weyl_observer_forecast_route_2026-11-10.md).
- Open physics acceptance: [action-to-CLASS gate](ge19_physics_acceptance_decision_action_to_CLASS_2026-11-10.md), issue #2.

**Scientific status:** \`GE19_NATIVE_SIGNED_K_SHAPE_UNRESOLVED_NOT_A_MEMORY_DISCOVERY\`. Retain negative/null results and avoid post-hoc source rescaling.
