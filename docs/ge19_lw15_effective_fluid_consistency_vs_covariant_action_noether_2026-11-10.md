# GE19 LW15 — exact CLASS effective-fluid conservation, but not independent NL0B action closure

**10 November 2026.** Classification: **GE19_LW15_IMPLEMENTED_TOTAL_FLUID_JD_JT_IDENTICALLY_ZERO_ACTION_EQUIVALENCE_STILL_OPEN**.

**Key result:** frozen AeST background and CLASS effective-fluid density/momentum equations algebraically conserve effective stress for *any* aether E' forcing. This proves code-internal stress consistency and simultaneously explains why the earlier LW13 Hamiltonian identity by itself cannot certify that the physically correct scalar Euler partner of the NL0B action was implemented. This is **not** a new failure, no new cosmological data, and does not reverse the old analytic NL0B covariant completion PASS.

## 1. Frozen provenance and independent test

- Original CLASS AeST patch \`v019/apply_patch_v019.py\`, Git blob \`c78484eb916bfee2730759c0bdc813a706bf9a68\`.
- Positive-bath injection \`v019j/apply_memory_patch.py\`, blob \`14796a5ed9e6265ed6810c792a93d7328a109364\`, whose physical memory force modifies the aether \`E_rhs_aest\` row, not direct Einstein stress.
- Original \`v019/patch/source/aest_memory.c\`, blob \`9a522a653a1855eda3cb67e856f9fc10a1e73d54\`, defines \`rho_A=(Q K_Q-K)/3\`, \`p_A=K/3\`, \`K_Q=I0/a^3\` and \`c_a²=K_Q/(Q K_QQ)\`.
- Prior [NL0B eight-identity theory PASS](nl0b_covariant_memory_completion_result.md) and [LW14 rank-one scalar/aether Ward](ge19_lw14_reconcile_nl0b_linear_bath_ward_and_lw13_total_constraint_2026-11-09.md) remain in their **original** frozen scopes.
- LW15 immutable formula protocol \`ge19/lw15_effective_fluid_action_dictionary_predata_20261110.json\` commit \`729a34c343853dd7c5616415f5e4cacc95a91b67\`, blob \`e4614f21987e1c3dd895590127525d61c7aa992e\`, created before the independent 11-gate computation.
- Original-source-locked Python \`ge19/lw15_effective_fluid_action_dictionary_audit_20261110.py\`, commit \`c3032367d83e1bd34411b8e75717551a196dbd26\`; **not yet run in researcher's WSL**.
- Actually executed **independent** SymPy 1.14.0 source-equation derivation: **11/11 exact algebraic gates PASS**. Saved in \`results/ge19_lw15_effective_fluid_background_conservation_independent_symbolic_20261110.json\`, commit \`68fceedae8011682dcfd909971063b643904b330\`. No CLASS solve, no observed shear residual.

## 2. Original background identities derived independently from K(Q)

Let \(\mathcal H=a'/a\) be conformal Hubble rate. Original AeST homogeneous model:
\[
\rho_A=\frac{QK_Q-K}{3},\qquad
p_A=\frac K3,\qquad
K_Q=I_0/a^3,\qquad c_a^2=\frac{K_Q}{QK_{QQ}}.
\]
For a regular branch \(K_{QQ}\ne0\), \(Q'=-3\mathcal H K_Q/K_{QQ}\). Differentiation **rather than assuming fluid conservation** gives
\[
\rho_A'=-\mathcal H QK_Q=-3\mathcal H(\rho_A+p_A),\qquad
p_A'=-\mathcal H\frac{K_Q^2}{K_{QQ}}=c_a^2\rho_A',
\]
and
\[
(\rho_A+p_A)'=-3\mathcal H(1+c_a^2)(\rho_A+p_A).
\]
All four corresponding exact symbolic checks PASS.

## 3. Original AeST effective-fluid conservation is an exact construction identity

Define \(D_A=\rho_A\delta_A\), \(P_A=\rho_A\Pi_A\), \(T_A=(\rho_A+p_A)\theta_A\) and \(R_A=\rho_A+p_A\). The original v019 Newtonian scalar equations are
\[
\delta_A'=3\mathcal H(w_A\delta_A-\Pi_A)
 -(1+w_A)(\theta_A-3\Phi'),\qquad
\theta_A'=(3c_a^2-1)\mathcal H\theta_A+
\frac{k^2\Pi_A}{1+w_A}+k^2\Psi.
\]
The same effective pressure in the Einstein stress source is
\[
\Pi_A=c_a^2\delta_A+
\frac{c_a^2k^2}{3a^2\rho_A}\left[K_BE_A+(2-K_B)\chi\right],
\quad
\chi=Q\left(\frac{a\theta_A}{k^2}+\alpha_A\right).
\]
Differentiating \(D_A,T_A\) and substituting the independently derived AeST background laws produces, exactly,
\[
\boxed{D_A'=-3\mathcal H(D_A+P_A)-T_A+3R_A\Phi',}
\]
\[
\boxed{T_A'=-4\mathcal H T_A+k^2P_A+k^2R_A\Psi.}
\]
Therefore the **implemented, not independently action-derived** Ward defects
\[
J_D^{\rm code}=D_A'+3\mathcal H(D_A+P_A)+T_A-3R_A\Phi',
\]
\[
J_T^{\rm code}=T_A'+4\mathcal H T_A-k^2P_A-k^2R_A\Psi
\]
vanish identically. **Crucially this works for any algebraic \(\Pi_A\) and requires neither the \(\alpha_A'\) nor the \(E_A'\) differential equation.**

### Why this does not close the physical action

The original positive-bath E-source is
\[
E_A'=E'_{A,0}-\frac{aQ\eta}{2K_B}B_{\chi,\mathrm{raw}}.
\]
Suppose a deliberately *incorrect* forcing \(F_{\mathrm{arbitrary}}(k,\tau)\) were used in this one row without the scalar Euler partner required by the action. Since the two identities above never differentiate the pressure or use \(E_A'\), **they would still return exactly \(J_D^{\rm code}=J_T^{\rm code}=0\)**.

Thus
\[
\boxed{J_D^{\rm code}=J_T^{\rm code}=0\ \not\Rightarrow\
\text{full AeST+NL0B Euler/action equivalence}.}
\]
This is a counterexample to an *inference*, **not** a discovered inconsistency in the actual source. The earlier NL0B theory audit already concluded that the physical memory scalar and aether Euler sources are proportional and no extra scalar constraint is independent. What has not been **independently** reconstructed is their exact source-to-effective-fluid implementation change of variables in CLASS.

### Negative controls show what *is* tested

Deliberately change only the pressure in density evolution, \(\Pi_A\to\Pi_A+\Delta\Pi\), while keeping the Einstein pressure unchanged. Then
\(J_D^{\rm code}=-3\mathcal H\rho_A\Delta\Pi\).

Change only the pressure in velocity evolution. Then
\(J_T^{\rm code}=k^2\rho_A\Delta\Pi\).

Use a background pressure derivative with error \(\Delta p_A'\). Then
\(J_T^{\rm code}=\theta_A\Delta p_A'\).

These three independent nonzero defects are recovered exactly by symbolic algebra. Thus the check is **sensitive to pressure/background inconsistencies** but **insensitive to action-correctness of an independently driven E row**.

## 4. Scope and scientific decision

| Verification | Result |
|---|---|
| AeST background energy equation from original K(Q) | Exact PASS |
| Original CLASS effective-fluid energy/momentum Ward identities | Exact PASS |
| Negative controls for malformed pressure and background | Exact PASS |
| Old NL0B covariant theory source redundancy | Prior analytic PASS, unchanged |
| Independent **off-shell** scalar/aether/full-metric Euler to CLASS variable map | **OPEN** |
| Original full-action physical J_D=J_T from all Euler equations | **NOT INDEPENDENTLY CERTIFIED** |
| Complete Einstein–AeST A_eff and retarded W Green | **OPEN** |
| Real DES/ACT gravitational memory observation | **NONE** |

One substantive physics task remains before the full constrained Green: **derive the action's scalar Euler variation and its exact combination with the AeST effective fluid D/T and aether E rows**, retaining the original gradient/projector normalization and the aether-unit and auxiliary constraints. It must be an **off-shell source-to-variables map**, not another conservation-form test or a retrofitted numerical correction. If it agrees, promote only the proven action/CLASS linear sector. If not, record the exact defect and do not edit frozen source/parameter values to make it fit.

No new CLASS sweeps, H4 reopening or observed-data fitting. Preserve: LW03 radial FAIL, LW05 LOS BLOCK, LW08 differential source UNRESOLVED, H4/Z21 uncertified, LW09 two-history **bath** theorem PASS but physical observer OPEN.

## Optional WSL reproduction (no CLASS run)

~~~bash
set +e
cd ~/aest-memory-gravity
git pull --ff-only
source .venv/bin/activate
python3 -u -m ge19.lw15_effective_fluid_action_dictionary_audit_20261110 --self-test
set -o pipefail
python3 -u -m ge19.lw15_effective_fluid_action_dictionary_audit_20261110 \
  2>&1 | tee results/ge19_lw15_effective_fluid_action_dictionary_audit_20261110.log
echo "EXIT="
~~~

The last echo is simply an optional shell status marker; it can be replaced by \`echo "LW15 check complete"\` on a shell that does not support PIPESTATUS. No new cosmological simulation is needed.
