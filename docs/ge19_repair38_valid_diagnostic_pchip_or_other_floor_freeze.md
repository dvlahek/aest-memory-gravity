# GE19 Repair38 valid diagnostic — frozen-source propagation-floor localization freeze

## Status

Repair38 repair02 completed successfully and is frozen as a valid diagnostic result.

Terminal classification:

`GE19_REPAIR38_FROZEN_SOURCE_RADAU_SUBSTEP_LOCALIZATION_COMPLETE`.

Frozen route:

`PCHIP_OR_OTHER_FLOOR_REMAINS`.

Repair38 is diagnostic-only. It does not certify Z21 and does not license lensing.

Repair37 remains historical valid FAIL and is not relabelled.

## Frozen local artifacts

Canonical JSON:

- bytes: `4268`;
- SHA-256:
  `08dd95c614118c66e37349e2b8d058e85163812fed77c9b048e0ce57e339e5dd`.

NPZ:

- bytes: `16161137`;
- SHA-256:
  `aff63771c1800b0db236cd020cf0d2772f6d9a0fd0328573d055392f2c60da67`.

Repair02 FULL log:

- bytes: `4268`;
- SHA-256:
  `08dd95c614118c66e37349e2b8d058e85163812fed77c9b048e0ce57e339e5dd`.

Outer runner log:

- bytes: `7053`;
- SHA-256:
  `6e6b4477528ca63858a14f2fecf7bd2183498739b4c6a4d8db2d4cf3ba10dd16`.

Terminal marker:

`GE19_REPAIR38_REPAIR02_DIAGNOSTIC_COMPLETE`.

## Frozen contract

Repair38 loaded the frozen Repair37 Nt128:

- total H4 main source arrays;
- total H4 constraint-source arrays;
- projected p0;
- shift-scale arrays defining the frozen active mask.

The H4 source was not recomputed.

The projected boundary was not resolved.

The source-stage representation remained the Repair07 PCHIP interpolator.

The Radau tableau remained the Repair07 two-stage Radau IIA method.

Only the number of internal Radau substeps per frozen Nt128 interval varied:

`1,2,4`.

The science shift target remained report-only at `1e-6`.

## Factor-1 reproduction

Factor 1 reproduces frozen Repair37 exactly in the registered controls:

- Z21 global relative L2:
  `0.0`;
- shift-metric global relative L2:
  `0.0`;
- projected p0 exact:
  `true`;
- frozen active sample count:
  `23850`.

All implementation gates pass.

## Frozen substep results

Substep 1:

- active Linf:
  `1.1749387207106255e-6`;
- active RMS:
  `1.0515104304068532e-6`;
- active median:
  `1.087992879156214e-6`;
- canonical Radau/algebraic residual max:
  `2.4043192247369374e-13`;
- all outputs finite:
  `true`.

Substep 2:

- active Linf:
  `1.341600178925417e-6`;
- active RMS:
  `1.1859570854138313e-6`;
- active median:
  `1.2340964134638693e-6`;
- canonical Radau/algebraic residual max:
  `2.404627126840512e-13`;
- all outputs finite:
  `true`.

Substep 4:

- active Linf:
  `1.3797699672147026e-6`;
- active RMS:
  `1.2040175184159568e-6`;
- active median:
  `1.2523655565644014e-6`;
- canonical Radau/algebraic residual max:
  `2.4046656679304236e-13`;
- all outputs finite:
  `true`.

The preregistered material-improvement condition is not met:

- Linf factor2/factor1:
  `1.1418469365908643`;
- Linf factor4/factor2:
  `1.0284509415613365`;
- registered factor1-to-factor2 Linf order:
  `-0.19136927187304698`;
- registered factor2-to-factor4 Linf order:
  `-0.040472977086756685`.

Therefore the frozen route is

`PCHIP_OR_OTHER_FLOOR_REMAINS`.

## Post-freeze localization from the frozen NPZ

These quantities are diagnostic analyses of the frozen outputs and do not
change the preregistered routing.

The propagated Z21 state itself converges cleanly under internal Radau
substepping:

- ||Z1-Z2|| / ||Z2-Z4|| =
  `8.030548956166639`;
- corresponding observed order =
  `3.0054986115619555`.

The complete shift-metric field differences also converge at approximately
third order:

- ||m1-m2|| / ||m2-m4|| =
  `7.9105878110222365`;
- corresponding observed order =
  `2.983784900834436`.

Thus the Radau discretization converges with its expected third-order
signature, but it converges toward a nonzero shift-residual floor instead of
removing that floor.

A report-only p=3 Richardson estimate from factors 2 and 4 gives:

- active Linf limiting value approximately
  `1.385222794113172e-6`;
- active RMS limiting value approximately
  `1.2065975802734033e-6`.

This is not a science threshold modification and is not a PASS claim.

## Interpretation

Repair38 falsifies the specific hypothesis that the sole remaining Repair37
shift failure is primarily caused by insufficient internal Radau step
resolution.

The Radau propagation itself shows the expected third-order convergence.

The remaining floor is therefore upstream or stage-representation dependent.
The next licensed localization target is the frozen source-at-stage
representation, with Repair07 PCHIP as the primary candidate, while keeping
the H4 source nodes, projected boundary, physical operator and science
threshold frozen.

A future diagnostic should distinguish interpolation/stage-source error from
any other reconstruction-stage floor before another science reclosure is
preregistered.

## Claim boundary

Repair38 certifies only the numerical localization above.

It does not certify:

- Z21;
- a primordial homogeneous Z21 mode;
- a full-species nonlinear cosmology;
- finite physical eta;
- lensing;
- any observational signal.
