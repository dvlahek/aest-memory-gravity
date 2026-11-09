# GE19 LW10 — original AeST+CLASS memory source to Bardeen Weyl: constrained retarded operator

**Date: 2026-11-09. Outcome: GE19_LW10_CROSS_REPOSITORY_STATIC_SOURCE_ANCHORS_13OF13_PASS_OBSERVER_GREEN_NOT_EVALUATED.** Physics-first structural derivation based on the original frozen CLASS/AeST source code, NOT a computed causal Green matrix, physical paired cosmological histories, or a sky detection. This is an **intermediate analytic milestone**, not full Einstein–AeST action-level proof of observational memory.

## Source authenticity

The code evidence was independently inspected using the original patch files in the GE19 GitHub branch and the untouched official CLASS 0.77 checkout at exact commit e85808324f51fc694d12e3ed7439552a3c3f9540. Underlying file blob locks:

- Official source/perturbations.c: c78fe4376d2eeebfbf4ff0cfca13b048d4513fa0
- Original v019/apply_patch_v019.py: c78484eb916bfee2730759c0bdc813a706bf9a68
- Original v019j/apply_memory_patch.py: 14796a5ed9e6265ed6810c792a93d7328a109364
- Original v019w/apply_variational_forcing_patch.py: 00c3f5da5a1b7734c67c82aa9181a443736101bf

All 13 preregistered substantive source anchors were confirmed in those original files. The inspection outcome and exact provenance are saved in results/ge19_lw10_readonly_crossrepo_source_anchor_evidence_20261109.json, commit 00e54de63b38c8fb374d33cc9cc96dac1280d568. The separate local patched-worktree static auditor has been committed in ge19/lw10_source_to_weyl_constrained_green_static_audit_20261109.py, but NOT YET executed against the researcher's local WSL checkout. Preregistration was committed BEFORE the 13-anchor audit in ge19/lw10_source_to_weyl_constrained_green_predata_20261109.json, commit 1e69d9c5879e7b292628535593311381ad8cd342.

## 1. Original source insertion is fixed

In the frozen Newtonian-gauge AeST effective-fluid system, the scalar-aether closure variable is E_A, the aether potential is alpha_A, the effective dark-component velocity divergence is theta_A, and density contrast delta_A. The original positive-bath action gives the linear spatial-aether Euler source

\[
\Delta E_{\mathrm{rhs}}=-\frac{\eta Q(t)}{2}B_{\chi,\mathrm{raw}}.
\]

In the *conformal-time* CLASS E_A differential equation, the first-order physical eta-tangent source is

\[
\boxed{F_E(k,\tau)=
-\frac{a(\tau)Q(\tau)}{2K_B}\,
B_{\chi,\mathrm{raw}}[\chi_0](k,\tau)}.
\]

The original v019w patch records exactly this source and adds the frozen externally provided forcing in the dy[E_aest] row only. The numerical amplifier lambda in LW01 is NOT a finite measured physical eta. This source is *a vector entry*, not a direct addition to Phi or Psi.

The original field dictionary is
\[
\chi=Q\left(\frac{a\theta_A}{k^2}+\alpha_A\right),\qquad
X_L=\frac{k}{a}\chi.
\]

## 2. Chain through the effective AeST pressure and evolution

The original v019 implementation has, in conformal Newtonian gauge and with the same CLASS variables,

\[
\Pi_A=c_a^2\delta_A+
\frac{c_a^2 k^2}{3a^2\rho_A}
\left[K_B E_A+(2-K_B)\chi\right],
\]
\[
\delta_A'
=3\mathcal H(w_A\delta_A-\Pi_A)
 -(1+w_A)(\theta_A-3\Phi'),
\]
\[
\theta_A'
=(3c_a^2-1)\mathcal H\theta_A
+\frac{k^2\Pi_A}{1+w_A}+k^2\Psi,
\qquad
\alpha_A'=a(E_A-\Psi).
\]

Here H_conf=a'/a, while c_a² is the CLASS background adiabatic sound speed; primes refer to conformal time. The AeST effective pressure contribution to the linear total stress is delta_p_A=rho_A Pi_A, and the effective fluid contributes to total density and velocity sources.

**Exact *direct partial derivatives* read from the original source** when all other state and metric inputs are held fixed:

\[
\frac{\partial\Pi_A}{\partial E_A}
=\frac{c_a^2K_B k^2}{3a^2\rho_A},
\quad
\left.\frac{\partial\theta_A'}{\partial E_A}\right|_{\rm direct}
=\frac{c_a^2K_B k^4}{3a^2\rho_A(1+w_A)},
\]
\[
\left.\frac{\partial\delta_A'}{\partial E_A}\right|_{\rm direct}
=-\frac{\mathcal H c_a^2K_B k^2}{a^2\rho_A},\quad
\left.\frac{\partial\alpha_A'}{\partial E_A}\right|_{\rm direct}=a.
\]

These identify an algebraically nontrivial route **provided the relevant coefficients do not vanish**. They are not the full Jacobian of the Einstein-constrained system; variations of chi, Psi, Phi, radiation/shear and the other species feed back.

In particular, a tiny c_a² can strongly suppress the pressure route. Other routes through alpha, chi and E_rhs may remain. It is invalid to assert a measured magnitude, a guaranteed nonzero sum over all paths, or the absence of cancellations based only on these partial derivatives.

## 3. Original Einstein metric relations and physical Weyl output

The official pinned CLASS Newtonian-gauge scalar equations compute

\[
\Psi=\Phi-\frac{9}{2}\frac{a^2}{k^2}\Sigma_\sigma,
\qquad
\Phi'=-\mathcal H\Psi+
\frac{3}{2}\frac{a^2}{k^2}\Sigma_\theta,
\]

with
\(\Sigma_\sigma=\sum_i(\rho_i+p_i)\sigma_i\) in the exact CLASS shear convention and
\(\Sigma_\theta=\sum_i(\rho_i+p_i)\theta_i\)
in its momentum convention. The metric state Phi is integrated as dy[phi]=phi_prime. The Weyl/Bardeen transfer reported by CLASS is

\[
\boxed{
W=(\Phi+\Psi)/2
=\Phi-\frac94\frac{a^2}{k^2}\Sigma_\sigma}.
\]

**Direct memory bath Einstein stress at first order is zero** on the homogeneous relaxed FLRW background in the original NL0B audit. Its gravitational effect is *indirect*, through the linear AeST state variables, induced effective-fluid stress and Einstein constraints. Direct bath stress zero does not imply metric response zero.

A transparent symbolic pathway is

\[
F_E\ \longrightarrow\ E_A\
\longrightarrow\bigl(\Pi_A,\alpha_A,\chi,\delta_A,\theta_A\bigr)\
\longrightarrow(\Sigma_\theta,\Sigma_\sigma,\Phi,\Psi)\
\longrightarrow W.
\]

The metric may respond through other species' anisotropic stresses as the full system evolves. An instantaneous change in E_A is NOT identical to an instantaneous change in W; the causal source must propagate through the full constrained state.

## 4. What can rigorously be said about the Green function?

For fixed k, first linearize the original, actually implemented Newtonian-gauge Einstein–AeST–ordinary-species system about the same frozen eta=0 background. After imposing and *consistently eliminating* algebraic Einstein constraints and approximation-branch conditions, write its full state as u and its source coefficient as e_E. Then, **on any smooth regime where the resulting linearized evolution operator exists**, the variational equation is

\[
u'(\tau)=A_{\rm eff}(k,\tau)\,u(\tau)
+e_E\,F_E(k,\tau),\qquad
\delta W(k,\tau)=C_W(k,\tau)u(\tau).
\]

Here A_eff includes feedback from all gravitational constraints, matter, radiation, free streaming and AeST fluid and aether variables; C_W includes the induced anisotropic-shear contribution. If \(\mathcal U(k;\tau,s)\) is the retarded fundamental state matrix,

\[
\partial_\tau\mathcal U(k;\tau,s)
=A_{\rm eff}(k,\tau)\mathcal U(k;\tau,s),\quad
\mathcal U(k;s,s)=I,
\]

the correct **formal** observer representation for matched zero initial state variation is

\[
\boxed{\delta W(k,\tau)=
\int_{\tau_i}^{\tau}ds\,
G_{WE}(k;\tau,s)F_E(k,s),\qquad
G_{WE}(k;\tau,s)=C_W(k,\tau)
\mathcal U(k;\tau,s)e_E.}
\]

If initial data differ, one must add \(C_W\mathcal U(\tau,\tau_i)\delta u_i\). Discrete CLASS approximation switches and tight-coupling regimes require piecewise treatment / matching. The actual A_eff, its propagator and the full Green kernel have **NOT been calculated** here. Thus the representation is a rigorously *conditional structural identity* for linear forced evolution, not a newly evaluated closed-form Green function.

**LW01 provides a limited but relevant empirical-in-code result:** the originally frozen externally forced E_A source produces a reproducible nonzero signed W transfer on native CLASS nodes. Accordingly, the *implemented, forced single-history* source-to-W transfer is numerically nontrivial in that specific regime. It does **not** show that a particular smooth compact pulse from LW09 is dynamically realizable or produces a nonzero difference in W at a chosen observation time.

## 5. The real two-history obstacle

LW09 proved that, for two freely prescribed smooth histories X_A and X_B with equal present X and all present time derivatives, the original reduced retarded bath gives distinct B_A(0) and B_B(0). But the full NL0B action with its auxiliary oscillators is a **local Markovian theory in its enlarged physical state**. For two physical solutions with identical *complete* state on a Cauchy surface, well-posed uniqueness would force identical future behavior. The constructed X-only equality does **not** set the full oscillator/matter/metric state equal.

To claim an observable memory difference one needs **at least one physical solution-pair (or an independently controlled physical perturbation experiment)** in the *original coupled theory* and a nonzero observer difference after specifying which current metric/matter controls are held matched. A formal nonzero causal source functional does not by itself imply that the difference survives constraints, gauge, observable windows or competitor-model degeneracies.

A useful conditional lemma: if a genuinely physical E-source perturbation can be varied by an arbitrary smooth compactly supported function on a past interval, and the true retarded G_WE is nonzero as a distribution on that interval, then a smooth test source exists whose late W response is nonzero. **Neither independent controllability nor physical admissibility of such test sources has been established** for the closed Einstein–AeST problem. This conditional lemma cannot be advertised as a physical observer theorem.

## 6. Scientific next gate without numerical drift

The next research milestone should be **one static constrained-state reduction**: extract A_eff and C_W from the *original modified CLASS Newtonian scalar equations* on a clean interval without approximation switches, and check algebraically whether Einstein/Noether constraints are satisfied and the source entry is independent. Only after this exact operator is closed should one set up a bounded physical two-history response test, if needed.

This is not an invitation to another H4/Z21 numerical campaign, and it does not authorize DES Y3 residuals. Existing status stays:
- LW01 native Weyl tangent PASS, source-to-W transfer nontrivial for original forced history;
- LW03 radial quadrature FAIL, LW04 time-grid source PASS;
- LW05 full cosmic-shear LOS support BLOCK;
- LW06 native matter–Weyl cross PASS, LW08 differential tiny and UNRESOLVED;
- LW07b true DES lens n(z) support candidate redMaGiC4/5 but angular forward model/likelihood BLOCK;
- LW09 original positive-bath prescribed-history theorem PASS, physical history pair/observer OPEN;
- LW10 code-level E-to-W structural source route PASS on 13/13 pristine source anchors, full Green / history discrimination UNPROVEN;
- H4/Z21 uncertified; no observational memory detection.

### Optional lightweight WSL static audit (no CLASS execution)

Run with the preexisting pinned and already patched CLASS checkout:

~~~
cd ~/aest-memory-gravity
set +e
git pull --ff-only
source .venv/bin/activate
python3 -u -m ge19.lw10_source_to_weyl_constrained_green_static_audit_20261109 --self-test
python3 -u -m ge19.lw10_source_to_weyl_constrained_green_static_audit_20261109 --class-root "$PWD/class_v077"
~~~

The program pins the original historical patch blobs and the untouched CLASS commit and original source blob, checks corresponding markers in the *modified local worktree*, then reports its structural source state without running CLASS. Any preflight mismatch is a provenance or implementation issue, **not** a physical disproof. Its output defaults to results/ge19_lw10_source_to_weyl_constrained_green_static_audit_20261109.json.
