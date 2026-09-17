# NL1C7B4 Repair07a — implementation lock

## Locked provenance

- Preregistration commit: `6a7971661ff612a1928413a3a4dc8ca31373dcf2`
- Preregistration blob: `9a3a1742432bb5e93b51409dfdc7672ac1cfbf13`
- Repair07a implementation commit: `9fa982e454d0df4178e113e64d27cf9376aeb87f`
- Repair07a evaluator blob: `59cac7b5105bc779c27ce1daea9e1a52fe582cae`
- Parent Repair07 evaluator blob: `ef591df4e92b262963e928218e3932943ab9e45c`
- Frozen B4 evaluator blob: `8559120dc273be3174eca130ca313ed6ff5acb25`
- Repair05 evaluator blob: `34fd22c73171fce5e32920a94d71d05de61521f6`

## Retained artifacts

- Repair06 artifact: `10500046102`
  - digest: `sha256:b589d1f595782d793cdcc0f6cde1de1e4df1994b32f27ac64ee253fd665b4b1d`
- Certified C7A state artifact: `10481526695`
  - digest: `sha256:c2ede2e602e35bbd52afdc0a5eee22cb1bf5c6efc2e1063bf8f2b91a0554fb6c`
- Dense C7A trace artifact: `10469031693`
  - digest: `sha256:193325536405f9a21a238f5fbe71a772d2484a096dcbfec3d6007e825cc38f70`

## Frozen numerical/science settings

- `eta = 0`
- scales: `[5.0, 10.0, 20.0] h^-1 Mpc`
- radial resolutions: `[256, 512]`
- state reproduction limit: `1e-12`
- algebra identity limit: `1e-10`
- inherited C7A Fourier envelope: `2e-2`
- historical B4 raw-constraint limit: `1e-7` unchanged and not a Repair07a pass gate
- historical Repair05/06 linear-interface limit: `1e-5` unchanged and not a Repair07a pass gate

## Sole Repair07a change

The only implementation difference from frozen Repair07 is the harness bridge that interpolates the already-retained native dense-trace `theta_A` to `a_i` using the same `PchipInterpolator(log(a), theta_A)` construction used by frozen B4 for its exported fields.

The parent Repair07 evaluator remains byte-for-byte unchanged.

## Locked terminal classes

- `NL1C7B4_REPAIR07A_COVARIANT_FOURIER_BRIDGE_DIAGNOSTIC_PASS`
- `NL1C7B4_REPAIR07A_COVARIANT_FOURIER_INTERFACE_MISMATCH`
- `NL1C7B4_REPAIR07A_IMPLEMENTATION_FAIL`

Diagnostic PASS is not B4 PASS.

## Claim boundary

No state replacement, coefficient fit, sign flip, source insertion, point removal, threshold change, nonlinear evolution, or finite-eta execution is permitted.
