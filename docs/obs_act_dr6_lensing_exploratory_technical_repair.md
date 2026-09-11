# ACT DR6 exploratory scan — technical CLASS output repair

Date: 2026-09-11

The first local ACT DR6 exploratory execution ended with

`ACT_DR6_LENSING_EXPLORATORY_SCAN_INCOMPLETE`

before any eta point was evaluated. The official ACT DR6 likelihood itself loaded successfully with the frozen `act_baseline`, `lens_only=True`, `like_corrections=False`, data v1.2 configuration. CLASS then rejected the theory input because `lensing=yes` was requested while the output contained only `lCl`.

CLASS requires scalar CMB spectra to be present when its lensed-spectrum module is enabled. This is an input-contract failure only; no ACT likelihood value, eta response, or model comparison was produced by the failed execution.

## Frozen repair

Keep unchanged:

- official ACT DR6 likelihood package/version/data/variant;
- `lens_only=True` and `like_corrections=False`;
- all cosmological and AeST parameters;
- eta grid `{0,1/256,1/128,1/64,1/32,1/16,1/8}`;
- `lensing=yes`;
- `l_max_scalars=4000`;
- `halofit` exploratory nonlinear prescription;
- eta-zero memory-on/off regression gate `1e-8`;
- `C_L^{phiphi}` to `C_L^{kappakappa}` conversion;
- exploratory interpretation and the formal D2C6H FAIL status.

Change only the CLASS theory request from

`output = lCl`

to

`modes = s`

`output = tCl,lCl`.

The additional `tCl` is generated solely to satisfy the CLASS `lensing=yes` input contract. It is not passed to the ACT likelihood: the frozen lens-only likelihood call continues to receive zero primary-CMB spectra and has likelihood corrections disabled. Therefore no primary-CMB information is added by this repair.

This repair does not alter the preregistered scientific question or any observational gate. The failed execution remains recorded as `INCOMPLETE`.
