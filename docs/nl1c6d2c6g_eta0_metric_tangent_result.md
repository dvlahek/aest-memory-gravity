# NL1C6D2C6G eta=0 direct metric tangent calibration result

## Classification

`NL1C6D2C6G_ETA0_DIRECT_METRIC_TANGENT_CALIBRATION_PASS`

The preregistered eta=0 direct-memory metric-tangent calibration passed all frozen gates G1--G6. This result does not alter the historical `NL1B_SECOND_ORDER_DYNAMICAL_CLOSURE_INCOMPLETE` classification and does not license observational inference.

## Provenance and zero-coupling identity

Executed implementation HEAD: `b293f2fc3ad117e1802e7f7a6f8ef1343b28ba3b`.

All required ancestors were present. The physical memory metric source vanished exactly at eta=0, and all 27 completion members reproduced the eta=0 retained trajectory with zero state and E differences.

## Direct-bath convergence

The direct tan--Gauss--Legendre stress/metric tangent was evaluated with order 256 and checked against order 512 on the frozen sentinels. The worst relative differences were:

- `sigma=+1|kind=simple|beta0=0.1`: `1.102290176101e-07`
- `sigma=+0|kind=exponential|beta0=0.5`: `4.725454805213e-08`
- `sigma=-1|kind=sharp|beta0=1`: `3.466752713858e-08`

All controls passed.

## Direct-source calibration

The global one-way direct-memory calibration against 1% of the frozen baseline CLASS Psi RMS is

`FEEDBACK_ETA_CAP_1PCT_BASE_PSI = 2.5792572200217887e-17`.

The preregistered direct-source ladder is

`{6.448143050054472e-18, 1.2896286100108944e-17, 2.5792572200217887e-17}`.

The limiting member is `sigma=-1|kind=simple|beta0=1` at z=0.2. At that checkpoint,

- `Psi_hat_rms_per_eta = 2.6664137551877785e9`
- `Phi_hat_rms_per_eta = 9.273378798742732e8`
- `Weyl_hat_rms_per_eta = 1.7390758753135054e9`
- baseline `Psi_rms = 6.877366929633488e-06`.

For that member the corresponding direct-only calibration scales are approximately 1%, 10%, and 100% of the frozen baseline Psi RMS at eta = `2.5792572200217887e-17`, `2.579257220021789e-16`, and `2.5792572200217885e-15`.

## Interpretation and scope

This number is a **direct-memory-source calibration**, not a final physical bound on eta. The D2C6G metric projection holds the non-memory AeST/matter response frozen. It therefore does not yet include the induced coupled eta-tangent response of alpha, chi, E, matter, and the metric potentials themselves. Such induced response may amplify or partially cancel the direct component.

Accordingly:

- `SELF_CONSISTENT_FEEDBACK_LADDER_LICENSED=True` only in the sense that a separately preregistered coupled weak-field eta-tangent/feedback stage may now be constructed.
- `OBSERVATIONAL_STEP_LICENSED=False`.
- The direct-only cap must not be quoted as an observational or final theory constraint on eta.

## Next required step

Construct and certify the full coupled eta=0 AeST weak-field tangent. It must combine the already certified nonlinear memory scalar-current tangent with the corrected direct memory metric source and the exact AeST metric/matter response, including the feedback term in `alpha' = a(E-Psi)`. No ad hoc GR/Poisson replacement is permitted. A finite-positive-eta self-consistent feedback ladder may be run only after that coupled tangent is certified.