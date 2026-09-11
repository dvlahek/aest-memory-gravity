# Full-J mode-coupling Jacobian — locked result

Date: 2026-09-11

Branch: `fullj-mode-coupling-jacobian`

## Lineage

- preregistration / pre-data: `3da01842fce5a54a852c3f7736d7cb0c8f267341`
- initial Jacobian implementation: `29acf393580d08b5d5ddd70c3ec5c7f55d68ec60`
- dense-background regression fix finalized at: `7b0bb76e56f4ac8db80644e4469230f8b0415998`
- locked summary commit parent: `7cfaf60119257fb3b762b8ee9a8cd922622c6f62`

## Final classification

```text
FULLJ_MODE_COUPLING_JACOBIAN_NODE_COUPLING_SUPPORTED
FULLJ_JAC_EXIT=0
OBSERVATIONAL_CLAIM_LICENSED=False
```

The diagnostic completed all 27 preregistered nonlinear backgrounds and all 351 tangent solves.

## Frozen numerical result

```text
complete_backgrounds = 27 / 27
diag_uv_stable_backgrounds = 27 / 27
expected_tangent_solves = 351
diag_slope_min = -2.081550211198209
diag_slope_median = -2.0056427140938844
diag_slope_max = -1.9150696997181162
tangent_residual_max = 9.956119175663654e-11
z0p25_node_support_branches = 9 / 9
z0p25_coupling_ratio_median = 1.6926065628668243
z0p25_diag_bump_median = 0.8661087943237868
```

The dense-background regression guard reproduced the completed dense-map source realization before any nonlinear/Jacobian solve:

```text
z=0.25 delta_rms = 2.871804732026e+01
z=0.25 nodeN(k=0.6) = 1.165387182751e-01
z=0.5  delta_rms = 1.053860907840e+01
z=1.0  delta_rms = 1.754686661334e+00
```

## Node / mode-coupling result

At `z=0.25`, all 9 co-primary interpolation/beta branches satisfy the preregistered node-coupling support test. Across these branches:

- source-node ratio at `k=0.6 Mpc^-1`: approximately `0.11654`;
- raw transfer bump: approximately `10.20` to `15.29`;
- local diagonal Jacobian bump: approximately `0.848` to `0.892`;
- off-diagonal row-coupling ratio: approximately `1.39` to `3.36`;
- every branch has `supports_node_coupling=True` (preregistered robust gate required at least 6/9).

Representative `z0.25_simple_b1`:

```text
source_node_ratio = 0.1165387182751355
raw_transfer_bump = 10.774611378076882
local_diag_bump = 0.8532202739925832
row_coupling_ratio = 1.5967312887110265
dominant_offdiag_input_k_Mpc = 0.025
supports_node_coupling = True
```

## Locked interpretation

The large low-redshift bump in the raw ratio

\[
T_\Phi(k)=\frac{|\Phi_k|}{|S_k|}
\]

is not a singular local ultraviolet response of the tested full-`J` operator. It is explained by the combination of a small source Fourier coefficient (a source node) and nonlinear off-diagonal mode coupling in the frozen multimode full-`J` state.

The local diagonal response is UV-stable on every tested background and is numerically close to

\[
K_{ii}(k)\propto k^{-2},
\]

with the median fitted high-`k` slope `-2.0056427140938844`.

Therefore the completed dense-map nonmonotonicity must not be interpreted as evidence for an intrinsic full-`J` high-`k` runaway. Conversely, this result does not establish an observational lensing prediction or an ACT fit.

## Scope and limits

This result is restricted to the tested frozen quasistatic nonlinear reclosure:

- baryonic source realization extracted from the pinned nonredundant F-state CLASS calculation;
- no nonlinear matter re-evolution;
- eta = 0;
- memory disabled;
- no ACT likelihood;
- no observational claim;
- the current full-`J` solver returns the scalar potential `Phi`; an independently certified `Psi` / Weyl-potential closure is still required before CMB-lensing projection.

The nonlinear response is a mode-coupled operator, not a generally valid scalar transfer function `T(k,z)`.

## Artifact SHA256 manifest

```text
c03de9e4da5a0a1fdcbaa45e05297ef445ebe305f607fa28d6a7dbfd719742fd  fullj_mode_coupling_jacobian_bundle.zip
b2628861874357484637ab9503187f1120fe64050e13077d26a8678166a205bc  fullj_mode_coupling_jacobian_summary.csv
96cf981702551824b53584a76ac96d805625564dc77a0412c95d2743535716c8  fullj_jacobian_FULL_runner.log
b818126617f2dcc9065c378615ff51a6cbd12b9dee02a817bd8def03c2c12b85  fullj_mode_coupling_jacobian.json
174805de54ced35b4ee2e436695c941dfddce3575af1a3964aba79c49d8d2c85  fullj_mode_coupling_jacobian.log
b99a44a95cce1f78b6df2bbc87995f8934b5d30b702f65ee63029d059e521a32  fullj_mode_coupling_jacobian_matrix.csv
```

## Closure decision

This node/Jacobian diagnostic is closed. No further variants of the same test are required unless a concrete implementation bug or a theory-definition inconsistency is discovered.

The next open physics problem is to derive and certify the full-`J` metric/Weyl closure required for lensing, without replacing the demonstrated mode-coupled response by an unjustified scalar `T(k,z)`.
