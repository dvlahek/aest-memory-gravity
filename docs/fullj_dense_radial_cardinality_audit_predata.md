# Full-J dense radial same-environment cardinality audit — pre-data declaration

## Purpose

The completed CLASS-residual R2 milestone is locked as

`FULLJ_DENSE_RADIAL_CLASS_RESIDUAL_R2_FAIL`

at result-lock commit

`4d87865a8e45985388dfab2b9d8922faa9290f7f`.

The completed run combines 21 stored K2 R2 nodes from the preceding dense milestone with 20 new H3 R2 nodes produced from a 41-mode corrected-CLASS data object. Corrected CLASS itself reproduced the stored K2 reference values exactly, but the nonlinear R2 nodes were not explicitly rerun at the same physical K2 values inside the 41-mode data object.

This audit tests only that possible cardinality/state-plumbing dependence. It does not retune, repair or reclassify either historical dense FAIL.

## Frozen hypothesis

For a custom single-mode periodic embedding, all inactive CLASS histories have zero real-space basis amplitude. Therefore the direct R2 result at a fixed physical k should be invariant, within numerical precision, to using the previous 21-history data object or the current 41-history data object.

If this invariance fails, the radial jaggedness seen in the completed K3 diagnostic cannot yet be interpreted physically.

If it passes, the inactive-history cardinality hypothesis is rejected and the observed radial/saturation structure can be treated as a property of the frozen single-mode construction rather than a data-object plumbing artifact.

## Required ancestry and local inputs

Require as ancestors:

- completed dense signed-transfer FAIL result: `55495cc968082f1cf6638785f7609c787971835c`
- completed CLASS-residual R2 FAIL result lock: `4d87865a8e45985388dfab2b9d8922faa9290f7f`
- R2 evolving-Weyl result: `1f42f88e9724c58d2d242a65ca7266a207e4a0f8`
- R1 zero-safe transfer phase PASS: `20679c5274e936037c226904d40c9d6779b00a49`

Require local completed JSON files:

- `results/fullj_dense_radial_weyl_extension.json`, classified exactly `FULLJ_DENSE_RADIAL_WEYL_EXTENSION_FAIL`
- `results/fullj_dense_radial_class_residual_r2.json`, classified exactly `FULLJ_DENSE_RADIAL_CLASS_RESIDUAL_R2_FAIL`

The latter must preserve the completed gate state with G1-G6 and G11 true and G7-G10 false.

## Frozen environment and numerics

Use the same isolated corrected CLASS dense-k64 environment as the completed CLASS-residual R2 run:

- pinned CLASS commit `e85808324f51fc694d12e3ed7439552a3c3f9540`
- identical corrected AeST patch chain
- `_MAX_NUMBER_OF_K_FILES_=64` as a technical output-capacity repair only
- one 41-value `k_output_values` request on the frozen K3 grid.

Freeze

- `sigma=0`
- `kind=simple`
- `beta0=1.0`
- `NX=128`
- `NSTEP=4096`
- `n_embed=10`
- `z=[6,5,4,3,2,1.5,1,0.5,0.2]`.

No physics parameter or R2 equation may change.

## Frozen audit nodes

Rerun exactly six existing K2 physical nodes inside the same 41-mode K3 data object:

`K_AUDIT/h = [0.035, 0.040, 0.100, 0.150, 0.1625, 0.175] Mpc^-1`.

The first two bracket the low-k region in which the new odd-eighth H3 nodes showed large saturation residuals. The remaining four sample the central and low-z jagged region of the completed K3 residual diagnostic.

No node may be changed after rerun outputs are seen.

## Probe definition

At each audit k use exactly the same deterministic probe rule as the completed dense milestones:

- amplitude: log-linear interpolation of the original six locked `MODE_AMP` values in `log k`
- phase: linear interpolation of the original six locked phases in k
- periodic embedding index `n_embed=10`
- transfer extraction removes the applied phase and divides out the applied amplitude.

## Comparisons

For each of the six nodes and nine redshifts compare the new 41-history rerun against the stored 21-history direct result:

- real Weyl transfer `Re(T_W)`
- derived Weyl power using the same primordial normalization
- saturation residual `eps_sat`
- corrected CLASS reference.

Also report the rerun imaginary transfer and solver/metric health.

Pointwise relative transfer ratios are not used as gates because the signed transfer can cross zero. Use zero-safe vector norms across redshift and across the complete 54-cell audit set.

## Frozen gates

### C-G1 — provenance/setup

All required commits must be ancestors. Both local completed JSONs must retain their locked classifications/gate states. Require the exact six-node set, 41-node K3 grid, reference member, redshift list, `NX=128`, `NSTEP=4096`, and `n_embed=10`.

### C-G2 — 41-mode CLASS reference consistency

At the six audit nodes and nine redshifts, compare the new 41-mode corrected CLASS reference against the stored 21-mode corrected CLASS reference. Require

- median zero-safe scalar relative difference <= `1e-8`
- maximum zero-safe scalar relative difference <= `1e-5`.

### C-G3 — rerun solver/metric health

All six reruns must be finite at all nine checkpoints with

- canonical residual <= `1e-10`
- Hamiltonian/momentum/shear residuals <= `1e-8`.

### C-G4 — rerun phase health

Across the 54 rerun transfer cells require

- global `||Im T||_2/||T||_2 <= 1e-8`
- maximum absolute `|Im T| <= 1e-8`
- real projection changes power by at most `1e-12` relatively.

### C-G5 — transfer cardinality invariance

Let `T41` denote the new rerun real transfer and `T21` the stored old direct transfer. Require

- global `||T41-T21||_2 / max(||T21||_2,tiny) <= 1e-5`
- maximum of the six per-k redshift-vector relative L2 differences <= `5e-5`.

### C-G6 — power cardinality invariance

Using identical primordial normalization, require

- global power relative L2 difference <= `1e-4`
- maximum of the six per-k redshift-vector power relative L2 differences <= `5e-4`.

### C-G7 — saturation cardinality invariance

Compare the rerun `eps_sat` values with the stored 21-history `eps_sat` values at the same 54 cells. Require

- maximum new rerun `eps_sat <= 2e-2`
- maximum absolute old/new `eps_sat` difference <= `1e-4`
- global old/new saturation relative L2 difference <= `1e-3`.

This gate does not extend the 3D saturated-closure license. It tests only if the earlier K2 saturation result is reproduced in the 41-history data object.

## Classification

PASS:

`FULLJ_DENSE_RADIAL_CARDINALITY_AUDIT_PASS`

FAIL:

`FULLJ_DENSE_RADIAL_CARDINALITY_AUDIT_FAIL`

INCOMPLETE:

`FULLJ_DENSE_RADIAL_CARDINALITY_AUDIT_INCOMPLETE`

## Interpretation lock

PASS means the number of inactive corrected-CLASS histories does not explain the completed K3 radial/saturation structure at the audited nodes. The existing CLASS-residual R2 FAIL remains a FAIL and no continuous-power or lensing license is granted.

FAIL means the 21-history and 41-history direct R2 constructions are not numerically equivalent at fixed physical k. In that case the completed G7-G10 failures must not be given a physical radial interpretation until the cardinality dependence is repaired.

Regardless of outcome keep

- `THREE_D_BOUNDED_CONTINUOUS_WEYL_POWER_LICENSED=False`
- `THREE_D_CONTINUOUS_WEYL_POWER_LICENSED=False`
- `EVOLVING_WEYL_POWER_LICENSED=False`
- `ACT_LIKELIHOOD_LICENSED=False`
- `OBSERVATIONAL_CLAIM_LICENSED=False`.