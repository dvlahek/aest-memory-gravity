# NL1C7B4 Repair09 — implementation lock

## Status

Locked after implementation and before any Repair09 runner/workflow execution.

## Locked preregistration

- preregistration commit: `ee97aec3e274f3996c87c622a770f5233666f7f6`;
- file: `docs/nl1c7b4_repair09_predata_repair08_exact_constraint_retest.md`;
- blob: `3e4f6ed8cf8a70a791f0ffef68c9b780ba7552c6`.

## Locked implementation

- implementation commit: `8f04b382aaa44960df18f662c2fa8330665e82c2`;
- file: `nl1c7b/initial_constraint_certification_repair09.py`;
- blob: `0cd67cecfbd590cb8819ad37314dc5b49047bc93`.

Frozen imported implementations:

- base B4 evaluator `nl1c7b/initial_constraint_certification.py`: blob `8559120dc273be3174eca130ca313ed6ff5acb25`;
- B4 Repair01 exact variational dictionary `nl1c7b/initial_constraint_certification_repair01.py`: blob `253a0ae2a19a597f06358704ea276c9005973af3`;
- B4 Repair02 exact nonlinear dictionary evaluator `nl1c7b/initial_constraint_certification_repair02.py`: blob `eff076ec9a511f64bc693dc48b07b2ce26cfbaeb`;
- frozen C7A reconstruction `nl1c7a/a6_a10_spherical_reconstruction.py`: blob `ff383c1ddc2cb2a684e2b5dd11fde0ae811e4fac`;
- certified Repair08 representation evaluator `nl1c7a/evaluate_identity_preserving_repair08.py`: blob `94fb3f42a7c819b0525860f7344d5dbaff93da19`.

No imported physics implementation may change for this Repair09 execution.

## Locked Repair08 state

Repair09 consumes the already certified local Repair08 state exactly:

- NPZ SHA-256: `4639f3b5c0afcddb2f98c8b9f6a9dbbf8661dac685b12d235c09075a106dafa7`;
- NPZ byte size: `103024`;
- Repair08 result JSON SHA-256: `054851decab71e79a05aca2bc9fb287bb1239c8fb425989f40920004c3d88453`;
- Repair08 result-freeze commit: `6a8812f9b8d9f4fa373212376b6c01b4649076aa`.

The historical C7A NPZ is not a Repair09 state input.

## Locked dense trace provenance

- artifact: `10469031693`;
- artifact digest: `sha256:193325536405f9a21a238f5fbe71a772d2484a096dcbfec3d6007e825cc38f70`;
- run: `35149865129`;
- run head: `4a275f4777a7e487004f4783bc2a929a93ac8188`.

The trace is background/control provenance only, as specified in the preregistration.

## Locked settings and gates

- `a_i = 0.02`;
- `eta = 0`;
- scales `[5,10,20] h^-1 Mpc`;
- primary radial state `Nr=256` loaded directly from Repair08 NPZ;
- control radial state `Nr=512` reconstructed from the same continuous Repair08 representation;
- Y families `Simple`, `Exponential`, `Sharp`;
- beta values `1.0, 0.5, 0.1`;
- total cases: `54`;
- exact nonlinear dictionary limit: `1e-12`;
- Repair08 state-anchor reproduction limit: `1e-12`;
- original B4 raw-constraint limit: `1e-7` for both H and M;
- historical two-grid RMS ratio limit: `2.0`.

The Repair05/06 `1e-5` interface threshold is not a Repair09 PASS gate.

## Claim boundary

Repair09 cannot modify, project, fit, rescale, clip, select, or delete any state, source, coefficient, sign, branch, scale, beta value, or radial point. It cannot linearize Q or clip K. It performs no nonlinear evolution and no finite-eta run.

Allowed terminal classifications remain exactly:

- `NL1C7B4_REPAIR09_REPAIR08_EXACT_NONLINEAR_CONSTRAINT_PASS`;
- `NL1C7B4_REPAIR09_REPAIR08_RAW_CONSTRAINT_FAIL`;
- `NL1C7B4_REPAIR09_IMPLEMENTATION_FAIL`.

No threshold or classification rule may be changed after execution.