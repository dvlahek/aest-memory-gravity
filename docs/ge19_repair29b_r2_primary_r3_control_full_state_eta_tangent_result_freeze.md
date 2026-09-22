# GE19 Repair29B R2-primary / R3-control full-state eta tangent — result freeze

## Status

First valid Repair29B science execution:

`GE19_REPAIR29B_R2_PRIMARY_R3_CONTROL_FULL_STATE_ETA_TANGENT_PASS`.

This certifies the Repair28 R2 complete eta-tangent representation as the primary numerical parent, with the separately preregistered targeted R3 precision control.

Repair28 remains a historical FAIL and is not relabelled.

## Workflow provenance

Workflow run:

`35744723602`.

Job:

`106803230666`.

Execution HEAD:

`fb41fee2dae478555fcff562ed125094ce81f5be`.

Artifact:

- ID:
  `10701244502`;
- name:
  `results_bundle_ge19_repair29b_r3_tangent_precision`;
- ZIP digest:
  `sha256:a52c1ff21d6a83cf122db412be40a223996015886e06007a03cf93080c3a1459`;
- size:
  `957385989` bytes.

## Frozen science outputs

JSON:

- SHA-256:
  `081a80fe892f9cddf5ad38a69e43b82c24887e67a8b26162a2d4a229d04f8890`;
- bytes:
  `9129`.

NPZ:

- SHA-256:
  `c97afa5f42e4066239955ac98475c70e37e14c8f0abc373050cc38bbf10c2f81`;
- bytes:
  `143204`.

FULL log:

- SHA-256:
  `e402030a244b2ae26d084a565cef4033abb90fb0cfe307d1c8944f874dd9c5e4`;
- bytes:
  `9434`.

Forcing summary:

- SHA-256:
  `12a20cab894f08ab4ceb76b4d52b8f927b9b67038a0d88e196831b1189e991aa`.

Forcing table:

- SHA-256:
  `6fe54caa5a1714eaf145db954c19f2415d02bf31dc518c44ac615aa195b96054`.

## Frozen selector

Repair29A fixes the target lambda set:

[
lambdain{5.0,1.25}.
]

Tracked pairs:

- `phi_newtonian, lambda=5.0`;
- `phi_newtonian, lambda=1.25`;
- `psi_newtonian, lambda=1.25`.

No target was added or removed after localization.

## R3 precision

R3:

- `tol_perturbations_integration = 6.25e-9`;
- `perturbations_sampling_stepsize = 0.0003125`.

This is the exact factor-two refinement of the frozen R2 precision controls.

## Forcing and grid controls

Forcing 1024/2048 relative L2:

`7.3452194491696035e-09`.

Forcing cosine:

`0.9999999999999999`.

Requested-k relative miss:

`0.0`.

Background-grid relative mismatch:

`0.0`.

All pass.

## R3 tangent precision

Maximum R3 versus frozen R2 same-lambda tangent relative L2:

`0.0032949735424532643`.

Frozen gate:

`0.005`.

PASS.

The maximum occurs in the Newtonian-potential sector at `lambda=1.25`.

Representative values:

- phi, lambda=5.0:
  `0.0012110838842350658`;
- phi, lambda=1.25:
  `0.003294973522104308`;
- psi, lambda=1.25:
  `0.0032949735424532643`.

## R3 even-residual closure

Maximum tracked R3 even residual:

`0.0026472718092593337`.

Frozen historical Repair28 limit:

`0.005`.

PASS.

Tracked precision ladder:

### phi, lambda=5.0

- R1:
  `0.0014639928567112925`;
- R2:
  `0.002932307980192869`;
- R3:
  `0.002071554260687448`.

R3/R2:

`0.7064586239509514`.

R3 <= R2.

### phi, lambda=1.25

- R1:
  `0.006093567316834002`;
- R2:
  `0.002773848983141527`;
- R3:
  `0.0026472718092593337`.

R3/R2:

`0.9543676765925309`.

R3 <= R2.

### psi, lambda=1.25

- R1:
  `0.006093565021327332`;
- R2:
  `0.0027738476702882536`;
- R3:
  `0.0026472663500726238`.

R3/R2:

`0.9543661601999667`.

R3 <= R2.

Therefore every tracked R3 residual is below the original frozen Repair28 threshold and is not larger than its R2 counterpart.

## Gate summary

All Repair29B gates PASS:

- Repair29A provenance and selector exact;
- forcing relative-L2 control;
- forcing cosine control;
- requested-k matching;
- background-grid matching;
- R3/R2 same-lambda tangent precision;
- tracked R3 even residual <= 5e-3;
- tracked R3 even residual <= R2;
- all outputs finite.

## Scientific conclusion

Repair29B confirms that the complete eta tangent is numerically stable at the R2 level under the independently preregistered R3 refinement.

Therefore the certified representation is:

`R2 primary complete eta-tangent representation with targeted R3 numerical control`.

Repair28 remains a historical FAIL because its R1 even-residual gate was exceeded. Repair29B does not alter that historical classification.

## Claim boundary

Repair29B certifies only the complete first-order eta tangent numerical representation.

It does not:

- solve reduced H2/Z11;
- solve H4/Z21;
- introduce finite physical eta;
- change Repair28 thresholds;
- relabel Repair28;
- make observational claims.

## Next licensed step

A separately preregistered reduced H2/Z11 reclosure may now use:

- Repair22 certified reduced Z10/Z20 coordinate system;
- Repair29B-certified R2 full-state eta tangent as the reference/boundary parent;
- the same frozen background and low-mode scope.

Only after reduced Z11 is independently certified may H4/Z21 be constructed.
