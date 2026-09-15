# Stable AeST cosmic memory R7a — live epoch derivative post-data checkpoint

Date: 2026-09-15
Branch: `fullj-evolving-weyl-bridge`

## Frozen provenance

R7a preregistration was locked before implementation/result in commit

`04c15f83032dd8a4a1baf2d26b576b00cc4c2681`.

Historical R7 remains

`STABLE_AEST_COSMIC_MEMORY_R7_PHYSICAL_BRIDGE_FAIL`

with post-data lock

`cf0132f7877160948e1ba4670eda19750d82159b`.

The first R7a execution failed technically before a science result because the frozen CLASS input parser rejected negative `aest_eta`. This was documented before repair in

`d91067389d73cc3afd1857df5fb3bee851844420`.

The repair changed only the disposable R7a parser domain to permit signed eta for the central-derivative diagnostic. The physical equations, epoch windows, epsilon values, observables, and preregistered gates were not changed. The repair implementation was audited in

`d562dacdd95e44a1f523262755c2666df781869d`.

## Formal result

The completed repaired run returned

`STABLE_AEST_COSMIC_MEMORY_R7A_LIVE_LOOKBACK_DECOMPOSITION_CERTIFIED`

with exit code 0.

All preregistered gates passed:

- R7A-G1 provenance and parent lock: PASS,
- R7A-G2 live physical source topology: PASS,
- R7A-G3 finite runs and baseline identity: PASS,
- R7A-G4 full central-derivative amplitude consistency: PASS,
- R7A-G5 direct physical bridge to R5b: PASS,
- R7A-G6 live epoch reconstruction: PASS.

The baseline is exactly identical to frozen R5b at stored precision for `sigma8`, `fsigma8`, and linear `C_L^{kappa kappa}`.

## Central-derivative control

Comparing the full central derivative from `eta=+-0.025` with the independent `eta=+-0.05` control gives:

- `sigma8`: E = 2.838183990316935e-4, C = 0.9999999649430891,
- `fsigma8`: E = 1.2815832400349598e-3, C = 0.9999992619272847,
- `C_L^{kappa kappa}`: E = 1.0715543034218933e-4, C = 0.9999999961381122.

Thus the symmetric local derivative is stable across the two locked epsilon scales.

## Direct physical bridge to R5b

The live full central derivative agrees with the previously certified one-sided R5b derivative:

- `sigma8`: E = 6.869108103056808e-4, C = 0.999999779704104,
- `fsigma8`: E = 3.7973586513146383e-3, C = 0.9999936913666798,
- `C_L^{kappa kappa}`: E = 7.613247231653896e-3, C = 0.9999782408564648.

This closes the R7 replay ambiguity: the live physical derivative reproduces the certified observable tangent without force-table transport.

## Epoch reconstruction

The four disjoint live physical epoch derivatives reconstruct the full derivative with:

- `sigma8`: E = 3.3916425185515607e-4, C = 0.9999999973745712,
- `fsigma8`: E = 1.0296612101930425e-3, C = 0.9999999072232559,
- `C_L^{kappa kappa}`: E = 3.9386737266240484e-4, C = 0.9999999486756445.

The decomposition is therefore licensed in the locked `tau H0=10`, order-20, linear-observable setup.

## Lookback structure

For the full redshift vectors, signed projection fractions onto the full response are:

### sigma8

- `z >= 10`: 0.00369,
- `2 <= z < 10`: 0.18132,
- `0.5 <= z < 2`: 0.73897,
- `z < 0.5`: 0.07636.

### f sigma8

- `z >= 10`: 0.00209,
- `2 <= z < 10`: 0.10555,
- `0.5 <= z < 2`: 0.68347,
- `z < 0.5`: 0.20983.

### linear C_L^{kappa kappa}

- `z >= 10`: -0.00366,
- `2 <= z < 10`: -0.17301,
- `0.5 <= z < 2`: 0.28958,
- `z < 0.5`: 0.88686.

The lensing response therefore contains substantial temporal cancellation: intermediate-redshift contributions project oppositely to the final full lensing tangent, while the latest epoch supplies the dominant positive projection.

At observed `z=0.2`, the signed pointwise fractions are approximately:

- `sigma8`: ancient 0.00345, intermediate 0.17022, recent-structure 0.74219, late 0.08448;
- `fsigma8`: ancient 0.00010, intermediate 0.00978, recent-structure 0.54909, late 0.44243.

The dominant epoch shifts with observed redshift: toward `z=2`, the `2 <= z < 10` interval dominates the growth response.

For the full lensing tangent, the two sign changes occur near `L ~= 595.3` and `L ~= 1819.2`. These zero crossings arise from changing cancellation among the epoch components, not from a single global amplitude rescaling.

## Licensed interpretation

R7a licenses the following statement in the locked stable-AeST regime (`tau H0=10`, memory order 20, linear observables, tolerance 3e-8):

The first-order physical memory response admits a reproducible causal lookback decomposition into disjoint cosmic epochs. Growth observables are dominated by the recent structure-formation interval at low observed redshift and shift toward earlier epochs for higher-redshift observations. The lensing response exhibits a distinct temporal cancellation pattern, with the latest epoch providing the largest positive projection and the intermediate epoch contributing with opposite sign in the covariance-free vector projection used here.

R7a does not license an observational detection, tau-generality, a universal entire-Universe memory claim, permanent elasticity loss, or reclassification of historical R7.
