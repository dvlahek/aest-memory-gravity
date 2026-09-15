# Stable AeST DESI DR1 R9b2h derivative-stable quadrature post-result record

## Frozen result

R9b2h completed with

`STABLE_AEST_DESI_DR1_R9B2H_CROSS_METHOD_DERIVATIVE_FAIL`

and runner exit code 1. This is a scientific/numerical FAIL under the preregistered R9b2h gates, not a technical run failure. It is retained permanently and is not reclassified below.

Observed gates:

- H1 provenance and construction: PASS
- H2 finite physicality: PASS
- H3 log-linear resolution convergence: PASS
- H4 shape-preserving value-level quadrature agreement: PASS
- H5 within-method central-derivative consistency: PASS
- H6 cross-method tangent agreement: FAIL
- H7 requested-support convergence: reported PASS by the implementation, but the post-result inspection below shows that this control was vacuous because the actual returned CLASS transfer support did not change.

## Completed artifact hashes

- JSON SHA-256: `7cdf0f17572c351acb118e858a8fc5c206484fa6af2cf8e66531b8cd5927eea2`
- science log SHA-256: `3aa11987326590ed317b6751ae86536281896dfceb0eb8a5326425cb0047aaf0`
- full-runner log SHA-256: `bb5834f73177c3494312d43354e02b886a276aec04f084bb3ee68bcf54562da1`.

## What passed

The bounded log-linear quadrature is numerically converged:

- LL4096 vs LL8192: maximum relative changes are about `1.1e-7` in sigma8 and `3.3e-10` in f.
- LL8192 vs LL16384: maximum relative changes are about `1.1e-8` in sigma8 and `2.5e-10` in f.

The value-level LL8192/PCHIP8192 discrepancy is also small:

- f: `3.655951970370135e-05`
- sigma8_dd: `8.799490619389062e-05`
- sigma8_tt: `1.2455120884599525e-04`.

Both methods separately satisfy the frozen finite-difference consistency gate E <= 0.05 and C >= 0.995. For example at tau_H0=10:

- LL8192: E=`0.02599485727739099`, C=`0.9999311345375457`
- PCHIP8192: E=`0.01034634232543952`, C=`0.999994390741391`.

Thus neither method is internally unstable with respect to epsilon=0.025 versus 0.05.

## Why H6 failed

The eta response being differentiated is much smaller than the absolute value-level interpolation/quadrature offset. At tau_H0=10, the primary LL8192 tangent norm is only `2.7925286587329862e-06`, while the PCHIP8192 tangent norm is `4.33806367808099e-06`. The first redshift component changes sign:

- LL8192 primary first component: `+2.4917887153641516e-06`
- PCHIP8192 primary first component: `-4.104537123517105e-06`.

Consequently the full tangent comparison gives E=`1.5214518963247057`, C=`-0.699389227550778` at tau_H0=10, and similarly fails at all four tau values.

This does not identify a solver, transfer, or physical instability. R9b2f already localized the historical catastrophic direct-velocity behavior to extrapolation outside the returned CLASS k support, while R9b2e showed raw-history/transfer closure on explicit modes. R9b2h instead shows a new numerical-conditioning issue: estimating a response of order 1e-6 by subtracting two independently interpolated/integrated O(1) quantities allows a tiny method-dependent common-mode bias to dominate the derivative.

## H7 post-result qualification

The implementation requested `P_k_max_h/Mpc = 5, 10, 20`, but every returned transfer table in the completed artifact has the same

- `n_k = 108`
- `k_h,max = 4.182301935446609`.

Therefore the reported zero difference between the kmax=5,10,20 controls compares identical actual transfer support. H7 remains part of the frozen historical JSON, but it must not be interpreted as an empirical extension-to-k=20 convergence test.

## Consequence

R9b2h does not license a corrected DESI projection. It also does not justify changing the frozen E or C thresholds.

The next and final numerical construction should differentiate the power/variance functional before taking square roots and ratios. On identical CLASS k nodes define

`dP/deta = [P(+eps)-P(-eps)]/(2 eps)`

and integrate this signed difference spectrum directly on the original nodes, with no P(k) interpolation and no extrapolation. Then

`d sigma/deta = (d variance/deta)/(2 sigma_0)`

and

`d f/deta = d sigma_tt/deta / sigma_dd,0 - sigma_tt,0 d sigma_dd/deta / sigma_dd,0^2`.

This construction removes the common-mode quadrature offset before the response is evaluated. Simpson integration on the original log-k nodes is primary; trapezoidal integration on those same nodes is the independent control. The historical E<=0.05 and C>=0.995 thresholds remain unchanged.
