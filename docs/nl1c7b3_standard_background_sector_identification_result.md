# NL1C7B3 standard background sector identification — result freeze

Status: **HISTORICAL SCIENCE FAIL / CI SUCCESS**

Classification:

`NL1C7B3_STANDARD_BACKGROUND_IDENTIFICATION_FAIL`

## Provenance

- official run: `35195633648`
- head: `43573a7c1eaf9090b0890297edcadde017bdb9bb`
- artifact: `10484764897`
- artifact SHA256: `d6b80e99cb456314e130f5e7e65c15b4f608ac9fc8a8395263404045e9fa67e4`
- pinned CLASS: `e85808324f51fc694d12e3ed7439552a3c3f9540`
- parent B2 Repair01 run: `35193003807`

## Result

The source-declared standard sector identified from the frozen CLASS model is

`rho_g + rho_ur + rho_ncdm[0] + rho_lambda`.

At `a_i=0.02`, the PCHIP evaluation gave

- `rho_std_CLASS = 3.5096716852244486e-05 Mpc^-2`,
- `rho_std_C6 = 1.0529015055673347e-04 Mpc^-2`,
- fixed B2 remainder `rho_rem = 1.0529789814922824e-04 Mpc^-2`,
- closure error normalized by `3H^2 = 1.2808707952552944e-06`.

The standard-sector fractions were

- photons: `0.4899960704630926`,
- ultra-relativistic species: `0.22768234434229967`,
- massive ncdm: `0.28133802617571657`,
- cosmological constant: `0.0009835590188910677`.

Gate results:

- B3-G1 provenance: PASS
- B3-G2 parent reproduction: FAIL
- B3-G3 source-declared standard species: FAIL in the implementation because `rho_tot`, an aggregate diagnostic column, was treated as an additional density sector
- B3-G4 fixed-remainder closure: FAIL at `1.2808707952552944e-06` versus `1e-7`
- B3-G5 full homogeneous closure: FAIL at the same normalized level
- B3-G6 interpolation control: PASS; PCHIP-linear change `5.9138299302176154e-09`

Fresh background-table PCHIP versus retained source-trace PCHIP differed by

- `H`: `2.985661547178624e-07` relative,
- `rho_b`: `7.190446501540032e-11` relative,
- effective `rho_cdm`/AeST: `2.2674302495123033e-06` relative.

## Post-result diagnosis boundary

No science gate is retroactively changed here. Two representation issues are recorded for a separate preregistered repair:

1. `rho_tot` is a CLASS aggregate/diagnostic total density and is not an independent source-declared species to add to the standard-sector sum.
2. B2 retained quantities and B3 `get_background()` PCHIP values were evaluated on different exported numerical grids. Their `10^-6`-level mismatch is larger than the frozen `10^-8` parent-reproduction gate and is of the same order as the residual standard-sector closure mismatch.

A repair may therefore test the same frozen model at one common exact redshift using CLASS direct background evaluation/source identities. It may not fit the remainder, alter the physical species sum, relax the original B3 thresholds, or claim radial/nonlinear evolution.
