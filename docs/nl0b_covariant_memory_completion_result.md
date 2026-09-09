# NL0B result — covariant memory completion audit

Final classification: **NL0B_COVARIANT_MEMORY_COMPLETION_PASS**

Predata commit: `52426fc79285fc6a01c0712167d9b45e6a26f67c`

Scope: analytic theory audit only. No observational data and no nonlinear numerical outcome were used.

## 1. Published AeST dictionary fixes the memory drive

Skordis & Zlosnik define the scalar perturbations in Newtonian gauge by

\[
\phi=\bar\phi+\varphi,
\qquad
A_i=\partial_i\alpha,
\]

and

\[
\chi\equiv\varphi+\dot{\bar\phi}\,\alpha,
\qquad
\theta\equiv\frac{\varphi}{\dot{\bar\phi}}.
\]

The repository bridge uses the same relation as

\[
u_A=\frac{a\Theta_A}{k^2},
\qquad
\chi=Q(u_A+\alpha).
\]

Hence \(\varphi=Qu_A\) in the bridge conventions.

For

\[
X_\mu=h_\mu{}^\nu\nabla_\nu\phi,
\qquad h_{\mu\nu}=g_{\mu\nu}+A_\mu A_\nu,
\]

the first-order spatial piece is

\[
X_i^{(1)}=\partial_i\varphi+Q\partial_i\alpha
=\partial_i\chi.
\]

The physical orthonormal component is therefore

\[
X_{\hat i}^{(1)}=a^{-1}\partial_i\chi.
\]

This is also visible directly in the published quadratic AeST action, whose scalar-gradient combination is \(|\nabla\varphi+Q_0\mathbf A|^2\).

**Identity 1: PASS.**

## 2. FLRW null

On homogeneous FLRW,

\[
\nabla_i\bar\phi=0,
\qquad A_i=0,
\]

so

\[
X_\mu^{(0)}=0.
\]

The regular retarded bath solution is \(U_{j\mu}^{(0)}=0\). Therefore the memory action and its background variation vanish.

**Identity 2: PASS.**

## 3. Oscillator reduction

For the frozen candidate

\[
\mathscr D_AU_{j\mu}=h_\mu{}^\nu A^\rho\nabla_\rho U_{j\nu},
\]

write a spatial covector on FLRW as \(U_{ji}=a\,u_{ji}\). Then

\[
\mathscr D_AU_{ji}=a\dot u_{ji}.
\]

The invariant volume supplies \(a^3\), so the Euler equation for the physical spatial component contains the required Hubble friction:

\[
\ddot U_{j,L}+3H\dot U_{j,L}+\omega_j^2U_{j,L}
=\sqrt\eta\,\omega_j\sqrt{w_j}\,X_L.
\]

With

\[
U_{j,L}=\sqrt\eta\,q_j,
\qquad X_L=(k/a)\chi,
\]

this gives

\[
\ddot q_j+3H\dot q_j+\omega_j^2q_j
=\omega_j\sqrt{w_j}(k/a)\chi.
\]

Changing to conformal time gives exactly

\[
q_j''+2\mathcal Hq_j'+a^2\omega_j^2q_j
=ak\omega_j\sqrt{w_j}\chi.
\]

**Identity 3: PASS.**

## 4. Backreaction variable

The candidate potential is a completed square. Variation with respect to \(X_\mu\) gives

\[
\frac{\delta\mathcal L_{\rm mem}}{\delta X^\mu}
=-\frac{\eta}{2}\mathcal B_\mu,
\]

where

\[
\mathcal B_\mu
=\sum_j\left[w_jX_\mu-\omega_j\sqrt{w_j}\,q_{j\mu}\right].
\]

For a scalar Fourier mode,

\[
\mathcal B_L
=(k/a)\sum_j\left[
w_j\chi-\sqrt{w_j}(a\omega_j/k)q_j
\right]
=(k/a)B_{\chi,\rm raw}.
\]

**Identity 4: PASS.**

## 5. Frozen E closure

At first order the only dependence of the candidate bath on the scalar aether perturbation \(\alpha\) is through

\[
X_i=\partial_i(\varphi+Q\alpha).
\]

Thus

\[
\delta X_i=Q\,\partial_i\delta\alpha.
\]

The spatial-aether Euler equation consequently receives

\[
-\frac{\eta Q}{2}\mathcal B_i.
\]

Removing the common scalar gradient gives

\[
\Delta E_{\rm rhs}
=-\frac{\eta Q}{2}B_{\chi,\rm raw},
\]

which is exactly the frozen CLASS closure.

The factor \(1/2\) is fixed by the preregistered action normalization and was not adjusted after this reduction.

**Identity 5: PASS.**

## 6. Direct linear Einstein stress

The FLRW background has \(X_\mu=U_{j\mu}=0\). Every term in the memory Lagrangian is quadratic in these quantities. A metric variation therefore cannot generate a term first order in cosmological perturbations around this background; the direct bath stress starts at second order.

This matches the preserved source audit

\[
\text{memory direct linear Einstein stress}=0.
\]

**Identity 6: PASS.**

## 7. No extra independent linear scalar constraint

The apparent concern is that the completed-square bath depends on \(\chi=\varphi+Q\alpha\), so its variation contributes to both the scalar and spatial-aether field equations.

At first order these two bath sources are not independent. If \(\mathcal F_\chi\) denotes the scalar-potential bath variation, then

\[
\Delta\mathcal E_\varphi=\mathcal F_\chi,
\qquad
\Delta\mathcal E_\alpha=Q\mathcal F_\chi.
\]

Hence the orthogonal field-equation combination

\[
\Delta(\mathcal E_\alpha-Q\mathcal E_\varphi)=0
\]

is unchanged.

More importantly, the candidate action is diffeomorphism invariant and its direct stress tensor has no first-order term. The linear Einstein equations are therefore the same as in the frozen AeST system. The linear Bianchi identity, together with separately conserved ordinary matter/radiation, gives the same first-order conservation equations for the AeST effective density and momentum variables. These are precisely the standard-form \(\delta\) and \(\theta\) equations used in the repository and in the published AeST formulation.

The bath scalar variation is therefore the Noether-related partner of the modified spatial-aether equation; it does not impose an additional independent first-order condition requiring a new CLASS fluid source.

**Identity 7: PASS.**

## 8. Drude transfer identity

At fixed H,

\[
q_j(s)=
\frac{\omega_j\sqrt{w_j}}{s^2+3Hs+\omega_j^2}X_L(s),
\]

so

\[
\frac{\mathcal B_L}{X_L}
=\sum_jw_j
\frac{s(s+3H)}{s(s+3H)+\omega_j^2}.
\]

Writing

\[
A^2=\tau^2s(s+3H),
\qquad r_j=\omega_j\tau,
\]

gives

\[
K_N(A)=\sum_jw_j\frac{A^2}{A^2+r_j^2},
\]

which is exactly the historical finite positive bath response. The positive continuum measure used in v0.19k/v0.19r yields

\[
K(A)=\frac{A}{1+A}.
\]

**Identity 8: PASS.**

# Classification

All eight preregistered identities are satisfied:

\[
\boxed{\text{NL0B\_COVARIANT\_MEMORY\_COMPLETION\_PASS}}
\]

## What is now frozen

For the strong nonlinear path we freeze the **minimal local conservative completion** defined in the NL0B predata file:

- \(X_\mu=h_\mu{}^\nu\nabla_\nu\phi\);
- aether-orthogonal positive auxiliary vectors \(U_{j\mu}\);
- projected aether derivative \(\mathscr D_A\);
- the completed-square coupling with \(\sqrt\eta\);
- the same positive fixed Drude spectrum;
- no new nonlinear memory shape parameter.

This completion is not claimed to be mathematically unique. Linear data cannot uniquely select all nonlinear completions. It is the minimal local conservative extension selected **before nonlinear outcomes are computed**, and it reproduces the already certified linear theory exactly.

## Remaining gate before NL1 numerics

The memory sector is now closed. The remaining baseline-theory issue is AeST itself away from \(Y=0\): the frozen cosmological bridge fixes \(K(Q)=-F(0,Q)/2\), while weakly nonlinear structure probes the leading \(Y\)-dependence of \(F(Y,Q)\).

The next step is therefore **NL0C**: freeze the published MOND/gradient branch of \(F(Y,Q)\) and derive which coefficients enter the second-order cosmological equations. No nonlinear numerical result should be generated before NL0C is fixed.

References used for the analytic dictionary:

- C. Skordis and T. Zlosnik, Phys. Rev. Lett. 127, 161302 (2021), especially Eqs. (5), (7)–(13).
- Historical repository bath audits v0.19k–v0.19s.
