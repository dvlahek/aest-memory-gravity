# GE19 Repair28 cancellation-free full-state eta tangent — result freeze

## Status

First valid Repair28 science execution:

`GE19_REPAIR28_CANCELLATION_FREE_FULL_STATE_ETA_TANGENT_FAIL`.

This is a scientific/numerical FAIL under the preregistered gates.

It is not an implementation failure.

Successful setup stages included:

- frozen implementation audit;
- frozen Repair26 parent download and hash verification;
- pinned CLASS checkout;
- dependency install;
- frozen AeST + GE15 cancellation-free patch chain;
- CLASS build.

The science step completed and emitted valid JSON/NPZ outputs, then exited with code 2 because one preregistered gate failed.

## Workflow provenance

Workflow run:

`35723905248`.

Job:

`106732873966`.

Execution HEAD:

`8401060842028a4db80ac1bbc948c78dd34960b4`.

Artifact:

- ID: `10692716361`;
- name: `results_bundle_ge19_repair28_full_state_eta_tangent`;
- ZIP digest:
  `sha256:0549f84dc1313c7a34c7d6002939bdc34692b195881145489aa89023e9b9c34d`;
- size:
  `1317009489` bytes.

## Frozen science outputs

JSON:

- SHA-256:
  `1fd3a4310ea737f6da0d16fa37572c175c26005f6a3ee3f84e5e74f9c82b05a0`;
- bytes:
  `16514`.

NPZ:

- SHA-256:
  `101c38d91344d12071ecb343c35769326f80975e013b7d159f573aae73879705`;
- bytes:
  `530980`.

FULL log:

- SHA-256:
  `694fda61ad3f460e79f32ea35ecf6fda0c2a5933f3230b766485518f82af8cc5`;
- bytes:
  `16819`.

Frozen forcing summary:

- SHA-256:
  `12a20cab894f08ab4ceb76b4d52b8f927b9b67038a0d88e196831b1189e991aa`.

Frozen forcing table:

- SHA-256:
  `6fe54caa5a1714eaf145db954c19f2415d02bf31dc518c44ac615aa195b96054`.

## Forcing closure

Repair26 cancellation-free R1 trace is the forcing parent:

`608ee0b4c868a701db6976f756b9a551cd9ddffe1e8e4ab37c5cd2361405a6f8`.

The 1024/2048 forcing control gives:

- relative L2:
  `7.3452194491696035e-09`;
- cosine:
  `0.9999999999999999`.

Both forcing gates pass.

## Grid controls

- requested-k relative miss:
  `0.0`;
- common-background-grid relative mismatch:
  `0.0`.

Both gates pass.

## Lambda-affinity controls

R1:

- maximum tangent affinity:
  `0.0032350146226643416`;
- minimum cosine:
  `0.9999948335306801`.

R2:

- maximum tangent affinity:
  `0.003920019104722244`;
- minimum cosine:
  `0.9999923195162824`.

Frozen gates:

- relative L2 <= `0.005`;
- cosine >= `0.9999`.

Both precision levels pass.

## Even-residual control

R1:

`0.006093567316834002`.

Frozen limit:

`0.005`.

FAIL.

R2:

`0.002932307980192869`.

Frozen limit:

`0.005`.

PASS.

This is the only failed Repair28 gate.

## R1/R2 precision closure

Maximum consensus-state R1/R2 relative L2:

`0.0021596786199411513`.

Frozen limit:

`0.005`.

PASS.

The largest displayed field-level contribution is the Newtonian potential pair:

- phi:
  `0.002159678258007378`;
- psi:
  `0.0021596786199411513`.

Other state components are substantially smaller.

At the initial surface a=0.4, maximum R1/R2 state abs-or-rel mismatch:

`3.757145306980154e-06`.

Frozen limit:

`0.005`.

PASS.

## chi11 precision closure

R1/R2 chi11 relative L2:

`3.0996811715058834e-07`.

Frozen limit:

`0.005`.

PASS by more than four orders of magnitude.

Thus the already important chi11 direction is extremely stable between R1 and R2.

## Gate summary

PASS:

- GE15 cancellation-free patch provenance;
- Repair26 forcing reconstruction;
- forcing quadrature control;
- requested-k matching;
- common background grid;
- R1 lambda affinity;
- R2 lambda affinity;
- R1 tangent cosine;
- R2 tangent cosine;
- R2 even residual;
- R1/R2 consensus-state precision;
- R1/R2 chi11 precision;
- a=0.4 R1/R2 state closure;
- all outputs finite.

FAIL:

- R1 even residual <= 5e-3.

## Interpretation

The first valid Repair28 result does not certify the complete full-state eta tangent because the preregistered R1 even-residual gate is exceeded by about 22%.

However, the failure is highly localized:

- R2 already satisfies the identical even-residual gate;
- R1 and R2 consensus tangents agree within the independent 5e-3 precision gate;
- chi11 is exceptionally stable;
- lambda affinity and tangent direction cosines pass at both precision levels.

This pattern is consistent with a precision-sensitive even-in-lambda contamination of the coarser R1 signed-difference runs, not with a failure of the first-order eta tangent itself. That interpretation remains descriptive until a separately preregistered precision/localization audit is performed.

No Repair28 threshold is relaxed and Repair28 remains FAIL.

## Stop boundary

Do not:

- rerun Repair28 with a relaxed threshold;
- certify the full-state Z11 parent from Repair28;
- construct reduced Z11;
- solve H4/Z21;
- introduce finite eta.

## Licensed next step

A separately preregistered Repair29 may localize the R1 even residual by field and lambda and test its numerical precision scaling using the frozen Repair28 output plus an independently specified tighter precision level.

Repair29 must not alter the Repair28 classification.
