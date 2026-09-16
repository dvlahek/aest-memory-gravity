# Stable AeST R12a Repair03 — post-data freeze

Date: 2026-09-16
Branch: `fullj-evolving-weyl-bridge`
Pre-run HEAD: `395f474ba13bb6297384274e799a109b89d7c50e`

## Classification

`STABLE_AEST_R12A_REPAIR03_DIRECT_TRANSFER_CERTIFIED`

Repair03 passes the preregistered direct-transfer certification. The result removes perturbation-history time interpolation from the observable construction and evaluates CLASS transfer functions directly at the six frozen redshifts. The signed fractional response is formed on the common native transfer k grid before interpolation to the six frozen target k values.

All preregistered gates G1-G9 pass. `science_evaluated=true` and the transfer-level linear E_G response is certified on the frozen 6 x 6 k-z grid.

Repair02 remains a historical interpolation-control FAIL and is not reclassified.

## Artifact hashes

- JSON SHA256: `0bbc97d55afa2560f48cc226dd0f7043ffdcc023eac84cd796b4631fc27f6c4e`
- NPZ SHA256: `dc750d4f6649c71f2c53a339c96761bccbbfca684ff8eeb047a23555cdb9fa19`
- science log SHA256: `bdaf1e7b2ed7ef2bb54c3091c142257b3ebc9ca430930afd090630a39c6a9633`
- full runner log SHA256: `d611d8f12962bb58f3884a92f781ef1b4c8dd3ec62e4804562ab1754becdce67`
- environment SHA256: `b736aa07bb64eb45749352a056361295dd8c65a11d496f9d3382a1bf2ef584cd`

Runner exit: `0`.

## Frozen provenance

- Repair03 preregistration: `de7511bed7fc984bf0ba40d1afc70a63de88ebb2`
- Repair03 implementation: `6ab94ed0365a12deae546f71088aee267300f39b`
- Repair03 locked runner / pre-run HEAD: `395f474ba13bb6297384274e799a109b89d7c50e`
- Repair02 post-data freeze: `472ab501cfe564510b38e1c2831c4024ae012ecf`
- R8a2 parent: `590dbc69e2823f583b157af2297e357991103c47`
- R10a parent: `b7da648f1810ea0c047b6e511e3f87211e830329`
- R11a Repair02 parent: `84c4ba550ce3b262c78c69054056ab2778014677`

The runner passed lock, import, anti-stale-code, parent, frozen source, and direct-transfer API checks before evaluating the science response.

## Gate status

PASS:

- R12A-R03-G1 provenance/source
- R12A-R03-G2 direct-transfer interface and exact-redshift coverage
- R12A-R03-G3 native k-grid eta closure
- R12A-R03-G4 pure-GR convention
- R12A-R03-G5 eta-zero closure and tau invariance
- R12A-R03-G6 PCHIP-logk / linear-logk response control
- R12A-R03-G7 epsilon consistency
- R12A-R03-G8 differential decomposition
- R12A-R03-G9 local eta=0.05 linearity

Native transfer k grids close exactly across eta cases in the recorded result:

`native_k_max_relative_difference = 0.0`.

## GR and eta-zero controls

Pure GR passes under both independent k interpolation operators. The GR comparison gives

- linear-logk: `E=0.00412784857706632`, `C=0.9999999498771784`
- PCHIP-logk: `E=0.004127845813943467`, `C=0.9999999498743524`

and E_G is positive over the frozen grid.

AeST eta=0 closes onto the GR reference at `E ~= 1.953e-6` for every tau and both k operators. Eta-zero tau dependence is negligible: the maximum recorded pointwise relative variation is about `6.04e-10`, far below the frozen `5e-6` gate.

## Removal of the Repair02 interpolation ambiguity

Repair02 failed because the very small eta derivative was formed only after separately interpolating perturbation histories in time. Cubic time interpolation was internally stable, but the preregistered PCHIP time-interpolation control was not.

Repair03 removes that operation entirely. No perturbation-history time interpolation is used. CLASS transfer functions are requested directly at every frozen redshift, the response is formed first on the native k grid, and only the already-formed response is interpolated in ln k.

The two independent k interpolation operators now agree well. For primary epsilon=0.025, PCHIP-logk versus linear-logk gives

- tau10: `E=0.00010871452367470641`, `C=0.9999999941847411`
- tau5: `E=0.002292435253529841`, `C=0.9999979875549722`
- tau2.5: `E=0.004367024772986486`, `C=0.9999905045899945`
- tau1.25: `E=0.004784830414672814`, `C=0.9999885728628155`

All are comfortably inside the preregistered `E<=0.05`, `C>=0.995` gate.

This resolves the Repair02 numerical ambiguity without selecting the earlier cubic branch post-data.

## Epsilon consistency

Primary epsilon 0.025 and control epsilon 0.05 agree for all tau and both k operators.

For the primary PCHIP-logk operator:

- tau10: `E=0.0008199479596366036`, `C=0.9999996754103191`
- tau5: `E=0.0062265267667252`, `C=0.9999863195149004`
- tau2.5: `E=0.018403593478131586`, `C=0.9998308046405943`
- tau1.25: `E=0.038446514568579934`, `C=0.9992685682814354`

The worst case remains below the frozen `E<=0.05` threshold.

## Differential identity and local linearity

The differential identity

`T_EG = T_W - T_fdelta`

passes for every tau and both k interpolation operators. Linear-logk decomposition errors are of order `2.6e-8` to `3.5e-8`. The largest PCHIP-logk decomposition error is `E=0.0006376201843399218` at tau1.25, still far inside the frozen `E<=0.02` gate.

The direct eta=+0.05 physical response also agrees with `0.05*T_EG(eps=0.025)` for every tau. The worst case is tau1.25 with `E=0.047513079296261536`, `C=0.9988823809925295`, inside the preregistered `E<=0.10`, `C>=0.99` gate.

## Certified transfer-level amplitude

For the primary PCHIP-logk response, the 36-point E_G tangent norms are

- tau10: `3.362817241233927e-7`
- tau5: `3.324910996908658e-7`
- tau2.5: `3.2705815300334884e-7`
- tau1.25: `3.15605205963543e-7`

For the physical edge eta=+0.05, the direct 36-point L2 fractional shifts are

- tau10: `1.6798673181694558e-8`
- tau5: `1.6542205338379974e-8`
- tau2.5: `1.5958648866166046e-8`
- tau1.25: `1.5874965369857036e-8`

The maximum absolute pointwise fractional shifts are

- tau10: `1.5248645077500122e-8`
- tau5: `1.5001645276681304e-8`
- tau2.5: `1.4380882427719855e-8`
- tau1.25: `1.4369911813567571e-8`

For all four tau values, the maximum occurs at the high-k / low-z edge of the frozen domain:

`k = 0.20 h/Mpc`, `z = 0.29536404346937617`.

The 36-point RMS physical eta=0.05 fractional shift is approximately `2.65e-9` to `2.80e-9`.

## Tau coherence

The response direction is highly coherent across the frozen memory timescales. Relative to tau10:

- tau5: cosine `0.9999630356378019`, norm ratio `0.9887278309803836`
- tau2.5: cosine `0.9996493312331726`, norm ratio `0.9725718929742985`
- tau1.25: cosine `0.9994084980436596`, norm ratio `0.938514297160369`

Changing tau over the frozen range therefore changes the amplitude modestly and does not generate a qualitatively different transfer-level direction.

## Component scale

The reported

`A_ratio = ||T_EG|| / max(||T_W||, ||T_fdelta||)`

lies between about `0.906` and `0.917` across the four tau values. Thus the small certified E_G response is not explained by an extreme cancellation that suppresses E_G by many orders of magnitude relative to both component fractional responses. The linear memory response itself is small on this frozen domain.

## Scientific interpretation and claim boundary

Repair03 certifies a nonzero, numerically robust, transfer-level linear response of Weyl-to-growth consistency to the AeST memory parameter on the preregistered domain

- `k = [0.03, 0.05, 0.08, 0.10, 0.15, 0.20] h/Mpc`
- `z = [0.29536404346937617, 0.5096288678782911, 0.7057956472488681, 0.9185851971138159, 1.3170658832980264, 1.4905017757527006]`
- `tau H0 = [10, 5, 2.5, 1.25]`
- physical edge `eta=0.05`.

The certified physical fractional E_G effect is of order `1e-8` over this grid.

This PASS licenses only the transfer-level linear E_G response. It does not license

- an observational E_G detection,
- a galaxy-bias cancellation claim,
- a cross-correlation likelihood result,
- an eta bound,
- a tau bound,
- or a nonlinear-structure claim.

The JSON correctly records all of these claim-scope fields as false except `transfer_level_EG_response=true`.

The high-k / low-z location of the largest response is a motivation for a separately preregistered nonlinear-structure study. It is not itself evidence of nonlinear amplification.

## Final status

Repair03 is frozen as a successful direct-transfer certification:

`STABLE_AEST_R12A_REPAIR03_DIRECT_TRANSFER_CERTIFIED`

Repair02 remains frozen separately as

`STABLE_AEST_R12A_INTERPOLATION_CONTROL_FAIL`.
