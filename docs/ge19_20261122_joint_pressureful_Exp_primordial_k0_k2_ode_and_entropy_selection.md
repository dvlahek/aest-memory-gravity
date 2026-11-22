# GE19 — Original Exp pressureful all-species primordial coefficient system at k⁰ and k²

**22 November 2026 | physics-first.** The quarter/enthalpy CLASS C executable is built and ELF-verified (SHA-256 `9b63ca76f1b308f31d78cfea3cf65c097f4d70eb55582188b7e587512a8230b9`). This note makes the *actual missing Einstein–matter source* for the k² AeST bath hierarchy computationally explicit without inventing primordial initial data or fitting DES.

**New source module:** [primordial_exp_pressureful_joint_k2_system_20261122.py](../ge19/physics_gate/primordial_exp_pressureful_joint_k2_system_20261122.py). It assembles **19 first-order coefficient equations** and two equivalent representations of the two Einstein initial-value constraints, on the original expanding Exp background. It **does not** integrate a guessed physical mode or certify the unreduced covariant action.

## 1. Exact background and precise expansion

All equations use conformal time `tau`, `\mathcal H=a'/a`, Newtonian `\Phi,\Psi`, CLASS-normalized `8 pi G/3=1`, early photon-baryon tight coupling, massless free-streaming neutrinos and minimally coupled pressureful AeST in place of CDM. Keep `w_A(a)` and `c_A²(a)` as *running functions*, not a dust fit.

The original frozen positive Exp branch has

```math
Q=Q_0+Z_0 Z,\qquad
K_Q=4K_2 Z_0 Z e^{Z²}=I_0a^{-3},\qquad
K=2K_2Z_0²(e^{Z²}-1),
```
```math
\rho_A=(QK_Q-K)/3,\quad
R_A=\rho_A+p_A=QK_Q/3,\quad
w_A=K/(QK_Q-K),\quad
c_A²=\frac{Z_0Z}{Q(1+2Z²)}.
```

The positive `Z(a)` is uniquely determined by the scalar shift charge `Z²+\log Z=\log[I_0/(4K_2 Z_0)]-3\log a`. The source code solves this monotonic equation and uses the exact species background `\rho_\gamma,\rho_\nu\propto a^{-4}`, `\rho_b\propto a^{-3}`, `\mathcal H²=a²(\rho_\gamma+\rho_\nu+\rho_b+\rho_A)`. Its caller must supply the calibrated `I_0` and standard-species normalizations; no substitute values are guessed.

Define `d_A:=\delta_A/(1+w_A)`. For all scalar densities/potentials `Y(k,\tau)=Y_0(\tau)+k²Y_2(\tau)+O(k⁴)`. Scale velocity divergence and neutrino multipoles as

```math
\theta_s=k²(V_{s0}+k²V_{s2}+\cdots),\quad
\sigma_\nu=k²(Z_{\nu0}+k²Z_{\nu2}+\cdots),\quad
F_{\nu3}=k³J_{\nu3}+\cdots .
```

There are exactly 19 real coefficient functions:
`Phi0,Phi2; delta_gamma0,2; delta_nu0,2; delta_b0,2; d_A0,2; V_gamma0,2; V_nu0,2; V_A0,2; Z_nu0,2; J_nu3`.

## 2. Fully coupled momentum/shear equations to both orders

With `R_\gamma=4\rho_\gamma/3`, `R_\nu=4\rho_\nu/3`, `R_A=\rho_A(1+w_A)`, for each `i=0,2`:

```math
\boxed{\Psi_i=\Phi_i-\frac92a²R_\nu Z_{\nu i},\quad
\Phi_i'=-\mathcal H\Psi_i+
\frac32a²\left[(R_\gamma+\rho_b)V_{\gamma i}
+R_\nu V_{\nu i}+R_A V_{Ai}\right].}\tag{1}
```

The source does *not* freeze the photon/neutrino metric to the old dustlike solution: all four background stress components feed (1) at each order. Even a tiny AeST sound speed does not justify neglecting the background gravitational source.

## 3. Pressureful AeST and ordinary-species coefficient dynamics

The exact original AeST effective-fluid density+Euler pair (under the conditional `S_A=O(k²)` branch) gives

```math
\boxed{
d_{A0}'=3\Phi_0',\qquad
d_{A2}'=-V_{A0}+3\Phi_2',
\qquad
V_{Ai}'=-\mathcal H V_{Ai}+\Psi_i+
c_A²(d_{Ai}+3\mathcal H V_{Ai}).
}\tag{2}
```

No constant-`w` assumption is used: the background identity `w_A'=-3\mathcal H(1+w_A)(c_A²-w_A)` removes its derivative from the normalized continuity equation.

Photons, free-streaming neutrinos and baryons obey at the appropriate retained order

```math
\delta_{\gamma0}'=4\Phi_0',\quad
\delta_{\gamma2}'=-\frac43V_{\gamma0}+4\Phi_2',
\quad
\delta_{\nu0}'=4\Phi_0',\quad
\delta_{\nu2}'=-\frac43V_{\nu0}+4\Phi_2',
```
```math
\delta_{b0}'=3\Phi_0',\quad
\delta_{b2}'=-V_{\gamma0}+3\Phi_2',
\quad
R_b=\frac{3\rho_b}{4\rho_\gamma},
```
```math
V_{\gamma i}'=
-\frac{\mathcal H R_b}{1+R_b}V_{\gamma i}
+\frac{\delta_{\gamma i}}{4(1+R_b)}+\Psi_i,
\quad
V_{\nu0}'=\frac{\delta_{\nu0}}4+\Psi_0,
\quad
V_{\nu2}'=\frac{\delta_{\nu2}}4+\Psi_2-Z_{\nu0}.
```

Neutrino quadrupole and octupole are retained exactly to the coefficient order required for the Einstein shear at k²:

```math
Z_{\nu0}'=\frac4{15}V_{\nu0},\quad
Z_{\nu2}'=\frac4{15}V_{\nu2}-\frac3{10}J_{\nu3},\quad
J_{\nu3}'=\frac67Z_{\nu0}.\tag{3}
```

This **is a closed 19-variable linear coefficient operator** when the Exp background is supplied, but it is not yet a uniquely selected Cauchy solution. Its validity is limited to primordial `k\tau\ll1`, tightly coupled baryons+photons and relativistic neutrinos. Do not continue this truncated hierarchy through recombination or the finite DES k range.

## 4. The *actual* physical source for the next AeST X₂/S₂ stage

The coefficient needed by the original reduced AeST bath is now **an actual state output**, not the frozen radiation/dustlike analytic proxy:

```math
\boxed{
\Delta_{A2}=d_{A2}+3\mathcal H V_{A2}. }\tag{4}
```

The total Einstein comoving constraints are

```math
\mathcal C_0=\sum_{s=\gamma,\nu,b}
[\rho_s\delta_{s0}+3\mathcal H R_s V_{s0}]
+R_A(d_{A0}+3\mathcal H V_{A0})=0,
```
```math
\boxed{
\mathcal C_2=\sum_{s=\gamma,\nu,b}
[\rho_s\delta_{s2}+3\mathcal H R_s V_{s2}]
+R_A(d_{A2}+3\mathcal H V_{A2})
+\frac{2\Phi_0}{3a²}=0.}\tag{5}
```

Here `R_b^{(stress)}=\rho_b`, while `R_b` in the photon drag is the unrelated conventional **baryon loading** `3\rho_b/(4\rho_\gamma)`; the code keeps these separate. Equation (5) is an essential **initial eigenvector constraint**, not an extra ODE. The Einstein Hamiltonian equations are **algebraically redundant** with (5) once the Einstein momentum equation (1) has been imposed:
```math
\mathcal H\!am_i=\frac32a²\mathcal C_i\qquad (i=0,2).
```
Thus they provide two presentations of the same condition, **not four independent tests**. Physical consistency additionally requires the independently derived scalar-current/Ward equations and the proper limiting adiabatic initial state.

## 5. A genuine new analytic entropy/velocity relation

Define the gauge-invariant leading and next-coefficient AeST–photon relative-entropy perturbation

```math
S_{A\gamma,i}=d_{Ai}-\frac34\delta_{\gamma i}.
```

Subtracting the explicit photon and AeST continuity equations yields the **exact coefficient identities**

```math
\boxed{
S_{A\gamma,0}'=0,\qquad
S_{A\gamma,2}'=V_{\gamma0}-V_{A0}.}\tag{6}
```

For the tightly coupled baryons, `(\delta_{bi}-3\delta_{\gamma i}/4)'=0` through i=2. For massless free-streaming neutrinos,
```math
(\delta_{\nu2}-\delta_{\gamma2})'
=\frac43(V_{\gamma0}-V_{\nu0}).
```

**Consequences:** the two new CLASS enthalpy initial-condition corrections remove the artificial **leading** AeST/photon relative entropy, but do *not* ensure a fully adiabatic k² mode. Even if `S_{A\gamma,2}(\tau_i)=0`, nonzero relative leading velocity creates next-order relative entropy. Its amplitude and compatibility with a regular no-isocurvature physical solution depend on the coupled Einstein + scalar/aether system.

## 6. Where the triangular k²→k⁴ construction resumes

Under the **separately unproved** analytic original scalar/aether branch `X=k²X_2`, `S_A=k²S_2` and a retarded bath with no free homogeneous oscillator mode, the X₂/S₂ equation from [the original source-locked reduced hierarchy](../ge19/physics_gate/primordial_k2_XS_retarded_bath_hierarchy_20261122.py) has the actual `\Delta_{A2}` from Eq. (4). The reduced action `-k² S_A/(3a²)` matter-density stress and phase gradient `k²S_A` then enter the metric/matter at k⁴. The operator assembled here is therefore a **necessary first block**, not proof of the physical branch, nonzero metric response, or observational detectability.

The next *one* science gate is selecting a **single physically regular, correctly normalized primordial eigenvector** for (1)–(5) jointly with `X_2,S_2` and the scalar-current Ward/Noether constraints. The beginning-of-time limit is singular: the previous finite-time retarded Green kernel and the k expansion cannot simply be exchanged. Arbitrarily setting `X_2,S_2,q,p=0` at the CLASS start would impose a mode selection rather than derive it.

Do not perform another arbitrary numerical seed run, new nuisance fit or DES projection yet. Once the mode is derived, use the existing verified ELF CLASS code path with the *transported* positive bath and original quarter source to compute `(T_{\delta,1},T_{W,1})(k,z)`, **both** contributions to `\partial_\eta P_{\delta W}` and the already frozen DES 26-row nuisance-projected estimator.

**Status:** **EXACT_EXP_PLUS_PRESSUREFUL_ALL_SPECIES_K0_K2_COEFFICIENT_OPERATOR_ASSEMBLED / GROWING_MODE_NOT_SELECTED / X2_S2_PHYSICAL_RETARDED_HISTORY_NOT_SELECTED / FULL_PHYSICS_GO=FALSE / DES_detection=FALSE.**
