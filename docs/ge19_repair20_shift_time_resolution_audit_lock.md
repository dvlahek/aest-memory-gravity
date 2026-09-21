# GE19 Repair20 shift near-null + time-resolution audit lock

## Status

**DIAGNOSTIC IMPLEMENTATION LOCKED BEFORE REPAIR20 LOCAL RESULT**

Repair19 remains frozen historical FAIL:

`GE19_REPAIR19_PROJECTED_BOUNDARY_REDUCED_H3_Z20_PROPAGATION_FAIL`.

Repair20 is diagnostic only. It does not relabel Repair19 and does not certify Z20.

## Parent Repair19 freeze

Commit:

`71e1e60e133b79828163fe077f5991e98d40d6bb`

File:

`docs/ge19_repair19_projected_boundary_h3_z20_result_freeze.md`

Blob:

`642006d7f5dac17edb6ff39822fc2e09b74fd5e3`

Frozen local Repair19 artifacts:

- JSON SHA-256:
  `32837e04a9ea6c83642a0d465f0312cc17a02ddad168760764f3c7b999a0a14d`;
- NPZ SHA-256:
  `d638c86e48dd5c912629068f56c3780d0a611ed26ff5c161cd792a14328f7215`.

## Repair20 preregistration

Commit:

`7af03dcf16023dee12df1d93a36abf1a97881ec8`

File:

`ge19/repair20_predata_shift_near_null_time_resolution_audit.json`

Blob:

`ef26c42b8f7ec72bae23c7c173c5b8e0c3232599`

## Repair20 implementation

Initial implementation commit:

`fe4ba2f9b0bf176fc5dd9f92c3ee2dcbb9da352e`

First local execution terminated before science evaluation with

`GE19_REPAIR20_SHIFT_NEAR_NULL_TIME_RESOLUTION_AUDIT_IMPLEMENTATION_FAIL`

because the implementation requested a nonexistent Repair13 NPZ key `ln_a_primary`.

Repair13 actually freezes the primary x-grid under key `x64`.

Implementation-only repair commit:

`9bb8e4fd36be3fd26fb11b06a215b2806a269467`

File:

`ge19/repair20_shift_near_null_time_resolution_audit.py`

Final science blob:

`09c46fa2a585ba8d055ff396abc48f0bf7e40812`

The only science-script change is

`z13["ln_a_primary"] -> z13["x64"]`.

No equation, source, boundary, grid, threshold, near-null rule or routing changed.

## Frozen diagnostic design

Time ladder:

`Nt = 32, 64, 128`.

Common parent:

- frozen Repair13 Nt64 Z10 and Z10dot;
- PCHIP real/imag interpolation to all ladder grids;
- no H1 recomputation;
- Nt64 interpolation identity required.

Physics/source:

- same Repair13 reduced background;
- same Repair14 GE06+GE07+Lambda c2+Y2 source;
- same Repair18 projected boundary;
- same Repair07 two-stage Radau IIA canonical march;
- Nx=1024;
- C={C_min,C_star,C_max};
- beta0={1,0.5,0.1};
- m=1..40.

No source formula, sign, component order or normalization is changed.

## Frozen shift telemetry

At every C,beta,m,time sample Repair20 records:

- original Repair07 relative shift backward error;
- absolute shift residual;
- natural scale
  `max(|lhs|,|source|,sum|row_i w_i|,tiny)`;
- lhs magnitude;
- source magnitude;
- row-contribution scale.

The original shift metric and original threshold `1e-6` are unchanged.

## Frozen near-null rule

On Nt128 define

`S_ref = max shift natural scale`

over the complete diagnostic set.

A sample is **near-null** if

`scale <= sqrt(eps_float64) * S_ref`.

A sample is **active** otherwise.

This classification is diagnostic only. It does not alter the historical Repair19 gate.

## Frozen diagnostic controls

Positive Repair20 routing requires:

- common-parent Nt64 interpolation identity <= `1e-14`;
- Repair19 Nt64 main RHS reproduction <= `1e-12`;
- Repair18 projected p0 reproduction <= `1e-12`;
- Nt128 near-null absolute residual / S_ref <= `1000 eps_float64`;
- active Nt128 original shift relative metric <= `1e-6`;
- observed active 64->128 order >= `2.5`;
- Nt64->Nt128 state relative L2 <= `5e-3`;
- linear-system residual <= `1e-8`;
- anisotropy backward error <= `1e-6`;
- finite outputs.

The 32->64 observed order is report-only.

Expected Radau IIA global order is 3.

## Frozen routing

Only:

- `NEAR_NULL_MONITOR_PLUS_TIME_TRUNCATION_CONFIRMED`;
- `ACTIVE_SHIFT_PROPAGATION_ISSUE_REMAINS`;
- `IMPLEMENTATION_FAIL`.

Even the positive route does not certify Z20. It only licenses a separately preregistered monitor/certification repair.

## Prelock history

Initial dedicated prelock:

run `35627302721`

conclusion:

`failure`.

The failure was audit-only: synthetic PCHIP identity used bit-for-bit `np.array_equal` at interpolation nodes. No science code or preregistered rule failed or changed.

Audit-only fix commit:

`01906c451c789b07e0050b16b0f2dda81582aee0`.

Only the synthetic prelock comparison was changed to a relative-L2 tolerance. Repair20 science implementation blob remained unchanged.

Final dedicated prelock:

run `35627410376`

job `106425061096`

conclusion:

`success`.

Terminal marker:

`GE19_REPAIR20_PRELOCK_AUDIT_PASS`.

Synthetic convergence controls:

- 32->64 observed order: `3.0`;
- 64->128 observed order: `3.0`.

Frozen blobs reproduced:

- Repair07:
  `e34d28a2062c748f48bc82fa928844b02631de25`;
- Repair14:
  `06c5ced952c2370cfa4aaadb6ef8f72d2d7221de`;
- Repair18:
  `c7b3a5c689bd78a65a8150c26e1fbfae108cb580`.

## Stop rule

No Repair19 relabeling.

No Z20 certification.

No q20, H4 or Z21.

No threshold relaxation.

No observable/data inference.

## Claim boundary

Repair20 may diagnose the origin of the Repair19 shift-only failure. It does not change the physical model or any historical science classification.


## Post-lock implementation amendment before first science result

The first local Repair20 attempt on 2026-09-21 stopped immediately before any ladder propagation because the script referenced a nonexistent frozen NPZ key `ln_a_primary`.

This is classified as an implementation failure, not a science result.

The repaired script reads the exact frozen Repair13 primary grid from `x64`, which is the key written by the Repair13 NPZ producer.

Amended prelock workflow commit:

`410e6c35544a7225a91ca659c4001904c483cc12`.

Amended prelock workflow blob:

`111d8ea596cf9c2f640fdb6a7cf4121c2925e78e`.

The amended prelock explicitly requires `z13["x64"]` and forbids `ln_a_primary`.

Amended dedicated prelock run:

`35632117507` — SUCCESS.

Job:

`106440568725`.

The synthetic third-order ladder and frozen Repair07/14/18 provenance checks remain unchanged and PASS.

This amendment occurred before any Repair20 science result and does not alter the preregistration.
