# NL1C7 initial-data closure audit — Repair01 preregistration

Status: **PRE-DATA REPAIR LOCKED AFTER TECHNICAL FAILURE, BEFORE RE-RUN**

Historical technical-failure workflow: `35091142502` at head `f2237a3be3036cd5a10570dde6a52ea89ec98785`.

The run passed the frozen preregistration/implementation lock check and the certified NL1C6 parent provenance check, then failed before producing a science classification. The failure occurred in SymPy `H.rank()` with `OverflowError: too many digits in integer` while simplifying the exact symbolic principal Hessian containing the frozen `Z0=1e-17` scale.

## Frozen repair

Repair01 changes only the symbolic full-rank evaluation algorithm:

- remove the generic `H.rank()` call;
- retain the exact G11 determinant identity check already present in the audit;
- certify generic principal rank 4 from the nonzero determinant identity plus the already frozen positive G11 kinetic margin;
- retain the independent exact background matrix-rank check at the homogeneous eta=0 point.

No physical equation, variable count, parent provenance, initial profile, gate, threshold, classification boundary, or interpretation is changed.

Expected allowed result remains `NL1C7_INITIAL_DATA_CLOSURE_INCOMPLETE` if the frozen matter density/velocity data fail to uniquely select the remaining eta=0 metric/scalar/aether mode content.
