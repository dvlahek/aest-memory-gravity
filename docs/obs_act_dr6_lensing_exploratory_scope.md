# Exploratory ACT DR6 lensing scan — frozen scope

Date: 2026-09-11

Status: frozen before evaluating ACT DR6 likelihood values with the corrected AeST+memory implementation.

## Historical status

D2C6H remains formally

`NL1C6D2C6H_FINAL_SELF_CONSISTENT_METRIC_FEEDBACK_TANGENT_FAIL`.

The H failure is preserved and is not repaired or relabeled here. Consequently this observational stage is explicitly **exploratory**. It may identify a preferred direction, a null response, or an approximate bound, but it does not by itself certify a detection or a final model constraint.

No additional intermediate nonlinear-box certification is introduced before this observational stage.

## Observable and likelihood

Use the official `ACTCollaboration/act_dr6_lenslike` likelihood with

- package version `1.2.1`;
- data version `v1.2`;
- `variant = act_baseline`;
- `lens_only = True`;
- `like_corrections = False`;
- default Hartlap correction retained.

This is the ACT-only DR6 lensing baseline likelihood without primary-CMB likelihood corrections.

The likelihood input is the convergence spectrum

\[
C_L^{\kappa\kappa}=\frac{[L(L+1)]^2}{4}C_L^{\phi\phi}.
\]

The conversion is performed explicitly from the CLASS raw lensing-potential spectrum.

## Frozen AeST+memory model

Use the same corrected CLASS v3.3.4 source commit and AeST cosmology inherited by the current project:

- CLASS upstream SHA `e85808324f51fc694d12e3ed7439552a3c3f9540`;
- `H0 = 67.3324639084866` km/s/Mpc;
- `omega_b = 0.022377376877682164`;
- `omega_cdm = 0.12006705327635288`;
- `tau_reio = 0.06174082364515668`;
- `n_s = 0.9666229454895277`;
- `A_s = 2.1308864352626987e-9`;
- one massive neutrino with `m_ncdm = 0.06 eV` and inherited temperature convention;
- Newtonian gauge;
- AeST Exp model;
- `K_B = 0.0665`;
- `Q0 = 1e-4 Mpc^-1`;
- `K2 = 9500`;
- `Z0 = 1e-17 Mpc^-1`;
- `tau H0 = 1`;
- validated compressed memory bath order `39`.

All cosmological and AeST parameters other than eta are fixed. This is not an MCMC and no nuisance or cosmological parameter is refit.

## Frozen eta grid

Evaluate exactly

`eta = {0, 1/256, 1/128, 1/64, 1/32, 1/16, 1/8}`.

This grid is fixed before inspecting ACT likelihood outputs and spans the finite-positive-eta scalar-current range already explored in D2C6D/E.

The scan reports for every eta:

- ACT DR6 lensing `lnL` and `chi2 = -2 lnL`;
- `Delta chi2` relative to eta=0;
- raw `C_L^{phiphi}` and converted `C_L^{kappakappa}` summaries;
- the best grid point only as an exploratory discrete-grid diagnostic.

No interpolation-based best fit, posterior interval, significance, or look-elsewhere claim is made in this stage.

## Perturbative scope

The linear CLASS observable uses the already implemented physical finite-eta memory closure

`E_rhs -> E_rhs - Q B_chi/2`

with the normalized Drude bath.

The corrected D2C6F-R2/H direct memory metric stress is **not** inserted into linear CLASS stress-energy. That action-derived direct stress starts at second perturbative order; treating it as a first-order CLASS source would mix perturbative orders. D2C6H remains relevant as a nonlinear-box feedback diagnostic, but its direct quadratic source is not part of this linear CMB-lensing spectrum.

## Theory settings

Use CLASS CMB/lensing spectra to `l_max_scalars = 4000` with lensing enabled. Use standard CLASS `halofit` as an exploratory nonlinear correction so that the ACT likelihood is not compared to a deliberately linear-only lensing template. This nonlinear prescription is not claimed to be an AeST-calibrated nonlinear structure model and is part of the exploratory status.

Before ACT values are interpreted, the same execution performs a technical eta-zero regression: memory enabled with `eta=0` must reproduce memory disabled for `C_L^{kappakappa}` to relative L2 `<= 1e-8` on `2 <= L <= 2999`.

## Output classification

Successful execution label:

`ACT_DR6_LENSING_EXPLORATORY_SCAN_COMPLETE`

Technical execution failure label:

`ACT_DR6_LENSING_EXPLORATORY_SCAN_INCOMPLETE`

A successful scan remains exploratory regardless of the sign or magnitude of `Delta chi2` because D2C6H remains a formal FAIL and because the nonlinear lensing prescription is not an AeST-specific calibration.
