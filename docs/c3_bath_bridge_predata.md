# C3 direct bath-bridge pre-data declaration

## Status and purpose

This diagnostic is preregistered after the completed C3-R4 dense full-history reference run `34478778787` on commit `e7b7fa01c4db8d3168a38f746a78f806032b289b`, and before any direct CLASS-versus-offline bath-state comparison is generated.

Historical D2C6C-R3 and C3-R4 classifications remain immutable FAILs. This audit is diagnostic only. It cannot relax any gate and cannot license finite positive physical eta.

R4 showed that the corrected CLASS live eta=0 bath and the offline real-space bath lead to substantially different tangent amplitudes even when the CLASS forcing history is sampled densely from very early times. The next unresolved bridge is therefore the bath representation itself.

## Frozen inputs

The audit retains exactly:

- corrected CLASS v3.3.4 SHA `e85808324f51fc694d12e3ed7439552a3c3f9540`;
- the existing AeST eta=0 base trajectory and positive compressed bath;
- physical `eta=0`;
- tau-H0 = 1;
- bath order 39;
- the six frozen modes `k_h=[0.03,0.05,0.08,0.10,0.15,0.20] h/Mpc`;
- the nine frozen checkpoints `z=[6,5,4,3,2,1.5,1,0.5,0.2]`;
- the R3 modewise prehistory convention and the same offline analytic bath propagator;
- no nonlinear completion, tangent forcing, finite eta, likelihood, or parameter fit.

## Representation identity to test

CLASS evolves normalized coordinates `q_j` satisfying

`q_j'' + 2 H_conf q_j' + a^2 omega_j^2 q_j = a k omega_j sqrt(w_j) chi`.

The offline bath coordinate `z_j` is defined by

`z_j'' + 2 H_conf z_j' + a^2 omega_j^2 z_j = a omega_j^2 chi`.

The frozen algebraic mapping is

`z_j = omega_j q_j / (k sqrt(w_j))`.

Consequently the two residuals must agree,

`B_CLASS = sum_j [w_j chi - sqrt(w_j) (a omega_j/k) q_j]`

and

`B_offline = chi - a sum_j w_j z_j`,

using the same positive order-39 weights whose sum is one.

## Instrumentation

A CLASS instrumentation-only patch exposes the already-evolved order-39 bath coordinates `q_j` and `p_j=q_j'` in dense scalar perturbation output for the six frozen `k_output_values`. It must not alter their evolution equations or the physical closure.

The audit reconstructs `chi` from the same CLASS `alpha_aest`, `theta_cdm`, scale factor and background `Q` used elsewhere in D2C6C. For each mode independently, the offline `z_j` bath is initialized at the first retained dense CLASS history point with the transformed CLASS state

`z_j(tau_first)=omega_j q_j(tau_first)/(k sqrt(w_j))`

and

`z_j'(tau_first)=omega_j p_j(tau_first)/(k sqrt(w_j))`.

This initialization deliberately removes any uncertainty from unobserved pre-output history. From that common state onward, CLASS and offline propagation are compared over exactly the same retained base trajectory. No zero reset is used in this audit.

## Frozen diagnostics

At each of the nine checkpoints, for each of six modes:

1. `Z_STATE_REL`: relative L2 error across the 39 transformed bath coordinates between offline `z_j` and transformed CLASS `q_j`.
2. `ZP_STATE_REL`: relative L2 error across the 39 transformed bath derivatives between offline `z_j'` and transformed CLASS `p_j`.
3. `B_REL`: relative error between `B_offline` and `B_CLASS`, normalized by the larger of `|B_CLASS|` and `1e-12` times the maximum `|B_CLASS|` on that mode's nine-checkpoint trajectory.
4. `CHI_REL`: consistency check for the scalar source used by both paths; the offline source interpolation and CLASS dense-history `chi` must agree at the checkpoints to relative error <= `1e-8`.

The audit also reports per-mode and global maxima for `Z_STATE_REL`, `ZP_STATE_REL`, `B_REL`, and `CHI_REL`.

## Predeclared interpretation thresholds

These are diagnostic thresholds, not D2C6C acceptance gates.

- `BATH_STATE_BRIDGE_PASS=True` only if global max `Z_STATE_REL <= 5e-3` and global max `ZP_STATE_REL <= 5e-3`.
- `B_RESIDUAL_BRIDGE_PASS=True` only if global max `B_REL <= 5e-3`.
- `SOURCE_BRIDGE_PASS=True` only if global max `CHI_REL <= 1e-8`.

If source bridge fails, the result is `C3_BATH_BRIDGE_INCOMPLETE` because the two solvers were not demonstrably driven by the same base source.

If source bridge passes but bath-state or residual bridge fails, the result is `C3_BATH_BRIDGE_MISMATCH_IDENTIFIED`.

If all three pass, the result is `C3_BATH_BRIDGE_PASS`, which means the bath implementation itself is consistent and the remaining C3 discrepancy lies downstream in the tangent/source bridge.

No threshold may be changed after output is seen. Any repair identified from this audit requires a separate pre-data declaration.

`FINITE_POSITIVE_ETA_NONLINEAR_MEMORY_LICENSED=False` for every outcome of this audit.
