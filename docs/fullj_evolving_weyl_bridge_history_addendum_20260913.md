# Full-J evolving Weyl bridge history addendum — 2026-09-13

This addendum continues `docs/fullj_evolving_weyl_bridge_history.md` after the local quarter-lattice FAIL. Historical PASS/FAIL classifications are not rewritten.

## 2026-09-13 — spike source-localization SATURATED MODE SUPPORTED

The preregistered 54-run source-localization audit completed with all 54/54 integrations finite and all six gates passing. The formal classification is

`FULLJ_STOCHASTIC_TAGGED_SPIKE_SOURCE_LOCALIZATION_SATURATED_MODE_SUPPORTED`.

Numerical controls are exceptionally tight:

- canonical residual max `1.629046198061689e-14`
- broadband saturation max `4.1265012159319604e-05`
- Hamiltonian residual max `1.663117397156145e-16`
- momentum residual max `1.5587807576658656e-16`
- baseline reproduction relative L2 `0`
- time-step response relative L2 `7.788524341635357e-08`
- epsilon response relative L2 `1.535767360943723e-08`
- same-k doubled-box response relative L2 `2.4754810242363324e-14`
- same-k doubled-box power relative L2 `3.3300644743246557e-15`
- Weyl decomposition residual `4.548117222258197e-16`.

The exact saturated surrogate

`div[(1+j_eff) grad chi] -> 2 lap chi`

reproduces the full retained nonlinear tagged response with response global relative L2 `4.150917802835319e-08`, power global relative L2 `1.0044222314457634e-07`, `z=0.2` real-response correlation `0.9999999999999999`, and center-power relative differences of order `1e-7`.

The local sharp response therefore does not require the small residual nonlinear constitutive term. Within the tested regime it is carried by the saturated mode dynamics. The time-step, finite-tag and same-k box explanations are excluded at the tested center wavenumbers.

Formal result lock: `docs/fullj_stochastic_tagged_spike_source_localization_result.md`, commit `86ab13ffa1048860731f65348074ede1b469c644`.

A post-hoc mechanistic note (`docs/fullj_spectral_fringe_hypothesis.md`, commit `1dcafa0643fa99e5de527dcb4a66589814ec6301`) reframes the earlier power-spike language in terms of candidate signed-transfer node/lobe structure. This is a working hypothesis only; no physical fringe claim is yet licensed.

## Remaining geometry confound and next preregistered audit

The nine-node source-localization set consists only of quarter-offset points in the common `kF/h=0.00125, NX=1024` geometry. The strongest earlier apparent spike ratios were defined by interleaving those points with parent `0.0025`/`0.005` nodes inherited from coarser geometries. Therefore the node/lobe interpretation still requires one direct same-k certification at the parent near-node wavenumbers.

A new 12-run audit is preregistered before those data are recomputed. It reruns

`k/h = {0.1000,0.1025,0.1625,0.1650,0.1950,0.1975}`

in the same quarter-grid geometry `kF/h=0.00125, NX=1024`, background `bg=0`, both tag signs, and compares directly with the already locked repaired parent response at identical physical `k`.

Predata commit: `3039f8378af06c7ceecd1932fa5ec93890d971e7`.
Implementation commit: `2bc431b063e9f80f2db9b532cbca3e7b5ce2daff`.
Runner commit: `d90a4920fbad3e9eb9ce6cc80d66dbed9422eb70`.

Target PASS classification:

`FULLJ_STOCHASTIC_TAGGED_SPECTRAL_FRINGE_GEOMETRY_CERTIFIED`.

If it passes, geometry forensics for these windows stop. The next milestone is a Fourier-reduced saturated elastic-mode solver and preregistered held-out predictions of signed-transfer node/lobe locations. No further blind radial grid halving is planned.
