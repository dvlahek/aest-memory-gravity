# GE19 Repair26 cancellation-free full-history bath boundary — result freeze

## Status

First valid Repair26 science execution:

`GE19_REPAIR26_CANCELLATION_FREE_FULL_HISTORY_BATH_BOUNDARY_PASS`.

Frozen route:

`CANCELLATION_FREE_FULL_HISTORY_BATH_BOUNDARY_CERTIFIED`.

Successful workflow:

- run: `35721220889`;
- job: `106724330805`;
- head: `32b1808ab3b8d59a54412f1eecf6a28b5bbf5829`;
- conclusion: `success`.

The earlier run `35721094832` remains a frozen implementation failure caused only by the missing SymPy dependency and produced no Repair26 science result.

## Frozen artifact

Artifact:

- ID: `10690709843`;
- name: `results_bundle_ge19_repair26_cancellation_free_full_history_bath_boundary`;
- ZIP digest:
  `sha256:33faae31aae0ebe3cc52ac2083193ec8ba3dfe284fb07f06ef2568cad8e3938f`;
- size: `34735591` bytes.

Science outputs:

- JSON:
  `80ba0b5927217be000991c82b4afb5f39b5e0ff369bc9b630a88ec11dabdedb6`,
  `6542` bytes;
- NPZ:
  `ba6265af81e440c610a4ac4805e7c55b45f3bd681e14731b8d067e47a979fdd8`,
  `787203` bytes;
- FULL log:
  `80ba0b5927217be000991c82b4afb5f39b5e0ff369bc9b630a88ec11dabdedb6`,
  `6542` bytes.

Frozen generated histories:

- R1 full-history cancellation-free trace:
  SHA-256 `608ee0b4c868a701db6976f756b9a551cd9ddffe1e8e4ab37c5cd2361405a6f8`,
  bytes `26643162`;
- R2 full-history cancellation-free trace:
  SHA-256 `a3fee42d20b94813c2f5e58ca9c77237e7cf7ebf313dac937bdad750554d8f5f`,
  bytes `53287403`;
- R1 dense trace:
  SHA-256 `7f57ab676f2a31cf0abf93ff0f8b0f1f2f80bb9a58d7cf1e47e10a158c57c69f`,
  bytes `9759738`;
- R2 dense trace:
  SHA-256 `bb52495c93c1b8ed0c7fd9b41749eca464e46fca64b96d3d9445d07bf75a7842`,
  bytes `10965632`.

The R1 dense hash is exactly the frozen GE15 R1 dense trace hash.

## Construction

Repair26 uses the already certified exact cancellation-free first-order state:

`s=chi/Q`,

with

`alpha=s-a theta/k^2`

and

`chi=Q s`.

Initial `s` is exactly zero.

No physical equation, state dimension, model parameter, Fourier realization, bath equation or q20 equation is changed.

No legacy v0.77 fitted scale is used.

## Full-history trace closure at a=0.4

R1 history:

- nodes: `1796`;
- a range:
  `0.1428571428571419 ... 1.0`;
- bracket around a=0.4:
  `0.39953919419256334 ... 0.4000388311146992`;
- exact reconstructed target mismatch:
  `0.0`.

R2 history:

- nodes: `3592`;
- a range:
  `0.1428571428571419 ... 1.0`;
- bracket around a=0.4:
  `0.39984557997742914 ... 0.40009553675500664`;
- exact reconstructed target mismatch:
  `0.0`.

Requested-k and common-time mismatch are zero.

## Initial X10 closure

At a=0.4:

- R1 cancellation-free full-history trace X10 versus GE15 dense X10:
  `3.9819456608594117e-11` abs-or-rel max;
- R2 trace versus GE15 dense X10:
  `3.163231556278803e-11`;
- R1 versus R2 trace X10:
  `7.11299054009343e-12`;
- R1 versus R2 GE15 dense X10 relative L2:
  `3.542283132639446e-08`.

All are far below the frozen `2e-3` trace gate.

This directly replaces the historical Repair24 bridge mismatch of order unity with a cancellation-free first-order parent that closes against GE15.

## Retarded first-order bath boundary

R1 versus R2 full retarded boundary:

- z10 relative L2:
  `3.5309623104625126e-06`;
- v10 relative L2:
  `0.0023720775441813187`.

Frozen limit for each:

`5e-3`.

Quadrature closure, R1 Nq1024 versus Nq2048 weighted boundary:

- z10 relative L2:
  `4.492427062849641e-06`;
- v10 relative L2:
  `0.0018366352033811495`.

Frozen limit for each:

`5e-3`.

All outputs are finite.

## Frozen gates

Every preregistered Repair26 gate passes:

- GE15 patch provenance;
- requested-k closure;
- common-time closure;
- full-history coverage of a=0.4;
- exact target reconstruction;
- R1 trace X0 versus GE15;
- R2 trace X0 versus GE15;
- R1 versus R2 trace X0;
- R1 versus R2 z10;
- R1 versus R2 v10;
- Nq1024 versus Nq2048 weighted z10;
- Nq1024 versus Nq2048 weighted v10;
- finiteness.

## Scientific conclusion

Repair26 confirms the mechanism suggested by GE14/GE15 and localized by Repair25.

The historical v0.77 first-order bath-drive history was generated in the cancellation-prone alpha-coordinate representation,

`chi=Q(a theta/k^2+alpha)`,

whose early-time near-cancellation is known to generate a stiff, precision-dependent chi seed.

Regenerating the same eta=0 physical solution in the exact cancellation-free coordinate

`s=chi/Q`

removes the apparent mode-amplitude incompatibility. The full-history trace then agrees directly with the certified GE15 window state at a=0.4, and the retarded z10/v10 boundary is stable under both R1/R2 precision refinement and bath quadrature refinement.

Therefore the Repair25 discrepancy is not licensed as a physical mode-dependent normalization law and no fitted rescaling is adopted.

## License and stop boundary

Repair26 certifies only the cancellation-free full-history first-order bath parent and its retarded z10/v10 boundary.

Licensed next step:

a separately preregistered q20 reconstruction rerun that changes only the first-order bath parent from the historical v0.77 trace to the frozen Repair26 R1 cancellation-free trace/boundary.

Still not certified:

- q20;
- H4/Z21.

Repair24 remains historical FAIL and is not relabelled.
