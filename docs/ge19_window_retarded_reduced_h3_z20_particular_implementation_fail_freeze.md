# GE19 first locked execution — implementation-failure freeze

## Status

The first locked local GE19 execution terminates before any Stage-A science classification with

`GE19_WINDOW_RETARDED_REDUCED_H3_Z20_PARTICULAR_IMPLEMENTATION_FAIL`.

This is not a Stage-A reduced-H1 FAIL and not an H3/Z20 FAIL.

No Z20 state was constructed.

## Frozen execution provenance

Locked runner commit:

`1ef0785d502a2c7cc6999a8c81cdeeb8c77bfe94`.

Implementation lock commit:

`f8ee1f794052791a46ad72ddea1bf00b4df24e3b`.

The local run reports:

- `GE19_LOCK_PASS`;
- `GE19_LOCAL_INPUTS_PRESENT`.

Uploaded first-run files:

- full GE19 log:
  - bytes: `6072`;
  - SHA-256:
    `f325c29ca464c11b31935bd493a663d8883b6ddb9951f8030bffac90e7c89395`;
- local runner log:
  - bytes: `6237`;
  - SHA-256:
    `4c49f2056a60bb8da94f351b4e09b1ca08562d1d71422e38aeea65e6a34c8819`.

## Failure

Before the first reduced-H1 sparse solve, the physical-parameter GE06 linear operator evaluation emits repeated overflows in symbolic terms containing the Exp-background factor.

The terminal exception is

`RuntimeError('reduced H1 sparse solve failed C=C_min m=3: Factor is exactly singular')`.

Because the assembled matrix contains non-finite coefficients generated before LU factorization, the singular-factorization message is not evidence of a physical or gauge singularity.

## Root cause

The frozen GE06 generator is analytically correct. Its original validation used benign representative audit parameters

- `Q0=0.2`;
- `Z0=0.7`.

GE19 evaluates the same symbolic coefficient functions on the physical frozen Exp model

- `Q0=1e-4 Mpc^-1`;
- `Z0=1e-17 Mpc^-1`;
- `K2=9500`.

The generated expressions contain factors equivalent to

[
expleft[left(rac{Q_b-Q_0}{Z_0}ight)^2ight].
]

In the physical Exp background, `Q_b` and `Q0` differ only by an O(Z0) quantity. Reconstructing the dimensionless background coordinate by floating-point subtraction of these two nearly equal Mpc^-1 numbers is numerically ill-conditioned.

The pinned CLASS background implementation does not use that subtraction. It evolves the conserved `K_Q`, solves the Exp dimensionless coordinate `Z` stably, and then evaluates

[
Q=Q_0+Z_0 Z,
]

[
K_Q=4K_2 Z_0 Z e^{Z^2},
]

[
K_{QQ}=4K_2 e^{Z^2}(1+2Z^2).
]

Thus the GE19 failure is a numerical background-coordinate reconstruction defect in the component-generator evaluation path.

## Licensed Repair01

A single Repair01 is licensed before any GE19 science output.

Repair01 may change only the physical Exp-background coordinate supplied to the already frozen GE06 `f_c1/f_c2` coefficient functions.

The stable coordinate must be reconstructed from the frozen GE15 background state using the exact CLASS background identities.

A permitted route is:

[
K_Q=rac{3(ho_{m dark}+p_{m dark})}{Q_{m trace}},
]

then solve the exact Exp relation

[
rac{K_Q}{4K_2Z_0}=Z e^{Z^2}
]

using the same positive-branch Newton equation as CLASS,

[
y+rac12ln y=ln x,qquad y=Z^2.
]

Then use

[
Q_{m action}=Q_0+Z_0Z
]

inside the symbolic generator.

Repair01 must independently reconstruct and report

[
p=K/3,qquad
ho=(QK_Q-K)/3,qquad
c_{m ad}^2=K_Q/(QK_{QQ})
]

against the frozen GE15 background values.

## Forbidden changes

Repair01 may not change:

- GE06 or GE07 frozen source-generator files;
- the reduced-H1 equations;
- the H3 equation or signs;
- any Stage-A or Stage-B threshold;
- beta0 values;
- C values;
- modes, phases or amplitudes;
- Nx/Nt controls;
- gauge;
- initial matching surface;
- window-retarded Z20 convention;
- matter model;
- historical GE19 implementation-failure classification.

## Claim boundary

This execution reached no valid reduced-H1 state and no Z20 state.

Therefore it carries no physical conclusion about H1 reclosure, H3, or Z20.
