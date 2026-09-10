# D2C6C–D2C6D resolution postmortem and canonical project state

Date: 2026-09-10

This document is the canonical record of the D2C6C/C3 debugging sequence, the resolved causes, the certified repairs, and the current licensed scope for the AeST finite-memory program on branch `v053-exp-normalization-corrected`.

## 1. What looked broken

The original D2C6C eta=0 nonlinear-memory tangent test repeatedly failed C3, even though the nonlinear base trajectories, constraints, bath-order convergence, time convergence, and spatial convergence were healthy. Historical R2/R3 C3 mismatches were about 8.7–8.8%, and later full-history CLASS references made the discrepancy even larger.

The repeated failures were not treated as disposable. Historical FAILs remain part of the record. Repairs were separately preregistered before new target outputs.

## 2. First localization: the bath bridge itself was not the problem

A direct CLASS/offline bath-bridge audit compared the CLASS bath states with the offline real-space bath representation under the exact algebraic map

`z_j = omega_j q_j / (k sqrt(w_j))`.

After technical common-domain repairs, the bath state bridge and bath residual bridge passed. The transformed CLASS and offline bath dynamics agreed when initialized from the same state. Therefore the Drude bath ODE, the `q <-> z` mapping, and the offline `bath_advance` implementation were exonerated as the main cause of C3.

## 3. Root cause A: passive eta=0 bath states contaminated the CLASS integrator

A direct zero-coupling audit compared

- `memory=no`, eta=0
- `memory=yes`, eta=0

inside the same CLASS build for all six target k modes and for alpha, E, and theta.

Because the physical memory closure is multiplied by eta, the two runs must be identical at eta=0. Instead, the old implementation produced a large and highly structured discrepancy only for the highest-k mode, approximately

`alpha(memory=yes, eta=0) / alpha(memory=no) ~= 1.53174`.

The cause was numerical, not conceptual: the eta=0 calculation still allocated the 39-node bath q/p state pairs, adding 78 very fast passive variables to CLASS's NDF15 system. Even though the bath was physically decoupled, those variables entered the coupled adaptive integration/Newton/error-control problem and changed the numerical trajectory of the core AeST state.

### Repair

For physical eta=0, the passive bath states are no longer allocated/evolved inside the CLASS core state vector. The eta=0 memory response is instead reconstructed from the uncontaminated core chi history using the separately validated bath evolution. Finite-positive-eta physical closure remains unchanged.

### Certification

After this repair, the zero-coupling audit returned exact equality to printed precision for all 18 comparisons (6 k modes x alpha/E/theta):

`ZERO_COUPLING_PASS=True` and `REL_L2=0` for every tested field/mode.

This removed the spurious factor ~1.53174.

## 4. Root cause B: C3 compared two different linearized systems

After root cause A was removed, a zero-safe C3 reference still failed. A scale/sign audit showed that the mismatch was not a single normalization factor or sign: best-fit signed scales varied strongly by mode and some response shapes were almost orthogonal.

The implementation review then found the second and decisive issue. The original D2C6C preregistration defined the C3 tangent with external CLASS metric/matter fields held fixed at eta=0. However, the old CLASS +/-lambda reference was produced by rerunning the full coupled CLASS system. The memory perturbation therefore changed the AeST matter variables and metric through Einstein feedback, which then fed back into the response.

The offline D2C6C tangent intentionally did not contain this full Einstein/matter feedback. The old C3 comparator was therefore comparing different linearized problems.

### Repair: R6 frozen-metric reference

R6 replaced the full-CLASS +/-lambda comparator by a direct frozen-metric CLASS-variable tangent reference. It uses the same frozen eta=0 background/metric/matter source data and the same order-39 tauH0=1 memory forcing, and integrates the CLASS-variable tangent system directly.

Preregistration commit:
`520e0f265a15413c2ea3e61f0739171b0e503bb7`

Implementation/workflow head:
`28ccf6d776e19d63b104d6e9186999994a9b6b0b`

Run:
`34500820787`

R6 result:

- alpha C3 relative L2 = `2.94328e-5`
- E C3 relative L2 = `3.75802e-5`
- chi C3 relative L2 = `2.94328e-5`
- frozen gate = `5e-3`

Classification:
`C3_R6_FROZEN_METRIC_TANGENT_PASS`

Thus the eta=0 tangent construction, bath forcing, and offline canonical tangent agree once the same linearized problem is compared on both sides.

## 5. Formal D2C6C recertification: R7

R7 reran the full original D2C6C all-27 certification with the corrected R6 C3 reference and otherwise unchanged C1-C8 gates, nonlinear completion family, resolutions, bath orders, and tolerances.

Preregistration commit:
`28883005c9c7e955443ad7e145b0f22179b42f5a`

Implementation/workflow head:
`a6c61e275ce2ab949dd108ac2b326a4ed617ebcc`

Run:
`34502078991`

Result:

- all 27/27 nonlinear completion members healthy
- all C1-C8 gates true
- C2 bridge and flux-Jacobian checks passed with large margin
- corrected C3 passed
- constraint, bath-order, time, and spatial convergence gates passed

Most important formal output:

`FINITE_POSITIVE_ETA_NONLINEAR_MEMORY_LICENSED=True`

This is the point at which the eta=0 tangent/nonlinear-memory certification was formally complete.

## 6. First physical finite-positive-eta continuation: D2C6D

After R7 licensed eta>0, a new preregistered retained scalar-current finite-eta test was run. This is not claimed as the complete nonlinear AeST+memory theory because direct nonlinear memory Einstein stress and fully dynamical matter/metric backreaction remain outside this retained scalar-current stage.

Frozen eta ladder:

- eta = 2^-8 = 0.00390625
- eta = 2^-7 = 0.0078125
- eta = 2^-6 = 0.015625

Primary coverage: 27 completion members x 3 eta values = 81 trajectories.

Preregistration commit:
`fc120a6666c751139cc1fc794f148c90e05938a5`

Additional pre-output conservative control-health clarification:
`23bd7c3c77c2fe1a848bf3d3d3213b5e2bfd4644`

Implementation commit:
`3102e56676277f46b947db31b8ed5a1fcd431d5f`

Workflow head:
`0e596eb342e56fae56287017876fb2ee07c4c2b4`

Run:
`34507347610`

Artifact:
`10165882118`

Classification:
`NL1C6D2C6D_FINITE_POSITIVE_ETA_RETAINED_SCALAR_CURRENT_PASS`

All D1-D8 gates were true.

Key numbers:

- finite-eta source identity elliptic residual = `3.722320738534e-15`
- source increment residual = `0`
- eta -> 0 tangent continuation max = `1.652607142832e-4` (gate `5e-3`)
- worst bath-order displacement convergence = `7.300833467277e-4` (gate `1e-2`)
- worst time displacement convergence = `8.226445166693e-4` (gate `2e-3`)
- worst space displacement convergence = `8.424055195685e-4` (gate `5e-3`)
- all 81 primary finite-eta trajectories healthy
- all tested constraints remained approximately 1e-15 to 1e-14
- `min(1+j_eff)` remained positive for every tested case

The finite-eta displacements scale almost linearly across the dyadic eta ladder, and the smallest eta converges cleanly to the independently certified eta=0 tangent.

Formal output:
`LARGER_AMPLITUDE_RETAINED_ETA_STEP_LICENSED=True`

Scope guard remains:
`FULL_NONLINEAR_OR_OBSERVATIONAL_STEP_LICENSED=False`

## 7. What is now established

Within the retained scalar-current AeST memory model and the frozen test family, we now have a continuous validated chain:

1. stable physical nonlinear eta=0 trajectories for all 27 completion members;
2. direct CLASS/offline bath-equation equivalence;
3. exact eta=0 zero-coupling invariance after removal of passive bath-state contamination;
4. independently validated eta=0 memory tangent against a correctly matched frozen-metric CLASS-variable reference;
5. full D2C6C all-27 C1-C8 certification;
6. first physical finite-positive-eta continuation over three positive eta values and all 27 completion members;
7. numerical convergence in bath order, time resolution, and spatial resolution at finite eta;
8. clean eta -> 0 recovery of the certified tangent.

This resolves the C3/D2C6C implementation crisis. The repeated historical C3 failures were caused by two implementation/reference errors, not by a demonstrated conceptual inconsistency of the retained memory construction.

## 8. What is not yet established

Do not overclaim the following:

- no full nonlinear AeST + memory Einstein-stress completion has yet been certified;
- no fully dynamical metric/matter finite-eta backreaction stage has yet been certified;
- no observational likelihood/detection has been established by D2C6C/D2C6D;
- no larger-amplitude retained eta scan has yet been performed beyond eta=0.015625;
- Nature/Nature Physics-level observational relevance must still be established separately.

## 9. Immediate next licensed step

The next technically licensed experiment is a separately preregistered larger-amplitude finite-positive-eta scan within the same retained scalar-current model. Its purpose should be to locate the onset of measurable nonlinear departure from the tangent regime and characterize saturation/response curvature while preserving the already frozen physical equations. It should not be used to retrospectively alter the successful D2C6D gates.

Only after that retained-amplitude behavior is understood should the program move to the missing full nonlinear metric/matter/Einstein-stress completion or to observational projection, each under its own preregistration and scope statement.

## Canonical interpretation

The correct concise interpretation of the current state is:

**The C3/D2C6C problem is solved. Two implementation/reference mismatches were isolated and repaired under preregistered diagnostics. The repaired eta=0 tangent passes, the full all-27 D2C6C certification passes, and the first physical finite-positive-eta retained scalar-current continuation passes for 81 trajectories with clean eta->0, bath-order, time, spatial, constraint, and positivity checks. The retained model is now licensed for a larger-amplitude eta scan, but not yet for claims of full nonlinear AeST+memory or observational detection.**
