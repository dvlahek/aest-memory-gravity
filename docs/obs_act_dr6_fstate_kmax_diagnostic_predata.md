# ACT DR6 nonredundant F-state high-k diagnostic — pre-data declaration

Purpose: determine if the remaining direct-LOS kmax sensitivity of the linear AeST Exp implementation approaches a plateau or continues to grow when the ordinary CLASS line-of-sight k support is extended.

This is a diagnostic calculation only. It is not an ACT likelihood fit and does not license an observational claim.

Frozen model/numerics:
- CLASS upstream: e85808324f51fc694d12e3ed7439552a3c3f9540
- AeST model: Exp
- K_B = 0.0665
- tau H0 = 1
- memory order = 39
- eta = 0
- nonredundant evolved closure state F = K_B E + (2-K_B) chi
- E reconstructed algebraically as E = [F-(2-K_B)chi]/K_B
- linear theory only
- Newtonian gauge
- l_max_scalars = 4000
- want_lcmb_full_limber = no
- identical cosmological start point as the R9/F-state ACT lineage

Frozen kmax grid:
- k_max_tau0_over_l_max = 2.4, 3.0, 4.0, 5.0

Outputs:
- finite/positive C_L^{kappa kappa} check for L=2..2999
- full-spectrum relative L2 changes for every consecutive kmax pair and against kmax=5
- ratios at representative multipoles L = 10,20,50,100,200,500,700,1000,1500,2000,2500,2999
- local kmax growth exponent p_L = ln[C_L(5)/C_L(4)] / ln(5/4)
- compact descriptive classification:
  * PLATEAU_LIKE only if relL2(5,4) <= 0.01
  * SLOWING_BUT_NOT_CONVERGED if relL2(5,4) > 0.01 but is smaller than relL2(4,3)
  * NO_PLATEAU if relL2(5,4) >= relL2(4,3)

No threshold above is an observational or model-validity gate. The purpose is only to distinguish numerical saturation from continued high-k growth.
