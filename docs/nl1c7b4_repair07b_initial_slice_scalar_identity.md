# NL1C7B4 Repair07b — initial-slice scalar-identity audit

## Status

Locked before Repair07b implementation.

Repair07a is frozen as `NL1C7B4_REPAIR07A_IMPLEMENTATION_FAIL`. Its only failed gate was the full-time serialized native-trace scalar identity, `1.5898457860349032e-07 > 1e-10`, while the same algebraic identity evaluated at the B4 initial slice was `2.3926238952144846e-14`.

Repair07b is a diagnostic-domain repair. It does not change the algebra threshold, physics equations, retained data, state, interpolation family, or B4 thresholds.

## Motivation and scope

B4 is an initial-constraint certification at `a_i = 0.02`. Repair07/07a introduced a full-time concatenated identity check over all 179 serialized native times, although no later-time state is used by the B4 initial constraint.

The stored scalar identity

`chi - Q alpha_A = a Q theta_A / k^2`

contains a cancellation. Repair07a measured cancellation condition numbers from about `1.52` to `9432`, with median about `574`. A relative norm of the small cancelled composite over the entire text-serialized trace is therefore not a suitable algebra gate for an initial-slice certification. The observed full-trace residual remains reported and is not reinterpreted as passing.

Repair07b restricts the algebra gate to the physical domain of B4: the retained native trace evaluated at `a_i` with the same PCHIP in `log(a)` already used by the frozen bridge.

## Frozen provenance

Repair07a result-freeze commit must be an ancestor of the execution HEAD.

Retained inputs remain exactly:

- Repair06 artifact `10500046102`, digest `sha256:b589d1f595782d793cdcc0f6cde1de1e4df1994b32f27ac64ee253fd665b4b1d`.
- Certified C7A state artifact `10481526695`, digest `sha256:c2ede2e602e35bbd52afdc0a5eee22cb1bf5c6efc2e1063bf8f2b91a0554fb6c`.
- Dense C7A trace artifact `10469031693`, digest `sha256:193325536405f9a21a238f5fbe71a772d2484a096dcbfec3d6007e825cc38f70`.

Parent code remains unchanged:

- frozen B4 evaluator blob `8559120dc273be3174eca130ca313ed6ff5acb25`;
- Repair05 evaluator blob `34fd22c73171fce5e32920a94d71d05de61521f6`;
- Repair07 evaluator blob `ef591df4e92b262963e928218e3932943ab9e45c`;
- Repair07a evaluator blob `59cac7b5105bc779c27ce1daea9e1a52fe582cae`.

## Frozen settings

- `eta = 0`.
- scales `[5, 10, 20] h^-1 Mpc`.
- radial resolutions `[256, 512]`.
- state reproduction limit `1e-12`.
- algebra identity limit `1e-10` unchanged.
- inherited C7A Fourier envelope `2e-2` unchanged.
- B4 raw constraint threshold `1e-7` unchanged and not a Repair07b pass gate.
- Repair05/06 linear-interface threshold `1e-5` unchanged and not a Repair07b pass gate.

## Repair07b gates

### G1 — provenance and state immutability

Require the inherited Repair07a provenance/state gate to pass and official state reproduction <= `1e-12`.

### G2 — exact covariant identities

Require both symbolic K residuals to be exactly zero and the GR Repair05 vs closed-form comparison to remain <= `1e-10` at every retained scale/resolution.

### G3 — B4 initial-slice scalar identity

Require:

1. native retained `theta_A` exists for all 128 k-groups;
2. `theta_A(a_i)` is obtained only by `PchipInterpolator(log(a), theta_A)` from the retained dense trace;
3. all bridged values are finite;
4. `composite_first_vs_theta_at_ai_relative_L2 <= 1e-10`.

The Repair07a quantity `native_identity_relative_L2` over all serialized native times must still be copied into the Repair07b output, but is diagnostic-only and is not a Repair07b gate. Repair07b must explicitly report that this quantity failed the historical Repair07a G3 threshold.

No new tolerance is introduced for the full-time serialized diagnostic.

### G4 — inherited Fourier interface envelope

Require represented-sector Fourier 0i `max_epsilon_0i <= 2e-2`, unchanged from Repair07.

### G5 — no post-result repair

No state write, coefficient fit, sign flip, source insertion, radial point removal, threshold change, nonlinear evolution, or finite eta.

## Terminal classifications

- `NL1C7B4_REPAIR07B_INITIAL_SLICE_BRIDGE_DIAGNOSTIC_PASS`
- `NL1C7B4_REPAIR07B_COVARIANT_FOURIER_INTERFACE_MISMATCH`
- `NL1C7B4_REPAIR07B_IMPLEMENTATION_FAIL`

A Repair07b diagnostic PASS does not imply B4 initial-constraint PASS. It only establishes that the frozen initial slice and represented Fourier bridge are internally consistent enough to license a separately preregistered identity-preserving scalar-representation repair. The current C7A NPZ remains immutable.

## Claim boundary

Repair07b must preserve the Repair07a full-trace failure, the historical Repair06 mismatch, all pointwise radial diagnostics, and all original thresholds. No data point may be removed and no source may be inferred or fitted.
