# NL1C7B4 Repair01 pre-data — log-domain exact Exp constraint audit

Status: **PRE-DATA / LOCKED BEFORE REPAIR01 SCIENCE EVALUATION**

Historical parent: official NL1C7B4 run `35211367954`, classification `NL1C7B4_CONSTRAINT_IMPLEMENTATION_INCOMPLETE`, artifact `10492575332`, SHA256 `9fdf56fd2c2b224c934cc15be31d5d27076971b50ab2961849c151939d60ef74`, result freeze `d42e22945e2ca6acaf412741198e4b8c6659598a`.

## Purpose

The historical B4 run reproduced the certified C7A state but could not directly evaluate the frozen Exp Q-sector because `exp(Z^2)` overflowed float64. Repair01 changes **only the numerical representation of the same exact Exp contribution**. It does not change the state, action, `Z0`, Q dictionary, Y family, radial grids, normalization, or the original NL1C7 `1e-7` constraint gate.

## Frozen inputs

All B4 provenance, scale ladder `R_sigma={5,10,20} h^-1 Mpc`, `Nr={256,512}`, `a_i=0.02`, 9-point eighth-order radial derivative, B1 dust source, B3 direct homogeneous background, nine C6 Y branches, and C7A state reconstruction remain exactly as in `docs/nl1c7b4_predata_initial_constraint_certification.md`.

The exact nonlinear scalar remains

`Q_C6 = cosh(u) sigma + sinh(u) phi_r/L`,

with `sigma=phidot` at `N=1,b=0`, and

`Z=(Q_C6-Q0)/Z0`,

`K=2 K2 Z0^2 [exp(Z^2)-1]`,

`K_Q=4 K2 Z0 Z exp(Z^2)`.

No linearized Q, clipping, saturation, asymptotic replacement of the physics, or modified `Z0` is allowed.

## Repair01 numerical representation

All non-Exp action contributions are evaluated directly from the frozen reduced action and must remain finite in float64. The Exp `K(Q)` lapse and shift contributions are represented by sign and logarithmic magnitude, factoring out `exp(Z^2)` algebraically before numerical evaluation.

For the lapse constraint, the exact K-sector contribution in the frozen gauge is

`C_H,K = 2 L R^2 [K - cosh(u) phidot K_Q]`.

For the shift constraint,

`C_M,K = -2 L R^2 cosh(u) phi_r K_Q`.

These identities must be verified symbolically from the same `2 N L R^2 K(Q)` action term before numerical use.

## Rigorous normalized-residual bound

For either constraint write the exact additive decomposition

`C = C_K + sum_{j!=K} C_j`.

Let

`A=|C_K|`, `B=sum_{j!=K}|C_j|`.

The original B4 normalized residual is

`epsilon=|C|/(A+B)`.

Repair01 may evaluate the mathematically rigorous triangle lower bound

`epsilon >= max(0,(A-B)/(A+B))`.

When `A` is stored logarithmically, the ratio `B/A` is evaluated as `exp(log(B)-log(A))` without materializing `A`. No threshold-dependent approximation is allowed.

If this lower bound exceeds the unchanged `1e-7` gate at any non-center radius, the corresponding raw constraint is rigorously proven to fail even though its absolute Exp magnitude cannot be materialized. No cancellation from any finite non-K term can then restore the gate.

## Y branches and grid control

All nine frozen Y branches (`Simple`, `Exponential`, `Sharp` x `beta0={1,0.5,0.1}`) are evaluated. The log-domain K term is common to all Y branches; all Y-dependent non-K terms are nevertheless included in `B` separately for each branch.

Both `Nr=256` and `Nr=512` are evaluated for all three frozen scales. The center is excluded exactly as in the original G3 gate.

## Classification

- If the rigorous lower bound proves `max epsilon_H > 1e-7` or `max epsilon_M > 1e-7` for any frozen case: `NL1C7B4_REPAIR01_RAW_INITIAL_CONSTRAINT_FAIL`.
- If all exact normalized residuals/bounds remain `<=1e-7` and all original B4 gates pass: `NL1C7B4_REPAIR01_RAW_INITIAL_CONSTRAINT_PASS`.
- If the non-Exp action cannot be generated/evaluated consistently or the log-domain identities fail: `NL1C7B4_REPAIR01_LOG_DOMAIN_IMPLEMENTATION_FAIL`.

A FAIL does not imply the nonlinear AeST theory itself is inconsistent. It means the **unmodified linear C7A growing-mode state** is not an admissible raw initial state of the full nonlinear spherical action at the frozen finite amplitude. Any subsequent nonlinear initial-data completion or constraint projection must be separately preregistered and may not rewrite this historical result.
