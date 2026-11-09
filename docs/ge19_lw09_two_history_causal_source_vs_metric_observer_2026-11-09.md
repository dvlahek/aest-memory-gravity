# GE19 LW09 — smooth two-history memory theorem and Einstein–AeST observer boundary

**9 November 2026. Classification: GE19_LW09_SMOOTH_TWO_HISTORY_BATH_MEMORY_PASS_METRIC_OBSERVER_OPEN.** This is an analytic **prescribed-driver constitutive-bath** result, not a dynamically constructed pair of cosmological histories, not a Weyl metric observation, not a fitted or detected signal. The exact positive Drude spectrum and a negative post-pulse response were ALREADY established in the earlier GE19 note (ge19_physics_first_positive_drude_cosmological_algebraic_memory_tail_2026-11-09.md). The incremental contribution here is the smooth all-jets-identical pair and a precise source-to-observer limitation.

## 1. Original, frozen positive-memory constitutive law

For constant H>0, c=3H, tau>0 and relaxed auxiliary state, the original NL0B Drude bath has Laplace susceptibility

\[
K_H(s)=\frac{\tau\sqrt{s(s+c)}}{1+\tau\sqrt{s(s+c)}}.
\]

The exact step relaxation in the prior project derivation is

\[
f_H(t)=Z e^{-\alpha t}+\int_0^c \rho_H(\lambda)e^{-\lambda t}d\lambda,
\]
\[
D=\sqrt{c^2+4/\tau^2},\quad
\alpha=(c+D)/2,\quad Z=2/(\tau^2\alpha D)>0,
\]
\[
\rho_H(\lambda)=\frac{\tau}{\pi}
\frac{\sqrt{(c-\lambda)/\lambda}}
{1+\tau^2\lambda(c-\lambda)}>0,\qquad 0<\lambda<c.
\]

Consequently f_H(0)=1, f'_H(t)<0 and f''_H(t)>0 for t>0. With relaxed past, for any smooth prescribed driver X the normalized restoring response is

\[
B(t)=\int_{-\infty}^t f_H(t-s)\dot X(s)ds.
\]

## 2. Explicit smooth two-history counterexample

Fix T>eps>0, Xstar>0, and observation time t0=0. Take history A to be identically zero. Take history B to be the smooth nonnegative bump

\[
X_B(t)=
\begin{cases}
X_\star\exp\bigl(4-[u(1-u)]^{-1}\bigr),
&-T<t<-\epsilon,\quad u=(t+T)/(T-\epsilon),\\
0,&\mathrm{otherwise}.
\end{cases}
\]

Because X_B is exactly zero on a full neighborhood of t0, all instantaneous derivatives agree exactly with the reference:

\[
X_A^{(n)}(0)=X_B^{(n)}(0)=0,\qquad n=0,1,\ldots.
\]

Integration by parts with zero compact-pulse boundary terms proves

\[
B_B(0)=\int_{-T}^{-\epsilon}f'_H(-s)X_B(s)ds<0,\quad B_A(0)=0.
\]

The strict inequality follows from the positive spectral representation and the nonzero pulse. Since -f'_H is positive and decreases, the absolute response obeys

\[
[-f'_H(T)]\int_{-T}^{-\epsilon}X_B(s)ds
\le -B_B(0)\le
[-f'_H(\epsilon)]\int_{-T}^{-\epsilon}X_B(s)ds.
\]

This is a proved **effective constitutive-law** memory discriminator. It works also in the Maxwell H=0 limit; the constant-H algebraic tail provides an additional shape distinction but is not necessary for history dependence.

## 3. Exact scope of the instantaneous-competitor no-go

An instantaneous reduced constitutive law of finite order

\[
B_{\rm inst}(t)=F(t,X(t),\dot X(t),\ldots,X^{(N)}(t)),
\qquad F(t,0,\ldots,0)=0
\]

must give zero on both histories at t0, so cannot reproduce the strict difference above.

This does NOT disprove local dynamical gravity with hidden states. The original NL0B action itself is local and Markovian in the **enlarged** field state consisting of metric, aether, scalar and all positive auxiliary oscillator coordinates and momenta. Its reduced X-only description is retarded after eliminating auxiliary fields. An alternative hidden-field model, additive time-dependent external source, arbitrary scale/time operator, or another history-dependent law may mimic this bath response. The two histories have equal present X and all X derivatives but **not equal complete instantaneous internal state**.

## 4. What is gauge invariant, and what is not proven

On homogeneous FLRW the background aether-orthogonal scalar gradient

\[
X_\mu=h_\mu{}^\nu\nabla_\nu\phi
\]

vanishes, as does the relaxed bath backreaction B_mu. Their *linear perturbations* are therefore gauge invariant (Stewart–Walker zero-background criterion). The original scalar dictionary is X_i^(1)=partial_i chi, chi=varphi+Q alpha_aether, with longitudinal physical X_L=(k/a)chi. The Bardeen Weyl combination W=(Phi+Psi)/2 is independently gauge invariant.

But a pair of freely **prescribed** X histories is not automatically a pair of solutions of the coupled Einstein–AeST evolution/constraint system. Gauge invariance of a source does not establish nonzero metric response for an arbitrary source.

The original frozen action gives the spatial-aether linear source

\[
\Delta E_{\rm rhs}=-\frac{\eta Q(t)}2 B_{\chi,\mathrm{raw}}.
\]

For the *original constrained baseline linear operator* L_0 and source-entry J_E, any consistent first eta metric response has formal structure

\[
L_0\,\delta_\eta Z=J_E[-Q B_{\chi,\mathrm{raw}}/2],\qquad
\delta_\eta W=P_W\delta_\eta Z
=\int_{t_i}^{t}dt'\,G_{WE}(k;t,t')
[-Q(t')B_{\chi,\mathrm{raw}}(k,t')/2]
+\delta W_{\mathrm{initial}}.
\]

G_WE must include all metric constraints, aether/scalar redundancy, matter evolution and gauge conventions. The initial term vanishes only for fixed matched retarded initial states. LW01 **numerically demonstrated a nonzero signed native W eta tangent for the frozen baseline forcing**, consistent with at least some transfer to W, but it did NOT compute this Green kernel for the two new freely chosen histories.

### The actual physical observer gate

To turn this result into a causal metric test we must prove all of the following, without tuning observational residuals:

1. Two *dynamically admissible* Einstein–AeST–auxiliary solutions can realize suitable different past histories while sharing specified present accessible metric/matter controls (not merely X).
2. The coupled constrained retarded Green operator exists in the original fixed gauge/initial-data convention and has demonstrably nonzero action on the physical difference of histories at a gauge-invariant metric observer.
3. The metric response maps into a supported sky statistic, with physical eta normalization, complete relevant redshift/scale/angular windows, source n(z), bias and nuisance treatment. LW03 radial quadrature FAIL and LW05 full cosmic-shear LOS BLOCK are not lifted by this theorem.
4. A genuinely restricted Markov/instantaneous alternative and cosmic nuisance templates cannot reproduce the forecasted discriminant under independent held-out histories. A completely arbitrary mu(k,z) can fit a single response trajectory.

A result stopping before all four gates is not gravitational-memory **observation** or a Nature-level astrophysical discovery.

## 5. Frozen reproducibility and numerical illustration

Predata: ge19/lw09_two_history_constitutive_observer_gate_predata_20261109.json, committed before the example at **af7d11b1adb28fc8e71cf9ec8452cbe76ee0b9d8**, Git blob 1ce822be6a15640f43b5f1e6785e2a641dd8dde4. Canonical source code: ge19/lw09_two_history_constitutive_observer_20261109.py, commit c588453761a54510e24458996979cba9d00ac144. The example was independently computed with the same positive spectral formula using Gaussian nodes 96/192, **not** by executing the Git-locked canonical script against a local cloned repo. The independently run small replay JSON is stored in results/ge19_lw09_two_history_bath_archive_replay_20261109.json, commit 682ceeef813b2a5b4c93cef66cd6c0cb32ad3aa7; SHA256 b4c299911d339927eac978db0775447674843f2b3ed0bca837ac49835c46d3bd.

Illustrative dimensionless choices H=0.12, tau=1.7, T=5, eps=0.5, Xstar=1. The resulting bath forces are

\[
B_B(0)_{96}=-0.15126758553352906,\quad
B_B(0)_{192}=-0.15126758553352643,
\]

with relative quadrature difference 1.74312e-14. The spectral normalization is unity within floating precision and the rigorous bounds give 0.0382453 < -B_B(0) < 0.6934893. **No measured cosmological amplitude is inferred.**

## Decision

**PASS**: exact causal bath history dependence with a smooth no-finite-jet discriminator, and independent illustrative spectral quadrature consistency. **OPEN/BLOCKED**: dynamically admissible two-history Einstein–AeST pair and observer Green kernel; gauge-invariant W difference; complete calibrated observable and likelihood. Stop repeated CLASS sweeps; next work should first derive the original action's constrained source-to-metric observer map analytically.

Existing results unchanged: LW01 native signed Weyl PASS, LW03 radial FAIL, LW04 time sampling PASS, LW05 LOS BLOCK, LW06 cross-power PASS, LW07b DES metadata-only lens n(z) PASS with no observed fit, LW08 small differential source response UNRESOLVED, H4/Z21 uncertified.
