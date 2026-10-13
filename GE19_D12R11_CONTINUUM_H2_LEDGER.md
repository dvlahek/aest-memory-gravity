# GE19 D12R11 continuum-H2 proof ledger

Status date: 2026-10-13

Frozen science branch: `physics-first-gravitational-elasticity`

Frozen science HEAD used by the D12R11 campaign:

`6282ed54e35d4db6b58fcd13d1c7403419f8afb7`

This ledger is intentionally maintained on a documentation branch so that documenting results does not advance the frozen science HEAD and invalidate scripts that lock that commit.

## Purpose

D12R11 closes the physical continuum error of the mixed H2 state `Z11` used by the H4 weakly nonlinear memory calculation.

The H2 equation is

```text
L_GE06 Z11 = -2 M1_GE05[Z10,q10]
```

with the exact Repair32B forcing contract

```text
B10 = X10 - weighted_z10
```

followed by the frozen factor-two GE05 M1 map.

The goal is a componentwise continuous physical error enclosure for `Z11`. The proof is decomposed into a numerical-approximant residual term, a true-continuum forcing term, an initial-boundary term, and the already frozen D3 weighted stability propagation.

## Non-negotiable campaign rules

- Do not change the frozen H4 science gate `H4_active_shift_Nt128_Linf <= 1e-6`.
- Do not use observations or lensing to tune theory.
- Do not relabel historical FAIL results.
- Do not reopen the completed D55 bath/Ward H-channel campaign as if it were the H2 `weighted_z10` functional.
- Do not rerun the Cr12i 12/24/48 convergence ladder.
- Do not rebuild a new `Z11` approximant unless a frozen parent is shown to be invalid.
- Do not repeat a CLOSED audit unless a parent SHA changes or a concrete contract conflict is found.
- A route/provenance audit is not a science certificate.
- Keep the nominal-drive bath proof separate from the true-`X10` perturbation proof.

## Inherited CLOSED parents

### D12R10 canonical operator

The original-action canonical H1/H2 operator has already been validated interval-wise. The D12R10 operator/stability work is inherited and is not to be redone inside D12R11.

Key inherited closures:

- D12R10B5 Lambda-inclusive production/base equivalence: CLOSED.
- D12R10C pointwise interval canonical operator: CLOSED.
- D12R10D1 all-interval operator regularity: CLOSED.
- D12R10D2R1 all-interval Hermite residual machinery: CLOSED.
- D12R10D3A3R1 weighted directed stability: CLOSED.
- D12R10D3B2 global componentwise H1 propagation: CLOSED.
- D12R10D3C4 frozen GE15/GE18 initial-state binding: CLOSED.

Frozen D3 weight vector:

```text
[1.0,
 4.2600064233019915e-07,
 18.824651094825395,
 7.473544456039019e-05,
 70.05131661239456,
 0.0037932905339115967,
 1.5514636208127106e-06,
 0.014275398389646789]
```

D3A3R1 key stability result:

```text
GLOBAL_MAX_SEGMENT_LOG_GROWTH = 12.7322549055
GLOBAL_MAX_SEGMENT_AMPLIFICATION = 3.384917184e5
GLOBAL_COMPONENT_RADIUS_MAX = 0.064169650686
STABILITY_SUBDIVISION_FROZEN = 8
```

### H2 exact forcing identity

Cr12AAR1 established the same-parent GE05 M1 identity:

- `B10 = X10 - weighted_z10`.
- direct metric and pt M1 terms are zero.
- direct-action M1 reproduces Repair32B `source_from_B`.
- factor two remains exactly 2.
- same-parent relative defect was approximately `2.48e-16`.

This identity is CLOSED and must not be re-derived again unless the source contract changes.

### H2 initial boundary

Fresh-R2 boundary work established that the initial H2 derivative is bound to the physical R2 parent. The fresh-R2 initial derivative versus inherited Z11 derivative difference was approximately `4.27e-22`.

The initial-boundary route is therefore inherited as a frozen-parent binding. Final D12R11 propagation still needs to package the corresponding initial-error contribution explicitly.

## D12R11 ledger

### D12R11A — Repair32B route audit

**Status: CLOSED / route audit**

Result:

- retained exact GE05 M1 source map and canonical H2 operator,
- identified PCHIP/IVP representation dependencies that are not continuum proofs,
- established that the physical proof must replace representation assumptions with continuous-parent enclosures.

No new H2 solve.

### D12R11B — existing Cr12i approximant audit

**Status: CLOSED / route audit**

Result:

- Cr12i already supplies the selected fine48 numerical `Z11` approximant,
- no new convergence campaign is required,
- D3 operator/stability proof is reusable,
- only the continuous forcing error, continuous residual, and physical error propagation remained open.

Cr12i parent classification:

`GE19_D55CR12I_FINE48_Z11_QGE06_EXACT_STAGE_PARENT_PASS_H4_RECLOSURE_OPEN`

### D12R11C — GE05/H2 forcing identity audit

**Status: CLOSED / contract audit**

Result:

- Repair32B equation confirmed as `L_GE06 Z11 = -2 M1_GE05`,
- `B10 = X10 - weighted_z10`,
- Cr12AAR1 reproduces the same direct-action M1 source,
- D55Cr11f Ward H-channel is NOT the H2 `weighted_z10` forcing functional and must not be reused as such,
- full fine48 `Z11` trajectory was not previously persisted.

### D12R11D — full fine48 Z11 artifact replay

**Status: CLOSED / artifact certificate**

Classification:

`GE19_D12R11D_FULL_SUB48_Z11_ARTIFACT_REPLAY_PASS_CONTINUUM_ERROR_OPEN`

Result:

- materialized the already selected sub48 / `Nt=6097` trajectory,
- no new convergence ladder,
- no new science solve.

Frozen replay controls:

```text
H1_state_relL2 = 0
H1_dot_relL2 = 0
X10_relL2 ~= 5.78e-19
weighted_z10_relL2 ~= 5.13e-16
B10_relL2 ~= 2.89e-17
Z11_relL2 = 0
Z11dot_relL2 = 0
H2 linear residual ~= 3.87e-16
```

Local artifacts:

```text
results/d47_offclock_first_interval/ge19_d12r11d_full_sub48_z11_artifact_replay.json
results/d47_offclock_first_interval/ge19_d12r11d_full_sub48_z11_artifact_replay.npz
```

Known hashes:

```text
JSON SHA256 = 4a772409dd7ec8f61097922f3d6dbf57a10a288b718e6f45ebbb77c97bf61f1d
NPZ  SHA256 = 2c83c285541f1bea17dd789e926ffaa6d2211370d272fa61a4c3c5252042adf2
```

Claim boundary: artifact identity only. Physical continuum `Z11` error remained open.

### D12R11E — nominal fine48 continuous Z11 residual

**Status: CLOSED / rigorous nominal residual certificate**

Result:

- all six modes,
- 6096 intervals per mode,
- total 36576 continuous intervals,
- validated original-action canonical operator,
- frozen mathematical PCHIP forcing generated from the fine48 source,
- no new H2 solve.

Key result:

```text
global max weighted component residual upper = 5.623409858451296e-09
global minimum Az pivot lower ~= 8.1457101547e-04
worst mode = 20
worst canonical component = 5
worst interval = final interval
```

Claim boundary: rigorous residual of the frozen numerical approximant against the nominal fine48 PCHIP forcing. It does NOT include true-continuum `B10/M1` forcing error.

### D12R11F1A — original fine48-drive majorant inheritance audit

**Status: historical FAIL / preserved**

The audit compared different start epochs and reported a required majorant inflation. This was a contract error, not a physics failure.

Do not relabel this result.

### D12R11F1A-R1 — corrected full-history majorant binding

**Status: CLOSED / contract certificate**

Result:

- exact target clock alignment,
- exact piecewise-linear base-node replay,
- corrected Cr11b state majorants valid for the fine48 drive,
- no bath solve.

Key values:

```text
global max delta-X sup upper ~= 7.46e-09
global max relative B-energy inflation ~= 2.4660e-03
```

The correction is small and does not require reopening the D55 bath campaign.

### D12R11F1 — continuum-r weighted-z10 node enclosure

**Status: CLOSED / science-relevant bath certificate**

Classification:

`GE19_D12R11F1_FINE48_DRIVE_CONTINUUM_R_WEIGHTED_Z10_NODE_ENCLOSURE_PASS_CONTINUOUS_TIME_AND_TRUE_X_OPEN`

Result:

- continuum bath measure handled in `t=(2/pi) atan(r)`,
- direct signed Cr11e interval propagation on compact-core cells,
- analytic low-r state bound,
- analytic UV `z=X+u` tail,
- all 6097 fine48 target nodes certified against frozen `Nq=2048 weighted_z10`.

Key result:

```text
global max node continuum-r weighted-z10 error upper ~= 2.3866933783e-06
worst mode = 20
worst node = final target node
```

Known parent/output lock used by the proof:

```text
D12R11F1 NPZ SHA256 = 74b7bf180ee6712d56bda840e72211e4ed31c9ec414507a8a25948d130488944
D55Cr11e source SHA256 = 8f5e99ff9ff492076074d51f8cfb5e81aedbe742e05c03dbc63dc486bf308fa4
```

Claim boundary: continuum-r error at all fine48 nodes for the nominal fine48 drive. Continuous time and true physical `X10` were still open.

### D12R11F1 implementation-only first attempt

**Status: historical implementation FAIL / preserved**

The first F1 script failed before any bath propagation because a local variable named `git` shadowed the global `git()` helper. The minimal rename fixed the script. This event has no science meaning and must not be interpreted as a failed bath certificate.

### D12R11F1B — continuous-in-step weighted-z10 extension

**Status: CLOSED / nominal-drive continuous-time certificate**

Result:

- no new bath propagation,
- extended F1 node certificates continuously across every fine48 interval,
- compared the physical continuum bath state to a proof-only piecewise-linear interpolation of the frozen finite-bath `weighted_z10` nodes.

Key result:

```text
global max continuous-in-step PL-reference error upper ~= 6.2801129568e-06
worst mode = 20
worst interval = final fine48 interval
```

Dominant worst-case pieces were approximately:

```text
UV u variation       ~= 3.21e-06
node enclosure        ~= 2.39e-06
midband variation     ~= 6.78e-07
low-r variation       ~= 1.11e-09
```

Claim boundary: nominal fine48 drive only. The piecewise-linear reference is a proof reference, not a new physical finite-bath solver. True physical `X10` uncertainty remains open.

### D12R11F2A — true-X reference and bath-majorant contract

**Status: CLOSED / route-provenance audit**

Result:

- D55Cr10b already provides rigorous continuous-in-step physical `X10` error versus the D17 collocation reference,
- six-mode continuous bounds are approximately `2.92e-11` to `6.56e-11`,
- global worst bound is approximately `6.5632910674e-11`,
- fine48 versus D17 at common sub4 nodes is very small but nonzero,
- common-node worst mismatch is `1.3691072562e-11` for mode 20,
- Cr11b `B_energy` does NOT include Cr10 true-`X10` uncertainty,
- Cr11b `B_energy` is constructed from the nominal full-history/D17 path and its TV/initial-value majorant.

Do not replace a continuous reference binding by the common-node mismatch alone.

### D12R11F2B0 — Cr10 continuous-reference contract

**Status: CLOSED / static source-contract audit**

No H1 solve, bath propagation, or H2 solve was performed.

The Cr10 source already contains the continuous machinery that had been at risk of being re-audited repeatedly:

- D17 dense-sub4 canonical trajectory is the numerical reference,
- 508 D17 sub4 steps,
- `NSPLIT=64` rigorous subsegments per D17 step,
- Radau stages are rebuilt from the archived D17 endpoints,
- the collocation state inside a step is the quadratic polynomial generated from `ya`, `fy1`, and `fy2`,
- the physical `X10` functional uses an interval original-action row contracted with the signed propagated center plus variation/radius terms,
- all 64 subsegments and the archived right endpoint are included.

The Cr10 local cache contains only:

```text
next_step
A   (508,8,8)
D   (508,8,8)
q   (508,8)
qc  (508,8)
qr  (508,8)
```

The cache does NOT directly store a sampled continuous `X10` reference array. The continuous D17 collocation reference is reconstructed from the archived D17 trajectory and Radau stage data inside the Cr10 source.

Therefore the genuinely open bridge is NOT another Cr10 audit. It is the rigorous continuous difference between:

1. the D17 collocation `X10` reference already used by Cr10, and
2. the fine48 piecewise-affine `X10` drive used by the F1/F1B bath proof.

## Current CLOSED/OPEN matrix

| Component | Status |
|---|---|
| exact GE05 M1 forcing identity | CLOSED |
| full selected fine48 `Z11` artifact | CLOSED |
| nominal continuous `Z11` residual | CLOSED |
| D3 weighted H2 operator stability | CLOSED / inherited |
| initial physical H2 parent binding | CLOSED / inherited, final packaging pending |
| continuum-r nominal-drive `weighted_z10` at nodes | CLOSED |
| continuous-time nominal-drive `weighted_z10` | CLOSED |
| Cr10 true-to-D17 continuous `X10` certificate | CLOSED / inherited |
| D17 common-node to fine48 `X10` binding | CLOSED as diagnostic only |
| D17 continuous collocation reference to fine48 affine drive | OPEN |
| bath response to true-`X10` drive uncertainty | OPEN |
| true continuum `B10` error | OPEN |
| true GE05 M1 / H2 forcing error | OPEN |
| physical continuum `Z11` error | OPEN |
| H4 M5/M9 derivative envelopes | NOT STARTED in D12R11 |
| full original H4 Ward | OPEN |
| `Z21` | OPEN |
| lensing | NOT LICENSED |

## Next genuinely open proof route

Do not perform another inventory of Cr10, Cr11b, Cr11e, Repair32B, or Cr12i unless a parent mismatch is discovered.

### F2B — D17 collocation-reference to fine48-affine X10 binding

Construct a rigorous continuous-in-step enclosure of

```text
X10_D17_collocation(x) - X10_fine48_affine(x)
```

on the full target window.

Requirements:

- reuse the frozen D17 archived trajectory,
- reuse the exact Radau-2 collocation polynomial already reconstructed by Cr10,
- use the original-action `X10` functional,
- compare against the fine48 affine drive on the 12 fine48 substeps corresponding to each D17 sub4 step,
- no new H1 solve,
- no new science threshold.

Then combine with the existing Cr10 true-to-D17 continuous error to obtain a rigorous true-to-fine48 drive bound.

### F2C — bath response to true-X perturbation

For the bath difference driven by `delta X`, rigorously bound the response of

```text
z' = r^2 p
p' = -c p - (z-X)
```

and integrate the resulting `delta z` over the continuum bath measure.

This step must be a dynamical perturbation proof. Do not assume an `L-infinity` contraction without proving it.

### F2D — exact B10/M1/H2 forcing bridge

Use

```text
delta B10 = delta X10 - delta weighted_z10
```

and the already CLOSED linear Repair32B/Cr12AAR1 M1 identity to obtain the true H2 forcing-error enclosure.

### D12R11G — final physical continuum Z11 propagation

Combine:

1. D12R11E nominal residual,
2. F2D true forcing error,
3. frozen physical initial-boundary error,
4. frozen D3 componentwise weighted stability.

Only after this propagation may the ledger record

```text
TRUE_PHYSICAL_CONTINUOUS_Z11_ERROR_ENCLOSED = True
```

## Stop conditions

The following are not valid reasons to reopen prior work:

- wanting a smaller diagnostic number when the current bound is already rigorous,
- changing bath cell resolution without a demonstrated need,
- replacing the UV proof because it dominates but still gives an adequate rigorous enclosure,
- rechecking Cr10 continuous-X implementation after F2B0,
- rerunning Cr12i convergence,
- rerunning D17 H1 numerical convergence.

A prior CLOSED item is reopened only if a parent SHA changes, a source contract changes, or a concrete inconsistency is demonstrated.
