# GE03 Repair02 — retained-artifact directory resolution implementation lock

## Status

Repair02 implementation locked before the first Repair02 execution.

The GE03 science implementation remains unchanged.

## Parent implementation state

Repair01 science implementation:

- file: `ge03/weakly_nonlinear_y_memory_cross_source.py`;
- frozen blob:
  `9f8836668d83c6874ca58fd8dc2c7f2de187c1d7`.

Repair01 implementation lock:

- blob:
  `430f39073f6fc3727e9652c62d1a77c9dbdbea79`.

## Repair02 preregistration

Commit:

`c70f559e2285f0d7ad627d1d7bdaa2e25a52b6df`.

File:

`docs/ge03_repair02_predata_artifact_directory_resolution.md`.

Frozen blob:

`67b836e3f2a1a1070fb4b501a4d7d9c8790bcd74`.

## Repair02 implementation

Commit:

`007c051e20824d936c9c5075db66276147786248`.

File:

`tools/ge03_resolve_v077_artifact_dir.sh`.

Frozen blob:

`d3fe4deb838245b91e5600bbbee7362366f9bb3e`.

## Exact behavior

Given a workflow artifact download root, the resolver:

1. recursively searches for `v076_v077_base_trace.dat`;
2. requires exactly one match;
3. takes the containing directory as the science artifact directory;
4. requires all plus/minus traces for
   `lambda={10,5,2.5,1.25}`
   in that same directory;
5. prints the resolved directory path and nothing else on success.

It does not read or modify trace content.

## Frozen science content

Unchanged:

- v0.77 artifact ID `10090367181`;
- v0.77 artifact digest
  `sha256:24b97e5738eb07be4f12d433ff5f9fe22249e199e186d5617aca5dc81f748378`;
- exact GE03 operator implementation;
- all lambdas, beta values, modes, phases, grids, finite-difference steps and gates;
- PASS/FAIL classification rule;
- claim boundary.

## Runner rule

After this lock, the workflow may be changed only to:

- verify this Repair02 preregistration and resolver blob;
- call the resolver on the downloaded artifact root;
- pass the returned directory unchanged to the locked GE03
  `--artifact-dir` argument.

No other GE03 code or science setting may change.

The first workflow execution after that runner-only change is eligible to produce the first GE03 science classification.
