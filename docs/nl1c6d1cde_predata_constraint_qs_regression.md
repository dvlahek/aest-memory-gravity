# NL1C6D1CDE predata — scalar constraints and quasistatic regressions

Status: **PREREGISTERED BEFORE NL1C6D1CDE NUMERICAL RESULTS**.

Frozen label:

`NL1C6D1CDE_PREDATA_CONSTRAINT_QS_REGRESSION`

This is a sub-audit of the already preregistered `NL1C6D1_PREDATA_DYNAMICAL_FORMULATION_AUDIT`. It does not by itself classify the full D1 formulation audit and does not permit NL1C6D2 branch evolution unless the remaining nonlinear dynamical reduction is derived and audited.

## Authoritative equations

The linear scalar constraints are taken from Skordis & Zlosnik, Phys. Rev. D 106, 104041 (2022), Hamiltonian scalar sector, equivalently reproduced by Bataki, Skordis & Zlosnik, arXiv:2307.15126v3, Eqs. (114)–(115):

`C_Psi = -1/2 P_alpha + 2 k^2 (Phi - k^2 eta/6) ~= 0`

`C_zeta = -(k^2/6) P_Phi - P_eta ~= 0`.

The quasistatic weak-field target is Verwayen, Skordis & Boehm, MNRAS 531 (2024) 272–289, Eqs. (1)–(3):

`Phi = tildePhi + chi`

`lap tildePhi + mu^2 Phi = 4 pi G_N rho_b/(1+beta0)`

`lap tildePhi = div[j(x) grad chi]`.

Repository conventions remain unchanged, including physical-coordinate derivatives, `x = c^2 |grad_phys chi|/(a0 Mpc_in_metres)`, `mu^2 = 2 K2 Q0^2/(2-K_B)`, and the three frozen interpolation functions.

## C: scalar-constraint regression

Test all `beta0 in {1.0,0.5,0.1}` and all six repository low-k modes `{0.03,0.05,0.08,0.10,0.15,0.20} h/Mpc`.

Two analytic scalar-sector families are tested:

1. the propagating X mode already validated in D1B; in conformal Newtonian gauge its nondynamical canonical fields are reconstructed by the exact constraints;
2. the nonpropagating omega=0 Y mode `Y=A0 t+B0`, `P_Y=A0`, using the canonical relation `P_alpha=P_Y` and the exact constraint solution `Phi=P_alpha/(4k^2)` with `eta=P_eta=P_Phi=0`.

No empirical constraint projection is allowed. Algebraic reconstruction from the exact first-class constraints is allowed and is explicitly reported.

For every sampled state, define each normalized constraint residual as absolute constraint divided by the sum of the absolute magnitudes of its terms plus `1e-300`. Required gates:

- maximum normalized constraint residual at initialization `<=1e-10`;
- maximum normalized constraint residual over the sampled evolution `<=1e-7`.

The X mode is sampled over eight periods using the same velocity-Verlet convention as D1B. The Y mode is sampled over the same dimensionless time window after scaling time by the corresponding X-mode period. No nonlinear branch-selection source is used.

## D: independent quasistatic full-J operator identity

At `Nx=256`, compare an independent implementation of the published quasistatic equations against the frozen NL1C6R3 operator. The independent implementation must duplicate the continuum formulas and spectral discretization rather than call the repository residual helper.

Deterministic manufactured fields use Fourier modes `{3,5,8,10,15,20}`, fixed phases already present in the repository, and amplitudes chosen before results so that the sampled `x` values include nonlinear finite-gradient values. Test scale factors `a in {1/7, 0.5, 1.0}`, all three beta0 values and all three interpolation families.

The independent and frozen implementations must agree, using relative L2 differences with a `1e-300` denominator floor, for:

- nonlinear divergence operator;
- `tildePhi` reconstructed from its Poisson equation;
- total `Phi`;
- final full-J residual.

Required maximum discrepancy: `<=1e-12`.

For `sharp`, the physical residual and `j(x)` are compared on every grid point. The derivative/Jacobian coefficient `j+x dj/dx` is compared only away from the kink `x_t=(1+beta0)/beta0`; the preregistered exclusion neighbourhood is

`|x-x_t| <= 1e-10 * max(1,x_t)`.

The exclusion applies only to derivative/Jacobian comparison, never to the physical residual.

## E: large-gradient regression

Use the frozen NL1C5B baryon-source artifact and the same native evaluation snapshots `0.2 <= z <= 1.5` used by NL1C6R3. For each beta0, independently construct the saturated `j=1/beta0` Helmholtz solution and compare it with the existing frozen analytic solution and saturated residual.

Required maximum relative error across `chi`, `Phi`, and saturated field residual: `<=1e-10`.

The input artifact identity remains frozen to SHA-256

`0ab60cbc32210ad3fb75c881f91a9db11148280e9223ea644680ed8cdfbaa590`.

## Frozen sub-audit classifications

If C, D and E all pass:

`NL1C6D1CDE_CONSTRAINT_QS_REGRESSION_PASS`

otherwise:

`NL1C6D1CDE_CONSTRAINT_QS_REGRESSION_FAIL`

Even a PASS leaves `full_D1_classified=false` until the nonlinear time-dependent reduction required by D1-A is derived from AeST rather than postulated. No D2 or NL1C7 science run is permitted from this sub-audit alone.