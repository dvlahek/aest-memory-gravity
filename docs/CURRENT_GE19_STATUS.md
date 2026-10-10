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
