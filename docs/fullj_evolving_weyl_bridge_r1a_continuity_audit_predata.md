# Full-J evolving-FLRW Weyl bridge R1A — direct CLASS continuity identity audit predata

Status: **PREREGISTERED AFTER THE R1 LINEAR-CLOSURE FAIL AND BEFORE ANY R1A OUTPUT**.

Frozen label: `FULLJ_EVOLVING_WEYL_BRIDGE_R1A_CONTINUITY_AUDIT_PREDATA`.

## Motivation

The historical R0 bridge remains `FULLJ_EVOLVING_WEYL_BRIDGE_FAIL` and the R1 bridge remains a separate post-R0 repair attempt. The early R1 output improves the catastrophic R0 linear mismatch by many orders of magnitude but still fails the linear CLASS regression: the reconstructed `delta_A`, `Phi`, `Psi`, and `W` do not follow the corrected CLASS linear solution.

Before any further nonlinear 27-member rerun, isolate the effective-fluid continuity equation directly on the corrected CLASS trajectory itself. This audit contains **no nonlinear full-J solve** and cannot license Weyl power or ACT.

## Frozen inputs

Use exactly the D2C6-certified corrected CLASS environment and the same six scalar `k` histories and nine checkpoints retained by D2C6/R1:

- `k = K_MPC` from the locked D2C6 lineage,
- `z = {6,5,4,3,2,1.5,1,0.5,0.2}`,
- Newtonian gauge,
- `eta=0`, memory disabled,
- effective AeST component stored in the corrected CLASS CDM slot,
- CLASS variables `delta_cdm`, `theta_cdm`, `alpha_aest`, `E_aest`, `phi`, `psi`.

No fit, rescaling, sign change, mode deletion, checkpoint deletion, or threshold change is permitted after seeing the audit result.

## Frozen identity

For each mode and checkpoint, reconstruct the D2C5 effective-fluid quantities

`rho_A = (Q K_Q - K)/3`,

`p_A = K/3`,

`w_A = p_A/rho_A`,

`c_ad^2 = K_Q/(Q K_QQ)`,

`chi = Q(a Theta_A/k^2 + alpha)`.

Use the exact corrected CLASS pressure closure

`Pi_A = c_ad^2 delta_A + c_ad^2 k^2 [K_B E + (2-K_B) chi]/(3 a^2 rho_A)`.

The conformal-time continuity identity to be tested is

`delta_A' = 3 Hconf (w_A delta_A - Pi_A) + (1+w_A)(3 Phi' - Theta_A)`,

with `Hconf = a H` and `Theta_A = theta_cdm` in the corrected CLASS convention.

`delta_A'` and `Phi'` are evaluated from the same dense CLASS splines, not finite differences on the nine retained checkpoints.

## Frozen gates

Primary scientific gate:

- global relative L2 mismatch of the 54 values (`6 k x 9 checkpoints`) between the CLASS `delta_A'` and the full continuity RHS must be `<= 5e-3`.

Modewise guard:

- each of the six per-mode relative L2 mismatches over the nine checkpoints must be `<= 1e-2`.

Exact algebraic velocity-map guard:

- the mode-level identity `chi = Q(a Theta_A/k^2 + alpha)` inverted back to `Theta_A` must agree with corrected CLASS `theta_cdm` to `<= 1e-12` relative L2.

These thresholds are fixed before R1A output.

## Frozen diagnostics if the primary identity fails

Without changing the gate equation, record the following diagnostics over the same 54 points:

1. `Pi_required`, obtained by algebraically solving the continuity equation for `Pi_A`, and its relative L2 mismatch to `Pi_formula`.
2. The three RHS term arrays:
   - `T_H = 3 Hconf (w delta - Pi)`,
   - `T_phi = 3(1+w) Phi'`,
   - `T_theta = -(1+w) Theta`.
3. Effective multiplicative coefficients, evaluated only where the corresponding denominator is numerically resolved:
   - `c_theta = (T_H + T_phi - delta') / [(1+w) Theta]`, expected `+1`;
   - `c_phi = [delta' - T_H + (1+w)Theta] / [3(1+w)Phi']`, expected `+1`;
   - `c_H = [delta' - (1+w)(3Phi'-Theta)] / [3 Hconf (w delta-Pi)]`, expected `+1`.
4. Median, 16th, and 84th percentiles of these coefficients on a denominator mask `|denominator| > 1e-8 * max(|denominator|)`.

These are diagnostic only. No alternative convention becomes accepted from this run.

## Classification

All frozen gates pass:

`FULLJ_WEYL_R1A_CONTINUITY_IDENTITY_PASS`.

At least one frozen gate fails:

`FULLJ_WEYL_R1A_CONTINUITY_IDENTITY_FAIL`.

Input/provenance unavailable:

`FULLJ_WEYL_R1A_CONTINUITY_IDENTITY_INCOMPLETE`.

Always:

- `NONLINEAR_TRAJECTORY_RERUN=False`
- `EVOLVING_WEYL_POWER_LICENSED=False`
- `ACT_LIKELIHOOD_LICENSED=False`
- `OBSERVATIONAL_CLAIM_LICENSED=False`
