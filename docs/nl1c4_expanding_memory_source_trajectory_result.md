# NL1C4 result — expanding action-derived memory-source trajectory

Final classification: **NL1C4_EXPANDING_MEMORY_SOURCE_TRAJECTORY_PASS**

Predata commit: `5020070b7003521cc525ee713eeb0536558b14bb`.

Implementation commit: `6616c3a6bb4255f39d4c15a7518ecf10b4e9a68e`.

Workflow commit: `617b0e285a87b7c371dbecf43830f4c45a0b863b`.

GitHub Actions run: `34342076308` — technical SUCCESS.

Artifact: `results_bundle_nl1c4_expanding_memory_source_trajectory`, ID `10100147091`, SHA256 `93bd02a25dc675f6f6a05e104b1ebadb4aefd5c06e5bb4aa0978fdec2a5b14e4`.

The historical v0.77 input artifact was verified exactly before use: run `34315590099`, artifact ID `10090367181`, SHA256 `24b97e5738eb07be4f12d433ff5f9fe22249e199e186d5617aca5dc81f748378`.

Scope: action-derived retarded-memory source evaluated on the certified v0.77 memory-off physical-amplitude signal-band reference. No finite physical eta, screened-state re-evolution, collapse statistic, observational data or likelihood was used.

## Real-space reference

The six frozen modes

\[
k_h=\{0.03,0.05,0.08,0.10,0.15,0.20\}\;h\,{\rm Mpc}^{-1}
\]

were synthesized in a periodic box with deterministic preregistered phases and primordial amplitudes. The real-space physical-gradient RMS reproduces the prior NL1C0 band integral with maximum relative error

\[
3.8125\times10^{-16}.
\]

All eight native evaluation times in `0.2<=z<=1.5` remain in the previously identified high-gradient regime,

\[
1.0911\times10^7\le x_{\rm rms}\le9.4551\times10^7.
\]

## Retarded memory source

Using the frozen positive Drude continuum at `tauH0=10`, the longitudinal source is

\[
\mathcal B_x=X-\sum_jw_j\partial_xz_j.
\]

The normalized eta derivative of the direct memory energy source from the NL1C3B action is

\[
\widehat\rho_{\rm mem}
=\frac14\sum_jw_j\left[
\left(\frac{\partial_x z_{j,\xi}}{r_j}\right)^2
+\left(\partial_xz_j-X\right)^2
\right].
\]

Both quantities are finite and strictly nonzero at every preregistered evaluation time.

The source remains large relative to the projected gradient:

\[
0.9827228\le
\frac{B_{\rm rms}}{X_{\rm rms}}
\le0.9939683.
\]

The normalized direct metric-energy source satisfies

\[
0.245422\le
\frac{\langle\widehat\rho_{\rm mem}\rangle}{X_{\rm rms}^2}
\le0.248402.
\]

These are source-level ratios only; they are not multiplied by a finite eta and are not observational energy densities.

## Numerical closure

Primary/control Drude quadrature agreement is excellent:

\[
\epsilon_B=1.2975\times10^{-6},
\qquad
\epsilon_\rho=4.7515\times10^{-8}.
\]

The `Nx=256` versus `Nx=512` spatial checks are at approximately machine precision:

\[
\epsilon_B=1.61\times10^{-16},
\qquad
\epsilon_\rho=4.60\times10^{-16}.
\]

All preregistered gates pass.

## Consequence

NL1C4 shows that the full action-derived retarded memory source is not algebraically erased when evaluated at the certified finite perturbation amplitude. In particular, the direct eta-linear metric source identified in NL1C3 is present and numerically controlled.

The limitation is essential: the reference state is still the certified v0.77 memory-off CLASS state. It has not yet been reclosed or evolved with the saturated finite-amplitude AeST Y sector. Therefore this is **source survival on the certified reference**, not yet **memory survival after screened-state reclosure**, and not a nonlinear-collapse result.

The next physics test is a self-consistent screened AeST field reclosure at fixed matter state, followed by the same eta=0 action-derived memory source. Only after that survives should the program proceed to dynamical matter/collapse response.
