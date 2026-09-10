# C3 R5 zero-coupling-safe reference repair — pre-data declaration

## Motivation

The direct CLASS zero-coupling audit established that `aest_memory_enabled=yes, aest_eta=0` changes the sixth requested AeST mode even though the memory closure is multiplied by eta. The failure is numerical/implementation-induced by carrying 78 passive bath states inside the same stiff NDF15 system. The first five modes remain within the existing 5e-3 gate, while the sixth shows an approximately 1.53174 amplitude ratio.

Historical D2C6C R2/R3/R4, bath-bridge, source-term, and zero-coupling results remain immutable.

## Frozen repair

This repair changes only the eta=0 tangent/reference implementation.

1. In CLASS, when `aest_eta == 0`, passive memory bath coordinates are not allocated or evolved in the perturbation state vector. The physical AeST core therefore follows exactly the memory-disabled equations. For `aest_eta > 0`, the existing finite positive Drude bath equations and closure are unchanged.
2. The eta=0 bath needed for the variational derivative is computed outside the CLASS state vector from the memory-off CLASS source trajectory using the already validated analytic `bath_advance` representation with order 39 and `tau H0 = 1`.
3. The resulting dense forcing is exactly
   `F_eta0 = -a Q B_chi^(0)/(2 K_B)`
   with `B_chi^(0) = chi - a sum_j w_j z_j`.
4. Fresh signed-lambda CLASS runs use memory disabled and the existing external tangent-force hook. Physical eta remains zero and signed lambda is not physical eta.
5. No nonlinear equations, completion parameters, k modes, redshift checkpoints, background parameters, or C3 gates are changed.

## Frozen validations

A. Re-run the six-mode CLASS eta=0 zero-coupling audit. Required: all alpha/E/theta relative-L2 comparisons <= 5e-3.

B. Build the R5 linear tangent reference from the memory-off CLASS core plus external order-39 bath and compare it against the unchanged D2C6C nonlinear eta=0 tangent implementation using the original C3 gate:
- alpha <= 5e-3
- E <= 5e-3
- chi <= 5e-3

C. Existing bath-order/time/space/constraint gates remain unchanged if the full D2C6C evaluator is invoked.

No response sign, ordering, or amplitude condition is introduced. No tolerance may be altered after output.

`FINITE_POSITIVE_ETA_NONLINEAR_MEMORY_LICENSED=False` regardless of R5 outcome. A PASS only validates the eta=0 tangent bridge and licenses a separately preregistered finite-positive-eta test.