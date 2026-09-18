# NL1C7B4 Repair19a — implementation lock

## Status

Locked after implementation and before any Repair19a execution.

Repair19a is diagnostic only. It does not solve the nonlinear constraints or write a state artifact.

## Frozen Repair19 parent

- result-freeze commit:
  `f42b238052d9db58f8eecf7098bd83c231863612`
- result-freeze blob:
  `88e20ee5c1a52258f0b8f40af328a1f6657ca433`
- Repair19 JSON SHA-256:
  `ccf4a362f6a8a791f681d565881ff5728520752b1cbd93d72024b0919e1fe879`
- classification:
  `NL1C7B4_REPAIR19_GAUGE_FIXED_EXACT_NONLINEAR_CONSTRAINT_FAIL`.

## Preregistration

Final pre-run preregistration:

- commit:
  `e022993a8f006c15e8a1ab845d0dc2837d9d4adb`
- file:
  `docs/nl1c7b4_repair19a_predata_gauge_fixed_linear_conditioning_audit.md`
- blob:
  `c1fa7153cfd3621898764b5a0569b2470da65ed6`.

The only preregistration amendment before implementation introduced distinct terminal classes for scientific linear infeasibility versus coordinate disagreement.

## Implementation

- commit:
  `c2f8e7896096066d7e997bb6f41b05efb01706af`
- file:
  `nl1c7b/initial_constraint_certification_repair19a.py`
- blob:
  `3322ed5cb6ed36471b5d700966d9a3fba646d2d8`.

## Frozen science domain

Exactly six lambda=1 canonical parent cases:

- eta=0
- Y=Simple
- beta=1
- scales=5,10,20 h^-1 Mpc
- Nr=256,512.

No nonlinear least-squares solve occurs.

## Frozen constrained subspace

Both coordinate systems span exactly:

- Y4=0
- Qmean=0

inside the same physical `(y_L,q_Rt)` correction space.

### Chain basis

Exactly the frozen Repair19 local chain/path-incidence basis.

### Orthonormal basis

- standard Helmert contrasts over the first four y_L nodes;
- identity on y_L nodes 5..m;
- standard m-dimensional Helmert mean-zero q_Rt basis.

The orthonormal basis is not a new physical ansatz. It is only a coordinate change inside the same constrained subspace.

## Frozen full Jacobian

For every case compute one full physical sparse/grouped SciPy 2-point Jacobian at x=0 with the frozen Repair18a half-band-16 pattern.

Then form algebraically:

- `J_chain=J_x B_chain`
- `J_orth=J_x B_orth`.

No reduced-coordinate finite-difference Jacobian is used.

## Frozen linear solver

For both reduced maps:

- SciPy `lsmr`
- atol=1e-12
- btol=1e-12
- conlim=1e16
- maxiter=10000.

Linear-feasibility gate:

`||F0+J dz||/||F0|| <= 1e-6`

for both bases and all six cases.

Physical-solution agreement gate:

`||dx_chain-dx_orth||/max(||dx_chain||,||dx_orth||) <= 1e-5`.

## Frozen nonlinear probes

Only the orth-basis linearized physical correction is probed.

Exact nonlinear amplitudes:

- 1
- 1/2
- 1/4
- 1/8.

These 24 probes are descriptive and impose no H/M closure threshold.

They must be finite and preserve exact-Q reconstruction to 1e-12.

## Frozen imported blobs

- Repair19 evaluator:
  `2532094b518dfc2990fa0d77d8123d793b0107b3`
- Repair18a evaluator:
  `767199e8ab620f5d6dabd50d0efde9828f22048b`
- Repair16 evaluator:
  `fbd7d24f748fc398638d4eea4b7707801161e52a`
- Repair01 source dictionary:
  `253a0ae2a19a597f06358704ea276c9005973af3`
- Repair09 exact helpers:
  `0cd67cecfbd590cb8819ad37314dc5b49047bc93`
- base B4:
  `8559120dc273be3174eca130ca313ed6ff5acb25`
- Repair08:
  `94fb3f42a7c819b0525860f7344d5dbaff93da19`
- C7A reconstruction:
  `ff383c1ddc2cb2a684e2b5dd11fde0ae811e4fac`.

## Terminal classes

- `NL1C7B4_REPAIR19A_GAUGE_FIXED_LINEAR_CONDITIONING_CHARACTERIZED`
- `NL1C7B4_REPAIR19A_GAUGE_FIXED_LINEAR_INFEASIBILITY`
- `NL1C7B4_REPAIR19A_REDUCED_COORDINATE_NUMERICAL_DISAGREEMENT`
- `NL1C7B4_REPAIR19A_IMPLEMENTATION_FAIL`.

No basis, tolerance, case, physical field, source, coefficient, sign, branch, eta value, point set, or historical threshold may change after the first Repair19a execution.
