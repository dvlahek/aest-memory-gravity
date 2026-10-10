# GE19 D16 — original H1dot endpoint-Hermite GE05 physical-time bath bridge

**Freeze: predata and synthetic static checks only, 2026-09-26. No original physical D16 execution is included in this package.** Preserve all immutable original D13/D14/D15a physical archives and original Repair37 `SCIENCE_FAIL`.

## Physics object

The original H3F on-shell H1 parent contains the six positive-mode state `[N,S,u,phi,T,dr]` and cosmic-time derivatives `[Sdot,udot,phidot,Tdot]` at original `Nt128`/`Nt64` nodes. With original Repair13 scalar charge and unchanged action,

\[
 X_{10}=Q u+\frac{ik}{a}\phi,\qquad
 \partial_xX_{10}= -\frac{3K_Q}{K_{QQ}}u+
 \frac{Q}{H}\dot u+\frac{ik}{a}\left(\frac{\dot\phi}{H}-\phi\right),
 \quad x=\ln a.
\]

The interval cubic Hermite curve matches all four original on-shell endpoint jets. It remains a **surrogate**: no continuous-source H1 defect or rigorous `sup |X_H-X_true|` has been produced. The original Nt128/Nt64 nonnested-grid comparison is empirical only.

The original Repair24 analytic `step_linear_nd` is reused without modification, with exact original modes, weights, full original Repair26 initial state and positive original action `H(x)` reconstructed by D15a. For each fixed numerical substep [xa,xb] and `s=t/tau`,

\[
 \Delta s_{\rm phys}=\int_{x_a}^{x_b}\frac{dx}{\tau H(x)},\qquad
 h_{\rm eff}=\frac{x_b-x_a}{\Delta s_{\rm phys}}.
\]

The original kernel solves an affine approximation to the Hermite drive using this effective `h_eff`. Its numerical output carries both `z` and **physical-time** `v=dz/ds` continuously across all numerical and original knots. Thus it does not inherit the original R1 *x-embedded* spurious current jump. Finite substeps still have a smooth GE05 defect, including unknown true-H1 drive error. Gauss16 is fixed for the clock integral; the empirical time refinement is 4, 8, 16 substeps per original R1 interval. The original linear `X10` at physical-clock 16 substeps is a matched drive control. The original frozen R1 remains an immutable baseline.

At each original action knot, one-sided finite-substep original GE05 residuals satisfy

\[
 R_{\rm GE05}^{\pm}=\frac{3a^3}{\tau}\left(H_{\rm action}-\frac{h_{\rm eff}^{\pm}}{\tau}\right)v_{16},
 \qquad E_{q_j,10}^{\pm}=-\frac{\sqrt{w_j}}{2\omega_j}R_{\rm GE05}^{\pm}.
\]

This formula uses that the substep affine drive and Hermite surrogate agree at the original knot; the **unknown** true-drive discrepancy is separate and not set to zero as a physics claim. Both signed `+4 E_q\partial_\chi q` and noncancelling original six-positive/six-negative pair envelopes are saved. The one-sided smooth coefficients do not absorb D15a's distributional *x-embedded R1* impulses.

## Frozen scientific boundary

D16 must not claim a continuum H1 solution, an H1 interpolation error bar, an absolute all-interval bath error budget, a rigorous `Nq`/time error bound from two discretizations, actual original first-order GE05 bath on-shell, original full GE05/H4 Noether, external action boundary, original `E_{i00}\partial_\chi F_{i21}`, `Z21`, lensing or observational evidence. In particular, small `W` can arise through signed cancellation; report the unsigned envelope alongside it. High-phase original modes are **retained** throughout propagation, and any high-phase comparison is diagnostic only.

## Source and reproducibility

The companion preregistration fixes all original D13/D14/D15a SHA-256 parents, original source Git blobs, six-mode scope, all 12 original `C × Nt × Nq` cohorts, numerical substeps, clocks, and false-inference stops *before* any actual physical D16 run. The local runner rejects overwritten outputs and mismatched parents. The synthetic test uses an independent augmented-matrix-exponential affine oscillator, an analytic varying-H physical clock, exact Hermite endpoint derivatives and a missing-`a^-1` negative control.
