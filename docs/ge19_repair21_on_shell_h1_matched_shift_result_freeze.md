# GE19 Repair21 on-shell H1 parent + matched-shift audit result freeze

## Status

Frozen first completed locked Repair21 diagnostic execution.

Classification:

`GE19_REPAIR21_ON_SHELL_H1_PARENT_MATCHED_SHIFT_AUDIT_COMPLETE`.

Frozen routing:

`INTERPOLATED_H1_PARENT_DEFECT_CONFIRMED`.

Repair19 and Repair20 remain historical results and are not relabelled.

Repair21 does not itself certify Z20.

## Frozen local outputs

Science JSON:

- bytes: `5400`;
- SHA-256: `e27d12f18a992a1c8c3217e67c0efd39dcf7c9d7aadcfbbb3220f7508bca1bb2`.

Inner FULL log:

- bytes: `5400`;
- SHA-256: `e27d12f18a992a1c8c3217e67c0efd39dcf7c9d7aadcfbbb3220f7508bca1bb2`.

Science NPZ:

- bytes: `8542781`;
- SHA-256: `c6fcde7d39480ec7f03de2acf0f33f648a997404c9cca8f83990ed7b50667f3b`.

Outer local runner log:

- bytes: `9980`;
- SHA-256: `3cb6061fedac996e52ecc9a72cd15b5e6da9563010d47ab487977aef8b9ffb02`.

Terminal marker:

`GE19_REPAIR21_DIAGNOSTIC_COMPLETE`.

## Frozen provenance

Exact frozen parent hashes:

- Repair13 JSON:
  `ae3cc790ecffbd5498b5852273c72ae578d4615de29bbb616673c05cdb3e74b7`;
- Repair13 NPZ:
  `011c0ae54fd21d70c0e2c695ce62e7b74a3c5529a07c9023c882a447d5b40ca3`;
- Repair18 JSON:
  `d5603138c2f488413686323d1241613f6ef707b586116aa7fe865ae25ceb0edc`;
- Repair19 JSON:
  `32837e04a9ea6c83642a0d465f0312cc17a02ddad168760764f3c7b999a0a14d`;
- Repair20 JSON:
  `5f1dc8e48963c6403f142958c8ce34ab1457953b47868d1a65317655cd0644eb`;
- Repair20 NPZ:
  `99937112b889bc556ada756bc7b4e834991a6019596fdbc353a40294ad3968a6`.

Repair21 confirms:

- H1 recomputed independently at target resolutions;
- no physics/source formula edit;
- no shift-metric edit;
- no shift-threshold relaxation.

## On-shell H1 parent certification controls

Nt64 frozen Repair13 reproduction:

- Z10 relative L2 max: `0.0`;
- Z10dot relative L2 max: `0.0`.

Global H1 controls:

- linear-system relative L2 max:
  `4.3389056048311334e-16`;
- shift backward error max:
  `6.370007701051935e-08`;
- anisotropy backward error max:
  `2.0133086499281873e-16`;
- initial dynamic match:
  `5.826069165486057e-14`;
- Nt64/Nt128 H1 state relative L2 max:
  `1.5405620815417885e-05`;
- all outputs finite.

All preregistered H1 gates PASS.

## Repair20 interpolated-parent counterfactual

Against the genuine Nt128 on-shell H1 parent:

- interpolated Z10 relative L2:
  `1.550833145877632e-05`;
- interpolated Z10dot relative L2:
  `1.292831927156242e-05`;
- resulting H3 main-RHS relative L2:
  `2.486632550432435e-04`.

Thus the separately interpolated H1 state/derivative parent used only by Repair20 produces a materially different H3 source even though its state-level discrepancy is small.

## Near-null definition on the on-shell Nt128 run

Nt128 scale reference:

`S_ref = 0.0030031148043192296`.

Near-null threshold:

`sqrt(eps) S_ref = 4.47498977827911e-11`.

Near-null rule:

`scale <= sqrt(eps) S_ref`.

Nt128 near-null absolute residual / S_ref:

`9.599035682049098e-15`.

This passes the frozen `1000 eps` criterion.

## Matched active shift convergence

Common physical comparison grid:

`Nt128 ln(a)`.

Active sample count:

`24057`.

Near-null sample count:

`22023`.

Matched active Linf:

- Nt64 interpolated:
  `7.79643019280292e-06`;
- Nt128:
  `8.067171929789269e-07`.

Matched active RMS/L2:

- Nt64 interpolated:
  `5.7080811823488185e-06`;
- Nt128:
  `6.394230852137805e-07`.

Observed matched orders:

- Linf:
  `3.2357755356022007`;
- RMS/L2:
  `3.1225511606202474`.

Both exceed the preregistered minimum `2.5` and are consistent with the expected third-order Radau IIA global behavior.

Most important:

`Nt128 active shift Linf = 8.067171929789269e-07 < 1e-6`.

Therefore the original active shift tolerance is satisfied without relaxation when the H1 parent is genuinely on shell.

Worst Nt128 active sample:

- C_star;
- beta0=0.5;
- m=6;
- time index 29;
- ln(a) = `-0.7486914714227706`;
- metric = `8.067171929789269e-07`;
- absolute residual = `1.0183082199879866e-16`;
- natural scale = `1.2622864974870901e-10`.

## Other H3 controls

- Nt64/Nt128 state relative L2:
  `1.520874923438771e-05`;
- linear-system relative L2 residual max:
  `2.1762890113126683e-13`;
- anisotropy backward error max:
  `6.391121604651976e-16`;
- Repair18 boundary p0 reproduction:
  `0.0`;
- all outputs finite.

Every preregistered H3 diagnostic gate PASS.

## Scientific conclusion

Repair21 confirms that the unresolved active Repair20 shift residual was caused by the off-shell first-order parent construction used in that diagnostic.

The critical distinction is:

- Repair20: separately PCHIP-interpolated Z10 and Z10dot from Nt64;
- Repair21: independently solved on-shell H1 parent at Nt128.

With the genuine on-shell parent, the active shift residual falls below the original `1e-6` threshold and converges at approximately third order.

Therefore the correct route is:

`INTERPOLATED_H1_PARENT_DEFECT_CONFIRMED`.

This is a numerical-parent consistency result, not a change to the H3 physics.

## Certification consequence

Repair21 licenses a separately preregistered Z20 certification run.

That run must use:

- independently solved on-shell H1 parents;
- the unchanged Repair14 H3 source;
- the unchanged Repair18 projected boundary;
- the unchanged Repair07 canonical integrator;
- active shift threshold `1e-6`;
- near-null rows certified by the frozen machine-level absolute-residual rule rather than by the meaningless relative ratio of two near-zero quantities;
- matched Nt64/Nt128 convergence.

Repair21 itself remains diagnostic and does not certify Z20.

## Stop rule

No q20 and no H4/Z21 until the next certification run passes and is frozen.

No observable/data bridge before Z20 certification.

No historical Repair19/20 relabelling.

## Claim boundary

Repair21 confirms the interpolated-H1-parent defect and closes the active-shift diagnostic question. It does not yet certify the physical second-order state.
