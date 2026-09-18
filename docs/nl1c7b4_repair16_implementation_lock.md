# NL1C7B4 Repair16 — implementation lock

## Status

Locked after Repair16 implementation and before any Repair16 execution.

## Parent state

Repair15a local PASS freeze:

- commit: `045c5b28b74ff258dbc775057cf3e9387d47b37c`
- file: `docs/nl1c7b4_repair15a_result_freeze.md`
- blob: `2843173d5a024ad3e256b0f3eeda5f5bafae0242`
- result JSON SHA-256:
  `596c7b13c4683840bcf40f6850356e179e77f873c3a3b42ba0b54730ae80811d`
- state NPZ SHA-256:
  `997d0033eeed1f3e60c1907c7938a0ea87a1cf38de6ab860340bd003d18d6e6e`

## Preregistration

- commit: `f39e797ab9c6df71fe4b026f783654eef45e3e2c`
- file: `docs/nl1c7b4_repair16_predata_repair15a_exact_constraint_retest.md`
- blob: `70f6edc9bb5e7847abc68b2947115c42757e88df`

## Implementation

- commit: `c31b740460f25ffd9d8cb4b60dea593ea7db8587`
- file: `nl1c7b/initial_constraint_certification_repair16.py`
- blob: `fbd7d24f748fc398638d4eea4b7707801161e52a`

## Frozen imported physics/evaluator blobs

- Repair09 exact nonlinear evaluator/helper:
  `0cd67cecfbd590cb8819ad37314dc5b49047bc93`
- Repair01 exact variational source dictionary:
  `253a0ae2a19a597f06358704ea276c9005973af3`
- Repair02 exact nonlinear dictionary helpers:
  `eff076ec9a511f64bc693dc48b07b2ce26cfbaeb`
- base B4 definitions:
  `8559120dc273be3174eca130ca313ed6ff5acb25`
- Repair08 evaluator:
  `94fb3f42a7c819b0525860f7344d5dbaff93da19`
- frozen C7A spherical reconstruction:
  `ff383c1ddc2cb2a684e2b5dd11fde0ae811e4fac`

## Locked settings

- a_i = 0.02
- eta = 0
- scales = 5,10,20 h^-1 Mpc
- radial grids = 256,512
- Y = Simple, Exponential, Sharp
- beta = 1.0,0.5,0.1
- total cases = 54
- exact nonlinear Q dictionary limit = 1e-12
- state-anchor limit = 1e-12
- raw Hamiltonian limit = 1e-7
- raw radial-momentum limit = 1e-7
- two-grid RMS ratio limit = 2.0

The Repair12 perturbative-order gates are not Repair16 PASS criteria.

## Primary/control semantics

Primary Nr=256 states are loaded directly from the exact Repair15a NPZ.

Nr=512 is an independent continuous-representation control: frozen Repair08 continuous state plus the exact same Repair15a Fourier density-Q correction evaluated directly on the 512 grid.

No B4 residual is used to construct either state.

## Claim boundary

Repair16 forbids any state projection, coefficient fit/rescale, source insertion/removal, sign change, K clipping, Q linearization, point removal, threshold change, Y/beta/scale selection, nonlinear evolution, finite eta, or observational claim.

## Terminal classes

- `NL1C7B4_REPAIR16_REPAIR15A_EXACT_NONLINEAR_CONSTRAINT_PASS`
- `NL1C7B4_REPAIR16_REPAIR15A_RAW_CONSTRAINT_FAIL`
- `NL1C7B4_REPAIR16_IMPLEMENTATION_FAIL`

No threshold/classification rule may change after first execution.
