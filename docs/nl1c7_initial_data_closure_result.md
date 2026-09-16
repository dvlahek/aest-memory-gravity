# NL1C7 eta=0 spherical evolution — initial-data closure result

Status: **CERTIFIED INCOMPLETE BEFORE TRAJECTORY**

Final classification:

`NL1C7_INITIAL_DATA_CLOSURE_INCOMPLETE`

## Certified provenance

- original technical-failure run: `35091142502` (SymPy generic `H.rank()` overflow; no science classification reached)
- Repair01 preregistration commit: `47af6894bfbe2a863165570bf23dea006f0ddc8d`
- Repair01 implementation blob: `0040ed81ac2e4adb197612a5b37e9bd4de6dea6a`
- certified Repair01 workflow run: `35091301474`
- certified head: `c4351a752eccc99a86cf458acb4c52a509f63f6e`
- artifact: `10444427175`
- artifact SHA256: `f1f5327bc6c19fb379723ad5f6b03816453d21bc7bfce33a564d217fee01b91a`

## Certified audit

All pre-evolution audit gates passed:

- the NL1C6 four-field principal block is full rank;
- the exact G11 determinant identity is reproduced with symbolic residual `0`;
- the homogeneous-background principal rank is `4` with determinant `-161728`;
- the frozen global kinetic lower bound is `2520.561445 > 0`;
- lapse/Hamiltonian and radial-shift/momentum supply two retained constraints;
- four second-order fields `(L,R,u,phi)` therefore require eight initial radial functions, leaving six free functions after the two constraints;
- the frozen matter overdensity plus matter growing-mode velocity do not uniquely select the remaining metric/scalar/aether growing-mode content;
- no nonlinear trajectory was executed before unique initial data were available.

## Interpretation boundary

This result is not a failure of the spherical self-gravity closure. It identifies a missing **initial-mode selection bridge** between the already certified eta=0 linear cosmological growing solution and the nonlinear spherical variables. Regular-center and asymptotic-background boundary conditions constrain radial behavior but do not remove the remaining propagating eta=0 mode freedom.

The next licensed step is a separately preregistered eta=0 linear growing-mode bridge. After that bridge is certified, NL1C7 must reuse the already frozen compensated Gaussian profile and the original evolution gates unchanged.
