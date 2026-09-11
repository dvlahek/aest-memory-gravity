# Full-J cosmological reclosure PoC — predata

Classification before implementation: **FULLJ_COSMO_RECLOSURE_POC_PREDATA**.

This diagnostic is frozen after the nonredundant F-state high-k result `SLOWING_BUT_NOT_CONVERGED` and before inspecting any full-J cosmological reclosure output.

## 1. Scientific question

Does the already published nonlinear quasistatic AeST scalar operator suppress the response per unit baryonic source over the physical wavenumber range where the linear CLASS lensing prediction became strongly k-cutoff dependent?

This is a fixed-state, physical-coordinate, periodic quasistatic **snapshot reclosure proof of concept**. It is not a full nonlinear FLRW evolution, does not re-evolve matter, does not include finite eta or the retarded memory bath, and does not evaluate ACT or any other observational likelihood.

## 2. Source state

Generate a fresh baryonic transfer state with the same pinned CLASS commit and the same eta=0 nonredundant F-state implementation used by the high-k diagnostic:

- CLASS SHA `e85808324f51fc694d12e3ed7439552a3c3f9540`;
- AeST model `Exp`;
- `K_B=0.0665`;
- `eta=0`;
- memory disabled for the source extraction;
- current frozen ACT-start cosmology used by the F-state diagnostic.

Use baryon transfer `d_b(k,z)` only. No CDM, total matter, neutrino, lensing likelihood, or fitted amplitude is inserted into the nonlinear right-hand side.

Frozen snapshots:

`z = {1.0, 0.5}`.

Frozen physical mode grid:

`k = {0.04, 0.10, 0.20, 0.40, 0.80, 1.20} Mpc^-1`.

The native CLASS transfer grid must cover every requested k without extrapolation. `d_b` is interpolated linearly in `ln k` on the native transfer grid.

## 3. Periodic reconstruction

Use box fundamental `k_f = 0.02 Mpc^-1`, giving exact Fourier mode numbers

`m = {2,5,10,20,40,60}`.

Use `Nx=256`; all source modes lie below the 2/3 de-alias cutoff. Deterministic phases remain

`[0.13, 0.71, 1.29, 2.03, 2.77, 3.41]`.

Use the same primordial normalization as NL1C6,

`A_s=2.1308864352626987e-9`, `n_s=0.9666229454895277`, `k_*=0.05 Mpc^-1`,

and one frozen log-trapezoid weight vector computed on the complete six-mode grid. Weights are not recomputed by branch or redshift.

At each snapshot reconstruct

\[
\delta_b(x)=\sum_i \sqrt{2\Delta_i P_R(k_i)}\,d_b(k_i,z)\cos(k_ix+\varphi_i),
\]

and

\[
S_b(x,a)=\frac32\left(\frac{100}{c_{\rm km/s}}\right)^2\omega_b a^{-3}\delta_b(x),
\]

with `omega_b=0.022377376877682164`.

## 4. Frozen physical equation

Use exactly the NL1C6 published quasistatic system:

\[
\Phi=\tilde\Phi+\chi,
\]

\[
\nabla_{\rm phys}^2\tilde\Phi+\mu^2\Phi=\frac{S_b}{1+\beta_0},
\]

\[
\nabla_{\rm phys}^2\tilde\Phi=\nabla_{\rm phys}\cdot[j(x)\nabla_{\rm phys}\chi],
\]

\[
x=\frac{c^2|\nabla_{\rm phys}\chi|}{a_0},\qquad a_0=1.2\times10^{-10}{\rm m\,s^{-2}},\]

with

\[
\mu^2=\frac{2K_2Q_0^2}{2-K_B},
\]

`K_2=9500`, `Q0=1e-4 Mpc^-1`, `K_B=0.0665`.

All nine previously frozen NL1C6 constitutive branches remain co-primary:

- `kind in {simple, exponential, sharp}`;
- `beta0 in {1.0, 0.5, 0.1}`.

No branch may be selected after the result is seen.

## 5. Constitutive continuation

NL1C6R showed that source-amplitude continuation can encounter a near-singular/fold region before physical source amplitude. Therefore this PoC does not vary the physical source amplitude.

At full physical `S_b`, start from the analytic saturated solution with `j=1/beta0` and continue the constitutive law

\[
j_\lambda(x)=(1-\lambda)\frac1{\beta_0}+\lambda j(x),\qquad 0\le\lambda\le1.
\]

The corresponding exact directional coefficient is

\[
A_{{\rm eff},\lambda}=(1-\lambda)\frac1{\beta_0}+\lambda\left(j+x\frac{dj}{dx}\right).
\]

Only the path changes; the final `lambda=1` equation is exactly the published full-J equation.

Continuation is deterministic:

- initial step `Delta lambda = 1/16`;
- maximum step `1/16`;
- on a failed Newton step halve `Delta lambda`;
- minimum step `1/4096`;
- Newton maximum 80 iterations;
- GMRES and deterministic dyadic backtracking as in NL1C6R.

If the minimum continuation step fails, that branch/snapshot is classified as solver-inconclusive. No favorable alternate root is selected.

## 6. Numerical controls

For every branch and snapshot:

1. the `lambda=0` numerical residual must reproduce the analytic saturated high-gradient solution with relative L2 `<=1e-10`;
2. the final `lambda=1` solution must satisfy `R2 <=1e-8` and independently reconstructed `R1 <=1e-10`;
3. all fields and regime diagnostics must be finite.

This PoC intentionally has no publication-level resolution gate. A positive result licenses only a larger controlled nonlinear calculation, not an observational claim.

## 7. High-k response diagnostic

For each requested source mode extract the Fourier coefficients of the physical `lambda=1` solution and define

\[
T_\Phi(k,z)=\frac{|\Phi_k|}{|({S_b}/(1+\beta_0))_k|},
\]

and the Poisson-normalized response

\[
G_\Phi(k,z)=k_{\rm phys}^2 T_\Phi(k,z),\qquad k_{\rm phys}=k/a.
\]

Also report `|Phi_full/Phi_saturated|`, `x_rms`, the fractions in `x<0.1`, `0.1<=x<=10`, `x>10`, and the full-J residuals.

The frozen high-k modes are `k={0.40,0.80,1.20} Mpc^-1`. Fit the log-slope of `T_Phi` over these three points and record if

`T_Phi(0.40) > T_Phi(0.80) > T_Phi(1.20)`.

## 8. Descriptive classification

If any co-primary branch/snapshot cannot reach a residual-valid `lambda=1` solution:

**FULLJ_COSMO_RECLOSURE_POC_INCONCLUSIVE_SOLVER**.

If all 18 branch/snapshot solutions are valid, and every case has monotonically decreasing `T_Phi` over `{0.40,0.80,1.20}` with fitted high-k slope `<= -1`, classify:

**FULLJ_COSMO_RECLOSURE_POC_UV_SUPPRESSION_ROBUST**.

If all solutions are valid but that condition is not universal:

**FULLJ_COSMO_RECLOSURE_POC_UV_SUPPRESSION_NOT_ROBUST**.

These labels describe only the frozen-source quasistatic response. They do not establish nonlinear matter growth, a unique nonlinear FLRW solution, a converged CMB lensing spectrum, or agreement with ACT DR6.
