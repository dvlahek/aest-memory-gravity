# GE19 H4F2e — valid GE07, GE05 M2 and Lambda shift-action subset

## Classification and scope

`GE19_H4F2E_SHIFT_ACTION_SUBIDENTITY_PASS`.

This is a separately preregistered exact action-level **shift-row
subset** of the still-open H4F2 full signed six-piece source/parent
Noether identity. It derives and audits the independent GE07 dust
mixed shift row, the actual frozen GE05 M2 per-node shift coefficient
with GE06 raw-row mapping, and identically zero Lambda shift
variation. The H4 source is not fitted.

No corrected H3F/H3G common-grid source evaluation,
no full Noether identity and no H4/Z21 state solve occurred.

## Immutable inputs and successful run

Preregistration:
`ge19/h4f2e_predata_dust_m2_lambda_shift_action.json`,
blob `a48ea8b15bf1c1141d9407c7400f416171f4b22b`.

Corrected implementation:
`ge19/h4f2e_dust_m2_lambda_shift_action_audit.py`,
blob `7dab9b996fc97ca9a291eb90166babec1abfba23`.

Dedicated workflow:
`.github/workflows/ge19-h4f2e-shift-action.yml`,
blob `1e24ccf1efe98beb876e6a0f3741d13190641eac`.

Successful GitHub Actions run:
- run `36027647449`, job `107728145216`;
- conclusion `success`;
- terminal marker `GE19_H4F2E_SHIFT_ACTION_SUBIDENTITY_PASS`;
- artifact ID `10821105892`;
- result `results/ge19_h4f2e_dust_m2_lambda_shift_action.json`;
- JSON length `3688` bytes;
- JSON SHA-256
  `32b0fbc9cddd55d51b6380e6ad36c1da39229c8820974a00eb2837ca7bcf6dd2`.

Every exact frozen blob, action/row binding, GE07 mixed-polarization,
GE05 second-directional/normalization and deterministic Fourier
gate passed. The deterministic GE05 M2 sample uses three bath
nodes, five time samples and 256 periodic spatial points. It
does not represent a new corrected-parent propagation.

## First failed attempt preserved

The first run `36027249827`, job `107726804297`,
failed while constructing deterministic test data:
time axis `(5,1,1)` did not broadcast with
node-space array `(3,1,256)`. No result JSON was produced
and no source/physics result was inferred.

Immutable first-failure freeze:
`docs/ge19_h4f2e_first_ci_test_grid_implementation_failure_freeze.md`,
blob `e7bc1859ca0e509dc16e32d983dc6264fd2b781d`.

The only scientific-code change for the valid run
was replacing `tt=np.arange(nt)[:,None,None]`
with `tt=np.arange(nt)[None,:,None]` in the
deterministic test. Preregistration, action terms,
source signs, all gates and original 1e-6
shift science target were unchanged.

## Exact signed source identities

For the frozen GE07 action

`L_d=N L R^2 varrho [W^2-(T_x/L)^2-1]`,

`W=(T_t-b T_x)/N`,

the independent shift Euler row is exactly

`E_b,dust=-2 L R^2 varrho W T_x`.

The mixed H4 coefficient under
`epsilon (Z10+eta Z11)` is
`partial_eta partial_epsilon^2 E_b,dust|0`.
It matches the independent frozen GE07
second-directional polarization. With the
original `L Z=-E_inhom` convention,
the implemented mixed RHS is the **negative**
of this mixed Euler coefficient, equivalently
`-2 Q_GE07,bilinear` before `fft_low`.

The frozen NL0B/GE05 node action satisfies

`E_b,mem = -(L R^2/2) [A(q) cosh(u) q_x
                 +(omega q-sqrt(w)X_phi) sqrt(w)sinh(u) phi_x]`.

On the frozen first-order FLRW directional
state, its complete second epsilon derivative is

`E_b,mem^(2)=-a^3 q_t q_x`

per bath node. The frozen GE05-to-GE06
factor two and RHS minus sign therefore give

`S_b,M2=+2 a^3 sum_j(q_j,t q_j,x)`

before spatial Fourier projection. The
actual frozen `ge05.f_c2["b"]` and
`repair37.memory_m2_chunk`/source mapping
were checked with deterministic nodal fields,
not replaced by the asserted formula.

The frozen `L_lambda=-6 rho_lambda N L R^2`
has no `b` dependence, so its direct shift
source is identically zero at this order.

Stage E Y and GE05 M1 both have zero
independent shift source rows at their frozen
mixed H4 order, but M2 and the analytic GE06/GE07
terms have genuine constraint rows. The
subidentities do not imply termwise or
aggregate shift-Ward cancellation.

## Next structural obligation

Instantiate the **remaining GE06 independent
shift/anisotropy rows** and all actual
GE06/GE07/Lambda/M2 mixed H4 source and
background/H1/Z11/corrected H3F/H3G/bath/dust
parent Euler residuals in the signed H4F2b
formal Ward coefficient. This must include
the same action conventions, source-grid
derivatives and frozen GE05 normalization.
Only a subsequently frozen *full six-piece*
H4F2 proof may license a separately
preregistered common corrected-parent/time
structural audit.

Historical Repair37 remains science FAIL;
Repair38--44 remain diagnostics; H3F/H3G
remain certified within their own scopes.
Z21 remains NOT CERTIFIED and lensing blocked.
