# Result: stochastic tagged spike source-localization audit

## Classification

`FULLJ_STOCHASTIC_TAGGED_SPIKE_SOURCE_LOCALIZATION_SATURATED_MODE_SUPPORTED`

This is a formal PASS of the preregistered mechanistic source-localization audit. It does not alter the historical repaired-regression or quarter-lattice FAIL classifications and does not license bounded continuous power, 3D/evolving Weyl power, LOS lensing, ACT likelihood use, or observational claims.

## Frozen inputs

- quarter-lattice parent NPZ SHA256: `468521f4f4c41807659cf4a8a9924149f012aef8f46ad97e91c876a7ffc3886a`
- source-localization result NPZ SHA256: `f18aaa614fa72ccbb0e63a10e7bb49c51bd69b15e806ac7ba69e0f61b52ffa91`
- source-localization JSON SHA256: `64b62d88ee7e452e25e1ef4d2278c21c81930f30520e04a2ea027e24ad59cc0b`
- Gaussian coefficient SHA256: `9c511b09899cb874d09c0513b89b82c796769886ecba5dd6347c71678b19d200`
- physical metric-projection cutoff: `0 < |k|/h <= 0.32`
- local nodes: `{0.09875,0.10125,0.10375,0.16125,0.16375,0.16625,0.19375,0.19625,0.19875}`
- center nodes: `{0.10125,0.16375,0.19625}`
- total new integrations: `54`

## Numerical controls

All 54/54 runs were finite and all six preregistered gates passed.

Key diagnostics:

- canonical residual max: `1.629046198061689e-14`
- broadband saturation max: `4.1265012159319604e-05`
- Hamiltonian residual max: `1.663117397156145e-16`
- momentum residual max: `1.5587807576658656e-16`
- Weyl decomposition residual: `4.548117222258197e-16`
- baseline reproduction versus locked parent: exact within stored precision (`global relative L2 = 0`)

### Time-step control

Comparing `NSTEP=4096` with `8192` at the three center nodes:

- tagged-response global relative L2: `7.788524341635357e-08`
- tagged-power global relative L2: `5.739943013115494e-08`
- per-center tagged-response relative L2 max: `1.1089643338981745e-07`

The sharp response is therefore not explained by RK4 phase error at the tested resolution.

### Tag-amplitude control

Comparing `epsilon=0.05` with `0.025`:

- tagged-response global relative L2: `1.535767360943723e-08`
- tagged-power global relative L2: `3.618715264802528e-08`
- per-center tagged-response relative L2 max: `2.651288266545707e-08`

The sharp response is therefore not a finite-tag artifact in the tested range.

### Same-k doubled-box control

Comparing the same three physical `k` values between `kF/h=0.00125, NX=1024` and `kF/h=0.000625, NX=2048`:

- tagged-response global relative L2: `2.4754810242363324e-14`
- tagged-power global relative L2: `3.3300644743246557e-15`
- per-center tagged-response relative L2 max: `4.451875642260564e-14`

The center responses are therefore box invariant to numerical precision under the validated physical-k metric projection.

## Saturated-surrogate mechanism

The exact surrogate

`div[(1+j_eff) grad chi] -> 2 lap chi`

was rerun at all nine local nodes with no other equation, CLASS forcing, metric reconstruction, initial state, parameter, or tag normalization changed.

Agreement with the full retained nonlinear operator is exceptionally tight:

- tagged-response global relative L2: `4.150917802835319e-08`
- tagged-power global relative L2: `1.0044222314457634e-07`
- tagged-response per-k relative L2 max: `6.182885486137577e-08`
- correlation of `Re T(k,z=0.2)` across the nine nodes: `0.9999999999999999`
- relative center-power differences at `z=0.2`: `1.02e-7`, `1.51e-7`, `1.29e-7`

Thus the local sharp tagged response does not require the small residual nonlinear constitutive term. Within the tested regime it is carried by the saturated mode dynamics.

## Component localization

The stored decomposition satisfies

`T[W_total] = T[W_CLASS] + T[W_corr]`

at relative residual `4.55e-16`.

The local shape is present in several coupled quantities, including the canonical variables, effective-fluid variables and Weyl pieces. The result therefore does not support interpreting the effect as a failure of the nonlinear constitutive operator. It instead motivates a Fourier-reduced saturated-mode description.

One important limitation remains: the local nine-node source-localization set consists of quarter-offset points. The strongest earlier apparent power spikes were defined by interleaving those points with parent `0.0025`/`0.005` nodes. Before promoting a spectral-fringe interpretation, the parent near-node values should be rerun in the same `kF/h=0.00125, NX=1024` geometry. This is a small same-k geometry certification, not another grid-halving campaign.

## Scope

Validated:

- `STOCHASTIC_TAGGED_SPIKE_SOURCE_LOCALIZATION_TESTED=True`
- `STOCHASTIC_TAGGED_SATURATED_MODE_MECHANISM_SUPPORTED=True`

Still not licensed:

- bounded continuous tagged-power interpolant
- continuous/evolving 3D Weyl power
- LOS lensing
- ACT likelihood use
- observational claim

## Decision

Do not return to blind radial power interpolation.

The next bounded test should rerun the six interleaved parent near-node wavenumbers in the same quarter-grid geometry and compare them at identical physical `k` with the already locked repaired parent response. If that same-k certification passes, the merged local profile is geometry-independent and the next milestone is a Fourier-reduced saturated elastic-mode solver with preregistered held-out node/lobe predictions.
