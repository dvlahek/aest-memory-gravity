# GE19 LW16 — exact bath scalar Euler projection into CLASS effective velocity

**Date:** 2026-11-10. **Classification:** GE19_LW16_BATH_SOURCE_PROJECTION_TO_THETA_PASS_FULL_ACTION_FLUID_DICTIONARY_OPEN.

This is a narrowly bounded, exact *off-shell bath source* result. It extends the **previously known** NL0B scalar–aether proportionality (Identity 7 PASS) with a direct change-of-variables calculation for the original CLASS effective velocity divergence. It is **not** the off-shell variation of the complete AeST + NL0B quadratic action, and **not** a proof that the CLASS effective fluid density/velocity rows reproduce all of the action's Euler equations. No cosmological solver, parameter fit or observed DES/ACT data were used.

## 1. Provenance and ordering

- Actual researcher WSL LW15 original \`results/ge19_lw15_effective_fluid_action_dictionary_audit_20261110.json\`, now uploaded verbatim into GitHub commit \`a0bc8f645b003e745f56b6419a6d3165f4836c53\`, SHA256 \`7732d5bc13ea7ff5df2fcf9747862215954af53348d0083fe7d66c195cb527f1\`. It passes **11/11 exact algebraic gates** and **18/18 original-source anchors**, while reporting complete action equivalence OPEN. Earlier LW12 source SHA \`fdec5a67d0ba5a7f22fa9b59e22116b18e6b94dce8e18578a526c36164d0b00f\` matches.
- LW16 formula protocol \`ge19/lw16_scalar_to_velocity_bath_euler_projection_predata_20261110.json\`, precommitted as \`865cbfdf72b3b9fd39e3ffbde5aae9c99b6c7d65\` (blob \`d03d947f78b216834ca64926d369ba9c255f7fb2\`). The basic NL0B rank-one identity was known before this registration; no blind-discovery claim.
- Canonical reproducible source \`ge19/lw16_scalar_to_velocity_bath_euler_projection_20261110.py\`, commit \`fd62b46fe7021be34e6028b193c563f530f5e5f2\`; **not yet executed in researcher's WSL**.
- Actual separate SymPy 1.14.0 algebra on the original reduced action completed **11/11 checks PASS**, including negative controls, and is archived at \`results/ge19_lw16_bath_projection_independent_symbolic_20261110.json\`, commit \`f8888ad46d08839f11a1311216dfd69aedfbeb40\`. Its independent local calculation artifact SHA256 is \`8a35bbe1488d8cd9c30408d2ecf144a9896e709d1fbf889ddc0741551fc7487e\`; the GitHub archival JSON has the same checked scientific facts, not claimed to be byte-identical to that local artifact.
- Original frozen parent code: \`v019/apply_patch_v019.py\` blob \`c78484eb916bfee2730759c0bdc813a706bf9a68\`; \`v019j/apply_memory_patch.py\` blob \`14796a5ed9e6265ed6810c792a93d7328a109364\`; original NL0B analytic result blob \`d005b1c135fead856510aa76b6174fb9051fa552\`. Seven exact documentary/source strings were independently checked and present in the unchanged GitHub code.

## 2. Exact one-mode reduced bath source in original AeST variables

At fixed homogeneous background time with positive a,k,Q, positive spectral mode w, frequency omega, normalized auxiliary coordinate q and physical memory parameter eta, take the **same frozen completed-square quadratic bath potential**
\[
\mathcal L_{\rm bath}^{(2)}
=-\frac{\eta}{4}\left[\omega q-\sqrt w\frac{k}{a}
(\varphi+Q\alpha)\right]^2,\qquad
\chi=\varphi+Q\alpha,\quad
B_\chi=w\chi-\frac{a\omega\sqrt w}{k}q.
\]

At fixed q, background and metric, its **unprojected action Euler source components** are
\[
\mathcal E_\varphi^{\rm bath}
=-\frac{\eta}{2}\frac{k^2}{a^2}B_\chi,\qquad
\mathcal E_\alpha^{\rm bath}
=Q\mathcal E_\varphi^{\rm bath}.
\]
Their rank-one source direction is the previously frozen NL0B Identity 7, not new independent theoretical covariance.

The actual original CLASS v019 field dictionary uses
\[
\Theta_A=\text{effective dark velocity divergence},\qquad
\theta_{\rm pot}=\frac{a\Theta_A}{k^2},\qquad
\boxed{\varphi=Q\frac{a\Theta_A}{k^2}},\qquad
\chi=Q\left(\frac{a\Theta_A}{k^2}+\alpha\right).
\]
Here the symbol \(\Theta_A\) explicitly means **CLASS velocity divergence**, not the original scalar potential \(\varphi/Q\). That distinction is essential.

## 3. New exact chain-rule relation in CLASS velocity coordinates

At fixed time, q, metric and alpha, the field redefinition obeys \(\delta\varphi=(Qa/k^2)\delta\Theta_A\). Therefore the reduced bath action variation is
\[
\boxed{
\mathcal E_{\Theta_A}^{\rm bath}
=\frac{Qa}{k^2}\mathcal E_\varphi^{\rm bath}
=\frac{a}{k^2}\mathcal E_\alpha^{\rm bath}
=-\frac{\eta Q}{2a}B_\chi.}
\]

The original CLASS aether scalar-potential equation removes the spatial \(k^2/a^2\) projection. Define its bath source on the **same frozen reduced action normalization** as
\[
F_{\alpha,\mathrm{projected}}
\equiv\frac{a^2}{k^2}\mathcal E_\alpha^{\rm bath}
=-\frac{\eta Q}{2}B_\chi.
\]

This is **exactly the sign and factor** of the old v019j aether closure assignment
\[
\Delta E_{\rm rhs}=-\frac{\eta Q}{2}B_{\chi,\rm raw}.
\]
The full conformal-time \(\Delta E_A'=(a/K_B)\Delta E_{\rm rhs}\) contains the additional pre-existing \(a/K_B\) factor. It is **not** the same object as the raw aether Euler derivative.

The new useful bridge is the exact **reduced bath Euler-source** identity
\[
\boxed{\mathcal E_{\Theta_A}^{\rm bath}
=\frac1a F_{\alpha,\mathrm{projected}}.}
\]

The Hessian in \((\Theta_A,\alpha)\) is
\[
H_{\Theta_A,\alpha}=
-\frac{\eta w Q^2}{2}
\begin{pmatrix}
1/k^2&1/a\\
1/a&k^2/a^2
\end{pmatrix},
\]
which has rank one and null direction \((k^2/a,-1)^T\). Thus the reduced spatial source remains single-direction after the exact variable change; this does not imply a new independent metric degree of freedom.

The independent SymPy check recovers **11/11 exact gates**, including detection of a deliberately incorrect spatial normalization and a missing scalar source.

## 4. What this does NOT mean for the CLASS velocity evolution row

**Critical distinction:**
\[
\mathcal E_{\Theta_A}^{\rm bath}=\delta S_{\rm bath}/\delta\Theta_A
\quad\text{is not}\quad \Theta_A'_{\rm CLASS}.
\]
The first is a component of the variational derivative of the reduced action under a field redefinition. The second is a first-order effective-fluid evolution equation, obtained in the **full coupled theory** after using Einstein equations, scalar/aether constraints, field redefinitions and equations of motion. Comparing these as if they were the same differential equation would give a false implementation-bug diagnosis.

LW15 showed the original CLASS density/velocity effective-fluid rows have zero \`J_D^code,J_T^code\` for arbitrary forcing in the E row. LW16 now gives the *necessary bath Euler variation* in the new coordinates. But we have **not** derived the *full original AeST scalar kinetic Euler equation* under this transformation, nor its precise combination with:
- temporal aether and unit-norm multiplier equations;
- normalized auxiliary orthogonality constraints and their field derivatives;
- full metric variation, Hamiltonian and momentum constraint identities;
- source/time derivative terms induced by \(Q(t)\), \(a(t)\), other AeST action terms and tensor density normalizations.

Accordingly, we CANNOT declare either that an explicit memory term is missing from the CLASS velocity conservation equation, or that the full action-to-fluid dictionary is completely certified. Both assertions exceed this reduced calculation.

## 5. Status and one genuine next physics condition

- **LW15:** original WSL 11/11 and 18/18 PASS, as originally classified; exact implemented fluid conservation is true but not sufficient to check action correctness.
- **LW16:** reduced NL0B off-shell bath Euler projection to CLASS velocity variable PASS, original source normalization exactly recovered; complete action-field-to-fluid Noether identity OPEN.
- **Old NL0B:** historical covariant eight-identity analytic PASS unchanged. LW03 radial FAIL, LW05 full shear LOS BLOCK, LW08 differential source UNRESOLVED, H4/Z21 uncertified unchanged; the global \(A_{\rm eff}\), physically valid memory histories and DES/ACT astronomical detection remain OPEN.

**Only next substantive gate:** derive the **complete independent linear AeST scalar + constrained aether/auxiliary Euler-to-fluid transformation**, not merely its bath contribution. Match the full transformed equation with the exact \((D_A,T_A,E_A,\alpha_A)\) CLASS rows on a smooth Newtonian branch, verify the temporal Bianchi identity and report any nonzero mismatch. Do not substitute a numerical CLASS impulse, new parameter fitting or another fluid-conservation identity for this derivation.

## Optional local source-bound LW16 reproduction, without CLASS

~~~bash
set +e
cd ~/aest-memory-gravity
git pull --ff-only
source .venv/bin/activate
python3 -u -m ge19.lw16_scalar_to_velocity_bath_euler_projection_20261110 --self-test
python3 -u -m ge19.lw16_scalar_to_velocity_bath_euler_projection_20261110
~~~

This checks all frozen original source blobs, the actual LW15 WSL result SHA and exact algebra, and writes the canonical local LW16 JSON. Its result is already independently computed and archived in the repository; WSL replication is optional.
