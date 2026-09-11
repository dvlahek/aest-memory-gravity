# ACT DR6 lensing: nonredundant F-state production fix — pre-data declaration

Date: 2026-09-11

## Motivation

R9 direct-LOS and the redundant F-balance experiment both failed the frozen `k_max_tau0_over_l_max` convergence gate. The redundant F experiment evolved both `E` and `F = K_B E + (2-K_B) chi`, creating an off-constraint direction `D = F-K_B E-(2-K_B)chi`. The present test removes that redundancy rather than adding another numerical degree of freedom.

## Frozen physical model

- AeST model: `Exp`
- `K_B = 0.0665`
- `tau H0 = 1`
- memory order: `39`
- same background/cosmological starting point and CLASS upstream commit as R9
- linear theory only
- ACT DR6 lensing likelihood v1.2, `act_baseline`, `lens_only=True`, `like_corrections=False`, `trim_lmax=2998`
- no primary-CMB likelihood
- direct line-of-sight lensing route: `want_lcmb_full_limber = no`

## Numerical representation under test

Replace the AeST perturbation state variable `E` by

`F = K_B E + (2-K_B) chi`

with no increase in state dimension. The evolved scalar state is therefore `(delta, theta, alpha, F)` rather than `(delta, theta, alpha, E, F)`.

Whenever the unchanged physical equations require `E`, reconstruct it algebraically as

`E = [F - (2-K_B) chi]/K_B`.

The pressure/stress closure uses the evolved `F` directly. The finite-memory and external tangent contributions are transformed exactly into the `F` equation. No cutoff, damping factor, UV regulator, new free parameter, altered cosmological parameter, or modified physical source term is allowed.

## Frozen certification gates

1. eta=0 memory on/off regression at final `k_max_tau0_over_l_max=3.0`:
   `relL2(Ckk_on,Ckk_off) <= 1e-8`.
2. k-support convergence at eta=0, comparing `k_max_tau0_over_l_max=2.4` and `3.0` after ACT binning:
   `relL2(binned_k30,binned_k24) <= 1e-2`.
3. Every lensing spectrum used by the gate must be finite and strictly positive on `L=2..2999`.

Failure of either gate stops the run before any eta scan and leaves ACT physics interpretation unlicensed.

## Conditional eta scan

Only if all certification gates pass, run the frozen eta grid

`eta = {0, 1/256, 1/128, 1/64, 1/32, 1/16, 1/8}`

at `k_max_tau0_over_l_max=3.0`, with the same ACT likelihood configuration. Record `chi2(eta)`, `Delta chi2` relative to eta=0, and the best grid point. This remains an exploratory linear-lensing result; nonlinear/Halofit AeST lensing is outside the scope of this run.

## Interpretation rule

- Gate PASS: the nonredundant F coordinate is numerically licensed for the frozen linear ACT scan, which proceeds in the same run.
- Gate FAIL: do not tune another numerical representation. The remaining k-support sensitivity is treated as a property requiring physical high-k/full-J/nonlinear completion rather than another CLASS lensing workaround.
