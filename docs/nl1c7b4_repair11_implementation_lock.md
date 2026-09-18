# NL1C7B4 Repair11 — implementation lock

## Status

Locked after Repair11 implementation and before any Repair11 execution.

## Preregistration

- commit: `02e1e7eaffd08aa289830810250057314594b9cf`
- file: `docs/nl1c7b4_repair11_predata_esector_analytic_covariant_audit.md`
- blob: `e35181ff632bbc6461dc087d9800e63779000f18`

## Implementation

- commit: `95ba6dd33105ff0b4cada77e0df44ed819edf4a0`
- file: `nl1c7b/initial_constraint_certification_repair11.py`
- blob: `72d324d94100ee4555698bf44acd45c6b612c927`

## Frozen parent/result chain

- Repair10 result-freeze commit: `de03f563ee3e8700b3159be5a46b73633c85db8d`
- Repair10 result-freeze blob: `86021d3ac9086585a2c01223a9700b6f67896f30`
- Repair10 JSON SHA-256: `f1fc1a86d2d488f5e88f0d32b0d3d1d5ce9dab22f52e51fa69801948aeb6de9d`
- Repair08 JSON SHA-256: `054851decab71e79a05aca2bc9fb287bb1239c8fb425989f40920004c3d88453`
- Repair08 NPZ SHA-256: `4639f3b5c0afcddb2f98c8b9f6a9dbbf8661dac685b12d235c09075a106dafa7`

## Frozen imported code blobs

- Repair10 evaluator: `c72a85d6d42176fb8c6a5ebf5f8e101541272701`
- Repair09 evaluator: `0cd67cecfbd590cb8819ad37314dc5b49047bc93`
- Repair01 exact non-K source dictionary: `253a0ae2a19a597f06358704ea276c9005973af3`
- Repair02 helpers: `eff076ec9a511f64bc693dc48b07b2ce26cfbaeb`
- base B4 evaluator: `8559120dc273be3174eca130ca313ed6ff5acb25`
- Repair08 evaluator: `94fb3f42a7c819b0525860f7344d5dbaff93da19`
- frozen C7A reconstruction: `ff383c1ddc2cb2a684e2b5dd11fde0ae811e4fac`

## Locked audit settings

- implementation-equivalence normalized error limit: `1e-10`
- Repair10 hotspot absolute-or-relative reproduction limit: `1e-12`
- virtual amplitudes: `1, 1/2, 1/4, 1/8`
- allowed adjacent log2 slope interval: `[1.8,2.2]`
- scales: `5,10,20 h^-1 Mpc`
- radial grids: `256,512`
- eta: `0`

The amplitude-scaling copies are diagnostics only and are never written as official states.

## Claim boundary

No state modification/write/projection, coefficient fit/rescaling, source insertion/removal, sign change, historical-threshold change, radial-point removal, Y/beta/scale selection, nonlinear evolution, finite eta, B4 PASS claim, or observational-detection claim is licensed.

Allowed classifications:

- `NL1C7B4_REPAIR11_ESECTOR_ANALYTIC_COVARIANT_AUDIT_PASS`
- `NL1C7B4_REPAIR11_ESECTOR_INTERFACE_MISMATCH`
- `NL1C7B4_REPAIR11_IMPLEMENTATION_FAIL`
