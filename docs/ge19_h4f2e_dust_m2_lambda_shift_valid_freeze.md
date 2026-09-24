# GE19 H4F2e — valid frozen dust/M2/Lambda mixed shift-action subset

## Exact result and claim boundary

Classification:
`GE19_H4F2E_SHIFT_ACTION_SUBIDENTITY_PASS`.

This valid **source-action shift-row subset** proves the
frozen GE07 dust mixed directional shift expression, the
GE05 NL0B M2 action-derived shift expression and its
exact GE05-to-GE06 factor-two H4 source mapping, and the
identically zero direct Lambda shift row. The deterministic
source-only Fourier comparison passed.

It does **not** prove complete GE06 analytic mixed
shift-source or full six-piece H4 source/parent Ward
compatibility. There was **no corrected-parent common-grid
evaluation and no H4/Z21 state solve**.
Historical Repair37 science FAIL and Repair38--44
diagnostics remain unchanged.

## Preregistration, versioning and successful CI

- preregistration:
  `ge19/h4f2e_predata_dust_m2_lambda_shift_action.json`,
  blob `a48ea8b15bf1c1141d9407c7400f416171f4b22b`;
- valid implementation:
  `ge19/h4f2e_dust_m2_lambda_shift_action_audit.py`,
  blob `7dab9b996fc97ca9a291eb90166babec1abfba23`;
- dedicated workflow:
  `.github/workflows/ge19-h4f2e-shift-action.yml`,
  blob `1e24ccf1efe98beb876e6a0f3741d13190641eac`;
- valid execution commit:
  `bf0ca930ef67437e7c23d34312b25d40ecdd580d`;
- successful GitHub run: `36027647449`;
- job: `107728145216`;
- conclusion: `success`;
- terminal marker:
  `GE19_H4F2E_SHIFT_ACTION_SUBIDENTITY_PASS`;
- artifact ID `10821105892`;
- JSON `results/ge19_h4f2e_dust_m2_lambda_shift_action.json`,
  3688 bytes;
- JSON SHA-256:
  `32b0fbc9cddd55d51b6380e6ad36c1da39229c8820974a00eb2837ca7bcf6dd2`.

All source-blob/action binding, GE07 exact mixed
polarization, GE05 first/second coefficient, GE05
M2 signed Fourier source and Lambda shift gates
passed.

## Historical unsuccessful executions (not source SCIENCE_FAIL)

The first CI run `36027249827` failed before
the final source checks because the synthetic
node/time/space grid was mis-broadcast.
That first failure is preserved in
`docs/ge19_h4f2e_first_ci_test_grid_implementation_failure_freeze.md`
and is NOT a source or physical science FAIL.

The subsequent run `36027613828` failed at
its static Git blob gate: the source file had
the corrected new blob
`7dab9b996fc97ca9a291eb90166babec1abfba23`,
but the workflow still required old blob
`0c6aa6539b8a1a2d18b9ba09e87e5fe578c691e5`.
It did not execute the source audit and produced
no result artifact. Changing only the CI's
stale blob lock enabled the valid run above;
source equations and preregistration remained
unchanged.

## Action-to-source conventions

GE07 frozen dust action:

`L_d=NLR^2 varrho[((T_t-b T_x)/N)^2-(T_x/L)^2-1]`.

Its exact independent shift Euler row is

`E_b,dust=-2LR^2 varrho W T_x`,
`W=(T_t-bT_x)/N`.

The frozen GE07 mixed source is the signed
polarized second directional coefficient and
must retain the Repair37 GE06 source
`-2*fft_low(Q_bilinear)` convention. The
second physical epsilon derivative and
the bilinear Q coefficient must not be
interchanged without the required factor.

The frozen per-node GE05 action gives

`E_b,mem=-(LR^2/2)[A(q)cosh(u)q_x+
(omega q-sqrt(w)X_phi)sqrt(w)sinh(u)phi_x]`.

At the FLRW first-order background its
second physical epsilon derivative is

`E_b,mem,20=-a^3 delta q_t delta q_x`.

The mapped M2 H4 source uses precisely
`-2*fft_low(E_b,mem,20)` **after summing
the actual frozen first-order bath nodes**.
The deterministic test verifies both
this sign/scale and the original normalized
low-mode Fourier mapping.

`L_lambda=-6rho_lambda NLR^2` does not
contain b, so its direct Euler shift
and mixed H4 shift source vanish identically.

The Stage E Y and frozen M1 source families
have zero independent shift source; they
do not imply that the combined H4 independent
shift source vanishes.

## Next step

Instantiate the remaining actual GE06
and all GE07/GE05 M2/Lambda **all-row**
source dictionary, with signed complete
parent Euler residual and boundary
terms on one corrected H3F/H3G/Z11/H1
time representation. The H4F2a–e analytic
subsets are necessary controls but do
not constitute the complete H4F2 proof.

Only after a separately frozen full
six-piece H4 source/parent Noether PASS
may a common-parent/time structural
source audit precede any new H4/Z21
science solve. The original active-shift
science threshold remains `1e-6`.
No fitted scale or source intervention.

**Z21 NOT CERTIFIED. Lensing blocked.**
