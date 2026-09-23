# GE19 Repair42 local direct-target H4 diagnostic runner — lock

## Status

The first local Repair42 execution path is frozen.

Runner:

`ge19/run_local_repair42_direct_target_h4_propagation_diagnostic.sh`.

Runner commit:

`72544472263b65d52cc09e9206df8a2e9961fae5`.

Runner blob:

`a5802ac72e2623dde7def42e18c6b223282ff11b`.

Static runner audit:

- run:
  `35918237745`;
- job:
  `107375233398`;
- conclusion:
  `success`.

## Bound contract

Repair42 preregistration:

- commit:
  `8aa14dffd3d508bcc4920b9cb68ff520a4d2520d`;
- blob:
  `cbdb7b66e57a24c44fb03c0856ffdc1977303844`.

Repair42 implementation:

- commit:
  `e2634cfe7be0eb5590305ae55197d483dbd9818f`;
- blob:
  `8576118fec60dd6ac1593459da9354d424d04fd5`.

Implementation lock:

- commit:
  `b6ebbd5e896b37c7f0591bedb18734cc7ba47d79`;
- blob:
  `d79c5ac42e828cf1d2bbd4308f57792b3bc80986`.

Dedicated prelock:

- workflow commit:
  `a7303cb29ec0929c8e2d00350804af70856a60fb`;
- workflow blob:
  `ece1e7ca5522b71ad92f045bf7cc6cefbd896080`;
- run:
  `35918082912`;
- job:
  `107374703486`;
- conclusion:
  `success`.

Frozen Repair41 reference:

- JSON/FULL SHA-256:
  `1b18fede26b021e077ffe5c8b6b7ff0dc727b4defaab48e63491c86d868d1320`;
- NPZ SHA-256:
  `6bfb87ea21d55e2a1d2b16aee9bc8d7246111f91a064a78b74d2ed946ec2ba45`.

Frozen Repair37 baseline:

- JSON SHA-256:
  `da8f2f00c22c866ec3f82381d23f69bf036e630fe2a29c5c44657984b760f61a`;
- NPZ SHA-256:
  `572d8937c1d742b10da66e34cc076377c1b2feb20b8f72eb25c3eaf31a59829f`.

## Execution rule

The runner verifies exact local parent hashes before execution.

Repair42 propagates the original factor-1 frozen Repair37 PCHIP baseline and
six direct-target variants:

- direct382 M1 only;
- direct382 Q_GE06 only;
- direct382 both;
- direct763 M1 only;
- direct763 Q_GE06 only;
- direct763 both.

The direct target arrays are never interpolated. They are injected only at
the exact Repair41 factor-1 stage/right-endpoint coordinates.

Routing uses only the existing science target 1e-6.

Repair42 remains diagnostic-only and cannot certify Z21 or license lensing.
