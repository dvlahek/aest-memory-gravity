# NL1C7B4 Repair15a — local result freeze

## Status

Frozen local WSL PASS result from the first locked Repair15a execution.

Terminal classification:

`NL1C7B4_REPAIR15A_DENSITY_Q_COMPLETED_STATE_CERTIFIED`

with

`SCIENCE_RC=0`.

Execution HEAD:

`a8cb5365100d104406573886466e2d6c335096c2`.

This is a local WSL science result, not an official GitHub Actions run.

## Frozen output hashes

- result JSON:
  - bytes: `12743`
  - SHA-256:
    `596c7b13c4683840bcf40f6850356e179e77f873c3a3b42ba0b54730ae80811d`
- state NPZ:
  - bytes: `103868`
  - SHA-256:
    `997d0033eeed1f3e60c1907c7938a0ea87a1cf38de6ab860340bd003d18d6e6e`
- evaluator log:
  - bytes: `12743`
  - SHA-256:
    `596c7b13c4683840bcf40f6850356e179e77f873c3a3b42ba0b54730ae80811d`
- local runner log:
  - bytes: `15236`
  - SHA-256:
    `e8ee0567a85dbde3ae193a74a511564ee6983d19021fe41fa816a8e4b878b849`

## Gate result

All Repair15a gates PASS:

- R15A_G1 exact native-k grid match for KQ accessor
- R15A_G2 inherited frozen Repair15 all gates
- R15A_G3 claim boundary

All six inherited Repair15 gates PASS:

- frozen Repair08 + Repair14a provenance
- exact Fourier density-Q completion identity
- real-space density-Q identity
- unchanged Repair08 state-field regression
- metadata/output integrity
- claim boundary

## Certified state

New state artifact:

`results/nl1c7b4_repair15a_density_q_completed_primary_states.npz`

Only `phidot_minus_Q` differs from the historical Repair08 state.

All other Repair08 state fields reproduce with maximum relative-L2 error exactly `0.0`.

The certified canonical relation is

`deltaQ_full
 = rho_A delta_A/(Q K_QQ)
 + k^2/[a^2 Q K_QQ] [K_B E_A+(2-K_B)chi]`.

No B4 residual was used to construct the correction.

## Identity precision

Maximum Fourier completion relative-L2 error across scales:

`1.2371762394800946e-16`.

Maximum real-space density-Q identity relative-L2 error:

`5.596291289812758e-16`.

Both are far below the frozen `1e-12` certification limits.

## State change

The absolute `phidot_minus_Q` corrections are small in absolute units but comparable to the historical field itself:

- scale 5:
  - correction L2 `1.1218657289874718e-18`
  - correction Linf `2.2117223556705615e-19`
- scale 10:
  - correction L2 `2.6596129593382285e-18`
  - correction Linf `5.529946667353531e-19`
- scale 20:
  - correction L2 `1.775406283243844e-18`
  - correction Linf `4.0190005968606153e-19`

## Historical boundary

- Repair08 NPZ remains immutable.
- Repair15 attempt01 remains a harness failure.
- Repair14a remains the density-Q bridge identification parent.
- no coefficient, sign, source, threshold, radial subset, scale, Y family, or beta value changed.
- no constraint projection was used.
- no nonlinear evolution or finite eta run occurred.
- no B4 PASS is claimed here.

## Licensed continuation

Only this exact certified R15a state may be consumed by a separately preregistered exact nonlinear B4 retest under the unchanged historical raw-constraint limit

`max epsilon_H <= 1e-7`

and

`max epsilon_M <= 1e-7`.

The retest must retain all 54 historical scale/grid/Y/beta cases and the two-grid control.
