# GE19 — physically regular leading AeST velocity and closed pressureful Exp radiation source, without guessing an initial mode

**22 November 2026 | new original-background analytic boundary for the existing 19-variable Einstein–AeST coefficient system.** The original quarter-action CLASS candidate has a researcher-verified executable; **no new CLASS run, DES input, fitting, numerical sweep, or artificially reset bath** is used here.

**Source module**: [primordial_exp_pressureful_joint_k2_system_20261122.py](../ge19/physics_gate/primordial_exp_pressureful_joint_k2_system_20261122.py) now exports the exact `leading_aest_photon_slip_source`, `strict_radiation_pressureful_exp_source` and `frozen_exp_strict_radiation_pressure_bound`. Its full 19-coefficient evolution still requires the physical initial state and action+Ward selection.

## 1. Exactly select the finite leading AeST velocity — no dust assumption

In conformal Newtonian gauge, `d_A=\delta_A/(1+w_A)` and `\theta_A=k² V_{A0}+O(k⁴)`. The **original pressureful effective-fluid** Euler row at order k⁰ of the velocity *potential* is

```math
V_{A0}'+(1-3c_A²)\mathcal H V_{A0}=\Psi_0+c_A² d_{A0}.
```

The original shift-symmetric Exp background implies `Q'/Q=-3c_A²\mathcal H`, so for **arbitrary time-varying** `w_A(a),c_A²(a),Q(a)` (and actual `\mathcal H`) this has an **exact integrating factor**:

```math
\boxed{(aQV_{A0})'=aQ(\Psi_0+c_A²d_{A0}).}\tag{1}
```

Therefore

```math
V_{A0}(\tau)=\frac{1}{a(\tau)Q(\tau)}
\left[C_A+\int_{\tau_{\rm past}}^\tau a(s)Q(s)
(\Psi_0(s)+c_A²(s)d_{A0}(s))\,ds\right].
```

The independent homogeneous piece `C_A/(aQ)` has an unbounded early-time velocity potential on the strict original positive Exp branch, since `Q=Q_0+Z_0Z`, `Z²+\ln Z=-3\ln a+\mathrm{const}`, and `aQ\to0` as `a\to0`. If one **physically requires bounded** `V_{A0}` and a convergent bounded forcing, this excludes `C_A\ne0` and selects the no-free-growing-velocity branch. This is a genuine **partial** primordial mode selection, not a proof that all scalar/aether amplitudes are fixed or that every gauge representation has the same simple regularity condition.

Also `d_{A0}'=3\Phi_0'` and `\delta_{\gamma0}'=4\Phi_0'`; thus `S_{A\gamma,0}=d_{A0}-3\delta_{\gamma0}/4` is exactly conserved on the first-order source system. Set it zero by the *adiabatic initial-state requirement*, not by the differential equation alone.

## 2. The leading AeST–photon velocity equality is EXACT even for running sound speed

In the **strict radiation leading metric** `a=A\tau`, `\mathcal H=1/\tau`, `\Psi_0=\mathrm{const}`, `d_{A0}=-3\Psi_0/2`, the regular solution of (1) is

```math
\boxed{V_{A0}=\frac{\tau\Psi_0}{2}=V_{\gamma0}.}\tag{2}
```

Substitution into the *original* AeST pressureful Euler row gives an identically vanishing residual **for any running** `c_A²(\tau)`; no approximation `c_A²=0` was made. The previous exact source operator implies

```math
S_{A\gamma,2}'=V_{\gamma0}-V_{A0}=0
```

at this strict radiation leading order, assuming no independent velocity/entropy homogeneous branch. Thus generic statements that the k² relative entropy **must** be generated at leading radiation order are false: it can first enter through matter loading/backreaction and the evolved metric.

## 3. The exact physical source that can generate next-order AeST–photon entropy

Let `R_b=3\rho_b/(4\rho_\gamma)` denote the photon baryon-loading parameter (not the AeST enthalpy). Set `u=V_{A0}-V_{\gamma0}` and `S_0=d_{A0}-3\delta_{\gamma0}/4`. Subtract the exact pressureful AeST Euler and tight-coupled photon–baryon Euler **on the same expanding background**. The result, independently simplified symbolically for arbitrary `c_A²,\mathcal H,R_b,\Psi_0`, is

```math
\boxed{
(aQu)'=aQ\left[
\left(3c_A²-\frac{1}{1+R_b}\right)
\left(\mathcal H V_{\gamma0}+\frac{\delta_{\gamma0}}4\right)
+c_A² S_0
\right].}\tag{3}
```

With `S_0=0` and the regular condition `\lim_{\tau\to0}aQu=0`, Eq. (3) determines the slip from the *actual* Einstein + photon–baryon leading solution instead of treating it as an arbitrary free parameter. Since `S_{A\gamma,2}'=-u`, it also supplies an explicit nested causal integral for the next-order relative entropy, with `S_{A\gamma,2}(0)=0` if the physical branch is strictly adiabatic.

In the strict radiation solution of (2), `\mathcal H V_{\gamma0}+\delta_{\gamma0}/4=\Psi_0/2-\Psi_0/2=0`, so the **entire exact right-hand side vanishes**, despite nonzero Exp `c_A²`. Any actual first nonzero entropy source must therefore be calculated from corrections to `\mathcal H,V_\gamma,\delta_\gamma` and baryon loading in the **fully coupled** system. It cannot be guessed from the small nonzero sound speed alone.

## 4. A new exact pressureful `Delta_A2` boundary in the leading radiation limit

Retain `Q(\tau)` and `c_A²(\tau)` from the original Exp shift-charge law **exactly**, while using the strict leading radiation metric (`a=A\tau`, all matter backreaction omitted only at the asymptotically small `\rho_{A,b}/\rho_r` order). Write its previously source-derived radiation+massless-neutrino potentials as

```math
\Phi_2=f(R_\nu)\Psi_0\tau²,\qquad
\Psi_2=g(R_\nu)\Psi_0\tau²
```
where `R_\nu=\rho_\nu/(\rho_\nu+\rho_\gamma)` and

```math
f(R)=-\frac{56R²+580R+525}{630(2R+25)},\qquad
g(R)=\frac{56R²+10R-525}{630(2R+25)}.
```

The no-isocurvature density solution of the AeST continuity row, requiring no independent k² constant mode, is

```math
\boxed{d_{A2}=D(R_\nu)\Psi_0\tau²,\quad D=3f-\frac14.}\tag{4}
```

The *pressureful* Euler row is

```math
V_{A2}'+(1-3c_A²)\frac{V_{A2}}{\tau}
=\Psi_0\tau²\left[g+c_A²D\right].
```

Use the exact Exp law `Q'/Q=-3c_A²/\tau`, multiply by `aQ`, and integrate by parts. The regular, no-free-velocity solution is

```math
\boxed{
V_{A2}=\Psi_0\left[
\left(g+\frac{4D}{3}\right)\frac{\int_0^\tau s³Q(s)\,ds}{\tau Q(\tau)}
-\frac{D}{3}\tau³\right].
}\tag{5}
```

The boundary term `s^4Q(s)\to0` follows from the Exp positive branch's logarithmic growth of Q as `s\to0`. Taking the **actual enthalpy-normalized comoving density** from the shared all-species k² operator,

```math
\Delta_{A2}=d_{A2}+\frac3\tau V_{A2},
```

all explicit D terms cancel. The result is a surprisingly simple **exact pressureful Exp reference-radiation source**:

```math
\boxed{
\Delta_{A2}^{\rm rad,Exp}=
-\frac{15+4R_\nu}{40}\Psi_0\,\tau²\,\mathcal F_Q(\tau),
\qquad
\mathcal F_Q(\tau)=
\frac{4}{\tau⁴ Q(\tau)}\int_0^\tau s³Q(s)\,ds.
}\tag{6}
```

The coefficient `-(15+4R_\nu)/40` comes from the **independently solved six-equation radiation+neutrino Einstein/Boltzmann system** in [the original archived source](../ge19/physics_gate/radiation_neutrino_delta_source_20261111.py). Its older dustlike AeST approximation corresponds exactly to `\mathcal F_Q=1`. Equation (6) now retains the *full original Exp running pressureful effect* on the regular AeST **test-fluid radiation boundary**, instead of just asserting that the sound speed is small.

This is not the complete finite-`y_m` physically backreacted mode, and it does NOT solve the free regular scalar/aether `X_2,S_2` amplitudes, full Ward, or the actual k,z Weyl transfer.

## 5. Rigorous bound for the frozen Exp parameters — what IS and is NOT negligible

On the frozen positive Exp branch, the independent original-background audit established uniformly

```math
0\le c_A²\le c_{\max}=
\frac{Z_0}{2\sqrt2 Q_0}
=\frac{10^{-17}}{2\sqrt2\,10^{-4}}
=3.53553390593\times10^{-14}.
```

From `Q'/Q=-3c_A²/\tau` and `s\le\tau`, we have `1\le Q(s)/Q(\tau)\le(\tau/s)^{3c_{\max}}`, and hence (when `3c_{\max}<4`)

```math
\boxed{
1\le\mathcal F_Q(\tau)\le\frac4{4-3c_{\max}},
\quad
0\le\mathcal F_Q-1\le
\frac{3c_{\max}}{4-3c_{\max}}
=2.65165042945\times10^{-14}.
}\tag{7}
```

**This bounds ONLY the pressureful-running-Q correction to the strict radiation, nonbackreacting AeST comoving source** (6). It does **not** bound the physical finite-density Einstein/matter backreaction, the `X_2,S_2` dynamics, bath history, matter–Weyl metric response, the DES shape or `eta`. Avoid turning this mathematically precise tiny correction into an unjustified claim that gravity memory itself is negligible.

## 6. Einstein constraints genuinely propagate in the assembled full Exp coefficient operator

Let `\mathcal C_i` be the k⁰ or k² total **comoving Einstein constraint**, with the explicit k² metric term as in [the joint operator note](ge19_20261122_joint_pressureful_Exp_primordial_k0_k2_ode_and_entropy_selection.md). Define `\mathcal M_i=(R_\gamma+\rho_b)V_{\gamma i}+R_\nu V_{\nu i}+R_AV_{Ai}` and `\rho_{\rm tot}=\rho_\gamma+\rho_\nu+\rho_b+\rho_A`. Independently differentiate each `\mathcal C_i` using **all 19 equations** and the exact full background laws

```math
a'=a\mathcal H,\;\;
\rho_{\gamma,\nu}'=-4\mathcal H\rho_{\gamma,\nu},\;\;
\rho_b'=-3\mathcal H\rho_b,\;\;
\rho_A'=-3\mathcal H R_A,\;\;
R_A'=-3\mathcal H(1+c_A²)R_A,
```
```math
\mathcal H'=\mathcal H²-\frac32a²(R_\gamma+R_\nu+\rho_b+R_A).
```

A direct independent symbolic simplification gives the **exact constraints-propagation identity for each order**:

```math
\boxed{
\mathcal C_i'+3\mathcal H\mathcal C_i
=3\bigl(a²\rho_{\rm tot}-\mathcal H²\bigr)\mathcal M_i
=0,\quad i=0,2,
}\tag{8}
```

where the final zero uses the **actual** full Friedmann equation `\mathcal H²=a²\rho_{\rm tot}`. The two orders were independently simplified exactly (not fitted numerically). Therefore if the coupled initial state satisfies the total comoving Einstein condition, it preserves that condition throughout **this truncated primordial fluid–Einstein system**. It does **not** prove the full unreduced AeST scalar/aether Ward or the full CLASS production hierarchy. The Hamiltonian and comoving constraints are equivalent once momentum evolution has already been imposed; do not count them as four independent constraints.

## 7. Decision: isolate the true remaining selection problem

We now have **(i)** a unique *bounded* leading AeST velocity for given physical metric+entropy source, **(ii)** an explicit generated next-order relative-entropy kernel, **(iii)** an exact pressureful Exp leading radiation source `Delta_A2` and a very tight independent error bound relative to the dustlike *radiation reference* for the frozen parameters, and **(iv)** proof that the full Exp coefficient Einstein constraint propagates once imposed initially.

What is **still not done**: select the growing mode of the **entire finite-k covariant Einstein–AeST–NL0B** system, including nontrivial `X_2,S_2` homogeneous/Noether sector, include the first nonzero `\rho_A/\rho_r` and `\rho_b/\rho_r` metric backreaction in the *pressureful* k² coefficient (the older 42-gate dustlike mixed coefficient is not a substitute), transport the actual positive bath from the physical past, and compute the full finite-k matter–Weyl transfer.

**One targeted next calculation**: extend the leading reference-radiation boundary (6) by the first jointly conserved physical Exp matter fraction correction within the **same** 19-variable coefficient operator, and simultaneously impose the action's scalar-current/Ward regularity on `X_2,S_2`. If one cannot select a unique physical primordial mode, stop and report that obstruction rather than launching another artificial CLASS/Asimov campaign.

**Status:** `PRESSUREFUL_EXP_RADIATION_DELTA_A2_EXACT_BOUND / CONSTRAINTS_PROPAGATE_IN_K0_K2_OPERATOR / HOMOGENEOUS_AEST_VELOCITY_SELECTED_CONDITIONALLY / FULL_PRIMORDIAL_GROWING_MODE_OPEN / FULL_PHYSICS_GO=false / DES_detection=false`.
