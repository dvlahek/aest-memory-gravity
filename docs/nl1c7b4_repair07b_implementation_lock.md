# NL1C7B4 Repair07b — implementation lock

## Locked history

- Repair07a result-freeze commit: `a7bf8abe83e3cc50ecdf23ab291ed5df673b20c5`.
- Repair07b preregistration commit: `463bf43a41b47c7a321adf195a36acafc990df9e`.
- Repair07b preregistration blob: `7abf9c060dab3da6d3e1ee3d535e848702c6232b`.
- Repair07b implementation commit: `82090bc98bf96276b9f7b12c2d3a9d969e7ed5fb`.
- Repair07b evaluator blob: `1b9c4f6c8cb62f1d4e6dc8cf818941288c64ed1b`.

## Locked parent code

- Repair07a evaluator blob: `59cac7b5105bc779c27ce1daea9e1a52fe582cae`.
- Repair07 evaluator blob: `ef591df4e92b262963e928218e3932943ab9e45c`.
- Repair05 evaluator blob: `34fd22c73171fce5e32920a94d71d05de61521f6`.
- frozen B4 evaluator blob: `8559120dc273be3174eca130ca313ed6ff5acb25`.

## Retained artifacts

- Repair06 artifact `10500046102`, digest `sha256:b589d1f595782d793cdcc0f6cde1de1e4df1994b32f27ac64ee253fd665b4b1d`.
- Certified C7A artifact `10481526695`, digest `sha256:c2ede2e602e35bbd52afdc0a5eee22cb1bf5c6efc2e1063bf8f2b91a0554fb6c`.
- Dense C7A trace artifact `10469031693`, digest `sha256:193325536405f9a21a238f5fbe71a772d2484a096dcbfec3d6007e825cc38f70`.

## Frozen science settings

- `eta = 0`.
- scales `[5.0, 10.0, 20.0] h^-1 Mpc`.
- radial resolutions `[256, 512]`.
- state reproduction limit `1e-12`.
- algebra identity limit `1e-10` unchanged.
- inherited C7A Fourier envelope `2e-2` unchanged.
- historical B4 raw-constraint limit `1e-7` unchanged and not a Repair07b pass gate.
- historical Repair05/06 linear-interface limit `1e-5` unchanged and not a Repair07b pass gate.

## Sole Repair07b change

Repair07b changes only the domain of the scalar algebra gate from the full 179-time text-serialized trace to the B4 initial slice `a_i=0.02`. The gate remains `<=1e-10` and uses the same retained dense trace and PCHIP(log(a)) bridge.

The Repair07a full-trace value must remain in the output as a historical non-gating diagnostic and must remain marked as failed under the old Repair07a definition.

## Locked terminal classes

- `NL1C7B4_REPAIR07B_INITIAL_SLICE_BRIDGE_DIAGNOSTIC_PASS`
- `NL1C7B4_REPAIR07B_COVARIANT_FOURIER_INTERFACE_MISMATCH`
- `NL1C7B4_REPAIR07B_IMPLEMENTATION_FAIL`

A diagnostic PASS is not B4 PASS and licenses only a separately preregistered identity-preserving scalar-representation repair.
