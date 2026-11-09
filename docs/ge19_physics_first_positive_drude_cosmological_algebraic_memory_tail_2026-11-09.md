# GE19 — physics-first observable route: exact cosmological Drude memory tail

**Date:** 2026-11-09. **Theory:** frozen canonical NL0B AeST gravitational elasticity with positive continuum Drude spectrum; *no* new coupling, action, H4 repair, or numerical solver. **Classification:** ANALYTICALLY DERIVED CAUSAL MEMORY-RESPONSE THEOREM, METRIC OBSERVABLE AND DETECTABILITY OPEN.

## Scientific objective and frozen provenance

The frozen original NL0B covariant action uses the aether-orthogonal gradient \(X_\mu=h_\mu{}^\nu\nabla_\nu\phi\), a positive spectrum of auxiliary modes, and normalized restoring response
\[
B_\mu=\sum_j[w_jX_\mu-\omega_j\sqrt{w_j}\,q_{j\mu}].
\]
At linear order on FLRW \(X_L=(k/a)\chi\), and the *physical* first-eta correction to the aether equation is frozen as \(\Delta E_\mathrm{rhs}=-(\eta Q/2)B_{\chi,\mathrm{raw}}\), where \(B_L=(k/a) B_{\chi,\mathrm{raw}}\). The bath has no direct linear Einstein stress. Metric observables therefore require the **coupled linear Einstein+AeST response**, not simply plotting \(B\).

Original repository theory sources:
- \`docs/nl0b_covariant_memory_completion_result.md\`: exact positive continuum transfer \(K(A)=A/(1+A)\), \(A=\tau\sqrt{s(s+3H)}\).
- \`docs/gravitational_maxwell_viscoelasticity.md\`: \(H=0\) ordinary Maxwell stress relaxation, positive Drude continuum and finite \(H\) transfer; **did not previously derive the positive spectral decomposition or long-time power law below**.
- \`docs/gravitational_elasticity_canonical_nl0b_interpretation.md\`: local action and positive-bath energy.
- \`docs/linear_numerical_chain_closed.md\`, \`docs/v077_preserved_interpretation.md\`, \`docs/v078_preserved_interpretation.md\`: reproducible native-grid *matter-state* eta tangent, with precisely stated numerical provenance.
- \`docs/v067_v068_preserved_interpretation.md\`: **v0.68 linear matter/Weyl response FAIL**; no Weyl detection/certification imported from it.

**All following exact transform results assume:**
1. \(H>0\) **constant** in physical time; write \(c=3H\), \(\tau>0\).
2. The exact frozen **infinite positive continuum Drude spectrum**, not an arbitrary finite discrete bath or a gap.
3. Retarded/relaxed internal initial state; no freely excited auxiliary homogeneous modes.
4. Linear externally prescribed strain \(X(t)\) (the coupled metric response is a separate operator).
5. \(A(s)=\tau\sqrt{s}\sqrt{s+c}\) on the retarded branch continued from \(\mathrm{Re}\,s>0\).

## 1. Exact causal susceptibility

The existing continuum response is
\[
\boxed{\mathcal K_H(s)=\frac{B(s)}{X(s)}
       =\frac{\tau\sqrt{s(s+c)}}{1+\tau\sqrt{s(s+c)}}.}
\]
At high frequency \(\mathcal K_H(s)\to1\), while the formal static susceptibility is \(\mathcal K_H(0)=0\) for all \(H\ge0\).

At \(H=0\), \(\sqrt{s^2}=s\) on the causal Laplace branch:
\[
\mathcal K_0(s)=\frac{\tau s}{1+\tau s}.
\]
For a unit step in \(X\), the normalized stress relaxation \(f_H(t)\) has transform
\[
\widehat f_H(s)=\frac{\mathcal K_H(s)}s,\qquad
B_\mathrm{step}(t)=X_0 f_H(t).
\]
Thus \(f_0(t)=e^{-t/\tau}\).

## 2. NEW exact positive relaxation-spectrum representation at H>0

Set
\[
D=\sqrt{c^2+4/\tau^2},\quad
\alpha=\frac{c+D}{2}>c,\quad
Z=\frac{2}{\tau^2\alpha D}>0
\]
and on the interval \(0<\lambda<c\)
\[
\boxed{
\rho_H(\lambda)
=\frac{\tau}{\pi}
\frac{\sqrt{(c-\lambda)/\lambda}}
     {1+\tau^2\lambda(c-\lambda)}
>0 .}
\]

Then the **exact retarded step response for all \(t\ge0\)** is
\[
\boxed{f_H(t)=Z\,e^{-\alpha t}
       +\int_0^c \rho_H(\lambda)e^{-\lambda t}\,d\lambda.}
\]

**Derivation:** \(\widehat f(s)=\tau\sqrt{s(s+c)}/\{s[1+\tau\sqrt{s(s+c)}]\}\). With the retarded branch \(\sqrt s\sqrt{s+c}\), the only branch cut is \([-c,0]\); the only physical-sheet simple pole is at \(s=-\alpha<-c\), solving \(\tau\sqrt{\alpha(\alpha-c)}=1\) on the negative-real continuation. Its residue is \(Z\). For \(s=-\lambda+i0\), \(0<\lambda<c\), \(\sqrt{s(s+c)}=i\sqrt{\lambda(c-\lambda)}\), so
\[
-\frac1\pi\operatorname{Im}\widehat f(-\lambda+i0)
=\rho_H(\lambda).
\]
The inverse Laplace contour yields the above spectral representation, with **no missing pole or negative spectral weight**.

The initial-value theorem gives the exact **normalization**
\[
f_H(0^+)= Z+\int_0^c\rho_H(\lambda)\,d\lambda=1.
\]
Consequently \(f_H(t)>0\), \(f_H'(t)<0\) for finite \(t>0\), and
\((-1)^n f_H^{(n)}(t)\ge0\) for all \(n\ge0\): the response is **completely monotone**, a positive mixture of physical relaxation rates, despite its origin in a conservative positive oscillator bath. This is a stronger physical statement than a numerical “relaxation-like” plot.

**Important limit:** as \(H\to0^+\), the branch interval collapses, \(Z\to1\), \(\alpha\to1/\tau\), and \(f_H\to e^{-t/\tau}\). No contradiction with the ordinary Maxwell result.

## 3. NEW algebraic cosmological memory tail

Near \(\lambda=0\), the continuum density is
\[
\rho_H(\lambda)
=\frac{\tau\sqrt c}{\pi}\lambda^{-1/2}[1+O(\lambda)]
\quad(c>0\ \mathrm{fixed}).
\]
A direct Watson/Laplace asymptotic yields
\[
\boxed{
f_H(t)\sim \frac{\tau\sqrt c}{\sqrt{\pi t}}
=\frac{\tau\sqrt{3H}}{\sqrt{\pi t}},
\qquad t\to\infty,\ H>0\ \mathrm{fixed}.
}
\]
Thus the constant-\(H\) *positive Drude continuum* remembers a step as a \(t^{-1/2}\) tail; the \(H=0\) Maxwell response relaxes exponentially. The limits \(H\to0\) and \(t\to\infty\) are **non-uniform/noncommuting**.

At small positive harmonic frequency \(\nu\) in Fourier convention \(X(t)\sim e^{-i\nu t}\):
\[
\mathcal K_H(-i\nu+0^+)
\sim\tau\sqrt{3H\nu}\,e^{-i\pi/4}
\quad(\nu\to0^+,\ H>0\ \mathrm{fixed}),
\]
whereas at \(H=0\), \(\mathcal K_0(-i\nu)\sim-i\nu\tau\). The **fractional low-frequency exponent \(1/2\)** and the corresponding \(-45^\circ\) small-frequency phase (vs \(-90^\circ\) for \(H=0\)) are parameter-independent shape predictions within this idealized constant-H model.

Physical caveat: the asymptotic regime requires \(t\) sufficiently large that the small-\(s\) expansion holds, parametrically \(t\gg\max(c^{-1},c\tau^2)\); an actual evolving FLRW history \(H(t)\) may not remain approximately constant over that timescale. A finite or gapped bath has a different asymptotic. **Do not claim universal \(t^{-1/2}\) behavior in all real cosmic histories.**

## 4. NEW pulse history discriminator — stress persists after the driver vanishes

For \(X(t)=X_0[\Theta(t)-\Theta(t-T)]\), \(T>0\), the exact causal linear result is
\[
\boxed{B(t)=X_0\bigl[f_H(t)-\Theta(t-T)f_H(t-T)\bigr].}
\]
Because \(f_H\) strictly decreases, \(B(t)<0\) for all \(t>T\), even though \(X(t)=0\) then. At long times with fixed \(H>0\),
\[
\boxed{B(t)\sim
-\frac{X_0\tau\sqrt{3H}\,T}{2\sqrt\pi\,t^{3/2}}.}
\]
The negative *post-pulse counterresponse* distinguishes an instantaneous constitutive law from the retarded memory model without introducing a new free parameter.

For a general absolutely continuous strain history with relaxed past,
\[
B(t)=\int_{-\infty}^t f_H(t-u)\,\dot X(u)\,du,
\]
with the derivative interpreted as a Stieltjes measure if the driver jumps. Two source histories may have the same instantaneous \(X\) but different \(B\), i.e. genuine physical history dependence. **This is a bath constitutive prediction, not automatically an observable deflection angle or density contrast.**

## 5. Physical/observational bridge that does NOT require H4

The original linear perturbation hierarchy remains
\[
L_0 Z_{10}=0,\qquad
L_0 Z_{11}=-M_1[Z_{10},q_{10}],
\qquad
\Delta E_\mathrm{aether}=-\frac{\eta Q}{2}B_{\chi,\mathrm{raw}},
\]
where \(X_L=(k/a)\chi\) and the \(\eta\)-tangent fields/couplings are the **same** frozen v0.77/v0.78 construction. Extract a **gauge-invariant signed linear Weyl/Bardeen potential** \(\Phi_W=(\Phi+\Psi)/2\) by the same frozen gauge/conventions, and define only after its native-state transfer is independently validated
\[
T_{W,\eta}(k,z)=
\left.\partial_\eta \Phi_W(k,z)\right|_{\eta=0}.
\]
No H4 or \(Z_{21}\) is needed for this **linear** tangent. A gauge-invariant linear lensing projection / ISW source can then be built from \(\Phi_W\) (and, for ISW, its time derivative), but only on a physically valid linear scale/redshift window and before fitting observations.

**The critical distinction:** v0.77 only certified the native **total-matter state** tangent over \(0.03\le k\le0.20\,h/\mathrm{Mpc}\), \(0.2\le z\le1.5\); v0.78 separately diagnosed off-native power-time interpolation. **v0.68 Weyl tangent historically FAILed** its fixed-grid interpolation and global-affinity gates and must NOT be relabeled. Therefore a native-grid, signed, additive **Weyl** eta-tangent verification, together with same-node matter tangent controls and the exact original CLASS gauge/source dictionary, remains an **independent first observational gate**; do not claim linear Weyl detection today. The existing code \`v068/linear_scale_memory_response_map.py\` can inform provenance but its historical derived Weyl spectrum cannot be used as certification.

A defensible single next campaign (when execution resources are available) is *one preregistered, native-node, additive signed Weyl+matter tangent control* in the existing frozen v0.77 CLASS setup, not multiple arbitrary “repair” variants. Do not invent observational likelihoods or tune \(\tau,\eta,K_B\) against the data. Avoid ratios or log-power near zero crossings and do not infer transfer phase from power alone. After passing, a separate held-out tomographic lensing/ISW comparison could test a **real observable**. Strong-lensing/nonlinear structure, finite-eta, and H4-dependent weakly nonlinear lensing remain unlicensed.

## 6. Status and falsifiability

**Already follows analytically from the frozen theory, no new solver:**
- exact positive normalized step relaxation spectrum in constant H;
- strictly monotone positive relaxation;
- \(t^{-1/2}\) step and negative \(t^{-3/2}\) post-pulse tails for fixed \(H>0\);
- low-frequency \(1/2\) exponent with phase \(-\pi/4\);
- \(H\to0\) recovery of ordinary exponential Maxwell relaxation.

**Not demonstrated:**
- that a realistic \(H(t)\) retains those asymptotic powers;
- a measured gravitational strain \(X\) or memory force \(B\) in the sky;
- a nonzero, numerically certified *linear Weyl* eta transfer under the original v0.68 failed gates;
- a survey detection, significance, likelihood, or lensing spectrum;
- any new H4, \(Z_{21}\) or finite-amplitude backreacted cosmology.

**Research decision:** keep the Cr12ad original frozen H4 failure CLOSED. This independent analytic causal-memory signature plus the already certified v0.77 native matter-state signal is a physically meaningful route to an *independent linear observational prediction* without violating the H4 stop decision. Do not claim that a positive bath force alone constitutes an observational discovery.
