# GE19 D12R11 continuum-H2 proof ledger

Status date: 2026-10-14

Frozen science branch: `physics-first-gravitational-elasticity`

Frozen science HEAD used by the D12R11 campaign:

`6282ed54e35d4db6b58fcd13d1c7403419f8afb7`

This ledger is maintained on a documentation branch so documentation commits do not advance the frozen science HEAD.

## High-level project position

The main project frontier is **pre-Z21**, not H2 in isolation.

```text
corrected H3 / Z20 / q20                 CLOSED
six-source H4 source construction        CLOSED
Y mixed-H4 Ward sector                   CLOSED exactly
D12R10/D12R11 continuous Z11 parent      CLOSED
full non-Y numerical H4 Ward budget      OPEN
full integrated physical H4 Ward         OPEN
final Z21 solve under frozen gate         NOT YET LICENSED
lensing                                   BLOCKED UNTIL Z21
```

Frozen science gate:

```text
H4_active_shift_Nt128_Linf <= 1e-6
```

Historical Repair37 remains FAIL and is never relabeled:

```text
1.1749387207106255e-06
```

The October 10 project headline remains correct: finish the full H4 Ward proof, then perform the final Z21 solve. D12R10/D12R11 were opened only because the D9 prelock showed that sampled/PCHIP parent representations were insufficient for a rigorous non-Y Ward error budget.

## Campaign rules

- Do not change the `1e-6` H4 science gate.
- Do not use observations or lensing to tune theory.
- Do not relabel historical FAIL results.
- Do not reopen a CLOSED audit unless a parent SHA changes or a concrete contract conflict appears.
- Do not rerun the Cr12i 12/24/48 ladder.
- Do not rebuild a new Z11 approximant unless a frozen parent is shown invalid.
- Keep route/provenance audits distinct from science certificates.
- Record each CLOSED result here before moving to the next open mathematical link.

## Inherited CLOSED parents

### Corrected weakly nonlinear parents

- corrected-Y `Z20`: certified.
- corrected-Y `q20`: certified.
- H4F3B six source families: exact source sum PASS.
- Y mixed-H4 Ward contribution: exact zero at the frozen FLRW background.

### D12R10 canonical H1/H2 machinery

- D12R10B5 Lambda-inclusive operator closure: CLOSED.
- D12R10C pointwise interval canonical operator: CLOSED.
- D12R10D1 all-interval operator regularity: CLOSED.
- D12R10D2R1 Hermite residual machinery: CLOSED.
- D12R10D3A3R1 directed weighted stability: CLOSED.
- D12R10D3B2 componentwise propagation: CLOSED.
- D12R10D3C4 frozen physical-parent initial binding: CLOSED.

Frozen D3 weights:

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

Repair32B / Cr12AAR1:

```text
L_GE06 Z11 = -2 M1_GE05[Z10,q10]
B10 = X10 - weighted_z10
```

Same-parent direct-action M1 reproduces the Repair32B source, the factor 2 is exact, and the same-parent relative defect is about `2.48e-16`.

### H2 initial boundary

Fresh-R2 versus inherited Z11 initial dynamic derivative difference:

```text
4.268123713790712e-22
```

The same frozen Repair32B boundary is retained.

## D12R11 proof ledger

### D12R11A — Repair32B route audit

**CLOSED / route audit**

Retained the exact M1 source and H2 operator. Identified PCHIP/IVP assumptions that could not by themselves serve as continuum certificates.

### D12R11B — Cr12i approximant audit

**CLOSED / route audit**

Cr12i already provides the selected fine48 Z11 approximant. No new convergence campaign is required.

Parent classification:

`GE19_D55CR12I_FINE48_Z11_QGE06_EXACT_STAGE_PARENT_PASS_H4_RECLOSURE_OPEN`

### D12R11C — forcing identity audit

**CLOSED / contract audit**

Confirmed Repair32B equation, exact B10/M1 contract, and that the D55 Ward H-channel certificate is not the pointwise H2 `weighted_z10` functional.

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

```text
global max weighted residual upper = 5.623409858451296e-09
global minimum Az pivot lower ~= 8.1457101547e-04
worst mode = 20
worst component = 5
worst interval = final interval
```

JSON SHA256:

`438c42ff33372f4665ecdb3e2690fafb2f3c08ce86837dd6b414beee4fceb64d`

### D12R11F1A — original majorant inheritance audit

**HISTORICAL FAIL / PRESERVED**

Compared different start epochs. Contract error, not a physics failure. Never relabel.

### D12R11F1A-R1 — corrected full-history majorant binding

**CLOSED / contract certificate**

```text
global max delta-X sup upper ~= 7.46e-09
global max relative B-energy inflation ~= 2.4660e-03
```

### D12R11F1 — continuum-r weighted-z10 node enclosure

**CLOSED / bath certificate**

Classification:

`GE19_D12R11F1_FINE48_DRIVE_CONTINUUM_R_WEIGHTED_Z10_NODE_ENCLOSURE_PASS_CONTINUOUS_TIME_AND_TRUE_X_OPEN`

```text
global max node error upper ~= 2.3866933783e-06
worst mode = 20
```

### D12R11F1B — continuous-in-step nominal-drive weighted-z10

**CLOSED / bath certificate**

Classification:

`GE19_D12R11F1B_FINE48_DRIVE_CONTINUOUS_IN_STEP_WEIGHTED_Z10_PL_REFERENCE_ENCLOSURE_PASS_TRUE_X_OPEN`

```text
global continuous-in-step upper ~= 6.2801129568e-06
worst mode = 20
```

### D12R11F2A — true-X reference / majorant contract

**CLOSED / route-provenance audit**

Cr10 contains the continuous-in-step X10 certificate for the D17 collocation reference. Cr11b `B_energy` is nominal-path only. Common-node agreement is not itself a continuous proof.

```text
global common-node |Xfine48-XD17| ~= 1.3691072562e-11
```

### D12R11F2B0 — Cr10 continuous-reference source contract

**CLOSED / route audit**

Confirmed 508 D17 steps, 64 rigorous subsegments per step, signed center/radius propagation, Radau-2 collocation polynomial, and continuous original-action X10 functional.

### D12R11F2B — D17 collocation to fine48 affine continuous X10 binding

**CLOSED / rigorous continuous X10 binding**

Classification:

`GE19_D12R11F2B_D17_COLLOCATION_TO_FINE48_AFFINE_CONTINUOUS_X10_BINDING_PASS`

```text
global max D17 -> fine48 affine upper = 8.937207651715796e-08
global max true -> fine48 affine upper = 8.943637276453392e-08
worst mode = 20
```

NPZ SHA256:

`71143ebef61fb3e6078c5339d7525664652437ff5bf311932bbd3adf3964c1ad`

### D12R11F2C — true-X10 total variation and direct B10 error

**CLOSED / rigorous continuous B10 certificate**

Classification:

`GE19_D12R11F2C_TRUE_X10_TOTAL_VARIATION_DIRECT_B10_ERROR_ENCLOSURE_PASS`

```text
global max direct true-drive B10 error upper = 4.495551894006195e-08
global max total true-continuum B10 to finite-reference upper = 6.325068475693854e-06
worst mode = 20
```

Hashes:

```text
JSON = 01362b7214ce61fd45b8c7de93d1ccd98194e9254c0c14f3883f5ae22d6172d9
NPZ  = 3d31e0c1447750b7819bb218a3d2eb5e49797d1e7b82f8829dee09f1f0000842
```

### D12R11F2D — exact Repair32B canonical H2 forcing error

**CLOSED / rigorous continuous H2 forcing certificate**

Classification:

`GE19_D12R11F2D_EXACT_REPAIR32B_CANONICAL_H2_FORCING_ERROR_PASS`

```text
raw aether = Q*a^3*B10
raw scalar = -a^2*(i*k)*B10
canonical pu = -raw_aether/H
canonical pphi = -raw_scalar/H
normalization factor = 2 exactly
```

Canonical source-map contract defect: exactly zero.

```text
global max canonical H2 forcing error upper = 2.374712650678017e-03
worst mode = 20
worst component = p_phi
worst interval = 6095
```

NPZ SHA256:

`a9e7075525fc6e9c0a41d1efe7e664ca6b3d62a316b99bd3133a68242ef48687`

### D12R11G — physical continuum Z11 error propagation

**CLOSED / rigorous physical continuum Z11 certificate**

Classification:

`GE19_D12R11G_PHYSICAL_CONTINUUM_Z11_ERROR_ENCLOSURE_PASS_H4_RECLOSURE_PARENT_READY`

G combines D12R11E nominal residual, the true B10/H2 forcing error, the PL→PCHIP bridge, the D22R3 initial-boundary bridge, and frozen D3 componentwise stability.

```text
global PL -> PCHIP B10 upper = 2.0506309900867423e-11
global true -> PCHIP B10 upper = 6.325088982003756e-06
global continuous weighted-inf Z11 upper = 1.1365337328877092e-04
global continuous physical state upper = 266.79155380398845
global continuous physical derivative upper = 1.2319323690969992
worst mode = 20
```

The large physical `u` readout is a valid but coarse scalar continuous-norm conversion, not a physical blow-up.

Hashes:

```text
JSON = 782f9d85f730abf91a88c6a10ba11650cfe05ed25a33e4ef4d682af46efcb0f2
NPZ  = 8f01ee3f8d6d2cea95e08916b6a91065101599592ab07889db4383bdecfe3343
```

G remains valid and is not relabeled.

### D12R11G1 — tight continuous componentwise Z11 enclosure

**CLOSED / preferred H4 parent certificate**

Classification:

`GE19_D12R11G1_TIGHT_CONTINUOUS_COMPONENTWISE_Z11_ENCLOSURE_PASS_H4_PARENT_READY`

G1 changes only the continuous-in-step readout. It preserves the same H2 approximant, forcing, physics, endpoint propagation, science gate, and parent chain. The scalar continuous norm is replaced by a rigorous componentwise augmented-Metzler whole-interval bound:

```text
exp(A t) = exp(-alpha t) exp(K t),  K=A+alpha I >= 0
exp(A t) <= exp(K t) <= exp(K h),  0 <= t <= h
```

Validation:

```text
all outputs finite = true
endpoint replay = PASS
operator scalar fallback total = 0
new componentwise continuous bound <= old scalar bound = true
new physical bounds <= old scalar physical bounds = true
```

Endpoint replay is essentially exact:

```text
global endpoint replay max abs = 5.8140341499535175e-18
global endpoint replay max relative = 1.1736360450783432e-12
```

Tight global results:

```text
old scalar continuous weighted-inf upper = 1.1365337328877092e-04
tight componentwise continuous weighted-inf upper = 5.041273260960460e-06
tightening factor = 22.54457701567198

tight continuous physical state upper = 2.5801248476877237
worst state = mode 20, u

tight continuous physical derivative upper = 2.542065710968569e-02
worst derivative = mode 20, udot
```

For mode 20, the tight continuous weighted component vector is:

```text
[2.8712450121161085e-08,
 1.099134842407077e-06,
 5.815812280745985e-08,
 6.2771902537448294e-09,
 3.061196276055288e-08,
 5.041273260960460e-06,
 3.3316623818902575e-06,
 4.134944880936828e-09]
```

Hashes:

```text
JSON = 7bb4bcbbc3d3e45c5555b0437321785bc4f6150e40c68b2821a3f69ba3e4159e
NPZ  = 82f49da27b08a96dc6919c14549af408e1737e9ee652c81f847de840809be787
```

Claim boundary: D12R11G1 is now the preferred continuous physical Z11 parent for H4 error-budget work. It does not certify the full original H4 Ward identity or Z21.

## D12R11 closure decision

**D12R11 is CLOSED. Do not open G2 or another H2/Z11 campaign unless a parent SHA changes or a concrete contradiction is found.**

The preferred parent for the remaining H4 numerical budget is D12R11G1.

## Current real frontier

Return immediately to the actual pre-Z21 line:

```text
remaining non-Y D9 numerical budgets / high derivatives / roundoff
        -> full integrated physical H4 Ward
        -> final Z21 solve
        -> apply frozen H4 gate <= 1e-6
        -> only then lensing
```

The next work must be an H4/D9 task, not another D12R11 audit.

## Historical checkpoints relevant to Z21

- 2026-09-24: corrected H3/Z20 work underway; Z21 blocked by source/Ward prerequisites.
- 2026-09-25: Z20 and q20 certified; six-source H4 construction available; physical all-parent Ward still open.
- 2026-10-10: D12R2 background/F21 work closed. Project headline: full H4 Ward next, then final Z21 solve.
- 2026-10-10 to 2026-10-11: D9 prelock exposed missing rigorous numerical budgets. D12R8 removed the Y sector structurally. D12R9 showed that sampled/PCHIP representations were insufficient for the remaining non-Y parent proof.
- D12R10/D12R11 repaired that foundation.
- 2026-10-14: D12R11G1 closes the continuous physical Z11 parent with a tight componentwise whole-interval enclosure. The project returns to the non-Y D9/full-H4-Ward frontier.

## Stop condition for repeated work

Before starting any new audit, check this ledger. If the relevant contract is CLOSED and all parent SHAs are unchanged, do not repeat it. Move to the next OPEN H4/Z21 link.
