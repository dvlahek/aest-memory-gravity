# GE19 Repair27 cancellation-free-parent q20 reconstruction — result freeze

## Status

First valid Repair27 science execution:

`GE19_REPAIR27_CANCELLATION_FREE_PARENT_Q20_RECONSTRUCTION_PASS`.

Frozen route:

`CANCELLATION_FREE_PARENT_Q20_CERTIFIED`.

Repair27 certifies the window-local particular baseline second-order normalized-bath projection on the frozen Repair22 low-mode scope.

Repair24 remains a historical FAIL and is not relabelled.

## Frozen local outputs

Science JSON:

- SHA-256:
  `99a2183e7088c7492f624cae2d294612380714c1d81aa7ff49cc4fcd1c62c74b`;
- bytes:
  `8801`.

Science NPZ:

- SHA-256:
  `2b1566d402e4c9e8daee8e5c7084b3da7735442b4fb604d51489b708662fd9c0`;
- bytes:
  `3550984`.

Inner FULL log:

- SHA-256:
  `99a2183e7088c7492f624cae2d294612380714c1d81aa7ff49cc4fcd1c62c74b`;
- bytes:
  `8801`.

Science exit:

`0`.

## Frozen parent provenance

Repair26 parent:

- workflow run:
  `35721220889`;
- workflow job:
  `106724330805`;
- artifact:
  `10690709843`;
- artifact digest:
  `sha256:33faae31aae0ebe3cc52ac2083193ec8ba3dfe284fb07f06ef2568cad8e3938f`;
- result JSON SHA-256:
  `80ba0b5927217be000991c82b4afb5f39b5e0ff369bc9b630a88ec11dabdedb6`;
- R1 full-history trace SHA-256:
  `608ee0b4c868a701db6976f756b9a551cd9ddffe1e8e4ab37c5cd2361405a6f8`;
- R1 full-history trace bytes:
  `26643162`.

Repair22 and Repair13 frozen hashes were reproduced exactly.

The only scientific-parent change relative to Repair24 is:

historical v0.77 first-order full-history trace

->

frozen Repair26 R1 cancellation-free full-history trace.

No Repair25 fitted normalization is used.

## Full-history boundary

The frozen Repair26 R1 history brackets the GE19 initial surface at

- `a_lo=0.39953919419256334`;
- `a_hi=0.4000388311146992`.

The exact partial-step target mismatch is

`0.0`.

Requested-k mismatch and common-time mismatch are also zero.

## q20 controls

Initial H1 X10 bridge:

`3.981945660904338e-11`

against the unchanged frozen limit

`1e-10`.

PASS.

G2 spatial Nx256/Nx512 low-mode relative L2:

`3.4518767056924556e-15`

against

`1e-10`.

PASS.

q20 quadrature Nq1024/Nq2048 weighted-z20 relative L2:

`8.23684251511779e-05`

against

`1e-2`.

PASS.

q20 time Nt64/Nt128 weighted-z20 relative L2:

`3.2441966579873734e-05`

against

`5e-3`.

PASS.

z10 time Nt64/Nt128 weighted-z10 relative L2:

`2.567987045993896e-05`

against

`5e-3`.

PASS.

All weighted q20 outputs are finite and all frozen C,beta,m cases are complete.

The normalized c2 sqrt(w) cancellation and vectorized interval propagator self-test also pass.

## Constructed q20 scale

Across the frozen C envelope, the primary weighted-z20 L2 norm is approximately

`1.582e7`.

Representative X20 L2 is approximately

`1.130e9`.

Representative B20_linear L2 is approximately

`1.114e9`.

The weighted G2 term is approximately

`1.516e-7`.

The displayed beta0 dependence of the certified projection is negligible at numerical precision.

## Scientific conclusion

Repair27 closes the only gate that failed in Repair24 without changing the q20 equations, Repair22 Z20 parent, grids, quadrature orders, or science thresholds.

The historical Repair24 failure was therefore caused by the cancellation-prone first-order v0.77 bath parent.

With the independently certified Repair26 cancellation-free full-history parent, the same frozen Repair24 q20 construction passes every gate.

Therefore:

- `q20_constructed=true`;
- `q20_certified_projection=true`;
- `CANCELLATION_FREE_PARENT_Q20_CERTIFIED`;
- H4/Z21 construction is licensed after this result freeze.

## Claim boundary

Repair27 certifies only the window-local particular baseline second-order normalized-bath response through

`weighted_z20 = sum_j w_j z20_j`

on the frozen Repair22 low-mode scope.

It does not:

- choose a primordial/homogeneous second-order bath mode;
- solve H4/Z21;
- introduce finite eta;
- make observational claims.

## Next licensed step

A separately preregistered H4/Z21 construction may now use:

- Repair22 certified Z20;
- Repair27 certified q20 projection;
- GE04 DY2;
- GE05 M1/M2;
- the already certified first-order eta tangent.

No H4/Z21 result is contained in Repair27.
