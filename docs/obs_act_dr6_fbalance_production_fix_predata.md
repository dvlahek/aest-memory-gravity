# AeST ACT DR6 F-balance production repair — pre-data declaration

This declaration is frozen before running the repaired CLASS/ACT calculation.

## Problem fixed

R9 established that the ACT likelihood and the direct line-of-sight GR calculation are numerically healthy, but the AeST lensing prediction is not converged when the ordinary CLASS integration range is increased from `k_max_tau0_over_l_max=2.4` to `3.0`. The current AeST perturbation implementation reconstructs the pressure-gradient combination

\[
F \equiv K_B E + (2-K_B)\chi,
\qquad
\chi=Q\left(a\theta/k^2+\alpha\right),
\]

by subtracting two separately evolved quantities and then multiplies it by `k^2/(a^2 rho)` in the pressure perturbation. The repair changes only the numerical representation: `F` is added as a redundant state and evolved directly from the already implemented equations. No physical equation, cosmological parameter, memory kernel, likelihood setting, amplitude, scale cut, or fitting freedom is changed.

Writing `B=2-K_B`, the unchanged equations imply exactly

\[
F' = a\left[\left(\frac{BQ}{K_B}-H\right)F
+\left(K_Q-\frac{2BQ}{K_B}\right)\chi\right]
+F'_{\rm mem}+K_B f_{\rm ext},
\]

where the existing finite-memory closure contributes

\[
F'_{\rm mem}=-\frac{aQ}{2}B_{\chi,\rm mem},
\]

and `f_ext` is the already existing optional variational forcing added to `E'`. This identity follows algebraically from the current `theta`, `alpha`, and `E` equations together with the implemented background identity `Q'/Q=-3(aH)c_ad^2`. The large `Pi` terms cancel analytically before floating-point evaluation.

`E`, `alpha`, matter variables and all finite-bath variables remain evolved exactly as before. `Pi_aest` is evaluated from the directly evolved `F` instead of reconstructing `K_B E + (2-K_B) chi` at every RHS call. The regular adiabatic initial condition is `F=0`, identical to the existing leading-order `E=chi=0` condition.

## Frozen model and likelihood

- upstream CLASS: `e85808324f51fc694d12e3ed7439552a3c3f9540`
- same patch lineage as R9, with the F-balance repair appended last
- AeST Exp model
- `K_B=0.0665`
- `tau H0=1`
- memory order `39`
- linear CLASS lensing only; no nonlinear/Halofit correction
- `l_max_scalars=4000`
- ACT DR6 lensing likelihood `act_dr6_lenslike==1.2.1`, data v1.2
- `variant=act_baseline`, `lens_only=True`, `like_corrections=False`, `trim_lmax=2998`
- fixed cosmology identical to R9/R7
- eta grid `0, 1/256, 1/128, 1/64, 1/32, 1/16, 1/8`

## Frozen certification gates

Before any eta scan is interpreted physically, the same run must satisfy all of the following:

1. CLASS completes with finite, strictly positive `C_L^kappakappa` over `L=2..2999`.
2. At eta=0, memory-on and memory-off spectra agree to relative L2 <= `1e-8`.
3. AeST direct-LOS convergence between `k_max_tau0_over_l_max=2.4` and `3.0` has ACT-binned relative L2 <= `1e-2` (the same gate used in R9).
4. The repaired eta=0 spectrum contains no negative or non-finite ACT-support multipoles.

No chi-square value, eta preference, sign, monotonicity or detection threshold is a certification gate.

If all gates pass, the same executable continues immediately to the frozen seven-point eta scan and reports ACT chi-square and Delta-chi-square. In that case an exploratory **linear-theory ACT physics interpretation** is permitted. `OBSERVATIONAL_CLAIM_LICENSED` remains `False` because the nonlinear/Halofit sector is still outside this certification.

If any gate fails, the eta scan is not physically interpreted and no ACT model claim is licensed.
