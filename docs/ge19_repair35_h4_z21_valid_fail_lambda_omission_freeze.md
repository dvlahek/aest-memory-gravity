# GE19 Repair35 H4/Z21 valid FAIL — Lambda omission localization freeze

## Status

The first valid Repair35 science execution is frozen exactly as emitted.

Classification:

`GE19_REPAIR35_DIRECT_BILINEAR_MATCHED_SHIFT_H4_Z21_FAIL`.

Repair35 is not relabelled.

Its direct GE06/GE07 bilinear Q-cross repair worked. The remaining shift failure
is localized to a separate H4 implementation omission: the Lambda sector used
in the certified reduced background and lower-order parents was not carried
into the Repair35 H4 linear operator or mixed quadratic source.

## Frozen local artifacts

Science JSON:

- SHA-256:
  `5b9a785d3dc1005968e91d8e5a36646001d2fea788c9e1c4a0130c4c450d4b93`;
- bytes:
  `460263`.

Science NPZ:

- SHA-256:
  `c2d00ba5395134752222cef197e05d074824f94599cfcfb0d20d53925273a59a`;
- bytes:
  `26026415`.

Inner FULL log:

- SHA-256:
  `5b9a785d3dc1005968e91d8e5a36646001d2fea788c9e1c4a0130c4c450d4b93`;
- bytes:
  `460263`.

Outer local runner log:

- SHA-256:
  `00be66cdaa28ebff66de8628650ee9e62ac1d61853c01134c6cad41dfa131ff7`;
- bytes:
  `464720`.

Terminal marker:

`GE19_REPAIR35_VALID_SCIENCE_FAIL_FREEZE_REQUIRED`.

## What Repair35 closed successfully

Direct quadratic cross:

- exact symbolic polarization identity:
  PASS;
- numerical swap symmetry relative L2:
  `5.806093345923313e-15`;
- old balanced-polarization difference, report only:
  `6.148797801436034e-10`.

Source controls:

- DY2 Nx1024/Nx2048:
  `2.9384475883958845e-05`;
- total H4 spatial control:
  `4.7562677781547786e-17`;
- memory quadrature:
  `1.0712218077978013e-06`;
- H4 source Nt128/Nt64:
  `1.8704084900967867e-04`.

Canonical solve controls:

- Radau/algebraic residual:
  `2.342470445459017e-13`;
- state Nt128/Nt64:
  `3.792872866687044e-05`;
- anisotropy:
  `2.371062656668157e-16`;
- all projected boundary metrics:
  machine level;
- all outputs finite.

Thus the Repair34 floating Q-cross audit defect is closed.

## Frozen failed gates

Only the propagated-shift family fails:

- active Nt128 Linf:
  `0.006259823617443525`;
- matched Nt64 Linf:
  `0.006266242848258575`;
- active RMS:
  `0.0027818898439655503`;
- matched Nt64 RMS:
  `0.0027896802666711957`;
- observed Linf order:
  `0.0014620016339260422`;
- observed RMS order:
  `0.003988992741879638`;
- near-null absolute residual / Sref:
  `1.2098659474068817e-11`.

Worst active sample:

- C:
  `C_min`;
- beta0:
  `0.1`;
- mode:
  `40`;
- final Nt128 node;
- metric:
  `0.006259823617443525`;
- absolute residual:
  `1.3827956692480324e-06`;
- scale:
  `2.209001009860335e-04`.

This is not the Repair34 near-null-only artifact. It is an active finite-scale
constraint defect and does not improve from Nt64 to Nt128.

## Localization: missing Lambda sector in Repair35 H4

The frozen reduced background used from Repair13 is Lambda-inclusive and stores

`bg["rho_lambda_action"]`.

The certified H1/H3 chain used Repair11's Lambda-inclusive first-directional
operator. Repair11 implements

`install_lambda_operator(r7, lambda_by_bg)`

which augments the frozen local GE06+GE07 matrix by the exact first
directional coefficients of

`L_lambda = -6 rho_lambda N L R^2`.

In particular:

- lapse/S:
  `-18 rho_lambda a^2`;
- isotropic/N:
  `-18 rho_lambda a^2`;
- isotropic/S:
  `-36 rho_lambda a`;
- shift and anisotropy:
  exactly zero.

Repair35 `build_context()` reconstructed the Lambda-inclusive background but
did not call `r11.install_lambda_operator`.

Therefore the canonical Repair35 H4 solve used a Lambda-inclusive background
with a Lambda-omitting linear operator.

This contradicts the certified Repair11/Repair13/Repair22/Repair32B reduced
coordinate system.

## Localization: missing mixed Lambda Q source

Repair14 already froze the exact second directional Lambda equation source:

- lapse:
  `Q_lambda,N(d,d) = -36 rho_lambda a S^2`;
- isotropic:
  `Q_lambda,iso(d,d) = -72 rho_lambda a N S - 36 rho_lambda S^2`;
- all other main rows and both constraint rows:
  zero.

For two directions d and e, the exact symmetric mixed coefficient is

`B_lambda(d,e) = [Q_lambda(d+e,d+e)-Q_lambda(d-e,d-e)]/4`.

Therefore:

- lapse:
  `B_lambda,N = -36 rho_lambda a S_d S_e`;
- isotropic:
  `B_lambda,iso = -36 rho_lambda a (N_d S_e + N_e S_d) - 36 rho_lambda S_d S_e`.

The H4 contribution is

`-2 B_lambda(Z10,Z11)`.

Repair35 `Q_total` contained only the direct GE06 and GE07 mixed
coefficients. It did not add this frozen Lambda mixed source.

Thus both pieces required by the same reduced Lambda-inclusive theory were
omitted:

1. the first-directional Lambda contribution to `L_total`;
2. the mixed second-directional Lambda contribution to `Q_total`.

## Why this explains the Repair35 pattern

The canonical Radau residual only certifies the equations represented by the
matrix actually supplied to the solver. Therefore it can remain at
`~1e-13` even if the physical reduced operator is incomplete.

Likewise, the state can converge strongly between Nt64 and Nt128 while
converging to the solution of the wrong Lambda-omitting H4 operator.

The independent propagated shift/Noether constraint is sensitive to the
covariant compatibility of the full source/operator system. The observed
nonconvergent active defect is therefore consistent with this Lambda-sector
omission.

## Frozen interpretation

Repair35 remains a historical valid FAIL.

Its direct Q-cross construction is retained.

Repair35 does not certify Z21.

The result does not establish a physical H4 inconsistency of the
Lambda-inclusive AeST-memory model because the executed H4 operator/source
was not the complete frozen Lambda-inclusive system.

## Licensed next step

A separately preregistered Repair36 may change only the localized Lambda
implementation omissions:

1. install the exact frozen Repair11 first-directional Lambda operator on all
   Nt128 and Nt64 Repair13 backgrounds;
2. add the exact Repair14-derived symmetric mixed Lambda quadratic source
   `-2 B_lambda(Z10,Z11)`;
3. retain all Repair35 parents, GE06/GE07 direct bilinear Q source, DY2,
   GE05 M1/M2 mapping, Repair18 boundary, Repair07 Radau propagator, grids,
   and numerical thresholds unchanged.

No observational input, finite eta, fitted normalization, threshold
relaxation, primordial Z21 claim or full-species claim is licensed.

## Canonical status

**Repair35 = historical valid FAIL caused by an H4 Lambda-sector
implementation omission. Z21 remains uncertified. Repair36 is licensed only
to restore the frozen Lambda-inclusive L and Q pieces.**
