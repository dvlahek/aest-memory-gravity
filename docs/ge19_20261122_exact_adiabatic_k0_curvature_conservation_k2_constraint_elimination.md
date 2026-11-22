# GE19 — Exact adiabatic Einstein–Exp invariant manifold and constrained 8-equation primordial k² source

**22 November 2026. A materially stronger reduction of the already archived 19-variable, pressureful Einstein–AeST+photon/baryon/neutrino early-universe source.** Original positive Exp background; conformal Newtonian gauge; tightly coupled photons/baryons; massless free-streaming neutrinos through octupole; \(8\pi G/3=1\); **conditional original reduced action assumption** \(X=S_A=O(k²)\). This is not a full covariant AeST+NL0B growing-mode or DES observation.

**Reproducible source:** [primordial_exp_adiabatic_k0_k2_reduced_20261122.py](../ge19/physics_gate/primordial_exp_adiabatic_k0_k2_reduced_20261122.py), comparing its reconstructed state/derivatives with every row of the locked [19-coefficient original Exp fluid–Einstein source](../ge19/physics_gate/primordial_exp_pressureful_joint_k2_system_20261122.py), original blob `716ba23eaeb683c48a0f2fdcae52663b8d4bfe70`. Independent symbolic reduction has been checked (not a CLASS run).

## 1. The exact leading adiabatic submanifold at arbitrary positive Exp scale factor

Let \(h=\mathcal H\), \(R_\gamma=4\rho_\gamma/3\), \(R_\nu=4\rho_\nu/3\), \(R_A=\rho_A+p_A\), and \(R_T=R_\gamma+R_\nu+\rho_b+R_A\). The pressureful AeST enthalpy-normalized contrast is \(d_A=\delta_A/(1+w_A)\). Select common **adiabatic** density/velocity initial data at \(k^0\):

```math
\boxed{
V_{\gamma0}=V_{\nu0}=V_{A0}=V,\qquad
\delta_{\gamma0}=\delta_{\nu0}=-4hV,\qquad
\delta_{b0}=d_{A0}=-3hV.
}\tag{1}
```

These are *restrictions on the primordial initial branch*, not automatic consequences of any arbitrary AeST perturbation. They imply **individual** photon, neutrino, baryon and AeST *comoving density contrasts vanish at \(k^0\)*, rather than merely their weighted Einstein sum.

Substitute Eq. (1) in the **actual full-background** Euler rows:
```math
V_{\gamma0}'=\frac{-hR_b V+\delta_{\gamma0}/4}{1+R_b}+\Psi_0
=-hV+\Psi_0,\qquad
V_{\nu0}'=\delta_{\nu0}/4+\Psi_0=-hV+\Psi_0,
```
```math
V_{A0}'=-hV+\Psi_0+
c_A²(d_{A0}+3hV)=-hV+\Psi_0.
```
Thus **all three velocities remain equal**, with *arbitrary running \(c_A²(a)\), \(w_A(a)\), baryon loading* and neutrino shear. Use the exact Exp+all-species background derivative
```math
h'=h²-\frac32a²R_T
```
and the shared Einstein momentum source
```math
\Phi_0'=-h\Psi_0+\frac32a²R_TV
```
to check directly
```math
(-4hV)'=4\Phi_0',\quad(-3hV)'=3\Phi_0'.
```
Hence the density relations are also **dynamically invariant**, including pressureful AeST, not merely initial guesses. These identities were independently simplified symbolically to zero for arbitrary \(h,R_T,c_A²,R_b,\Phi,\Psi\). The k⁰ total Einstein comoving constraint is identically satisfied term by term.

**New exact conserved quantity on this submanifold:**
```math
\boxed{\mathcal R:=\Phi_0+hV,\qquad
\mathcal R'=\Phi_0'+h'V+hV'=0.}\tag{2}
```
This is the leading comoving-curvature amplitude in these Newtonian-gauge conventions. Its conservation holds in the supplied pressureful Exp + all-species coefficient system at **any early time where the retained Boltzmann/tight-coupling approximation applies**, not just to first order in \(\rho_A/\rho_r\). A full covariant scalar/aether action Ward certificate is still required to promote this adiabatic fluid submanifold to the unique physical AeST mode.

## 2. Solve the *complete* leading metric+matter backreaction by a two-component Volterra system

Let \(Z_{\nu0}\) be the neutrino shear coefficient defined by \(\sigma_\nu=k²Z_{\nu0}+O(k⁴)\), so
```math
\Psi_0=\Phi_0-\frac92 a²R_\nu Z_{\nu0}
=\mathcal R-hV-\frac92a²R_\nu Z_{\nu0}.
```
The full k⁰ multi-species evolution reduces **exactly** to
```math
\boxed{
V'=\mathcal R-2hV-\frac92a²R_\nu Z_{\nu0},\qquad
Z_{\nu0}'=\frac4{15}V,\qquad \mathcal R'=0.
}\tag{3}
```
Equivalently, for the *physical-past regular mode*, the causal Volterra relations are
```math
\boxed{
V(\tau)=\frac1{a(\tau)^2}
\int_0^\tau a(s)^2
\left[\mathcal R-\frac92a(s)^2R_\nu(s)Z_{\nu0}(s)\right]\,ds,
\quad
Z_{\nu0}(\tau)=\frac4{15}\int_0^\tau V(s)\,ds .
}\tag{4}
```
In Eq. (4), \(a(\tau)\) comes from **the actual Exp + photon + neutrino + baryon Friedmann evolution**, not a frozen radiation fit; this *automatically retains all leading \(\rho_A/\rho_r,\rho_b/\rho_r\) metric backreaction* within the exact coefficient operator. No external dustlike metric amplitudes, no source reinterpretation, and no bath reset. This is a definition of the physical-past regular solution, not yet its evaluation on a finite CLASS time grid.

**Pure radiation normalization and uniqueness at leading order.** As \(\tau\to0\), set \(R=\rho_\nu/(\rho_\nu+\rho_\gamma)\), \(a\propto\tau\), \(h=1/\tau\), \(a²R_\nu=4R/(3\tau²)\). The unique regular nonzero-curvature solution has
```math
\boxed{
V\sim\frac{\mathcal R}{3+4R/5}\tau,\quad
Z_{\nu0}\sim\frac{2\mathcal R}{15(3+4R/5)}\tau²,\quad
\Psi_0\sim\frac{2\mathcal R}{3+4R/5},\quad
\Phi_0\sim\left(1+\frac{2R}{5}\right)\Psi_0 .
}\tag{5}
```
For the \(\mathcal R=0\) homogeneous system, \(V\sim\tau^p\) has indicial polynomial \((p+1)(p+2)+8R/5=0\), whose two roots have negative real part for \(0\le R\le1\). Thus **boundedness of the leading \(k^0\) metric/velocity mode rejects its homogeneous solutions** in the strict radiation limit; the growing adiabatic submanifold is selected by one \(\mathcal R\) normalization, within the stated fluid/Einstein sector. A possible independent aether stress-null mode at \(k²\) remains a **different unresolved problem**.

## 3. A stronger relative-entropy result: k² density is adiabatic even after metric backreaction

The exact original 19-variable normalized density equations imply
```math
(d_{A2}-3\delta_{\gamma2}/4)'=V_{\gamma0}-V_{A0},\quad
(\delta_{\nu2}-\delta_{\gamma2})'=\frac43(V_{\gamma0}-V_{\nu0}),\quad
(\delta_{b2}-3\delta_{\gamma2}/4)'=0.
```
Equation (1) makes **all these derivatives zero identically for arbitrary full Exp background**. Therefore if one selects zero initial primordial relative entropy at order \(k²\),
```math
\boxed{\delta_{\nu2}=\delta_{\gamma2}=D_2,\qquad
\delta_{b2}=d_{A2}=\frac34D_2,}\tag{6}
```
these relations remain true through the retained full evolving \(k²\) Einstein–matter system. This corrects the earlier weaker suggestion that the leading matter-fraction correction itself necessarily generates \(k²\) AeST/photon entropy. **At the next order \(k⁴\)**, \(V_{A2}-V_{\gamma2}\) can generate a nonzero relative entropy; nothing here excludes that response.

## 4. Exactly seven k² equations — no fixed-radiation proxy

Set \(P_2=\Phi_2\), \(D_2=\delta_{\gamma2}\), \(G_2=V_{\gamma2}\), \(N_2=V_{\nu2}\), \(A_2=V_{A2}\), \(Z_2=Z_{\nu2}\), \(J_3=F_{\nu3}/k³\). With \(\Psi_2=P_2-\frac92a²R_\nu Z_2\) and \(R_b=3\rho_b/(4\rho_\gamma)\), the full coupled pressureful-source operator is

```math
\boxed{\begin{aligned}
P_2'&=-h\Psi_2+\frac32a²[(R_\gamma+\rho_b)G_2+R_\nu N_2+R_AA_2],\\
D_2'&=-\frac43V+4P_2',\\
G_2'&=\frac{-hR_bG_2+D_2/4}{1+R_b}+\Psi_2,\\
N_2'&=D_2/4+\Psi_2-Z_{\nu0},\\
A_2'&=-hA_2+\Psi_2+c_A²\left(\frac34D_2+3hA_2\right),\\
Z_2'&=\frac4{15}N_2-\frac3{10}J_3,\\
J_3'&=\frac67Z_{\nu0}.
\end{aligned}}\tag{7}
```

These seven first-order ODEs plus Eq. (3) (two evolving values) are *exactly equivalent to all 19 fluid/Einstein coefficient rows on the selected k⁰ and k² adiabatic manifold*, after taking the background derivative \(h'=h²-\frac32a²R_T\) into account. They include **all finite early-time matter fractions through the exact background source**, not only first order in \(y_m\). This is a mathematically closed coefficient operator, not a completed finite-\(k\) CLASS solver.

## 5. Eliminate the last Einstein k² constraint: only six evolving k² unknowns

The *one independent* order-\(k²\) Einstein comoving Cauchy constraint is

```math
\boxed{
\mathcal C_2=
\underbrace{\left[\rho_\gamma+\rho_\nu+\frac34(\rho_b+R_A)\right]}_{A_D>0}D_2
+3h\underbrace{\left[(R_\gamma+\rho_b)G_2+R_\nu N_2+R_AA_2\right]}_{M_2}
+\frac{2\Phi_0}{3a²}=0.}\tag{8}
```

All coefficients \(A_D,R_A\) retain the original Exp pressure, and \(A_D>0\) on the frozen positive model. Therefore we can **eliminate** the full density coefficient instead of choosing it or fitting it:

```math
\boxed{
D_2(t)=-
\frac{3hM_2+2\Phi_0/(3a²)}
{\rho_\gamma+\rho_\nu+\frac34(\rho_b+R_A)},\qquad
\Delta_{A2}=\frac34D_2+3hA_2.
}\tag{9}
```

The second quantity is **the actual full Einstein-constrained, pressureful input for the original quarter-action \(X_2,S_2\) and causal bath**. It is not the dustlike fixed-radiation source from the older mixed-series report.

**Preservation of the removed photon continuity equation:** differentiate (8), insert *all seven equations* in (7), the exact background \(\rho_{\gamma,\nu}'=-4h\rho_{\gamma,\nu},\rho_b'=-3h\rho_b,R_A'=-3h(1+c_A²)R_A\), the Einstein Raychaudhuri law \(h'=h²-\frac32a²R_T\), and \(\Phi_0'=-h\Psi_0+\frac32a²R_TV\). Independent symbolic simplification gives

```math
\boxed{\mathcal C_2'+3h\mathcal C_2=0.}\tag{10}
```

No new free forcing appears in the \(k²\) constraint. Thus imposing \(\mathcal C_2=0\) initially and evolving the remaining six variables is **mathematically equivalent** to evolving seven and conserving the constraint. Explicit functions `constrained_photon_density_k2`, `constrained_rhs`, `constrained_driver_delta_A2` implement Eqs. (8)–(10) in the linked source.

**Total complexity:** **eight dynamical first-order equations** (two leading metric/neutrino variables plus six \(k²\) coefficients) and **one conserved curvature amplitude \(\mathcal R\)**. This replaces the original 19-variable coupled primordial source subsystem on the selected adiabatic branch. It does *not* eliminate the missing \(X_2,S_2\) equations from the complete original AeST action.

## 6. What this DOES and DOES NOT finish

**Established within the already derived early Einstein + pressureful AeST + photons/baryons/massless neutrino coefficient operator:** exact leading all-species adiabatic invariant manifold, unique bounded strict-radiation \(k^0\) solution for given curvature, conserved curvature, exact \(k²\) no-relative-entropy invariant, complete finite-background backreacted **equation** for \(\Delta_{A2}\) without a dust proxy, and valid \(19\to8\) dynamical coefficient reduction.

**Not established:** *full original unreduced covariant action* scalar/aether/multiplier/Ward equivalence; the physical \(X_2,S_2\) regular/homogeneous source selection; absence of a physical AeST scalar isocurvature mode at \(k²\); a uniquely selected global \(k²\) growing solution and actual numerical coefficients on Exp background; physically transported NL0B auxiliary data \((q_j,p_j)\); any finite-\(k\) Weyl transfer or DES significance. The adiabatic submanifold **is a branch assumption consistent with this fluid sector**, not a proof that the full gravitational memory theory must realize it.

**Next single physical calculation:** solve the remaining 8-dimensional constrained k² coefficient system with its *regular past* boundary, **simultaneously** enforce the original scalar-current/Ward at \(k²\) to select \(X_2,S_2\) without a hidden homogeneous mode, and reconstruct the full Einstein source \(\Delta_{A2}(t)\) from Eq. (9). Transport the no-free bath from that selected history; only then does the original quarter-force have a physical signed Weyl prediction.

**Flags:** `ADIABATIC_FLUID_EINSTEIN_K0_K2_REDUCTION_DERIVED`; `FULL_PRIMORDIAL_ACTION_WARD_MODE_OPEN`; `FULL_PHYSICS_GO=false`; `DES_detection=false`.
