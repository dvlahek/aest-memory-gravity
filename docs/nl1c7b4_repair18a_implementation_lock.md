# NL1C7B4 Repair18a — implementation lock

## Status

Locked after Repair18a implementation and before any Repair18a execution.

## Frozen Repair18 parent result

Repair18 result freeze:

- commit:
  `ff3517dc9a5d394339d20e82b3dd4158346f5498`
- file:
  `docs/nl1c7b4_repair18_result_freeze.md`
- blob:
  `aa934847951036cfe925becd91740b35b3c0d065`
- Repair18 JSON SHA-256:
  `8f8b6ce1316bd5cad3442ebd0cba692e4d4c82060685da083517b990cac36922`.

Repair18 remains classified:

`NL1C7B4_REPAIR18_MINIMAL_NONLINEAR_PROJECTION_FEASIBILITY_FAIL`.

## Preregistration

- commit:
  `7472d7be86c4de2b9f8f74463bad557757d0b60c`
- file:
  `docs/nl1c7b4_repair18a_predata_dimensionless_rt_coordinate.md`
- blob:
  `0b24906bc85d8f824053965d631be35de75d6af0`.

## Implementation

- commit:
  `de0eba957933ba96ddb879c16928e5a288b7ed52`
- file:
  `nl1c7b/initial_constraint_certification_repair18a.py`
- blob:
  `767199e8ab620f5d6dabd50d0efde9828f22048b`.

## Coordinate-only change

Repair18 physical solver variables:

- `y_L`
- physical `delta R_t`

Repair18a solver variables:

- `y_L`
- dimensionless
  `q_Rt = delta R_t/(a H R_s)`.

Physical projection remains exactly:

- `L=L_p exp(y_L)`
- `R_t=R_{t,p}+q_Rt(a H R_s)`.

The physical bounds are unchanged:

- `y_L in [-0.5,0.5]`
- `delta R_t/(a H R_s) in [-0.5,0.5]`.

## Frozen solver

Unchanged except for the coordinate representation above:

- scipy `least_squares`
- method `trf`
- 2-point finite differences
- sparse half-band 16
- zero initial correction
- `x_scale='jac'`
- `ftol=1e-12`
- `xtol=1e-12`
- `gtol=1e-12`
- `max_nfev=400`
- no multistart.

## Frozen science domain

Unchanged from Repair18:

- eta=0
- canonical solve branch Simple, beta=1
- lambdas 1, 1/2, 1/4, 1/8
- scales 5,10,20 h^-1 Mpc
- grids 256,512
- 24 canonical solves
- exact frozen 11-source nonlinear constraints
- exact Q reconstruction
- historical raw threshold 1e-7
- correction scaling gate [1.8,2.2]
- lambda=1 two-grid correction ratio <=2
- all non-projection fields bitwise frozen.

## Frozen imported blobs

- Repair18 evaluator:
  `c0e589fe120a148148c2e21406219e197d2c16db`
- Repair17 localization:
  `c39d9e7bc20eef55fbd0bcea2bd19f42d8cfd8b5`
- Repair16 exact retest:
  `fbd7d24f748fc398638d4eea4b7707801161e52a`
- Repair10 localization:
  `c72a85d6d42176fb8c6a5ebf5f8e101541272701`
- Repair09 exact nonlinear evaluator:
  `0cd67cecfbd590cb8819ad37314dc5b49047bc93`
- Repair02 exact nonlinear helpers:
  `eff076ec9a511f64bc693dc48b07b2ce26cfbaeb`
- Repair01 source dictionary:
  `253a0ae2a19a597f06358704ea276c9005973af3`
- base B4:
  `8559120dc273be3174eca130ca313ed6ff5acb25`
- Repair08:
  `94fb3f42a7c819b0525860f7344d5dbaff93da19`
- C7A reconstruction:
  `ff383c1ddc2cb2a684e2b5dd11fde0ae811e4fac`.

## Frozen parent artifact hashes

Repair15a JSON:

`596c7b13c4683840bcf40f6850356e179e77f873c3a3b42ba0b54730ae80811d`

Repair15a NPZ:

`997d0033eeed1f3e60c1907c7938a0ea87a1cf38de6ab860340bd003d18d6e6e`

Repair16 JSON:

`a225f435ef61eaf33a1b4466eea678b23d1a221a537589bd8e2b0717ed66335b`

Repair17 JSON:

`09750aeb9fdce7bbbbe148c8478b9af5067a72ab20a1e48171f5a9e3a1d4b82e`

Repair18 JSON:

`8f8b6ce1316bd5cad3442ebd0cba692e4d4c82060685da083517b990cac36922`

## Terminal classes

- `NL1C7B4_REPAIR18A_DIMENSIONLESS_RT_COORDINATE_FEASIBILITY_PASS`
- `NL1C7B4_REPAIR18A_DIMENSIONLESS_RT_COORDINATE_FEASIBILITY_FAIL`
- `NL1C7B4_REPAIR18A_IMPLEMENTATION_FAIL`.

No solver tolerance, finite-difference rule, threshold, physical projection variable, branch, lambda, point set, or classification rule may change after the first Repair18a execution.
