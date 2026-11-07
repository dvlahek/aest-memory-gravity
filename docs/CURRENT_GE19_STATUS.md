# GE19 current scientific status

Last updated: 2026-11-07 (living checkpoint)
Branch: `physics-first-gravitational-elasticity`.
This is the **canonical living GE19 checkpoint**. Read it first when resuming the GravitationalElasticy / AeST Memory Gravity project. Earlier frozen results and classifications are immutable; the 2026-10-10 snapshot is preserved at the end.

## 2026-11-06: established theory and current frontier

**Physics goal.** Predict an observable, history-dependent gravitational response from the already derived covariant NL0B auxiliary-field/positive-Drude realization of Maxwell-type gravitational elasticity. The NL0C/AeST Y sector controls static/gradient-dependent modified gravity; the NL0B bath adds retarded/rate-dependent memory. This action, the elastic mismatch and Maxwell law are **already derived**, not tasks to restart. Sources: `docs/gravitational_elasticity_canonical_nl0b_interpretation.md`, `docs/gravitational_maxwell_viscoelasticity.md`.

**Certified or frozen prerequisites within their explicit scopes:**
- Repair13 AeST+dust+Lambda background and H1; D47–D55 original-action primary/C-star H1, continuous X10, continuum bath and first-order GE05 on-shell controls.
- D56 corrected nonanalytic Y action, including both scalar and aether rows. Corrected H3F `Z20` CERTIFIED; H3G corrected `q20` reconstructed PASS.
- H4F3B assembled **all six genuine signed, action-completed H4 sources** PASS (source-level only). H4F1 bath covariance; H4F2b signed mixed Ward template; H4F2f GE06 shift subset; H4F2h physical-clock FD4/FD8 source representation; H4F3D operator/parent ledger; D12R2 **exact background Euler on-shell elimination** PASS for arbitrary F21/L21/b21.
- D22–D41 source-representation/shift diagnostics: zero observed original shift-gate failures among **30,720 tested clock-node cases** in a limited numerical scope. This does not replace full H4 Noether certification. Historical Repair37, Cr12ac, D22A science FAILs remain FAIL.
- Existing CLASS/Planck/ACT/SPT, growth–Weyl and DES Y3 tracks provide theory/observation infrastructure, **not** a confirmed gravitational-memory detection. Observations must never tune the theory.

**Exploratory corrected-H4F3B C-star Z21 V5–V11 (local 2026-11-06):**
- **Critical storage correction:** actual solver state order is `[N,S,u,phi,T,delta_varrho]`, although one metadata record incorrectly declared another order. The enormous ~1e11 amplitude is **aether u**, **not** metric S. Prior ~68% `W_proxy` GE05/full interpretation based on wrong indexing is invalid.
- V5: `W_proxy=N-S/a` GE05/full global L2 ~0.0859 (Nt128), opposed in phase. Not gauge-invariant lensing. V6: `X_lin=Q*u+(ik/a)*phi` dominated by aether; GE05/full ~0.7009.
- V7–V8 located broad normalized shift issues, but RHS row norms mix physical units and are not the original active-mask constraint scale.
- V9: m=5 replay reproduced archived states and shift metrics **exactly**. At z=0.2, beta0=1, Nt128: full shift |residual|=5.81423406e-11, local scale=5.35299188e-05, metric=1.0861653e-06; GE05-forcing split |residual|=3.06937799e-06, scale=4.28201549e-06, metric=0.71680684. A restricted m5 active mask is **not** the original global active mask.
- V10: signed *source-only* m5 Ward GE05 vs nonGE05 norms approximately 2.2453e-08 each with total ~3.34993e-13 (Nt128); near-antiparallel. Source-Ward is not required to vanish separately; no full Noether claim.
- V11: signed complex m5 shift residual split GE05/nonGE05 cancels ~105,581x at z=0.2 Nt128 (~12,639x Nt64); `GE05 + nonGE05` state matches full at ~8.9e-16 relative L2 Nt128. **Expected linear superposition**, not an independent physics discovery. Splits use the SAME full-memory operator/background, **not** a memory-free theory.
- Local evidence: `results/ge19_z21_m5_shift_replay_v9.{json,npz,log}`, `results/ge19_z21_m5_signed_source_ward_v10.{json,log}`, `results/ge19_z21_m5_signed_shift_superposition_v11.{json,log}`. Some local artifacts may not be versioned in GitHub.

**Hard scientific status (unchanged):**
`full_H4_Ward_certified=false`; `Z21_certified=false`; `lensing_licensed=false`.
The complete actual **source + linear-operator + all-parent Euler + boundary** mixed-H4 Noether/Ward test remains the substantive blocker. Large aether Fourier coefficients need proper perturbative scaling/validity checks before physical interpretation. Do not relax `H4_active_shift_Nt128_Linf <= 1e-6`, fit missing coefficients, use observational tuning or relabel historical FAIL.

## Next research route (do not restart completed derivations)

1. Inventory and reuse H4F1/H4F2/H4F3D/D12R2 (and any later D12R9 provenance audits **only if actual frozen evidence verifies them**). Identify the **specific missing all-sector signed operator/parent/boundary Ward remainder**; no new general-purpose V12/V13 numerical diagnostic treadmill.
2. Conduct **one integrated actual common-grid H4 Ward/Noether closure** on corrected H4F3B six-piece sources, certified parents and original clock/row conventions.
3. **Only if Ward PASSes**, conduct one final action-completed Z21 science solve with unchanged active-shift gate and perturbative-consistency checks.
4. **Only if Z21 PASSes**, derive/calculate a gauge-invariant weakly nonlinear Weyl/null-geodesic lensing prediction and then compare with prepared observations using frozen theory parameters.

## 2026-11-06: integrated Ward analytical gap map (documentation, not a new science PASS)

Source-bound review of H4F3D1/D3/D4, D9, D10R1, D12R2 and D12R3 identifies the *specific outstanding* full-H4 action-realization tasks: (G1) physical first-order parent Euler residuals on common corrected H4 grids, including per-node GE05 bath; (G2) complete signed actual operator+parent+boundary Ward balance; (G3) pre-residual FD4/FD8 derivative/regularity/roundoff budget and defined B_total; (G4) only then one preregistered full-cohort structural test. The exact formal eta-bath parent `4*sum E_q10*d_x q10` and unknown-state background elimination are already proven in their frozen scopes; do not rederive them. No V12/V13 replay or Z21 science solve licensed.

Full source-bound integration map: [`docs/ge19_h4_integrated_ward_gap_map_2026-11-06.md`](ge19_h4_integrated_ward_gap_map_2026-11-06.md). This adds documentation/navigation and **does not change** `full_H4_Ward_certified=false`, `Z21_certified=false`, `lensing_licensed=false`.

## 2026-11-06: formal linear Ward syzygy and Y-source support (ANALYTIC SCOPE ONLY)

The existing H4F3D4 spatial Noether identity together with D12R2 on-shell background yields the **conditional continuum linear operator syzygy** `-d_t E_b10-a d_x E_L10=0` for arbitrary first-order fields, **provided** the linear Euler rows are derived from the same frozen covariant action. Independent certification of this identity for the actual production `Cmat` remains open. Stage E H4 Y forcing has only `u` and `phi` rows: hence its **direct** H4 source-Ward projection in shift/isotropic/anisotropy rows is exactly zero. This avoids needing a Y zero-crossing FD8 derivative envelope *for that direct term only*; it does not close all Y-dependent regularity or amend D12R3's frozen prerequisites.

Source-bound result: [`docs/ge19_h4_linear_syzygy_y_support_analytic_2026-11-06.md`](ge19_h4_linear_syzygy_y_support_analytic_2026-11-06.md); independent SymPy check `ge19/h4f3d_ward_syzygy_y_support_scope_analytic.py`. This narrows G2/G3 proof scope, but **no physical Ward PASS** and no license for a new Z21 solve or lensing.

## 2026-11-07: GE06+Lambda / GE07 background lapse cancellation — analytic progress

Source-bound symbolic derivation gives `E_N00^(GE06+Lambda)=+6C` and `E_N00^GE07=-6C` on the exact frozen Repair13 background, using `varrho_dust_action=3*C/a^3`. Thus the **total** homogeneous lapse Euler factor vanishes exactly, while neither of these two contributions vanishes separately. An explicit GE07 off-shell Euler Ward calculation and first-order expansion show that dropping the dust `E_N00*partial_x(N10)` term before combining sectors leaves a spurious defect `+6C*partial_x(N10)`. This identifies a real potential false-FAIL in a sector-by-sector Cmat test.

Analytic details and precise claim boundary: [`docs/ge19_linear_euler_background_sector_cancellation_2026-11-07.md`](ge19_linear_euler_background_sector_cancellation_2026-11-07.md). Source-bound read-only symbolic audit: `ge19/h4f3d_linear_sector_background_lapse_audit.py`. Independent local SymPy algebra checks passed on the source formulas; the committed audit has **not yet been executed on the actual checkout** and is not a new CI or full Cmat Ward PASS.

**Next physics gate:** derive and verify the combined GE06+GE07+Lambda arbitrary-jet linear Ward identity for the original 16x10 canonical Cmat with its exact time/row/momentum conventions. Do not assume separate sectors are on shell, rerun Z21, change source weights, adjust FD tolerance or interpret V11 split cancellations as physical lensing. `full_H4_Ward_certified=false`, `Z21_certified=false`, `lensing_licensed=false`.

## 2026-11-07: local sector-Ward proof executed PASS; 16 Cmat jet conditions now explicit

Uploaded local script result `GE19_LINEAR_GE06_LAMBDA_GE07_LAPSE_BACKGROUND_EXACT_PASS_TOTAL_CMAT_OPEN` has all source pins and symbolic gates PASS; frozen locally verified JSON SHA-256 `72d1376a28d75d18b8b34f3239fef1cf4f9c681f2861f78432ff931768af2dcf`, log SHA-256 `0182b737ffb78efd936e39a5a1f70700938ae7b59ec24a25bb562f5c3dd8bc27`. GE06+Lambda lapse background Euler `+6C` cancels GE07 `-6C`. Dust-only operator Ward has `+6 i k C N10`, so a sector-wise test after falsely imposing `E_N00^dust=0` is invalid.

Source-derived `Cmat` Ward `W=-d_t(Bw)-ika[Jw-d_t(Pw)]` with `B=C10+C11`, `P=C14`, `J=(C6+2(C12+C13))/3` has **16 independent integrable-jet coefficient conditions** (not 20 independent w/wdot coefficients). Formal coefficient-map algebra checked independently; **actual source-derived production Cmat all-16 evaluation remains OPEN**. Reference: [`docs/ge19_h4f3d_linear_audit_freeze_and_cmat_jet_gate_2026-11-07.md`](ge19_h4f3d_linear_audit_freeze_and_cmat_jet_gate_2026-11-07.md), companion source `ge19/h4f3d_cmat_integrable_jet_analytic_gate.py`. No new H4 science PASS, no Z21 or lensing license; D9/D12R3 budget still OPEN.

## 2026-11-07: 16 integrable-jet analytic gate executed locally PASS

Researcher-supplied **local** log and JSON of `ge19/h4f3d_cmat_integrable_jet_analytic_gate.py` agree: `GE19_CMAT_INTEGRABLE_JET_FORMAL_CONTRACT_PASS_ACTUAL_CMAT_OPEN`. All five frozen source blob pins and seven source-row binding gates match; exact symbolic 16-jet decomposition, product rule and GE07 dust-only `+6ikC*N` obstruction PASS. JSON SHA-256 **`bbc8b998a7d135522695ae4c4961ffab3ff5da66b12a2604109f0adeab627aae`** (2260 bytes); log SHA-256 **`fef8e1dd9eba7960a553fbe9ae52b3887eeccbb71cbd15fe5d46f296a96b42d2`** (172 bytes). These are user-local uploads, not claimed as GitHub CI artifacts.

**Crucial:** `production_Cmat_16_coefficients_evaluated=false`; `full_H4_Ward_certified=false`; `Z21_certified=false`; `lensing_licensed=false`. Next gate must evaluate the **actual frozen GE06+GE07+Lambda production Cmat** all-16 identities with the full Repair13 background derivatives, including independent L momentum and integrated jet relations; do not spend time on more abstract formal Ward replays.

## 2026-11-07: next single gate prepared — original production Cmat all-16 analytic syzygy (NOT YET RUN)

New read-only source-bound analytic test `ge19/h4f3d_actual_cmat_16jet_source_bound_analytic.py` at commit `15ec059f` reconstructs exactly the three Ward-relevant original GE19 canonical rows **B=C10+C11, J=(C6+2(C12+C13))/3, P=C14** directly from the pinned GE06 and GE07 first-action-variation generators and the Repair11 Lambda L row, with the exact same (w=(N,drho,S,u,phi,T,Sdot,udot,phidot,Tdot)) and Fourier jet map. Analytic background chain rule uses Repair13 `Hdot=-(Q*K_Q+3C/a^3)/2`, `Qdot=-3H*K_Q/K_QQ`, `adot=aH`, and tests all 16 exact coefficients modulo the frozen Friedmann `H^2` relation. **This program has been committed but not yet executed**; it is the next source-realization test, not another V-series single-mode replay or a full actual H4 Ward.

If 16 conditions PASS, it closes only the **continuum canonical linear operator syzygy** portion of G2. G1 physical parents and G3 physical FD4/FD8 tolerance remain open, and `full_H4_Ward_certified=false`, `Z21_certified=false`, `lensing_licensed=false` stay unchanged. A failed/unfinished analytic test must be frozen as UNRESOLVED; do not modify the original source coefficients or scientific thresholds.

## 2026-11-07: **ACTUAL production Cmat linear Ward identity PASS (16/16)**

Researcher-executed source-bound analytic check `ge19/h4f3d_actual_cmat_16jet_source_bound_analytic.py` classified `GE19_ACTUAL_FROZEN_CMAT_16JET_EXACT_WARD_SYZYGY_PASS_H4_OPEN`, with **16/16 exact source-derived integrable-jet coefficients**, **6/6 pinned source blobs** and **15/15 original row/background bindings**. The proof used exact Repair13 background ODE/Friedmann relationships, original GE06/GE07/Lambda action coefficients, the shift `C10+C11`, L projection `(C6+2(C12+C13))/3` and independent time-differentiated L momentum `C14`; no `Z21` was solved. User-local immutable evidence: JSON `results/ge19_h4f3d_actual_cmat_16jet_20261107.json` SHA256 `ad61f5b9ce326fdd8ec6991274c8737ec26b40f6178f60200ad70a9e603c00ed`, log SHA256 `7d7d56f18340931298f7b0755022d66545dc65bbcabaef03fe4baddf9dff2d3f`.

**PROMOTE ONLY:** the actual **continuum linear canonical GE06+GE07+Lambda operator syzygy** part of G2 is now source-bound analytically closed. Earlier planned `ACTUAL_CMAT_16_COEFFICIENTS_OPEN` is **superseded by this PASS**. **NOT PROMOTED:** complete mixed H4 all-parent / boundary identity, common-grid FD4/FD8 Ward, physical error budget, H4 science, Z21 or lensing. Explicit frozen flags remain `full_H4_Ward_certified=false`, `Z21_certified=false`, `lensing_licensed=false`. Do not assume discrete FD4 of Cmat rows obeys the exact continuum identity without a physical derivative/error proof.

Full dated proof record: [`docs/ge19_actual_cmat_16jet_operator_ward_pass_2026-11-07.md`](ge19_actual_cmat_16jet_operator_ward_pass_2026-11-07.md). **Next focus is G1/G3** (actual all-interval H1/Z11/GE05 parent Euler and lower-boundary closure; preregistered FD4/FD8 M5/M9/roundoff structural `B_total`). Prior D12R9B/C/D provenance reports have not been re-audited from exact local files in this turn; never infer that they certified the missing envelopes. Once G1+G3 close, attempt one integrated full physical H4 Ward. Preserve all historical FAILs and original `1e-6` active shift criterion.

## 2026-11-07: Stage E Y zero-gradient analytic tangent bound (scope limited)

For frozen Stage E `F(g)=g|g|` with `g=g10+eta*g11`, a new mathematical proof gives `|F(g10+eta*g11)-F(g10)-2eta|g10|g11|<=eta^2|g11|^2` **uniformly at all zero crossings**. At fixed Fourier cutoff `|k|<=K`, `||d_x P_K remainder||_L2 <= K eta^2 ||g11||_L4^2`. The direct Y source-Ward remains identically zero from its exact shift/isotropic/anisotropy support. This proof does **not** provide C9 regularity of the Y flux or time-domain M9 bounds of the FD8 actual-grid parent scheme, and therefore **does not close G3**. Full proof and claim boundary: [`docs/ge19_stagee_y_flux_uniform_tangent_bound_2026-11-07.md`](ge19_stagee_y_flux_uniform_tangent_bound_2026-11-07.md). No solver executed or physical H4 certification promoted.

## 2026-11-07: G1A continuum parent-to-H4-source bound and G1B real parent ancestry

**New bounded analytic consequence:** with the source-bound actual 16/16 continuum Cmat syzygy and original D12R2 background, the H4F3D4 mixed Ward reduces identically (for physical compatible action-derived fields) to `W_six_source + R_parent - dchi(B_parent)=0`; the unknown Z21/F21 drops out. This yields a rigorous *conditional* bound for the spatially projected source Ward in terms of first-order parent Euler `L2` residuals, spatial first-derivative `L∞` field bounds and the exact four-fold GE05 bath term, without needing time M5/M9 **for that continuum mathematical identity**. Details: [`docs/ge19_g1a_parent_to_h4_source_distributional_bound_2026-11-07.md`](ge19_g1a_parent_to_h4_source_distributional_bound_2026-11-07.md), commit `3de6e71`. This does not replace the immutable D9/D12R3 *physical FD4/FD8 strong pointwise* budget or qualify full H4 science.

**New source-provenance issue, not a claimed discrepancy:** H4F3B consumes H1/H1dot stored in **H3F** (H3F reruns Repair21 H1); Repair32B Z11 was built using H1 stored in **Repair22**. Both NPZs have the same key naming and are source/sha locked but nodal equality, off-clock identity and certificate transfer from D47 R5g/D55 have **not been asserted** by the H4F3B clock-grid identity check. One read-only, frozen-hash G1B comparison of *those actual files* is prepared: `ge19/h4f3d_g1b_frozen_h1_parent_lineage_identity.py` (commit `e3ef0d2`), detailed source map [`docs/ge19_g1b_h4_parent_lineage_ancestry_2026-11-07.md`](ge19_g1b_h4_parent_lineage_ancestry_2026-11-07.md), commit `dd9698e`. **NOT YET EXECUTED**; it will report exact nodal H1/H1dot equality or a difference without fitting tolerance. No new solver or physical Ward defect is evaluated.

**Next focused step:** run the single G1B immutable H3F-vs-Repair22 H1 parent comparison. If arrays match, then trace whether the D47 R5g continuous H1 certificate applies to this precise parent lineage; if not, identify the difference before G1 Euler residual interval proof. Z11 continuous residuals, Repair26 q10/D55 scope transport, G3 physical error budget and all H4 science flags remain OPEN. Original source and original `1e-6`/temporal-order gates unchanged.

## 2026-11-07: G1B initial local run — IMPLEMENTATION FAIL, corrected without changing science

Researcher-provided `results/ge19_g1b_h1_parent_lineage_20261107.log` reports `UnboundLocalError: cannot access local variable 're' where it is not associated with a value`, at regex compilation in `ge19/h4f3d_g1b_frozen_h1_parent_lineage_identity.py`. Root cause: the later local `re=` relative-L2 assignment made Python regard the standard-library module name `re` as local throughout `main()`. The run stopped **before loading or comparing any H1/H1dot arrays** and produced no valid science classification or frozen JSON. This is **G1B_IMPLEMENTATION_FAIL**, not a difference of parent lineages and not a GE19 physics FAIL.

One-line-logic code correction committed as `5aa6e02c7e26d21e89983f2b816381f51c8a41ba`: `import re as regex`, `match=regex.compile(...)`. Original H3F/Repair22 NPZ SHA locks, all source pins, comparison semantics, and existing PASS/FAIL science gates remain unchanged. The corrected script is **not yet locally re-executed**. Re-run with a new output name only if previous output exists; otherwise reuse the intended JSON and save fresh log as `results/ge19_g1b_h1_parent_lineage_20261107_r1.log`.

## Progress recording convention (apply going forward)

- Update this living document **at every material scientific gate** (new analytic proof, actual certified PASS, genuine science FAIL, interpretation correction, physical observable). Clearly distinguish formal / source-only / exploratory / numerical / certified claims, and record date, exact file path, input SHA and fixed gate when available.
- Review status **weekly while research is active**, but if no evidence changed, leave the science claims unchanged; report `NO MATERIAL STATUS CHANGE`.
- Keep dated frozen result files and old failure records immutable. Git history records revisions of this living file. Avoid unnecessary GitHub Actions or repeated expensive diagnostic reruns.
- For resuming, read this checkpoint then `docs/ge19_history_2026-10-10.md`, the D12R2 freeze and latest relevant local results.

---

## Archived checkpoint from 2026-10-10 (verbatim)

# GE19 current scientific status

Last updated: 2026-10-10

Branch: `physics-first-gravitational-elasticity`

This file is the short recovery point for the active AeST Memory Gravity / GravitationalElasticy weakly nonlinear track. Historical FAIL results remain immutable and are not relabelled after later repairs.

## Active physical interpretation

The active model is the covariant NL0B memory completion interpreted as Maxwell-type gravitational viscoelasticity. The AeST Y sector supplies the static / gradient-dependent modified-gravity response and the NL0B sector supplies the history / rate-dependent response.

## Certified / closed prerequisites

The following are no longer active blockers:

- Repair13 reduced AeST+dust+Lambda homogeneous background and H1 closure: PASS.
- Continuous original-action H1 enclosure on the primary C-star six-mode set from the D47/R5g chain: PASS within its declared scope.
- Continuous X10 control, continuum bath quadrature and first-order GE05 bath on-shell closure from the later D55 chain: PASS within the locked primary/C-star route.
- Corrected nonanalytic Y action completion: model-level normalization/sign issue identified and repaired.
- H3F corrected-Y `Z20`: `GE19_H3F_CORRECTED_Y_H3_Z20_CERTIFIED`.
- H3G corrected-Y `q20`: `GE19_H3G_CORRECTED_Y_Q20_RECONSTRUCTION_PASS`.
- H4F3B corrected six genuine H4 source families: `GE19_H4F3B_ACTUAL_CORRECTED_SIX_SOURCE_PASS_FULL_WARD_OPEN`.
- H4F3D formal operator / parent Ward ledger through D12r1: structural algebra and conditional background multipliers complete.
- D12R2 exact background on-shell elimination: `GE19_H4F3D12R2_EXACT_BACKGROUND_ONSHELL_ELIMINATION_PASS_F21_INDEPENDENT`.
- Clock-grid source/constraint forensic route D22-D41: historical failures preserved; direct signed source representation and subsequent full 128-node shift replay gave no observed original `1e-6` shift-gate failures in 30,720 evaluated clock-node cases. This remains a numerical diagnostic, not a full H4 Ward certificate.

D12R2 was preregistered at commit

`9573f0316b0bdce5cb8b3e824602d05ca7b3dcdd`

and the frozen result is documented in

`docs/ge19_h4f3d12r2_exact_background_onshell_elimination_result_freeze.md`.

## Important immutable negative results

- Repair37 / old frozen H4 science failure remains immutable.
- Cr12ac coherent-M2 frozen-H4 result remains a robust failure around the original `1e-6` gate.
- D22A parent-candidate failure remains immutable under its original numerical representation.
- Historical implementation failures D10, D16, D20, D21, D27, D31, D34 and related repairs remain historical records and must not be relabelled.

These negative results motivated the model-level nonanalytic-Y correction. They are not candidates for further source fitting, threshold relaxation or observational tuning.

## Current frontier

Formal mixed Ward identity:

`W21 = sum_i(E_i00 dchi F_i21 + 2 E_i10 dchi F_i11 + 2 E_i11 dchi F_i10) + bath_parent - dchi(B21) - dt(E_b21)`.

D12r1 retained the unknown `F21`, `L21`, `b21` terms instead of setting them to zero. D12R2 now closes that specific structural issue exactly: under the frozen Repair13 background equations, the multiplying background Euler factors vanish, so

`E00*dchi(F21) = 0`

and

`L21*E_L00 - b21*E_b00 = 0`

for arbitrary unknown `F21/L21/b21`, without solving for or assigning those states.

Historical D11 FD4/FD8 residual arrays remain numerical diagnostics and are not promoted to exact discrete zeros.

## Next two gates

1. **One integrated full actual H4 Ward test**
   - same corrected H4F3B six-source arrays;
   - unchanged canonical linear operator;
   - certified H1, Z11, H3F Z20, H3G q20, dust and GE05 bath parents;
   - exact D12R2 background elimination;
   - complete lower boundary;
   - same physical grids/cohorts;
   - source-only Ward is not required to vanish.

2. **One final action-completed Z21 science solve, only if full Ward PASSes**
   - use the original frozen H4 gate `H4_active_shift_Nt128_Linf <= 1e-6`;
   - no fitted source factor, no threshold change and no observation-based tuning;
   - lensing is licensed only after this Z21 gate passes.

## Hard scientific rules

- Never relax the original `1e-6` H4 gate.
- Never tune theory to observations.
- Never fit missing source coefficients.
- Never relabel historical failures.
- Preserve old frozen-H4 and diagnostic artifacts as immutable provenance.
- A source-only, restricted, sampled, clock-grid or conditional PASS is not a full H4 Noether certificate.
- Lensing remains blocked until an action-completed Z21 passes the original gate.

## Recovery path

If work is interrupted, resume from this file, `docs/ge19_history_2026-10-10.md`, and the D12R2 result-freeze document. The immediate task is now the single integrated full actual H4 source + operator + all-parent + boundary Ward test. No further background/F21 closure work is needed unless that test reveals a genuinely new structural contradiction.
