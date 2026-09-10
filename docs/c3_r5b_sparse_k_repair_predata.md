# C3 R5B sparse-k technical repair — pre-data declaration

R5A run 34492625578 again confirmed exact eta=0 zero coupling for all 18 frozen alpha/E/theta comparisons. It then built all six finite full-prehistory external bath-force tables successfully, but the first signed-lambda CLASS case aborted with `AEST_TANGENT_FORCE_K_MISS` at an unrelated internal transfer-grid mode k=1.3492948258 Mpc^-1. The force table intentionally contains only the six frozen target modes up to 0.1346649278 Mpc^-1.

R4 already defined the required reference-only sparse-k behavior: exact frozen target modes use the tabulated tangent force, while unrelated CLASS transfer-grid k values receive zero forcing when `AEST_TANGENT_ALLOW_K_MISS=1`. R5 omitted that helper patch.

Frozen R5B repair: port only the previously used sparse-k miss suppression into the R5 CLASS setup and set `AEST_TANGENT_ALLOW_K_MISS=1` for the fresh signed-lambda reference subprocesses. Do not add R4 dense live-bath output instrumentation. Exact-k matching tolerance, interpolation, target force table, equations, lambda, order, tauH0, k modes, redshifts, and C3 gates remain unchanged.

Historical R5/R5A runs remain immutable technical INCOMPLETE after successful zero-coupling validation. `FINITE_POSITIVE_ETA_NONLINEAR_MEMORY_LICENSED=False` regardless of outcome.