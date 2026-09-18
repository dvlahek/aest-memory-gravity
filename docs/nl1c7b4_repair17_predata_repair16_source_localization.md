# NL1C7B4 Repair17 — pre-data exact signed source localization of Repair16 residual

## Status

Pre-data / pre-run diagnostic preregistration.

Repair16 is frozen at commit

`af47a7c33c0f09744b98828e0727279b1c3d6475`

with terminal class

`NL1C7B4_REPAIR16_REPAIR15A_RAW_CONSTRAINT_FAIL`.

Repair17 does not repair the state. It localizes the exact nonlinear residual that remains after the certified Repair15a density-Q completion.

## Frozen parents

Repair16 local result JSON:

- SHA-256:
  `a225f435ef61eaf33a1b4466eea678b23d1a221a537589bd8e2b0717ed66335b`;
- classification:
  `NL1C7B4_REPAIR16_REPAIR15A_RAW_CONSTRAINT_FAIL`.

Repair15a certified state:

- JSON SHA-256:
  `596c7b13c4683840bcf40f6850356e179e77f873c3a3b42ba0b54730ae80811d`;
- NPZ SHA-256:
  `997d0033eeed1f3e60c1907c7938a0ea87a1cf38de6ab860340bd003d18d6e6e`.

## Exact source labels

Use exactly the frozen Repair10 signed decomposition:

1. GR_kin
2. GR_curv_NL
3. GR_curv_Rr
4. GR_Nr_boundary
5. AeST_E2
6. AeST_EX
7. AeST_X2
8. AeST_J
9. AeST_K
10. dust
11. standard_bg

No regrouping, coefficient change, sign change, or omitted source is allowed.

## State construction

Use exactly the Repair16 state semantics:

- primary Nr=256 loaded directly from the certified Repair15a NPZ;
- Nr=512 reconstructed from the same frozen continuous Repair08 representation plus the exact Repair15a Fourier density-Q correction;
- same background Q/KQQ construction;
- same dense trace;
- eta=0.

No state array is modified by Repair17.

## Exact reproduction gate

For all 54 scale/grid/Y/beta cases, Repair17 must reproduce the frozen Repair16:

- max_epsilon_H
- max_epsilon_M

using the signed 11-source decomposition.

For each scalar comparison, require absolute-or-relative error <= `1e-12`.

Repair16 raw PASS/FAIL labels are historical and must remain unchanged.

## Signed closure gate

At every non-center radial point and every case, require

`sum(named H sources) = exact H numerator`

and

`sum(named M sources) = exact M numerator`

with normalized closure error <= `1e-12`.

## Hotspot localization

For each case, report at the exact max-epsilon H and M radial points:

- radial index;
- r in Mpc;
- epsilon;
- signed numerator;
- denominator;
- all 11 signed source values;
- dominant source by absolute magnitude;
- second source by absolute magnitude;
- dominant/rest signed ratio.

No hotspot is removed from any gate.

## Two-grid reporting

For each scale/Y/beta pair, report the dominant and second source labels and hotspot radii independently on Nr=256 and Nr=512.

Label agreement is reported but is not imposed as a physics gate.

## Frozen settings

- scales: 5,10,20 h^-1 Mpc
- Nr: 256,512
- Y: Simple, Exponential, Sharp
- beta: 1.0,0.5,0.1
- total cases: 54
- all non-center radial points retained
- eta=0
- exact Repair16 raw threshold remains 1e-7 but is not altered or reinterpreted

## Gates

### R17_G1 — frozen provenance

Exact Repair16 JSON hash/class/gate pattern, Repair15a hashes/class, dense coverage, and imported evaluator blobs.

### R17_G2 — exact Repair16 reproduction

All 54 H/M max epsilon values match Repair16 to absolute-or-relative `1e-12`.

### R17_G3 — exact signed decomposition closure

Maximum normalized H and M closure errors <= `1e-12`.

### R17_G4 — complete hotspot localization

All 54 cases have complete finite 11-source H/M hotspot records.

### R17_G5 — complete two-grid localization report

Exactly 27 scale/Y/beta pairs are reported at both grids.

### R17_G6 — claim boundary

Require no state change, projection, fit, source/sign/coefficient change, clipping, point selection, threshold change, nonlinear evolution, finite eta, B4-PASS relabel, or observational claim.

## Terminal classifications

PASS:

`NL1C7B4_REPAIR17_REPAIR16_SOURCE_LOCALIZATION_PASS`

FAIL:

`NL1C7B4_REPAIR17_IMPLEMENTATION_FAIL`.

Repair17 has no state-repair classification.

## Interpretation boundary

A PASS may identify which exact nonlinear-order sources dominate the residual after the first-order density-Q bridge completion.

It does not establish that any dominant source coefficient is wrong.

Any nonlinear constraint-correction construction must be separately preregistered after Repair17 is frozen.
