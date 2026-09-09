# NL1C6 predata — full-J baryonic quasistatic reclosure

Classification before implementation: **NL1C6_PREDATA_FULL_J_BARYONIC_RECLOSURE**

This gate is frozen after `NL1C5B_BARYON_SOURCE_FREEZE_PASS` and before inspecting any full-J baryonic reclosure result.

Historical classifications remain immutable.

## 1. Scientific question

Does the published full quasistatic AeST scalar system admit a numerically self-consistent periodic finite-amplitude field branch when it is sourced by the correctly frozen **baryonic** CLASS state, rather than by the total-matter diagnostic source used in NL1C5 or by the invalid saturated high-gradient closure?

This is a fixed-state, physical-coordinate, quasistatic/subhorizon **snapshot reclosure**. It is not a derivation of the full nonlinear FLRW equations, it does not re-evolve matter, and it does not yet evaluate the retarded memory bath.

## 2. Frozen input identity

Use only the retained NL1C5B artifact:

- GitHub Actions run `34345121613`;
- artifact ID `10101422385`;
- artifact SHA256 `0ab60cbc32210ad3fb75c881f91a9db11148280e9223ea644680ed8cdfbaa590`;
- file `nl1c5b_baryon_source_freeze.npz`;
- native `k_native_h`, `z_native`, and `d_b` arrays.

The NL1C5B result already proves that this state lies on exactly the same native k/z grid as v0.77 and that its fresh `d_m` reproduces the preserved v0.77 `d_m` with relative L2 `0.0`.

No observational data, likelihood, finite physical eta, or memory forcing is allowed in NL1C6.

## 3. Frozen reconstruction

Use the exact signal-band modes

\[
k_h=\{0.03,0.05,0.08,0.10,0.15,0.20\}\;h\,{\rm Mpc}^{-1}
\]

and deterministic phases

`[0.13, 0.71, 1.29, 2.03, 2.77, 3.41]` radians.

The log-trapezoid mode weights and primordial spectrum remain

\[
P_{\cal R}(k)=A_s(k/k_*)^{n_s-1},
\]

with

- `A_s = 2.1308864352626987e-9`,
- `n_s = 0.9666229454895277`,
- `k_* = 0.05 Mpc^-1`,
- `H0 = 67.3324639084866 km s^-1 Mpc^-1`.

At each native redshift reconstruct

\[
\delta_b(x)=\sum_i\sqrt{2\Delta_iP_{\cal R}(k_i)}\,
 d_b(k_i,z)\cos(k_ix+\varphi_i).
\]

The periodic box has fundamental mode `0.01 h/Mpc`, so the six requested modes are exact integer Fourier modes `3,5,8,10,15,20`.

The physical baryonic source is

\[
S_b(x,a)=\frac{4\pi G_N}{c^2}\,\delta\rho_b
=\frac32\left(\frac{100}{c_{\rm km/s}}\right)^2
\omega_b a^{-3}\delta_b(x),
\]

with the frozen `omega_b = 0.022377376877682164`.

No CDM, total-matter, or massive-neutrino transfer is inserted into the primary right-hand side.

## 4. Published full quasistatic AeST system

Use the weak-field quasistatic equations of Verwayen, Skordis & Boehm, MNRAS 531 (2024) 272-289, DOI `10.1093/mnras/stae1225`, equations (1)-(4):

\[
\Phi=\tilde\Phi+\chi,
\]

\[
\nabla_{\rm phys}^2\tilde\Phi+\mu^2\Phi
=\frac{S_b}{1+\beta_0},
\]

\[
\nabla_{\rm phys}^2\tilde\Phi
=\nabla_{\rm phys}\cdot\left[j(x)\nabla_{\rm phys}\chi\right],
\]

with

\[
x=\frac{c^2|\nabla_{\rm phys}\chi|}{a_0},
\qquad a_0=1.2\times10^{-10}\;{\rm m\,s^{-2}}.
\]

The homogeneous Fourier modes of `delta_b`, `tildePhi`, and `chi` are fixed to zero. This is the periodic density-contrast version of the published static system used only as the declared quasistatic snapshot reclosure.

The mass scale remains the already frozen

\[
\mu^2=\frac{2K_2Q_0^2}{2-K_B},
\]

with `K_B=0.0665`, `K_2=9500`, and `Q0=1e-4 Mpc^-1`.

## 5. Frozen full interpolation family

All nine NL1C1 combinations remain co-primary. No branch may be selected after seeing the outcome.

For `x=|grad chi|/a0`:

### Simple

\[
j_S(x)=\frac{x}{1+\beta_0+\beta_0x}.
\]

### Exponential

\[
j_E(x)=\frac1{\beta_0}\left[1-\exp\left(-\frac{\beta_0x}{1+\beta_0}\right)\right].
\]

### Sharp

\[
j_H(x)=\min\left(\frac{x}{1+\beta_0},\frac1{\beta_0}\right).
\]

Use every combination of

`kind in {simple, exponential, sharp}`

and

`beta0 in {1.0, 0.5, 0.1}`.

## 6. Numerical representation

Spatial derivatives are pseudospectral. The nonlinear flux `j(x) grad chi` is formed pointwise in real space and dealiased with the same 2/3 rule already validated in NL1A/NL1C1.

Primary resolution: `Nx=256` at all 24 native times.

Resolution control: `Nx=512` at all native times satisfying `0.2 <= z <= 1.5` (eight native times).

The nonlinear equations may be solved after eliminating `tildePhi` through the zero-mean inverse physical Laplacian of the full-J operator. The final reported residuals must nevertheless be evaluated in the original coupled equations above.

## 7. Frozen solver continuation

The final equation is fixed; continuation is only a numerical path to that equation.

For each interpolation/beta0 branch:

1. order native slices from largest z to smallest z;
2. at the first slice, start from the homogeneous field and use source-amplitude continuation with
   `lambda = {1/64, 1/32, 1/16, 1/8, 1/4, 1/2, 1}`;
3. at each later slice, initialize from the preceding converged physical-time solution;
4. if a direct step fails, use the same fixed seven-point source-amplitude continuation at that slice;
5. Newton updates use the analytic directional derivative of `div[j(x) grad chi]`, with a Krylov linear solve and deterministic backtracking line search;
6. maximum Newton iterations `40` per continuation step;
7. accepted equation residual relative L2 `<= 1e-8`.

No solver tolerance or continuation grid may be changed after an outcome is inspected.

## 8. Locked regression and numerical gates

### G1. Artifact and mode identity

- NL1C5B artifact SHA256 matches exactly;
- all six requested k modes match the native grid with relative error `<=1e-12`;
- exactly the frozen native z grid from NL1C5B is used;
- at least eight native times lie in `0.2<=z<=1.5`.

### G2. Published high-gradient regression

Before the physical full-J solve, replace `j(x)` numerically by the constant `1/beta0` and solve the same coupled implementation for deterministic source snapshots. It must reproduce

\[
\nabla^2\Phi+(1+\beta_0)\mu^2\Phi=S_b,
\qquad
\chi=\frac{\beta_0}{1+\beta_0}\Phi
\]

with relative L2 `<=1e-10` for every beta0. This locks signs, factors of `1+beta0`, the physical Laplacian, and the source normalization independently of the nonlinear result.

### G3. Coupled full-J residuals

For every kind, beta0, and native time:

\[
R_1=\nabla^2\tilde\Phi-\nabla\cdot[j(x)\nabla\chi],
\]

\[
R_2=\nabla^2\tilde\Phi+\mu^2(\tilde\Phi+\chi)-S_b/(1+\beta_0).
\]

Require normalized relative L2 `<=1e-8` for `R2`. `R1`, which is also checked independently after reconstruction, must be `<=1e-10` relative to the larger of the operator/source norms.

All fields and diagnostics must be finite.

### G4. Resolution control

At the eight evaluation times compare `Nx=256` and `Nx=512` for

- Fourier coefficients `m=1..32` of `chi`;
- Fourier coefficients `m=1..32` of `Phi`;
- `x_rms`.

Require each normalized discrepancy `<=5e-3` for all nine branches.

### G5. Deterministic branch check

At the eight evaluation times, independently re-solve from two fixed starts:

- the baryonic high-gradient Helmholtz field;
- the mass-dominated start `chi = S_b/[(1+beta0) mu^2]`, zero-mean.

If both converge to valid residuals, compare their low-mode `chi` solutions with the continuation branch. Agreement `<=1e-4` is the uniqueness/branch-consistency gate.

If distinct residual-valid roots are found, do **not** choose the more favorable root. Classify the outcome as

**NL1C6_FULL_J_MULTIBRANCH_REQUIRES_BOUNDARY_SELECTION**.

This is a scientific branch diagnosis, not a numerical failure.

## 9. Regime diagnostics — not gates

For each solution report

- `x_rms`, `x_min`, `x_median`, `x_max`;
- fractions of spatial points with `x<0.1`, `0.1<=x<=10`, and `x>10`;
- `min/max/mean j(x)`;
- ratios of `chi`, `tildePhi`, and total `Phi` gradient RMS;
- source and field RMS.

These quantities diagnose whether the actual fixed point lies in the deep-MOND, transition, or screened portion of the already frozen full interpolation. They are not used to select a branch or redefine a PASS.

## 10. Classification

If G1-G4 pass for all nine co-primary branches and G5 finds no distinct residual-valid root:

**NL1C6_FULL_J_BARYONIC_RECLOSURE_PASS**

If G1-G4 fail because the declared equations cannot be solved to the frozen numerical tolerances:

**NL1C6_FULL_J_BARYONIC_RECLOSURE_FAIL**

If G1-G4 pass but G5 identifies distinct residual-valid roots:

**NL1C6_FULL_J_MULTIBRANCH_REQUIRES_BOUNDARY_SELECTION**

A PASS establishes only a self-consistent full-J quasistatic field branch for the fixed baryonic snapshots under the declared periodic physical-coordinate reclosure. It does not establish nonlinear matter growth, halo formation, finite-eta dynamics, observational agreement, or a unique full-FLRW nonlinear solution.

## 11. Continuation rule

Only after NL1C6 yields a single numerically controlled full-J branch may the NL0B/NL1C3B eta=0 retarded bath be evolved on the **full native-time reclosed chi trajectory**.

That next test must preserve all nine co-primary interpolation/beta0 combinations and must not evaluate a finite physical eta before the eta=0 memory tangent/source is certified on the reclosed baseline.
