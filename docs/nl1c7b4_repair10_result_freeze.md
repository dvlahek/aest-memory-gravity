# NL1C7B4 Repair10 — local result freeze

## Status

Frozen local WSL reproduction result for the preregistered Repair10 exact raw source-term localization on the frozen Repair09 failure and certified Repair08 state.

Terminal classification:

`NL1C7B4_REPAIR10_RAW_SOURCE_LOCALIZATION_DIAGNOSTIC_PASS`

with `SCIENCE_RC=0`.

## Execution provenance

- branch execution HEAD: `a04f0a84812da74c794d9c105da71e151ce1ebd0`;
- Repair10 preregistration commit: `c43c3147da0ac7d9990d6badd422095b2b737ff9`;
- Repair10 implementation commit: `29ec99242e456a1780176e0cb85ee35614f02486`;
- Repair10 implementation-lock commit: `490ab43db80a496c6d883ce09ea953a48c21080f`;
- Repair10 local-runner commit: `6f4902dbefa2b3aa2c66162a67eeeb9997620fdf`;
- Repair10 workflow/execution HEAD: `a04f0a84812da74c794d9c105da71e151ce1ebd0`;
- frozen Repair09 result-freeze commit: `04d85232092cdc747cf317f2937f1c33a1c0dddc`;
- Repair09 result JSON SHA-256: `be8b54823690ffefb62470c34ee3d7addeef45e2db81e40b10cce4b833376ffc`;
- exact Repair08 NPZ SHA-256: `4639f3b5c0afcddb2f98c8b9f6a9dbbf8661dac685b12d235c09075a106dafa7`.

## Frozen local output hashes

- result JSON:
  - bytes: `178090`
  - SHA-256: `f1fc1a86d2d488f5e88f0d32b0d3d1d5ce9dab22f52e51fa69801948aeb6de9d`
- evaluator log:
  - bytes: `178536`
  - SHA-256: `815029c7a111bfcb190b9e53e67db4636a38a5f8f13ea252449f7965f9bde38a`
- local runner log:
  - bytes: `180636`
  - SHA-256: `c3d5ec464ff30cb9201f5c821f4775cbbdd022c1c0dcad76611ed5ac187102ba`

## Gate result

All six preregistered Repair10 gates pass:

- R10_G1 exact frozen provenance: PASS
- R10_G2 exact Repair09 reproduction: PASS
- R10_G3 signed decomposition closure: PASS
- R10_G4 complete hotspot localization: PASS
- R10_G5 two-grid localization reporting: PASS
- R10_G6 claim boundary: PASS

Signed source bookkeeping closes exactly in the stored run:

- max Hamiltonian decomposition closure: `0.0`
- max momentum decomposition closure: `0.0`
- closure limit: `1e-12`

## Source localization

Across all 54 frozen cases:

- Hamiltonian dominant label: `GR_Nr_boundary` in `54/54`;
- Hamiltonian second label:
  - `GR_curv_NL` in `36/54`;
  - `GR_curv_Rr` in `18/54`;
- radial-momentum dominant label: `AeST_E2` in `54/54`;
- radial-momentum second label: `AeST_EX` in `54/54`.

Thus the Repair09 momentum failure is not localized to the Exp K(Q) term. At the max-epsilon_M hotspots the K contribution is many orders below the dominant E2 contribution.

Representative Simple, beta=1 momentum hotspots:

- scale 5 h^-1 Mpc:
  - Nr=256: r=`45.19569132414301` Mpc, epsilon_M=`0.9999939272091828`,
    AeST_E2=`-9.087177024783368e-13`,
    AeST_EX=`-9.232342448184978e-15`,
    AeST_K=`-3.959080748737482e-18`,
    dominant/opposing-rest diagnostic=`-98.40706289781214`;
  - Nr=512: r=`45.339757320253625` Mpc, epsilon_M=`0.9999934459904295`,
    dominant `AeST_E2`, second `AeST_EX`.

- scale 10 h^-1 Mpc:
  - Nr=256: r=`68.95837439147593` Mpc, epsilon_M=`0.9998968500568601`,
    dominant `AeST_E2`, second `AeST_EX`;
  - Nr=512: r=`69.05593807238628` Mpc, epsilon_M=`0.9999999999944811`,
    dominant `AeST_E2`, second `AeST_EX`.

- scale 20 h^-1 Mpc:
  - Nr=256: r=`232.03561112807444` Mpc, epsilon_M=`0.9984004027833683`,
    dominant `AeST_E2`, second `AeST_EX`;
  - Nr=512: r=`232.04655284929802` Mpc, epsilon_M=`0.9982810686119208`,
    dominant `AeST_E2`, second `AeST_EX`.

The dominant labels and hotspot radii are stable under Nr=256 -> 512.

## Interpretation

Repair10 localizes the exact frozen raw radial-momentum mismatch to the `AeST_E2` Euler-Lagrange contribution at the max-epsilon_M hotspots, with `AeST_EX` consistently second.

This is a diagnostic localization only. It does not prove that the coefficient or sign of E2 is wrong, and it does not license modifying E2, EX, K, the state, or any threshold.

The Hamiltonian residual remains a near-cancellation among the large GR curvature/boundary terms, with smaller AeST_K, GR_kin, dust, and background contributions. Repair10 does not change the historical B4 failure.

No observational-detection, B4-PASS, finite-eta, or nonlinear-evolution claim is made.

## Licensed next step

The next legal diagnostic is a separately preregistered analytic/covariant audit of the frozen AeST `E^2` and `E X` shift variations and their first-order momentum contribution on the homogeneous B3 background and Repair08 perturbation.

That audit may compare:

1. the symbolic variation of
   `N L R^2 K_B E^2`
   and
   `2 N L R^2 C E X`
   with respect to shift variables;
2. their exact spherical implementation in `build_nonK()`;
3. the corresponding linear Fourier/covariant momentum contribution implied by the C7A variables.

It may not fit, flip, remove, or rescale either term. Any later model or implementation correction requires a new preregistration supported by that audit.
