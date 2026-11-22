# GE19 — First action-normalized primordial k² sector: exact X/S/retarded bath hierarchy and the *remaining* physical initial data

**22 November 2026. Physics-first checkpoint, no CLASS or DES execution.** The researcher verified the immediately preceding original reduced X/S scalar-current bridge with **17/17** symbolic checks and **4/4** source locks. Original [WSL JSON](../results/ge19_X_S_Ward_bridge_20261122_r1.json) and [log](../results/ge19_X_S_Ward_bridge_20261122_r1.log) are archived byte-identically (Git blobs \`75d01bed4127e355427262d792cb6b8c197d2abc\`, \`06fc219877b79a18376250353d7d46bfbab75523\`; respective SHA-256 \`666e95abd7838d0378987257a37447f20d78ef80c804f862c166ad010776faa3\` and \`b1b038f2a4042b1c30b1a6f68e7ad1f8b9af14ccc60da33519de9ecb8055b398\`). The two reuploaded 13/13 Exp reports match earlier archives. None asserts physical/observational memory detection.

**New:** expose the exact **O(k²)** coefficient problem of the original reduced AeST–NL0B equations, from which one can see precisely why the k=0 adiabatic mode and the proxy dust source do NOT fix the late-time memory signal. A single [source-locked 14-identity SymPy script](../ge19/physics_gate/primordial_k2_XS_retarded_bath_hierarchy_20261122.py) checks the hierarchy algebra, with 14/14 independently reproduced locally. Canonical researcher WSL source-locked run pending.

## 1. Starting point is action-normalized, not the historical half-source CLASS patch

Use cosmic proper time \`t\`, fixed regular \`a>0,Q>0,K_B\ne0,K_{QQ}>0\`, one scalar Fourier k, \`C=2-K_B\`, \`c=c_a²=K_Q/(QK_{QQ})\` and the original positive normalized retarded bath:
\`\`\`math
S_A=K_B E_A+CQX,\qquad X=\chi/Q,
\`\`\`
\`\`\`math
\dot X=-\frac{CQ}{K_B}X+
\left(\frac1{K_B}+\frac{k²}{a²Q²K_{QQ}}\right)S_A+c\Delta_A,
\`\`\`
\`\`\`math
\dot S_A=\left(\frac{CQ}{K_B}-H\right)S_A+
Q\left(K_Q-\frac{2CQ}{K_B}\right)X-\frac{\eta Q}{4}B_\chi,
\`\`\`
\`\`\`math
\ddot q_j+3H\dot q_j+\omega_j²q_j
=\omega_j\sqrt{w_j}\frac{kQX}{a},\qquad
B_\chi=W_bQX-\frac a k\sum_j\omega_j\sqrt{w_j}q_j,\quad W_b=\sum_jw_j>0.
\`\`\`
This reduced system has already been checked with the original scalar-current, stress and source dictionary. It is **not** yet proven equivalent to the complete unreduced covariant 3+1 action plus all Einstein/Boltzmann/multiplier equations.

## 2. The physically relevant *necessary* k=0 adiabatic input

A prior independent frozen Exp radiation-era leading adiabatic mode has
\`\`\`math
\alpha_A=-\frac12a\tau\Psi_0,\qquad
\varphi=\frac12aQ\tau\Psi_0,\qquad
\chi=\varphi+Q\alpha_A=0,\quad E_A=0
\`\`\`
to leading kτ and vanishing matter fraction. Thus the selected adiabatic **leading** stress is \`S_A=0\` and \`X=0\`. This is an analytic *leading mode*, NOT evidence that all finite-k coefficients \`X_2,S_2\` vanish.

For a regular, even-in-k expansion at a fixed finite background time, suppose
\`\`\`math
\Delta_A=k²\Delta_2(t)+O(k^4),\quad
X=k²X_2(t)+O(k^4),\quad
S_A=k²S_2(t)+O(k^4).
\`\`\`
If the retarded bath has **no independent q=O(k) free-mode amplitude** and was sourced by a history with X=O(k²), its driven auxiliary amplitude is odd in k:
\`\`\`math
q_j=k³q_{3j}(t)+O(k^5),\qquad
\dot q_j=k³p_{3j}(t)+O(k^5).
\`\`\`
This is a *conditional selected analytic branch*; **no unconditional full action theorem has yet selected it**. At a finite saved time, retarded q_{3j},p_{3j} need not vanish because their values retain earlier history.

## 3. Exact O(k²) original-AeST–NL0B equations: no lost bath

Substituting into the source-locked original equations and comparing powers of k yields
\`\`\`math
\boxed{
\dot X_2=-\frac{CQ}{K_B}X_2+\frac{S_2}{K_B}+c\Delta_2,
}\tag{1}
\`\`\`
\`\`\`math
\boxed{
\dot S_2=\left(\frac{CQ}{K_B}-H\right)S_2+
Q\left(K_Q-\frac{2CQ}{K_B}\right)X_2-
\frac{\eta Q}{4}B_2 ,
}\tag{2}
\`\`\`
\`\`\`math
\boxed{
\dot q_{3j}=p_{3j},\quad
\dot p_{3j}=-3Hp_{3j}-\omega_j²q_{3j}
+\frac{\omega_j\sqrt{w_j}Q}{a}X_2,
}\tag{3}
\`\`\`
\`\`\`math
\boxed{
B_2=W_bQX_2-a\sum_j\omega_j\sqrt{w_j}q_{3j}.
}\tag{4}
\`\`\`
**Two nontrivial findings**:

- In \`\dot X\`, the direct \`k²S_A/(a²Q²K_{QQ})\` gradient feedback is \`O(k^4)\`, so does **not** enter the first \`k²\` ODE for an analytic stress \`S_A=O(k²)\`. Thus the seemingly large bound \`c/R_A\` **cannot by itself enhance the leading analytic k² feedback**. This is an *ordering argument at fixed regular t*, not a uniform early-time bound as a(t)→0; the full primordial Frobenius problem must examine that limit separately.
- Although the driven q_j are \`O(k³)\`, the physical delayed source has a compensating \`1/k\` in its definition and is \`O(k²)\`. **True retarded bath feedback can therefore appear at the *same spatial gradient order* as instantaneous elasticity.** It is temporally delayed, not necessarily penalized by an extra spatial k².

The latter statement does NOT establish nonzero late Weyl memory or its amplitude, since (1)–(4) depend on initial data selected by full regularity and propagate into physical metric variables only through the complete constrained Einstein/action operator.

## 4. The dustlike 42/42 proxy supplies a source candidate, not the full physical delta₂

The previously researcher-verified coupled Einstein–Boltzmann pressureless AeST-like proxy gives
\`\`\`math
\Delta_2^{\rm proxy}(t)=
-\frac{15+4R_\nu}{40}\Psi_0\,\tau(t)^2
\left[1-\frac15 y_m(t)\right]+\cdots,\qquad
y_m=(\rho_A+\rho_b)/\rho_r.
\`\`\`
But the actual \`\Delta_2\` in Eq. (1) must be determined *jointly* from original AeST action density/pressure/momentum, the photon+baryon+neutrino hierarchy, and all Einstein constraints. Its correction can depend on X₂,S₂ and physical barotropic background. Importing the proxy as an externally imposed exact source and announcing a fully physical eigenvector would repeat the old fixed-radiation mistake.

## 5. What is **still undetermined** after all leading radiation and 42/42 proxy successes

At a finite t_i, (1)–(4) is a linear causal initial-value system. If \`Z_2=(X_2,S_2,q_{3j},p_{3j})\`, its formal solution is
\`\`\`math
Z_2(t)=U_2(t,t_i)Z_2(t_i)
+\int_{t_i}^{t}U_2(t,s)b_\Delta(s)\Delta_2(s)\,ds.
\`\`\`
The matter source specifies the particular integral, **not** the homogeneous coefficient \`Z_2(t_i)\`. Original action stress-null displacements in the scalar/aether variables can change the homogeneous X₂ amplitude while leaving instantaneous metric stress fixed. Even the leading pure-gauge/adiabatic statement \`X_0=S_0=0\` does NOT determine X₂,S₂ or the q3/p3 history. Imposing all of them as zero at the first CLASS saved time is not certified physical selection. Conversely letting them float to maximize lensing is also unjustified.

This identifies the one remaining hard physics problem **without a new parameter scan**: derive the \`k²\` Newtonian-gauge initial Frobenius matrix of the *unreduced* original 3+1 Einstein–AeST–NL0B scalar/aether/multiplier action, coupled to the full ordinary-species Boltzmann system; impose adiabaticity, acceptable regularity, genuine retarded history and complete Noether/Ward propagation. Either this **selects one** (or a documented number of) physical mode coefficients, or it rules out the candidate. Only then evolve the physical metric Weyl response.

**Status: REDUCED_ORIGINAL_ACTION_ANALYTIC_K²_HIERARCHY_VALID_CONDITIONALLY; FULL_PHYSICS_GO=False; DES_detection=False.** Do not reinterpret historical \`W_{1,delayed}\` as physical before this test.

## Reproducibility

[One source-locked 14-gate SymPy derivation](../ge19/physics_gate/primordial_k2_XS_retarded_bath_hierarchy_20261122.py). Local exact coefficient checks 14/14 pass. WSL source locks and canonical log not yet reported.
