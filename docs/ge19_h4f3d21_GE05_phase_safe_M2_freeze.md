# GE19 D21 — original-action GE05 phase-safe M2 scalar-current derivative

## Problem and immutable input

The actual D20R1 `C_star, Nt=128, Nq=2048` five-source diagnostic passed. It also identified an original-knot FD4 GE05 bath Euler relative residual of `0.9987361238517092`, which is NOT interchangeable with the D19R1 action-clock sampled residual `0.00019634732715346443` at 256 bath substeps. Original M2 computed `-dt p_t^{(2)}` through FD4 on the 128 original times and thus its high-phase temporal contribution was unresolved.

All original sources and the D17, D19R1, D20R1 numerical results are SHA locked. No theory change, tolerance tuning, observational data or overwrite of the source parents is permitted.

## Source-action identity and exact algebra

For the original GE05 memory action `L=NLR^2 [A_q^2-(omega*q-sqrt(w)*Xphi)^2]/4` and original `epsilon`-second directional coefficient, the scalar-phi temporal current is **exactly**

`p_t^(2) = a^3*w*u_10*(z_10-X_10)` with `X_10=Q_action*u_10+phi_10,x/a` and normalized `q_10=sqrt(w)*z_10/omega`.

Its physical-time derivative, using the first-order ODE jet of the D19R1 bath and the D17 action H1 jet, is

`dt p_t^(2) = a^3*w*[(3H u_10 + dt u_10)*(z_10-X_10)+u_10*(v_10/tau - H*X_10,x)]`.

Only the scalar row of the original M2 contribution is changed by

`delta M2_scalar_mapped = +2*Fourier_low(sum_nodes(dt_pt_chain_rule - dt_pt_original_FD4))`.

The `+2` is the original **minus-two GE05-to-GE06 H4 RHS mapping** applied to raw scalar Euler `-dt p_t - dx p_x`. All other M2 rows are exactly preserved from the D20R1 NPZ.

The frozen source-only Ward projection uses shift (row 6), isotropic (row 1), and anisotropic (row 7) source rows, so its change is identically zero for this scalar-only M2 correction. This does **not** establish the full mixed Noether identity.

## Gates, controls and scope

The driver independently evaluates frozen original `ge05.f_c2['pt']` for every retained bath node and checks it against the exact normalized identity, including all original Gauss weights. It checks action D17 X and X_x, the original Repair07 cancellation-safe H1 reconstruction, exact D19 weighted bath replay, original FD4 stencil, scalar-only M2 support, and finite output. It reports the magnitude and signed Fourier structure of the phase-safe correction without a magnitude acceptance gate. Manufactured tests use both slow and high-frequency z; wrong jets and high-phase FD4 are negative controls.

This is a **conditional source-derivative numerical reclosure only**. D19R1 z/v at frozen knots are numerically converged but D17 continuous H1, all-interval GE05 on shell, the dependent physical q20/B20/M1 and Z11, all nonbath Euler/boundary terms, full H4 operator Ward, Z21 and lensing remain open. The old H3G B20/M1 appears only in a clearly labeled mixed comparison. Frozen Repair37 `SCIENCE_FAIL` remains immutable.
