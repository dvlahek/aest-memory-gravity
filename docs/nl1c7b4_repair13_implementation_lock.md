# NL1C7B4 Repair13 — implementation lock

## Status

Locked after Repair13 implementation and before any Repair13 execution.

## Preregistration

- commit: `f2bd2d3b693d41680e254d714aec1233502e3ce0`
- file: `docs/nl1c7b4_repair13_predata_hamiltonian_first_order_source_localization.md`
- blob: `20783a1dfdb17c5fe067171cef275a9bba32ea9f`

## Implementation

- commit: `df3250a70c37303bde723688e87a071f42b2d380`
- file: `nl1c7b/initial_constraint_certification_repair13.py`
- blob: `213d9fd22c5979ee1a47da653562dc43cb5c68cb`

## Frozen parent chain

- Repair12 result-freeze commit: `167af8e7b6d610c307b67fed7890fe0547c27bfa`
- Repair12 result-freeze blob: `791015da17a25d2f75dbd8238bdbf04faa8dbaf0`
- Repair12 JSON SHA-256: `99c963dc65cca35c90c6b892fb4192bed1a8c03776664c9da532a5702c62767c`
- Repair11 JSON SHA-256: `48c8caf0c5758b089318bcd18885c87725bc244ed5a47862ac841b37b834742d`
- Repair10 JSON SHA-256: `f1fc1a86d2d488f5e88f0d32b0d3d1d5ce9dab22f52e51fa69801948aeb6de9d`
- Repair08 JSON SHA-256: `054851decab71e79a05aca2bc9fb287bb1239c8fb425989f40920004c3d88453`
- Repair08 NPZ SHA-256: `4639f3b5c0afcddb2f98c8b9f6a9dbbf8661dac685b12d235c09075a106dafa7`

## Frozen imported code blobs

- Repair12 evaluator: `2199f8221bf341515301887de2f9fbf5a28b68a8`
- Repair11 evaluator: `72d324d94100ee4555698bf44acd45c6b612c927`
- Repair10 evaluator: `c72a85d6d42176fb8c6a5ebf5f8e101541272701`
- Repair09 evaluator: `0cd67cecfbd590cb8819ad37314dc5b49047bc93`
- Repair01 source dictionary: `253a0ae2a19a597f06358704ea276c9005973af3`
- base B4 evaluator: `8559120dc273be3174eca130ca313ed6ff5acb25`
- Repair08 evaluator: `94fb3f42a7c819b0525860f7344d5dbaff93da19`
- C7A reconstruction: `ff383c1ddc2cb2a684e2b5dd11fde0ae811e4fac`

## Locked localization settings

- positive lambda values: `1,1/2,1/4,1/8`
- source first-order-like interval: `[0.8,1.2]`
- source second-order-like interval: `[1.8,2.2]`
- numerical-zero source L2 threshold: `1e-24`
- Repair12/Repair10 reproduction tolerance: `1e-12`
- source/coefficient closure tolerance: `1e-12`
- projection-sum tolerance: `1e-12`
- all 54 cases retained
- all 11 sources retained
- all non-center radial points retained
- no post-result source selection

## Claim boundary

Historical B4 FAIL and Repair12 first-order Hamiltonian result remain unchanged.

No state write/projection, nonlinear constraint correction, coefficient fit/rescale, source insertion/removal, sign change, K clipping, Q linearization, threshold change, radial-point removal, Y/beta/scale selection, nonlinear evolution, finite eta, B4-PASS relabel, or observational-detection claim is licensed.

Allowed terminal classes:

- `NL1C7B4_REPAIR13_HAMILTONIAN_FIRST_ORDER_SOURCE_LOCALIZATION_PASS`
- `NL1C7B4_REPAIR13_IMPLEMENTATION_FAIL`
