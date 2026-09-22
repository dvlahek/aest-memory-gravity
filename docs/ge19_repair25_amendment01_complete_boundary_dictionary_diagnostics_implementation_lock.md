# GE19 Repair25 amendment01 complete boundary-dictionary diagnostics — implementation lock

## Status

Pre-science diagnostic-completeness amendment locked before any Repair25 science result.

Amendment implementation commit:

`1f97e4f08ad40abc1623ec529a41bbca1531dcaa`.

No Repair25 audit result existed before this amendment.

## Reason

The first Repair25 implementation already covered the frozen routing gates but did not emit every diagnostic explicitly required by the Repair25 boundary-dictionary audit: full raw complex amplitude/magnitude/phase/ratio telemetry, complex least-squares fits, explicit v0.77 Q_trace closure, and the complete declared frozen-convention factor set.

This is an implementation-completeness correction only.

No physics equation, comparison surface, interpolation rule, threshold, routing criterion, parent result, or claim boundary is changed.

## Frozen amendment

File:

`ge19/repair25_amendment01_complete_boundary_dictionary_diagnostics.json`.

Blob:

`23c85b181fdb095e7c91d2601cee251878b57b5c`.

Classification:

`GE19_REPAIR25_PREDATA_AMENDMENT01_COMPLETE_BOUNDARY_DICTIONARY_DIAGNOSTICS`.

## Amended implementation

File:

`ge19/repair25_first_order_bath_boundary_dictionary_audit.py`.

Blob:

`1827b1a03268964043be9f7b13fdc704f54d4d05`.

The amended implementation additionally reports:

- the three common positive-mode complex amplitudes at a=0.4;
- magnitude and phase for each;
- complex ratios v0.77/GE15, GE15/GE19 and v0.77/GE19;
- global complex least-squares factors at the exact surface;
- global and per-mode complex fits across the common overlap window;
- v0.77 Q_trace versus GE15 Q at a=0.4 and on the overlap window;
- Q_action versus GE15 Q and v0.77 Q_trace at a=0.4;
- explicit exact-factor diagnostics for
  `1,-1,a,1/a,k,1/k,ik,-ik,ik/a,-ik/a,a/(ik),Q,1/Q,H0,c_light/H0,2,1/2,i,-i,k/a,a/k`.

Candidate-factor diagnostics report the direct residual before any extra fit. An optional additional complex fit is report-only and cannot be used to select a Repair25 route.

## Unchanged frozen gates

All original Repair25 thresholds remain byte-for-byte unchanged in the parent preregistration:

- Q_action vs GE15: `1e-10`;
- GE15 algebraic identity: `1e-10`;
- Repair22 X10 vs GE15 relative L2: `1e-8`;
- Repair22 X10 vs GE15 pointwise abs-or-rel: `1e-6`;
- v0.77 vs GE15 direct compatibility: `1e-3`;
- best global scale residual compatibility: `1e-3`;
- per-mode shape cosine: `0.9999`.

Routing logic is unchanged.

## Prelock

Amended dedicated prelock workflow blob:

`2c5e5b94cffc040df09dd1af676834b2291cda19`.

Dedicated Repair25 amended prelock:

- run `35717692112`;
- conclusion `success`.

Static GE19 audit on the same head:

- run `35717692097`;
- conclusion `success`.

Both runs use head:

`1f97e4f08ad40abc1623ec529a41bbca1531dcaa`.

## Stop boundary

Repair25 remains diagnostic only.

- q20 is not rerun;
- q20 is not certified by this audit;
- no fitted normalization is adopted;
- no candidate convention factor is adopted;
- H4/Z21 remains unlicensed.

Only the frozen Repair25 routing result may determine the next separately preregistered step.
