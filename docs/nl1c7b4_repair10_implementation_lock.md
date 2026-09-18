# NL1C7B4 Repair10 — implementation lock

## Status

Locked after Repair10 implementation and before any Repair10 execution.

## Preregistration

- commit: `c43c3147da0ac7d9990d6badd422095b2b737ff9`
- file: `docs/nl1c7b4_repair10_predata_raw_source_localization.md`
- blob: `b9f4235bd6b62b8e7b79beecbe20a6d2178197b4`

## Implementation

- commit: `29ec99242e456a1780176e0cb85ee35614f02486`
- file: `nl1c7b/initial_constraint_certification_repair10.py`
- blob: `c72a85d6d42176fb8c6a5ebf5f8e101541272701`

## Frozen imported code

- Repair09 evaluator: `0cd67cecfbd590cb8819ad37314dc5b49047bc93`
- Repair01 exact non-K variational dictionary: `253a0ae2a19a597f06358704ea276c9005973af3`
- Repair02 exact nonlinear dictionary evaluator: `eff076ec9a511f64bc693dc48b07b2ce26cfbaeb`
- base B4 evaluator: `8559120dc273be3174eca130ca313ed6ff5acb25`
- Repair08 representation evaluator: `94fb3f42a7c819b0525860f7344d5dbaff93da19`

## Frozen parent result

- Repair09 result-freeze commit: `04d85232092cdc747cf317f2937f1c33a1c0dddc`
- Repair09 result-freeze blob: `09debcf9c89248f0f158b25d27fb39bdf38cefaf`
- Repair09 result JSON SHA-256: `be8b54823690ffefb62470c34ee3d7addeef45e2db81e40b10cce4b833376ffc`
- classification: `NL1C7B4_REPAIR09_REPAIR08_RAW_CONSTRAINT_FAIL`

## Frozen state and trace

- Repair08 JSON SHA-256: `054851decab71e79a05aca2bc9fb287bb1239c8fb425989f40920004c3d88453`
- Repair08 NPZ SHA-256: `4639f3b5c0afcddb2f98c8b9f6a9dbbf8661dac685b12d235c09075a106dafa7`
- dense trace artifact: `10469031693`
- dense trace digest: `sha256:193325536405f9a21a238f5fbe71a772d2484a096dcbfec3d6007e825cc38f70`

## Locked diagnostics

Repair10 may only reproduce and decompose the exact Repair09 source arrays.

Source labels are exactly:

- `GR_kin`
- `GR_curv_NL`
- `GR_curv_Rr`
- `GR_Nr_boundary`
- `AeST_E2`
- `AeST_EX`
- `AeST_X2`
- `AeST_J`
- `AeST_K`
- `dust`
- `standard_bg`

The numerical reproduction and bookkeeping-closure tolerance is `1e-12`. This is not a physical constraint threshold.

No new dominance or hotspot-stability threshold is defined.

## Claim boundary

No state modification, projection, coefficient fitting, source insertion, sign change, K clipping, Q linearization, radial-point removal, Y/beta/scale selection, threshold change, nonlinear evolution, finite eta, B4 PASS claim, or observational-detection claim is licensed.

Allowed terminal classes:

- `NL1C7B4_REPAIR10_RAW_SOURCE_LOCALIZATION_DIAGNOSTIC_PASS`
- `NL1C7B4_REPAIR10_IMPLEMENTATION_FAIL`
