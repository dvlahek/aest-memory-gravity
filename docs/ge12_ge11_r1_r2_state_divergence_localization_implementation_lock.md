# GE12 GE11 R1/R2 state-divergence localization — implementation lock

## Status

Implementation locked before the first GE12 execution.

GE12 is diagnostic only. It uses the frozen GE11 Repair01 artifact and does not execute CLASS.

## Parent

Frozen parent:

`GE11_REPAIR01_DENSE_LOCAL_JET_FIXED_REFINEMENT_FAIL`.

Workflow run:

`35497478790`.

Artifact:

- ID `10600652596`;
- digest
  `sha256:b35a3a0c8bbd22483bd04c006b20ceb97d3c7f263e178382026cba2983628ecc`.

Frozen dense trace hashes:

- R1 `c50aae91fee94f00e1cbb5bd3c4d9352f15d892e91b230fad690f06c43e25fbd`;
- R2 `5a9480f69744db59ab8ca7fbdef56398c5fe38493730976d92b25873f46379b1`.

Frozen parent complete-jet cross-level maxima:

- global relative L2 `0.45886068704381233`;
- pointwise abs-or-rel `0.7829092344800966`.

## Preregistration

Commit:

`6424b782631fb923623dac0ed85019534a5245a7`.

File:

`ge12/predata_ge11_r1_r2_state_divergence_localization.json`.

Frozen blob:

`0c3fbc8b8c7c229f9b8a1232e9824151990f11ee`.

## Implementation

Commit:

`51ec675013c66296c2c3990494d2c928dd033207`.

File:

`ge12/ge11_r1_r2_state_divergence_localization.py`.

Frozen blob:

`24f387ca6922d52159e361a1bdc372e2076eb952`.

## Frozen reconstruction

GE12 imports and reuses without modification the GE09/GE11 functions:

- `read_table`;
- `group_modes`;
- `build_interps`;
- `eval_state`;
- `jet_from_state`.

The common representation is exactly:

- variable `ln(a)`;
- 64 common nodes;
- `0.2<=z<=1.5`;
- CubicHermiteSpline for derivative-aware fields;
- PCHIP for algebraic/background fields.

No interpolation family is changed.

## Frozen raw channels

- `phi`;
- `psi`;
- `delta_dark`;
- `theta_dark`;
- `alpha_aest`;
- `E_aest`;
- `Q`;
- `H_over_H0`;
- `rho_dark`;
- `p_dark`;
- `cad2_dark`;
- interpolated physical-prime channels for
  `phi,delta_dark,theta_dark,alpha_aest,E_aest`.

## Frozen derived channels

- `uA=a theta_dark/k^2`;
- `varphi=Q uA`;
- `chi=Q(uA+alpha_aest)`;
- `Pi`;
- `pt`;
- `ut_kernel=H alpha_aest-E_aest+psi`;
- `u_kernel=alpha_aest`.

## Frozen diagnostics

For every raw/derived channel:

- global relative L2;
- pointwise abs-or-rel maximum;
- cosine.

For the preregistered scale channels:

- least-squares multiplicative R2/R1 scale;
- post-rescaling relative L2.

Also:

- per-k relative L2 for the preregistered channels;
- scale fits in eight equal ln(a) bins;
- complete GE06 jet reconstruction.

## Frozen gates

Require:

- exact retained artifact metadata/digest;
- exact parent classification;
- exact R1/R2 dense trace hashes;
- exactly 64 common nodes;
- reconstructed parent global jet maximum within `1e-12`;
- reconstructed parent pointwise jet maximum within `1e-12`;
- exact derived dictionary identities within `1e-12`;
- all reported quantities finite.

No physical-amplitude or scale-fit result is a PASS gate.

## Terminal classifications

Pass:

`GE12_GE11_R1_R2_STATE_DIVERGENCE_LOCALIZED`.

Fail:

`GE12_GE11_R1_R2_STATE_DIVERGENCE_DIAGNOSTIC_FAIL`.

## Claim boundary

GE12 cannot:

- relabel GE11 Repair01;
- select R1 or R2;
- add R3;
- alter the precision values;
- alter the local-jet mapping;
- license `Z20`;
- infer a physical instability.
