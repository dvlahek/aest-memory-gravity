# Stable AeST kSZ R11a Repair02 — dense-resolution closure (post-data)

Date: 2026-09-16
Branch: `fullj-evolving-weyl-bridge`

## Formal classification

`STABLE_AEST_KSZ_R11A_REPAIR02_DENSE_RESOLUTION_CERTIFIED`

Repair02 passed all nine preregistered gates and closes the numerical pairwise-velocity response chain over the frozen linear-theory domain.

Historical R11a (`STABLE_AEST_KSZ_R11A_NATIVE_DENSITY_FAIL`) and Repair01 (`STABLE_AEST_KSZ_R11A_REPAIR01_RESOLUTION_FAIL`) remain frozen historical results and are not reclassified.

## Frozen parent chain

- R11a postdata: `94efaf95b4582a177bd80dd566d5d2c26b4e212c`
- Repair01 preregistration: `608851bff8d4fc8ab063cc338ec0cd102a9f74f8`
- Repair01 implementation: `11f51614a5c5ddecdcb24e898011d0d47df2b7ea`
- Repair01 runner: `d2c1b9d811cdc7344039a015210a675ec7361360`
- Repair01 postdata: `43ce2d7cd772438efe34edabc25572c7b7516bee`
- Repair02 preregistration: `f7dfff4cb6c4fc43fdd99a9a5679d509afa01714`
- Repair02 implementation: `ce2e91c6617deef81c8db7da988ca39e9b9a4d6f`
- Repair02 runner / run head: `45c0093c76380d2d680df90d14154516e4372826`

The run reused the same 25 frozen R9b2k checkpoints. No CLASS call or source-state regeneration was permitted.

## Gate result

All gates passed:

- G1 provenance/checkpoints;
- G2 common bounded support and baseline physicality;
- G3 asymptotic dense-resolution closure;
- G4 epsilon consistency;
- G5 D1 -> D2 native-density convergence;
- G6 linear-vs-PCHIP cross-operator agreement;
- G7 local eta=0.05 linearity;
- G8 background-prefactor audit;
- G9 physical-shift dense-resolution closure.

Therefore `science_evaluated = true` for the frozen theory-only pairwise-velocity response.

## Numerical closure

The response-before-integration construction removes the cancellation instability seen in historical R11a.

At the final dense grids:

- LINEAR16384 -> LINEAR32768 gives `E ~ 2.80e-3`, `C ~ 0.99999737`;
- LINEAR32768 -> LINEAR65536 gives `E ~ 1.94e-4`, `C ~ 0.999999988`;
- both are comfortably inside the frozen dense-resolution gate `E <= 0.01`, `C >= 0.999`.

The physical eta=0.05 direct shift is also resolution closed:

- LINEAR32768 -> LINEAR65536 gives `E ~ 1.98e-4`, `C ~ 0.999999987` for every tau.

Native-density convergence at tau10 remains healthy at the 32768-node primary grid:

- linear: `E ~ 2.47e-3`, `C ~ 0.99999753`;
- PCHIP: `E ~ 5.2e-4`, `C ~ 0.99999988`.

LINEAR32768 versus PCHIP32768 cross-operator agreement passes for every tau and both epsilon values:

- `E ~ 3.54e-3`;
- `C ~ 0.99999371` or higher.

Epsilon consistency is also very strong, with E from roughly `9e-6` to `1.8e-4` and cosines essentially unity.

The background-prefactor audit gives

`max |D ln(H/h)/D eta| = 0`.

Thus the certified signal arises from the density/velocity source response, not a background H/h prefactor shift.

## Certified physical response at eta = 0.05

For tau/H0 = 10, 5, 2.5, 1.25, the largest fractional pairwise-velocity shifts are approximately:

- tau10: `1.7988e-6`;
- tau5: `1.7854e-6`;
- tau2.5: `1.7592e-6`;
- tau1.25: `1.7091e-6`.

The largest fractional response occurs near

- `z = 0.29536404346937617`;
- `r = 60 Mpc/h`.

The maximum absolute eta=0.05 velocity shifts are approximately:

- tau10: `1.1363e-4 km/s` = `0.1136 m/s`;
- tau5: `1.1278e-4 km/s` = `0.1128 m/s`;
- tau2.5: `1.1111e-4 km/s` = `0.1111 m/s`;
- tau1.25: `1.0789e-4 km/s` = `0.1079 m/s`.

The RMS fractional shifts are only about `4.9e-7` to `5.1e-7`.

The direct eta=0.05 shifts agree with the local linear prediction with `E ~ 0.0162` and `C ~ 0.99988`, within the frozen G7 gate.

## Tau dependence

The certified pairwise-velocity tangent remains extremely coherent across tau.

Relative to tau10:

- tau5: `E = 0.00738`, `C = 0.999999981`;
- tau2.5: `E = 0.02188`, `C = 0.999999851`;
- tau1.25: `E = 0.04959`, `C = 0.999999268`.

Shorter relaxation time therefore modestly reduces the tangent norm but does not change its shape materially or rescue detectability.

## Scientific interpretation

R11a Repair02 licenses a numerically controlled **linear-theory unbiased-matter pairwise-velocity response** over the frozen domain `40 <= r <= 200 Mpc/h` and the six frozen redshifts.

The physical eta=0.05 effect is extremely small: the largest certified velocity shift is only about `0.11 m/s`, with fractional shifts of order `1.7e-6` to `1.8e-6`.

Therefore the kSZ/pairwise-velocity route is **amplitude-unpromising in the certified local AeST regime**. This conclusion is a theory-sensitivity statement, not an observational kSZ null or kSZ likelihood result.

No claim is licensed for:

- kSZ detection;
- optical-depth inference;
- halo/galaxy pairwise velocities without tracer modeling;
- eta or tau bounds;
- nonlinear small-scale dynamics;
- observational kSZ likelihood constraints.

Given the certified amplitude, constructing an R11b observational kSZ likelihood is not justified as the next priority. The natural continuation is the previously planned Weyl-to-growth consistency / `E_G`-type test, which asks if a ratio or cross-channel observable amplifies the memory signature even when individual absolute channels are small.

## Frozen artifact hashes

- Repair02 full runner SHA256: `1f06afc21ddb44042de3c5a64895c5fc5f7cbd487ee34127e78c75e312f9d30f`
- Repair02 environment SHA256: `98f2ff99fa426058c01eb49dd107543787f24b97acb76a870171011200d296e9`
- Repair02 JSON SHA256: `f5166409be08edc93e739b2b901bd183a2a588325eb6c71eb0ad0e8a82d2b4a1`
- Repair02 NPZ SHA256: `55aa2c936fdea2038397aeedb616b3ac505c4d9109e96961261c2541e05da951`
- Repair02 science log SHA256: `1476c9468b474b9b9e3c38a93a109b4d422f22e0e81e2ccc93741aa02cf8f85d`
