# NL1C6 result — first full-J baryonic quasistatic reclosure

Final preregistered classification:

**NL1C6_FULL_J_BARYONIC_RECLOSURE_FAIL**

This FAIL is a **numerical globalization failure of the first declared solver**, not evidence that the published full-J field system has no solution.

Predata commit: `0e6c3ee66df1e215dde73ae75cfcacc957d4f69e`.

Implementation commit: `cb1fe919e96ca08c156e46877e2a266adfd3c4da`.

Workflow commit: `52ce59ae663e34b8ae04b68c416728fd888dc01e`.

GitHub Actions run: `34346092041` — technical SUCCESS with honest scientific FAIL classification.

Artifact: `results_bundle_nl1c6_full_j_baryonic_reclosure`, ID `10101742589`, SHA256 `59f8e8035e1a62c9761f3d55058fcabbb45bcf19d2c5245882bb6beb92ff3e1e`.

No observational data, finite physical eta, or memory source was used.

## Controls that passed

The NL1C5B source artifact identity passed exactly. The six requested signal-band modes were exact native-grid matches and the baryon state was finite.

Most importantly, the independently frozen high-gradient regression passed for every beta0 and every evaluation snapshot. Replacing the full interpolation by `j=1/beta0` in the same coupled implementation reproduced the published screened Helmholtz solution with maximum regression error

`1.5679255329173794e-14`.

This strongly constrains the implementation signs, the `1+beta0` factors, the physical-coordinate Laplacian, the baryonic source normalization, and the `Phi=tildePhi+chi` reconstruction.

## Why the full-J run failed

All nine co-primary full-J branches stopped at the same location:

- first native slice: `z = 6.000000000000045`;
- first frozen source-homotopy amplitude: `lambda = 1/64`;
- Newton iteration: `0`;
- GMRES: converged (`info = 0`);
- failure: `line_search_failed_gmres_0`;
- relative residual before the rejected step: `1.0`.

Thus no physical full-J snapshot was accepted, no resolution comparison was reached, and no branch-selection test was reached. The zero values printed for aggregate residual/resolution maxima are therefore empty pre-solution placeholders and must not be interpreted as successful field residuals.

The uniform iteration-zero failure across Simple, Exponential, and Sharp and across all three beta0 values indicates that the first globalization path leaves the local zero-field basin too aggressively. Near the homogeneous state, the full-J operator has vanishing first derivative while the nonlinear spatial term grows beyond the mass-dominated linearization as the Newton step is applied. The fixed first homotopy amplitude and finite backtracking range were therefore insufficient to establish a descent step.

## Consequence

NL1C6 remains an immutable FAIL under its preregistered numerical prescription. It does **not** reject the full published AeST quasistatic system.

The appropriate next gate is a separately preregistered solver-repair test that keeps the physical equations, baryonic source, all nine co-primary branches, resolutions, residual gates, and branch-consistency gates unchanged, while replacing only the failed globalization strategy by a deterministic continuation that starts closer to the zero-source solution and verifies convergence independently of the previous failed path.
