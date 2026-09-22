# GE19 Repair27 cancellation-free-parent q20 reconstruction — implementation lock

## Frozen scope

Repair27 is a one-parent substitution of the already frozen Repair24 q20 construction.

The q20 science core remains:

`ge19/repair24_q20_construction.py`

with blob:

`fc271987d1bddcd023cc9c057ddcad036b1d72fb`.

Repair27 changes only the first-order full-history bath parent:

historical v0.77 alpha-coordinate trace

->

frozen Repair26 R1 cancellation-free trace.

No fitted Repair25 scale is used.

## Frozen files

Preregistration:

- file:
  `ge19/repair27_predata_cancellation_free_parent_q20_reconstruction.json`;
- blob:
  `392844e89bab78efdef3c5f8c84f4068cf71cb03`;
- prereg commit:
  `2c711fe61d7a8a98dac1141d314663cc34927dcf`.

Implementation:

- file:
  `ge19/repair27_cancellation_free_parent_q20_reconstruction.py`;
- blob:
  `adbab56e67f765ab5e2b37980abae42312a55b44`;
- implementation commit:
  `bb43045a5a708f34ea6af645a616aa812babee00`.

Dedicated prelock workflow:

- file:
  `.github/workflows/ge19-repair27-prelock-audit.yml`;
- workflow commit:
  `2cbc212d51b40364e12f2d2bd8b9c5439cb540ee`;
- successful prelock run:
  `35721673299`;
- job:
  `106725765558`.

Global GE19 static audits also passed for both preregistration and implementation commits.

## Frozen Repair26 parent

- successful run:
  `35721220889`;
- artifact:
  `10690709843`;
- artifact digest:
  `sha256:33faae31aae0ebe3cc52ac2083193ec8ba3dfe284fb07f06ef2568cad8e3938f`;
- R1 full-history trace SHA-256:
  `608ee0b4c868a701db6976f756b9a551cd9ddffe1e8e4ab37c5cd2361405a6f8`;
- bytes:
  `26643162`;
- a=0.4 bracket:
  `[0.39953919419256334, 0.4000388311146992]`.

## Frozen inherited Repair24 gates

Unchanged:

- X10 initial bridge <= `1e-10`;
- G2 Nx256/Nx512 <= `1e-10`;
- q20 Nq1024/Nq2048 <= `1e-2`;
- q20 Nt64/Nt128 <= `5e-3`;
- z10 Nt64/Nt128 <= `5e-3`;
- exact full-history bracket;
- a=0.4 reconstruction <= `1e-15`;
- finite and complete outputs;
- normalized c2 sqrt(w) cancellation;
- vectorized propagator self-test <= `1e-12`.

No threshold may be changed after execution.

## Stop boundary

The first execution that reaches and emits a valid Repair27 JSON is the science result and must be frozen as PASS or FAIL.

Do not rerun a valid science FAIL.

Repair27 itself does not solve H4/Z21.
