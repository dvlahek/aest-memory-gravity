# GE19 LW11 — the first conditional, locally nonzero E-to-Weyl retarded Green jet

**9 November 2026. Classification: GE19_LW11_CONDITIONAL_LOCAL_E_TO_WEYL_GREEN_TAYLOR_JET_DERIVED_NOT_GLOBAL.**

This is an *analytical local-time consequence* of the implemented, original Newtonian scalar AeST+CLASS evolution equations, not the full constrained Green function, a dynamically valid pair of memory histories, a physical eta signal, or observational evidence. All 26/26 exact source-text anchors passed locally in the researcher's original patched CLASS checkout (LW10). Do not upgrade a source-code audit to Ward certification.

## Original evidence and exact provenance

- Frozen LW11 scientific assumptions and formulas, committed **before this new symbolic calculation**: ge19/lw11_local_weyl_green_jet_predata_20261109.json, commit 508bca735601897e88317506c9313e88977dbd08.
- Original researcher WSL LW10 audit is stored **byte-for-byte** at results/ge19_lw10_source_to_weyl_constrained_green_static_audit_20261109.json, SHA-256 **10e8dd7f3eaa988a48966ce7892e1da653f4215c4ce09499a4c62981cf350851**, committed as fb133a28f7e114231984b2d61110c40461ce464a. The actual local CLASS HEAD is e85808324f51fc694d12e3ed7439552a3c3f9540, and **26/26** code text anchors for official, patched worktree, original AeST and memory forcing match. It reports A_eff_assembled=false, Green_evaluated=false and physical-history-pair-certified=false.
- Original patch: v019/apply_patch_v019.py, blob c78484eb916bfee2730759c0bdc813a706bf9a68; positive memory forcing: v019j/apply_memory_patch.py, blob 14796a5ed9e6265ed6810c792a93d7328a109364; derivative forcing: v019w/apply_variational_forcing_patch.py, blob 00c3f5da5a1b7734c67c82aa9181a443736101bf.
- Official pinned CLASS source/perturbations.c, blob c78fe4376d2eeebfbf4ff0cfca13b048d4513fa0; original AeST background: v019/patch/source/aest_memory.c.
- Pure algebraic independent simplification completed with SymPy 1.14.0; machine-readable exact symbolic result: results/ge19_lw11_local_weyl_green_jet_symbolic_20261109.json, commit 928d792b723471817f812b157b4178a2dc25a5a3. **No CLASS runs or DES/ACT data were executed/read.**

## 1. Source and pressure route

The original eta-zero variational source is inserted only in the conformal-time E_aether scalar row:

\[
E' = (E')_{\rm original} + F_E,\qquad
F_E = -\frac{a Q}{2 K_B}\,B_{\chi,{\rm raw}}.
\]

This external mathematical source is measured **per unit eta at eta=0**, not a finite physically fitted eta, and is different from freely varying an admissible internal bath solution. The AeST pressure perturbation is

\[
\Pi_A=c_a^2\delta_A+\frac{c_a^2 k^2}{3a^2\rho_A}
[K_B E+(2-K_B)\chi],\quad
\chi=Q(a\theta_A/k^2+\alpha_A),
\]

so the **fixed-other-state direct partial** is

\[
D_E\Pi_A\equiv\frac{\partial\Pi_A}{\partial E}
=\frac{c_a^2 K_B k^2}{3 a^2\rho_A}.
\]

Then, in the exactly implemented conformal-time effective-fluid Euler equation,

\[
\theta_A' = (3c_a^2-1)\mathcal H\theta_A
+\frac{k^2\Pi_A}{1+w_A}+k^2\Psi,
\]

the direct fixed-state derivative is

\[
D_E\theta_A'=
\frac{c_a^2 K_B k^4}
{3a^2\rho_A(1+w_A)}.
\]

## 2. Original Einstein momentum equation closes the leading chain

The pinned CLASS Newtonian scalar momentum constraint is used in the integrated metric variable equation

\[
\Phi'=-\mathcal H\Psi+
\frac32\frac{a^2}{k^2}\Sigma_\theta,\qquad
\Sigma_\theta=\sum_i(\rho_i+p_i)\theta_i.
\]

The AeST fluid has \(\rho_A+p_A=\rho_A(1+w_A)\), so

\[
D_{\theta_A}\Phi'
=\frac32\frac{a^2}{k^2}\rho_A(1+w_A).
\]

The two factors multiply to

\[
\boxed{
D_E(\Phi'')\big|_{\rm immediate\;partial\;chain}
=\frac32\frac{a^2}{k^2}\rho_A(1+w_A)
\cdot\frac{c_a^2 K_B k^4}
{3a^2\rho_A(1+w_A)}
=\frac12\,c_a^2 K_B k^2.}
\]

The factors a, rho_A and (1+w_A) cancel exactly. This is **not a complete dynamical Jacobian calculation**. It is the immediate pressure–Euler–momentum pathway under the unchanged CLASS source conventions.

The other original constraint gives

\[
\Psi=\Phi-\frac92\frac{a^2}{k^2}\Sigma_\sigma,\quad
W=\frac{\Phi+\Psi}{2}
=\Phi-\frac94\frac{a^2}{k^2}\Sigma_\sigma.
\]

The original AeST v019/v019j patches add effective pressure and momentum but **no direct E-sourced anisotropic shear**. If other free-streaming species' shear states and their first relevant derivatives have no instantaneous direct E coupling in the *same smooth Newtonian scalar approximation branch*, the leading E-to-Weyl contribution is the Phi term above. CLASS has approximation switches and algebraic closure branches. A full branch-dependent elimination check remains necessary before upgrading this to an unconditional result for every epoch.

## 3. Conditional first nonzero Green Taylor coefficient

For the forced system with unit **mathematical** impulse in the E' row at conformal time s and fixed matched initial state, E undergoes a unit impulse jump, whereas W and W' are initially unchanged under the above direct-shear assumptions. After a short positive time lag \(\Delta=\tau-s\),

\[
\delta W(k,s+\Delta)
=\frac12\left(\frac12 c_a^2(s)K_B k^2\right)
\Delta^2+o(\Delta^2).
\]

Thus the **conditional local retarded source-to-Weyl transfer** has

\[
\boxed{
G_{WE}(k;s+\Delta,s)=
\frac14 c_a^2(s)K_B k^2\Delta^2
+o(\Delta^2),\quad \Delta\downarrow0.}
\]

This is a **leading local jet, not a computed global Green operator**. Its sign is the sign of the unit *E-row source*. The physical bath source itself has \(F_E=-a Q B_\chi/(2K_B)\), so one may **not** identify this sign with a positive/negative observed lensing change.

The original AeST background code sets

\[
c_a^2 = \frac{K_Q}{QK_{QQ}},\qquad
K_Q=I_0/a^3.
\]

For a valid calibrated original Exp branch \(I_0>0\), \(a>0\), \(Q>0\), and \(K_{QQ}>0\), the sound speed parameter is **strictly positive**. This gives a mathematically nonzero local coefficient for any k>0 and K_B>0 **under the stated smooth constrained-gauge and shear assumptions**, not a guaranteed globally observable solution.

## 4. Limits of the local jet and remaining work

1. **Source controllability is not physical history controllability.** An arbitrary delta-like F_E is not an independently admissible solution of the original Einstein–AeST+positive-bath system. The LW09 pair of freely prescribed X histories with equal present X and all derivatives cannot simply be plugged in as a source in the self-consistent cosmology.
2. **Full A_eff and C_W still open.** We have not assembled and checked the complete linear constrained Jacobian for every species, Einstein Hamiltonian and momentum constraint, neutral/noether Ward identities, tight-coupling/free-streaming approximation branches, gauge source conventions and all initial-condition constraints. A possible additional shear coupling must be audited at the intended local background regime.
3. **No global propagation or survey statistic.** A local nonzero Taylor coefficient does not imply a nonzero late-time integrated response for a particular history or absence of cancellations. LW03 radial quadrature FAIL and LW05 cosmic-shear LOS BLOCK remain unchanged. LW07b redMaGiC n(z) source selection is not an angular observed lensing window.
4. **No uniqueness against memoryless competitors.** The original positive bath is local Markovian with hidden oscillator states and non-Markovian only after integrating them out. Scale/time-dependent effective gravity can reproduce individual trajectories. A physical observable must distinguish *specified rival models* after nuisance marginalization.
5. **No Nature observational conclusion.** Not measured finite eta, not recovered J-hat, not DES/ACT significance. LW08 antisymmetric matter–metric derivative remains unresolved at high relative noise; it is not repaired by this local jet.

## 5. Single scientifically substantive next gate

Derive the **full, explicitly constrained smooth-regime** state Jacobian A_eff and Weyl observer C_W from the *original modified CLASS*, including the Hamiltonian constraint residual as a separate Ward/Einstein check. Check the short-lag coefficient against that complete operator. Construct a **dynamically admissible matched-control history pair** or a well-defined controlled-source physical protocol in that closed model. Evaluate the specific retarded Green integral for such a pair. If either gate fails, report **source-to-metric structural response only**.

Avoid a new source-grid sweep, observational posthoc tuning, H4/Z21 reopening, or a synthetic impulse treated as astronomical data. Until these gates pass, the correct classification remains **CONDITIONAL LOCAL GREEN JET, FULL METRIC OBSERVER OPEN**.
