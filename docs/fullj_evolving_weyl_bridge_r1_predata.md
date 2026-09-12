# Full-J evolving-FLRW Weyl bridge R1 — effective-density closure repair predata

Status: **PREREGISTERED AFTER THE HISTORICAL R0 FAIL AND BEFORE ANY R1 WEYL OUTPUT**.

Frozen label: `FULLJ_EVOLVING_WEYL_BRIDGE_R1_PREDATA`.

## Historical result retained

The R0 bridge run at commit `1adb113c62fae8a9610fcc19b64fca0ffa325a9d` remains

`FULLJ_EVOLVING_WEYL_BRIDGE_FAIL`.

Its informative pattern was:

- G3 static full-J regression PASS at ~1e-15;
- G4 metric projection constraints PASS at ~1e-16;
- G5 finite output 27/27 PASS;
- G1 source traceability FAIL because the implemented density map was not the retained D2C5 effective-fluid density variable;
- G2 linear CLASS FAIL catastrophically;
- G6 slip FAIL as a downstream consequence of the huge erroneous metric correction.

No R0 result is reclassified.

## Fault identified

R0 treated the algebraic quantity

`Q P_chi/(6 a^3)`

as the full Newtonian-gauge Einstein density perturbation `delta rho_A`.

Although `P_chi=2 a^3 K_QQ U` is an exact canonical identity, D2C5 does not identify `Q K_QQ U/3` with the complete effective-fluid density source. The retained metric sector is expressed in the effective-fluid variables `(delta_A, Theta_A, Pi_A)`, with `delta_A` obeying its own continuity equation. Therefore the R0 algebraic density substitution was an incomplete metric-source map.

## Frozen R1 repair

The already locked scalar-current trajectory equations are unchanged. R1 augments the one-way metric post-processing system by one action-derived effective-fluid state `delta_A(x,t)`.

For each retained spatial point/mode, use the D2C5 relations

`Theta_A = -lap(chi/Q - alpha)/a`,

`rho_A = (Q K_Q - K)/3`,

`p_A = K/3`,

`w_A = p_A/rho_A`,

`c_ad^2 = K_Q/(Q K_QQ)`,

and

`Pi_A = c_ad^2 delta_A - c_ad^2 lap(K_B E + (2-K_B) chi)/(3 a^2 rho_A)`.

The conformal-time continuity equation is

`delta_A' = 3 Hconf (w_A delta_A - Pi_A) + (1+w_A)(3 Phi' - Theta_A)`,

where `Hconf=a H`.

The metric is reconstructed relative to the same corrected CLASS baseline. Define

`Delta rho_A = rho_A (delta_A - delta_A_CLASS)`,

`Delta q_A = (rho_A+p_A)(Theta_A - Theta_A_CLASS)`,

`Delta shear_A = 0`.

Use the same D2C6G Hamiltonian/momentum/shear projection as R0:

`X = Delta Phi' + Hconf Delta Psi`,

`k^2 X = (3/2) a^2 Delta q_A`,

`k^2 Delta Phi + 3 Hconf X + (3/2) a^2 Delta rho_A = 0`,

`k^2(Delta Psi-Delta Phi) + (9/2)a^2 Delta shear_A = 0`.

Thus the continuity equation uses

`Phi' = Phi_CLASS' + X - Hconf Delta Psi`.

This closes `delta_A` without a fitted Poisson law, slip function, interpolation parameter, or modification of the locked scalar-current trajectory.

Initial condition at the frozen D2C6 start redshift `z=6` is exactly the corrected CLASS effective-component density contrast at the same spatial realization:

`delta_A(z=6) = delta_A_CLASS(z=6)`.

The nonlinear completion still adds no retained shear source. Therefore R1 does not impose zero evolving slip: corrected CLASS baseline slip is retained, while the nonlinear correction has zero additional shear at this weak-field order.

## Numerical rule

Use the same `Nx=128`, `Nstep=4096`, fixed-grid classical RK4 interval and checkpoints as the locked D2C6 trajectory lineage. The canonical trajectory and `delta_A` are integrated together only as a triangular system: the canonical RHS never depends on the R1 density state or reconstructed R1 metric. Hence the locked scalar-current dynamics is unchanged.

No refit, rescaling, sign flip, mode removal, checkpoint removal, or threshold change is permitted.

## Frozen gates

R1 retains the original bridge scientific gates:

- G1 source traceability: every retained source relation must be action/D2C5 or corrected-CLASS traceable; closed algebraic identities `<=1e-12`.
- G2 linear CLASS regression: relative L2 for `Phi`, `Psi`, and `W=Phi+Psi` each `<=5e-3`.
- G3 static full-J regression: `<=1e-10`.
- G4 metric constraint residuals: Hamiltonian, momentum, shear each `<=1e-8`.
- G5 finite output: 27/27 members finite.
- G6 evolving-slip distinction: reconstructed slip must equal the retained CLASS slip to `<=1e-12` when the nonlinear completion adds no shear source, and the retained CLASS slip must not be silently overwritten by zero.

The R1 source-traceability audit no longer tests the invalid R0 statement that `Q P_chi/(6a^3)` is the complete Einstein density perturbation. It instead tests the exact D2C5 velocity map, `rho+p=Q K_Q/3`, `c_ad^2=K_Q/(Q K_QQ)`, and the zero additional nonlinear shear statement.

## Classification

All frozen R1 gates pass:

`FULLJ_EVOLVING_WEYL_BRIDGE_R1_PASS`.

A derived R1 system exists but one or more frozen gates fail:

`FULLJ_EVOLVING_WEYL_BRIDGE_R1_FAIL`.

The retained D2C5 equations are still insufficient to close the density/metric system without an extra assumption:

`FULLJ_EVOLVING_WEYL_BRIDGE_R1_INCOMPLETE_METRIC_CLOSURE`.

A PASS licenses a separately preregistered evolving-Weyl covariance/power diagnostic on this theory grid. It does not license ACT.

Always:

- `HISTORICAL_R0_FAIL_PRESERVED=True`
- `ACT_LIKELIHOOD_LICENSED=False`
- `OBSERVATIONAL_CLAIM_LICENSED=False`
- `NO_STATIC_W_EQUALS_2PHI_PROMOTION=True`
