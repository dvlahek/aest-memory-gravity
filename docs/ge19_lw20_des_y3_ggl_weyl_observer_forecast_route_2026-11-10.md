# GE19 LW20 — shortest defensible path to an observational gravitational-memory test: DES Y3 GGL

**10 November 2026. Classification: GE19_LW20_MAGLIM4_LENS_ONLY_SUPPORT_SCREEN_PASS_GGL_FORWARD_AND_FORECAST_BLOCKED.**

**Core decision:** switch the first observational test away from the **full cosmic shear κκ** line-of-sight transfer (LW05 FAIL/BLOCK on current k/z domain) to **DES Y3 galaxy–galaxy lensing** (foreground lens positions × background-source tangential shear), supplemented by galaxy clustering to control galaxy bias. This does **not** magically unblock GGL: its full forward, source n(z), integration tails and covariance are not yet certified. It does avoid an unnecessarily strong requirement that the *memory Weyl field itself* be modeled at every redshift between observer and source for an observable whose leading cross-correlation is localized by the **foreground lens distribution**.

Reference existing measurement/model methodology: DES Y3 Prat et al., *High-precision measurement and modeling of galaxy–galaxy lensing*, Phys. Rev. D 105, 083528 (2022), DOI 10.1103/PhysRevD.105.083528. The DES model includes intrinsic alignments, magnification, nonlinear/small-scale limits, bias, source shear and systematic nuisances. Prior Weyl analysis Tutusaus, Bonvin, Grimm, *Nature Communications* 15, 9295 (2024), DOI 10.1038/s41467-024-53363-6, already measured a MagLim-based Weyl evolution parameter. A generic Weyl-only evolution signal is **not new** and cannot be called evidence unique to memory.

## 1. Actual prior frozen evidence — no new CLASS runs or sky fits

Source files:
- The frozen researcher LW19 16/16 full reduced 1+1 temporal action Ward WSL JSON remains in results/ge19_lw19_reduced_full_action_temporal_invariance_20261110_r1.json, SHA-256 7a13c89f7387299f3ce20bc92716004c8096ea0f170ac7cd0739fcc50d44207e. This is a **reduced theory** proof, not a full action-to-CLASS bridge.
- Real DES Y3 calibrated **lens n(z)** source-support metadata: results/ge19_lw07b_des_y3_nz_only_audit_20261109.json, git blob 5323b8457cbe7e7426c3e6eb4345183c3660cbff. It did **not** read observed gamma_t or survey covariance and did **not** certify full source kernels. It calculates **lens n(z) probability-mass fractions**, not fractions of GGL signal.
- Matter–Weyl native source tangent numerical diagnostics: results/ge19_lw08_density_weyl_relative_tangent_20261109_archive_replay.json, git blob f3039640de268cd2136474f1ac716a80695b3713. The symmetric cross-spectrum product response was previously reproducible, while the **antisymmetric/differential matter–Weyl channel is UNRESOLVED** due to 74–199% relative disagreement among source amplification choices. λ=10,5,2.5,1.25 were purely numerical derivative amplifications, **not physical η**.
- Pre-observation candidate and formula lock ge19/lw20_ggl_observer_preforecast_predata_20261110.json, commit b402cd4f00f0b39bf54f354720fd138464b43fd7, git blob f3915e650e044433a4cec18efd3381848bdb7ec1. MagLim4/ell selection was made AFTER looking at lens n(z) support, **not** after looking at any new observed shear residuals. This is a transparent preforecast candidate, not an independently blinded discovery.
- Source-locked script ge19/lw20_ggl_preforecast_support_and_fisher_gate_20261110.py, commit b7125da20cd9f48a93ac2b7847e9101f5aca15b3. Not yet run in researcher's WSL. It reads frozen project JSONs only, checks selection and preconditions, and **refuses to report detection or σ_η** without physical source/survey data.
- Independently recomputed exact source-metadata audit results/ge19_lw20_ggl_observer_preforecast_support_archive_replay_20261110.json, commit d3b05fde064d0b59f2278b06ccc227053ea60a2c. It is a read-only replay, not the canonical code's WSL output.

## 2. Why GGL does not require full cosmic-shear Weyl support to source redshift

Use the original Newtonian-gauge transfer Weyl variable
\[
W(k,z)=\frac12\bigl(\Phi(k,z)+\Psi(k,z)\bigr)
\]
and, with one consistently specified convergence sign \(s_\kappa\in\{\pm1\}\), normalized foreground lens distribution \(n_L(\chi)\) **per comoving distance**, background source \(n_S(\chi_s)\), source lensing efficiency
\[
g_S(\chi)=\int_\chi^\infty d\chi_s\,n_S(\chi_s)\frac{\chi_s-\chi}{\chi_s}.
\]

In a spatially flat linear Limber/flat-sky approximation, a direct potential-based foreground–convergence angular cross power is, up to the explicitly fixed sign convention,
\[
\boxed{
C_\ell^{g\kappa}
=s_\kappa\,\ell(\ell+1)
\int d\chi\,
\frac{n_L(\chi)b_L(\chi)g_S(\chi)}{\chi^3}
P_{\delta_g,W}\!\left(k=\frac{\ell+1/2}{\chi},z(\chi)\right).
}
\]

This expression uses the **actual matter–Weyl** cross power rather than imposing the ΛCDM Poisson equation to turn W into matter power, which would inadvertently erase a possible modified-gravity response. \(P_{\delta_g,W}\) must be in a consistent gauge and physical sign/unit convention; matching galaxies to the underlying tracer requires bias, magnification, relativistic source effects where relevant and an explicit original CLASS dictionary.

**Essential distinction:** \(P_{\delta_g,W}\) is sampled primarily on **lens distances \(\chi\) where \(n_L(\chi)\) has weight**. The source galaxies enter through \(g_S(\chi)\), but the GGL cross spectrum does **not** require the Weyl perturbation \(W(k,z_s)\) to be numerically available at all background-source redshifts. By contrast, cosmic-shear κκ contains two broad lensing kernels and requires W/matter transfer across much of the total foreground path. Thus **LW05's cosmic-shear support BLOCK is not automatically a GGL support BLOCK**, although there are independent GGL support requirements.

A measured DES Y3 observable is the **binned \(\gamma_t(\theta)\)**, obtained through Hankel/J₂ or curved-sky angular windows with scale cuts and masking, not three isolated multipoles. Approximations and systematics require validation. The above formula alone is **not a DES likelihood**.

## 3. Data-supported narrow initial candidate — only a geometric screen

From archived actual DES Y3 calibrated lens n(z), sample **MagLim, lens bin 4**:

| Multipole | Lens n(z)-mass inside native k,z domain | Lens n(z)-mass outside |
|---:|---:|---:|
| ell 100 | 0.9967622379524206 | 0.0032377620475794 |
| ell 150 | 0.9963078304964734 | 0.0036921695035266 |
| ell 200 | 0.9927818494758363 | 0.0072181505241637 |
| ell 300, excluded screening control | 0.9755598951471407 | 0.0244401048528593 |

Original native support: \(k=0.03\text{–}0.20\,h\,{\rm Mpc}^{-1}\), \(z=0.24761975\text{–}1.38523688\), with eight distinct certified z nodes in primary window. We screened on **informational 99% n(z)-probability-mass** only. No source n(z), lensing-efficiency weighting, nontrivial bias/magnification, actual \(\gamma_t\) angular windows, or full modeled GGL signal has passed. **Even a 0.3–0.7% unsampled lens tail could contribute disproportionately to the observable integral.** It must not be dropped by assumption, extrapolation or artificial zero padding.

This sample/ell selection is **not** an optimal significance forecast or a Nature-level novelty claim. MagLim4 is motivated partly by comparison to existing published MagLim Weyl studies, but their J-hat constraints and reference z*=10 mapping must **not** be silently treated as measurements of the current eta model.

## 4. Decisive identifiability gate: marginalize galaxy bias and other nuisance parameters

A nonzero stable \(\partial_\eta P_{\delta W}\) is **not sufficient** for a distinctive detection. In a single lens bin the leading GGL \(C_\ell^{g\kappa}\) scales roughly with bias \(b_L\). If the memory tangent changes only the same overall amplitude across all accepted angular bins, it is **degenerate with nuisance galaxy bias**.

Let \(\boldsymbol t=\partial_\eta\boldsymbol\mu\) be a **physically calibrated** predicted DES data-vector derivative; \(D_{i\alpha}=\partial_{\nu_\alpha}\mu_i\) a nuisance design matrix; \(V\) the survey data-vector covariance; and \(P_{\nu}\) the nuisance-prior precision. For a Gaussian Asimov forecast (at fixed covariance),
\[
\boxed{
F_{\eta\eta}^{\rm marg}=
\boldsymbol t^TV^{-1}\boldsymbol t-
(D^TV^{-1}\boldsymbol t)^T
(D^TV^{-1}D+P_\nu)^{-1}
(D^TV^{-1}\boldsymbol t).
}
\]
If \(\boldsymbol t\) lies in an **unconstrained** nuisance-amplitude direction, the marginal Fisher information becomes zero even though \(\boldsymbol t\ne0\). Conversely a correct combination with galaxy clustering and multiple lens/source redshift bins may constrain bias/geometry degeneracies and preserve memory sensitivity; that must be **computed**, not assumed. Four small algebraic unit selftests in the LW20 executable cover no nuisance, exact collinearity, nuisance orthogonality and finite-prior regularization. Those are synthetic mathematical checks, **not** results for DES.

The LW08 unstable *antisymmetric* matter-vs-Weyl response is therefore a significant **physical identifiability risk**, not merely a request for smaller numerical error bars. Source-level symmetric amplitude may be easily absorbed by realistic nuisance freedoms and standard evolving-dark-energy effects. To argue unique memory, preregister a **shape/redshift/causal kernel** distinguishing a restricted memoryless rival with explicit shared nuisance parameters.

## 5. Exactly what is missing for a legitimate Asimov forecast

The next task must produce **one bounded forward campaign** with the following independently verifiable pieces:

1. **Physics input:** physically normalized \(\partial_\eta P_{\delta W}(k,z)|_{\eta=0}\), from original full coupled Einstein–AeST+NL0B including photon/baryon/neutrino and a verified action-to-CLASS stress/gauge dictionary. The existing frozen LW06 tangent is a candidate physics input only after its numerical λ and physical η normalizations and source-to-observer scope are checked.
2. **Support:** extend/validate the native transfer on the **foreground lens** redshift intervals and projected \(k=(\ell+1/2)/\chi(z)\), only where the actual GGL windows require it, with a converged radial quadrature. Do not attempt a full high-z cosmic-shear sweep merely to make LW05 green; **eight native lens-z nodes are not yet a certified GGL quadrature**.
3. **Survey response:** real calibrated DES Y3 MagLim4 **and background-source** \(n(z)\), lensing efficiency, measured lens-source angular \(\gamma_t\) bins/windows, scale cuts, covariance, mask and nuisance models (bias, IA, magnification, photo-z, shear calibration, point mass etc.). Do not substitute raw n(z)-mass support for a true angular/data-vector operator.
4. **Asimov discrimination:** freeze the approved cosmological and physical \(\eta,K_B,\tau\) prior assumptions; calculate nuisance-marginal \(F_{\eta\eta}\) for GGL and ideally jointly with galaxy clustering. If F is negligible, do **not** chase precision or tune a model to force detection; report a no-power/no-identifiability result.
5. **Only then** examine the observed data fit, with a held-out or appropriately corrected confirmatory design. Existing published MagLim Weyl J-hat constraints and generic geometry–matter tests mean an ordinary scale-dependent Weyl deviation alone is **not a new discovery claim**.

**Current output is NOT a forecast.** There is no licensed \(\sigma_\eta\), SNR, Δχ², percent shear change or observational detection for GE19. Existing LW03 radial FAIL, LW05 cosmic-shear LOS BLOCK, LW08 differential source UNRESOLVED, H4/Z21 uncertified and no full physical history-pair observable remain intact.

## 6. Minimal local command, no CLASS or DES data

This just verifies the frozen source-support facts and tests Schur-complement algebra, producing a fail-closed readiness JSON.

~~~bash
cd ~/aest-memory-gravity
git pull --ff-only
source .venv/bin/activate
set +e
set -o pipefail
python3 -u -m ge19.lw20_ggl_preforecast_support_and_fisher_gate_20261110 --self-test
python3 -u -m ge19.lw20_ggl_preforecast_support_and_fisher_gate_20261110 --out results/ge19_lw20_ggl_preforecast_support_20261110_r1.json
~~~

It is safe to run once; it refuses to overwrite output. Do not interpret its ready-to-screen status as a certified survey forward model. No more repeated LW19 reruns are needed.
