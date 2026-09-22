# GE19 Repair30 local execution runner — lock

## Status

Repair30 local execution path is frozen.

Science implementation remains:

`ge19/repair30_reduced_h2_z11_reclosure.py`.

No H4/Z21 code is present in this runner.

## Frozen runner

File:

`ge19/run_local_repair30_reduced_h2_z11_reclosure.sh`.

Blob:

`130ec26365667a76b32108a0bbfcc425f78c3233`.

Runner commit:

`741e418d677161d65dafc5adbd0c1f7503c69d3b`.

Global static audit for the runner:

- run:
  `35748043859`;
- conclusion:
  `success`.

## Frozen Repair30 science contract

Preregistration:

- blob:
  `264b52832e762dd2010df1eba83e5f2c1a4d8874`;
- commit:
  `5fd14e9dc46ced04a838d79cc3b47319c4e4f22f`.

Implementation:

- blob:
  `2ce2bf7ccd5bf48504c619500d12d4eb03bfe259`;
- commit:
  `91e59269dbfd4476230cf8cc25c5579b44691b8d`.

Dedicated prelock:

- blob:
  `3ad421859cb6745c0708fb247222b135381cf1db`;
- commit:
  `55e690ebe1414b0929eb75c72ea1b75b4ba9f4a3`;
- successful run:
  `35747790884`;
- job:
  `106813756378`.

Implementation lock:

- blob:
  `4f4d177cb6df5ab0b10f1c7c8334b579549bc22f`;
- commit:
  `937a0681c07c46eacfc0c021ebd389edb9378840`.

## Lean R2 reference packaging

Packaging workflow:

- file:
  `.github/workflows/ge19-repair30-r2-reference-pack.yml`;
- blob:
  `1b837aaa649a4eac928691e8ae07c18511e6dd14`;
- workflow commit:
  `708c0f345ac8baa46cc6188468db585fed4c5651`;
- successful run:
  `35747827610`.

Lean artifact:

- ID:
  `10703327330`;
- name:
  `ge19_repair30_r2_reference_only`;
- ZIP digest:
  `sha256:a3f531235f6953e5d6d022948eb91fe196c238b1729e61cf577a078d5fa59043`;
- artifact size:
  `516826` bytes.

Contained frozen R2 reference:

- file:
  `ge19_repair28_cancellation_free_full_state_eta_tangent.npz`;
- SHA-256:
  `101c38d91344d12071ecb343c35769326f80975e013b7d159f573aae73879705`;
- bytes:
  `530980`.

This is byte-identical to the Repair28 R2 NPZ certified as the primary complete eta-tangent representation by Repair29B.

The packaging workflow changes no science content.

## Required local parents

The runner requires the already frozen local results:

- GE15 R1 dense accepted-step trace;
- Repair13 JSON/NPZ;
- Repair22 JSON/NPZ;
- Repair27 JSON/NPZ.

Every file is hash-checked before Repair30 science starts.

If the lean R2 reference is absent locally, the runner downloads only artifact `10703327330` through run `35747827610`.

## Environment requirement

The repository virtual environment must be active:

`source .venv/bin/activate`.

If `VIRTUAL_ENV` is absent, the runner stops before science with exit code 5.

## Stop rule

The first execution that emits a valid

`ge19_repair30_reduced_h2_z11_reclosure.json`

is the Repair30 science result.

- exit 0:
  freeze PASS;
- exit 2 with valid JSON:
  freeze scientific FAIL and do not rerun the same test;
- any other exit before a valid science JSON:
  implementation/execution failure only and may be repaired without changing the frozen science contract.

No Repair30 threshold may be changed after a valid science result.
