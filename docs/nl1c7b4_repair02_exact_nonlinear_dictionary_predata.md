# NL1C7B4 Repair02 pre-data — exact nonlinear Q-dictionary completion

Status: **PRE-DATA / LOCKED BEFORE REPAIR02 EVALUATION**

Pre-result classification: `NL1C7B4_REPAIR02_PREDATA_EXACT_NONLINEAR_Q_DICTIONARY_COMPLETION`.

## Motivation

NL1C7A certified a unique eta=0 linear growing-mode spherical state. NL1C7B4 Repair01 then proved that the naive promotion of that linear state to the exact nonlinear C6 scalar invariant fails all 54 frozen raw-constraint cases. The failure is driven by using the linear substitution `sigma = Q_bg + deltaQ_C7A` inside the exact nonlinear invariant

`Q = cosh(u) sigma + sinh(u) phi_r/L`.

The purpose of Repair02 is to complete only this dictionary relation exactly, with no new physical mode and no constraint fit.

## Frozen parents

- C7A certified state: run `35183893359`, artifact `10481526695`, SHA256 `c2ede2e602e35bbd52afdc0a5eee22cb1bf5c6efc2e1063bf8f2b91a0554fb6c`.
- Dense trace: run `35149865129`, artifact `10469031693`, SHA256 `193325536405f9a21a238f5fbe71a772d2484a096dcbfec3d6007e825cc38f70`.
- B3 direct homogeneous background PASS: run `35196289353`, artifact `10486515383`, SHA256 `12f3157fa05e7c0c4fc431005a506cbfa6347aa78dafd1a1dedf4328b193d3ec`.
- B4 raw-domain historical implementation result: run `35211367954`, artifact `10492575332`, SHA256 `9fdf56fd2c2b224c934cc15be31d5d27076971b50ab2961849c151939d60ef74`.
- B4 Repair01 raw constraint FAIL: run `35212527939`, artifact `10493461020`, SHA256 `0cd7ff857d2965915176563341a18d2979f82ebe3ea59be090459030018c1aa0`.
- B4 Repair01 result freeze commit: `c158cbaa8bcfbd3bec9feb0a3449b66aec0e63d0`.

All C6 physical constants, all nine Y branches, all three scales, both radial grids, and the `1e-7` constraint threshold remain unchanged.

## Frozen nonlinear completion

Let the certified linear scalar invariant target be

`Q_target(r) = Q_bg + deltaQ_C7A(r)`,

where `Q_bg` is the already certified stable Exp-background inversion from KQ and `deltaQ_C7A` is exactly the C7A `phidot_minus_Q` profile generated from the frozen growing-mode transfer.

In the C7 gauge `N=1`, `b=0`, the exact C6 invariant is

`Q = cosh(u) phidot + sinh(u) phi_r/L`.

Repair02 changes only `phidot`, uniquely by exact inversion:

`phidot_completed = [Q_target - sinh(u) phi_r/L] / cosh(u)`.

No other field is changed.

This completion is not a free-mode choice. Given the frozen `Q_target`, `u`, `phi`, and `L`, it is algebraically unique. Its difference from the C7A linear substitution begins at second order in perturbations:

`phidot_completed - Q_target = -u phi_r/L - (u^2/2) Q_target + O(delta^3)`.

Thus the certified first-order growing mode is preserved.

## Forbidden operations

Repair02 must not modify `L`, `R`, `Ldot`, `Rdot`, `u`, `udot`, `phi`, `delta_b`, or `dust_vr`.

It must not:

- solve the Hamiltonian or momentum constraint for a field,
- fit any amplitude, phase, radial function, or background constant,
- change `delta0`, scale, radial domain, Y branch, beta0, K(Q), J(Y), matter source, or standard background content,
- clip or linearize Q or K,
- smooth/filter the state,
- change the `1e-7` gate.

## Repair02 gates

### R2-G1 — exact target preservation

For every scale and both grids, after completion require pointwise

`Q_exact_completed = cosh(u) phidot_completed + sinh(u) phi_r/L`

to reproduce `Q_target` with maximum normalized error `<=1e-12`, using scale `max(|Q_target|, |Q_bg|, 1e-300)`.

### R2-G2 — first-order preservation

The completed `phidot` must differ from the original C7A linear `Q_target` only by the exact algebraic nonlinear correction above. No independently supplied radial correction is allowed. The implementation must report the relative L2 correction and the maximum absolute correction, but no post-result limit is imposed on those diagnostics.

### R2-G3 — Exp-domain restoration

For all scales and grids, exact completed `Z=(Q_exact_completed-Q0)/Z0` and the corresponding Exp K(Q), KQ, and KQQ evaluations must be finite without clipping or log-domain substitution.

### R2-G4 — unchanged raw constraints

Using the exact same frozen B4 action-term normalization and original `1e-7` threshold, evaluate Hamiltonian and radial momentum constraints for every one of the `54` frozen cases.

PASS requires both maxima `<=1e-7` for every case.

### R2-G5 — grid control and no selection

Both Nr=256 and Nr=512 must be retained. All 9 Y branches and all 3 scales remain co-primary. No case may be dropped or selected after result inspection.

## Classification

If R2-G1 through R2-G5 all pass:

`NL1C7B4_REPAIR02_EXACT_NONLINEAR_DICTIONARY_CONSTRAINT_PASS`.

If G1-G3 pass but one or more unchanged raw constraints exceed `1e-7`:

`NL1C7B4_REPAIR02_DICTIONARY_COMPLETED_RAW_CONSTRAINT_FAIL`.

If the exact nonlinear dictionary cannot be reproduced or the Exp sector remains non-finite:

`NL1C7B4_REPAIR02_DICTIONARY_COMPLETION_IMPLEMENTATION_FAIL`.

A Repair02 constraint PASS would license a separately preregistered short eta=0 constraint-propagation evolution. It would not license the long collapse run directly.
