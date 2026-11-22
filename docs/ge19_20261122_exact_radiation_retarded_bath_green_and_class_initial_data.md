# GE19 — Exact retarded radiation-era bath transport to CLASS q/p data; why finite-time resets erase physical history

**22 November 2026; physics-first result after the verified 10/10 conditional Weyl onset and DES Y3 covariance r3.** This document derives an **actual history-to-initial-data map** from the original NL0B oscillator action. It is not a claim that the *physical original Einstein–AeST–NL0B primordial mode chi(k,t)* has yet been solved. No CLASS run, numerical scan, DES fit or observed residual inspection is performed.

## 1. Original invariant bath equations and the regular coordinate

For each original positive `omega_j,w_j` at comoving `k>0`, proper cosmic time `t`, with `chi=varphi+Q alpha_A` (linear gauge invariant), the original restricted quadratic action yields

```math
\ddot q_j+3H\dot q_j+\omega_j^2q_j
=\omega_j\sqrt{w_j}\frac{k\chi}{a},\qquad
B_\chi=W_b\chi-\frac ak\sum_j\omega_j\sqrt{w_j}q_j.
```

The *exact* change of coordinates `r_j=a omega_j sqrt(w_j)q_j/k`, already independently source-checked in [the regular-bath note](ge19_20261122_des_y3_detectability_threshold_and_exact_regular_causal_bath_operator.md), gives for arbitrary expanding `a(t)`:

```math
\boxed{\ddot r_j+H\dot r_j+(\omega_j^2-2H^2-\dot H)r_j=\omega_j^2 w_j\chi,\quad
 B_\chi=W_b\chi-\sum_jr_j.}\tag{1}
```

Crucial implementation detail from the **actual original C patch** [v019j](../v019j/apply_memory_patch.py), Git blob `14796a5ed9e6265ed6810c792a93d7328a109364`: it uses
`dy_q=p_j`, `dy_p=-2mathcal H p_j-a²omega²q_j+a k omega sqrt(w_j)chi`,
where `p_j=q'_j=dq_j/dtau`, **not** `dot q_j` in cosmic time. Its historical electric-field bath feedback is `-0.5 Q Bchi` before `K_B` normalization, whereas the original restricted action requires **`-0.25 Q Bchi`**. This document does **not** change or certify the frozen C patch.

## 2. Exact causal Green function in the radiation reference background

In the radiation power-law limit `a(t)=A sqrt(t)`, `H=1/(2t)`, so `-2H²-dot H=0` exactly. The operator becomes

```math
\boxed{L_j r_j:=\ddot r_j+\frac1{2t}\dot r_j+\omega_j²r_j=\omega_j² w_j\chi(t).}\tag{2}
```

At `t>0` its independent homogeneous solutions are
```math
f_j(t)=t^{1/4}J_{-1/4}(\omega_j t),\quad
g_j(t)=t^{1/4}J_{1/4}(\omega_jt),\quad
\mathcal W_j=f_j\dot g_j-\dot f_j g_j=\frac{\sqrt2}{\pi\sqrt t}.
```
The Wronskian was independently verified against direct derivatives of these Bessel solutions at positive t, and `L_jf_j=L_jg_j=0` was independently simplified exactly using Bessel identities. The retarded kernel (zero for `t<s`) is
```math
\boxed{G_j(t,s)=\frac{\pi\sqrt s}{\sqrt2}
\bigl[f_j(s)g_j(t)-g_j(s)f_j(t)\bigr]\Theta(t-s),\quad
\partial_tG_j(t,s)|_{t=s+}=1.}\tag{3}
```
Given an independently physically derived scalar–aether strain history `chi_0(k,s)`, the **no-independent-homogeneous-bath** choice is the causal integral
```math
\boxed{r_{j,0}^{\mathrm{ret}}(k,t)=
\omega_j^2 w_j\int_0^t G_j(t,s)\chi_0(k,s)\,ds.}\tag{4}
```
It selects both free integration constants in the general solution to zero **with respect to the specified physical past**. It does not follow from mere boundedness: `g_j(t)~sqrt(t)` is a homogeneous mode whose original `q_j~\mathrm{const.}` remains regular as `t\to0`, but is free rather than driven. Similarly `f_j(t)~\mathrm{const.}` gives `q_j~t^{-1/2}`, generally irregular in the original q variable.

**Important domain:** Eq. (3)–(4) is exact for the *reference* `a=A sqrt t`, not for the complete Exp AeST+neutrino+baryon expanding background. For the true model use Eq. (1) with the actual `H,\dot H` and an independently justified physical-past/no-free initial-state condition. Do not use a radiation Green function across radiation–matter equality.

## 3. Exact map from physically transported memory to CLASS conformal initial data

Once the physically selected history is known on the interval from its physical past to any chosen finite CLASS integration entry time `t_i>0`, Eq. (4) gives `r_i` and
```math
\dot r_{j,i}^{\mathrm{ret}}
=\omega_j^2w_j\int_0^{t_i}
\partial_tG_j(t_i,s)\chi_0(k,s)\,ds.
```
For **every** expanding background, the exact transformation back to the C patch's conformal variables is
```math
\boxed{
q_{j,i}=\frac{k r_{j,i}}{a_i\omega_j\sqrt{w_j}},
\qquad
p_{j,i}=q'_{j,i}
=\frac{k}{\omega_j\sqrt{w_j}}\bigl(\dot r_{j,i}-H_i r_{j,i}\bigr).
}\tag{5}
```
These initial values are **generally not zero** even in a wholly retarded, no-free-homogeneous-mode physical model. Setting `q=p=0` at an *arbitrary finite* `t_i` discards the earlier forcing and redefines the theory's observed history. The only legitimate zero checkpoint is one where the selected physical mode and its prior forcing actually imply the corresponding state. Eq. (5) is an exact conversion and directly resolves the previously ambiguous cosmic-vs-conformal auxiliary momentum.

The half-source old patch still fails the original quarter-action scalar-current consistency; merely supplying the correct q/p initial state would not fix that separate physics defect.

## 4. Singular radiation onset versus a reset at regular finite t_i — different coefficients

For a finite source `chi(t)=chi_n t^n+o(t^n)`, with `n>=0` and no added free bath mode, Eq. (2) has the leading sourced particular solution
```math
\boxed{r_j(t)=\frac{\omega_j²w_j\,\chi_n}
{(n+2)(n+\tfrac32)}t^{n+2}+o(t^{n+2}).}\tag{6}
```
This is immediate from `(d²/dt²+(2t)^{-1}d/dt)t^{n+2}=(n+2)(n+3/2)t^n`. In particular:

| Early `chi` behavior | Radiation-past sourced `r_j` coefficient |
|---|---|
| `chi ~ chi_0` | `omega² w chi_0 * t² / 3` |
| `chi ~ D t` | `2 omega² w D * t³ / 15` |
| `chi ~ chi_2 t²` | `omega² w chi_2 * t⁴ / 14` |

This differs from an arbitrary regular finite-time checkpoint with locally constant H: for `chi(t_i+h)~D h` and `r_i=dot r_i=0`, that calculation gives `r~omega² w D h³/6`. **Neither result invalidates the other**; they concern different limiting initial-value problems. Treating `t_i\to0` as a uniform limit of the finite-ti Taylor law is not justified, since `H~1/(2t)` becomes singular.

For finite positive Wb and spectral second moment `M2=sum_j w_j omega_j²`, the strict radiation sourced branch gives a leading **universal relative causal delay**
```math
\boxed{\frac{B_{\rm delayed}}{B_{\rm instant}}
\sim-\frac{M_2t²}{W_b(n+2)(n+3/2)}.}\tag{7}
```
This is a response *inside the bath*, not Weyl, DES shear or an observable signal by itself.

For the previously derived **conditional strict-Exp source-selected** `X_2~Dt²/[6L]`, `Q~Z0 sqrt(3L/2)`, `L=ln(t_*/t)`, one has
`chi_2 ~ k² D Z0 sqrt(3/2) t²/(6 sqrt L)`. The slowly varying logarithm leaves the leading power-law Green coefficient at `1/14` and reproduces the earlier independent reduced prediction
```math
B_{\rm delayed,2}\sim-
\frac{M_2 DZ_0\sqrt{3/2}}{84}\frac{t^4}{\sqrt L},
\quad
B_{\rm delayed}/B_{\rm instant}\sim-\frac{M_2}{14W_b}t².
```
This cross-check is **conditional on that source-selected branch**. It does not prove that the full physically adiabatic Einstein–AeST–NL0B state selects `X_2`, nor that the exact Exp a(t) remains pure radiation at a finite numerical start.

## 5. Why a finite-time CLASS reset could contaminate even a future Weyl claim

The previously proven **conditional** Einstein-projected local onset states that for transported `R(t)=sum_jr_j(t)` with `R(t_i+h)=R_mh^m+...` at regular `t_i`:
```math
\delta_h W_1=
\frac{c_i k²Q_iR_m}{8a_i²(m+1)(m+2)(m+3)}h^{m+3}+\cdots.
```
If physical prior forcing gives `R(t_i)\ne0` but the numerical pipeline resets q/p to zero at `t_i`, the **difference in the retarded-only Weyl tangent** begins at
```math
\boxed{W_{1,\mathrm{transported}}-W_{1,\mathrm{reset}}
=\frac{c_i k²Q_iR(t_i)}{48a_i²}(t-t_i)^3+\cdots,}\tag{8}
```
holding the eta0 scalar/ordinary baseline and tangent IC otherwise fixed. A reset can therefore remove an **h³** history contribution that is absent in the special **h⁶** initially relaxed local result. A nonzero `dot R(t_i)` can analogously remove h⁴. The full cosmological observable still involves cancellations, the physical initial-state derivative and integrated standard-species transfer, so Eq. (8) is a **local restricted comparator error estimate**, not a quantitative DES bias.

## 6. The exact remaining physical bottleneck — stop making new toy templates

The **regular radiation Green function and correct CLASS q/p conversion are now explicit**. The irreducible missing input to Eq. (4)/(5) is the *on-shell physical primordial* `chi_0(k,t)`, and independently the original-action matched full constraint-preserving coupled metric + photon/neutrino/baryon/AeST evolution through the DES lens window. The old dustlike AeST fixed-radiation series is **not** sufficient (20 Nov full Einstein constraint no-go). The frozen historical half-source C patch and its CDM pressureless initial density/gauge transform also remain incompatible with the original action for generic AeST equation-of-state; correcting only the memory coefficient cannot repair its primordial mode.

**Next permitted integration:** construct exactly one new isolated action-consistent implementation (do not mutate frozen v019/v019j), using original *quarter-source* `-eta Q Bchi/4`, correct `delta_A/(1+w_A)=3delta_gamma/4` and time gauge transform, jointly solved Einstein/matter + AeST eigenmode, the causal bath history-to-q/p mapping (5), and a physically verified stress/Ward residual. Compute physical `T_{\delta,1},T_{W,1}` over fixed k,z only after those conditions pass. Then the already certified 26-row DES covariance operator can assess nondegenerate gamma_t shape and nuisance-projected sensitivity. If no full physical state/bridge can be constructed, report the limited proven causal mechanism and a physical transfer blockage; do not invent a DES detection.

**Classification: RADIATION_REFERENCE_RETARDED_BATH_KERNEL_AND_CLASS_CONFORMAL_IC_MAP_DERIVED / PHYSICAL_PRIMORDIAL_CHI_NOT_SELECTED / FULL_PHYSICS_GO=FALSE / DES_DETECTION=FALSE.**
