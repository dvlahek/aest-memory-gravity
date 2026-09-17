# NL1C7B2 Repair01 predata — stable Exp background-energy evaluation

Status: **PRE-RESULT / FROZEN BEFORE RE-EVALUATION**

Classification before evaluation:

`NL1C7B2_REPAIR01_PREDATA_STABLE_EXP_ENERGY`

## Historical parent

The historical NL1C7B2 run is immutable:

- run `35190742632`
- head `c13207ef37540e7c01171c4d638b4058ad1fadd3`
- workflow conclusion: `success`
- science classification: `NL1C7B2_HOMOGENEOUS_BACKGROUND_RECONCILIATION_FAIL`
- artifact `10483358073`
- artifact SHA256 `aa017449e0d4bc2afa4906925c4c53151c4c1eae1571916851aeacf87ef16281`
- result-freeze commit `22923058c883dd36c6b507fa7079efba5000b4e0`.

The historical science result is not reclassified in place.

## Repair scope

Repair01 changes only the numerical representation used to evaluate the already frozen Exp scalar energy in B2-G3.

The historical evaluator recovered

`Z=(Q-Q0)/Z0`

from a printed double `Q≈1e-4` whose physical offset `Z0*Z` is only about `5.5e-17`. This inverse subtraction is cancellation limited.

The frozen CLASS AeST source does not recover `Z` this way. It evolves `KQ=I0/a^3`, defines

`x = KQ/(4*K2*Z0)`,

and solves the monotone Exp relation

`x = Z*exp(Z^2)`.

Repair01 must reproduce the same frozen source algorithm: solve for `y=Z^2` from

`y + 0.5*log(y) = log(x)`

using the same Newton structure and stopping scale as `aest_exp_Z_from_x`, then evaluate

`Q = Q0 + Z0*Z`,
`K = 2*K2*Z0^2*(exp(Z^2)-1)`,
`KQ_formula = 4*K2*Z0*Z*exp(Z^2)`,
`rhoA_formula = Q*KQ_formula-K`.

No physical parameter, trace value, interpolation rule, threshold, source term, or background species may be changed.

## Frozen inputs and thresholds

Exactly retain the original B2 inputs and gates:

- dense trace run `35149865129`, artifact `10469031693`, digest `193325536405f9a21a238f5fbe71a772d2484a096dcbfec3d6007e825cc38f70`
- B1 run `35185338047`, artifact `10481781728`, digest `645d29e4e8ac7cfa4fff9833a4ef500d34fc667373bfac3073883155fac519a7`
- `a_i=0.02`
- PCHIP in `ln a` as primary interpolation
- linear-in-`ln a` control
- 128 exact k modes
- k-spread limit `1e-10`
- scalar-energy relative-error limit `1e-8`
- homogeneous Hamiltonian residual limit `1e-7`
- interpolation-control limit `2e-2`
- `omega_b`, H0, Q0, K2, Z0 unchanged
- eta=0.

## Locked Repair01 gates

### R1 — provenance

Historical B2 run/artifact/result freeze and all original B2 parent artifacts must match exactly.

### R2 — stable source-equivalent Exp inversion

The implementation must identify the frozen source relation `KQ/(4*K2*Z0)=Z*exp(Z^2)` and reproduce its monotone inversion without using `(Q-Q0)/Z0` for the primary energy evaluation.

### R3 — scalar-energy consistency

Using the stable inversion, `3*rhoA_trace` must agree with `Q*KQ-K` to the unchanged normalized relative-error limit `<=1e-8`.

### R4 — no science-gate changes

The B2-G2 symbolic identity, baryon normalization, B2-G5 Hamiltonian residual, B2-G6 k/interpolation controls, and all original numerical limits must remain unchanged.

### R5 — homogeneous closure classification

If R1-R4 pass and B2-G5 now passes, classify

`NL1C7B2_REPAIR01_HOMOGENEOUS_BACKGROUND_RECONCILIATION_PASS`.

If R1-R4 pass but B2-G5 still fails, classify

`NL1C7B2_REPAIR01_HOMOGENEOUS_BACKGROUND_SECTOR_INCOMPLETE`

and report the signed remainder only. No missing source may be fitted or added in Repair01.

Any inconsistency in R1-R4 is

`NL1C7B2_REPAIR01_STABLE_EXP_EVALUATION_FAIL`.

## Claim boundary

Repair01 performs no radial initial constraint, nonlinear time step, turnaround, collapse, finite eta, or observable calculation.