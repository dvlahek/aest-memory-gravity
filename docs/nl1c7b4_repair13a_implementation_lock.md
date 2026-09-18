# NL1C7B4 Repair13a — implementation lock

## Status

Locked after Repair13a implementation and before any Repair13a execution.

## Preregistration

- commit: `271f6bbc4a21108d5d0c1beabb9764be56e280b3`
- file: `docs/nl1c7b4_repair13a_predata_roundoff_stable_source_localization.md`
- blob: `7b02b045ed9af2a71a9d8fc751dda3369e8af924`

## Implementation

- commit: `6f934ef8d87084e04ce9422309aeea355b15821e`
- file: `nl1c7b/initial_constraint_certification_repair13a.py`
- blob: `c6aa6f781b4a581db73b2dc4be38f0217dbb4a6b`

## Frozen parent chain

- Repair13 result-freeze commit: `f3d25b37eddd322b4e1ed147c99af9b2dec0227f`
- Repair13 result-freeze blob: `6297c1f4eb34a5493ec294bf635fa7c4a913f409`
- Repair13 JSON SHA-256: `ef6791edd595a2bd8b44e52a703915385a1e2c4d98345ff4cc509a5d22a61a9b`
- Repair12 JSON SHA-256: `99c963dc65cca35c90c6b892fb4192bed1a8c03776664c9da532a5702c62767c`
- Repair11 JSON SHA-256: `48c8caf0c5758b089318bcd18885c87725bc244ed5a47862ac841b37b834742d`
- Repair10 JSON SHA-256: `f1fc1a86d2d488f5e88f0d32b0d3d1d5ce9dab22f52e51fa69801948aeb6de9d`
- Repair08 JSON SHA-256: `054851decab71e79a05aca2bc9fb287bb1239c8fb425989f40920004c3d88453`
- Repair08 NPZ SHA-256: `4639f3b5c0afcddb2f98c8b9f6a9dbbf8661dac685b12d235c09075a106dafa7`

## Frozen imported-code blobs

- Repair13 evaluator: `213d9fd22c5979ee1a47da653562dc43cb5c68cb`
- Repair12 evaluator: `2199f8221bf341515301887de2f9fbf5a28b68a8`
- Repair01 exact source dictionary: `253a0ae2a19a597f06358704ea276c9005973af3`
- base B4 evaluator: `8559120dc273be3174eca130ca313ed6ff5acb25`
- Repair08 evaluator: `94fb3f42a7c819b0525860f7344d5dbaff93da19`
- C7A reconstruction: `ff383c1ddc2cb2a684e2b5dd11fde0ae811e4fac`

## Locked arithmetic model

- binary64 unit roundoff: `u=2^-53`
- source-sum bound: `gamma_64 * S`
- coefficient-sum bound: `gamma_96 * S/lambda`
- projection bound: `gamma_(32m+128) * T/D`
- no empirical tolerance fitted from Repair13 output
- all 54 cases retained
- all 11 sources retained
- all non-center points retained
- positive lambda values unchanged: `1,1/2,1/4,1/8`

The old Repair13 fixed normalized limits remain historically failed and are reported unchanged.

## Claim boundary

Repair13a may only certify numerical self-consistency of the frozen Repair13 payload.

No state write/projection, nonlinear constraint correction, coefficient fit/rescale, source insertion/removal, sign change, K clipping, Q linearization, historical-threshold change, point removal, Y/beta/scale selection, nonlinear evolution, finite eta, B4-PASS relabel, Repair13 historical relabel, or observational-detection claim is licensed.

Allowed terminal classes:

- `NL1C7B4_REPAIR13A_ROUNDOFF_STABLE_SOURCE_LOCALIZATION_PASS`
- `NL1C7B4_REPAIR13A_IMPLEMENTATION_FAIL`
