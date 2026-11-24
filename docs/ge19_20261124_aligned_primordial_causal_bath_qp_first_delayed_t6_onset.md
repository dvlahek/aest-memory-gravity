# GE19 — Primordial aligned/no-free branch: first genuine delayed-memory onset in original NL0B bath

**24 November 2026.** This is a **conditional analytic short-time result**, NOT a CLASS simulation, not a full covariant Einstein–AeST–NL0B physical-mode certificate, not a finite-k DES Weyl prediction, and not an observed detection. It is deliberately **delayed-only**: it separates the original instantaneous `W_b chi` force from the causal history `sum r_j` in the correctly quarter-normalized original AeST equation. No observational data or nuisance fits enter.

Parent results:
- [Covariantly interpretable primordial scalar–aether alignment boundary and why ordinary regularity leaves a free H2 mode](ge19_20261124_covariant_primordial_alignment_vs_free_tilt_symplectic_and_stress_gate.md), Git blob `b1e604e303ad8161c046e467b44161b186e16630`.
- [Original-action unique REDUCED no-free Volterra source and strict positive Exp asymptotics](ge19_20261123_original_action_aether_tilt_canonical_momentum_strict_exp_nofree_boundary.md), blob `8594a60456c49f295b35148588b87c0980864bfe`.
- [Exact original NL0B retarded oscillator and CLASS conformal q/p conversion](ge19_20261122_exact_radiation_retarded_bath_green_and_class_initial_data.md), blob `3dbbb396343746b22d7257d49c5c151a4fac2e53`.
- [Original-action k² X/S/quarter-force oscillator expansion](../ge19/physics_gate/primordial_k2_XS_retarded_bath_hierarchy_20261122.py), blob `a7fa9069fb2670a0231ed8374d09ebd0b684d192`.
- [Leading strict radiation+neutrino Einstein source](../ge19/physics_gate/radiation_neutrino_delta_source_20261111.py), blob `19e9efd5713dc8df3057c4b33f8c4a2921a96687`.

## A. Frozen assumptions and actual analytic primordial model choice

We **declare**, rather than infer from the unreduced action, a primordial scalar–aether alignment/no-independent-aether mode

```math
\lim_{t\to0^+}\Xi/Q=0,\qquad
\Xi/Q=ikX/a.
```

This excludes reduced H1 and H2 free modes at fixed finite \(k\), leaving only the physically past-forced reduced particular solution. The original positive Exp background and early radiation era are

```math
a=A_r\sqrt t[1+o(1)],\quad
L=\ln(t_\star/t)\to\infty,\quad
Q=Z_0\sqrt{\tfrac32L}[1+o(1)],
\quad K_Q=I_0/a³.
```

**Warning:** this is the mathematical strict \(t\to0\) asymptote, which is far deeper than the physically accessible \(Q\simeq Q_0=10^{-4}\) regime for the frozen \(Z_0=10^{-17}\). Do NOT numerically initialize CLASS with these asymptotes at a practical finite entry time. At practical times use exact calibrated Exp background and integrate the causal Volterra source from the selected physical early initial state.

The original Einstein–matter comoving source has the strict radiation growing limit

```math
\Delta_{A2}(t)=Dt+o(t),\qquad
D=-\frac{15+4R_\nu}{10 A_r²}\Psi_0
=-\frac{(15+4R_\nu)\mathcal R}{
5A_r²(3+4R_\nu/5)} ,
```

with `R_nu` the **fraction of all free-streaming ultrarelativistic radiation**, `\mathcal R` the leading conserved comoving curvature. This statement assumes the physical pressureful growing eight-equation Einstein/species solution has the strict regular radiation limit; no finite-time matter/metric numerical evolution is implied.

For the selected reduced no-free branch the already derived original-action baseline is

```math
X_{2,0}=\frac{Dt²}{6L}[1+o(1)],\qquad
P_{2,0}=aS_{2,0}
=\frac{I_0Z_0D}{12 A_r²}\sqrt{\frac32}
\frac{t²}{\sqrt L}[1+o(1)].
```

The actual **gauge-invariant aether/scalar strain coefficient** `\chi_2=QX_2` is

```math
\boxed{
\chi_{2,0}(t)=
\underbrace{\frac{DZ_0}{6}\sqrt{\frac32}}_{=:C_\chi}
\frac{t²}{\sqrt L}[1+o(1)].
}\tag{1}
```

## B. First actual retarded auxiliary history, including correct finite-time q/p scaling

For each original **positive finite** bath mode \((\omega_j,w_j)\), its original regular variable `r_{j2}` satisfies, in pure radiation,

```math
\ddot r_{j2}+\frac1{2t}\dot r_{j2}+\omega_j²r_{j2}
=\omega_j²w_j\,\chi_{2,0}(t),
\qquad r_{j2}^{\rm ret}(t)
=\omega_j²w_j\int_0^tG_j(t,s)\chi_{2,0}(s)\,ds.
```

The exact radiation Bessel Green function in the locked parent has the leading causal kernel `G_j(t,s)\sim2\sqrt s(\sqrt t-\sqrt s)` for \(0<s<t\ll\omega_j^{-1}\). Substitution of (1), using the slow logarithmic variation at fixed \(s/t>0\), gives

```math
\boxed{
r_{j2}^{\rm ret}(t)=
\frac{\omega_j²w_j C_\chi}{14}
\frac{t⁴}{\sqrt L}[1+o(1)].
}\tag{2}
```

This is the original **physical-past causal choice** with no independent oscillator homogeneous modes, not a reset at arbitrary \(t_i>0\). The coefficient 1/14 is the exact radiation driven-kernel integral `2[(2/7)-(1/4)]`.

Original CLASS uses conformal `p_j=dq_j/d\tau`, where `q_j=k³q_{j3}`, and exactly

```math
q_{j3}=\frac{r_{j2}}{a\omega_j\sqrt{w_j}},
\qquad
p_{j3}=\frac{\dot r_{j2}-H r_{j2}}{\omega_j\sqrt{w_j}}.
```

Thus the **strict early aligned-branch history** has

```math
\boxed{
q_{j3}(t)\sim
\frac{\omega_j\sqrt{w_j} C_\chi}{14A_r}
\frac{t^{7/2}}{\sqrt L},\qquad
p_{j3}(t)\sim
\frac{\omega_j\sqrt{w_j} C_\chi}{4}
\frac{t³}{\sqrt L}.
}\tag{3}
```

Both vanish in the singular past but **are nonzero at every finite physical CLASS start** when the actual strain history is nonzero. One must transport them rather than set `q_j(t_i)=p_j(t_i)=0`.

## C. Exact original quarter-source: instantaneous response begins at t⁴, DELAYED response at t⁶

Define `W_b=\sum_jw_j`, `M_{\omega²}=\sum_j\omega_j²w_j`, and `R_{2,0}=\sum_jr_{j2}^{\rm ret}`. The original **signed** force is

```math
-\frac{\eta Q}{4}B_2,\qquad
B_2=W_b\chi_2-R_2,
\quad
-\frac{\eta Q}{4}B_2
=\underbrace{-\frac{\eta QW_b\chi_2}{4}}_{\text{instantaneous}}
+\underbrace{\frac{\eta QR_2}{4}}_{\text{delayed-only}}.
```

In the exact early Exp asymptote `Q C_\chi/\sqrt L=DZ_0²/4`. Therefore at baseline \(\eta=0^+\), with equal no-free primordial conditions across \(\eta\),

```math
\boxed{
Q W_b\chi_{2,0}
=\frac{DW_bZ_0²}{4}t²[1+o(1)],
\qquad
Q R_{2,0}
=\frac{DM_{\omega²}Z_0²}{56}t⁴[1+o(1)].
}\tag{4}
```

The exact reduced proper-time first-\(\eta\) tangent \((X_{2,1},P_{2,1}=aS_{2,1})\) has initial-state tangent zero at the **physical past**, and equations

```math
\dot X_{2,1}=-\lambda X_{2,1}+\frac{P_{2,1}}{aK_B},
\qquad
\dot P_{2,1}=\lambda P_{2,1}+aQ(K_Q-2\lambda)X_{2,1}
-\frac{aQ}{4}B_{2,0},\quad
\lambda=(2-K_B)Q/K_B.
\tag{5}
```

Linearity separates the two pieces with identical physical-past tangent boundary conditions. With the exact original \(1/4\) source normalization, the leading **instantaneous-only** tangent coefficients are

```math
\boxed{
P_{2,1}^{\rm instant}(t)=
-\frac{A_r D W_b Z_0²}{56}\,t^{7/2}[1+o(1)],
\quad
X_{2,1}^{\rm instant}(t)=
-\frac{D W_b Z_0²}{224K_B}\,t^{4}[1+o(1)].
}\tag{6}
```

The genuinely **DELAYED-ONLY** tangent begins **two additional powers of proper time later**:

```math
\boxed{
P_{2,1}^{\rm delayed}(t)=
\frac{A_r D M_{\omega²}Z_0²}{1232}\,t^{11/2}[1+o(1)],
\quad
X_{2,1}^{\rm delayed}(t)=
\frac{D M_{\omega²}Z_0²}{7392K_B}\,t^{6}[1+o(1)] .
}\tag{7}
```

These rational coefficients follow by two elementary Volterra integrations after the exact \(1/14\) radiation bath kernel. The suppressed \(\lambda\) and \(QK_Q\) feedback terms are smaller than these leading source terms as \(t\to0\) (powers of \(t\) dominate the logarithmic \(Q\) factors). The arithmetic was independently checked symbolically in a local one-shot calculation; this is **not a numerical cosmological run**.

**Physical interpretation:** for the specified aligned/no-free primordial branch, the original NL0B positive bath induces a **causally delayed scalar/aether effect** that is sharply distinguishable in time from the instantaneous \(\eta W_b\chi\) term. This establishes a conditional analytic *early scalar memory onset*, not a gravitational Weyl detection. In particular the first direct Einstein stress due to \(S_{2,1}\) appears at order \(k^4\) and its **full** metric+ordinary-species response can cancel or reshape the direct source. One must solve that complete order and ultimately the full finite-k transfer to claim nonzero observable lensing.

The strict \(t\to0\) regime is also not a proxy for a survey-scale \(k\), cosmological equality/recombination transitions, or a dark-energy era. Do not extrapolate the \(t^6\) onset to DES redshifts or infer a detectability bound.

## D. Decision: actual next physics task, not another proof-by-assertion

**We have an explicit conditional primordial theory prediction** under the well-defined additional state condition \(\Xi/Q\to0\): \(X_2\) early forced amplitude, its physically retarded \(r_j,q_j,p_j\), and separate early \(\eta\)-tangent terms with an exact delayed-only \(t^6\) onset. This is significantly narrower than an arbitrary sheared template and uses no empirical tuning.

**Still essential before observational usage:** independently verify this **primordial alignment hypothesis** against the full unreduced covariant AeST multiplier/metric/scalar boundary and constraint equations; carry the coupled eight-equation pressureful Exp matter system forward using the **actual calibrated background** (including relativistic-to-massive neutrino treatment), transport the causal bath continuously, solve full \(k^4\) metric backreaction and then the full finite-k signed \(T_{\delta,1}(k,z),T_{W,1}(k,z)\). In particular a \(\sim t^6\) reduced \(X_2\) tangent is **not** a measured gravitational memory perturbation.

**Flags:** `PRIMORDIAL_ALIGNED_NOFREE_ASSUMED`; `STRICT_EXP_REDUCED_DELAYED_ONSET_T6_DERIVED`; `ORIGINAL_QUARTER_SOURCE_USED`; `FULL_COVARIANT_PRIMORDIAL_ALIGNMENT_NOT_PROVEN`; `FULL_PHYSICS_GO=false`; `DES_detection=false`.
