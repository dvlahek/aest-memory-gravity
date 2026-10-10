# GE19 D16R1 — independently versioned implementation repair

Original D16 failure: `unexpected frozen a=0.4 bracket: 0.39953919419256334, 0.4000388311146992`.

The exception is a deterministic ordering bug, not a changed Repair26 trace. Original Repair24 expects the historical v0.77 bracket until original Repair37 `build_context` initializes the exact Repair26 bracket from original Repair27. D16 computed its boundary before context. D13 and D15a computed context before boundary.

Only move the boundary call after original `build_context` and assert exact source-frozen Repair27 constants. Do not relax the 1e-15 original frozen bracket check, patch historical original source, alter R1 trace, physics, parents or data, or mark original D16 fail PASS. The D16R1 runner creates distinct results.

No actual D16R1 physical results in this source package. Original H1dot Hermite interior remains an uncertified surrogate. GE05 continuous all-interval on-shell, full Ward, Z21 and lensing remain OPEN.
