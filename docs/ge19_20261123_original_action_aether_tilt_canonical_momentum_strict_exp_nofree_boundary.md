# GE19 — original-action aether primordial boundary: finite tilt removes one mode, zero free momentum removes the other

**23 November 2026 | physics-first, no CLASS/DES/numerical campaign.** Result: the original longitudinal AeST action supplies a meaningful physical variable to classify the two remaining k² scalar/aether homogeneous modes in the strict positive Exp radiation past. **Uniformly bounded physical aether tilt excludes the constant-X branch, but not the sqrt(t) branch.** The latter corresponds to a finite independent primordial aether momentum/tilt. An explicit **no-independent-primordial-aether** state selects a unique reduced retarded particular solution, *under a stated source regularity hypothesis*. That initial-state choice is not yet a consequence of the complete unreduced 3+1 covariant action/Noether constraints.

Source anchors, checked in the actual repository before this analysis:
- Original longitudinal aether action `ge19/lw31_action_spatial_traceless_shear_20261110.py`, Git blob `6e41aebf8fdd4f1bc3339e92b9183fecb1503ed3`: `AE=vol*(KB*E**2+2*C*E*Xi-C*Xi**2+2*K(Qi))`, `u=eps*i*k*alpha/a`, `E=ch*((ut-b ux)/N+Nx/(NL))+sh*(...)`, `Xi=sh*sigma+ch*px/L`.
- Constraint/multiplier normalization `ge19/lw32_covariant_aether_auxiliary_multiplier_elimination_20261110.py`, Git blob `b10c7c74e3fd31ed902bc76cd09878c99332cd60`: `kinetic=a*KB*k*k*Ed*Ed`, with isolated local Hessian \(2aK_Bk²\). That is **not** the full ADM-reduced physical kinetic matrix.
- Exact baseline X₂/S₂ reduction `ge19/physics_gate/primordial_k2_XS_retarded_bath_hierarchy_20261122.py`, Git blob `a7fa9069fb2670a0231ed8374d09ebd0b684d192`, and reference-radiation indicial parent `ge19/physics_gate/primordial_X2_second_order_radiation_asymptotic_20261122.py`, Git blob `bca468290e2d050637011eb82de212bce82fd254`.
- Original frozen Exp `v019/patch/source/aest_memory.c`; source-verified \(K_Q=I_0/a³\), \(Q=Q_0+Z_0 Z\), \(Z²+\ln Z=\ln[I_0/(4K_2Z_0)]-3\ln a\).
- Earlier [Abel/Ward two-amplitude obstruction](ge19_20261123_primordial_XS_mode_selection_two_amplitude_abel_ward_obstruction.md) and [fully backreacted adiabatic Einstein/fluids k² source](ge19_20261122_exact_adiabatic_k0_curvature_conservation_k2_constraint_elimination.md).

## A. Action-linked canonical momentum, not an ad hoc variable

At fixed nonzero comoving Fourier \(k\), the original longitudinal aether quadratic action contains (up to the overall action normalization and Fourier-pair convention)

```math
L_{\rm AeST,long}^{(2)}
\supset a k²\,[K_BE_A²+2C E_A\chi-C\chi²],
\qquad E_A=\dot\alpha_A+\Psi,\quad \chi=\varphi+Q\alpha_A,\quad C=2-K_B.
```

Consequently, differentiating this **local, unreduced longitudinal term** with respect to \(\dot\alpha_A\) gives

```math
\boxed{
\pi_{\alpha_A}^{\rm local}\ \propto\ 2ak²(K_BE_A+C\chi)
=2ak²S_A.
}
```

On the analytic \(S_A=k² S_2+O(k⁴)\) branch, \(\pi_{\alpha_A}^{\rm local}\propto 2k⁴P_2\), where

```math
\boxed{P_2:=aS_2.}\tag{1}
```

This identifies the scaled variable as the **local longitudinal aether momentum**, with the important limit that **the full reduced ADM/metric/scalar physical symplectic matrix is not established by this isolated term**. In the original scalar action \(\chi\) is gauge invariant but \(\alpha_A\) alone need not be; no gauge-only interpretation of an \(X_2\) difference is licensed.

## B. Exact Hamiltonian form of the sourced reduced k² system at eta=0+

Take \(X_2=\chi_2/Q\), \(S_2=K_BE_{A2}+CQX_2\), \(\Delta_{A2}\) from the coupled full-Einstein, pressureful eight-equation primordial fluid source. In proper cosmic time, \(\lambda=CQ/K_B\), the **original quarter-action eta=0+ baseline equations** are exactly

```math
\boxed{
\begin{aligned}
\dot X_2&=-\lambda X_2+\frac{P_2}{aK_B}+c_A²\Delta_{A2},\\
\dot P_2&=\lambda P_2+aQ(K_Q-2\lambda)X_2.
\end{aligned}}\tag{2}
```

The inhomogeneous problem admits the explicit reduced *Hamiltonian representation*

```math
\boxed{
\mathcal H_{\rm red}(X_2,P_2;t)=
\frac{P_2²}{2aK_B}-\lambda X_2P_2
-\frac12aQ(K_Q-2\lambda)X_2²
+c_A²\Delta_{A2}P_2
}\tag{3}
```

with \(\dot X_2=\partial_{P_2}\mathcal H_{\rm red}\), \(\dot P_2=-\partial_{X_2}\mathcal H_{\rm red}\), assuming \(\Delta_{A2}\) is the **already solved** Einstein–matter input at this order. The homogeneous \(2\times2\) matrix has trace zero, so for its transfer \(\mathsf U_{XP}\),

```math
\boxed{\det\mathsf U_{XP}(t,t_i)=1,\quad
\mathsf U_{XP}^{T}J\mathsf U_{XP}=J,\quad
J=\begin{pmatrix}0&1\\-1&0\end{pmatrix}.}\tag{4}
```

This is an exact **reduced sourced Hamiltonian structure**, **not** an independent proof of the full constrained covariant theory's global symplectic form. It reproduces the earlier \(\det U_{XS}=a_i/a(t)\).

## C. Strict Exp radiation early-time asymptotics — the actual two modes

Use \(t\to0^+\), \(L=\ln(t_\star/t)\to\infty\), the radiation-dominated actual **leading** expanding background \(a=A_r\sqrt t\,[1+o(1)]\), \(H\sim1/(2t)\). In original positive Exp,

```math
K_Q=I_0/a³,\quad
Z²+\ln Z=\ln[I_0/(4K_2Z_0)]-3\ln a,\quad
Q=Q_0+Z_0Z,\quad
Z\sim\sqrt{\tfrac32L},\quad Q\sim Z_0\sqrt{\tfrac32L}.
```

The last \(Q\sim Z_0\sqrt{3L/2}\) is a **strict mathematical \(t\to0\) asymptote**. For frozen \(Q_0=10^{-4},Z_0=10^{-17}\), the \(Q_0\)-dominated *intermediate physical era* persists over an enormous logarithmic range; **do not substitute the strict asymptote as a numeric CLASS initial condition at realistic \(\tau_i\)**.

For the **homogeneous** difference between two solutions driven by the same \(\Delta_{A2}\), define \(P_h=aS_h\). The first-order equations are

```math
\dot X_h=-\lambda X_h+\frac{P_h}{aK_B},\qquad
\dot P_h=\lambda P_h+aQ(K_Q-2\lambda)X_h.
```

The \(\lambda\) terms grow at most as \(\sqrt L\), whereas
```math
aQK_Q=\frac{I_0Q}{a²}\sim
\frac{I_0Z_0}{A_r²t}\sqrt{\tfrac32L}.
```

The previously verified reference indicial roots are \(0,\frac12\). The strict Exp logarithmic coefficients yield two corresponding asymptotic branches:

**H₁ — constant strain mode.** For \(X_h(t)\to A_*\ne0\),

```math
\boxed{
P_h(t)\sim
-\frac{2I_0 Z_0A_*}{3A_r²}\sqrt{\frac32}\,
L^{3/2},\qquad
X_h=A_*+O(\sqrt t L^{3/2}).
}\tag{5}
```

In the long physically relevant \(Q\simeq Q_0\) regime this is instead approximately \(P_h\propto Q_0\log t\), still divergent as one extends the constant-Q reference toward its own artificial zero-time limit. The strict \(L^{3/2}\) asymptote and the constant-Q logarithm are **distinct, nonuniform limits**.

**H₂ — canonical-momentum/tilt mode.** A second independent solution has \(\lim_{t\to0}P_h=P_*\ne0\) and

```math
\boxed{
X_h(t)=\frac{2P_*}{A_rK_B}\sqrt t+o(\sqrt t),
\qquad
P_h(t)=P_*+o(1).
}\tag{6}
```

These expressions follow by integrating (2) with the above strict Exp coefficients: in H₁, \(\dot P\sim I_0 A_*Q/(A_r²t)\); in H₂ the \(aQK_QX_h\sim Q/\sqrt t\) term is integrable. They agree with the original constant-Q radiation reference's \(p=0,\frac12\) branches and finite \(a S_h\) for the second, but do **not** claim that the entire full Einstein–AeST–NL0B system possesses both physically permissible modes.

## D. What the original aether rapidity / electric norm actually select

The original LW31 covariant longitudinal aether rapidity perturbation is \(u=ik\alpha_A/a\), and the action/phase map gives

```math
\alpha_A=X-\frac{\varphi}{Q},\qquad
\frac{\varphi}{Q}=\frac{a\theta_A}{k²}.
```

At fixed **same Einstein–matter** \(V_{A2}\), an \(X_2\) homogeneous difference changes the physical aether rapidity at the relevant Fourier order by

```math
\boxed{\Delta u_h=\frac{ik³}{a}X_h.}\tag{7}
```

- **H₁:** \(\Delta u_h\sim i k³ A_*/(A_r\sqrt t)\) **diverges** as \(t\to0\). Uniform small-tilt perturbativity (or bounded physical aether rapidity) excludes \(A_*\ne0\) **within this analytic \(k²\) branch**. Mere bounded \(X_2\) would not.
- **H₂:** \(\Delta u_h\to i\,2k³P_*/(A_r²K_B)\), a **finite but generally nonzero** physical initial aether tilt. Thus bounded rapidity alone does NOT eliminate this independent amplitude.

For homogeneous differences, the local original electric variable satisfies \(E_{A2,h}=\dot X_h\). Its orthonormal spatial-gradient norm is proportional to \((k/a)E_{A,h}\). For H₂,

```math
E_{A2,h}\sim\frac{P_*}{A_rK_B\sqrt t},\quad
\frac{(k/a)E_{A,h}}{H}\longrightarrow
\frac{2k³P_*}{A_r²K_B}.
```

Thus even though the electric coefficient diverges as \(t^{-1/2}\), the electric strength **normalized to the background Hubble scale** can remain finite; its finiteness does not exclude H₂. H₁ has a logarithmically unbounded normalized electric strength.

**Do not substitute a weaker "finite quadratic electric action" test.** The isolated local electric term has integrand \(\propto a E_{A,h}²\), scaling as \(t^{-1/2}L^3\) for H₁ and \(t^{-1/2}\) for H₂. Both are integrable at \(t=0\): \(\int_0^\epsilon t^{-1/2}|\ln t|^n\,dt<\infty\) for finite \(n\). Therefore **finite action of the isolated electric term excludes NEITHER branch**. This does not establish finite *total constrained* action/energy: the scalar, lapse, shift, metric and bath boundary terms have not all been included, and the physically admissible norm may be stronger.

## E. Explicit no-independent-aether initial-state hypothesis yields a unique REDUCED particular solution

A **minimal physically transparent** additional primordial hypothesis is that the aether carries no free homogeneous tilt/momentum relative to the common adiabatic growing curvature mode. In the strict past, this means the *two independent* boundary data

```math
\boxed{\lim_{t\to0}X_2(t)=0,\qquad
\lim_{t\to0}P_2(t)=0.}\tag{8}
```

The first removes H₁; the second removes H₂. Equivalently, on these homogeneous asymptotic branches, \(\lim_{t\to0}X_2/a=0\) removes both, but is **stronger than mere bounded tilt**. The aether no-free condition is a *declared physical-state assumption* compatible with (2), **not yet proven to follow from the full covariant action or universally required by inflationary primordial perturbations**.

With \(f(t)=c_A²(t)\Delta_{A2}(t)\), the exact no-free reduced system is the **physical-past Volterra** equation

```math
\boxed{\begin{aligned}
X_2(t)&=\int_0^t
\left[-\lambda(s)X_2(s)+\frac{P_2(s)}{a(s)K_B}+f(s)\right]ds,\\
P_2(t)&=\int_0^t
\left[\lambda(s)P_2(s)+a(s)Q(s)(K_Q(s)-2\lambda(s))X_2(s)\right]ds.
\end{aligned}}\tag{9}
```

**New conditional existence/uniqueness result within the original reduced system.** Suppose the jointly selected regular Einstein–matter source has strict radiation asymptotic \(\Delta_{A2}(t)=D t+o(t)\) for fixed physical finite \(k\)-coefficient, and the strict positive Exp background above holds. Then

```math
c_A²(t)=\frac{1}{3L}[1+o(1)],\quad
f(t)=\frac{Dt}{3L}[1+o(1)].
```

The Volterra map (9) is a contraction sufficiently near \(t=0\) in the weighted space \(|X_2(t)|\le C\,t²/L\), \(|P_2(t)|\le C\,t²/\sqrt L\): the self-coupling kernels have respectively extra factors \(O(\sqrt t\,\sqrt L)\) or \(O(t\sqrt L)\), tending to zero, while the source terms land in these weights. Hence there is a **unique no-free particular solution in this regularity class**, with

```math
\boxed{
X_{2,\rm nf}(t)=\frac{D t²}{6L}[1+o(1)],
\qquad
P_{2,\rm nf}(t)=
\frac{I_0Z_0D}{12A_r²}\sqrt{\frac32}\,
\frac{t²}{\sqrt L}[1+o(1)].
}\tag{10}
```

The leading \(P\) coefficient follows by integrating \(aQK_Q X_2\); \(\lambda P\) and \(2\lambda aQX\) are subleading. The original gauge-invariant strain is then

```math
\boxed{\chi_{2,\rm nf}=QX_{2,\rm nf}
=\frac{DZ_0}{6}\sqrt{\frac32}\,
\frac{t²}{\sqrt L}[1+o(1)].}\tag{11}
```

This recovers the strict Exp conditional early source result from the archived primordial analysis and, importantly, also fixes the previously unresolved **leading reduced canonical momentum**. A direct independent analytic differentiation of the \(L^{3/2}\) H₁ expression and of the leading \(t²/\sqrt L\) \(P_{\rm nf}\) expression confirms their leading original source terms; no simulation has been performed. After constructing this selected asymptotic state, equation (9) propagates it to finite time using the **actual calibrated Exp \(a(t),Q(t),K_Q(t)\)** and actual full Einstein–matter \(\Delta_{A2}(t)\), not the strict asymptotic approximations at CLASS entry.

The **physical state restriction** (8) is independent of the original reduced Ward residual, which is automatically satisfied on shell for the original quarter source, and the full covariant multiplier/boundary constraints still have to be independently checked. Equation (9) at eta=0+ fixes the **baseline** scalar/aether history; the first eta tangent of the *full physically selected initial state* is not yet determined. With nonzero eta, the causal bath must also be transported from the same physical past.

## F. Scientific stop/forward decision

**New source-grounded partial classification:**
- Bounded physical aether rapidity (uniform linear perturbativity on the analytic branch) excludes H₁, but **permits H₂**, a finite independent tilt/momentum.
- Isolated electric quadratic-action finiteness does **not** select between H₁/H₂; treating it as a full physical energy theorem would be incorrect.
- Declaring **no independent primordial aether excitation** additionally sets the finite \(P_*\) to zero and leads to a mathematically unique **reduced**, physically past-selected no-free solution under the stated pressureful Einstein-source regularity.
- Two-mode nonuniqueness is therefore **one physical boundary choice**, not a reason to perform another unbounded numerical sweep.

**Still open**: full 3+1 unreduced covariant Einstein–AeST–NL0B constrained symplectic/energy regularity at primordial time; physical justification for (8) rather than an allowed independent aether-tilt/isocurvature mode; full pressureful Einstein k² growing solution at finite redshift; eta-dependent primordial tangent; physical finite-k through-equality memory transfer; DES significance. **No physical detection has been made.**

**Decision:** `AETHER_H1_UNIFORMLY_NONPERTURBATIVE / H2_FINITE_TILT_ALLOWED_UNLESS_NOFREE_BC / SOURCE_FORCED_REDUCED_VOLTERRA_UNIQUE_CONDITIONAL / FULL_COVARIANT_PRIMORDIAL_SELECTION_OPEN / FULL_PHYSICS_GO=false / DES_detection=false`.
