# GE19 Repair25 local execution runner — lock

## Status

The local Repair25 science runner is locked after the amended Repair25 diagnostic implementation and both amended prelock audits passed.

Runner file:

`ge19/run_local_repair25_first_order_bath_boundary_dictionary_audit.sh`.

Frozen runner blob:

`d18ce24a8fb37474790ffb5fa92d956274d5bb17`.

Runner commit:

`90fa68b72ffdd8fa626678b4917d8167f9a5e2d0`.

Static audit on the runner head:

- run: `35717855170`;
- conclusion: `success`.

## Locked science implementation

Repair25 preregistration blob:

`1e7f25eba5a4c8b297b563edfe6f9c4f276ec6c9`.

Repair25 amendment01 blob:

`23c85b181fdb095e7c91d2601cee251878b57b5c`.

Repair25 amended science implementation blob:

`1827b1a03268964043be9f7b13fdc704f54d4d05`.

Amended dedicated prelock:

- run: `35717692112`;
- conclusion: `success`.

Amended static prelock:

- run: `35717692097`;
- conclusion: `success`.

## Execution scope

The runner performs only the first-order boundary-dictionary audit.

It does not:

- rerun Repair24 q20;
- construct q20;
- adopt a fitted normalization;
- modify any frozen threshold;
- solve H4/Z21.

It consumes the already frozen local Repair24, Repair22, Repair13 and GE15 outputs and the frozen v0.77 trace.

## Frozen local hashes

- Repair24 JSON:
  `71f463524b47f72d2c5082667fe99141d2286ebc2938c4eed6b89a1583339f2a`;
- Repair22 JSON:
  `7d53b2458183c6b2cc326acdded70b2c3ce1fab959d8456e56d3b4f1f86ef374`;
- Repair22 NPZ:
  `3020e0d040f902ab2609e05705f4508d9919665b1344fa0e641644ea8fc41a16`;
- Repair13 JSON:
  `ae3cc790ecffbd5498b5852273c72ae578d4615de29bbb616673c05cdb3e74b7`;
- Repair13 NPZ:
  `011c0ae54fd21d70c0e2c695ce62e7b74a3c5529a07c9023c882a447d5b40ca3`;
- GE15 JSON:
  `5975774bf7af0f3af9acf16c8de2dbac0ca032894dc5c6879346a3e11efe84c1`;
- v0.77 trace:
  `98c8468e8ccdf902cad8d6e65f3852e863c6fd19df62ece61353ab725ac5a43e`;
- v0.77 trace bytes:
  `2657188`.

The GE15 JSON remains the binding source for the exact R1 dense-trace SHA-256.

## Valid science execution

The first valid science execution is the first invocation of this exact runner on a working tree containing the frozen local inputs above, with an active project virtual environment.

The runner writes:

`results/ge19_repair25_first_order_bath_boundary_dictionary_audit.json`

and

`results/ge19_repair25_first_order_bath_boundary_dictionary_audit_FULL.log`.

The first valid result must then be frozen without rerun or threshold change.
