# Full-J static snapshot Weyl operator result

Date: 2026-09-11

## Classification

```text
FULLJ_STATIC_SNAPSHOT_WEYL_OPERATOR_IDENTITY_PASS
STATIC_SNAPSHOT_WEYL_MAPPING_LICENSED=True
EVOLVING_FLRW_WEYL_POWER_LICENSED=False
ACT_LIKELIHOOD_LICENSED=False
OBSERVATIONAL_CLAIM_LICENSED=False
```

## Input

Locked parent classification:

```text
FULLJ_MODE_COUPLING_JACOBIAN_NODE_COUPLING_SUPPORTED
```

The exact locked NPZ used for this identity validation has SHA256:

```text
e59478e8068107f6b927ff94946395730d2a6cbea064e73bb6811568468c7882  fullj_mode_coupling_jacobian.npz
```

It contains 27 complete local response matrices of shape `13 x 13` on the frozen k grid.

## Frozen identity

Within the same D1A static/fixed-a dust reduction used by the full-J snapshot solver,

\[
\Psi=\Phi,
\]

and with the repository Weyl convention

\[
W=\Phi+\Psi,
\]

therefore

\[
\boxed{K^W=2K^\Phi}.
\]

## Regression result

Applying this identity to all 27 locked matrices gives

```text
backgrounds = 27
scale_residual = 0.0
max_abs_slope_difference = 3.1086244689504383e-15
max_abs_row_coupling_difference = 0.0
```

The fitted high-k diagonal slopes are unchanged to roundoff:

```text
Phi:  min    = -2.0815502111982096
      median = -2.0056427140938835
      max    = -1.9150696997181147

Weyl: min    = -2.0815502111982087
      median = -2.0056427140938830
      max    = -1.9150696997181158
```

Thus the static snapshot Weyl response inherits the locked ultraviolet behavior

\[
K^W_{ii}(k)\propto k^{-2}
\]

and exactly the same off-diagonal coupling ratios and node-coupling interpretation.

## Interpretation limit

This PASS is an exact transformation of the already locked static full-J Jacobian. It is not an independent evolving-FLRW calculation and does not construct a cosmological Weyl power spectrum.

The next eta=0 problem is statistical: propagate a controlled source covariance through the mode-coupled Weyl operator,

\[
C^W=K^W C^S K^{W\dagger},
\]

without replacing the operator by a scalar transfer function. An observational lensing projection remains blocked until a statistically meaningful source/ensemble prescription and the required evolving cosmological closure are certified.
