# GE19 — DES Y3 Asimov r3: real covariance works, amplitude-only memory comparator is unidentifiable, physical memory still unknown

**2026-11-22. Observable pipeline checkpoint. Stop further flat-template Asimov reruns.**

## 1. Actual researcher WSL evidence and immutable files

[Original r3 JSON](../results/ge19_des_y3_asimov_20261122_r3.json) and [r3 log](../results/ge19_des_y3_asimov_20261122_r3.log), uploaded by researcher, archived byte-identically with Git blob SHA-1 \`b937b93d760b84055b5a65ee411e52627bff3045\`, \`d43519641391d53d431bc6ccad3827df12f9b71a\`; original SHA-256 \`a110483e346702560cf844a0c157648d3ff2f8c5e51ab34f6b166516c1c09800\`, \`8b61961b0276ad9f9a453005da49445860161e393f949232cc2773868c74adf5\`. Reuploaded r2 JSON/log match their existing Git archives exactly.

Researcher log:
\`\`\`
GE19_ASIMOV_PROJECTION_SELFTEST_PASS 3
GE19_DES_Y3_FROZEN_GR_COVARIANCE_PROXY_AMPLITUDE_DEGENERACY_PASS_ONLY
GE19_PHYSICAL_MEMORY_TEMPLATE_GO False
GE19_DES_DETECTION False
\`\`\`

The original OBS06 GR reference \`results/obs06_des_y3_gr/obs06_fixed_des_example_gr_192.npz\` matched frozen SHA-256 \`564542d47fa95d5b5fb3c5b0c8bb4eae1ecbc93f450bf993ea0bbb98310546e3\`. Validated allowlisted fields \`gr_fixed_unfitted_theory\`, \`published_covariance\`, \`lens_bin\` and \`source_bin\`. The NPZ also contains \`observed_gammat\` and \`signed_residual_observed_minus_gr\`, which **were not read by the Asimov numerical calculations**; their existence/type/shape appeared only through .npy headers. The input GR reference was one *unfitted fixed* public-example CosmoSIS point, not the official DES joint 3x2pt best fit.

Full covariance extracted for the original preselected MagLim foreground bin 4 with sources 3 and 4, **13 rows each = 26 rows**. Successful covariance Cholesky and rank 2 of 2 independent per-source amplitude nuisance columns.

## 2. Actual result: one negative control, not the predicted physical memory

Define a purely **artificial** flat fractional template \`t_flat=epsilon*mu_GR\`, with \`epsilon=-1.712922233834667e−9\` per unit eta imported from **one historical nonphysical, uncorrected-action CLASS Weyl tangent at one k,z point**. There is NO claim that the same fraction applies to DES gamma_t or any theta bin.

Let D consist of two nuisance columns \`mu_GR 1_{source=3}\` and \`mu_GR 1_{source=4}\`. The full DES covariance C enters its Cholesky-whitened SVD projector. Since \`t_flat=epsilon*mu_GR\` is in the column space of D:

\`\`\`math
F_\perp=t_\mathrm{flat}^{T}\left[C^{-1}-C^{-1}D(D^TC^{-1}D)^+D^TC^{-1}\right]t_\mathrm{flat}=0
\`\`\`
**exactly**, for any valid positive-definite C, even with infinite instrumental precision. This result is primarily an algebraic identifiability obstruction to shape-independent signals, not a claimed measurement of physical memory.

Actual values from user's original r3 JSON:

| Diagnostic | Result | Interpretation |
|---|---:|---|
| selected rows | 26 | 13 each source bins 3,4 |
| \`F_unprofiled\` | 2.7245822792610327e−15 | Artificial comparator only |
| \`SNR_eta1_unprofiled\` | 5.219753135217252e−8 | Artificial comparator only; **not physical forecast** |
| \`nuisance_amplitude_columns/rank\` | 2/2 | nuisance span validated |
| \`relative_whitened_projection_residual\` | 3.7090812926740735e−16 | numerical orthogonality at machine precision |
| \`F_profiled_numeric_roundoff\` | 3.748285229433295e−46 | **exact mathematical value zero**; roundoff, not signal |
| \`SNR_eta1_profiled_numeric_roundoff\` | 1.936048870621115e−23 | numerical artifact, not sensitivity |

**Scientific conclusion:** real DES covariance and a usable fixed GR model can be ingested, but the one-point historical Weyl fraction is demonstrably insufficient to make an identifiable shear memory hypothesis. This does **not** show the shape-dependent **physical** GE19 response is zero or absent; it was not supplied.

## 3. One genuinely needed next physics deliverable — no more toy templates

Calculate from the **original quarter-normalized covariant action with the admissible finite-k primordial state and true retarded bath history**, throughout preselected DES foreground-support k,z:

\`\`\`math
T_{\delta W}^{(0)}(k,z),\qquad
\left.\partial_\eta T_{\delta W}(k,z)\right|_{0^+,\mathrm{delayed}},
\quad W=(\Phi+\Psi)/2 .
\`\`\`

Avoid the GR Poisson shortcut that would artificially remove the modified-Weyl response. Where linear primordial fluctuations share a common seed, derive the *matter–Weyl* cross-spectrum derivative, including both the density and metric responses, e.g.

\`\`\`math
\partial_\eta P_{\delta W}
\;\propto\; \left(\partial_\eta T_\delta\right) T_W^{(0)}
+T_\delta^{(0)}\left(\partial_\eta T_W\right)
\`\`\`

with exact gauge, signed source conventions and primordial normalization, not merely a single \`W_1/W_0\` point. Isolate delayed-only response from the instantaneous bath stiffness in a mathematically stated decomposition, and include any physical \`eta\` derivative of the growing initial-state branch rather than silently freezing unphysical arbitrary initial conditions.

Only then project through the frozen DES Y3 MagLim4×Source4/Source3 actual lens/source kernels, full-support Limber or validated non-Limber angular propagation, calibrated \`J_2\`/window and scale cuts, galaxy bias/clustering, IA, magnification, photo-z, shear calibration, point-mass and baryonic nuisance, and covariance. For physical tangential-shear tangent \`t_phys=d\boldsymbol{\gamma}_t/d\eta\`, compute \`F_{\perp,\mathrm{phys}}\` with physically restricted instantaneous-only rivals and all nuisance columns. One must assess error floor and degeneracy, then decide whether observed DES Y3 data justify a hypothesis test or only an upper limit.

### Stop / GO criteria

- **OBSERVER_INFRASTRUCTURE_PASS:** historical fixed GR + actual covariance + 26-row mapping and linear nuisance projector. r3 establishes this restricted GO.
- **PHYSICAL_MEMORY_TEMPLATE_BLOCK:** original full action/adiabatic Ward, quarter source and retarded observer \`t_phys\` not certified.
- **PHYSICAL_ASIMOV_SENSITIVITY_BLOCK:** \`F_{\perp,\mathrm{phys}}\` not computable without \`t_phys\`.
- **DES_detection=false:** no observed residuals inspected, no observed detection or bound on physical memory.
- **No r4 for same flat-control:** all repeated synthetic or uniformly rescaled templates are knowingly degenerate.

Related [original GGL route](ge19_lw20_des_y3_ggl_weyl_observer_forecast_route_2026-11-10.md), [previous single physics gate](ge19_20261119_observability_return_single_gate_decision.md), and [historical signed delayed-Weyl tangent](ge19_20261121_delayed_only_weyl_native_tangent_signed_audit.md).
