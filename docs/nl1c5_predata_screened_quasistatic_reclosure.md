# NL1C5 predata — screened quasistatic AeST field reclosure

Classification before implementation: **NL1C5_PREDATA_SCREENED_QUASISTATIC_RECLOSURE**

This gate is frozen after `NL1C4_EXPANDING_MEMORY_SOURCE_TRAJECTORY_PASS` and before inspecting any screened-reclosure outcome.

Historical classifications remain immutable.

## Scientific question

Does the action-derived retarded memory source remain nonzero after the finite-amplitude scalar field is reclosed with the **published high-gradient AeST equations**, rather than evaluated on the historical FLRW-linear `chi` field?

This is a controlled quasistatic/subhorizon reclosure at fixed total-matter state. It is not yet a dynamical re-evolution of the matter density and therefore cannot establish delayed collapse or a nonlinear matter power spectrum.

## Frozen historical input

Use only the retained certified v0.77 artifact:

- run `34315590099`;
- artifact ID `10090367181`;
- artifact SHA256 `24b97e5738eb07be4f12d433ff5f9fe22249e199e186d5617aca5dc81f748378`;
- `v077_native_state_tangent_affinity.npz` for the memory-off native total-matter state `d_m_base(k,z)`;
- `v076_v077_base_trace.dat` for the common native expansion history and historical `chi` context.

No observational data and no finite physical eta are used.

Use the exact retained modes

\[
k_h=\{0.03,0.05,0.08,0.10,0.15,0.20\}\;h\,{\rm Mpc}^{-1}
\]

which occur exactly in the v0.77 native `k` array, and the same deterministic real-space phases as NL1C4:

`[0.13, 0.71, 1.29, 2.03, 2.77, 3.41]` radians.

The log-trapezoid mode weights and primordial spectrum are frozen to

\[
P_\mathcal R(k)=A_s(k/k_*)^{n_s-1},
\]

with `A_s=2.1308864352626987e-9`, `n_s=0.9666229454895277`, `k_*=0.05 Mpc^-1`.

## Fixed matter-state reconstruction

For each native time, reconstruct a deterministic total-matter contrast representative

\[
\delta_m(x)=\sum_i
\sqrt{2\Delta_iP_\mathcal R(k_i)}\,
 d_m(k_i,z)\cos(k_ix+\varphi_i).
\]

The late-time source normalization is frozen before the result as

\[
\omega_m=\omega_b+\omega_{\rm cdm}+\omega_\nu,
\qquad
\omega_\nu=\frac{0.06}{93.14},
\]

with `omega_b=0.022377376877682164` and `omega_cdm=0.12006705327635288`.

This standard neutrino-density conversion is used only for the finite-amplitude field normalization. The primary source-survival ratios below are homogeneous under an overall rescaling of the reconstructed density field.

## Published screened AeST reclosure

Retain all three preregistered values

\[
\beta_0\in\{1,0.5,0.1\}
\]

as co-primary.

Use the already frozen mass scale

\[
\mu^2=\frac{2K_2Q_0^2}{2-K_B},
\]

with `K_B=0.0665`, `K_2=9500`, `Q_0=1e-4 Mpc^-1`.

At each time slice solve the published high-gradient AeST equations in physical spatial coordinates,

\[
\nabla_{\rm phys}^2\Phi+(1+\beta_0)\mu^2\Phi
=4\pi G_N\,\delta\rho_m,
\]

\[
\chi_{\rm scr}=\frac{\beta_0}{1+\beta_0}\Phi,
\]

with the homogeneous Fourier mode removed. In comoving Fourier variables this is

\[
\left[(1+\beta_0)\mu^2-\frac{k^2}{a^2}\right]\Phi_k
=\frac32\left(\frac{100}{c_{\rm km/s}}\right)^2
\omega_m a^{-3}\,\delta_{m,k}.
\]

This is the published AeST screened Helmholtz closure, not a GR/Poisson substitute.

## Saturation validity rule

The saturated reclosure is accepted only if its own reconstructed field remains in the certified high-gradient safety band,

\[
x_{\rm rms}=\frac{c^2}{a_0}
\sqrt{\langle|\nabla_{\rm phys}\chi_{\rm scr}|^2\rangle}
\ge10
\]

at **every native time used to integrate the retarded bath**, for every `beta0`.

If this fails for any co-primary branch, the result is classified

**NL1C5_SCREENED_RECLOSURE_TRANSITION_REQUIRES_FULL_J**

and the saturated reclosure is not promoted.

## Retarded memory source after reclosure

For each accepted screened branch, use the same frozen NL0B/NL1C3B positive Drude bath with `tauH0=10`, primary quadrature order `1024`, control order `512`, and regular zero response at the earliest native time.

Use

\[
X_{\rm scr}=\partial_x(\chi_{\rm scr}/a),
\]

\[
\mathcal B_{x,\rm scr}=X_{\rm scr}-\sum_jw_j\partial_xz_j,
\]

and the normalized direct eta-linear memory energy source

\[
\widehat\rho_{\rm mem}
=\frac14\sum_jw_j\left[
\left(\frac{\partial_x z_{j,\xi}}{r_j}\right)^2
+\left(\partial_xz_j-X_{\rm scr}\right)^2
\right].
\]

No finite physical eta is introduced.

## Locked numerical gates

For every `beta0`:

- v0.77 artifact SHA256 matches exactly;
- all six `k_h` values match the NPZ native grid with relative error `<=1e-12`;
- NPZ `z_native` and trace scale-factor grid agree to relative/absolute error `<=1e-12`;
- at least 8 native times lie in `0.2<=z<=1.5`;
- screened Helmholtz residual relative L2 `<=1e-10` at all native times;
- `chi_scr=beta0/(1+beta0) Phi` residual relative L2 `<=1e-12`;
- `Nx={256,512}` screened-field low-mode/gradient RMS agreement `<=5e-3`;
- primary/control quadrature relative L2 for `B_rms` and mean `rhohat_mem` over `0.2<=z<=1.5` each `<=1e-2`;
- all reported quantities finite.

## Frozen physical diagnosis

Provided the numerical gates and saturation-validity rule pass, define source survival by both conditions holding at every evaluation time for every co-primary `beta0`:

\[
B_{\rm rms}/X_{\rm rms}\ge10^{-3},
\]

\[
\langle\widehat\rho_{\rm mem}\rangle/X_{\rm rms}^2\ge10^{-6}.
\]

If they hold:

**NL1C5_SCREENED_MEMORY_SOURCE_SURVIVES**

If the reclosure is numerically valid but either source ratio falls below its frozen floor:

**NL1C5_SCREENED_MEMORY_SOURCE_SUPPRESSED**

The overall audit classification is

**NL1C5_SCREENED_QUASISTATIC_RECLOSURE_PASS**

only when all numerical gates and the high-gradient validity rule pass. A PASS plus `SOURCE_SURVIVES` permits the next stage: a genuinely dynamical screened scalar/matter eta=0 tangent calculation. It does not itself establish collapse regulation or observational agreement.
