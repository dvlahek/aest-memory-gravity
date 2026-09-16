# NL1C7A A4 Repair05 — diagnostic batching lock

Status: PRE-DATA TECHNICAL REPAIR LOCK

Parent historical run: `35103396771` (Repair04). That run passed provenance, output-only source boundary, diagnostic k-capacity patch, CLASS/classy build, and then stopped in the A4 coverage probe before classification because a single long `k_output_values` string exposed exactly the first 45 of the frozen 128 requested modes to CLASS. The first missing requested mode was `k=0.010788714446368123 1/Mpc`, with nearest native trace mode at relative separation `8.61155683554026e-3`.

## Frozen Repair05 change

The frozen 128-point grid remains

`K_H = geomspace(0.0015, 1.2, 128)` in `h/Mpc`, with `K_MPC = h K_H`.

Repair05 changes only diagnostic execution:

- fixed batch size: **24 requested k values per CLASS instance**;
- total batches: **6** (24,24,24,24,24,8);
- each batch uses the identical frozen eta=0 CLASS/AeST parameter set;
- each batch writes to its own accepted-source-grid trace file using the already-certified v0.72 multi-instance trace-path reload mechanism;
- from each batch trace, retain only rows whose k matches one of that batch's requested values at relative tolerance `1e-12`;
- concatenate those exact rows into the final A4 trace;
- no k interpolation, nearest-neighbour substitution, resampling, extrapolation, or post-data grid selection is allowed.

Repair04 `_MAX_NUMBER_OF_K_FILES_ = 160` may remain in the diagnostic build. It is output capacity only and does not change physical equations, solver tolerances, the frozen k grid, or science gates.

## Science gates

Unchanged from the frozen A4 probe:

- all 128 requested k values found exactly to relative tolerance `1e-12`;
- common native time/a grid across all requested modes to relative tolerance `1e-12`;
- at least 3 native times in `0.015 <= a <= 0.03` below `a_i=0.02`;
- at least 3 native times in the same window above `a_i=0.02`;
- all required trace fields finite.

Allowed classifications remain only:

- `NL1C7A_NATIVE_TRACE_COVERAGE_PASS`
- `NL1C7A_NATIVE_TRACE_COVERAGE_FAIL`

This repair licenses only C7A A3/A4 eta=0 native trace coverage. It does not license interpolation, radial reconstruction, nonlinear spherical evolution, finite eta, or any observational claim.
