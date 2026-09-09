# v0.75 preserved interpretation

Historical classification is retained unchanged:

`V075_FOURIER_K_RESOLUTION_CLOSURE_FAIL`

The successful technical run was GitHub Actions run `34284148170` at commit `812719c784cfa97e881a7a4e63f4e5850e68ac71`.

The preregistered CLASS k-resolution sequence was

- r1: `k_per_decade_for_pk=10`, `k_per_decade_for_bao=70`
- r2: `20`, `140`
- r3: `40`, `280`
- r4: `80`, `560`

The native-transfer tangent remained strongly lambda-affine at every resolution, with maximum normalized-RMS affinity about `2.9055e-4`, well below the preregistered `5e-3` limit. In contrast, the `pk_lin` tangent affinity remained about `0.25765`, and the maximum transfer-power versus `pk_lin` relative discrepancy remained about `125.796`. The r4-versus-r3 `pk_lin` all-runs global normalized RMS was zero to the reported precision.

Therefore increasing the preregistered CLASS scalar/Fourier k sampling density did not resolve the discrepancy. v0.75 rejects the specific hypothesis that the v0.72-v0.74 mismatch is explained by insufficient values of `k_per_decade_for_pk` / `k_per_decade_for_bao` over this tested sequence.

This result does **not** alter the historical classifications of v0.72-v0.74 and does **not** certify nonlinear evolution or observational evidence. The structured native-transfer memory tangent remains a descriptive, numerically lambda-affine result. A later separately preregistered audit may localize the discrepancy inside the CLASS chain from perturbation source to Fourier table to `pk_lin`, but cannot retroactively rescue v0.75.
