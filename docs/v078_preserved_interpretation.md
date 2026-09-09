# v0.78 preserved interpretation

Historical result retained unchanged:

`V078_TIME_INTERPOLATION_OPERATOR_CLOSURE_PASS`

Diagnosis:

`V078_TIME_INTERPOLATION_OPERATOR_DISCREPANCY_LOCALIZED`

The successful technical run was GitHub Actions run `34317337908` at commit `31c05c22b86e8ac01ce822306efecdcb03cff1d5`.

Artifact: `results_bundle_v078_time_interpolation_operator_closure`, artifact id `10090965339`, SHA-256 `2d3ee5564ad8abd35b094001dab728d5ad98d85687c65489c1e5667f03879c19`.

Frozen model and numerical configuration:

- `KB=0.0665`
- `tauH0=10.0`
- `p=0`
- pinned CLASS commit `e85808324f51fc694d12e3ed7439552a3c3f9540`
- tangent amplitudes `[10, 5, 2.5, 1.25]`
- v0.75 r4 sampling: `k_per_decade_for_pk=80`, `k_per_decade_for_bao=560`
- no observational data and no nonlinear evolution

Primary results:

- Forcing control passed: relative L2 `5.356775428992513e-07`, cosine `0.9999999999998566`.
- Source-derived matter power and CLASS Fourier matter power agree on common native `(k,tau)` nodes to maximum relative error `8.372390951150745e-15` across baseline and all forced runs.
- Exact native-k control passed with zero reported k mismatch and zero native-z-grid mismatch.
- At off-native times, while keeping exactly the same native Fourier k nodes, the discrepancy survives strongly.
- Baseline maximum source-vs-`pk_lin` relative discrepancy is `138.80340816499393` at approximately `k=0.1097167254 h/Mpc`, `z=0.4`, where source-derived power is `625.9788499561129` and `pk_lin=4.47756501913989`.
- Baseline has 820 compared points above the preregistered 0.5% discrepancy level; all forced runs also show many such points.

Interpretation locked by this result:

1. The native perturbation evolution and source-to-power normalization are internally consistent.
2. The discrepancy is not explained by k interpolation, since it survives at exactly the same native Fourier k nodes.
3. Under the frozen CLASS implementation, the discrepancy is localized to the distinct off-native time-interpolation operators: interpolation of the transfer/source state followed by squaring versus interpolation of the stored log-power quantity used by `pk_lin`.
4. Together with `V077_NATIVE_STATE_TANGENT_AFFINITY_PASS`, the linear memory-induced response in the native matter state `d_m(k,z)` is numerically certified under the tested frozen setup.
5. This closes the linear numerical-chain debugging. Later work should use the certified state/native-source representation and move to nonlinear AeST+memory physics rather than continue CLASS interpolation debugging.
6. This result does not alter historical FAIL classifications v0.72-v0.76 and does not constitute observational evidence or a nonlinear simulation.
