# NL1C7B4 Repair12 — implementation lock

## Status

Locked after Repair12 implementation and before any Repair12 execution.

## Preregistration

- commit: `d1b5c5f3aab13b3929f8c91eeea216724951c5f3`
- file: `docs/nl1c7b4_repair12_predata_full_constraint_order_audit.md`
- blob: `f10574705665d31dc88efb0cd34867ad2ed2de07`

## Implementation

- commit: `85b9120781b29854f7508f1a18a77f8b42c814f2`
- file: `nl1c7b/initial_constraint_certification_repair12.py`
- blob: `2199f8221bf341515301887de2f9fbf5a28b68a8`

## Frozen parent chain

- Repair11 result-freeze commit: `559650a2de9bf57a344401ba459adf2268212b81`
- Repair11 result-freeze blob: `5aade75b3c9f66427dba3ce6192d2500d4d604ee`
- Repair11 JSON SHA-256: `48c8caf0c5758b089318bcd18885c87725bc244ed5a47862ac841b37b834742d`
- Repair10 JSON SHA-256: `f1fc1a86d2d488f5e88f0d32b0d3d1d5ce9dab22f52e51fa69801948aeb6de9d`
- Repair08 JSON SHA-256: `054851decab71e79a05aca2bc9fb287bb1239c8fb425989f40920004c3d88453`
- Repair08 NPZ SHA-256: `4639f3b5c0afcddb2f98c8b9f6a9dbbf8661dac685b12d235c09075a106dafa7`

## Frozen imported code blobs

- Repair11 evaluator: `72d324d94100ee4555698bf44acd45c6b612c927`
- Repair10 evaluator: `c72a85d6d42176fb8c6a5ebf5f8e101541272701`
- Repair09 evaluator: `0cd67cecfbd590cb8819ad37314dc5b49047bc93`
- Repair01 exact non-K dictionary: `253a0ae2a19a597f06358704ea276c9005973af3`
- Repair02 helpers: `eff076ec9a511f64bc693dc48b07b2ce26cfbaeb`
- base B4 evaluator: `8559120dc273be3174eca130ca313ed6ff5acb25`
- Repair08 evaluator: `94fb3f42a7c819b0525860f7344d5dbaff93da19`
- frozen C7A reconstruction: `ff383c1ddc2cb2a684e2b5dd11fde0ae811e4fac`

## Locked audit settings

- lambda values: `0,1,1/2,1/4,1/8`
- positive lambda values: `1,1/2,1/4,1/8`
- gated L2 slope intervals: `1/2->1/4`, `1/4->1/8`
- accepted gated order interval: `[1.8,2.2]`
- Repair10 reproduction tolerance: `1e-12`
- bookkeeping closure tolerance: `1e-12`
- scales: `5,10,20 h^-1 Mpc`
- radial grids: `256,512`
- Y families: `Simple,Exponential,Sharp`
- beta values: `1.0,0.5,0.1`
- all 54 cases retained
- all non-center radial points retained
- eta: `0`

The lambda=0 baseline is fixed per case and may only be subtracted as preregistered to isolate perturbative increments. No fitted or lambda-dependent offset is licensed.

## Claim boundary

Historical B4 exact-nonlinear FAIL remains unchanged.

No state write/projection, nonlinear constraint correction, coefficient fit/rescale, source insertion/removal, sign change, K clipping, Q linearization, threshold change, radial-point removal, Y/beta/scale selection, nonlinear evolution, finite eta, B4-PASS relabel, or observational-detection claim is licensed.

Allowed terminal classifications:

- `NL1C7B4_REPAIR12_FULL_CONSTRAINT_SECOND_ORDER_AUDIT_PASS`
- `NL1C7B4_REPAIR12_FULL_CONSTRAINT_FIRST_ORDER_RESIDUAL`
- `NL1C7B4_REPAIR12_IMPLEMENTATION_FAIL`
