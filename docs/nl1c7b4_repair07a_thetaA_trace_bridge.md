# NL1C7B4 Repair07a — theta_A trace-bridge implementation repair

## Status

Locked before Repair07a implementation. This repair follows the failed local execution of Repair07, which terminated before producing a science classification because the Repair07 Fourier audit requested `tv['theta_A']` although the frozen B4 `at_ai()` bridge only exports `FIELDS+BG` and `theta_A` is not in `FIELDS`.

## Parent failure

Repair07 evaluator blob: `ef591df4e92b262963e928218e3932943ab9e45c`.

Observed local termination:

```text
KeyError: 'theta_A'
```

The failure occurred in `fourier_audit()` before the Fourier residual gate was evaluated. It is therefore an implementation failure and is not a physics result.

## Frozen inputs and physics

Repair07a must use exactly the same retained inputs, equations, radial resolutions, scales, eta value, thresholds, and claim boundaries as Repair07:

- Repair06 artifact `10500046102`, digest `sha256:b589d1f595782d793cdcc0f6cde1de1e4df1994b32f27ac64ee253fd665b4b1d`.
- Certified C7A artifact `10481526695`, digest `sha256:c2ede2e602e35bbd52afdc0a5eee22cb1bf5c6efc2e1063bf8f2b91a0554fb6c`.
- Dense C7A trace artifact `10469031693`, digest `sha256:193325536405f9a21a238f5fbe71a772d2484a096dcbfec3d6007e825cc38f70`.
- `eta = 0`.
- scales `5, 10, 20 h^-1 Mpc`.
- radial resolutions `Nr = 256, 512`.
- state reproduction limit `1e-12`.
- algebra identity limit `1e-10`.
- inherited C7A Fourier envelope `2e-2`.
- historical B4 raw-constraint limit `1e-7` unchanged and not a Repair07a pass gate.
- historical Repair05/06 linear-interface limit `1e-5` unchanged and not a Repair07a pass gate.

No state artifact may be modified or replaced.

## Sole permitted implementation change

The native dense trace already contains `theta_A`; Repair07 uses it directly as `g['theta_A']` in the native composite identity. The frozen B4 helper `at_ai()` does not export it because `theta_A` is not part of B4 `FIELDS`.

Repair07a may therefore add exactly one bridge operation:

1. call the unchanged frozen B4 `at_ai(gs)`;
2. for every native k-group `g`, interpolate the existing native `g['theta_A']` to `a_i` using the same independent variable `log(a)` and the same `PchipInterpolator` used by B4 `at_ai()`;
3. append that vector as `tv['theta_A']`;
4. execute the unchanged Repair07 evaluator logic.

No alternate interpolation family, smoothing, fitting, clipping, rescaling, sign change, species substitution, reconstructed velocity, or inferred missing source is allowed.

## Gates

Repair07a inherits all Repair07 science gates unchanged. In addition, the harness bridge must satisfy:

- the dense trace contains native `theta_A` for every one of the 128 k-groups;
- `theta_A(a_i)` is finite for every k;
- the bridge is produced only by PCHIP in `log(a)` from the retained dense trace.

The Repair07a wrapper may relabel the three terminal Repair07 classifications only to preserve provenance:

- `NL1C7B4_REPAIR07A_COVARIANT_FOURIER_BRIDGE_DIAGNOSTIC_PASS`;
- `NL1C7B4_REPAIR07A_COVARIANT_FOURIER_INTERFACE_MISMATCH`;
- `NL1C7B4_REPAIR07A_IMPLEMENTATION_FAIL`.

A diagnostic PASS does not imply B4 initial-constraint PASS.

## Claim boundary

Repair07a is a harness-only repair. It must not:

- modify the official C7A NPZ;
- write a replacement state NPZ;
- change any physical coefficient, sign, source, threshold, scale, radial resolution, or eta;
- remove radial points;
- fit or insert an unrepresented standard-sector source;
- execute nonlinear evolution;
- execute finite eta;
- claim B4 PASS.

If Repair07a reaches a terminal science classification, that result becomes the official outcome of this harness repair. The historical Repair07 local crash remains preserved as an implementation failure and must not be rewritten as a completed science result.
