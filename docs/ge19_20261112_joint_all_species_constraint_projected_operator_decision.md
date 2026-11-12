# GE19 — all-species Einstein constraint projection and the physical meaning of the frozen root

**12 November 2026.**  
**Decision:** `ALL_SPECIES_CONSERVED_STRESS_CONSTRAINT_PROPAGATION_PASS / AEST_ONLY_PROJECTED_FROZEN_ROOT_CONDITIONAL / FULL_PHYSICS_GO_BLOCK / DES_NOT_DETECTED`.

This is a *joint* analytic calculation, not another CLASS numerical sweep or DES fit. It uses the original AeST effective stress/phase dictionary, original reduced GR constraints, quarter normalized bath source, and all standard species as summed, conserved stress sources. It does **not** independently solve the photon–baryon collision hierarchy, neutrino hierarchy, production CLASS approximation switches, or all-field unreduced covariant action.

## 1. The constraint-projected, multi-species source equations

Let \(D_s=\delta\rho_s\), \(T_s=(\rho_s+p_s)\theta_s\), \(S_\sigma=\sum_s(\rho_s+p_s)\sigma_s\), \(S_D=\sum_s D_s\), \(S_T=\sum_sT_s\), and
\[
\Omega_s=S_D+\frac{3aH}{k^2}S_T=\sum_s(\rho_s+p_s)\Delta_s.
\]
These sums include photons, baryons, massless and massive neutrinos, and additional separate standard species. The *combined* standard stress obeys conservation, including cancellations of internal Thomson collision momentum exchanges; each colliding species need not be separately conserved.

Write \(R_A=QK_Q/3\), \(C=2-K_B\), \(c_a^2=K_Q/(QK_{QQ})\), \(g=c_a^2k^2/(a^2K_Q)\). From the **original** Newtonian Einstein Hamiltonian, momentum and shear conditions and AeST stress dictionary:
\[
\boxed{\begin{aligned}
\Psi&=\Phi-\frac{9a^2}{2k^2}S_\sigma,\\
\dot\Phi&=\frac{K_Q}{2}\varphi+\frac{3a}{2k^2}S_T-H\Psi,\\
D_A&=-\frac{2k^2}{3a^2}\Phi-HK_Q\varphi-\frac{3aH}{k^2}S_T-S_D.
\end{aligned}}\tag{1}
\]
In particular,
\[
\boxed{R_A\Delta_A+\Omega_s=-\frac{2k^2}{3a^2}\Phi.}\tag{2}
\]
Therefore the physical \(\Delta_A\) is *not* an independently adjustable source in the full Einstein system.

Imposing the actual original-action AeST density dictionary and \(\chi=\varphi+Q\alpha,\ E_A=\dot\alpha+\Psi\) yields the **constraint-projected scalar evolution**
\[
\boxed{\begin{aligned}
\dot\varphi &=Q\Psi-3Hc_a^2\varphi
+g(K_BE_A+C\chi-2\Phi)-\frac{3c_a^2}{K_Q}\Omega_s,\\
\dot\chi &=QE_A-3Hc_a^2\chi
+g(K_BE_A+C\chi-2\Phi)-\frac{3c_a^2}{K_Q}\Omega_s.
\end{aligned}}\tag{3}
\]
These satisfy \(\dot\alpha=E_A-\Psi\). They close with the unchanged, separately justified **quarter** reduced action source
\[
K_B(\dot E_A+HE_A)=K_Q\chi-C[\dot\chi-QE_A+(H+Q)\chi]-\frac{\eta Q}{4}B_\chi
\]
and original positive NL0B oscillator equations. The historical original `v019j` half-source has **not** been modified.

## 2. Hamiltonian constraint **propagates** with standard stress conservation

Let \(D=D_A+S_D,\ P=P_A+S_P,\ T=T_A+S_T,\ R=R_A+\sum_s(\rho_s+p_s)\). The total conservation identities are
\[
\dot D=-3H(D+P)-T/a+3R\dot\Phi,\qquad
\dot T=-4HT+\frac{k^2}{a}(P+R\Psi-S_\sigma).
\]
Using the original background \(\dot H=-3R/2\), momentum relation and **total** conservation, define
\[
\mathcal C_H=\frac{k^2}{a^2}\Phi+3H(\dot\Phi+H\Psi)+\frac32D,\quad
\mathcal C_\sigma=\Phi-\Psi-\frac{9a^2}{2k^2}S_\sigma.
\]
Direct independent symbolic differentiation gives the exact *off-Hamiltonian-shell* identity
\[
\boxed{\dot{\mathcal C}_H+3H\mathcal C_H=
\frac{Hk^2}{a^2}\mathcal C_\sigma.}\tag{4}
\]
Thus, **on the momentum and shear equations**, initially vanishing \(\mathcal C_H\) stays zero. Independently, differentiating the momentum constraint and using total stress momentum conservation plus shear gives the spatial Einstein trace
\[
\boxed{\ddot\Phi+H(3\dot\Phi+\dot\Psi)+(3H^2+2\dot H)\Psi
+\frac{k^2}{3a^2}(\Phi-\Psi)=\frac32P.}\tag{5}
\]
The AeST continuity and momentum equations in this same source-normalized system were **also symbolically checked**, rather than assumed. This closes **formal Einstein scalar stress consistency** but not actual C Boltzmann switch implementation or the unreduced action.

## 3. AeST-only **constraint-projected** characteristic equation

Set standard stress sources to zero **only for this independent subcase**. Unlike the earlier isolated frozen test, enforce (1)–(3), so
\(\Delta_A=-2k^2\Phi/(3a^2R_A)\), generally *not exactly zero*. At one frozen FLRW epoch and finite \(k>0\), define \(g=c_a^2k^2/(a^2K_Q)\). For a trial positive real frozen rate \(\lambda\) and all NL0B oscillators
\[
\mathcal W(\lambda)=\sum_jw_j\frac{\lambda(\lambda+3H)}
{\lambda^2+3H\lambda+\omega_j^2}.
\]
The **exact frozen \(4\times4\) determinant** for \((\Phi,\varphi,\chi,E_A)\), after eliminating the positive bath through \(\mathcal W\), has a rank-one gradient correction:
\[
\boxed{\mathcal P(\lambda,g)=D_GD_S+
g\left(K_QD_S-ND_G\right),}\tag{6}
\]
where
\[
\begin{aligned}
D_G&=(\lambda+H)(\lambda+3Hc_a^2)-\frac{QK_Q}{2},\\
D_S&=(\lambda+H)(\lambda+3Hc_a^2)
-\frac{Q}{K_B}\left[K_Q-C(H+Q-3Hc_a^2)-\frac{\eta Q}{4}\mathcal W(\lambda)\right],\\
N&=K_Q-CQ\left(1+\frac{C}{K_B}\right)-\frac{\eta Q}{4}\mathcal W(\lambda).
\end{aligned}
\]
The formula is an exact determinant identity for this **frozen constraint-projected reduced model**, not the full-time physical spectrum.

When \(g\to0\), \(\mathcal P=D_GD_S\). If \(D_S\) has a **simple** positive root distinct from a root of \(D_G\), it persists for sufficiently small \(g>0\) by continuity and the implicit function theorem. The associated nonzero metric amplitude is
\[
\boxed{\frac{\Phi}{\chi}=
\frac{g\left[K_B(\lambda+3Hc_a^2)/Q+C\right]}
{2(\lambda+H)(\lambda+3Hc_a^2)/K_Q-Q+2g},}\tag{7}
\]
provided the denominator is nonzero. Hence the constraint forces a **small but nonzero \(\Delta_A\)**, rather than automatically eliminating every scalar eigenvector.

**Important qualification of our previous finding:** The earlier AeST-only argument that a growing root is excluded when **\(\Delta_A\equiv0\)** is correct **under that additional exact assumption**. It does **not** exclude a mode with constraint-compatible \(\Delta_A\ne0\). Conversely, an instantaneous positive root in the projected matrix does **not** show that the evolving FLRW universe has a growing physical primordial mode, that the chosen adiabatic/no-free-bath initial history excites it, or that its Weyl signal is detectable.

## 4. Acceptance and remaining physics

**Supported:** formal multi-species stress source projection, preservation of H/M/shear/trace Einstein equations subject to the above conservation assumptions, AeST stress conservation, and the AeST-only frozen rank-one characteristic identity.

**Still unproved:** full time-dependent, constraint-projected **actual** photon–baryon–neutrino hierarchy; physical no-free-bath initial-mode excitation; complete unreduced covariant action-to-CLASS implementation; a stable, error-qualified physical \(\eta\)-dependent Weyl and galaxy response. The historical jagged \(10^{-6}\)-normalized transfers are not a detection or a qualified gain bound.

**Scientific decision:** `JOINT_EINSTEIN_STRESS_CLOSURE_PASS / LOCAL_AEST_ONLY_PROJECTED_ROOT_CONDITIONAL / FULL_PHYSICS_GO_BLOCK / DES_NOT_DETECTED`. No numerical CLASS or DES sweep.

### Reproducibility

- [One 21-identity symbolic source program](../ge19/physics_gate/constraint_projected_joint_operator_20261112.py), committed to the original branch. Equivalent local algebra has **21/21 PASS**; canonical source-locked WSL execution of this compact GitHub program is pending.
- [Frozen WSL 17/17 source](../results/ge19_coupled_frozen_gain_20261112_wsl.json); [14/14 first memory onset](../results/ge19_first_retarded_memory_onset_20261111_wsl.json); [9/9 radiation source](../results/ge19_radiation_neutrino_delta_source_20261111_wsl.json).
- [LW30 original ADM Einstein constraints](ge19_lw30_original_gr_aest_adm_scalar_constraints_class_bridge_2026-11-10.md), [LW33 scalar-source identity](ge19_lw33_exact_scalar_action_to_CLASS_offshell_source_decision_2026-11-10.md).

Single WSL source-lock algebra verification (no CLASS):
~~~bash
cd ~/aest-memory-gravity
git pull --ff-only
source .venv/bin/activate
set -o pipefail
python3 -u ge19/physics_gate/constraint_projected_joint_operator_20261112.py \
  --out results/ge19_constraint_projected_joint_operator_20261112_wsl.json \
  2>&1 | tee results/ge19_constraint_projected_joint_operator_20261112_wsl.log
rc=$PIPESTATUS
echo "EXIT=$rc"
~~~
Expected `GE19_CONSTRAINT_SOURCE_LOCKS_PASS 5`, `GE19_CONSTRAINT_PROJECTED_JOINT_IDENTITIES_PASS 21`, `GE19_FULL_PHYSICS_GO False`.
