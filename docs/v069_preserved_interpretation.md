# Preserved interpretation of v0.69

This note is result-informed and was added after completion of v0.69. It does not alter, relabel, rerun, or rescue any historical classification.

## Historical classifications retained unchanged

- v0.67: `V067_GROWTH_KERNEL_CLOSURE_AFFINITY_FAIL`
- v0.68: `V068_LINEAR_SCALE_MEMORY_RESPONSE_MAP_FAIL`
- v0.69: `V069_NONLINEAR_ONSET_DIAGNOSTIC_FAIL`

These labels remain authoritative for the preregistered gates used in the corresponding runs.

## What v0.69 established

The direct `classy.pk_lin` spectrum was finite and positive over the full preregistered grid, all three dimensionless-power thresholds `Delta_L^2 = 0.1, 0.3, 1.0` were bracketed in all runs, and the Drude forcing control passed. The baseline first-crossing locations overlap strongly with the transition region highlighted qualitatively by v0.68: 13 of 21 threshold-redshift crossings lie in `0.08 <= k <= 0.20 h/Mpc`. In particular, the baseline `Delta_L^2 = 1` crossings at `z=0.2` and `z=0.4` occur at approximately `0.147` and `0.181 h/Mpc`.

The first-crossing observable itself is not numerically certified. The preregistered fine-versus-every-other-grid crossing test failed badly, with a maximum relative difference of about 0.48, and the global four-lambda onset-response affinity also failed, reaching about 0.96. Therefore none of the v0.69 delay/advance amplitudes is promoted as a certified nonlinear-onset shift.

## Physical interpretation retained

The v0.69 failure is informative because it shows that a naive *first upward crossing* is too sensitive to narrow or rapidly varying structure in the linear AeST spectrum. This is consistent with the earlier rapid-k diagnostics and means that a single pointwise threshold crossing is not a robust proxy for the onset of a broadband nonlinear regime in this model.

At the same time, the overlap between the `Delta_L^2 ~ 0.1--1` region and the `k ~ 0.08--0.20 h/Mpc` response transition remains worth testing. A suitable follow-up should suppress sensitivity to isolated narrow excursions without modifying the physical model or the stored v0.67--v0.69 results.

## Guardrail for follow-up

The next test may use a preregistered broadband/coarse-grained definition of the linear dimensionless power and an implicit tangent of its threshold scale. It must remain a linear-theory diagnostic. It must not be described as a nonlinear simulation, nonlinear saturation result, halo prediction, screening result, or observational detection.
