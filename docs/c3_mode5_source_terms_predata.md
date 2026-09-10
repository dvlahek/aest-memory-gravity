# C3 mode-5 source-term audit — pre-data declaration

## Purpose

The direct bath-bridge audit on run 34485779925 showed that the transformed CLASS bath states and the offline bath evolution agree, while the reconstructed base source chi disagrees only for the sixth requested mode (k_h = 0.20 h/Mpc) by about 0.347. This audit localizes that source mismatch before any further C3 repair.

Historical D2C6C R2/R3/R4 results and bath-bridge results remain immutable. This audit cannot license finite positive eta and does not change any physics equation, parameter, solver tolerance, bath definition, nonlinear completion, or D2C6C gate.

## Frozen inputs

- branch: v053-exp-normalization-corrected
- corrected CLASS v3.3.4 commit: e85808324f51fc694d12e3ed7439552a3c3f9540
- physical eta = 0
- tau_H0 = 1 for the memory-enabled diagnostic CLASS run
- requested k_h/Mpc = [0.03, 0.05, 0.08, 0.10, 0.15, 0.20]
- frozen redshift checkpoints used for comparison: z = [5, 4, 3, 2, 1.5, 1, 0.5, 0.2]. z=6 is not needed for this source decomposition.

## Frozen comparisons

For each checkpoint of direct history index 5 and offline mode index 5, report independently:

- a_CLASS and a_offline
- Q evaluated on the direct and offline scale factors
- alpha_CLASS and alpha_offline
- theta_CLASS and theta_offline
- T_alpha = Q alpha
- T_theta = Q a theta / k^2
- chi = T_alpha + T_theta
- direct/offline ratios and symmetric relative differences for alpha, theta, T_alpha, T_theta, and chi when denominators are numerically usable.

In addition, build a 6x6 descriptive matching matrix between every direct CLASS history and every offline mode using the eight checkpoint trajectories of alpha and theta. For each direct history report the offline index with the smallest combined normalized L2 discrepancy. This checks whether the isolated sixth-mode mismatch is an ordering/index association error rather than a field-normalization error.

No threshold is used to tune or repair the model. Diagnostic labels are descriptive only:

- MODE5_INDEX_MISMATCH_CANDIDATE if direct history 5 matches an offline mode other than index 5 substantially better than index 5.
- MODE5_ALPHA_MISMATCH if alpha carries the dominant mode-5 discrepancy.
- MODE5_THETA_MISMATCH if theta carries the dominant mode-5 discrepancy.
- MODE5_SOURCE_COMBINATION_MISMATCH if alpha and theta separately agree but their reconstructed source terms do not.
- MODE5_SOURCE_MATCH if the previously observed mismatch is not reproduced.

The audit must print the raw numerical components needed to justify any label. No physics repair is permitted in the same result-producing commit.

FINITE_POSITIVE_ETA_NONLINEAR_MEMORY_LICENSED remains False regardless of the result.
