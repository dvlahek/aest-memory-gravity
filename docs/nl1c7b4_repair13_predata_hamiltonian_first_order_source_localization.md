# NL1C7B4 Repair13 — Hamiltonian first-order source localization

## Status

Locked before implementation and before any Repair13 execution.

Repair13 is licensed only by the frozen Repair12 result at commit `167af8e7b6d610c307b67fed7890fe0547c27bfa`, classification

`NL1C7B4_REPAIR12_FULL_CONSTRAINT_FIRST_ORDER_RESIDUAL`.

Repair13 does not modify the state, action, source dictionary, or historical B4 gate. It localizes the robust first-order Hamiltonian residual identified by Repair12.

## Frozen parent result

- Repair12 JSON SHA-256:
  `99c963dc65cca35c90c6b892fb4192bed1a8c03776664c9da532a5702c62767c`;
- Repair12 result-freeze commit:
  `167af8e7b6d610c307b67fed7890fe0547c27bfa`;
- Repair12 Hamiltonian gated slopes:
  `1.0021920951676406 <= p_H <= 1.025811179907278`;
- Repair12 momentum gated slopes:
  `2.005507037071882 <= p_M <= 2.0397790843808306`.

The historical B4 raw exact-nonlinear classification remains unchanged.

## Frozen exact source labels

Use exactly the same 11 Hamiltonian Euler-Lagrange contributions:

1. `GR_kin`
2. `GR_curv_NL`
3. `GR_curv_Rr`
4. `GR_Nr_boundary`
5. `AeST_E2`
6. `AeST_EX`
7. `AeST_X2`
8. `AeST_J`
9. `AeST_K`
10. `dust`
11. `standard_bg`

No source may be merged, omitted, rescaled, sign-flipped, or refitted.

## Frozen diagnostic path

Use the exact Repair12 virtual perturbation path and the same fixed B3 baseline.

For each source `i` and positive amplitude

`lambda in {1,1/2,1/4,1/8}`,

define

`Delta C_H_i(lambda)=C_H_i(lambda)-C_H_i(0)`.

Define the one-sided first-order profile estimate

`A_i(lambda)=Delta C_H_i(lambda)/lambda`.

The total profile is

`A_tot(lambda)=sum_i A_i(lambda)=Delta N_H(lambda)/lambda`.

All non-center radial points, all scales, grids, Y families, and beta values are retained.

## Source-order diagnostics

For every source and every frozen case, compute the L2 norms of `Delta C_H_i(lambda)` and adjacent log2 slopes.

Use the same asymptotic intervals as Repair12:

- `1/2 -> 1/4`;
- `1/4 -> 1/8`.

Descriptive source-order labels are preregistered as:

- `first_order_like` if both gated slopes lie in `[0.8,1.2]`;
- `second_order_like` if both lie in `[1.8,2.2]`;
- `higher_or_mixed` otherwise;
- `numerically_zero` if all positive-lambda L2 norms are <= `1e-24`.

These labels are descriptive and are not used to change any physics gate.

## First-order coefficient localization

At the smallest frozen amplitude `lambda=1/8`, define

`A_i = A_i(1/8)`

and

`A_tot = sum_i A_i`.

For each source report:

- `||A_i||_2`;
- `||A_i||_inf`;
- signed projection fraction
  `P_i=<A_i,A_tot>/||A_tot||_2^2` when `A_tot` is nonzero;
- cosine with `A_tot`;
- source-order label.

The projection fractions must sum to 1 within numerical tolerance.

## Cancellation diagnostics

For every pair of sources `i,j`, define

`c_ij = ||A_i+A_j||_2/(||A_i||_2+||A_j||_2)`.

Smaller `c_ij` means stronger opposing cancellation.

For every case report:

- the strongest-cancelling source pair;
- its `c_ij`;
- largest-`||A_i||_2` source;
- second-largest source;
- total `||A_tot||_2`;
- sum of individual source norms;
- global cancellation fraction
  `||A_tot||_2/sum_i ||A_i||_2`.

No cancellation threshold is used as a terminal gate.

## Cross-amplitude convergence

For each source, compare the first-order coefficient profiles at `lambda=1/4` and `1/8`:

`e_i = ||A_i(1/4)-A_i(1/8)||_2 / max(||A_i(1/8)||_2,1e-300)`.

This is reported descriptively. No source is dropped for weak convergence.

The total coefficient profile must satisfy the same diagnostic, but no new physical threshold is introduced.

## Gates

### R13_G1 — frozen provenance

Require exact Repair08/10/11/12 hashes and classifications, Repair12 result-freeze ancestry, exact dense coverage, and frozen imported-code blobs.

### R13_G2 — exact Repair12 lambda=1 reproduction

Reproduce all 54 Repair12 lambda=1 Hamiltonian max-epsilon and signed numerator values to absolute-or-relative tolerance `1e-12`.

### R13_G3 — per-source bookkeeping closure

For every positive lambda, every case, and every non-center point,

`sum_i Delta C_H_i(lambda)=Delta N_H(lambda)`

to normalized error `<=1e-12`.

### R13_G4 — first-order coefficient closure

At every positive lambda,

`sum_i A_i(lambda)=A_tot(lambda)`

to normalized error `<=1e-12`.

### R13_G5 — projection closure

At `lambda=1/8`, the finite projection fractions `P_i` must sum to 1 within `1e-12` for every case with nonzero `A_tot`.

### R13_G6 — complete source localization

Require all 54 cases, all 11 source labels, all four positive amplitudes, and no excluded non-center points.

### R13_G7 — Repair12 order reproduction

The total Hamiltonian gated slopes recomputed from the source decomposition must reproduce Repair12 and remain first-order-like under the already observed Repair12 criterion.

Specifically, both gated total-H slopes must lie in `[0.8,1.2]` in all 54 cases.

### R13_G8 — claim boundary

Require:

- historical B4 FAIL preserved;
- no state write/projection;
- no nonlinear constraint correction;
- no coefficient fit/rescale;
- no source insertion/removal;
- no sign change;
- no K clipping;
- no Q linearization;
- no threshold change;
- no radial-point removal;
- no Y/beta/scale selection;
- no nonlinear evolution;
- no finite eta;
- no B4-PASS relabel;
- no observational-detection claim.

## Terminal classifications

Allowed:

- `NL1C7B4_REPAIR13_HAMILTONIAN_FIRST_ORDER_SOURCE_LOCALIZATION_PASS`;
- `NL1C7B4_REPAIR13_IMPLEMENTATION_FAIL`.

A diagnostic PASS means only that the Repair12 first-order Hamiltonian residual has been reproducibly decomposed into source-level first-order profiles and cancellations.

It does not identify a source as physically wrong and does not license modifying any source. Any subsequent model/interface correction requires a separate preregistration supported by the Repair13 localization result.
