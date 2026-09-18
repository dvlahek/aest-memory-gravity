# NL1C7B4 Repair13a — local result freeze

## Status

Frozen local WSL result for the preregistered Repair13a roundoff-stable Hamiltonian source-localization certification.

Terminal classification:

`NL1C7B4_REPAIR13A_ROUNDOFF_STABLE_SOURCE_LOCALIZATION_PASS`

with local execution HEAD `98e7cc79cb975e543460862f9d83db7e1b5a2e3b`.

This is a local WSL science result, not an official GitHub Actions run.

## Frozen output

- result JSON bytes: `138364`
- result JSON SHA-256:
  `cad6cb2b49b3b20a0b6346390f8536fb90da8d5000ceed82ac0de86b912679b3`

The exact frozen parent Repair13 JSON remains:

`ef6791edd595a2bd8b44e52a703915385a1e2c4d98345ff4cc509a5d22a61a9b`.

## Gate result

All seven Repair13a gates pass:

- R13A_G1 exact historical provenance
- R13A_G2 historical Repair13 gate pattern
- R13A_G3 roundoff-aware source-sum closure
- R13A_G4 roundoff-aware coefficient closure
- R13A_G5 roundoff-aware projection identity
- R13A_G6 frozen localization payload unchanged
- R13A_G7 claim boundary

The historical Repair13 implementation failure is preserved and not relabeled.

## Roundoff certification

The preregistered binary64 model used

- `u=2^-53`;
- `gamma_64=7.105427357601052e-15`;
- `gamma_96=1.0658141036401616e-14`;
- projection bound `gamma_(32m+128) T/D`;
- no empirical tolerance fitted from Repair13 output.

Observed worst error/bound ratios:

- G3 source-sum closure: `0.009111833738363648`;
- G4 first-order coefficient closure: `0.006074555825575744`;
- G5 projection identity: `0.000361693342772238`.

All are far below unity.

## Certified frozen localization payload

Across all 54 frozen cases:

- `AeST_E2` is the largest first-order Hamiltonian coefficient by L2 norm in `54/54`;
- `AeST_E2` is `first_order_like` in `54/54`;
- `AeST_EX` is `first_order_like` in `54/54`;
- `AeST_X2` is `second_order_like` in `54/54`;
- `AeST_K`, GR curvature/kinetic terms, dust, and standard background contain first-order components as expected;
- the historical full Hamiltonian first-order residual from Repair12 is reproduced.

Representative frozen ordering is `AeST_E2` first and `AeST_EX` second.

## Interpretation boundary

Repair13a certifies source localization only.

It does not establish that the frozen E2 or EX action terms are physically wrong, and it does not license changing `K_B`, `C`, signs, the state, or the B4 threshold.

The historical B4 class remains

`NL1C7B4_REPAIR09_REPAIR08_RAW_CONSTRAINT_FAIL`.

No nonlinear evolution, finite eta, B4 PASS, or observational-detection claim is made.

## Licensed next step

A separately preregistered analytic Hamiltonian first-variation audit may derive the E2/EX lapse constraint on the B3 background and compare it with the C7A effective-density to scalar-Q bridge.

In particular it may test if the full first-order AeST density implied by the frozen spherical action is

`delta rho_A = Q K_QQ delta Q + a^-2 Laplacian[K_B E_A + (2-K_B) chi]`

and therefore if the current C7A relation

`delta Q = rho_A delta_A/(Q K_QQ)`

omits a finite-gradient E-sector contribution when `delta_A` is the CLASS effective-fluid density perturbation.

This identity must be established symbolically and then tested numerically without modifying the official Repair08 state.
