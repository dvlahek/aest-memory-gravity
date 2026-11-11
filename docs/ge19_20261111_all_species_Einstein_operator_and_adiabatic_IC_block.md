# GE19 — one joint all-species Einstein source / AeST initial-mode decision

**11 November 2026. Physics-first source and analytical review, no numerical CLASS runs.**

**Classification:** `CLASS_NEWTONIAN_ALL_SPECIES_METRIC_SOURCE_STRUCTURE_SUPPORTED / AEST_PRESSUREFUL_PRIMORDIAL_IC_CONDITIONALLY_INCONSISTENT / PHYSICAL_ETA_OBSERVER_BLOCK`.

The documented scope is the **actual** pinned CLASS v3.3.4 source `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`, the exact frozen `v019` and `v019j` patch source blobs, and the previously established GE19 restricted linear scalar action and bath normalization. It does **not** certify the complete all-species action-to-CLASS ODE or a gauge-independent retarded Weyl observable. The value of \(w_A\) at the actual start of the researcher's CLASS run is not measured here.

## 1. All-species Einstein sources: what the production CLASS code actually implements

The official CLASS Newtonian-gauge Einstein update in `source/perturbations.c`, original Git blob `c78fe4376d2eeebfbf4ff0cfca13b048d4513fa0`, contains (exact C expressions)
~~~c
ppw->pvecmetric[ppw->index_mt_psi] =
    y[ppw->pv->index_pt_phi] -
    4.5 * (a2/k2) * ppw->rho_plus_p_shear;
ppw->pvecmetric[ppw->index_mt_phi_prime] =
    -a_prime_over_a * ppw->pvecmetric[ppw->index_mt_psi]
    + 1.5 * (a2/k2) * ppw->rho_plus_p_theta;
~~~
The units are those of the pinned CLASS normalized stress variables. All standard species feed the same `ppw->delta_rho`, `ppw->delta_p`, `ppw->rho_plus_p_theta` and `ppw->rho_plus_p_shear`: photons, baryons, relativistic neutrinos, massive noncold neutrinos and relevant other species. The same source has Newtonian Einstein metric-source and radiation-streaming approximation logic.

The original frozen `v019/apply_patch_v019.py` (Git blob `c78484eb916bfee2730759c0bdc813a706bf9a68`) replaces **only the CDM-labeled stress contribution** when AeST is enabled, preserving the other species branches, and directly inserts
~~~c
ppw->delta_rho += rho_dark*y[ppw->pv->index_pt_delta_cdm];
ppw->rho_plus_p_theta += rho_plus_p_dark*y[ppw->pv->index_pt_theta_cdm];
ppw->rho_plus_p_tot += rho_plus_p_dark;
ppw->delta_p += rho_dark*Pi_aest;
~~~
with `rho_plus_p_dark=rho_dark+p_aest` and `Pi_aest` derived from the linear scalar pressure dictionary. There is no *direct* AeST/bath shear at linear order in the restricted GE06+GE05 action. Standard photons/free-streaming neutrinos **do** contribute their nonzero shear.

The resulting combined *source-level* Einstein relations in cosmic time, using \(D_A\equiv\delta\rho_A\), \(T_A\equiv(\rho_A+p_A)\theta_A\) in CLASS's normalized background stress units, and \(\mathcal H=aH\), are
\[
\begin{split}
\frac{k^2}{a^2}\Phi+3H(\dot\Phi+H\Psi)
+\frac32\Bigl[D_A+\sum_s\delta\rho_s\Bigr]&=0,\\
\Phi'+\mathcal H\Psi
-\frac{3a^2}{2k^2}\Bigl[T_A+\sum_s(\rho_s+p_s)\theta_s\Bigr]&=0,\\
\Phi-\Psi-\frac{9a^2}{2k^2}\sum_s(\rho_s+p_s)\sigma_s&=0.
\end{split}
\]
The last two are directly traceable to the C snippets (in this CLASS normalization). The first is the **expected** combined lapse constraint from the additive action stress tensors, not an independently integrated Hamiltonian residual of the candidate. The spatial pressure trace additionally includes \(\delta p_A+\sum_s\delta p_s\). The direct bath stress vanishes to first order about the zero-bath FLRW background. All sums are over **separate** standard species; the AeST CDM-labelled slot is NOT counted as an additional physical CDM fluid.

**Decision for this part:** the Newtonian **total stress assembly** is structurally compatible with the additive Einstein–AeST + minimally coupled ordinary matter action *conditional on correct AeST state and correct initial conditions*. This is **not** a full propagated constraint proof or an audit of every CLASS approximation branch.

## 2. Concrete missing adiabatic initial condition in the actual patched CLASS

This is the new discriminating **source-level** finding, independent of the value \(\gamma=1/4\). In the original official `source/perturbations.c` `perturbations_initial_conditions()`, the *unmodified* CDM-labelled state is initialized **in synchronous gauge** as
~~~c
ppw->pv->y[ppw->pv->index_pt_delta_cdm] =
    3./4.*ppw->pv->y[ppw->pv->index_pt_delta_g];
/* cdm velocity vanishes in the synchronous gauge */
~~~
and later transformed to Newtonian gauge using
~~~c
ppw->pv->y[ppw->pv->index_pt_delta_g] -= 4.*a_prime_over_a*alpha;
ppw->pv->y[ppw->pv->index_pt_delta_cdm] -= 3.*a_prime_over_a*alpha;
ppw->pv->y[ppw->pv->index_pt_theta_cdm] = k*k*alpha;
~~~
The standalone frozen `v019/apply_patch_v019.py` changes the CDM **evolution**, stress, background interpretation and adds \(\alpha_A,E_A\) IC, but it does **not** replace either inherited CDM initial density formula or this dust gauge-transform line (literal strings absent from both v019 and v019j memory patch sources). `v019j` sets \(q_j=p_j=0\), also leaving these density/gauge terms unchanged. The separately versioned quarter candidate changes the memory coefficient only, so it inherits the same initial-state issue.

For the actual AeST effective dark fluid \(\rho_A,p_A\), define \(w_A=p_A/\rho_A\), with background evolution \(\rho_A'=-3\mathcal H(\rho_A+p_A)\), while free-streaming photons satisfy \(\rho_\gamma'=-4\mathcal H\rho_\gamma\). A truly **adiabatic** perturbation corresponds at leading order to a common local time displacement, hence
\[
\boxed{
\frac{\delta_A}{1+w_A}=\frac34\delta_\gamma
\quad\Longleftrightarrow\quad
\delta_A=\frac34(1+w_A)\delta_\gamma .
}\tag{AD}
\]
This condition is gauge-independent in the sense that the *relative entropy* \(S_{A\gamma}\equiv\delta_A/(1+w_A)-3\delta_\gamma/4\) is invariant under a linear temporal gauge transformation for each separately conserved background stress. It is **not** the correct full primordial growing-mode eigenvector by itself; velocities, metric constraints, pressure gradients and auxiliary states must also be satisfied.

The **correct** gauge transformation of AeST density is
\[
\delta_A^{N}=\delta_A^{S}-3(1+w_A)\mathcal H\alpha,
\quad
\delta_\gamma^{N}=\delta_\gamma^{S}-4\mathcal H\alpha.
\tag{G}
\]
But the unchanged CDM code uses coefficient \(3\), not \(3(1+w_A)\), and begins with \(\delta_A^S=(3/4)\delta_\gamma^S\).

Writing \(d\equiv\delta_\gamma^S\), \(x\equiv\mathcal H\alpha\), the code therefore initializes
\[
\delta_A^{N,\mathrm{code}}=\frac34d-3x,\qquad
\delta_\gamma^N=d-4x.
\]
The **exact leading-order relative entropy** of that code-initialized fluid, if interpreted with the stated AeST background, is
\[
\boxed{
S_{A\gamma}^{N,\mathrm{code}}
=\frac{\delta_A^{N,\mathrm{code}}}{1+w_A}
-\frac34\delta_\gamma^N
=\frac{3w_A}{4(1+w_A)}(4x-d).
}\tag{IC}
\]
This is a direct algebraic identity (independently factorized with SymPy). For generic \(w_A\ne0\) and mode amplitudes it is nonzero. The expression disappears for **exact dust** \(w_A=0\), zero perturbations, or particular accidental choices of \(x,d\), but such cancellations have **not** been demonstrated for the actual fixed Exp benchmark. The actual \(w_A(t_i)\) has **not** been measured in this review; do not assert a numerical contamination or observed DES bias.

**Crucial:** correcting only the initial \(\delta_A\) *or* only the Newtonian gauge factor leaves the other wrong. And neither point alone completes a true joint adiabatic eigenmode or a causal NL0B initialization. A direct modification of the frozen code or after-the-fact normalization to make previous results look better is **not** authorized.

## 3. Bath initial state: a selected retarded sector, not generic regularity

For each original positive NL0B mode, the previously established original action gives
\[
\ddot q_j+3H\dot q_j+\omega_j^2q_j
=\omega_j\sqrt{w_j}\,k\chi/a.
\]
The source uses `q_j=p_j=0` at its first integration time and \(\chi_i=0\) at leading order. As rigorously shown in [the earlier independent bath initial-state decision](ge19_20261111_auxiliary_initial_state_and_physical_observer_decision.md), even an unforced radiation-era homogeneous solution may be regular and nonzero \(\propto t^{-1/4}J_{1/4}(\omega_jt)\). Thus regularity alone does not force zero auxiliary amplitudes; the **no-free-bath-mode retarded branch** is an additional physically selectable initial-condition sector.

Under **pure primordial adiabatic perturbations** of a strictly zero background auxiliary vector \(U_{j\mu}^{(0)}=0\), the infinitesimal time-shift-derived \(\delta U_{j\mu}\) is zero at leading order. This is **consistent with choosing** no independent free-bath/isocurvature mode and hence leading \(q_j=p_j=0\). It does **not** derive the actual combined Einstein–AeST–NL0B regular growing eigenmode, and does not make all regular nonadiabatic C modes disappear. The finite initial time and subleading forced response must still be controlled.

## 3A. Independent covariant necessary adiabatic field relations — what can already be closed

For the homogeneous unit timelike aether \(A_\mu^{(0)}=(-1,0,0,0)\), scalar \(\dot{\bar\phi}=Q\), and zero auxiliary background \(U_{j\mu}^{(0)}=0\), consider an infinitesimal time diffeomorphism generated by \(\xi^\mu=(T(t,\mathbf x),0,0,0)\). Applying the **same** Lie derivative to every original field (before choosing the Newtonian gauge) gives the purely adiabatic coordinate-shift contribution:
\[
\delta_\xi \phi=QT,\qquad
\delta_\xi A_i=-\partial_iT,\qquad
\delta_\xi g_{00}=-2\dot T,\qquad
\delta_\xi U_{j\mu}=0.
\]
In the *GE06* longitudinal coframe \(A_i^{(1)}=\partial_i\alpha_A\), hence
\[
\boxed{
\varphi=QT,\quad \alpha_A=-T,\quad\Psi=\dot T,\quad
\chi=\varphi+Q\alpha_A=0,\quad
E_A=\dot\alpha_A+\Psi=0,\quad q_j=p_j=0
}\tag{G0}
\]
for the **pure-gauge adiabatic variation**. All these identities follow from the common geometry: the scalar and aether have the *correlated perturbations* fixed by the background, rather than independently specified arbitrary first-order amplitudes. (A compensating spatial gauge transformation may be needed to express the same perturbation in strict Newtonian gauge; the gauge-invariant combinations \(\chi\) and \(E_A\) remain zero for the unexcited state.)

Similarly, \(\delta_\xi\rho_i=\dot{\bar\rho}_iT\) for each separately conserved background constituent, so \(\delta_A/(1+w_A)=3\delta_\gamma/4=-3HT\). This independently recovers the exact necessary adiabatic relation (AD) and explains why **zero free bath modes are compatible with** a purely adiabatic sector even though standalone bath regularity does not force the choice.

**Do not overinterpret:** Eq. (G0) constructs a *gauge-generated adiabatic perturbation* and its necessary \(k\to0\) consistency relations, **not** the nontrivial finite-\(k\) primordial growing solution with curvature, anisotropic neutrino stress and subleading \(k\tau\)-corrections. Those physical corrections, the source constraints, and stability of the numerical initial-value state remain the final joint acceptance task. It is precisely because the source uses \(\delta_A^S=3\delta_\gamma^S/4\) and the pressureless gauge transform at generic \(w_A\ne0\) that its initialization fails to coincide exactly with this covariantly generated adiabatic sector.

## 4. Joint result — a concrete conditional PHYSICS BLOCK, not another LW stage

| Physical component | New outcome | Confidence/scope |
|---|---|---|
| Total Newtonian Einstein source assembly, including photons, baryons, massive/relativistic neutrinos, AeST effective fluid | **Supported as additive source structure** | Exact pinned C statements; *not* independent full all-branches action equivalence |
| Direct linear bath stress in total metric sources | **Zero** on relaxed FLRW in fixed reduced action | GE05/GE06 linear perturbation order |
| Separate historical CDM slot vs AeST state | **Explicit repurposing**, no second CDM fluid in same state | Frozen v019 C patch |
| **AeST initial density and Newtonian gauge transform** | **Conditionally inconsistent** with exact adiabatic AeST when \(w_A\ne0\) | Exact original CLASS C source + gauge-kinematics identity (IC); size at actual \(t_i\) unknown |
| Regular bath \(\chi_i=0\) | **Does not uniquely determine q/p** | Explicit regular homogeneous oscillator counterexample |
| Pure no-free-bath-mode hypothesis | **One clearly defined physical sector** | Additional model assumption, not automatically all primordial solutions |
| Full physical growing mode, Einstein constraint propagation, numerical error-controlled source-to-Weyl | **UNRESOLVED** | P0 acceptance remains open |
| DES galaxy–Weyl physical transfer and lensing detection | **BLOCK** | Native transfer diagnostics insufficient |

**Concrete decision for P0:** The complete production `PHYSICS_GO` cannot be granted on the current evidence even for the otherwise action-normalized quarter candidate. **It is not enough to compare local E equations**: the inherited dust initialization of the AeST state must be replaced or mathematically shown to be an acceptably accurate limit of the *complete coupled primordial adiabatic Einstein–AeST–NL0B eigenmode*. This is a real action-to-implementation acceptance item, not a request to collect more arbitrary symbolic PASS results.

**Most efficient next physics step (one bounded calculation, not a sweep):** derive the leading joint superhorizon Newtonian-gauge growing-mode/adiabatic consistency conditions for \(\{\delta_A,\theta_A,\alpha_A,E_A,q_j,p_j,\Phi,\Psi,\delta_\gamma,\theta_\gamma,\delta_b,\theta_b,\nu\text{ species}\}\), including action density/phase definitions, all species background enthalpies and Einstein lapse/momentum/shear. Require (AD), (G), \(\chi_i=0\), and no homogeneous bath mode as explicit hypotheses; either obtain a consistent state vector, or label `PHYSICS_BLOCK`. No CLASS runs or DES tuning before this condition is resolved; the original old C and historical finite-eta data are preserved.

### Exact frozen references

- [Pinned CLASS v3.3.4 scalar metric and primordial IC code](https://github.com/lesgourg/class_public/blob/e85808324f51fc694d12e3ed7439552a3c3f9540/source/perturbations.c) (Git blob `c78fe4376d2eeebfbf4ff0cfca13b048d4513fa0`).
- [Original AeST fluid patch](../v019/apply_patch_v019.py) (Git blob `c78484eb916bfee2730759c0bdc813a706bf9a68`).
- [Original historical memory patch](../v019j/apply_memory_patch.py) (Git blob `14796a5ed9e6265ed6810c792a93d7328a109364`).
- [Reduced action and 15/15 researcher source matrix](ge19_20261111_joint_action_to_CLASS_scalar_source_matrix.md).
- [Known physical-matter observer and bath IC limit](ge19_20261111_auxiliary_initial_state_and_physical_observer_decision.md).
- [Original P0 issue](https://github.com/dvlahek/aest-memory-gravity/issues/2).

**Final scientific label:** `MULTISPECIES_METRIC_SOURCE_STRUCTURE_PASS / AEST_ADIABATIC_IC_CONDITIONAL_DEFECT / FULL_PHYSICS_GO_BLOCK`.
