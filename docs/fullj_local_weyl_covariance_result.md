# Full-J local Weyl covariance derived result

Date: 2026-09-11

## Classification

```text
FULLJ_LOCAL_WEYL_COVARIANCE_DERIVED_COMPLETE
STATIC_SNAPSHOT_ONLY=True
PHASE_ALIGNED_TANGENT_BASIS_ONLY=True
COSMOLOGICAL_RANDOM_PHASE_ENSEMBLE=False
EVOLVING_FLRW_WEYL_POWER_LICENSED=False
ACT_LIKELIHOOD_LICENSED=False
OBSERVATIONAL_CLAIM_LICENSED=False
```

This result is a deterministic post-processing diagnostic of the already locked full-J mode-coupling Jacobian. It is not an independent preregistered physics test.

## Algebraic health

For all 27 locked backgrounds and both covariance probes:

```text
max Hermiticity relative residual = 6.934599501705196e-17
min covariance eigenvalue / max |eigenvalue| = 4.797206627584994e-09
```

Thus every constructed local Weyl covariance is Hermitian and positive semidefinite well inside the frozen `1e-12` algebraic tolerance.

## Unit tangent covariance

For `C_S proportional to I` in the 13 certified phase-aligned tangent coordinates, the full mode-coupled to diagonal-only Weyl-power ratio over all backgrounds and output coordinates is

```text
min    = 1.0026036406535723
median = 2.7354708124481193
max    = 403.6490388083432
```

The corresponding off-diagonal power fraction is

```text
min    = 0.0025968793130205503
median = 0.6344322171344806
max    = 0.9975226003189498
```

Thus even before weighting by the frozen source spectrum, the median local tangent-coordinate variance is already dominated by off-diagonal response.

## Frozen-source spectral-shape covariance

Using diagonal tangent-coordinate variance proportional to the locked squared source amplitudes `|S_j|^2`, with only the global normalization divided out,

```text
full / diagonal power ratio:
min    = 1.0113406036637824
median = 1.2283521506206572
max    = 10468.423016594325

off-diagonal power fraction:
min    = 0.011213436524449616
median = 0.1859012096044903
max    = 0.9999044746282784
```

The broad median is smaller than in the unit probe because the locked source spectrum weights tangent directions non-uniformly. Nevertheless the node region can become overwhelmingly off-diagonal.

## z=0.25, k_out=0.6 Mpc^-1 node

For the nine co-primary branches at the previously identified source node:

### Unit tangent covariance

```text
full / diagonal power ratio:
min    = 2.9310953815082557
median = 3.8649169766598446
max    = 12.30253772035902

off-diagonal fraction:
min    = 0.6588306179632308
median = 0.7412622299420712
max    = 0.9187159574121738
```

### Frozen-source spectral shape

```text
full / diagonal power ratio:
min    = 5459.746972489549
median = 6508.701190011246
max    = 10468.423016594325

off-diagonal fraction:
min    = 0.9998168413289042
median = 0.9998463595161605
max    = 0.9999044746282784
```

Therefore, in the certified local phase-aligned tangent basis, the Weyl variance at the `z=0.25, k_out=0.6 Mpc^-1` node is effectively supplied by other tangent directions once the locked source spectral shape is used. The scalar/diagonal approximation misses the node response by factors of several thousand.

## Interpretation

This is the covariance-level version of the locked Jacobian result:

\[
\text{source node}+\text{off-diagonal full-J response}
\rightarrow
\text{finite output variance not represented by a scalar transfer multiplier}.
\]

It strengthens the methodological conclusion that a scalar `T(k,z)` is not an adequate representation of the tested nonlinear full-J response around these frozen backgrounds.

It does **not** yet establish a cosmological random-phase Weyl power spectrum. The current 13 tangent coordinates are the phase-aligned real perturbation directions calibrated around each deterministic nonlinear background. A true cosmological statistical prediction requires response information over phase/background realizations or a more complete nonlinear stochastic evolution.

## Next blocker

The next genuinely new eta=0 calculation, if pursued toward lensing, is a **phase/background ensemble response test**, not another kmax or local-UV test. Its purpose would be to determine whether the local mode-coupled covariance is stable under changes of the underlying source phases/background realization.

No ACT likelihood should be run before that statistical generalization and the evolving Weyl/lensing closure are certified.
