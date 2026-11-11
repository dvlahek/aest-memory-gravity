# GE19 — one joint action-to-CLASS scalar source matrix, with exact physical source coefficient

**11 November 2026 | single integrated physics continuation, not LW34.**
**Decision:** `REDUCED_LINEAR_SCALAR_ACTION_TO_CLASS_SOURCE_MATRIX_ALGEBRA_PASS / COMPLETE_3PLUS1_PRODUCTION_CERTIFICATION_OPEN / DES_BLOCK`.

This note is the **actual joint source/equation comparison**, not a proposed future series of audits. It is constructed from the original frozen GE06 (Einstein+AeST), GE05 (NL0B positive longitudinal bath), v019 (CLASS effective-fluid) and v019j (CLASS bath) source definitions. The supplemental single [reproducible SymPy source matrix](../ge19/physics_gate/action_to_class_scalar_matrix_20261111.py) was independently run **in standalone algebra mode** in the analysis container with **15/15 exact identities PASS**, with no numerical cosmological execution; the **subsequent original GitHub source-locked WSL execution passed 15/15 symbolic checks and 5/5 original source locks**, with byte-identical outputs archived as [matrix JSON](../results/ge19_action_to_class_scalar_matrix_20261111.json) (Git blob `5375bac561091fb3d98d4f978e2664e067f9906a`) and [WSL log](../results/ge19_action_to_class_scalar_matrix_20261111.log) (Git blob `81bbc96fcf09a17e52d3267e230f442fa86da73b`). Together with previously researcher-verified LW33, this supports a definite conditional statement, **not** full all-species CLASS equivalence or an observed memory discovery.

## 1. One common field and time basis

Use proper time \(t\), conformal time \(\tau\) with \(d\tau=dt/a\), \(H=\dot a/a\), \(\mathcal H=aH\), and one scalar Fourier \(k>0\), evaluated in Newtonian gauge **after independent metric lapse/shift/spatial variations**. Original AeST background shift symmetry and effective pressure:
\[
\dot K_Q=-3HK_Q,\quad
\dot Q=-3H\frac{K_Q}{K_{QQ}},\quad
c_a^2=\frac{K_Q}{QK_{QQ}},\quad
\rho_A=\frac{QK_Q-K}{3},\quad p_A=\frac{K}{3},\quad
R_A=\rho_A+p_A=\frac{QK_Q}{3}.
\]
These relations do **not require an AeST-only Friedmann equation**: \(H(t)\) may reflect the full background matter content, provided ordinary species are minimally coupled and the AeST scalar retains its original shift symmetry.

The common longitudinal scalar variables are
\[
\delta Q=\dot\varphi-Q\Psi,\quad E_A=\dot\alpha+\Psi,\quad
\chi=\varphi+Q\alpha,\quad
\theta_A=\frac{k^2\varphi}{aQ}
\quad\Longleftrightarrow\quad
\chi=Q\left(\frac{a\theta_A}{k^2}+\alpha_A\right).
\]

## 2. Exact effective-fluid state / action-pressure match

Original action (GE06/earlier LW24) gives
\[
D_A^{\rm action}
=\frac13\left[QK_{QQ}\delta Q-
\frac{k^2}{a^2}(K_BE_A+C\chi)\right],
\quad P_A^{\rm action}=\frac13K_Q\delta Q,\quad C=2-K_B.
\]
The **actual v019 CLASS pressure source** is
\[
\Pi_A=c_a^2\delta_A+
\frac{c_a^2k^2}{3a^2\rho_A}(K_BE_A+C\chi),
\qquad D_A=\rho_A\delta_A.
\]
When \(D_A=D_A^{\rm action}\), direct cancellation of the gradient terms gives the exact, **nontrivial pressure consistency equation**
\[
\boxed{\rho_A\Pi_A=c_a^2\left[D_A^{\rm action}+
\frac{k^2}{3a^2}(K_BE_A+C\chi)\right]
=\frac13K_Q\delta Q=P_A^{\rm action}.}\tag{P}
\]
Its truth is independent of any CLASS source-forcing amplitude and of the origin of \(H(t)\). It does **not** prove by itself that the dynamical state identity \(D_A=D_A^{\rm action}\) is maintained through a full evolution.

The original effective fluid momentum exactly matches the action phase:
\[
T_A=(\rho_A+p_A)\theta_A
=\frac{K_Qk^2\varphi}{3a}.
\]

## 3. The original CLASS theta/alpha rows reconstruct the scalar kinematics — independently of the E forcing

The original implemented Newtonian-gauge velocity equation is
\[
\theta_A'=(3c_a^2-1)\mathcal H\theta_A+
k^2\frac{\Pi_A}{1+w_A}+k^2\Psi,\quad
1+w_A=\frac{\rho_A+p_A}{\rho_A}.
\]
Because \(\varphi=(aQ/k^2)\theta_A\), \(\dot Q/Q=-3Hc_a^2\), and prime \(=a\,d/dt\), differentiation **before imposing E dynamics** yields exactly
\[
\boxed{\dot\varphi-Q\Psi
=Q\frac{\Pi_A}{1+w_A}
=\frac{3\rho_A\Pi_A}{K_Q}.}\tag{V}
\]
Together with \(\alpha_A'=a(E_A-\Psi)\), and \(\chi=\varphi+Q\alpha_A\),
\[
\boxed{\dot\chi
=Q\left[E_A+\frac{\Pi_A}{1+w_A}
-3Hc_a^2\alpha_A\right].}\tag{C}
\]
Thus the original velocity, alpha and pressure rows encode the **same covariant scalar-phase kinematics**, *conditional on the action density map*, without any independent \(\eta\) forcing in \(\theta_A'\). These exact symbolic identities were checked afresh in the 15-gate standalone matrix.

## 4. NL0B auxiliary Euler rows and the normalized action source

Per one positive bath node \((\omega_j,w_j)\), original GE05 longitudinal quadratic action on FLRW is
\[
L^{(2)}_{\rm bath,j}
=\frac{\eta a^3}{4}\left[
\dot q_j^{\,2}-
\left(\omega_jq_j-\sqrt{w_j}\,\frac{k\chi}{a}\right)^2\right],
\quad
B_{\chi,j}=w_j\chi-\frac{a\omega_j\sqrt{w_j}}{k}q_j,\quad
B_\chi=\sum_j B_{\chi,j}.
\]
Independent variation of \(q_j\), with \(\eta>0\), yields
\[
\ddot q_j+3H\dot q_j+\omega_j^2q_j
=\omega_j\sqrt{w_j}\,\frac{k\chi}{a}.
\]
In conformal CLASS time, for \(p_j=q_j'\),
\[
\boxed{q_j'=p_j,\qquad
p_j'=-2\mathcal H p_j-a^2\omega_j^2q_j
+a k\omega_j\sqrt{w_j}\,\chi.}\tag{B}
\]
This **exactly matches** original v019j literal q/p array equations for the normalized longitudinal bath.

The *raw* bath derivative with respect to \(\chi\) is
\[
\partial_\chi L^{(2)}_{\rm bath}
=-\frac{\eta ak^2}{2}B_\chi,\qquad
\partial_\alpha L^{(2)}_{\rm bath}
=Q\partial_\chi L^{(2)}_{\rm bath}
=-\frac{\eta ak^2Q}{2}B_\chi.
\]
The AeST scalar-electric quadratic term has \(\partial^2L^{(2)}_{\rm AeST}/\partial\dot\alpha^2=2aK_Bk^2\). Therefore the **normalized** aether source in proper time and then conformal time is
\[
\boxed{\Delta\dot E_A=-\frac{\eta Q}{4K_B}B_\chi,\qquad
\Delta E_A'=-\frac{a\eta Q}{4K_B}B_\chi.}\tag{E}
\]
In C, the \(\eta\) factor has already been incorporated into `Bchi_aest`; the following E evolution row divides the entire RHS by \(K_B\). Thus the **separate exploratory quarter branch** implements Eq. (E) *in that row*. The frozen historical `v019j` has coefficient **one-half**, not one-quarter, and does not insert a companion \(\eta\) source into the density/velocity rows.

The literal bath action contains an overall \(\eta\) in the normalized \(q_j\) representation. At \(\eta=0\) its Euler equation degenerates; a physical \(\eta\to0^+\) tangent needs a **selected continuous retarded auxiliary branch**, rather than inferring uniqueness from the zero-coupling algebra. Zero-auxiliary initial data in the historical code is a chosen regular branch that has **not** by itself been certified as a unique covariant cosmological initial-state condition.

## 5. Complete reduced scalar-charge compatibility and a *specific density-dictionary drift equation*

The exact researcher-tested LW33 identity, retaining independent residuals, is
\[
\boxed{\begin{aligned}
\mathscr S_\phi={}&\frac{6a^3}{Q}R_D
+\frac{2ak^2K_B}{Q}R_E
+\frac{2ak^2C}{Q}R_\chi
+\frac{2ak^2K_Q}{Q}R_{\rm geo}\\
&-\frac{6a^3}{Q}\dot R_\rho
-\frac{18a^3H}{Q}R_\rho
+\frac{a\eta k^2B_\chi}{2}(1-4\gamma),
\end{aligned}}\tag{S}
\]
where \(R_\rho=D_A-D_A^{\rm action}\), \(R_D\) is the fluid density evolution residual, \(R_E\) is the aether evolution residual, \(R_\chi\) and \(R_{\rm geo}\) are kinematic/dictionary residuals, and \(\gamma\) is the explicit bath coefficient in the undivided E RHS.

If those four non-density residuals vanish, **and** the original action scalar Euler equation \(\mathscr S_\phi=0\) holds, Eq. (S) implies a stronger, directly interpretable density-dictionary compatibility condition:
\[
\boxed{\dot R_\rho+3HR_\rho=
\frac{\eta Qk^2B_\chi}{12a^2}(1-4\gamma).}\tag{D}
\]
For \(\gamma=1/4\), \(a^3R_\rho\) is constant; matched \(R_\rho(t_i)=0\) is preserved. For \(\gamma=1/2\), the same action/CLASS dictionaries would require a *nonzero* forcing \(-\eta Qk^2B_\chi/(12a^2)\) for \(R_\rho\). A historical half source with unchanged fluid dynamics is incompatible with imposing all the original action Euler and dictionary equations simultaneously for generic \(B_\chi\ne0\).

**Critical logical limit:** Eq. (D) is a mathematical consequence **assuming** the independent original scalar Euler equation is satisfied. The current CLASS equations do not independently integrate \(\varphi\) as a separate scalar state, so a pass of their internally constructed fluid conservation or Einstein constraint propagation does **not** establish \(\mathscr S_\phi=0\). Direct state reconstruction/field-equation matching, including gauge and species, remains an acceptance obligation.

## 6. Standard species: what can be concluded from minimal coupling

For a fixed original minimally coupled action \(S_{\rm tot}=S_{\rm GR+AeST+NL0B}[g,A,\phi,U]+\sum_s S_s[g,\psi_s]\), variation gives \(\delta S_s/\delta A=\delta S_s/\delta\phi=\delta S_s/\delta U=0\) **at fixed metric and independent matter variables**. Therefore standard baryons, photons, neutrinos and ordinary CDM, *if included as separate minimally coupled sectors rather than conflated with the AeST effective dark fluid*, introduce **no new direct** \(\eta\) or bath companion into (B)/(E)/(S). They **do** modify \(H(t)\) and the total Einstein density/pressure/momentum/shear, and indirectly change \(E_A,\chi,q_j\) through \(\Phi,\Psi\) and Boltzmann evolution. A self-consistent action-to-CLASS mapping must keep that feedback.

The original `v019` implementation uses CDM-labeled array indices to carry the **AeST effective dark component** when `aest_enabled`, with a changed pressure/enthalpy. This is a state-bookkeeping substitution, **not** a demonstration that any independent physical CDM fluid is being evolved simultaneously. A correct full-species source matrix must distinguish that effective component from the remaining actual standard CLASS species. Merely adding \(T_A\) to an unmodified CDM momentum term would double count it.

Minimal coupling guarantees additivity at the **action-source** level, not exact equivalence across every CLASS approximation switch or gauge branch. Existing restricted LW30/31 and 11 November spatial-trace results supply AeST-only metric equations; the properly sourced **all-species spatial trace/shear, baryon-photon/neutrino Boltzmann feedback, normal/gauge equations and initial conditions** still require one direct joint verification on the implementation actually used.

## 6A. Specific non-symbolic implementation obstructions in the ORIGINAL C patch

A direct fresh reading of the original source-locked \`v019/apply_patch_v019.py\` and \`v019j/apply_memory_patch.py\` isolates two **implementation/interpretation obligations** that the 15 symbolic checks, the \(\eta=0\) equality and the fixed finite-\(\eta\) native \(d_m,W\) diagnostic cannot resolve.

**(i) AeST is substituted for the CDM-labeled *code state*, not a separately tracked physical CDM.** In \`v019\` the background explicitly uses:
~~~c
pvecback[pba->index_bg_rho_cdm] = rho_aest;
rho_m += rho_aest-3.*p_aest;
~~~
while the perturbation stress/matter-observer code says:
~~~c
ppw->delta_rho += rho_dark*y[ppw->pv->index_pt_delta_cdm];
delta_rho_m += rho_dark*y[ppw->pv->index_pt_delta_cdm];
rho_m += rho_dark;
rho_plus_p_m += rho_plus_p_dark;
~~~
These are exact source excerpts. They are not *by themselves* proof that CLASS is inconsistent: code may use distinct background and perturbation conventions for different observable definitions. **But they do mean the native transfer field labelled \`d_m\` cannot be casually identified with a separately evolved pressureless CDM density, or interpreted as the physical matter component in a survey cross-power without auditing the \`rho_m\`, \`delta_rho_m\`, \`rho_plus_p_m\` transfer normalization through the actual CLASS output functions.** This is a concrete, narrowly identifiable unverified observer convention, independently of the quarter-factor question. The model's physical effective dark fluid should not be double-counted as both AeST and ordinary CDM.

**Independent check against the actual pinned official CLASS v077 output pipeline:** Original official CLASS \`lesgourg/class_public\`, commit \`e85808324f51fc694d12e3ed7439552a3c3f9540\`, \`source/perturbations.c\` original Git blob \`c78fe4376d2eeebfbf4ff0cfca13b048d4513fa0\`, computes
~~~c
ppw->delta_m = delta_rho_m/rho_m;
ppw->theta_m = rho_plus_p_theta_m/rho_plus_p_m;
~~~
and, when its input flag \`matter_source_in_current_gauge\` is false, explicitly applies
~~~c
ppw->delta_m += 3. *a*H * ppw->theta_m/k2;
~~~
The pinned official source comment says **this gauge-invariant transformation is only valid if all matter components are pressureless and stable**. In \`source/input.c\` (original Git blob \`99ca121ad1d5be93fd0b87316849e85a6fa732c3\`), its default is \`ppt->has_matter_source_in_current_gauge = _FALSE_\`. The frozen original \`v019/ini/aest_exp.ini\` (Git blob \`f9a2bde8921a148e063f9657a8ede0a51c6a629d\`) sets \`gauge = newtonian\` but **does not override that output flag**. The one fixed-\(\eta\) source runner uses that original benchmark and also does not override this flag.

Therefore, with a pressureful AeST effective dark component included in the same CDM-labelled \`rho_m\` sum, the **native exported \`d_m\` at the selected \(\eta,z\) is using a pressureless-matter gauge conversion outside its stated derivation's assumptions**. Under the usual covariant comoving-gauge density definition for a separately conserved total matter-like effective fluid, the expected linear correction is
\[
D_m^{\rm com}=\frac{\delta\rho_m}{\rho_m}
+\frac{3aH}{k^2}\frac{\sum_i(\rho_i+p_i)\theta_i}{\rho_m}
=\delta_m+\frac{3aH}{k^2}\frac{\rho_m+p_m}{\rho_m}\theta_m,
\]
whereas the pinned CLASS code uses \(\delta_m+3aH\theta_m/k^2\). In a single effective AeST+pressureless-baryon mixture with the same stress bookkeeping, the candidate discrepancy would be
\[
\boxed{D_m^{\rm CLASS}-D_m^{\rm com}
=-\frac{3aH}{k^2}\frac{p_A}{\rho_m}\theta_m.}
\]
**Conditions and scope:** this formula assumes a coherent definition of the same effective total matter stress and no independent mass-exchange terms, with Newtonian \(\theta_i\) conventions matching CLASS. The actual \`rho_m\` background bookkeeping (\`rho_aest-3p_aest\` in its matter/radiation split) and possible additional species must first be reconciled before this expression can be used as a corrected survey observable. This is a **demonstrated invalid assumption of the default output conversion for generic \(p_A\ne0\)**, *not* a measured numerical error or proof of faulty Einstein/aether evolution. It could vanish in the exact dust limit; neither its size nor DES significance has been computed.

**Actionable fixed-observer remedy for a later bounded experiment:** request \`matter_source_in_current_gauge = yes\` in Newtonian gauge and **explicitly** define any gauge-invariant physical galaxy/matter observable from total action stress, pressure and momentum, rather than applying the pressureless \`d_m\` correction. Do not retroactively reinterpret the earlier 147 native k values as physical \(\partial_\eta P_{d_mW}\), and do not modify old frozen run inputs.

**(ii) Retarded auxiliary initial state is selected in C but has not been independently derived as unique.** In \`v019j\`, per-node normalized q/p states are allocated **only in Newtonian gauge**, zeroed at leading initial conditions, and copied on the captured approximation vector-rebuild branch:
~~~c
ppw->pv->y[ppw->pv->index_pt_mem_q_aest+jm] = 0.;
ppw->pv->y[ppw->pv->index_pt_mem_p_aest+jm] = 0.;
~~~
The source comments invoke \(\chi_i=0\) for leading adiabatic data. Such a zero state is a *specific chosen regular/retarded initialization* in the implemented oscillator, but the homogeneous second-order equation also has independent initial data; **\(\chi_i=0\) alone does not prove that \(q_i=p_i=0\) is the uniquely physically admissible initial state.** Need an asymptotic regularity/causal-prehistory argument and a check of *every relevant* source-vector switch/IC path in the actual patched CLASS C. This is a physics/implementation initial-value task, not another arbitrary numerical eta sweep.

**(iii) All four original Einstein metric scalar rows from GE06 (H/M/shear/trace) are *restricted-model action results*, not a source-level comparison to each actual CLASS Einstein row after all standard species.** Existing CLASS neutrinos/photons/baryons provide metric stress and free-streaming anisotropic shear. Minimal coupling shows absence of **direct** bath terms in their individual Euler variations, but cannot prove that the v019/v019j C implementation preserves the correct total action-derived constraints for all used approximation branches.

**Concrete P0 acceptance:** In *one* source-to-operator comparison, reconstruct the true transfer-density meaning and physical retarded q/p initial state, alongside full species+metric+E/scalar rows. If any remains unmatched, classify \`PHYSICS_BLOCK\`, even if the source coefficient is locally 1/4 and \`d_m,W\` arrays exist. No DES fit and no new LW stages are appropriate as substitutes.

## 7. Physics acceptance verdict — single candidate, no new LW campaign

| Equation / source | Joint comparison | Accepted scope |
|---|---|---|
| AeST \(D_A,\theta_A,\Pi_A\) stress dictionary | Eqs. (P)/(V) exact algebra | **Reduced linear scalar PASS**, assuming \(D_A=D_A^{\rm action}\) |
| \(\alpha_A,\chi,\delta Q\) state kinematics | Eq. (C) exact algebra | **Reduced linear scalar PASS** |
| Positive NL0B retarded oscillator q/p differential rows | Eq. (B) exactly matches original C | **Linear scalar longitudinal equation PASS**, initial physical branch still open |
| Original bath scalar/aether Euler source | Eq. (E) from action Hessian; LW33 Eq. (S) | **Quarter necessary** under original dictionary |
| Einstein lapse/shift/shear/trace | LW30/31 and 11 November new trace | **Reduced AeST-only action PASS**; full species source projection open |
| Full all-species C source/constraint/approximation-switch equivalence | Minimal coupling gives structure, not complete C evolution equivalence | **OPEN** |
| Physical causal, solver-accurate \(\partial_\eta P_{\delta_m W}(k,z)\) | Single positive-eta code transfer small, oscillatory in \(k\), errors unqualified | **BLOCK** |
| DES Y3 \(\gamma_t\) forecast and observed likelihood | Only real lens/source geometry frozen | **BLOCK**, no detection |

**One precise remaining deliverable:** jointly check the actual Newtonian-gauge CLASS all-species Einstein source rows and auxiliary initial/approximation state-switch equations against the **entire original constrained action-derived quadratic scalar system**, including its spatial trace and residual (S), rather than repeating symbolic individual-row PASS or tuning \(1/4\). If not independently established, label `PHYSICS_BLOCK`. If proved, only the isolated quarter candidate advances to **one** predeclared solver-error and retarded-history control, then a nuisance-marginal DES Y3 Asimov forecast. No observed DES residuals are permitted to set source coefficients.

**No new CLASS run, finite-eta sweep, H4/Z21 solve, GitHub Actions or astronomical detection in this result.**

### Source provenance and reproducibility

- [Single executable 15-identity matrix](../ge19/physics_gate/action_to_class_scalar_matrix_20261111.py), exact checks performed in a local isolated analysis runtime in **no-source-lock** mode (and subsequently reproduced in the original WSL with all five source locks). For WSL with the original frozen repo checkout and active `sympy`, invoke:
  ```bash
  cd ~/aest-memory-gravity
  git pull --ff-only
  source .venv/bin/activate
  python3 ge19/physics_gate/action_to_class_scalar_matrix_20261111.py \
    --out results/ge19_action_to_class_scalar_matrix_20261111.json
  ```
  Expect `GE19_ORIGINAL_SOURCE_LOCKS_PASS 5` and `GE19_SCALAR_MATRIX_SYMBOLIC_PASS 15`; the JSON explicitly retains `production_physics_go=false`. **Do not repeat CLASS numerics.**
- [LW33 complete reduced off-shell identity](ge19_lw33_exact_scalar_action_to_CLASS_offshell_source_decision_2026-11-10.md), with original actual researcher WSL PASS.
- [LW30/31 metric rows](ge19_lw30_original_gr_aest_adm_scalar_constraints_class_bridge_2026-11-10.md), [spatial trace](ge19_20261111_original_action_spatial_trace_linear_scalar_closure.md).
- [Existing physics Noether/source acceptance](ge19_20261111_physics_first_noether_scalar_source_closure_decision.md), [P0 Issue #2](https://github.com/dvlahek/aest-memory-gravity/issues/2).
