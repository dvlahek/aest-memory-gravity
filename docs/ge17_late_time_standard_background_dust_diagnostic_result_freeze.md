# GE17 late-time standard-background dust diagnostic — result freeze

## Status

Frozen first locked GE17 execution.

Terminal classification:

`GE17_LATE_TIME_STANDARD_BACKGROUND_DUST_DIAGNOSTIC_PASS`.

GitHub Actions run:

`35515531659`.

Execution HEAD:

`32b1de2e4b2914f1e78907fe0f7fd578f8a745ed`.

Artifact:

- ID `10606677735`;
- name `results_bundle_ge17_late_time_standard_background_dust_diagnostic`;
- ZIP SHA-256
  `e038cb3d512f38d9c49595d78515a50be159bda5024fe7d3da6382bce2cac7cb`.

## Frozen output hashes

Result JSON:

- bytes: `6527`;
- SHA-256:
  `e4614cfe316a4184190ef5c8d3ab3b0e722da6b08f86c14bf0624f6e881b4081`.

Result log:

- bytes: `6527`;
- SHA-256:
  `e4614cfe316a4184190ef5c8d3ab3b0e722da6b08f86c14bf0624f6e881b4081`.

Result NPZ:

- bytes: `2445307`;
- SHA-256:
  `589f107bd03b3a56cc5d074c52a90648c7b2136be19a668fd258cc76b67ba7b5`.

## Gate result

All locked GE17 diagnostic gates pass:

- pinned CLASS provenance;
- all required background columns;
- 910 native background rows in `0.2<=z<=1.5`;
- exact species reconstruction of total background density within the frozen `1e-12` gate;
- standard-sector continuity identity within the frozen `1e-5` gate;
- all outputs finite.

The numerical continuity identity error is

`5.516842945243289e-10`.

## Standard-sector equation of state

Over the frozen background window,

`||p_std||/||rho_std|| = 1.1411446090451888e-3`.

The maximum pointwise

`|p_std/rho_std|`

is

`1.3108268891307302e-3`.

Thus the standard sector is close to, but not exactly, pressureless.

Relative to the entire clustering background,

`||p_std||/||rho_std+rho_AeST|| = 1.8406434711926696e-4`

with maximum pointwise value

`2.1152925241376707e-4`.

Relative to the full FLRW density,

`||p_std||/||rho_tot|| = 1.4617774747444727e-4`

with maximum pointwise value

`1.8572535483054548e-4`.

## Conserved-dust background test

Define

`C(a)=a^3 rho_std(a)`.

Across `0.2<=z<=1.5`,

`max(C)/min(C)-1 = 2.0441041966086093e-3`.

The best constant normalization is

`C_star = 2.568543329983919e-9`.

The corresponding conserved dust background

`rho_dust=C_star/a^3`

approximates the full standard-sector background density with:

- global relative L2:
  `7.530875474909884e-4`;
- maximum pointwise relative error:
  `1.1436503307021572e-3`.

This is the dominant reduced-background matter error found by GE17.

## Frozen audit-redshift behavior

At the eight frozen H3 audit redshifts, the standard-sector equation of state rises smoothly from

`6.545014360331053e-4`

at `z=0.247619`

to

`1.2515782748385427e-3`

at `z=1.38524`.

The clustering-weighted pressure fraction rises from

`1.0544323498488494e-4`

to

`2.0193816306560437e-4`.

No abrupt background transition occurs.

## AeST background decomposition control

The inferred AeST background pressure is numerically negligible in the frozen Exp reference:

- global `||p_AeST||/||rho_AeST|| =
  1.0782016555263135e-14`;
- maximum pointwise
  `|p_AeST/rho_AeST| =
  1.1516004644575247e-14`.

This is a decomposition/provenance control, not a new AeST physics claim.

## Combined GE16 + GE17 matter picture

GE16 showed that once the full standard-sector density and momentum are retained, the perturbative stress omitted by a pressureless representation is tiny:

- pressure/density:
  `4.0296809261404915e-7`;
- shear/density:
  `5.717716788656946e-10`;
- worst pointwise pressure/density:
  `2.7446222891988022e-6`.

GE17 shows that the larger error is instead the background fact that the standard sector is not exactly one conserved dust component because photons, massless radiation and the finite-temperature massive neutrino remain present.

Therefore the correct reduced H3 matter model is not baryon-only dust and not an assertion of exact pressurelessness.

It is a **matched total-standard effective dust with an explicit background truncation envelope**.

## Next licensed model choice

A separately locked reduced-H3 model may use

`rho_dust(a)=C/a^3`

with central normalization

`C=C_star`.

Matter-systematic controls should bracket the exact GE17 standard background using frozen constants

`C_min=min[a^3 rho_std]`

and

`C_max=max[a^3 rho_std]`

computed from the frozen GE17 artifact.

The perturbative standard density and momentum remain matched to the frozen first-order standard-sector state; only pressure/shear are omitted in the pressureless GE07 source block.

The resulting Z20 solution must be labeled a **reduced-H3 matched-dust solution**, not the exact full-species CLASS second-order solution.

## Claim boundary

GE17 does not itself accept the reduction or license Z20.

It supplies the frozen background diagnostics and the model-error envelope needed for a separate reduced-H3 preregistration.
