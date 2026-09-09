# v0.77 preserved interpretation

Historical classification is retained unchanged:

`V077_NATIVE_STATE_TANGENT_AFFINITY_PASS`

The successful GitHub Actions run was `34315590099` at commit `747861af1c3727aa5903e7741ddd2ee14950984c`.

Primary native-state tangent observable:

`T_lambda(k,z) = [d_m(+lambda)-d_m(-lambda)]/(2 lambda)`.

Over the preregistered native-node window

- `0.03 <= k <= 0.20 h/Mpc`
- `0.2 <= z <= 1.5`

with `lambda = [10, 5, 2.5, 1.25]`, the maximum global normalized-RMS tangent affinity was about `2.254e-4` (0.0225%), well below the preregistered `5e-3` limit. Tangent-map cosines to the common mean were all above about `0.99999997`.

The independently preregistered even residual also passed, with maximum normalized residual about `1.0555e-3` (0.1055%) below the `5e-3` limit.

Combined with v0.76 native-node power closure at approximately machine precision, v0.77 supports the interpretation that the underlying eta=0 matter-state tangent is numerically affine and stable, while the larger fractional/log-power non-affinity seen near deep transfer minima is a conditioning effect associated with local division by very small `d_m` or `P_m`.

This result does not constitute an observational detection and does not by itself establish nonlinear regulation of structure formation. It certifies a linear-theory memory-induced response in the matter perturbation state for the frozen AeST model.

A separately preregistered v0.78 interpolation-operator closure audit may test whether the remaining off-native `get_transfer(z)` versus `pk_lin(k,z)` discrepancy is localized to the different time-interpolation operators. v0.77 must not be altered or retroactively reclassified by that later result.
