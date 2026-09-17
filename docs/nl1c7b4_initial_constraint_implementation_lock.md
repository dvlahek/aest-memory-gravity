# NL1C7B4 implementation lock — raw initial-constraint certification

Status: **IMPLEMENTATION LOCKED BEFORE OFFICIAL B4 RUN**

Pre-data parent: `336c219f713fe5f573ed25223f9c723956869038`.

Implementation:

- `nl1c7b/initial_constraint_certification.py`
- frozen blob: `8559120dc273be3174eca130ca313ed6ff5acb25`

The implementation reproduces the official C7A 256-point state from the retained dense trace and independently reconstructs the 512-point radial control state. It uses the preregistered ninth-point/eighth-order radial derivative operator.

Before any lapse/shift residual is interpreted, it evaluates the **exact nonlinear C6 scalar dictionary**

`Q_C6 = cosh(u) sigma + sinh(u) phi_r/L`

with `sigma = phidot` in the frozen `N=1,b=0` initial gauge. The frozen Exp sector uses

`Z=(Q_C6-Q0)/Z0`, `K=2 K2 Z0^2 [exp(Z^2)-1]`.

No linearization of `Q_C6`, clipping/saturation of `Z`, replacement of the Exp branch, constraint projection, state correction, or fitted source is permitted.

If the exact frozen Exp contribution is outside the finite float64 evaluation domain (`Z^2 > log(float64_max)`) on the certified state, the implementation terminates under the already preregistered classification

`NL1C7B4_CONSTRAINT_IMPLEMENTATION_INCOMPLETE`

before trajectory execution. This is a numerical/action-domain guard, not a modified science threshold.

The official run must verify the preregistration ancestry, this exact implementation blob, the C6/B1 source blobs, and the exact C7A and B3 Repair01 artifact digests before execution.
