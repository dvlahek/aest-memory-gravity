# GE19 D12R11 continuum-H2 proof ledger

Status date: 2026-10-14

Frozen science branch: `physics-first-gravitational-elasticity`

Frozen science HEAD used by the D12R11 campaign:

`6282ed54e35d4db6b58fcd13d1c7403419f8afb7`

This ledger is maintained on a documentation branch so documenting results does not advance the frozen science HEAD and invalidate scripts that lock that commit.

## High-level project position

The main project frontier is **pre-Z21**, not H2 in isolation.

```text
corrected H3 / Z20 / q20                 CLOSED
six-source H4 source construction        CLOSED
Y mixed-H4 Ward sector                   CLOSED exactly
full non-Y numerical H4 Ward budget      OPEN
full integrated physical H4 Ward         OPEN
final Z21 solve under frozen gate         NOT YET LICENSED
lensing                                   BLOCKED UNTIL Z21
```

The final science gate remains

```text
H4_active_shift_Nt128_Linf <= 1e-6
```

Historical Repair37 remains FAIL and must not be relabeled:

```text
1.1749387207106255e-06
```

On October 10 the project was correctly summarized at headline level as **finish the full H4 Ward proof, then perform the final Z21 solve**. Z21 was not actually licensed because D9 required numerical derivative/error budgets that the existing sampled/PCHIP parent representations could not rigorously support.

After D12R8 closed the Y mixed-H4 Ward contribution exactly, D12R9 identified the non-Y numerical certification bottleneck. D12R10/D12R11 are subordinate prerequisites inside this pre-Z21 H4-Ward closure, not a new main project phase.

## Non-negotiable campaign rules

- Do not change `H4_active_shift_Nt128_Linf <= 1e-6`.
- Do not use observations or lensing to tune theory.
- Do not relabel historical FAIL results.
- Do not reopen a CLOSED audit unless a parent SHA changes or a concrete contract conflict is found.
- Do not rerun the Cr12i 12/24/48 convergence ladder.
- Do not rebuild a new Z11 approximant unless a frozen parent is shown invalid.
- Do not reuse the D55 Ward H-channel bath certificate as the H2 `weighted_z10` forcing functional.
- Keep route/provenance audits distinct from science certificates.
- After a CLOSED result, record it here before starting another proof.

## Inherited CLOSED parents

### Corrected weakly nonlinear parents

- corrected-Y `Z20`: certified.
- corrected-Y `q20`: certified.
- H4F3B six source families: exact source sum PASS.
- Y mixed-H4 Ward contribution: exact zero at the frozen FLRW background.

### D12R10 canonical H1/H2 machinery

Inherited and not to be repeated:

- D12R10B5 Lambda-inclusive operator closure: CLOSED.
- D12R10C pointwise interval canonical operator: CLOSED.
- D12R10D1 all-interval operator regularity: CLOSED.
- D12R10D2R1 Hermite residual machinery: CLOSED.
- D12R10D3A3R1 directed weighted stability: CLOSED.
- D12R10D3B2 componentwise propagation: CLOSED.
- D12R10D3C4 frozen physical-parent initial binding: CLOSED.

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

### Exact H2 forcing contract

Repair32B / Cr12AAR1 established:

```text
L_GE06 Z11 = -2 M1_GE05[Z10,q10]
B10 = X10 - weighted_z10
```

Same-parent direct-action M1 reproduces the Repair32B source, the factor 2 is exact, and the same-parent relative defect is approximately `2.48e-16`.

This identity is CLOSED.

### H2 initial boundary

Fresh-R2 work showed the physical initial derivative is bound to the R2 parent. The fresh-R2 versus inherited Z11 initial derivative difference is approximately `4.27e-22`.

The final D12R11 propagation still has to include the initial contribution explicitly.

## D12R11 proof ledger

### D12R11A — Repair32B route audit

**CLOSED / route audit**

Retained the exact M1 source and H2 operator. Identified PCHIP/IVP assumptions that cannot serve as continuum certificates.

### D12R11B — Cr12i approximant audit

**CLOSED / route audit**

Cr12i already supplies the selected fine48 Z11 approximant. No new convergence campaign is required.

Parent classification:

`GE19_D55CR12I_FINE48_Z11_QGE06_EXACT_STAGE_PARENT_PASS_H4_RECLOSURE_OPEN`

### D12R11C — forcing identity audit

**CLOSED / contract audit**

Confirmed Repair32B equation, exact B10/M1 contract, and that D55Cr11f Ward H-channel is not the pointwise H2 `weighted_z10` functional.

### D12R11D — full fine48 Z11 artifact replay

**CLOSED / artifact certificate**

Classification:

`GE19_D12R11D_FULL_SUB48_Z11_ARTIFACT_REPLAY_PASS_CONTINUUM_ERROR_OPEN`

Selected trajectory: sub48 / `Nt=6097`.

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

Hashes:

```text
JSON = 4a772409dd7ec8f61097922f3d6dbf57a10a288b718e6f45ebbb77c97bf61f1d
NPZ  = 2c83c285541f1bea17dd789e926ffaa6d2211370d272fa61a4c3c5252042adf2
```

### D12R11E — nominal continuous Z11 residual

**CLOSED / rigorous nominal residual certificate**

Six modes, 6096 intervals each, total 36576 intervals.

```text
global max weighted residual upper = 5.623409858451296e-09
global minimum Az pivot lower ~= 8.1457101547e-04
worst mode = 20
worst component = 5
worst interval = final interval
```

Claim boundary: residual against nominal fine48 PCHIP forcing only. True-continuum B10/M1 forcing error is outside this certificate.

### D12R11F1A — original majorant inheritance audit

**HISTORICAL FAIL / PRESERVED**

Compared different start epochs. Contract error, not a physics failure. Do not relabel.

### D12R11F1A-R1 — corrected full-history majorant binding

**CLOSED / contract certificate**

```text
global max delta-X sup upper ~= 7.46e-09
global max relative B-energy inflation ~= 2.4660e-03
```

No bath solve.

### D12R11F1 — continuum-r weighted-z10 node enclosure

**CLOSED / bath certificate**

Classification:

`GE19_D12R11F1_FINE48_DRIVE_CONTINUUM_R_WEIGHTED_Z10_NODE_ENCLOSURE_PASS_CONTINUOUS_TIME_AND_TRUE_X_OPEN`

```text
global max node error upper ~= 2.3866933783e-06
worst mode = 20
worst node = final node
```

### D12R11F1B — continuous-in-step nominal-drive weighted-z10

**CLOSED / bath certificate**

Classification:

`GE19_D12R11F1B_FINE48_DRIVE_CONTINUOUS_IN_STEP_WEIGHTED_Z10_PL_REFERENCE_ENCLOSURE_PASS_TRUE_X_OPEN`

```text
global continuous-in-step upper ~= 6.2801129568e-06
worst mode = 20
worst interval = final interval
```

No new bath propagation and no H2 solve.

### D12R11F2A — true-X reference / majorant contract

**CLOSED / route-provenance audit**

Established that Cr10 already contains the continuous-in-step X10 certificate for the D17 collocation reference, Cr11b `B_energy` is nominal-path only, and common-node D17/fine48 agreement is not itself a continuous proof.

```text
global common-node |Xfine48-XD17| ~= 1.3691072562e-11
worst mode = 20
```

### D12R11F2B0 — Cr10 continuous-reference source contract

**CLOSED / route audit**

Confirmed 508 D17 steps, 64 rigorous subsegments per step, signed center/radius propagation, Radau-2 collocation polynomial, and continuous original-action X10 functional.

### D12R11F2B — D17 collocation to fine48 affine continuous X10 binding

**CLOSED / rigorous continuous X10 binding**

Classification:

`GE19_D12R11F2B_D17_COLLOCATION_TO_FINE48_AFFINE_CONTINUOUS_X10_BINDING_PASS`

```text
common clock max abs = 1.1102230246251565e-16
maximum D17 endpoint replay relative = 0
global max D17 -> fine48 affine upper = 8.937207651715796e-08
global max true -> fine48 affine upper = 8.943637276453392e-08
worst mode = 20
```

Per-mode true-to-fine48 continuous upper:

```text
m3  = 6.943141985919195e-10
m5  = 4.095450630188486e-09
m8  = 1.2863676398411737e-08
m10 = 2.2488462362623306e-08
m15 = 6.817607763932665e-08
m20 = 8.943637276453392e-08
```

NPZ SHA256:

`71143ebef61fb3e6078c5339d7525664652437ff5bf311932bbd3adf3964c1ad`

### D12R11F2C — true-X10 total variation and direct B10 error

**CLOSED / rigorous continuous B10 certificate**

Classification:

`GE19_D12R11F2C_TRUE_X10_TOTAL_VARIATION_DIRECT_B10_ERROR_ENCLOSURE_PASS`

The key identity is kept intact instead of separately bounding X and weighted-z:

```text
B10 = X10 - integral(z_r dmu)
    = - integral((z_r-X10) dmu)
```

For `delta u = delta z - delta X` with the identical frozen bath initial state, the Cr11b energy estimate gives

```text
sqrt(r^2 |delta u|^2 + |delta v|^2)/r
    <= |delta X(start)| + TV(delta X)
```

and the bath measure has total mass 1.

Global results:

```text
global max direct true-drive B10 error upper = 4.495551894006195e-08
global max total true-continuum B10 to finite-reference upper = 6.325068475693854e-06
worst mode = 20
```

Per-mode total true-continuum B10 upper:

```text
m3  = 4.977496681421009e-08
m5  = 2.913937143931808e-07
m8  = 9.106954135548411e-07
m10 = 1.593544800724346e-06
m15 = 4.826348367920702e-06
m20 = 6.325068475693854e-06
```

The direct true-drive term is much smaller than the nominal continuum-bath term; for mode 20 it is `4.49555e-08` versus `6.28011e-06`.

Hashes:

```text
JSON = 01362b7214ce61fd45b8c7de93d1ccd98194e9254c0c14f3883f5ae22d6172d9
NPZ  = 3d31e0c1447750b7819bb218a3d2eb5e49797d1e7b82f8829dee09f1f0000842
```

Claim boundary: the continuous physical `B10` error is CLOSED. It has not yet been mapped through the exact Repair32B canonical H2 forcing coefficients.

## Current real frontier

```text
D12R11F2D  true B10 -> exact Repair32B canonical H2 forcing error   OPEN
D12R11G    residual + forcing + initial boundary through D3         OPEN
```

After D12R11G, return immediately to the actual pre-Z21 frontier:

```text
remaining non-Y D9 numerical budgets / high derivatives / roundoff
        -> full integrated physical H4 Ward
        -> final Z21 solve
        -> apply frozen H4 gate <= 1e-6
        -> only then lensing
```

Do not treat D12R11 as the main project objective. It exists only to close one rigorous parent/error-budget requirement needed before the full H4 Ward and Z21 reclosure.

## Historical project checkpoints relevant to Z21

- 2026-09-24: corrected H3/Z20 work underway; Z21 not started because source/Ward prerequisites were incomplete.
- 2026-09-25: Z20 and q20 certified; six-source H4 construction available; physical all-parent Ward still open; Z21 and lensing blocked.
- 2026-10-10: D12R2 background/F21 work closed. Project headline: full H4 Ward next, then final Z21 solve.
- 2026-10-10 to 2026-10-11: D9 prelock exposed missing rigorous numerical budgets. D12R8 removed the Y sector structurally. D12R9 showed the remaining non-Y parents could not be justified from sampled/PCHIP representations.
- D12R10/D12R11 were opened to repair those proof foundations. They are prerequisites for the pre-Z21 Ward closure, not a replacement for Z21.

## Stop condition for repeated work

Before starting any new audit, check this ledger. If the relevant contract is CLOSED and all parent SHAs are unchanged, do not repeat it. Move to the next OPEN mathematical link.
