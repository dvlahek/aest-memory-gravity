# GE19 — Primordial AeST k² mode selection: an exact two-amplitude obstruction, not a Ward solve

**23 November 2026 — physics-first decision following the pressureful Exp 19→8 early-time Einstein+species adiabatic reduction.** No CLASS numerical evolution, rerun of existing symbolic gates, DES observed-data fit, parameter tuning or free bath reset. The purpose is to identify precisely what the original analytic action **can** select and what extra physical initial-state principle is required before a unique memory prediction exists.

## 1. Fixed regular epoch: exact two homogeneous amplitudes remain

At `eta=0+` baseline and a finite regular cosmic time `t`, in the **selected but still conditional** analytic finite-k branch `X=k²X_2+O(k⁴)`, `S_A=k²S_2+O(k⁴)`, source `Delta_A=k²Delta_{A2}+O(k⁴)`, the exact reduced original-action equations [source-verified in the original k² derivation](../ge19/physics_gate/primordial_k2_XS_retarded_bath_hierarchy_20261122.py) give

```math
\frac{d}{dt}\binom{X_2}{S_2}
=\mathsf A_2(t)\binom{X_2}{S_2}
+\binom{c_A²(t)\Delta_{A2}(t)}0,
\quad
\mathsf A_2=
\begin{pmatrix}
-A&1/K_B\\
Q(K_Q-2A)&A-H
\end{pmatrix},\quad
A=\frac{(2-K_B)Q}{K_B}.
\tag{1}
```

The signed `eta` source `-eta Q B_2/4` is in the second row for `eta>0`, with the bath's `eta→0+` retarded history selected separately; it does not alter the following baseline determinant calculation.

**Exact new structural theorem (Abel–Liouville):**

```math
\operatorname{tr}\mathsf A_2=-H=-\dot a/a,
\quad
\boxed{\det U_2(t,t_i)=
\exp[-\int_{t_i}^tH(s)\,ds]=\frac{a(t_i)}{a(t)}>0},
\tag{2}
```

where `U_2(t_i,t_i)=I`. Thus there are **two independent homogeneous initial amplitudes at every finite regular time**; the chosen, constrained eight-dimensional Einstein+ordinary-matter source `Delta_{A2}` does **not** make `(X_2,S_2)` unique. At a regular finite time,

```math
\boxed{
u(t)=U_2(t,t_i)u(t_i)
+\int_{t_i}^tU_2(t,s)
\binom{c_A²(s)\Delta_{A2}(s)}0\,ds,\quad
u=\binom{X_2}{S_2}.
}\tag{3}
```

The physical source is the fully backreacted pressureful one [from the exact constrained eight-equation fluid/Einstein branch](ge19_20261122_exact_adiabatic_k0_curvature_conservation_k2_constraint_elimination.md), **not** the rejected fixed-radiation dustlike source. The first term of (3) is unmeasured/unspecified without primordial state selection; setting `u(t_i)=0` at an arbitrary CLASS entry time silently resets the scalar/aether history.

## 2. Why Einstein k² and the ORIGINAL REDUCED Ward identity cannot algebraically remove those amplitudes

The original action density and phase dictionaries are

```math
D_A^{\rm action}=\frac13[QK_{QQ}\delta Q-\frac{k²}{a²}S_A],\quad
P_A=K_Q\delta Q/3,\quad
T_A=K_Qk²\varphi/(3a).
\tag{4}
```

On the declared branch `S_A=k² S_2+O(k⁴)` the first *direct* `S_2` density term is `-k⁴S_2/(3a²)`, and the first extra phase source also enters at `k⁴`. Thus the complete **k²** Einstein/matter operator is triangular and insensitive to changing the k² scalar/aether homogeneous amplitudes (provided all k² matter/metric data and its phase/pressure dictionary remain matched).

This is **not** a proof that Einstein k⁴ or the complete full covariant action is insensitive: the k⁴ constraints and complete Ward must still be solved.

There is a stronger warning about attempting to "add one more Ward constraint": the independently derived original **reduced** scalar-action off-shell residual identity [LW33](ge19_lw33_exact_scalar_action_to_CLASS_offshell_source_decision_2026-11-10.md) is

```math
\mathscr S_\phi=
\frac{6a³}{Q}R_D+
\frac{2ak²K_B}{Q}R_E+
\frac{2ak²C}{Q}R_\chi+
\frac{2ak²K_Q}{Q}R_{\rm geo}
-\frac{6a³}{Q}\dot R_\rho-\frac{18a³H}{Q}R_\rho
+\frac{a\eta k²B_\chi}{2}(1-4\gamma).
\tag{5}
```

For the original action `\gamma=1/4`, when density/phase/electric/continuity definitions and their evolution are imposed, *every term vanishes without a further algebraic condition on `X_2(t_i)` or `S_2(t_i)`*. A nonzero instantaneous spatial scalar current is balanced by evolution of its temporal charge; it is **not** required to vanish. Consequently, **within the source-verified reduced model, Ward is a propagation/compatibility condition, not an extra two-amplitude selection rule**. This does **not** extend to yet-unmapped independent multiplier/boundary or full 3+1 covariant action constraints, which might select or exclude branches.

### Concrete aether-field content of the two amplitudes

This is not merely an abstract two-by-two ODE ambiguity. The **original scalar/aether definitions** give at order k², with the same coupled matter velocity coefficient `V_{A2}`:

```math
\boxed{
\alpha_{A2}=X_2-aV_{A2},
\qquad
E_{A2}=\frac{S_2-(2-K_B)QX_2}{K_B}.
}
```

Thus a change `(\delta X_2,\delta S_2)=(\varepsilon,0)` at fixed matter/metric data changes `\alpha_{A2}` by `\varepsilon` and `E_{A2}` by `-(2-K_B)Q\varepsilon/K_B`, despite an unchanged k² Einstein source. This is exactly the old **instantaneous stress-null direction**, now expressed on the proper k² manifold. The gauge-invariant strain `\chi_2=QX_2` changes, so the ambiguity must **not** be declared a pure gauge mode without analyzing the full action constraints. The evolution can lift this stress-null state and create genuine k⁴ metric response.

## 3. The singular radiation past: bounded X₂ does not mean unique mode

The exact reduced second-order equation for `X_2` was derived in the [indicial parent](../ge19/physics_gate/primordial_X2_second_order_radiation_asymptotic_20261122.py):

```math
\ddot X_2+H\dot X_2+
\left[\frac{Q(CQ-K_Q)}{K_B}+
\frac{CQ}{K_B}H(1-3c_A²)\right]X_2
=\frac{d}{dt}(c_A²\Delta_{A2})
+\left(H-\frac{CQ}{K_B}\right)c_A²\Delta_{A2}
\qquad(\eta=0).
\tag{6}
```

For **reference radiation** `a=A\sqrt t` with constant reference `Q`, the highest-singularity part is `L_0X=\ddot X+\dot X/(2t)`. Its indicial equation and roots are

```math
p(p-\tfrac12)=0,\qquad p=0,\;\tfrac12.
\tag{7}
```

The archived source independently derives corrections for both reference homogeneous branches, schematically `X_{h1}=1+O(\sqrt t\log t)`, `X_{h2}=\sqrt t+O(t)`, while `S_{h1}` develops logarithmic/negative-power terms and `S_{h2}\sim t^{-1/2}`. An *isolated* gradient density contribution for the second mode has a finite normalized early-time reference limit. Accordingly **bounded X₂ alone excludes NEITHER branch**. Requiring `X_2\to0` would remove only the constant branch; the `\sqrt t` branch survives. Requiring independently bounded electric field `E_A`, finite full stress/energy, or absence of an aether isocurvature mode are different, stronger physical boundary requirements, and must not be conflated with simple `X_2` boundedness. Do not infer full regularity of either branch merely from one stress component.

**Strict Exp warning:** the original positive Exp `Q=Q_0+Z_0 Z`, `Z²+\ln Z=-3\ln a+\mathrm{const}` slowly grows like `\sqrt{\ln(1/t)}` as `t\to0`, while `K_Q\sim t^{-3/2}`, `c_A²=O(1/\ln(1/t))`. Under strict radiation `H\sim1/(2t)` the potential term of (6) scales no worse than `O(t^{-3/2}\sqrt{\ln(1/t)})+O(t^{-1}\sqrt{\ln(1/t)})=o(t^{-2})`. Hence the **formal leading indicial powers** remain 0 and 1/2; the exact slowly varying prefactors and the full coupled singular Exp limit still need a separate justified asymptotic analysis. The reference result is not automatically a full physical growing mode for Exp.

## 4. One transparent primordial choice: "purely adiabatic, no independent aether mode"

The cleanest *potential* way to get a unique theory-level memory transfer is to **state an independent physical primordial-state hypothesis**: the growing cosmological curvature mode excites `X_2,S_2` only through the already determined physical source `Delta_{A2}`, with no independent primordial scalar/aether homogeneous amplitude.

Then one must take the **physical-past-selected** particular solution of (3), *not* `X_2(t_i)=S_2(t_i)=0` at the arbitrary numerical entry time `t_i>0`:

```math
\boxed{
u_{\rm nofree}(t)=
\lim_{\epsilon\to0+}
\int_{\epsilon}^t U_2(t,s)
\binom{c_A²(s)\Delta_{A2}(s)}0\,ds,
}\tag{8}
```

*provided this limit exists in the actual full Exp background with the selected expanding solution*. Equation (8) is a **conditional Volterra boundary prescription**. Its existence, consistency with full unreduced action constraints and the absence of hidden `eta`-dependent initial-state terms are not yet certified.

Within the reference-radiation two-mode model, and if the particular solution vanishes faster than `\sqrt t` (the earlier source-selected branch has `X_{2,p}=O(t²/\ln(1/t))` conditionally), the **strong no-free condition**

```math
\boxed{X_2(t)=o(\sqrt t)\quad(t\to0+)}
\tag{9}
```

would remove both independent reference homogeneous modes. Merely `X_2\to0` would not. Condition (9) is a **deliberately stronger primordial boundary hypothesis**, **not** a derived requirement from Einstein, reduced Ward, or a generic "regular" perturbation. It must be justified independently as appropriate to the no-isocurvature initial state of the full covariant theory. The strict Exp case can have logarithmic corrections and requires its own proof.

## 5. Why this is the exact blocker to a DES prediction

The original one-sided `eta=0+` bath is driven linearly by `QX_2`. If independent initial scalar/aether amplitudes `A_*,B_*` are admitted, then

```math
u_0=u_{\rm nofree}+A_*u_{h1}+B_*u_{h2},\qquad
R_{2,0}=R_{\rm nofree}+A_*R_{h1}+B_*R_{h2}
```

for physically retarded, no-free oscillator states on each possible underlying scalar history. The original quarter source `-\eta Q[W_bQX_2-R_{2,0}]/4` therefore depends on `A_*,B_*`, and so does any following physical metric response at k⁴. A single signed matter–Weyl template cannot be claimed unique unless the physical primordial theory selects these amplitudes or they are explicitly treated as independent primordial parameters. Furthermore the initial `eta` derivative of the full physical eigenmode is separately unproven; the "same initial eta tangent" comparison is only a restricted source decomposition.

This is not a newly detected aether isocurvature mode, because the full-action admissibility, gauge/constraint regularity and energy norm of the two reduced solutions remain unproven. It is a **mathematically established reduced initial-data nonuniqueness**.

### Decision / stop rule

- **Proven exactly at regular finite t:** `tr A2=-H`, `det U2=a_i/a_t\ne0`; two reduced homogeneous amplitudes persist and the full k² Einstein fluid constraint cannot select them.
- **Proven within the original reduced Ward dictionary:** imposing the original action quarter-source and all stated evolution/dictionary residuals makes Ward identically compatible without an additional algebraic initial-amplitude constraint.
- **Proven in constant-Q reference radiation:** the indicial roots 0,1/2; bounded X₂ is insufficient.
- **Physical input still required:** demonstrate full covariant action regularity and choose between (A) explicit no-independent-aether mode (then evaluate the physical-past Volterra selection and oscillator history) and (B) permissible independent primordial aether mode (then observational template becomes a family, not a unique prediction). Avoid assigning favorable amplitudes from DES residuals.
- **Not attempted:** new CLASS run, physical \(k,z\) transfer, numerical scan, DES detection, model fitting.
- **Flags:** `REDUCED_PRIMORDIAL_XS_TWO_AMPLITUDE_OBSTRUCTION_EXACT / FULL_COVARIANT_PRIMORDIAL_SELECTION_OPEN / FULL_PHYSICS_GO=false / DES_detection=false`.

**Priority:** perform exactly one **full original-action primordial boundary/Noether classification**, checking actual aether electric/tilt and total stress/regularity of both branches in the strict Exp cosmological past. If that cannot select them, document the irreducible physical ambiguity rather than creating another numerical PASS sequence.
