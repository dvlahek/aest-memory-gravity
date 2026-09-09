# v0.76 preserved interpretation

Historical classification is retained unchanged:

`V076_NATIVE_NODE_POWER_CLOSURE_FAIL`

The successful technical run was GitHub Actions run `34313160040` at commit `234be56af3378cd555ee34f5b556fba836f7456b`.

Primary findings:

- Native-node source-to-Fourier closure was essentially exact in the preregistered primary window, with maximum relative discrepancy about `6.23e-15` across all baseline and +/-lambda runs.
- The corresponding baseline-only maximum was about `5.95e-15`.
- The historical off-node source-power versus `pk_lin` discrepancy remained large, with maximum relative discrepancy about `125.796` and baseline maximum about `7.378`.
- The native-node fractional power/source lambda-affinity gate failed only because the maximum normalized-RMS affinity reached about `7.766e-3` at lambda `5`, above the preregistered `5e-3` threshold. The other lambdas were below the threshold.
- The fixed v0.63 target-grid tangent affinity remained about `2.91e-4`.

The native closure rules out a mismatch in the source-to-power normalization, primordial prefactor, and native CLASS Fourier construction as the origin of the historical factor-scale discrepancy. However, because the preregistered native-node fractional-affinity control failed, v0.76 does not certify the stronger `TIME_INTERPOLATION_OPERATOR_DISCREPANCY_LOCALIZED` diagnosis.

Inspection after the result showed that the dominant fractional-affinity contributions occur near deep minima / near-zero structure in the matter transfer function, where dividing a finite tangent by a very small local baseline power makes the fractional/log response ill-conditioned. This post-result observation motivates a separate preregistered state-tangent audit that does not divide by local `d_m` or `P_m`.

This note does not alter v0.72-v0.76 historical classifications, does not retune any physical parameter, and does not claim nonlinear evolution or observational evidence.
