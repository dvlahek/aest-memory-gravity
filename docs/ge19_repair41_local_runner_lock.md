# GE19 Repair41 local direct fine-grid target runner — lock

## Status

The first local Repair41 execution path is frozen.

Runner:

`ge19/run_local_repair41_direct_fine_grid_target_source_reconstruction.sh`.

Runner commit:

`4de148a02d8a71703b6c5fe67b8ec610973e6e41`.

Runner blob:

`2f849033f378a476e73261d302953cf929f2ad93`.

Static runner audit:

- run:
  `35909013475`;
- job:
  `107343824000`;
- conclusion:
  `success`.

## Bound Repair41 contract

Preregistration:

- commit:
  `70caf9cdc460c8b1123677ae4a669ae58445cc90`;
- blob:
  `bc07d4130a22906496588f4bc539b19119b21885`.

Implementation:

- commit:
  `71fd90acb593201294c02f1f435a3652edc0ed0b`;
- blob:
  `b04d39d650afaa0a4657d4d96232ea67a35d725d`.

Implementation lock:

- commit:
  `2355763775fc026816929c17a115bab62f498616`;
- blob:
  `7079974b8d3dd7fad24fd196ca5c7ac0eea79864`.

Dedicated prelock:

- workflow commit:
  `faf3fd436265325cfc50e7f3e9e3fd2f2f85d9c3`;
- workflow blob:
  `f1ab26164b565677f757edab9d02f078ece27743`;
- run:
  `35908804106`;
- job:
  `107343128775`;
- conclusion:
  `success`.

Frozen Repair40 parent:

- freeze commit:
  `bd9446feccb28779fa3f59bd0206e18d2ebaed4e`;
- freeze blob:
  `d2dfd61d765a8fd3c96382bd19b89b7295c841f5`;
- JSON/FULL SHA-256:
  `f5618344db31328dc4e680eb41bb6a715da3fbe7e54ddff3cb53bc027386bf44`;
- NPZ SHA-256:
  `06c7799787abcc510259c626bcb9ca925f96efce13c7949a89690f243fbf01b5`;
- outer runner SHA-256:
  `112bffc28a638bff5a1148795068111475ee4781a923432b6b52cd5a34ec72f4`.

## Immutable external parents

The runner retrieves, or reuses if already present:

### Repair26 full-history cancellation-free bath trace

- workflow run:
  `35721220889`;
- artifact bundle:
  `results_bundle_ge19_repair26_cancellation_free_full_history_bath_boundary`;
- expected file:
  `ge19_repair26_R1_full_history_trace.dat`;
- SHA-256:
  `608ee0b4c868a701db6976f756b9a551cd9ddffe1e8e4ab37c5cd2361405a6f8`;
- bytes:
  `26643162`.

### Repair28 R2 eta-tangent reference

- workflow run:
  `35747827610`;
- artifact bundle:
  `ge19_repair30_r2_reference_only`;
- expected file:
  `ge19_repair28_cancellation_free_full_state_eta_tangent.npz`;
- SHA-256:
  `101c38d91344d12071ecb343c35769326f80975e013b7d159f573aae73879705`;
- bytes:
  `530980`.

## Execution rule

Repair41 directly reconstructs the parent chain needed by both mandatory
Repair40 targets on Nt382 and Nt763.

It then evaluates the target sources at the original Nt128 factor-1 Radau
stage coordinates by exact fine-grid integer-node lookup.

PCHIP and Akima are frozen comparison representations only.

A valid result may route to:

- `DIRECT_TARGET_REFERENCE_RESOLVED`;
- `DIRECT_TARGET_REFERENCE_UNRESOLVED`.

`IMPLEMENTATION_FAIL` is reserved for frozen binding, formula adapter,
stage-node mapping or finiteness failures.

Repair41 cannot solve or certify Z21 and cannot license lensing.
