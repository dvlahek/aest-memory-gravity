# NL1C7B4 Repair10 — exact raw source-term localization

## Status

Locked before implementation.

Repair10 is licensed only by the frozen Repair09 result at commit `04d85232092cdc747cf317f2937f1c33a1c0dddc`, classification `NL1C7B4_REPAIR09_REPAIR08_RAW_CONSTRAINT_FAIL`.

Repair10 does not repair the state, change the model, or relax a threshold. It answers one diagnostic question only:

**Which frozen Euler-Lagrange source terms dominate the exact raw Hamiltonian and especially radial-momentum residual on the already certified Repair08 state?**

The identity-preserving scalar representation is frozen and may not be changed.

## Frozen inputs

Primary state and trace provenance are inherited unchanged from Repair09:

- Repair08 NPZ SHA-256 `4639f3b5c0afcddb2f98c8b9f6a9dbbf8661dac685b12d235c09075a106dafa7`;
- Repair08 result JSON SHA-256 `054851decab71e79a05aca2bc9fb287bb1239c8fb425989f40920004c3d88453`;
- Repair09 result JSON SHA-256 `be8b54823690ffefb62470c34ee3d7addeef45e2db81e40b10cce4b833376ffc`;
- dense trace artifact `10469031693`, digest `sha256:193325536405f9a21a238f5fbe71a772d2484a096dcbfec3d6007e825cc38f70`;
- `a_i=0.02`;
- `eta=0`;
- scales `[5,10,20] h^-1 Mpc`;
- radial grids `Nr=256,512`;
- Y families `Simple, Exponential, Sharp`;
- beta values `1.0,0.5,0.1`;
- all 54 frozen cases retained.

The primary Nr=256 state is loaded directly from the certified Repair08 NPZ. Nr=512 is the same Repair08 continuous representation used by Repair09.

## Frozen exact source dictionary

Repair10 must use the same exact source construction as Repair09/Repair02.

The signed source labels are frozen as:

1. `GR_kin`
2. `GR_curv_NL`
3. `GR_curv_Rr`
4. `GR_Nr_boundary`
5. `AeST_E2`
6. `AeST_EX`
7. `AeST_X2`
8. `AeST_J`
9. `AeST_K`
10. `dust`
11. `standard_bg`

For each source `i`, define the exact signed Euler-Lagrange contribution already used by Repair09:

- Hamiltonian contribution `C_H_i`;
- radial-momentum contribution `C_M_i`.

Define

`N_H = sum_i C_H_i`

`D_H = sum_i |C_H_i|`

`N_M = sum_i C_M_i`

`D_M = sum_i |C_M_i|`

and retain the Repair09 epsilon definition with the same frozen denominator floor.

No contribution may be merged, rescaled, sign-flipped, omitted, or reinterpreted after execution.

## Diagnostic outputs

For every one of the 54 cases, Repair10 must report:

- Repair09-reproduced max epsilon_H and max epsilon_M;
- radial index and physical radius of the H hotspot;
- radial index and physical radius of the M hotspot;
- signed `C_H_i` for all 11 source labels at the H hotspot;
- signed `C_M_i` for all 11 source labels at the M hotspot;
- `N_H,D_H,epsilon_H` at the H hotspot;
- `N_M,D_M,epsilon_M` at the M hotspot;
- largest absolute source label and value at each hotspot;
- second-largest absolute source label and value at each hotspot;
- signed sum of all non-dominant terms;
- dominant-to-rest signed cancellation ratio when defined.

Repair10 must additionally report, for every scale/grid pair, the hotspot locations and dominant labels across all Y/beta cases without selecting a preferred branch.

## Gates

### R10_G1 — exact frozen provenance

Require the exact Repair08 and Repair09 hashes/classifications, frozen dense-trace coverage, 128 native k modes, and exact Repair09 result-freeze ancestry.

### R10_G2 — exact Repair09 reproduction

Recompute all 54 raw cases from the same state and source dictionary.

Require:

- the same number of cases;
- same scale/Nr/Y/beta keys;
- case-wise max epsilon_H and max epsilon_M agreeing with the frozen Repair09 JSON to relative/absolute numerical tolerance `1e-12`;
- Repair09 terminal classification remains the frozen raw-constraint FAIL.

This is a reproduction gate, not a new physics threshold.

### R10_G3 — signed decomposition closure

At every non-center radial point in every case, require

`|N_H - sum_i C_H_i|/(D_H+floor_H) <= 1e-12`

and

`|N_M - sum_i C_M_i|/(D_M+floor_M) <= 1e-12`.

Because `N_H` and `N_M` are defined by the same signed source arrays, this gate detects only bookkeeping/implementation errors.

### R10_G4 — complete hotspot localization

Require exactly 54 case-localization records, each with both H and M hotspot indices/radii and all 11 signed source values.

No physical dominance threshold is introduced. The largest and second-largest sources are descriptive outputs only.

### R10_G5 — two-grid localization reporting

Require complete paired reporting for all 27 matched Nr=256/512 cases. Hotspot movement and dominant-label agreement/disagreement are reported but are not converted into a new physics PASS/FAIL threshold.

### R10_G6 — claim boundary

Require:

- no state modification or projection;
- no coefficient fit;
- no source insertion;
- no sign change;
- no K clipping;
- no Q linearization;
- no radial-point removal;
- no Y/beta/scale selection;
- no threshold change;
- no nonlinear evolution;
- no finite eta;
- no observational-detection claim.

## Terminal classifications

Allowed classes are:

- `NL1C7B4_REPAIR10_RAW_SOURCE_LOCALIZATION_DIAGNOSTIC_PASS`;
- `NL1C7B4_REPAIR10_IMPLEMENTATION_FAIL`.

A diagnostic PASS means only that the frozen Repair09 raw-constraint failure has been exactly reproduced and decomposed term by term. It does not make B4 pass and does not license nonlinear evolution.

Any later coefficient/sign/source/state change requires a separate preregistration motivated by the Repair10 localization result.
