# GE19 LW12 — exact AeST–Phi direct Jacobian and explicit missing matter/radiation feedback

**Date:** 2026-11-09. **Classification:** GE19_LW12_EXACT_AEST_PHI_DIRECT_JACOBIAN_BLOCK_PASS_FULL_AEFF_OPEN.

This is a **new reproducible analytic reduction of the original code-implemented smooth-branch equations**. All 25 entries in the five-variable AeST–metric **partial** Jacobian agree with the independently derived compact rows in SymPy 1.14.0. This is NOT a complete Einstein–AeST effective Jacobian, constrained full Green function, dynamically admissible two-history metric comparison, or observed lensing detection.

## 0. Provenance, corrected formula-lock and result

- The original LW10 researcher's WSL source audit is preserved exactly at results/ge19_lw10_source_to_weyl_constrained_green_static_audit_20261109.json, SHA256 10e8dd7f3eaa988a48966ce7892e1da653f4215c4ce09499a4c62981cf350851, with **26/26 source anchors PASS**, original patched CLASS HEAD e85808324f51fc694d12e3ed7439552a3c3f9540.
- Original CLASS perturbation source: lesgourg/class_public at that HEAD, file blob c78fe4376d2eeebfbf4ff0cfca13b048d4513fa0; original AeST equations: v019/apply_patch_v019.py, blob c78484eb916bfee2730759c0bdc813a706bf9a68; physical bath addition: v019j/apply_memory_patch.py, blob 14796a5ed9e6265ed6810c792a93d7328a109364; frozen signed source injection: v019w/apply_variational_forcing_patch.py, blob 00c3f5da5a1b7734c67c82aa9181a443736101bf.
- An original formula protocol ge19/lw12_aest_metric_partial_jacobian_protocol_20261109.json was committed as 024da78afe291f425de7e9686fad1945fdd3e2b8. It contained an **incorrect zero placeholder for two external-species source columns**. This was corrected transparently **before the canonical formal calculation** in an immutable new protocol: ge19/lw12_aest_metric_partial_jacobian_protocol_r1_20261109.json, commit c4a9adcd5bf27094e2f36a3c48fe556a4047ed93, Git blob 4490f60447ffc21204cad5763097a0fbc62c5904. The original wrong placeholder remains auditable in Git history. No physical model parameters or acceptance criteria changed.
- Executable source ge19/lw12_aest_metric_partial_jacobian_20261109.py, commit 2981c5fd36e5dd8d2d4a6dee4f6d64cc8924d72b. It pins the corrected predata Git blob, original historical patch blobs and real LW10 output SHA, optionally checks the CLASS HEAD, and performs SymPy exact row-equivalence tests. **This canonical source has not yet been executed in the researcher's WSL.**
- Actual **independently performed** SymPy analytical calculation (without the Git check environment): results/ge19_lw12_aest_metric_partial_jacobian_symbolic_replay_20261109.json, commit 4fed0543130de2749a49b60b3a645aaab6b8cc3b. No CLASS solves, observational residuals or new background evolution were used. The algebraic result of the program and archive replay uses the same pinned original equations, but should not be presented as independent astrophysical observation.

## 1. State, background and external species sources

Use original conformal Newtonian-gauge CLASS perturbations with conformal time \(\tau\), comoving scalar wavenumber \(k>0\), and original homogeneous AeST background \(a,\mathcal H=a'/a,H,\rho_A,w_A,c_a^2,Q,K_Q,K_B\).

Define a five-component perturbed state
\[
u_A=(\delta_A,\theta_A,\alpha_A,E_A,\Phi)^T
\]
and constants
\[
g=1+w_A,\quad
\gamma=2-K_B,\quad
L=\frac{c_a^2 k^2}{3a^2\rho_A},\quad
\beta=\frac{3a^2\rho_A g}{2k^2}.
\]

The original AeST scalar and effective fluid pressure are
\[
\chi=Q\left(\frac{a\theta_A}{k^2}+\alpha_A\right),\qquad
\Pi_A=c_a^2\delta_A+L(K_B E_A+\gamma\chi).
\]

Crucially retain the **other-species** scalar shear and momentum stress:
\[
S=\frac92\frac{a^2}{k^2}\Sigma_{\sigma,\mathrm{other}},
\quad
M=\frac32\frac{a^2}{k^2}\Sigma_{\theta,\mathrm{other}}.
\]
They include the photon, baryon, neutrino and other active species in the original CLASS scalar hierarchy, with branch-dependent approximation closures. They are generally **dynamical**, not arbitrary constants or negligible source terms. The equations below use \(\Psi=\Phi-S\), \(\Phi'=-\mathcal H(\Phi-S)+\beta\theta_A+M\) and
\[
W=(\Phi+\Psi)/2=\Phi-S/2.
\]

The original variational eta=0 forcing is
\[
F_E=-\frac{aQ}{2K_B}B_{\chi,\mathrm{raw}},
\]
added in the E_A' row. This is a formal source for the *original frozen physical background*, NOT a freely fit cosmological eta.

## 2. Exact five-variable equations as implemented

The original AeST effective-fluid/aether equations give

\[
\begin{aligned}
\delta_A'&=3\mathcal H(w_A\delta_A-\Pi_A)
       -g(\theta_A-3\Phi'),\\
\theta_A'&=(3c_a^2-1)\mathcal H\theta_A
       +\frac{k^2}{g}\Pi_A+k^2(\Phi-S),\\
\alpha_A'&=a(E_A-\Phi+S),\\
E_A'&=\frac{a}{K_B}\{K_Q\chi-\gamma[
            Q\Pi_A/g+(H+Q)\chi-3c_a^2 H Q\alpha_A]\}
        -\mathcal H E_A+F_E,\\
\Phi'&=-\mathcal H\Phi+\beta\theta_A+\mathcal H S+M.
\end{aligned}
\]

**Important qualifications:** These five equations are a faithful original **dark/metric subsystem** in the smooth Newtonian scalar branch. They are **NOT a closed physical system**, because S and M depend on the remaining species' state variables, which themselves evolve in response to Phi and Psi.

Let \(e_d,e_\theta,e_\alpha,e_E,e_\Phi\) be row basis vectors of \(\mathbb R^5\), and define
\(p=\partial_{u_A}\Pi_A\),
\(x=\partial_{u_A}\chi\),
\(r_\Phi=-\mathcal H e_\Phi+\beta e_\theta\).
Then the complete **direct partial** 5×5 Jacobian block \(A_{AA}=\partial f_A/\partial u_A\) with the other-species state held fixed has explicit rows:

\[
\boxed{\begin{aligned}
r_\delta &=3\mathcal H w_A e_\delta-3\mathcal H p
          -g e_\theta+3g r_\Phi,\\
r_\theta &=(3c_a^2-1)\mathcal H e_\theta
          +(k^2/g)p+k^2 e_\Phi,\\
r_\alpha &=a e_E-a e_\Phi,\\
r_E &=\frac{a}{K_B}\left(
     [K_Q-\gamma(H+Q)]x-\frac{\gamma Q}{g}p
     +3\gamma c_a^2HQ e_\alpha\right)-\mathcal H e_E,\\
r_\Phi &=-\mathcal H e_\Phi+\beta e_\theta.
\end{aligned}}
\]

All **25** entries from a direct symbolic differentiation of the original five equations match these row expressions exactly.

## 3. New: exact non-AeST stress coupling columns

Treating \(S\) and \(M\) as independent *external species state functionals* during differentiation gives the exact 5×2 source-coupling matrix

\[
\boxed{
V=\frac{\partial f_A}{\partial (S,M)}
=\begin{pmatrix}
3g\mathcal H & 3g\\
-k^2 & 0\\
a & 0\\
0 & 0\\
\mathcal H & 1
\end{pmatrix}.
}
\]

This nonzero V was deliberately included in the corrected r1 protocol and is a concrete reason that the five-state A_AA is NOT A_eff. The Weyl observer also contains a non-AeST term:
\[
\boxed{\delta W=e_\Phi\,\delta u_A-\frac12\delta S.}
\]

The true full linear system must include an ordinary-species state \(u_O\) with branch-dependent \((\Sigma_{\sigma},\Sigma_\theta)\), its source/observer mapping and the other species' reaction to the AeST-induced \(\Phi,\Psi\):

\[
\begin{pmatrix}u_A'\\u_O'\end{pmatrix}
=
\begin{pmatrix} A_{AA}&A_{AO}\\A_{OA}&A_{OO}\end{pmatrix}
\begin{pmatrix}u_A\\u_O\end{pmatrix}
+\begin{pmatrix}e_E\\0\end{pmatrix}F_E.
\]

On a smooth linear branch with \((S,M)^T=H_O u_O\), \(A_{AO}=V H_O\). **The matrices \(H_O,A_{OA},A_{OO}\) have not been extracted or certified in this phase.** Because CLASS switches photon tight coupling, radiation streaming and other approximations, a purported globally fixed A_eff without branch matrices/matching would be scientifically misleading.

### Observable demonstration that A_OA is nonzero

The untouched CLASS Newtonian-gauge **baryon** density equation has \(\delta_b'=-\theta_b+3\Phi'\), so its direct partials in this smooth regime include
\[
\partial_{\theta_A}\delta_b'=3\beta,\quad
\partial_\Phi\delta_b'=-3\mathcal H.
\]
The baryon Euler equation includes \(k^2\Psi=k^2(\Phi-S)\), hence a direct \(\partial_\Phi\theta_b'=k^2\) at fixed other species state. Likewise the photon temperature-density evolution for RSA-off has \(\delta_\gamma'=-\tfrac43\theta_\gamma+4\Phi'\), giving \(\partial_{\theta_A}\delta_\gamma'=4\beta\). These exact entries are a **source-level counterexample to treating the five-state subsystem as globally dynamically closed**. They do not yet build the full species Jacobian.

## 4. Re-deriving the LW11 local causal observer coefficient

With the five-state Weyl row \(C=e_\Phi\) and the original source column \(e_E=(0,0,0,1,0)^T\), exact SymPy matrix multiplication gives
\[
C e_E=0,\quad C A_{AA}e_E=0,\quad
\boxed{C A_{AA}^2e_E=\tfrac12 c_a^2K_Bk^2.}
\]
In a time-smooth regime, and **only if** the cross-feedback through other species' shear has no E-driven contribution at this same leading Taylor order after full constraint elimination, this reproduces the LW11 short-lag impulse result
\[
G_{WE}(k;s+\Delta,s)=
\frac14 c_a^2(s)K_Bk^2\Delta^2+o(\Delta^2).
\]

Substituting the *physical* formal eta=0 source \(F_E=-aQB_{\chi,\rm raw}/(2K_B)\) into the **leading local convolution integrand** gives
\[
\left(\frac{c_a^2K_Bk^2}{4}\Delta^2\right)
\left(-\frac{aQ}{2K_B}B_{\chi,\rm raw}\right)
=
\boxed{-\frac{aQ c_a^2k^2}{8}\Delta^2 B_{\chi,\rm raw}}.
\]

The **explicit** K_B prefactors cancel in that local coefficient. **This does not establish K_B independence of the full solution**, since the background, Pi, A_eff, and bath source histories depend on K_B. It also does not establish the sign or size of observed cosmic shear.

## 5. The Hamiltonian/Noether constraint and observer are still open

The metric Phi is evolved using the original Newtonian-gauge Einstein momentum relation; Psi comes from the shear relation. The five-state algebra does **not** independently verify:

- propagation of the linear **Einstein Hamiltonian and momentum constraints** under the physical NL0B source and the original full matter/radiation system;
- full AeST action-level Noether/Ward identities across all dynamically active species and approximation branches;
- a well-posed, physically admissible pair of distinct cosmological histories sharing appropriate observable present controls;
- the global retarded state-transition matrix and nonzero Green action on that physical history difference;
- validated DES or ACT galaxy/shear angular windows, k/z coverage, nonlinear tracer prescriptions, or finite physical eta.

The global LW03 radial quadrature FAIL, LW05 full cosmic-shear LOS BLOCK, LW08 antisymmetric matter–Weyl tangent UNRESOLVED, and H4/Z21 un-certified results are unchanged. The LW10 local patched-CLASS static audit remains PASS, while LW11's impulse-source nonzero jet remains **conditional**.

## 6. Next bounded physics step

**LW13, if pursued:** on **one explicitly selected smooth late-time Newtonian scalar CLASS approximation regime**, extract the photon/baryon/neutrino \(u_O\) state basis and actual \(H_O,A_{OA},A_{OO}\) blocks, then construct the full \(A_{\rm eff}\) and \(C_W\), and verify the separate Hamiltonian/constraint residual on the same branch. No parameter scanning, no new CLASS time grid runs, and no observational residual inspection. If branch-specific source elimination or constraint propagation fails, stop and record a **nonclosure**, rather than fitting DES to rescue the theory.

### Optional CPU-only local replay

The canonical lightweight SymPy script may be run after \`git pull --ff-only\` with the existing LW10 JSON present in \`results/\`:

\`\`\`bash
cd ~/aest-memory-gravity
set +e
git pull --ff-only
source .venv/bin/activate
python3 -m pip install sympy
python3 -u -m ge19.lw12_aest_metric_partial_jacobian_20261109 --self-test
python3 -u -m ge19.lw12_aest_metric_partial_jacobian_20261109 \
  --class-root "$PWD/class_v077"
\`\`\`

The script does not execute CLASS; it returns \`results/ge19_lw12_aest_metric_partial_jacobian_20261109.json\`. The independent archive replay already verified the exact symbolic identities and is stored on GitHub. Running it again is optional.
