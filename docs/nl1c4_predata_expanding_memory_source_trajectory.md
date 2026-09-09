# NL1C4 predata — expanding action-derived memory-source trajectory

Classification before the official run: **NL1C4_PREDATA_EXPANDING_MEMORY_SOURCE_TRAJECTORY**

This follow-up is frozen after `NL1C3B_LONGITUDINAL_3PLUS1_MEMORY_BRIDGE_PASS`. It uses only the already certified v0.77 memory-off CLASS reference and the frozen NL0B/NL1C3B action. It does **not** solve the screened-resummed AeST state equations and therefore cannot by itself establish memory survival in the reclosed physical state.

Historical classifications remain immutable.

## Frozen input reference

Use the retained v0.77 artifact

- workflow run `34315590099`;
- artifact ID `10090367181`;
- artifact digest `sha256:24b97e5738eb07be4f12d433ff5f9fe22249e199e186d5617aca5dc81f748378`;
- file `v076_v077_base_trace.dat`.

The trace is the accepted native CLASS source-grid memory-off reference with columns `(k,tau,a,H_over_H0,chi,Q)`.

Use the already frozen signal-band modes

\[
k_h=\{0.03,0.05,0.08,0.10,0.15,0.20\}\;h\,{\rm Mpc}^{-1},
\]

and the native times satisfying

\[
0.2\le z\le1.5.
\]

Frozen cosmology/normalization:

- `H0=67.3324639084866 km s^-1 Mpc^-1`;
- `A_s=2.1308864352626987e-9`;
- `n_s=0.9666229454895277`;
- `k_pivot=0.05 Mpc^-1`;
- `a0=1.2e-10 m s^-2`;
- `tauH0=10`;
- no finite physical eta.

## Deterministic real-space representative

Use a periodic 1D box with fundamental mode `0.01 h/Mpc`, so the six retained modes are exact integer Fourier modes `{3,5,8,10,15,20}`.

For log-trapezoid weights `Delta_i` and primordial curvature power `P_R(k_i)`, reconstruct

\[
\chi_R(x,t)=\sum_i\sqrt{2\Delta_iP_R(k_i)}\,\chi_i(t)
\cos(k_i x+\varphi_i),
\]

with frozen phases

`[0.13, 0.71, 1.29, 2.03, 2.77, 3.41]` radians.

The physical projected gradient is

\[
X(x,t)=\partial_x[\chi_R(x,t)/a(t)].
\]

The real-space RMS must reproduce the prior NL1C0 band-integral RMS; this is a reconstruction control, not a new physics outcome.

## Retarded bath

Use the frozen positive Drude continuum quadrature from v0.22/v0.39 with tangent-time scale `tauH0=10`.

Primary quadrature order: `1024`.
Control quadrature order: `512`.

Regular initial condition: every normalized bath oscillator starts with zero response at the earliest retained trace time. Integrate across the complete native history before evaluating the `z=0.2..1.5` window.

For each quadrature node define the scalar response `z_j` satisfying the already certified dimensionless form

\[
z_{j,\xi\xi}+3h z_{j,\xi}+r_j^2z_j=r_j^2\chi_R/a.
\]

The longitudinal vector backreaction is

\[
\mathcal B_x=X-\sum_j w_j\partial_xz_j.
\]

The normalized eta-derivative of the direct memory energy density from the NL1C3B action is evaluated as

\[
\widehat\rho_{\rm mem}
=\frac14\sum_jw_j\left[
\left(\frac{\partial_x z_{j,\xi}}{r_j}\right)^2
+\left(\partial_xz_j-X\right)^2
\right].
\]

This quantity is an action-source diagnostic. It is not multiplied by a finite eta and is not interpreted as an observed energy density.

## Locked numerical/structural gates

- v0.77 artifact digest must match exactly;
- all six requested modes must match the trace to relative error `<=1e-12`;
- at least 8 common native times must lie in `0.2<=z<=1.5`;
- the FFT real-space `x_rms` reconstruction must agree with the analytic NL1C0 band RMS to relative error `<=1e-10`;
- primary/control quadrature relative difference for `B_rms` over the evaluation window must be `<=1e-2`;
- primary/control quadrature relative difference for mean `rhohat_mem` must be `<=1e-2`;
- the two preregistered spatial resolutions `Nx={256,512}` at primary quadrature order must agree in `B_rms` and mean `rhohat_mem` to relative error `<=5e-3`;
- all reported quantities must be finite;
- `B_rms>0` and mean `rhohat_mem>0` at every evaluation time;
- no finite eta, observational data, likelihood, halo model or collapse threshold is introduced.

## Classification

All numerical and structural gates pass:

**NL1C4_EXPANDING_MEMORY_SOURCE_TRAJECTORY_PASS**

A numerical/action inconsistency is found:

**NL1C4_EXPANDING_MEMORY_SOURCE_TRAJECTORY_FAIL**

A PASS means that the complete action-derived retarded memory source, including a direct eta-linear metric-energy source at finite perturbation amplitude, is well-defined and nonzero on the certified physical signal-band reference. It does **not** mean that the memory signal has already survived a self-consistent screened-resummed AeST reclosure.
