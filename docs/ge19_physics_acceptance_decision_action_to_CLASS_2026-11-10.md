# GE19 PHYSICS GO/BLOCK — one integrated source-to-CLASS acceptance decision

**Decision date:** 2026-11-10  
**Branch:** \`physics-first-gravitational-elasticity\`  
**Result:** \`PHYSICS_BLOCK_FULL_COVARIANT_ACTION_TO_CLASS_NOT_CERTIFIED\`  
**Nature:** One bounded **source/evidence review**, performed after researcher LW33 WSL PASS, **not** a new numerical run, independent mathematical proof, causal cosmological history solution, observational forecast, or claim of memory detection.

## 1. What was actually checked, directly in the frozen repository

These are immutable *original Git blob* identifiers at the reviewed branch:

| Source | Exact Git blob | What it establishes / does not establish |
|---|---|---|
| \`docs/nl0b_predata_covariant_memory_completion.md\` | \`9b1c013153faeddbd2add3d80eb29f673bc7748f\` | Candidate covariant positive-oscillator memory Lagrangian, aether-orthogonality multiplier and prescribed raw \(-\eta Q B_\chi/2\) source; no full kinetic-normalization proof |
| \`docs/nl0b_covariant_memory_completion_result.md\` | \`d005b1c135fead856510aa76b6174fb9051fa552\` | Historical Identity 5/7 PASS, now scientifically qualified by LW25–LW33; don't rewrite historical files |
| \`ge06/analytic_aest_directional_source_generator.py\` | \`a7afe0035054a9dca55d74a6497c081422114b4c\` | **Plane-symmetric analytic** GE06 Einstein–AeST reduced action, explicitly excludes the nonanalytic Y sector and full perturbation species |
| \`ge05/memory_directional_source_generator.py\` | \`40837d77f89028da30c28899e2d0530a4401844e\` | One normalized auxiliary scalar-longitudinal projection of the positive bath; not a full covariant scalar perturbation-to-CLASS map |
| \`v019/apply_patch_v019.py\` | \`c78484eb916bfee2730759c0bdc813a706bf9a68\` | Exact original effective-fluid density, momentum, pressure, aether and metric source dictionary in CLASS C patch |
| \`v019j/apply_memory_patch.py\` | \`14796a5ed9e6265ed6810c792a93d7328a109364\` | Historical memory patch changes the E RHS as \`E_rhs_aest -= 0.5*Q_aest*Bchi_aest;\` after multiplying \`Bchi_aest\` by \`aest_eta\`; it does **not** inject independent bath terms into the pre-existing \(\delta_A'\) and \(\theta_A'\) rows |
| \`docs/ge19_lw33_exact_scalar_action_to_CLASS_offshell_source_decision_2026-11-10.md\` | \`dedcb6148b6ee4353c32972fcc456d9e3a185ffd\` | Exact reduced off-shell scalar-current residual decomposition; not full unreduced 3+1 equivalence |
| \`docs/ge19_lw12_exact_partial_jacobian_and_species_feedback_2026-11-09.md\` | \`8668c7aecee583c0114b757777260f19ec88e20a\` | Explicitly identifies missing full ordinary-species feedback/metric-response operator and physical global retarded Green |
| \`docs/ge19_lw08_observational_novelty_collision_and_relative_tangent_2026-11-09.md\` | \`ddffe96a7ed9b6e01952b63b4b77581658655326\` | Differential matter–Weyl tangent numerically unresolved; existing Weyl/geometry-matter observational literature reduces novelty of an amplitude-only signal |
| \`docs/ge19_lw22_actual_wsl_geometry_result_freeze_and_lw23_physics_gate_2026-11-10.md\` | \`87b1f65acabe13d4a4be751848710a7e8bec3609\` | Real DES Y3 foreground/source **geometry** PASS only; no observed shear or covariance fit |

The last independent *researcher WSL* mathematical result, LW33, is archived byte-identically:
- \`results/ge19_lw33_action_scalar_current_class_residual_20261110_r1.json\`; Git blob \`d5c7bfd1038fee1ae63c1d03cd10802fc3744b47\`, **19/19** symbolic checks true;
- \`results/ge19_lw33_r1.log\`; Git blob \`fe74b75a76cb5c0ec6c8fc62859a527797ff5fcc\`, seven source locks PASS and \`PHYSICAL_OBSERVER_READY False\`.

**Scope warning:** This inventory is a comparison of identified original action source files, implementation patch code, and frozen results. It is not an exhaustive audit of every source file in a 600+ file research directory. It is sufficient to conclude that the *presented chain of proofs* does not certify the required complete physical action-to-CLASS bridge; absence of a proven bridge is not proof that none can exist.

## 2. The exact physical discrepancy

The original **restricted** GE06+GE05 scalar action and unchanged effective-fluid dictionary imply the off-shell identity

\[
\mathscr S_\phi =
\frac{6a^3}{Q}R_D +
\frac{2ak^2K_B}{Q}R_E +
\frac{2ak^2(2-K_B)}{Q}R_\chi +
\frac{2ak^2K_Q}{Q}R_{\rm geo}
-\frac{6a^3}{Q}\dot R_\rho
-\frac{18a^3H}{Q}R_\rho
+\frac{a\eta k^2 B_\chi}{2}(1-4\gamma).
\]

\(R_D,R_E\) are effective density/aether evolution residuals; \(R_\chi,R_{\rm geo},R_\rho\) and \(\dot R_\rho\) are the original action/CLASS dictionary residuals. This is a **conditional theorem of the reduced analytic longitudinal theory**, and it retains the density-definition residual and its time derivative.

Under the *same* original dictionary and all corresponding on-shell rows, \(\gamma=1/4\) is uniquely compatible with \(\mathscr S_\phi=0\) when the memory force is nonzero. The frozen CLASS \(\gamma=1/2\) leaves
\[
\boxed{\mathscr S_\phi=-a\eta k^2B_\chi/2}
\]
in **that reduced model**. An artificial \(\dot D\) or \(\dot\chi\) compensation is not legitimate unless independently derived from the full covariant action.

**Crucial caveat:** The full 3+1 covariant action, with its projected auxiliary derivatives, metric/aether unit multipliers, nonanalytic Y branch, complete background species and different CLASS gauge/source projections, has *not* been reduced and matched in one self-consistent calculation. Therefore this result **does not authorize** changing one coefficient in a physically certified cosmology; the historical code is frozen as an *implemented response*, not physically calibrated \(\partial_\eta W\). Never call the quarter coefficient a full-theory theorem.

## 3. One integrated gate — what would change BLOCK to GO?

The issue is **not** another numerical precision tolerance or independent symbolic selftest. There is exactly **one theory acceptance deliverable**: a complete constrained quadratic scalar action plus a source-to-state equivalence statement containing the following rows together, with the same gauge/time convention:

| Required field/observer mapping | Present evidence | Gate |
|---|---|---|
| Background \(Q,K(Q),H\) and original AeST \(\rho,p,c_a^2\) | LW24 and original CLASS background dictionary, within analytic reduced limit | **Partial / boundary known** |
| GR+AeST Hamiltonian/shift constraints and scalar traceless/shear equation | LW30/LW31 restricted action, WSL PASS | **Restricted PASS / full covariant open** |
| Unit timelike aether and orthogonal auxiliary multiplier elimination | LW32 regular local FLRW algebraic tangent elimination PASS | **Local PASS / all dynamic terms open** |
| Original full 3+1 covariant scalar and spatial-aether **kinetic, derivative, and source** Euler rows | LW17/LW25/LW27/LW29/LW33 restricted currents; exact factor two vs frozen patch | **BLOCK: complete joint map not established** |
| Scalar/effective-fluid \(\delta_A',\theta_A'\) and auxiliary dynamics, with all action-derived \(\eta\) sources | Original v019/v019j and LW33 restricted identity; old patch injects into E alone | **BLOCK: complete source-normalized equivalence not established** |
| Time/space gauge mapping, physical \(k\), \(t\leftrightarrow\tau\) normalization, branch/initial-state causality | Individual dictionary/Noether checks | **BLOCK: single full-source projection absent** |
| Einstein constraints propagated with baryons, photons, neutrinos and their feedback; full shear sources | LW12 documents missing full \(A_{\rm eff}\), LW30/LW31 AeST-only restricted constraints | **BLOCK: all-species full operator absent** |
| Action-consistent, finite and gauge-consistent retarded \(D_m,W\) transfer and physical \(\partial_\eta P_{D_mW}\) | LW01/06 implemented source-level tangents, LW08 differential channel unresolved | **BLOCK: real physical Weyl response not certified** |
| DES Y3 \(\gamma_t\), angular/LOS support, covariance and nuisance degeneracy | LW22 geometry only, LW20 forecast specification | **BLOCK: no survey forward or detection** |

The full action gate is **accepted** only if the original covariant equations imply the exact CLASS rows and source coefficient(s) including all nonzero companions, with constraint propagation. No ad hoc change to \(\theta_A\) or \(\delta_A\), no arbitrary rescaling of frozen \(\lambda\), no DES fitting to choose a normalization.

**Gate verdict today:** \`PHYSICS_BLOCK_FULL_COVARIANT_ACTION_TO_CLASS_NOT_CERTIFIED\`. A single physical-equivalence proof has **not** been delivered; this is a provenance- and mathematics-grounded scientific BLOCK, not an assertion that memory gravity is ruled out.

## 4. The actual project action — not another LW series

1. **Stop** additional LW scripts, unrelated Noether subgates, CLASS parameter sweeps and noisy GW/sky fitting. Freeze old \`v019j\` and all LW original results.
2. The **only permitted modeling task** before physical forward calculations is to put the *full covariant constrained quadratic scalar action* and the mapping onto all CLASS evolution/constraint rows into **one document with a common field basis and explicit gauge/time conventions**. Resolve the old raw-bath-force vs normalized-E-source discrepancy *without changing observational parameters*. If the action leads to quarter with original fluid rows, specify a **new versioned CLASS candidate**; if extra sources appear, include exactly those derived terms; if this cannot be completed, keep BLOCK.
3. Once the gate passes, **one tiny local validation** of \(\eta=0\) recovery, action source ratio, constraint propagation and causal auxiliary initialization (not a sweep). Only then compute physical transfer \(\partial_\eta P_{D_mW}\).
4. DES Y3 target stays fixed as **MagLim lens bin 4 × source bin 4**, with source bin 3 geometry control. Geometry efficiencies **0.15070638368625014** and **0.056512701041848266** (ratio ~2.667) from LW22 are not signal predictions. The physical first forecast must use actual angular \(\gamma_t\), complete foreground support, nuisance-marginal Fisher information, galaxy bias constraints and an explicitly restricted memoryless rival. The LW08 differential tangent remains unresolved and may be degenerate with ordinary amplitude nuisance.
5. A physics BLOCK is **not** a license to report a significance, detection, or novelty claim. A bounded theory note on the **restricted action-normalization discrepancy** may be viable with its limits accurately stated, separate from a physical observational discovery.

### No-go on shortcut "just halve the E source"

A one-line changed factor \(1/2\to1/4\) would pass *one* necessary reduced equation, but is **not sufficient** to certify a new physical cosmological model. It would ignore full-state variations of all auxiliary modes and the coupled metric/species response. Do not edit the original patch or claim physical results from old numerical derivative amplification.

**Final verdict:** action-to-CLASS \`BLOCK\`, observational forward \`BLOCK\`; theory-level restricted normalization result **supported**. No new code or numerical work executed for this decision.
