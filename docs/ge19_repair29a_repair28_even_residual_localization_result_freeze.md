# GE19 Repair29A Repair28 even-residual localization — result freeze

## Status

Frozen first Repair29A localization execution.

Classification:

`GE19_REPAIR29A_REPAIR28_EVEN_RESIDUAL_LOCALIZATION_COMPLETE`.

This is an artifact-only localization result. No CLASS run and no new physical tangent calculation was performed.

Repair28 remains frozen:

`GE19_REPAIR28_CANCELLATION_FREE_FULL_STATE_ETA_TANGENT_FAIL`.

## Execution provenance

Workflow run:

`35740993043`.

Job:

`106790392027`.

Execution HEAD:

`71fd14aa873eccf8a8a3c71a742ef376ed1da561`.

Artifact:

- ID: `10700165711`;
- name: `results_bundle_ge19_repair29a_even_residual_localization`;
- digest:
  `sha256:9f3fe1fda7620874020f7673b0dd12d1ea9fc69a4f57f550ec15ac3eb437a93b`;
- size:
  `322954` bytes.

## Frozen output hashes

JSON:

- SHA-256:
  `1fb5431023869f8e7b688236b03b1dc3f89f54336744afa5a4437d14fce7980c`;
- bytes:
  `20006`.

NPZ:

- SHA-256:
  `61e82270d6d15fe79220d3f44b95e60f454149b97024393dcd9471f98961f258`;
- bytes:
  `325154`.

FULL log:

- SHA-256:
  `1fb5431023869f8e7b688236b03b1dc3f89f54336744afa5a4437d14fce7980c`;
- bytes:
  `20006`.

## Frozen parent provenance

Repair29A verified the frozen Repair28 artifact:

- Repair28 workflow:
  `35723905248`;
- artifact:
  `10692716361`;
- artifact digest:
  `sha256:0549f84dc1313c7a34c7d6002939bdc34692b195881145489aa89023e9b9c34d`;
- Repair28 JSON SHA-256:
  `1fd3a4310ea737f6da0d16fa37572c175c26005f6a3ee3f84e5e74f9c82b05a0`;
- Repair28 NPZ SHA-256:
  `101c38d91344d12071ecb343c35769326f80975e013b7d159f573aae73879705`;
- Repair28 FULL SHA-256:
  `694fda61ad3f460e79f32ea35ecf6fda0c2a5933f3230b766485518f82af8cc5`.

Every raw R1/R2 full-state trace was verified against the hash and byte-count provenance frozen inside the Repair28 JSON.

## R1 localization

The global R1 maximum is:

- field:
  `phi_newtonian`;
- lambda:
  `1.25`;
- global normalized even residual:
  `0.006093567316834002`.

Frozen Repair28 limit:

`0.005`.

Only two R1 field/lambda pairs exceed the frozen limit:

1. `phi_newtonian, lambda=1.25`:
   `0.006093567316834002`;
2. `psi_newtonian, lambda=1.25`:
   `0.006093565021327332`.

No other R1 primary-field/lambda pair exceeds the historical Repair28 limit.

For the R1 global-worst pair, the largest per-mode normalized time-global contribution is the lowest requested k mode:

- k:
  `0.020199739172545982 1/Mpc`;
- per-mode normalized even residual:
  `1.4358974884498308`.

The largest absolute even residual for this pair also occurs at the lowest requested k mode, near:

- a:
  `0.7865378718764648`;
- z:
  `0.27139459618679607`;
- absolute even residual:
  `8.62837579163056e-12`.

The very large pointwise normalized values that occur where the tangent crosses near zero are descriptive only and are not used as gates.

## R2 localization

The global R2 maximum is:

- field:
  `phi_newtonian`;
- lambda:
  `5.0`;
- global normalized even residual:
  `0.002932307980192869`.

This is below the frozen Repair28 `0.005` limit.

The corresponding `psi_newtonian, lambda=5.0` value is

`0.0029323067769221473`.

For the two R1 failing pairs at lambda=1.25, R2 gives:

- phi:
  `0.002773848983141527`;
- psi:
  `0.0027738476702882536`.

Thus both historical R1 exceedances move below threshold at R2.

## Precision pattern

For the historical R1 worst pair:

`phi_newtonian, lambda=1.25`,

the ratio is

[
R2/R1 = 0.45520937718674764.
]

For

`psi_newtonian, lambda=1.25`,

[
R2/R1 = 0.455209333219528.
]

Therefore the two actual R1 threshold exceedances decrease by approximately a factor 2.20 when moving from R1 to R2.

The R2 global maximum occurs at lambda=5.0, where the R1 value was smaller:

- phi R1:
  `0.0014639928567112925`;
- phi R2:
  `0.002932307980192869`.

Therefore Repair29A does not claim globally monotone R1-to-R2 even-residual convergence for every lambda.

The next precision test must explicitly include the R2 global-worst lambda as well as the R1 failing lambda.

## Frozen Repair29B target selection

The Repair29A preregistered selector gives exactly:

[
\lambda \in \{5.0,1.25\}.
]

This is the union of:

- R1 global-worst lambda: `1.25`;
- R2 global-worst lambda: `5.0`;
- all R1 above-threshold lambdas: only `1.25`.

No other lambda may be added to or removed from Repair29B.

## Interpretation

Repair29A localizes the Repair28 failure to the Newtonian-potential sector.

The only actual R1 threshold exceedances are `phi_newtonian` and `psi_newtonian` at the smallest signed tangent amplitude, lambda=1.25.

Both fall well below threshold at R2.

However, because the R2 global maximum moves to lambda=5.0, the data do not support a simple monotone statement for every lambda from R1 to R2.

This is why the separately preregistered Repair29B R3 control includes both lambda=1.25 and lambda=5.0.

## Claim boundary

Repair29A:

- does not alter Repair28;
- does not change the 0.005 threshold;
- performs no new CLASS run;
- does not certify the complete eta tangent;
- does not solve reduced Z11;
- does not solve H4/Z21;
- introduces no finite eta and no observational input.

The next licensed step is the already preregistered Repair29B targeted R3 precision closure.
