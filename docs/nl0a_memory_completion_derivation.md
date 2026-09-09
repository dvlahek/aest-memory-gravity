# NL0A — local conservative memory completion candidate

Status: **NL0A_STRUCTURAL_REDUCTION_COMPLETE_FULL_VARIATIONAL_MATCH_PENDING**

This note follows the closed linear chain (v0.77/v0.78 PASS) and the NL0 equation audit. Its purpose is not to introduce a phenomenological nonlinear damping term. It reconstructs the preserved Drude memory as a local positive auxiliary-field system on the aether-orthogonal spatial sector and asks which part of the nonlinear completion is already fixed by the frozen linear model.

## 1. What the old bath audits already fix

The historical v0.19k–v0.19s sequence is stronger than a generic fitted memory ansatz.

For locally constant H,

\[
A^2=\tau^2 s(s+3H),
\]

and the exact retarded Drude response is

\[
K(A)=\frac{A}{1+A}.
\]

A positive oscillator realization gives

\[
K_N(A)=\sum_j w_j\frac{A^2}{r_j^2+A^2},
\qquad r_j=\omega_j\tau,
\]

with \(w_j>0\), \(\omega_j>0\). The continuum measure is

\[
d\mu(\omega)=\frac{2}{\pi}\frac{d\omega}{1+\omega^2},
\]

or, after \(\omega=\tan\theta\), simply \(d\mu=(2/\pi)d\theta\). The v0.19r construction therefore used a direct positive quadrature of a conservative continuum, not a source-dependent negative-weight fit.

The frozen CLASS bath equation is

\[
q_j''+2\mathcal Hq_j'+a^2\omega_j^2q_j
=a k\omega_j\sqrt{w_j}\,\chi,
\]

which in cosmic time is

\[
\ddot q_j+3H\dot q_j+\omega_j^2q_j
=\omega_j\sqrt{w_j}\,\frac{k}{a}\chi.
\]

The raw bath backreaction is

\[
B_{\chi,\rm raw}=\sum_j\left[
w_j\chi-\sqrt{w_j}\frac{a\omega_j}{k}q_j
\right],
\]

and the frozen AeST closure is

\[
\Delta E_{\rm rhs}=-\frac{\eta Q}{2}B_{\chi,\rm raw}.
\]

## 2. Key structural observation: the bath is naturally vectorial in real space

The factor \((k/a)\chi\) is not evidence for a fundamentally nonlocal spatial kernel. It is the scalar Fourier amplitude of a spatial gradient.

Define an aether-orthogonal spatial covector \(X_\mu\) whose scalar linear perturbation obeys

\[
X_{\hat i}^{(1)}=\frac{1}{a}\partial_i\chi.
\]

The natural fundamental AeST candidate is the spatial projection of the scalar gradient,

\[
X_\mu \equiv h_\mu{}^\nu\nabla_\nu\phi,
\qquad
h_{\mu\nu}=g_{\mu\nu}+A_\mu A_\nu.
\]

It vanishes identically on the homogeneous FLRW background. At first scalar order its potential is the familiar relative scalar/aether perturbation \(\delta\phi+\bar Q\alpha\). The repository bridge uses

\[
u_A=\frac{a\Theta_A}{k^2},
\qquad
\chi=Q(u_A+\alpha).
\]

Thus the remaining dictionary identity that must be checked explicitly against the published AeST perturbation conventions is

\[
\delta\phi=Q u_A,
\]

including the sign and scale-factor convention. If this identity holds, then \(X_{\hat i}^{(1)}=(1/a)\partial_i\chi\) exactly. This dictionary check is the only unresolved kinematic step in this section; it must not be assumed silently.

## 3. Local auxiliary-vector realization

Introduce, for every positive bath node, an aether-orthogonal auxiliary vector

\[
A^\mu U_{j\mu}=0.
\]

Let \(\mathscr D_A\) denote the projected derivative along the aether, acting on physical spatial components. The minimal conservative bath sector is the Caldeira–Leggett-type square

\[
\mathcal L_{\rm mem}
=\frac12\sum_j\left[
\frac12\,|\mathscr D_A U_j|^2
-\frac12\left|\omega_j U_j-\sqrt{\eta w_j}\,X\right|^2
\right].
\]

Equivalently, expanding the square,

\[
\mathcal L_{\rm mem}
=\frac14\sum_j\left[
|\mathscr D_A U_j|^2-\omega_j^2|U_j|^2
+2\sqrt{\eta}\,\omega_j\sqrt{w_j}\,U_j\cdot X
-\eta w_j|X|^2
\right].
\]

The \(\sqrt\eta\) parametrization is important. At \(\eta=0\) the physical auxiliary field decouples regularly. Writing

\[
U_j=\sqrt\eta\,V_j
\]

for \(\eta>0\), the normalized response field \(V_j\) has a finite \(\eta\to0\) limit. This is the action-level counterpart of the raw bath that was used in the certified eta=0 tangent.

The overall normalization shown here is selected so that the spatial aether variation has the frozen factor \(1/2\). A full variation in AeST conventions is still required before this is promoted from candidate to completed theory.

## 4. Exact bath equation at linear order

Varying with respect to \(U_j\) gives the projected oscillator equation. On FLRW, for the physical longitudinal scalar amplitude,

\[
\ddot U_j+3H\dot U_j+\omega_j^2U_j
=\sqrt\eta\,\omega_j\sqrt{w_j}\,X_L.
\]

With

\[
X_L=\frac{k}{a}\chi,
\qquad
U_j=\sqrt\eta\,q_j,
\]

we obtain

\[
\ddot q_j+3H\dot q_j+\omega_j^2q_j
=\omega_j\sqrt{w_j}\frac{k}{a}\chi,
\]

and therefore, after \(dt=a\,d\tau\),

\[
q_j''+2\mathcal H q_j'+a^2\omega_j^2q_j
=a k\omega_j\sqrt{w_j}\chi.
\]

This is exactly the preserved CLASS bath equation.

## 5. Exact backreaction variable

Variation of the bath potential with respect to \(X_\mu\) gives

\[
\frac{\partial\mathcal L_{\rm mem}}{\partial X^\mu}
=-\frac{\eta}{2}\sum_j
\left[w_jX_\mu-\omega_j\sqrt{w_j}\,q_{j\mu}\right].
\]

Define

\[
\mathcal B_\mu
\equiv
\sum_j\left[w_jX_\mu-\omega_j\sqrt{w_j}\,q_{j\mu}\right].
\]

For a scalar Fourier mode,

\[
\mathcal B_L
=\frac{k}{a}\sum_j\left[
w_j\chi-\sqrt{w_j}\frac{a\omega_j}{k}q_j
\right]
=\frac{k}{a}B_{\chi,\rm raw}.
\]

Thus the apparently Fourier-specific frozen quantity \(B_\chi\) is simply the scalar potential of a local spatial backreaction covector. No \(\sqrt{-\nabla^2}\) operator is required if the nonlinear completion is written in terms of spatial vectors rather than scalar potentials.

## 6. The old Drude kernel follows automatically

At fixed H, Laplace transforming the normalized oscillator equation gives

\[
q_j(s)=
\frac{\omega_j\sqrt{w_j}}{s^2+3Hs+\omega_j^2}
X_L(s).
\]

Therefore

\[
\frac{\mathcal B_L}{X_L}
=\sum_j w_j
\frac{s(s+3H)}{s(s+3H)+\omega_j^2}.
\]

With

\[
A^2=\tau^2s(s+3H),
\qquad r_j=\omega_j\tau,
\]

this becomes

\[
\frac{\mathcal B_L}{X_L}
=\sum_j w_j\frac{A^2}{A^2+r_j^2}=K_N(A),
\]

exactly the v0.19k finite positive oscillator transfer function. Taking the positive continuum measure reproduces

\[
K(A)=\frac{A}{1+A}.
\]

This establishes that the local auxiliary-vector construction is not a new response model. It is a real-space realization of the already preserved Drude bath.

## 7. Why the FLRW and linear-stress controls are automatic

On exact FLRW,

\[
X_\mu=0,
\qquad U_{j\mu}=0,
\]

so

\[
\mathcal L_{\rm mem}^{(0)}=0.
\]

Hence there is no homogeneous memory background correction.

Moreover \(X_\mu\) and \(U_{j\mu}\) are both first-order around FLRW, while the bath action is quadratic in them. Its direct metric stress therefore begins at second perturbative order. This reproduces the preserved source audit statement that there is no direct linear memory Einstein stress.

## 8. Relation to the frozen E closure

Because

\[
X_\mu=h_\mu{}^\nu\nabla_\nu\phi,
\]

a spatial variation of the aether changes \(X_\mu\) at first order by a factor proportional to the homogeneous scalar velocity \(Q\). The bath variation therefore supplies a spatial aether force proportional to

\[
-\frac{\eta Q}{2}\mathcal B_\mu.
\]

Taking the scalar potential gives precisely the target structure

\[
\Delta E_{\rm rhs}
=-\frac{\eta Q}{2}B_{\chi,\rm raw}.
\]

**This coefficient-level match is structural but not yet the final variational proof.** A full variation of \(S_{\rm AeST}+S_{\rm mem}\), with the unit-aether constraint and the exact perturbation conventions, must show that the complete first-order scalar system reduces to the frozen implementation without an additional independent linear equation or source that the CLASS bridge omitted.

## 9. What NL0A has solved

The previous NL0 concern about the single Fourier factor \(k\chi\) is resolved at the structural level:

- the drive is a local spatial gradient;
- the nonlinear auxiliary objects can be local aether-orthogonal vectors;
- the positive fixed-frequency Drude bath is retained exactly;
- causality is provided by the retarded initial-value problem;
- positivity/passivity is inherited from \(w_j>0\), \(\omega_j>0\);
- the homogeneous memory correction remains zero;
- direct memory Einstein stress remains absent at linear order;
- the eta=0 raw-bath limit is regular under \(U_j=\sqrt\eta q_j\);
- the frozen oscillator equation, finite kernel, and \(B_\chi\) structure are recovered exactly.

This is substantial progress: the nonlinear memory extension need not be spatially pseudodifferential or mode-by-mode.

## 10. What is still blocked

NL0A is **not** yet a full nonlinear AeST+memory theory. Two items remain before NL1 can start.

### NL0B-1 — perturbation dictionary proof

Verify directly from the AeST perturbation definitions that

\[
X_{\hat i}^{(1)}=\frac1a\partial_i\chi
\]

with the repository convention \(\chi=Q(u_A+\alpha)\), including all signs and factors of \(a\).

### NL0B-2 — full variational closure

Vary the combined action through first order around FLRW and verify all of the following simultaneously:

1. the bath oscillator equation is the frozen one;
2. the only independent memory modification of the frozen scalar closure is
   \(\Delta E_{\rm rhs}=-\eta QB_{\chi,\rm raw}/2\);
3. no extra direct linear Einstein stress is generated;
4. the scalar-field equation is either unchanged as an independent equation or its bath term is exactly redundant with the modified aether/effective-fluid system through the covariant identities;
5. eta=0 reproduces the closed v0.77/v0.78 system exactly.

If these five identities hold, the memory completion can be frozen before deriving second-order vertices.

## 11. Decision rule

- If NL0B passes exactly, proceed to NL1 and derive the second-order mode-coupling kernels from the combined action.
- If an extra first-order term appears, do **not** alter the historical CLASS equations. The candidate completion is rejected or reclassified as a new theory, and v0.77/v0.78 remain unchanged.

No nonlinear numerical result is to be generated before NL0B is closed.
