# NL1C7B4 Repair16 — pre-data exact nonlinear B4 retest on Repair15a state

## Status

Pre-data / pre-run preregistration.

Repair15a locally certified

`NL1C7B4_REPAIR15A_DENSITY_Q_COMPLETED_STATE_CERTIFIED`

and is frozen at commit

`045c5b28b74ff258dbc775057cf3e9387d47b37c`.

Repair16 performs the historical exact nonlinear B4 raw-constraint test on that new certified state representation.

No threshold, source, coefficient, sign, branch, radial point, or state variable may be altered after this preregistration.

## Frozen parent state

Repair15a:

- result JSON SHA-256:
  `596c7b13c4683840bcf40f6850356e179e77f873c3a3b42ba0b54730ae80811d`;
- state NPZ SHA-256:
  `997d0033eeed1f3e60c1907c7938a0ea87a1cf38de6ab860340bd003d18d6e6e`;
- state NPZ bytes:
  `103868`;
- classification:
  `NL1C7B4_REPAIR15A_DENSITY_Q_COMPLETED_STATE_CERTIFIED`.

Historical Repair08 remains immutable and is retained only as provenance for the continuous non-scalar representation.

## Scientific question

After completing the certified first-order density-Q bridge,

`deltaQ_full
 = rho_A delta_A/(Q K_QQ)
 + k^2/[a^2 Q K_QQ][K_B E_A+(2-K_B)chi]`,

does the exact nonlinear eta=0 B4 Hamiltonian and radial-momentum constraint satisfy the original raw threshold

`max epsilon_H <= 1e-7`

and

`max epsilon_M <= 1e-7`

without any additional correction?

## Exact nonlinear evaluator

Repair16 must reuse the frozen Repair09 exact nonlinear constraint semantics:

- same exact nonlinear Q completion;
- same stable Exp K(Q) coordinate;
- same frozen Repair01 non-K Euler-Lagrange dictionary;
- same exact K lapse/shift terms;
- same dust terms;
- same standard background term;
- same pointwise normalized raw epsilon definition;
- same center handling;
- same all-noncenter-point max and RMS metrics.

No Repair10/11/12/13/14 diagnostic rescaling enters the B4 PASS gate.

## Primary and control states

### Primary Nr=256

For each scale `5,10,20 h^-1 Mpc`, load the state directly from the exact frozen Repair15a NPZ.

No primary array may be reconstructed or replaced.

### Control Nr=512

Construct an independent 512-point control from the same continuous parent representation:

1. use the frozen Repair09 generalized Repair08 constructor for all non-density-Q-completion quantities;
2. use the same frozen dense trace and target profile;
3. construct the exact Repair15a Fourier correction
   `F_corr=k^2[a^-2 Q^-1 K_QQ^-1][K_B F_EA+(2-K_B)F_chi]`;
4. inverse-transform it directly onto the 512-point radial grid;
5. add it only to the control `phidot_minus_Q`.

The 512 state is a grid-control representation only and is not written as an official state artifact.

## State anchor

Independently reconstruct the corrected continuous representation at `Nr=256` and compare it to the frozen Repair15a primary NPZ.

Require for every state field and every scale:

`relative L2 <= 1e-12`.

This anchor includes the corrected `phidot_minus_Q`.

## Frozen settings

- `a_i=0.02`
- `eta=0`
- scales `5,10,20 h^-1 Mpc`
- radial grids `Nr=256,512`
- Y families:
  - Simple
  - Exponential
  - Sharp
- beta:
  - 1.0
  - 0.5
  - 0.1
- total exact constraint cases: `54`

## Gates

### R16_G1 — exact Repair15a provenance

Require exact parent JSON/NPZ hashes, certified Repair15a class/gates, metadata marker, frozen dense coverage, exact 128 native k modes, and exact frozen imported code blobs.

### R16_G2 — Repair15a state-anchor reproduction

Require independent continuous reconstruction at `Nr=256` to reproduce every frozen Repair15a state array to relative-L2 `<=1e-12`.

### R16_G3 — exact nonlinear dictionary

Require:

- frozen Repair01 K-dictionary identity;
- all Exp-sector quantities finite;
- exact nonlinear Q reconstruction normalized max error `<=1e-12`.

### R16_G4 — original raw B4 constraints

All 54 exact nonlinear cases must satisfy both

`max epsilon_H <= 1e-7`

and

`max epsilon_M <= 1e-7`.

No alternative perturbative-order criterion may substitute for this gate.

### R16_G5 — two-grid control

For every scale/Y/beta pair, define the historical RMS ratio metric between Nr=256 and Nr=512.

Require both H and M ratios `<=2.0`.

### R16_G6 — claim boundary

Require:

- primary state loaded directly from the certified Repair15a NPZ;
- no constraint projection;
- no coefficient fit/rescale;
- no source insertion/removal;
- no sign change;
- no K clipping;
- no Q linearization;
- no radial-point removal;
- no threshold change;
- no Y/beta/scale selection;
- no nonlinear evolution;
- no finite eta;
- no observational-detection claim.

## Terminal classifications

If G1,G2,G3,G6 fail:

`NL1C7B4_REPAIR16_IMPLEMENTATION_FAIL`.

If provenance/dictionary/claim gates pass but G4 fails:

`NL1C7B4_REPAIR16_REPAIR15A_RAW_CONSTRAINT_FAIL`.

If G4 passes but G5 fails:

`NL1C7B4_REPAIR16_IMPLEMENTATION_FAIL`.

If all gates pass:

`NL1C7B4_REPAIR16_REPAIR15A_EXACT_NONLINEAR_CONSTRAINT_PASS`.

## Interpretation boundary

A Repair16 PASS establishes exact nonlinear eta=0 initial-constraint closure for the frozen density-Q-completed state at the historical B4 threshold.

It does not establish nonlinear time-evolution stability, finite-eta viability, or observational agreement.

A PASS licenses a separately preregistered short-time nonlinear eta=0 evolution stage.

A FAIL must be frozen and localized without changing any historical threshold.
