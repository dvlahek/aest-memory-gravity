# NL1C7A Repair08 — identity-preserving scalar representation

## Status

Locked before Repair08 implementation.

Repair08 is licensed by the frozen Repair07b diagnostic PASS at commit `c32c77940b5a338fd6ca42f7251b3a1b57927fb7`, freeze blob `fa0d38dcce6902b224c8d5055a883ad163dab5bd`.

Repair07b established at the B4 initial slice that the retained growing-mode trace satisfies

`chi - Q alpha_A = a Q theta_A / k^2`

with relative L2 `2.3926238952144846e-14`, while the historical componentwise route differs from the identity-preserving composite by `9.340086572380209e-06`. The historical full-time serialized-trace Repair07a failure remains preserved and is not reclassified.

Repair08 is a numerical-representation repair only. It does not alter the physical growing mode, coefficients, target profile, eta, or any historical threshold.

## Frozen provenance

Retained inputs:

- certified C7A Repair01/evalfix artifact `10481526695`, digest `sha256:c2ede2e602e35bbd52afdc0a5eee22cb1bf5c6efc2e1063bf8f2b91a0554fb6c`;
- dense C7A trace artifact `10469031693`, digest `sha256:193325536405f9a21a238f5fbe71a772d2484a096dcbfec3d6007e825cc38f70`;
- dense trace run `35149865129`, head `4a275f4777a7e487004f4783bc2a929a93ac8188`.

Frozen C7A code:

- `nl1c7a/a5_denominator_audit.py` blob `47b486ca2defbd1db029df003b37909a9d4d170d`;
- `nl1c7a/a6_a10_spherical_reconstruction.py` blob `ff383c1ddc2cb2a684e2b5dd11fde0ae811e4fac`;
- `nl1c7a/evaluate_dense_time_repair01.py` blob `aa84b4892586a59455ec93b6dfdc0057adc20d38`;
- `nl1c7a/make_repair01_coverage_compat.py` blob `db52f94e1b896b2d277bb306a9eb4a63ea412ead`;
- historical evalfix workflow blob `3e784644e92aea67c8adbc36139d72694052e5ae`.

The historical certified C7A NPZ is read-only and must not be overwritten.

## Frozen physical/numerical settings

Repair08 inherits the certified C7A Repair01 settings exactly:

- `a_i = 0.02`;
- `eta = 0`;
- scales `[5.0, 10.0, 20.0] h^-1 Mpc`;
- primary Fourier quadrature `NQ = 256`;
- control Fourier quadrature `NQC = 512`;
- radial points `NX = 256`;
- A6 time-interpolation limit `2e-2`;
- A7 k-interpolation limit `2e-2`;
- A8 target-profile reconstruction limit `1e-4`;
- A9 bridge-identity limit `1e-6`;
- zero-norm exclusion `1e-14` exactly as in the frozen parent evaluator.

No threshold may be changed after execution.

## Canonical Repair08 scalar representation

For each of the exact 128 retained native k-groups, define on the native time grid

`varphi_theta(a,k) = a Q(a,k) theta_A(a,k) / k^2`.

The canonical Repair08 initial-slice scalar transfer is obtained by applying `PchipInterpolator(log(a), varphi_theta)` at `a_i` **after forming this composite on the native grid**.

An independent identity control is formed on the native grid as

`varphi_chi(a,k) = chi(a,k) - Q(a,k) alpha_A(a,k)`

and independently PCHIP-interpolated in `log(a)` to `a_i`.

The canonical theta route and independent chi route must agree at `a_i` with relative L2 <= `1e-10`.

The historical componentwise quantity

`PCHIP(chi) - PCHIP(Q) PCHIP(alpha_A)`

must be retained as a diagnostic only. It is not used to build the Repair08 scalar state.

No smoothing, fitting, clipping, rescaling, sign choice, source insertion, or alternate mode is allowed.

## State construction boundary

Repair08 must import the frozen C7A reconstruction implementation and reuse it for all unchanged fields. The only state quantities permitted to differ from the historical certified NPZ are:

- `phi`, because it is reconstructed from the new identity-preserving scalar transfer;
- `X_from_state`, because it is deterministically recomputed from the repaired `phi` using the frozen bridge definition.

All other per-scale state arrays written by the frozen reconstruction must reproduce the historical certified NPZ with relative L2 <= `1e-12`. Metadata `a_i`, scales, k-grid, and `h` must reproduce the historical artifact to floating-point identity or <= `1e-15` absolute/relative as appropriate.

A new NPZ may be written only if all Repair08 certification gates pass. The old C7A NPZ remains immutable.

## Repair08 gates

### R8_G1 — provenance and retained inputs

Require the frozen Repair07b result freeze, exact parent code blobs, exact dense trace provenance, exact certified C7A artifact provenance, 128 exact k groups, and compatible Repair01 coverage metadata.

### R8_G2 — A5 denominator recheck

Re-run the unchanged frozen A5 denominator audit on the retained dense trace and require its historical PASS classification with all gates true.

### R8_G3 — identity-preserving scalar construction

Require:

- native `theta_A` in all 128 k-groups;
- finite canonical and independent composite values;
- canonical theta route vs independent chi-composite route at `a_i` relative L2 <= `1e-10`.

Report the historical componentwise-vs-canonical relative L2 but do not gate on its size.

### R8_G4 — A6 time interpolation control

Build the primary repaired state with PCHIP in `log(a)` and its time-control state with linear interpolation in `log(a)`, including the scalar composite formed before time interpolation in each route. Apply the frozen A6 `2e-2` limit to every frozen `STATE` field using the same zero-norm rule.

### R8_G5 — A7 k interpolation control

Compare PCHIP-k and linear-k repaired states under the frozen A7 `2e-2` limit for every frozen `STATE` field using the same zero-norm rule.

### R8_G6 — A8 target-profile reconstruction

Run the unchanged frozen A8 target-profile reconstruction at 256 and 512 quadrature points and require all historical `1e-4` conditions.

### R8_G7 — A9 bridge identities

For the repaired primary state require the frozen bridge checks

- `X_from_chi` vs `X_from_state` <= `1e-6`;
- `E_from_class` vs `E_from_state` <= `1e-6`.

No bridge equation or tolerance may be changed.

### R8_G8 — A10 no-free-mode injection

Apply the frozen source audit to the Repair08 implementation and require no independent free-mode assignment, no clipping, exact frozen scale ladder, and single baryon target normalization.

### R8_G9 — unchanged-state regression

Against the historical certified C7A NPZ, require every reconstructed per-scale array except `phi` and `X_from_state` to agree within relative L2 `1e-12`. Report differences in `phi` and `X_from_state` without constraining them toward the historical representation.

### R8_G10 — claim boundary

No overwrite of the old C7A NPZ, no fitted coefficient/source, no sign flip, no point removal, no threshold change, no nonlinear evolution, and no finite eta.

## Terminal classifications

Allowed terminal classes are:

- `NL1C7A_REPAIR08_IDENTITY_PRESERVING_SCALAR_REPRESENTATION_CERTIFIED`;
- `NL1C7A_REPAIR08_SCALAR_IDENTITY_FAIL`;
- `NL1C7A_REPAIR08_TIME_INTERPOLATION_CONTROL_FAIL`;
- `NL1C7A_REPAIR08_K_INTERPOLATION_CONTROL_FAIL`;
- `NL1C7A_REPAIR08_RECONSTRUCTION_FAIL`;
- `NL1C7A_REPAIR08_BRIDGE_IDENTITY_FAIL`;
- `NL1C7A_REPAIR08_FREE_MODE_INJECTION_FAIL`;
- `NL1C7A_REPAIR08_STATE_REGRESSION_FAIL`;
- `NL1C7A_REPAIR08_IMPLEMENTATION_FAIL`.

A Repair08 CERTIFIED result certifies only a new eta=0 identity-preserving C7A initial-state representation. It does not imply B4 PASS, nonlinear stability, finite-eta viability, or observational detection. Only after a certified Repair08 artifact may a separately preregistered B4 retest consume that new artifact under the unchanged B4 thresholds.
