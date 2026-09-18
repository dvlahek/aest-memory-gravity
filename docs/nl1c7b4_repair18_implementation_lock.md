# NL1C7B4 Repair18 — implementation lock

## Status

Locked after Repair18 implementation and before any Repair18 execution.

## Parent Repair17 freeze

- commit: `6a2cbd69218b63d8d7891e9deef43764365c47ff`
- file: `docs/nl1c7b4_repair17_result_freeze.md`
- blob: `c800a4e296fa23d3d7596e5730609d2f87e15a3c`
- Repair17 JSON SHA-256:
  `09750aeb9fdce7bbbbe148c8478b9af5067a72ab20a1e48171f5a9e3a1d4b82e`

## Preregistration

- commit: `ddec97d478bfd667666830fb0e2203b7334464f5`
- file:
  `docs/nl1c7b4_repair18_predata_minimal_nonlinear_projection_feasibility.md`
- blob:
  `2ce19a30603e9d8ba5ade43a8c6d629464c171c5`

## Implementation

- commit: `c59b0c5c770de137085ea647784ae835e384fe0b`
- file:
  `nl1c7b/initial_constraint_certification_repair18.py`
- blob:
  `c0e589fe120a148148c2e21406219e197d2c16db`

## Frozen imported blobs

- Repair17 localization:
  `c39d9e7bc20eef55fbd0bcea2bd19f42d8cfd8b5`
- Repair16 exact retest/state construction:
  `fbd7d24f748fc398638d4eea4b7707801161e52a`
- Repair10 signed source localization:
  `c72a85d6d42176fb8c6a5ebf5f8e101541272701`
- Repair09 exact nonlinear evaluator:
  `0cd67cecfbd590cb8819ad37314dc5b49047bc93`
- Repair02 exact nonlinear dictionary helpers:
  `eff076ec9a511f64bc693dc48b07b2ce26cfbaeb`
- Repair01 source dictionary:
  `253a0ae2a19a597f06358704ea276c9005973af3`
- base B4:
  `8559120dc273be3174eca130ca313ed6ff5acb25`
- Repair08:
  `94fb3f42a7c819b0525860f7344d5dbaff93da19`
- C7A reconstruction:
  `ff383c1ddc2cb2a684e2b5dd11fde0ae811e4fac`

## Frozen parent artifacts

Repair15a:

- JSON SHA-256:
  `596c7b13c4683840bcf40f6850356e179e77f873c3a3b42ba0b54730ae80811d`
- NPZ SHA-256:
  `997d0033eeed1f3e60c1907c7938a0ea87a1cf38de6ab860340bd003d18d6e6e`

Repair16:

- JSON SHA-256:
  `a225f435ef61eaf33a1b4466eea678b23d1a221a537589bd8e2b0717ed66335b`

Repair17:

- JSON SHA-256:
  `09750aeb9fdce7bbbbe148c8478b9af5067a72ab20a1e48171f5a9e3a1d4b82e`

## Locked projection

Projection variables only:

- `L_minus_a`
- `Rdot_minus_aHr`

All other state fields are bitwise frozen during each solve.

Center corrections are exactly zero.

Virtual amplitudes:

- 1
- 1/2
- 1/4
- 1/8

Scales:

- 5
- 10
- 20 h^-1 Mpc

Grids:

- 256
- 512

Canonical solve branch:

- Simple
- beta=1.0

Total solves: 24.

## Locked solver

- scipy least_squares
- method trf
- 2-point finite-difference Jacobian
- sparse half-band 16
- zero initial correction
- x_scale=jac
- ftol=1e-12
- xtol=1e-12
- gtol=1e-12
- max_nfev=400
- y_L bounds [-0.5,0.5]
- delta R_t/(a H R_s) bounds [-0.5,0.5]
- no multistart

## Locked science gates

- exact Repair16 lambda=1 reproduction: 1e-12 abs-or-rel
- exact Q reconstruction: <=1e-12
- historical canonical max epsilon H <=1e-7
- historical canonical max epsilon M <=1e-7
- gated correction-order slopes:
  [1.8,2.2] on 1/2->1/4 and 1/4->1/8
- lambda=1 256/512 combined-correction ratio <=2.0
- non-projection fields bitwise unchanged
- no official NPZ output

## Terminal classes

- `NL1C7B4_REPAIR18_MINIMAL_NONLINEAR_PROJECTION_FEASIBILITY_PASS`
- `NL1C7B4_REPAIR18_MINIMAL_NONLINEAR_PROJECTION_FEASIBILITY_FAIL`
- `NL1C7B4_REPAIR18_IMPLEMENTATION_FAIL`

No solver, threshold, variable-pair, branch, lambda, or classification rule may change after first execution.
