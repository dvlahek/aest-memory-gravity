# CLASS eta=0 zero-coupling audit — pre-data declaration

## Purpose

The mode-5 source audit found that the memory-enabled eta=0 CLASS trajectory differs strongly from the memory-disabled CLASS trajectory for the sixth requested mode, despite the memory closure being multiplied by eta. This audit tests that zero-coupling identity directly, without the offline solver, tangent forcing, nonlinear completion, or likelihoods.

Historical D2C6C R2/R3/R4 and subsequent forensic results remain immutable. This audit cannot license finite positive eta and cannot alter any previous gate.

## Frozen implementation and inputs

- branch: `v053-exp-normalization-corrected`
- CLASS v3.3.4 commit: `e85808324f51fc694d12e3ed7439552a3c3f9540`
- identical corrected AeST baseline parameters in both runs
- requested modes: k_h/Mpc = [0.03, 0.05, 0.08, 0.10, 0.15, 0.20]
- checkpoints: z = [6, 5, 4, 3, 2, 1.5, 1, 0.5, 0.2]
- run A: `aest_memory_enabled=no`, `aest_eta=0`
- run B: `aest_memory_enabled=yes`, `aest_eta=0`, `aest_tau_H0=1`, `aest_memory_order=39`
- one OpenMP thread
- no external tangent force or trace environment variables

The only intended difference between A and B is allocation/evolution of the decoupled eta=0 bath state.

## Frozen outputs

For each mode and each field alpha_aest, E_aest, and theta_cdm, report:

- nine-checkpoint relative L2 difference between memory=yes eta=0 and memory=no;
- maximum pointwise symmetric relative difference over usable checkpoints;
- memory=yes / memory=no ratio at each checkpoint when the denominator is numerically usable.

Also report the global maximum relative L2 difference and the worst field/mode.

The diagnostic zero-coupling tolerance is frozen at 5e-3, equal to the existing D2C6C linear-regression tolerance. `ZERO_COUPLING_PASS=True` requires all 18 field/mode relative-L2 comparisons to be <= 5e-3 and finite. No tolerance may be changed after outputs are observed.

A failure localizes a CLASS implementation/numerics problem because no memory term is allowed to feed back into the AeST equations at eta=0. A pass would falsify the apparent zero-coupling violation and return attention to the source-audit construction.

No repair is permitted in the same result-producing commit.

`FINITE_POSITIVE_ETA_NONLINEAR_MEMORY_LICENSED=False` regardless of the result.