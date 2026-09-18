# NL1C7B4 Repair15 — implementation lock

## Status

Locked after Repair15 implementation and before any Repair15 execution.

## Parent result freeze

Repair14a local PASS freeze:

- commit: `be1ad5287a22feb81e9fceef0483eefb17b1a800`
- file: `docs/nl1c7b4_repair14a_result_freeze.md`
- blob: `ad041eef454a4d02675ee4f4df6afe506177a37f`
- JSON SHA-256:
  `d60398e2804222df70e8cd3acda5fb397e9cfdd2068415b9256af4d65a5c64ca`

Historical Repair08:

- JSON SHA-256:
  `054851decab71e79a05aca2bc9fb287bb1239c8fb425989f40920004c3d88453`
- NPZ SHA-256:
  `4639f3b5c0afcddb2f98c8b9f6a9dbbf8661dac685b12d235c09075a106dafa7`

## Preregistration

- commit: `fad9c5136d04de1618d3b94ef47a483529ba4d78`
- file: `docs/nl1c7b4_repair15_predata_density_q_completed_state.md`
- blob: `f2fa2983df554c1d9807c1e135ee17b0d1839c4e`

## Implementation

- commit: `50644d7e4def48a2da80e854e1e9f0ac3c0f2720`
- file: `nl1c7b/initial_constraint_certification_repair15.py`
- blob: `b455d72d768aec2ea2835e967418574de678be2d`

## Frozen imported code

- Repair08 evaluator:
  `94fb3f42a7c819b0525860f7344d5dbaff93da19`
- Repair09 exact-state helper/evaluator:
  `0cd67cecfbd590cb8819ad37314dc5b49047bc93`
- base B4 definitions:
  `8559120dc273be3174eca130ca313ed6ff5acb25`
- C7A spherical reconstruction:
  `ff383c1ddc2cb2a684e2b5dd11fde0ae811e4fac`

## Locked state change

The only allowed primary-state change is

`phidot_minus_Q_new
 = phidot_minus_Q_Repair08 + deltaQ_corr`

with

`F_corr
 = k^2/[a_i^2 Q_bg K_QQ_bg]
   [K_B F_EA + (2-K_B) F_chi]`.

All other Repair08 primary-state arrays are copied unchanged.

The correction is built only from frozen CLASS transfers and the analytic identity certified by Repair14a. No B4 residual is used to construct it.

## Locked gates

- provenance
- Fourier completion identity <= `1e-12`
- real-space density-Q identity <= `1e-12`
- unchanged state regression <= `1e-12`
- metadata/output integrity
- claim boundary

No gate may use the future B4 retest result.

## Output rule

The new NPZ

`results/nl1c7b4_repair15_density_q_completed_primary_states.npz`

is written only if all Repair15 gates pass.

Historical Repair08 NPZ is immutable.

## Terminal classes

- `NL1C7B4_REPAIR15_DENSITY_Q_COMPLETED_STATE_CERTIFIED`
- `NL1C7B4_REPAIR15_IMPLEMENTATION_FAIL`

A certified R15 state only licenses a separately preregistered exact nonlinear B4 retest at the original `1e-7` raw-constraint limit.
