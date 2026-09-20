# GE17 late-time standard-background dust diagnostic — implementation lock

## Status

Implementation locked before first GE17 execution.

GE17 is background-only and diagnostic. It does not accept an approximation.

## Theory provenance

Immediate dependency:

`GE16_LATE_TIME_STANDARD_MATTER_RESIDUAL_DIAGNOSTIC_PASS`.

GE16 established that in the frozen perturbative window the full standard sector is extremely close to pressureless **when its total density and momentum are retained**, but GE16 did not certify the background mapping required by the GE07 dust action.

GE17 closes only that diagnostic gap.

## Pinned runtime

CLASS commit:

`e85808324f51fc694d12e3ed7439552a3c3f9540`.

Cosmology is the frozen v0.63 baseline:

- `H0=67.3324639084866`;
- `omega_b=0.02238280`;
- `N_ur=2.046`;
- `omega_cdm=0.1201075`;
- one `m_ncdm=0.06 eV` species;
- `T_ncdm=0.7137658555036082`;
- Exp AeST background;
- `KB=0.0665`;
- `Q0=1e-4 Mpc^-1`;
- `K2=9500`;
- `Z0=1e-17 Mpc^-1`.

No perturbation output is requested.

## Standard-sector definition

Using the standard CLASS background output columns,

`rho_std = rho_b + rho_g + rho_ur + rho_ncdm[0]`.

`p_std = rho_g/3 + rho_ur/3 + p_ncdm[0]`.

The patched CLASS `rho_cdm` slot is the AeST effective-dark background density,

`rho_aest`.

Vacuum `rho_lambda` is excluded from the standard and clustering sectors.

Define

`rho_cluster = rho_std + rho_aest`.

## Dust diagnostics

GE17 reports:

1. `|p_std|/rho_std`;
2. `|p_std|/rho_cluster`;
3. `|p_std|/rho_tot`;
4. `C(a)=a^3 rho_std`;
5. `max(C)/min(C)-1` over the frozen window;
6. the best constant
   `C_star=mean[C(a)]`;
7. the conserved-dust fit
   `rho_dust=C_star/a^3`;
8. global and pointwise density errors of that fit;
9. the numerical continuity identity
   `d ln rho_std/d ln a +3 = -3 p_std/rho_std`;
10. the same background quantities at the eight frozen H3 audit redshifts.

The inferred AeST pressure

`p_aest=p_tot-p_std+rho_lambda`

is reported only as a decomposition/provenance check.

## Preregistration

Commit:

`0d0f2593130667c546ba785c889a174624ccfbfd`.

File:

`ge17/predata_late_time_standard_background_dust_diagnostic.json`.

Frozen blob:

`452b94e117c2d7f692c4dcdcfd0c3a8d0033fdee`.

## Implementation

Commit:

`269e4fdce534c70e9b4c85fcebd98b3115bbbd0d`.

File:

`ge17/late_time_standard_background_dust_diagnostic.py`.

Frozen blob:

`e7ca357404a1d24170564c243b626e051e532f96`.

## Frozen window

`0.2<=z<=1.5`.

Frozen audit redshifts:

- 0.247619;
- 0.312010;
- 0.451160;
- 0.604190;
- 0.772470;
- 0.957560;
- 1.161170;
- 1.385240.

## Frozen diagnostic gates

Require:

- pinned CLASS provenance;
- all required background columns;
- at least 64 native background rows in the window;
- species reconstruction of `rho_tot` to relative L2 <= `1e-12`;
- numerical continuity identity to relative L2 <= `1e-5`;
- all outputs finite.

## No approximation acceptance gate

GE17 has no threshold declaring the standard sector “dust enough”.

A PASS certifies only the decomposition and diagnostics.

A later separately preregistered model-choice step must select any approximation budget independently.

## Terminal classes

Pass:

`GE17_LATE_TIME_STANDARD_BACKGROUND_DUST_DIAGNOSTIC_PASS`.

Fail:

`GE17_LATE_TIME_STANDARD_BACKGROUND_DUST_DIAGNOSTIC_FAIL`.

## Claim boundary

Even PASS does not:

- accept matched effective dust;
- relabel GE08;
- license `Z20`;
- modify AeST;
- introduce finite eta;
- establish nonlinear-collapse or observational claims.
