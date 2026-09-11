# ACT DR6 lensing exploratory R9: certified direct-LOS bridge + eta scan (pre-data)

Status: **frozen before any R9 CLASS/ACT likelihood output**.

## Motivation

R7 validated the CLASS -> C_L^{kappa kappa} -> ACT DR6 standalone-lensing interface using GR. R8 then localized the AeST pathology to CLASS's `want_lcmb_full_limber=yes` route: the default switch at L=10 produced a sharp discontinuity, later switches produced oscillatory/negative auto-power values, while `want_lcmb_full_limber=no` produced a finite, positive, smooth AeST spectrum over L=2..2999.

R9 therefore does not attempt another blind full-Limber repair. It certifies the legacy/direct line-of-sight (LOS) CMB-lensing route at high k reach and, if that certification passes, immediately performs the frozen ACT eta scan on that certified route.

This is a numerical-route repair, not a theory change. No AeST equations, cosmological parameters, memory parameters, ACT data, likelihood settings, or eta-grid values are changed.

## Frozen code/model state

- Parent branch state: R8 HEAD `a7293637d8c1b2f2d436697a6c1f24005cc9a15b`.
- Upstream CLASS SHA: `e85808324f51fc694d12e3ed7439552a3c3f9540`.
- Same zero-safe finite-memory patch chain as R5-R8.
- Theory: linear only; no `non linear` entry.
- `l_max_scalars = 4000`.
- Base precision file: `v019p/pre/p3.pre`.
- Final certified LOS route adds:
  - `want_lcmb_full_limber = no`
  - `k_max_tau0_over_l_max = 3.0`
- A single convergence comparator uses `k_max_tau0_over_l_max = 2.4`.
- No interpolation, clipping, masking, sign repair, or replacement of C_L values is allowed.

## Frozen cosmology and AeST point

- H0 = 67.3324639084866 km/s/Mpc
- omega_b = 0.022377376877682164
- omega_cdm = 0.12006705327635288
- tau_reio = 0.06174082364515668
- n_s = 0.9666229454895277
- A_s = 2.1308864352626987e-9
- AeST Exp
- K_B = 0.0665
- tau H0 = 1.0
- memory order = 39

## Frozen ACT likelihood

- `act_dr6_lenslike==1.2.1`
- data version `v1.2`
- variant `act_baseline`
- `lens_only=True`
- `like_corrections=False`
- `trim_lmax=2998`
- 10 ACT bins
- no primary-CMB likelihood contribution

CLASS-format conversion is unchanged:

C_L^{kappa kappa} = (pi/2) L(L+1) D_L^{phi phi}.

## R9 certification stage

R9 computes, before any eta scan interpretation:

1. GR reference with CLASS default full-Limber route.
2. GR direct-LOS route with `want_lcmb_full_limber=no`, `k_max_tau0_over_l_max=3.0`.
3. AeST eta=0 direct-LOS route with `k_max_tau0_over_l_max=2.4`.
4. AeST eta=0 direct-LOS route with `k_max_tau0_over_l_max=3.0`.

All spectra must be finite and strictly positive for L=2..2999.

The certification gates are frozen as:

- GR ACT-binned direct-LOS vs full-Limber relative L2 <= 1e-2.
- AeST eta=0 ACT-binned kmax=2.4 vs kmax=3.0 relative L2 <= 1e-2.
- both GR likelihood values finite.
- both AeST eta=0 likelihood values finite.

No chi-square preference or AeST-vs-GR closeness is itself a gate.

If either relative-L2 gate fails, R9 stops before the eta scan and is classified `R9_DIRECT_LOS_CERTIFICATION_FAIL`.

## Frozen eta scan after certification

Only if all certification gates pass, use the final route

- `want_lcmb_full_limber=no`
- `k_max_tau0_over_l_max=3.0`

and scan exactly

eta = {0, 1/256, 1/128, 1/64, 1/32, 1/16, 1/8}.

No adaptive refinement or post-data grid modification is allowed inside R9.

For every point store:

- eta
- chi2
- Delta chi2 vs eta=0
- spectrum relative L2 vs eta=0
- Ckk min/max
- ACT binned theory vector

The best grid point is the minimum finite chi2. Interior/boundary status is descriptive only and is not a gate.

## Interpretation scope

If certification passes, R9 licenses interpretation of the **exploratory linear ACT DR6 direct-LOS eta scan**. It does not license a detection claim, because the nonlinear/Halofit AeST lensing interface remains unresolved and the scan is still a one-dimensional fixed-background exploratory test.

The purpose of R9 is to end the full-Limber numerical detour and return to physics using a validated CLASS route.