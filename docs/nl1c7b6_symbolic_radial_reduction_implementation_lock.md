# NL1C7B6 — symbolic radial-reduction implementation lock

## Status

Implementation locked before the first NL1C7B6 symbolic audit execution.

NL1C7B6 is a structural analytic-representation audit.

It does not solve the reduced radial equations and does not construct initial data.

## Parent frozen result

Parent B5 Repair01 terminal class:

`NL1C7B5_CONSERVATIVE_DIFFERENTIAL_CERTIFICATION_FAIL`.

Parent result-freeze commit:

`2a2739db609ffb58e899baa7308199fd8dbc528b`.

Parent result-freeze blob:

`05057f742b2fb5c2c9bb5cf316a047deecfd79bb`.

Parent result JSON SHA-256:

`bfeae8019b69f23e0fa659c6c3e0134353b85e0dcd67f0337c14d6f50b887c8d`.

No B5 solver-parameter continuation is reopened.

## Preregistration

Preregistration commit:

`571d5bacee7a18f8c853a95769e2963c045e3e69`.

Preregistration file:

`docs/nl1c7b6_predata_symbolic_radial_reduction_audit.md`.

Frozen preregistration blob:

`12ea9757ed08b9533f2877cdd186b7b07c25b7cd`.

## Implementation

Initial implementation commit:

`022073e40e7ef41fd5e073d2da235ffb76ed9e73`.

Final implementation commit:

`2082832d6c1c838ec2093bc82068eae1f9757857`.

Implementation file:

`nl1c7b/symbolic_radial_reduction_b6.py`.

Frozen implementation blob:

`4758345861dffe89baac2a1c90d5672a4ff2a7df`.

The only change after the initial implementation expands the machine-checked structural audit to the already frozen j/J, K, dust and background sectors required by the preregistration.

No scientific criterion changed.

## Frozen symbolic target

The audit reconstructs the existing B4/Repair01 action terms and applies the exact frozen Q identity

`p_t=[Q_target-sinh(u) phi_r/L]/cosh(u)`.

It must verify

`E=cosh(u)u_t+sinh(u)(L_t+u_r)/L`

and

`X=tanh(u)Q_target+phi_r/[cosh(u)L]`.

### Hamiltonian

Frozen target radial flux:

`F_H=4 R R_r/L + 2 K_B R^2 cosh(u) E + 2 C R^2 cosh(u) X`.

Frozen coefficient:

`A_H=[4 R R_r + 2 K_B R^2 cosh(u)sinh(u)(L_t+u_r) + 2 C R^2 phi_r]/L^2`.

The audit must establish that the exact H constraint is:

- affine in `L_r`;
- quadratic in algebraic `R_t`;
- independent of `R_{t,r}`;
- free of `L_{rr}`.

Thus

`L_r=-B_H/A_H`

is structurally unique away from coefficient zeros.

### Momentum

Frozen GR identities:

`S_M^GR=4(L R_r R_t + L_r R R_t + L_t R R_r)`

and

`F_M^GR=4 L R R_t`.

Their exact difference after radial differentiation must be

`M_GR=4 R L_t R_r - 4 L R R_{t,r}`.

All non-GR frozen momentum sectors must be independent of algebraic `R_t`.

The exact M constraint must therefore be:

- affine in `R_{t,r}`;
- independent of algebraic `R_t`;
- at most affine in `L_r`;
- free of second derivatives of solved fields.

Frozen solved derivative coefficient:

`-4 L R`.

Thus

`R_{t,r}=B_M/(4LR)`

away from the analytic center.

## Frozen parent audit

Exactly six lambda=1 parent states:

- scales 5,10,20 h^-1 Mpc;
- Nr=256,512.

For both

- `A_H`;
- `A_M=4LR`;

require on every noncenter node:

- finite;
- nonzero;
- constant sign;
- `min(abs(A))/max(abs(A)) >= 1e-8`.

Only the analytic center is excluded from coefficient division because `R(0)=0`.

No other radial point may be excluded.

The first-eight-node `A_H/r` and `A_M/r` values are descriptive center-structure outputs only.

## Boundary/gauge scope

This audit does not choose a numerical boundary policy.

It records only:

- two first-order solved functions;
- two integration constants;
- regular-center information;
- pre-existing asymptotic-background outer-boundary requirement.

Historical `Y4/Qmean` conditions remain correctly described as Repair18d1 projection-nullspace transversality functionals.

They are not silently reinterpreted as physical ODE boundary conditions.

A future radial solve requires a new preregistration specifying this relation explicitly.

## Frozen imported blobs

- base B4:
  `8559120dc273be3174eca130ca313ed6ff5acb25`;
- Repair01 source dictionary:
  `253a0ae2a19a597f06358704ea276c9005973af3`;
- Repair09 background helper:
  `0cd67cecfbd590cb8819ad37314dc5b49047bc93`;
- Repair16 parent reconstruction:
  `fbd7d24f748fc398638d4eea4b7707801161e52a`;
- Repair18a exact evaluator:
  `767199e8ab620f5d6dabd50d0efde9828f22048b`;
- Repair19c shared canonical constants:
  `f27ed8b39c1351e27d4f3b43b195ff4423e04c76`;
- Repair08 scalar identity helper:
  `94fb3f42a7c819b0525860f7344d5dbaff93da19`;
- C7A reconstruction:
  `ff383c1ddc2cb2a684e2b5dd11fde0ae811e4fac`.

## Terminal classifications

- `NL1C7B6_SYMBOLIC_REDUCTION_IMPLEMENTATION_FAIL`
- `NL1C7B6_SYMBOLIC_RADIAL_REDUCTION_FAIL`
- `NL1C7B6_RADIAL_REDUCTION_COEFFICIENT_DEGENERACY`
- `NL1C7B6_SYMBOLIC_RADIAL_REDUCTION_PASS`.

Only the final class licenses a separately preregistered numerical reduced-radial construction.

It does not certify initial data or license evolution by itself.
