# NL1C4 result — expanding action-derived memory-source trajectory

Final classification: **NL1C4_EXPANDING_MEMORY_SOURCE_TRAJECTORY_PASS**

Frozen predata document blob SHA: `c8174b6146f4fd440d50d5595700840cc101188b`.

Implementation-lock commit: `379ff2d8c8a65147114aca5363ad2eb6a894f992`.

Implementation commit: `97c84e489dcdd9ed30fe4b7a437b94df42569a27`.

Workflow commit: `e6b8b1956fdfd53aa6b4dfd3c25650fb192523cd`.

GitHub Actions run: `35074946151` — technical SUCCESS.

Artifact: `results_bundle_nl1c4_expanding_memory_source_trajectory`, artifact ID `10437352769`, SHA256 `5594457eab915ed2150e4a66d35cb8b98b8c5f6f084c3a0ced1f556f0a86913c`.

Scope: theory-only expanding periodic-box action-source trajectory. No finite physical eta, observational data, likelihood, halo model, collapse threshold, or off-native time interpolation was used.

## Frozen input and dependency

The run re-executed the frozen NL1C3B longitudinal 3+1 action bridge and required

`NL1C3B_LONGITUDINAL_3PLUS1_MEMORY_BRIDGE_PASS`

before evaluating the expanding source trajectory.

The retained v0.77 artifact was then checked against the frozen provenance:

- workflow run `34315590099`;
- artifact ID `10090367181`;
- digest `sha256:24b97e5738eb07be4f12d433ff5f9fe22249e199e186d5617aca5dc81f748378`;
- trace `v076_v077_base_trace.dat`.

All six requested modes were found with zero reported relative miss. Their common native histories contain 24 times, including exactly eight common native times in `0.2<=z<=1.5`.

## Reconstruction control

The deterministic six-mode real-space representative uses the frozen phases and exact integer Fourier modes `{3,5,8,10,15,20}`. The physical projected gradient is

\[
X(x,t)=\partial_x[\chi_R(x,t)/a(t)].
\]

Across both preregistered spatial resolutions and both Drude quadrature orders, the real-space RMS reproduces the analytic NL1C0 band RMS with maximum relative error

\[
3.15\times10^{-16},
\]

well below the frozen `1e-10` gate.

The resulting analytic `x_rms` values reproduce the previous high-gradient trajectory, rising from approximately

\[
1.0911\times10^7
\]

at `z=1.385` to

\[
9.4551\times10^7
\]

at `z=0.248`.

## Retarded-source controls

The complete native history was integrated before evaluating the frozen redshift window. The primary quadrature order was 1024 and the control order was 512.

Using the stricter locked maximum pointwise relative difference over the eight native evaluation times:

- `B_rms`, 512 vs 1024: `3.0820e-6`;
- mean `rhohat_mem`, 512 vs 1024: `1.4440e-7`;
- `B_rms`, `Nx=256` vs `Nx=512`: `4.0605e-16`;
- mean `rhohat_mem`, `Nx=256` vs `Nx=512`: `5.8019e-16`.

All are far inside their preregistered gates.

Both action-derived source diagnostics are finite and positive at every evaluation time. In the dimensionless acceleration-gradient normalization used for reporting, `B_rms` evolves from approximately `1.0845e7` at `z=1.385` to `9.2918e7` at `z=0.248`. The corresponding reported dimensionless-gradient-squared mean `rhohat_mem` increases from approximately `2.96e13` to `2.19e15`.

## Classification

Every numerical and structural gate passed. Therefore

\[
\boxed{\text{NL1C4\_EXPANDING\_MEMORY\_SOURCE\_TRAJECTORY\_PASS}}.
\]

This closes a specific bridge: the complete action-derived retarded memory source, including the direct eta-linear metric-energy source identified in NL1C3B, is well-defined, nonzero, and numerically stable on the certified expanding physical signal-band reference.

## What this does not establish

The result does not show that the memory signal survives a self-consistent screened-resummed AeST reclosure. It does not provide a spherical-collapse equation, a halo force law, a splashback prediction, or an observational constraint.

The next nonlinear checkpoint must therefore derive the self-gravitating spherical embedding from the already frozen action/field equations before any halo mass, collapse threshold, turnaround radius, or splashback observable is evaluated. The NL1C4 trajectory may be used as a dependency/control for that derivation, but not as a substitute for it.

Historical classifications remain unchanged.
