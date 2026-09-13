# Full-J direct-CLASS spectral-fringe extractor-equivalence audit

Date: 2026-09-13

## Motivation

The completed R3 direct-CLASS spectroscopy/GR-control run preserved the preregistered formal classification

`FULLJ_CORRECTED_CLASS_SPECTRAL_FRINGE_NUMERICAL_CONTROL_FAIL`

because DG-G2 (reproduction of the previously locked source-decomposition `W_CLASS` anchors) failed. All other preregistered gates passed: exact provenance/setup, dense-versus-sparse requested-k invariance, dense-grid health, fine-grid spectral structure, and AeST specificity against the matched GR control. The R3 result itself is not reclassified.

The failed DG-G2 comparison joined two numerically different extraction paths that had been assumed equivalent before data inspection:

1. the new raw direct CLASS history observable `W_direct(k,z)=phi(k,z)+psi(k,z)` read from `get_perturbations()`;
2. the historical source-decomposition `W_CLASS`, formed after CLASS-history spline loading, tagged spatial-basis reconstruction, Fourier extraction, and +/- tagged pair response.

The present audit asks only if these extraction paths are numerically equivalent on the already frozen 15 anchors. It introduces no new physical k values and no new science threshold from the R3 AeST/GR comparison.

## Frozen inputs

The audit must preserve and verify the following existing results and files:

- original direct-CLASS preregistration and its R1/R2/R3 technical repairs;
- R3 JSON/NPZ result and formal `NUMERICAL_CONTROL_FAIL` classification;
- locked source-decomposition JSON/NPZ and its historical classification;
- the same corrected CLASS git head and patched `source/aest_memory.c` SHA used by R3;
- memory forcing off (`aest_memory_enabled=no`, `aest_eta=0`);
- the same 15 anchor k/h values and redshifts `[6,5,4,3,2,1.5,1,0.5,0.2]`.

No historical FAIL is reclassified by this audit.

## Extractors

For every frozen anchor and redshift, evaluate four arrays from the same corrected AeST linear solution:

- **E1 raw-a direct**: R3 direct `phi+psi`, using scale-factor interpolation exactly as in the completed R3 calculation.
- **E2 raw-tau direct**: `phi+psi` evaluated from the same raw CLASS history at the exact conformal times corresponding to the frozen redshifts, with no spatial reconstruction.
- **E3 bridge-tagged reconstruction**: the historical bridge path: CLASS histories -> temporal splines -> tagged spatial basis -> Fourier coefficient -> +/- pair response, but run as a dedicated extractor audit with no nonlinear metric correction entering the quantity being compared.
- **E4 frozen source reference**: locked source-decomposition `merged__W_CLASS` on the same 15 anchors and redshifts.

The audit must also save pointwise differences and per-redshift relative L2 values for all relevant pairs.

## Predeclared numerical gates

All tolerances below are fixed before running the audit.

### EX-G1 provenance and frozen identity

Exact ancestry/provenance files are present, the R3 result remains `FULLJ_CORRECTED_CLASS_SPECTRAL_FRINGE_NUMERICAL_CONTROL_FAIL`, the same 15 anchors/redshifts are used, and no science grid or R3 gate is changed.

### EX-G2 direct coordinate equivalence

E1 and E2 must agree to

- global relative L2 <= `2e-5`;
- maximum per-anchor relative L2 <= `5e-5`.

Failure means the new direct extractor has a time-coordinate/interpolation inconsistency and the audit classification is numerical-control failure.

### EX-G3 bridge extractor self-equivalence

E3 must reproduce E4 to

- global relative L2 <= `2e-5`;
- maximum per-anchor relative L2 <= `5e-5`.

Passing EX-G3 means the historical frozen source-decomposition reference is reproducible by its own extraction path.

### EX-G4 direct-versus-bridge discrepancy localization

Compute E1-E3 and E1-E4 per anchor and redshift. This gate is descriptive, not a requirement for either extractor to equal the other. The audit must report:

- global and per-anchor relative L2;
- per-redshift relative L2;
- maximum absolute discrepancy location `(k/h,z)`;
- sign disagreements;
- correlation of second differences at z=0.2 over the three frozen five-point windows.

### EX-G5 direct signal controls preserved

Using the already completed R3 arrays only (no refit and no rerun), require that the following R3 facts are reproduced exactly from the locked NPZ/JSON:

- dense-versus-sparse AeST anchor difference = 0 within stored precision;
- all 51/15/51 arrays finite;
- z=0.2 extrema counts `[10,11,9]`;
- `kappa_AeST=0.403340049182677`;
- `kappa_GR=0.00016609014215828433`;
- `R_spec=2428.440628332372`.

This gate does not override the historical R3 classification.

## Predeclared classifications

If EX-G1, EX-G2, EX-G3 and EX-G5 pass while E1 differs materially from E3/E4 beyond the original DG-G2 tolerance:

`FULLJ_CLASS_FRINGE_EXTRACTOR_MISMATCH_CERTIFIED`

Interpretation: the R3 direct signal is numerically self-consistent and the failed DG-G2 gate arose because the direct and historical bridge-tagged observables are not numerically equivalent. This licenses a follow-up equation-level audit of the origin of the difference. It does not itself license a new-mode or observational claim.

If EX-G1, EX-G2 and EX-G5 pass but EX-G3 fails:

`FULLJ_CLASS_FRINGE_FROZEN_REFERENCE_NOT_REPRODUCED`

Interpretation: the historical source-decomposition reference cannot be recreated by its own extraction chain and must not be used to reject the direct result.

If EX-G2 fails, or provenance/finiteness fails:

`FULLJ_CLASS_FRINGE_EXTRACTOR_NUMERICAL_CONTROL_FAIL`

If all extractors agree within the original DG-G2 tolerance despite the frozen R3 summary reporting failure:

`FULLJ_CLASS_FRINGE_R3_COMPARISON_IMPLEMENTATION_DEFECT`

Otherwise:

`FULLJ_CLASS_FRINGE_EXTRACTOR_AUDIT_INCOMPLETE`

## Physics interpretation rule

A formal failure in an inherited comparison is not interpreted automatically as absence of physics. A discrepancy becomes physically interesting only after the relevant numerical path is independently reproduced and shown invariant to requested-k list, coordinate interpolation, provenance, and matched GR control. If the direct AeST fine-k structure remains numerically clean while a reduced/bridge extractor fails equivalence, the discrepancy is treated as a candidate clue about what the reduced observable removes, mixes, or reconstructs. No new-physics claim is made until an equation-level mode/dispersion audit produces a held-out prediction.