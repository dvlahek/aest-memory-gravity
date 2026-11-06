# GE19 current scientific status

Last updated: 2026-11-06 (new checkpoint)
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
