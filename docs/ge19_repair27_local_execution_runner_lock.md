# GE19 Repair27 local execution runner — lock

## Frozen purpose

This runner performs the first Repair27 q20 science execution after the Repair27 preregistration, implementation, and dedicated prelock have passed.

It does not change the Repair24 q20 core, any science threshold, any model parameter, or any Repair22/Repair26 parent state.

## Runner

File:

`ge19/run_local_repair27_cancellation_free_parent_q20_reconstruction.sh`.

Blob:

`e399470546344a5ec861da077690102cd8833fd1`.

Runner commit:

`cb65243947636c9fd50e193c869a01ce8631642b`.

## Frozen Repair27 files

Preregistration blob:

`392844e89bab78efdef3c5f8c84f4068cf71cb03`.

Implementation blob:

`adbab56e67f765ab5e2b37980abae42312a55b44`.

Dedicated prelock workflow blob:

`5ce383c8c47c4f4dc935ddefeccb492e591d8941`.

Repair27 implementation-lock blob:

`5444fc47dbf08d0d3b861ee607efaefd9dd1e83c`.

Frozen Repair24 q20 core blob:

`fc271987d1bddcd023cc9c057ddcad036b1d72fb`.

Repair26 result-freeze blob:

`4a620b1ace8445085d3618db177ca76ef9cadb6a`.

## Frozen Repair26 parent

Successful workflow:

`35721220889`.

Artifact:

`10690709843`.

Artifact digest:

`sha256:33faae31aae0ebe3cc52ac2083193ec8ba3dfe284fb07f06ef2568cad8e3938f`.

R1 full-history cancellation-free trace:

- SHA-256:
  `608ee0b4c868a701db6976f756b9a551cd9ddffe1e8e4ab37c5cd2361405a6f8`;
- bytes:
  `26643162`.

The runner downloads the named artifact only if the frozen trace is not already available locally and verifies the exact trace SHA-256 and byte count before science execution.

## Local frozen inputs

The runner requires the already retained:

- Repair22 JSON/NPZ;
- Repair13 JSON/NPZ;
- GE15 R1 dense accepted-step trace;
- GE15 R1 background trace.

It verifies all frozen Repair22/Repair13 hashes and the GE15 R1 dense trace hash before execution.

## Environment

An active Python virtual environment is mandatory.

If `VIRTUAL_ENV` is empty, the runner exits before science execution.

## Stop rule

The first execution that emits a valid Repair27 JSON is the Repair27 science result.

- exit 0: freeze PASS;
- exit 2 with valid JSON: freeze science FAIL and do not rerun;
- any other exit before valid science JSON: implementation/execution failure only.

No H4/Z21 solve is performed by this runner.
