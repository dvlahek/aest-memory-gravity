# GE19 H4F3d8 — independent RESTRICTED nonbath Euler and lower-boundary compiler freeze

## Result and exact scientific limit

**Classification:** `GE19_H4F3D8_RESTRICTED_NONBATH_EULER_BOUNDARY_COMPILER_PASS_ACTUAL_OPEN`.

The independent analytic compiler derives the signed mixed nonbath
Euler parent coefficient and the complete lower L/shift action-boundary
coefficient, with original frozen GE06/GE07/Lambda/NL0C source bindings.
Its separate exact-action controls rederive GE07 dust currents and
first-order FLRW dust Euler terms, Lambda metric Euler terms, and
the NL0C Y zero-set flux derivative. This is **not** actual-grid
evaluation of all GE06/Y/background/first-order parent Euler arrays,
a complete physical action-boundary audit or the full H4 Noether test.

The frozen H4F3d4 FORMAL signed result and H4F3d6 actual physical
bath-parent SUBSET remain separately classified. No artificial
source-only Ward smallness requirement has been added.

## Frozen new files and successful CI

- Preregistration:
  `ge19/h4f3d8_predata_independent_nonbath_euler_and_boundary.json`,
  Git blob `007bec20e450dd67263d32a33476dcb8a5c33996`;
  initial commit `11692e49f31d07db558a94a9194b28620288ad5d`.
- Compiler:
  `ge19/h4f3d8_independent_nonbath_euler_and_boundary.py`,
  exact final Git blob `861cd5a81c17380a727777a4e1ff08cd7e857522`.
- Dedicated workflow:
  `.github/workflows/ge19-h4f3d8-independent-nonbath-euler-boundary.yml`,
  exact final Git blob `3e477da1801e78695acad291bddcbf9020bbcc2c`.
- Atomic final repair commit `8b4691a59996531300c207a4af750037ae9a6c39`.
- [GitHub Actions 36151870934](https://github.com/dvlahek/aest-memory-gravity/actions/runs/36151870934):
  job `108126857772`, **success**, terminal marker
  `GE19_H4F3D8_INDEPENDENT_RESTRICTED_COMPILER_PASS_ACTUAL_OPEN`.
- The 9,926-byte successful CI JSON
  `results/ge19_h4f3d8_independent_nonbath_euler_boundary_compiler.json`
  has SHA-256
  `d9f30c9632d06dd8412ef36e1a2f4ee43d7cbe7922c6d780d3376b5d0f6220fd`.
  Artifact ID `10871858033` contains JSON and full log.

**Implementation history:** Initial CI
[36151698788](https://github.com/dvlahek/aest-memory-gravity/actions/runs/36151698788)
failed with a Python `NameError` in a static GE06 text-binding generator.
That implementation error was corrected without changing the preregistered
physics, original action files or tested identities, and the compiler
and its hash-pinned workflow were committed atomically. Only subsequent
run `36151870934` is classified as the restricted compiler PASS.

## Independently derived coefficients

For each `i=N,L,R,b,u,phi,T,rho`, the independent
`d_eta d_epsilon^2` check of `E_i partial_chi F_i` gives

`E_i00 F_i21,chi + 2 E_i10 F_i11,chi + 2 E_i11 F_i10,chi`.

All eight fields retain the homogeneous-background `E_i00` term
and both distinct first-order cross terms with their original 2.
The direct `E_i20 F_i20,chi` product is not a mixed-order parent term.
This does not delete the corrected H3F/H3G second-order contributions
from the ACTUAL six-piece H4 source.

Independent expansion of the original action product
`L E_L - b E_b`, with `L00=a,b00=0`, gives

`B21=a E_L21+B_lower`, where

`B_lower=L21 E_L00+2L10 E_L11+2L11 E_L10
 -b21 E_b00-2b10 E_b11-2b11 E_b10`.

The nonbath parent contributes
`W_nonbath=Sum_i mixed(E_i F_i,chi)-partial_chi B_lower`.
The compiler checks the full product derivative, both cross factors,
the negative shift sign, and independently wrong-sign/omitted-term
negative controls. Spatial `chi` is NOT temporal `xi=ln(a)`.

From the original frozen GE07 action, independent symbolic gates
confirm

`J_T^t=2 L R^2 rho W`,
`J_T^chi=-2 L R^2 rho b W-2 N R^2 rho T_chi/L`,
`E_rho10=2 a^3(delta T_t-delta N)`, without a spurious
`rho0` multiplier, and the original signed `E_L10,E_b10`
and first-order dust currents.

From `L_Lambda=-6rho_lambda NLR^2`, the independent
metric Euler derivatives and first-order FLRW coefficients pass.
No Lambda shift or fictitious derivative current appears.
The frozen GE06 jet-partial Euler dictionary is source-bound
WITHOUT importing the original module-level generator. The Y
flux `g |g|` has zero first directional derivative at
`g=0` from either side; its mixed `2|g10|g11` flux
remains in the corrected physical H4 source. No unsupported
globally smooth FD8 error claim is made at a Y zero set.

## Work still required before any full physical H4 Ward

1. Independently evaluate GE06 Einstein/aether/scalar, GE07,
   Lambda, NL0C/Y and all lower-parent Euler and original
   action-boundary arrays on the exact SHA-verified
   H4F3b/H3F/H3G/Z11/Repair13/Repair26 physical grids.
2. Run the original physical H4F3d7 in the user-local
   environment and freeze BOTH one-sided 2048-node
   interval-ODE and FD4 discrepancies. The earlier local
   H4F3d6 near-unit Euler ratio remains an OPEN diagnostic.
3. Separately preregister and justify the actual FD4/FD8
   structural numerical error budget, including endpoint
   weights, original stepwise R1 regularity and NL0C Y
   zero-set smoothness, BEFORE calculating the combined
   operator + six source + all parent physical Ward residual.

**Full actual H4 Noether NOT CERTIFIED; Z21 NOT CERTIFIED;
lensing blocked. Original Repair37 SCIENCE_FAIL unchanged.
Active shift <=1e-6 and temporal order >=2.5 unchanged.**
