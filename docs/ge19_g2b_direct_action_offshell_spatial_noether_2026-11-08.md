# GE19 G2B — independent spatial-diffeomorphism variation of frozen reduced action

**Date:** 2026-11-08. **Classification:** `GE19_G2B_REDUCED_GE06_GE05_GE07_OFFSHELL_SPATIAL_ACTION_COVARIANCE_SYMBOLIC_PASS_Y2_AND_FULL_H4_OPEN`. **Analytical**, not a new H4 solve, stage-source tuning or original all-parent Ward certification.

## Exact action sectors and their diffeomorphism variations

Frozen original `ge06/analytic_aest_directional_source_generator.py` (Git blob `a7afe0035054a9dca55d74a6497c081422114b4c`):
```text
L_GE06 =
 N L R²[-4 kL kR -2 kR² + KB E²+2C E X -C X²+2K(Q)]
 +2N Rx²/L +4 Nx R Rx/L.
kL=(Lt-b Lx-L bx)/(N L), kR=(Rt-b Rx)/(N R)
sigma=(pt-b px)/N
Q=cosh(u)sigma+sinh(u)px/L
X=sinh(u)sigma+cosh(u)px/L
E=cosh(u)[(ut-b ux)/N+Nx/(N L)]+sinh(u)[kL+ux/L].
```
Frozen original `ge05/memory_directional_source_generator.py` (blob `40837d77f89028da30c28899e2d0530a4401844e`):
```text
L_GE05 = N L R²/4 [Aq²-(omega q-sqrt(w) Xphi)²]
Aq=cosh(u)(qt-b qx)/N + sinh(u)qx/L
Xphi=sinh(u)(pt-b px)/N+cosh(u)px/L.
```
Frozen original GE07 dust source `ge07/pressureless_matter_directional_source_generator.py` (blob `cde8da77a80799cef00fc7c09c3633310fc9e3d4`):
```text
L_GE07=N L R² rho[((Tt-b Tx)/N)²-(Tx/L)²-1].
```

Independent symbolic jet-prolongation checks on these original analytical action expressions give, for a smooth infinitesimal spatial diffeomorphism `xi(t,chi)`:
```text
delta scalar f = xi f_chi,
delta L = xi L_chi + L xi_chi,
delta b = xi b_chi + xi_t - b xi_chi,
delta L_t = xi L_tchi + xi_t L_chi + xi_chi L_t + L xi_tchi,
delta b_chi = xi b_chichi + xi_tchi - b xi_chichi,
delta q_t = xi q_tchi + xi_t q_chi.
```
Under these transformations the original coframe invariants `kL,kR,sigma,Q,X,E` are **exact scalars**, while `N L R²`, `Rx²/L` and `Nx R Rx/L` are weight-one spatial densities. The three original action densities consequently obey the **off-shell** identity
```text
delta_xi L_GE06 = d_chi(xi L_GE06)
delta_xi L_GE05 = d_chi(xi L_GE05)
delta_xi L_GE07 = d_chi(xi L_GE07).
```
Multiple negative controls (wrong or omitted `xi_t` shift connection, omitted `xi_tchi` shift derivative, omitted `L` density weight, omitted scalar q transformation) break the identity. These independent symbolic checks were **executed on source-derived formulas** in the chat container; repository AST/source Git-blob checking is implemented in the reproducible Python `ge19_g2b_direct_frozen_action_spatial_noether_variation.py` SHA256 `e7787c14328bc72fe20b6c38db11ec49986965fca2f694b307d0249171d1e448`, **not yet executed on researcher's original WSL repository**. Complete derivation manuscript SHA256 `1f343bca9194cd84cc1c9d12dc94977663116c9debe299a12a448dc9703f533c`.

## Physical Noether content, not numerical source fitting

At the original action-Euler level,
```text
W = sum_i E_i (d_chi F_i)
    - d_chi(L E_L - b E_b) - d_t E_b = 0.
```
After frozen background on-shell elimination the original mixed H4 relation is
```text
d_t E_b21 = R_parent - d_chi(a E_L21 + B_parent)
```
with first-order parent Euler terms, physical-eta bath parent `+4 sum E_q10 d_chi q10`, and original boundary terms retained. Action covariance does **not** imply an arbitrary sampled H4 source or the historical parent approximations satisfy the actual differential Ward identity.

Independent original GE05 current variation gives first-order `J_q10^t=a³ qdot10/2`. For an R1 numerical trajectory whose physical velocity jumps at an internal interface, original Euler source has the **distributional** coefficient `-[J_q^t]= -sqrt(w)/(2omega) Delta J_z`, exactly matching the original D15a1 frozen interface source. Do not add this distributional current coefficient to a smooth-time L2 norm, or conflate legacy R1 with separately validated D55Cr11f continuum representation.

Finite Radau source values (even all 255 of G2A) **do not determine a unique continuous derivative or actual signed complex shift Euler residue**. The frozen original GE06+GE05+GE07 action is spatially covariant, but the nonanalytic `Y2` action sector, actual first-order signed Euler parents, original boundary/interface currents, full physical clock, FD4/FD8+roundoff `B_total` remain **OPEN**. Consequently **no missing H4 gauge term or new scalar coefficient is proven**, and no H4 science result is upgraded.

**Next meaningful theoretical target:** derive original nonanalytic Y2 spatial Ward/current and verify the parent+boundary signed relation to a common physical-clock source, **not** another G2A source-amplitude comparison.

Preserve: D55Cr11f Cstar continuum GE05 H-channel PASS within scope; Cr12abR2 IMPLEMENTATION_FAIL and active shift SCIENCE_FAIL; Cr12ad campaign CLOSED; H4 active shift unchanged `<=1e-6`; temporal order unchanged `>=2.5`; `FULL_ORIGINAL_H4_WARD=false`, `Z21_CERTIFIED=false`, `LENSING_LICENSED=false`.
