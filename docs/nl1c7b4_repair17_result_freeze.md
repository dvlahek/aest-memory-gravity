# NL1C7B4 Repair17 — local result freeze

## Status

Frozen local WSL diagnostic PASS from the first locked Repair17 execution.

Terminal classification:

`NL1C7B4_REPAIR17_REPAIR16_SOURCE_LOCALIZATION_PASS`

with

`SCIENCE_RC=0`.

Execution HEAD:

`519fc1fdd9a074bf14d94db9890ee62da4c0a2a8`.

This is a local WSL result, not an official GitHub Actions run.

## Frozen output hashes

- result JSON:
  - bytes: `181891`
  - SHA-256:
    `09750aeb9fdce7bbbbe148c8478b9af5067a72ab20a1e48171f5a9e3a1d4b82e`
- evaluator log:
  - bytes: `182337`
  - SHA-256:
    `c48e4bafe8e3b1283250d645898e40b0c7ca43ed39714b634e87ee99ccfbd98d`
- local runner log:
  - bytes: `184404`
  - SHA-256:
    `f4422fd400722b44e4bb75d0bfbbb3c10b2abe284857874e1bf938ae0742d441`

## Gates

All six frozen gates PASS:

- R17_G1 frozen provenance
- R17_G2 exact Repair16 reproduction
- R17_G3 signed decomposition closure
- R17_G4 complete hotspot localization
- R17_G5 complete two-grid localization report
- R17_G6 claim boundary

The signed decomposition closes exactly:

- max H closure = `0.0`
- max M closure = `0.0`.

## Global localization

Across all 54 exact cases:

- Hamiltonian dominant source:
  `GR_Nr_boundary` in 54/54;
- Hamiltonian second source:
  `GR_curv_NL` in 54/54;
- momentum dominant source:
  `AeST_E2` in 54/54;
- momentum second source:
  `AeST_EX` in 54/54.

Across all 27 scale/Y/beta two-grid pairs:

- H dominant label agrees between Nr=256 and Nr=512 in 27/27;
- M dominant label agrees between Nr=256 and Nr=512 in 27/27.

## Representative Simple beta=1 hotspots

### Scale 5 h^-1 Mpc

Nr=256:

- H:
  - epsilon `2.8244907235774306e-7`
  - r `5.125284583150239 Mpc`
  - dominant `GR_Nr_boundary=-0.07999999891587788`
  - second `GR_curv_NL=0.0400000007995726`
  - signed numerator `-4.519351565861825e-8`
- M:
  - epsilon `0.99999392720923`
  - r `45.19569132414301 Mpc`
  - dominant `AeST_E2=-9.087177024783368e-13`
  - second `AeST_EX=-9.232342448184978e-15`
  - signed numerator `-9.179519828229793e-13`
  - dominant/opposing-rest diagnostic `-98.4069866370852`.

Nr=512 gives the same source labels, with H hotspot at
`5.231510460029264 Mpc` and M hotspot at
`45.339757320253625 Mpc`.

### Scale 10 h^-1 Mpc

Simple beta=1:

- Nr=256:
  - H epsilon `6.591345400775493e-6`, r `9.318699242091343 Mpc`
  - M epsilon `0.9998965065630939`, r `68.95837439147593 Mpc`
- Nr=512:
  - H epsilon `6.590922989560273e-6`, r `9.300463040052025 Mpc`
  - M epsilon `0.9999999999944793`, r `69.05593807238628 Mpc`.

The source labels remain
`GR_Nr_boundary / GR_curv_NL` for H and
`AeST_E2 / AeST_EX` for M.

### Scale 20 h^-1 Mpc

Simple beta=1:

- Nr=256:
  - H epsilon `9.458326870987007e-6`, r `15.841788711555283 Mpc`
  - M epsilon `0.9984002409940183`, r `232.03561112807444 Mpc`
- Nr=512:
  - H epsilon `9.458367877931119e-6`, r `15.810787168088442 Mpc`
  - M epsilon `0.9982808847025694`, r `232.04655284929802 Mpc`.

The same source labels persist.

## Interpretation

Repair17 does not identify a coefficient or sign error.

The H hotspot is a near-cancellation among large GR curvature/boundary terms, with the remaining signed residual much smaller than the individual terms.

The M hotspot is overwhelmingly AeST_E2 dominated, with AeST_EX approximately two orders of magnitude smaller and of the same sign in the representative scale-5 case.

Together with the frozen Repair11 analytic result that the E2/EX momentum sources begin at quadratic perturbative order, this supports treating the remaining Repair16 residual as nonlinear-order constraint content of a state constructed only through first order.

Historical Repair16 remains FAIL and is not relabelled.

## Licensed continuation

A separately preregistered nonlinear constraint-projection feasibility test is licensed.

The projection must:

- preserve the certified Repair15a first-order matter/scalar content;
- change only preregistered geometric/extrinsic variables;
- demonstrate that the correction is asymptotically second order;
- use the exact frozen constraint dictionary;
- retain eta=0;
- make no observational claim.

No official corrected state may be written until the feasibility stage itself passes.
