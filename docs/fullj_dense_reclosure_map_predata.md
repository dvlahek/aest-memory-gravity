# Dense full-J cosmological reclosure map — predata

Classification before implementation: **FULLJ_DENSE_RECLOSURE_MAP_PREDATA**

This stage follows the completed PoC classification

`FULLJ_COSMO_RECLOSURE_POC_UV_SUPPRESSION_ROBUST`

with 18/18 valid snapshot branches, 18/18 monotone high-k responses, and high-k slopes between approximately -2.12 and -2.01. The purpose here is to map that nonlinear response on a denser `(k,z)` grid. It is not an ACT likelihood test.

## 1. Scientific question

Does the full published quasistatic AeST `J(x)` closure retain the PoC's finite, approximately Poisson-like UV response over a broader lensing-relevant scale/redshift domain, and can that response be tabulated as a controlled effective nonlinear map for a later lensing projection?

The primary quantity is

\[
T_\Phi(k,z)=\frac{|\Phi_k|}{|[S_b/(1+\beta_0)]_k|},
\qquad
G_\Phi(k,z)=k_{\rm phys}^2 T_\Phi(k,z),
\]

with `k_phys=k/a`.

This remains a fixed-state, periodic, physical-coordinate, baryonic quasistatic reclosure. It does **not** re-evolve matter, construct a full nonlinear FLRW solution, include the retarded memory bath, include finite physical eta, or evaluate an observational likelihood.

## 2. Frozen upstream model

Use the same nonredundant F-state CLASS source extractor as the successful PoC:

- CLASS upstream SHA `e85808324f51fc694d12e3ed7439552a3c3f9540`;
- AeST model `Exp`;
- `K_B=0.0665`, `Q0=1e-4 Mpc^-1`, `K2=9500`, `Z0=1e-17`;
- `eta=0`;
- memory disabled;
- Newtonian gauge;
- the same cosmological parameters used in the PoC.

Only the CLASS baryon transfer `d_b(k,z)` is used to construct the nonlinear right-hand side.

## 3. Frozen dense grid

Redshifts:

`z = {0, 0.25, 0.5, 0.75, 1, 1.5, 2, 3, 4, 6}`.

Comoving source modes in `1/Mpc`:

`k = {0.025, 0.05, 0.075, 0.10, 0.15, 0.20, 0.30, 0.40, 0.60, 0.80, 1.00, 1.20, 1.50}`.

Use a periodic fundamental

`k_fund = 0.0125 1/Mpc`,

so the requested modes are exact integer Fourier modes

`{2,4,6,8,12,16,24,32,48,64,80,96,120}`.

Primary spatial resolution is `Nx=384`; the 2/3 de-alias cutoff is mode 128, above the maximum sourced mode 120.

Deterministic phases are frozen to

`[0.13, 0.71, 1.29, 1.87, 2.45, 3.03, 3.61, 4.19, 4.77, 5.35, 5.93, 0.22681469282041355, 0.8068146928204127]` radians.

The primordial weighting remains the same log-trapezoid construction with the PoC values of `A_s`, `n_s`, and `k_*`.

No transfer extrapolation outside the native CLASS grid is allowed.

## 4. Co-primary nonlinear branches

Retain all nine PoC branches without post-result selection:

- `kind in {simple, exponential, sharp}`;
- `beta0 in {1.0, 0.5, 0.1}`.

Thus the primary map contains 10 redshifts x 9 branches = 90 independently reclosed nonlinear snapshots, each containing all 13 deterministic source modes simultaneously.

## 5. Physical equations

Use the same already-audited NL1C6 full-J quasistatic equations and source normalization as the successful PoC. No physical equation, interpolation family, mass scale, source normalization, or final residual gate may be changed in this stage.

The PoC constitutive continuation is also frozen:

\[
j_\lambda(x)=(1-\lambda)/\beta_0+\lambda j(x),
\]

at the **full physical source amplitude**, from the analytic saturated solution at `lambda=0` to the physical full-J equation at `lambda=1`.

Numerical continuation settings remain:

- maximum lambda step `1/16`;
- minimum lambda step `1/4096`;
- Newton maximum 80 iterations;
- Newton residual tolerance `2e-10`.

This continuation parameter is only a numerical path. Reported physics is always evaluated at `lambda=1`.

## 6. Frozen numerical gates

For every one of the 90 final full-J snapshots:

- all fields and diagnostics finite;
- `R2_relative_L2 <= 1e-8`;
- `R1_relative_L2 <= 1e-10`;
- the constitutive continuation reaches `lambda=1`.

The saturated analytic control at `lambda=0` must retain both residual and field regression errors `<=1e-10`.

## 7. Dense-map UV persistence gate

For each residual-valid `(z,kind,beta0)` snapshot fit the log slope of `T_phi` over the frozen high-k subset

`k >= 0.40 1/Mpc`, i.e. `{0.40,0.60,0.80,1.00,1.20,1.50}`.

The PoC-like UV response is considered persistent when, for every one of the 90 snapshots,

- the fitted slope satisfies `slope <= -1.0`;
- `T_phi(0.40) > T_phi(0.60) > ... > T_phi(1.50)`.

This is intentionally looser than the observed PoC slope near -2; it tests robust suppression rather than fitting the answer.

## 8. Outputs

Write:

- full per-branch JSON record;
- NPZ arrays for `T_phi`, `G_phi`, `RHG`, `x_rms`, residuals and slopes;
- long-form CSV with one row per `(z,kind,beta0,k)`;
- aggregate kernel CSV with median/min/max `T_phi` and `G_phi` across the nine co-primary branches at each `(z,k)`;
- a bundle ZIP containing code, predata and all outputs.

The aggregate CSV is an **effective nonlinear response map**, not yet a unique physical transfer function: the full-J operator is nonlinear and the modes are solved simultaneously, so the per-mode response can depend on the frozen multimode realization.

## 9. Classification

If all 90 snapshots reach `lambda=1`, pass the residual gates, and pass the dense-map UV persistence gate:

**FULLJ_DENSE_RECLOSURE_MAP_PASS**

If any snapshot fails to reach a residual-valid `lambda=1` state:

**FULLJ_DENSE_RECLOSURE_MAP_INCONCLUSIVE_SOLVER**

If all snapshots are residual-valid but at least one fails the frozen UV persistence gate:

**FULLJ_DENSE_RECLOSURE_MAP_UV_STRUCTURE_CHANGED**

In all cases:

`observational_claim_licensed = false`.

A PASS licenses construction of a subsequent nonlinear lensing projection experiment. It does not itself license an ACT comparison or claim observational agreement.