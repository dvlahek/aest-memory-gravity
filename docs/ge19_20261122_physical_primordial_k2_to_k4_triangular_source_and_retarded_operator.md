# GE19 — Triangular physical primordial hierarchy: solve the true Einstein–matter k² mode first, then the retarded AeST X₂/S₂, then Weyl at k⁴

**22 November 2026. Physics-first result after the original quarter/enthalpy CLASS executable was independently ELF-verified (SHA-256 `9b63ca76f1b308f31d78cfea3cf65c097f4d70eb55582188b7e587512a8230b9`, researcher `EXIT=0`).** This is an *exact coefficient-level structural result of the already source-verified reduced action/Einstein dictionary under an analytic finite-k branch*, not a full-physics growing-mode selection or DES detection. No new physics parameter, CLASS simulation, amplitude proxy, or observed DES residual was used.

## 1. Fix the scope and prevent a false simplification

Work in proper cosmic time at any **fixed finite regular** epoch `a>0`; take the original background `Q,K_Q,K_{QQ},H` and positive Drude bath. Let `C=2-K_B`, `c=K_Q/(QK_{QQ})`, `R_A=QK_Q/3`; `X=chi/Q`, `S_A=K_BE_A+Cchi`. Assume (not yet physically established at primordial singularity) a real scalar analytic adiabatic branch:

```math
X=k^2X_2+O(k^4),\quad
S_A=k^2S_2+O(k^4),\quad
\Delta_A=k^2\Delta_{A2}+O(k^4),\quad
q_j=k^3q_{j3}+O(k^5).
```

The physical **ordinary species, photons/baryons/neutrinos, full Einstein metric and exact expanding Exp background are NOT held fixed**. The `O(k²)` ordinary + AeST *fluid/phase* growing state must be solved self-consistently, with all `w_A,c` terms; the earlier 42-gate dustlike mixed series is an *independent test-fluid proxy*, not an acceptable physical substitute. Do not take the `t_i\to0` singular limit of this finite-regular-time k expansion without proving uniform control. The `X=S=O(k²)` assumption itself requires selection by the physical growing-mode/Noether/Ward problem; it is not guaranteed by the leading k=0 adiabatic gauge solution.

## 2. Exact dynamical block structure of the original reduced equations

From [the original action-to-CLASS scalar matrix](ge19_20261111_joint_action_to_CLASS_scalar_source_matrix.md) and [source-locked k² hierarchy](../ge19/physics_gate/primordial_k2_XS_retarded_bath_hierarchy_20261122.py) the k² equations are

```math
\boxed{
\frac{d}{dt}
\begin{pmatrix}X_2\\S_2\end{pmatrix}
=
\underbrace{
\begin{pmatrix}
-CQ/K_B &1/K_B\\
Q(K_Q-2CQ/K_B)&CQ/K_B-H
\end{pmatrix}}_{\mathsf A_2(t)}
\begin{pmatrix}X_2\\S_2\end{pmatrix}
+
\begin{pmatrix}
c\,\Delta_{A2}\\
-\eta QB_2/4
\end{pmatrix},
}
```
```math
B_2=W_bQX_2-\sum_j r_{j2},
\quad
\ddot r_{j2}+H\dot r_{j2}
+(\omega_j^2-2H^2-\dot H)r_{j2}
=\omega_j^2w_jQX_2.
```

The full source of the *first* box is explicit, but **must be obtained from a genuinely coupled pressureful multi-species solution**. Under the above analytic adiabatic scaling, the total Einstein comoving constraint

```math
R_A\Delta_A+\Omega_s+\frac{2k²}{3a²}\Phi=0,\qquad
\Omega_s=D_s+\frac{3aH}{k²}T_s
```

requires cancellation of the k⁰ comoving source and at k² gives the **actual source to be passed into the AeST block**:

```math
\boxed{
\Delta_{A2}(t)=-
\frac{\Omega_{s2}(t)+2\Phi_0(t)/(3a(t)^2)}
{R_A(t)} .
}
```

Here `Omega_s2` is the **fully coupled** coefficient for photons, baryons and neutrinos (and any additional standard species), with all appropriate streaming and background feedback. It is **not** the fixed-radiation/dustlike test-source coefficient from the earlier rejected 20 Nov approximation. Because the expression subtracts correlated Einstein sources, computing `Omega_s2` from the leading fluid fields alone or mixing gauge conventions can generate spurious divergence and cannot be used as a numerical signal. The k² constraint does not separately determine `Omega_s2`; that comes from the same physical Einstein + species evolution.

The original `X` gradient feedback `[k²/(a²Q²K_{QQ})]S_A` is **O(k⁴)**, not O(k²). The action metric/phase dictionary is

```math
D_A^{\rm action}=
\frac{QK_{QQ}}3\delta Q
-\frac{k²}{3a²}S_A,\quad
P_A=\frac{K_Q}3\delta Q,\quad
T_A=\frac{K_Qk²\varphi}{3a},\quad
\delta Q=\dot\varphi-Q\Psi,
```
```math
\dot\varphi=Q\Psi-3Hc\varphi+
Qc\left[\Delta_A+\frac{k² S_A}{3a²R_A}\right].
```

Therefore, on this same analytic branch:
- The **direct aether-gradient contribution to action density** `-k²S_A/(3a²)` first enters `D_A` at **k⁴**.
- Its first **phase/pressure feedback** is `Qc\,k²S_A/(3a²R_A)=k⁴ S_2/(a²QK_{QQ})`, using the *exact* identity `c/R_A=3/(Q²K_{QQ})`. No inverse power of the tiny Exp `c` appears in this coefficient.
- All original `eta Bchi/4` memory forcing in the reduced dynamical system enters the k² **S₂ sector**. There is no direct linear auxiliary-bath stress in the relaxed background; consequently this source does not enter the k² **Einstein–matter sector** through the action stress or phase.

Hence, **with the action source/dictionary and regular analytic initial data**, the calculation is a genuine *triangular hierarchy through k⁴*, not the previously assumed simultaneous unknown block:

```text
actual Exp background + ordinary (gamma,b,nu,...) and AeST phase/fluid
                  + full Einstein constraints
                     |
                   [solve k²]
                     v
             physical Delta_A2(k,t)
                     |
             original forced X2/S2
                + past bath r_j2
                     |
              [source enters at k⁴]
                     v
           coupled Einstein/matter k⁴ tangent
               -> Weyl -> DES gamma_t
```

The arrows describe an **order-by-order regular expansion**, not an already computed physical transfer. Non-analytic initial states, singular primordial-time limits, an eta-dependent initial metric/phase state, an omitted direct bath stress from full covariant action, or Ward/multiplier inconsistency can invalidate this triangularity for the *real full theory*. The k² metric is not yet numerically solved here.

## 3. Closed retarded response *operator* for delayed-only k² X/S, without a guessed shear template

For a physically chosen `eta=0+` adiabatic `X_2^{(0)},S_2^{(0)}`, solve the **retarded, no-free** auxiliary state on the *actual* expanding background (radiation Green's function is an early reference, not a through-equality approximation). Let `R_2^{(0)}=\sum_jr_{j2}^{(0)}` and `U_2(t,s)` be the fundamental matrix of the known `mathsf A_2`. At order k² the ordinary + Einstein response to the *dynamical delayed-only forcing* vanishes with equal initial phase/metric/ordinary eta-tangents, so the **difference of retarded and instant-only response** `u_{h,2}=(\delta_hX_{2,1},\delta_hS_{2,1})` obeys

```math
\boxed{
\dot u_{h,2}=\mathsf A_2 u_{h,2}
+\begin{pmatrix}0\\ Q R_2^{(0)}/4\end{pmatrix},
\quad
u_{h,2}(t_\star)=0,
\quad
u_{h,2}(t)=\int_{t_\star}^t
U_2(t,s)
\begin{pmatrix}0\\Q(s)R_2^{(0)}(s)/4\end{pmatrix}\,ds .
}
```

**Strict conditions:** identical baseline/evolving background and initial eta tangents, original quarter source, and all **instantaneous-only terms** subtracted in both models; `r_{j2}^{(0)}(t_\star)` is physically transported from before `t_\star` instead of reset there. These conditions are exactly why a one-point constant-fraction DES Weyl proxy is never a physical memory signal.

For pure radiation `a=A\sqrt t`, each `r_{j2}` is the previously derived exact retarded Bessel integral from `QX_2`; for the actual multi-species expanding cosmology it is the Green operator of `ddot r+Hdot r+(\omega²-2H²-dot H)r=\omega²wQX_2`. This produces a *nested time-memory kernel*, the physically relevant delayed structure, not a flat redshift-independent amplitude.

**Source order for the subsequent independent metric calculation:** the explicit first **density** forcing in the k⁴ Einstein problem is

```math
\boxed{\delta_hD_{A,4}^{\rm direct\,S}
=-\frac{\delta_hS_{2,1}}{3a²},}
```

and the explicit first **phase** forcing is

```math
\boxed{
(\delta_h\dot\varphi_4)^{\rm direct\,S}
=+\frac{\delta_hS_{2,1}}{a²QK_{QQ}}.
}
```

These are *direct source entries*, **not** full `D_{A,4}` or `dot varphi_4`: both also contain induced `delta_h\delta Q_4,\delta_h\Delta_{A4},\delta_h\Psi_4,\delta_h\varphi_4` and ordinary-matter/metric reactions that must be solved at the same k⁴ order.

The restricted sector, therefore, predicts **no delayed-only O(k²) metric response** from auxiliary bath dynamics if the initial matter/metric derivative matches and the branch is regular. Its first potentially observable constrained metric response is structurally **O(k⁴)** (or higher after further cancellations). **This is a formal long-wavelength order statement, not an amplitude bound at finite DES k, and it does not establish that the k⁴ coefficient is nonzero in the fully physical mode.**

## 4. Precisely what is and is not solved

**Now an exact conditional consequence of original reduced action equations**: the full physical growing-state calculation may be *organized*, not guessed, as a pressureful all-species+Einstein k² solution followed by a sourced 2×2 scalar/aether+retarded-bath system and then a jointly conserved k⁴ metric response. This is materially more economical than independently tuning two X₂/S₂ amplitudes, and immediately locates the earliest allowed delayed gravity signal.

**Still missing:** a source-verified *physical* pressureful Exp `Delta_A2` including actual photon/neutrino/baryon backreaction; a proved full unreduced covariant multiplier + Ward equivalent action; a physically selected no-isocurvature X₂/S₂ homogeneous sector (the 2×2 operator has independent solutions if one does not exclude them); the true retarded bath history; and a full k⁴ gravity+species response. At lensing k not asymptotically small, the **full finite-k** solver is still required, and the k²/k⁴ expansion by itself is insufficient.

**Scientific decision: TRIANGULAR_K2_TO_K4_REDUCED_SOURCE_OPERATOR_DERIVED / ORIGINAL_QUARTER_CLASS_BUILD_CONFIRMED / PHYSICAL_PRIMORDIAL_SOURCE_OPEN / PHYSICAL_WEYL_TRANSFER_OPEN / FULL_PHYSICS_GO=FALSE / DES_DETECTION=FALSE.** This note is deliberately a **derivation, not another synthetic PASS-test campaign**.


## 23 November 2026 — correction to the primordial Ward "selection" expectation

The next-step wording above ("enforce Ward at k² to select X₂/S₂") was **too strong**. In the *already verified original reduced* quarter-action dictionary, the scalar Ward residual is an exact combination of the density/phase/electric evolution and definition residuals (LW33); once they are imposed, Ward does **not** give two additional algebraic initial conditions. The original k² X₂/S₂ operator has `tr A₂=-H` and exact nonvanishing fundamental determinant `det U₂(t,t_i)=a_i/a(t)`, so it retains two homogeneous amplitudes at every finite regular time. The reference radiation indicial roots 0 and 1/2 are both bounded as X₂, and boundedness alone does not select a unique primordial mode. Full unreduced covariant boundary/multiplier constraints or an independently declared **no-independent-aether primordial state** must select these amplitudes. A physically past-selected Volterra solution can then be considered, without resetting at CLASS entry. See the [precise two-amplitude obstruction and explicit selection/stop rule](ge19_20261123_primordial_XS_mode_selection_two_amplitude_abel_ward_obstruction.md). The 19→8 pressureful Einstein–matter reduction remains valid **only inside its declared analytic adiabatic branch**; it does not prove the full theory selects that branch. No CLASS run, Weyl/DES detection, or extra physical signal is implied; `FULL_PHYSICS_GO=false`.
