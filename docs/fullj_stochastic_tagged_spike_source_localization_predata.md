# Pre-data: stochastic tagged spike source-localization audit

## Purpose

The repaired quarter-lattice campaign is formally classified

`FULLJ_STOCHASTIC_TAGGED_POWER_QUARTER_LATTICE_FAIL`.

All provenance, solver, metric-constraint, broadband-saturation, and stochastic-algebra gates passed, but direct quarter-grid measurements exposed new late-time radial spikes and non-monotone refinement. Blind radial halving is therefore stopped. This audit is mechanistic: it asks if the sharp tagged response is stable to time step, tag amplitude, and periodic box, and if it is reproduced by the exact saturated surrogate already suggested by the measured constitutive residual.

No power-lattice threshold is relaxed and no observational scope is licensed by this audit.

## Locked ancestry

- physical-k metric-projection repair PASS result: `20151ab785e923de20d720f3fdd8890576b6cc05`
- repaired power-lattice regression FAIL result: `9f5218629901643574373e32c84d137c9cda2494`
- repaired regression NPZ forensic addendum: `97d72584aa5ed26028e8e60e1e6ef0ccd1919a21`
- quarter-lattice preregistration: `3d309b51e44eb38569a7be263dbb14963ba4bd17`
- quarter-lattice formal FAIL result: `c1dd14b2d15fcd48519c328eb4906ef5d1b265b4`
- canonical history through the quarter-lattice decision: `ce8ef79da695fae7b37793f325678096eb5dc2ac`

The local parent quarter-lattice NPZ is frozen by SHA256

`468521f4f4c41807659cf4a8a9924149f012aef8f46ad97e91c876a7ffc3886a`.

The Gaussian coefficient SHA256 remains

`9c511b09899cb874d09c0513b89b82c796769886ecba5dd6347c71678b19d200`.

## Frozen targets

Three direct quarter-grid spike centers are selected from the completed quarter-lattice result:

- `k/h = 0.10125`
- `k/h = 0.16375`
- `k/h = 0.19625`

For source localization, each center is accompanied by its immediate quarter-grid neighbors:

- W1: `{0.09875, 0.10125, 0.10375}`
- W2: `{0.16125, 0.16375, 0.16625}`
- W3: `{0.19375, 0.19625, 0.19875}`

Thus the local shape set has nine physical wavenumbers.

Only frozen Gaussian background `bg=0` is used for the new mechanistic runs. This is fixed before the audit because the completed quarter-lattice campaign already measured B0/B1 agreement at `8.35e-08` in tagged response and `2.02e-07` in tagged power. The audit is therefore not a stochastic-convergence campaign.

The reference nonlinear member remains `sigma=0`, `kind=simple`, `beta0=1.0`.

## Baseline and controls

The baseline tagged perturbation is symmetric with `epsilon=0.05`.

Baseline geometry:

- `kF/h = 0.00125`
- `NX = 1024`
- `NSTEP = 4096`
- physical metric-projection cutoff `0 < |k|/h <= 0.32`.

Four new controls are frozen.

### C0 — baseline component rerun

All nine local nodes are rerun at the baseline setup for both tag signs. This produces 18 runs and must reproduce the locked parent `bg=0` tagged response before component localization is interpreted.

### C1 — time-step convergence

Only the three spike centers are rerun with

- `NSTEP = 8192`
- otherwise baseline geometry and `epsilon=0.05`.

This produces 6 runs.

### C2 — tag-amplitude convergence

Only the three spike centers are rerun with

- `epsilon = 0.025`
- otherwise baseline geometry and `NSTEP=4096`.

This produces 6 runs.

### C3 — same-k box doubling

Only the three spike centers are rerun in a doubled periodic box at fixed physical spacing:

- `kF/h = 0.000625`
- `NX = 2048`
- `NSTEP = 4096`
- `epsilon = 0.05`.

All three target wavenumbers and the six frozen Gaussian background modes are exact Fourier modes in this geometry. The physical metric-projection cutoff remains `0.32 h/Mpc`.

This produces 6 runs.

### C4 — exact saturated surrogate

All nine local nodes are rerun at the baseline geometry and time step, but only the nonlinear projected scalar-current operator is replaced by its exact saturated surrogate

`div[(1+j_eff) grad chi] -> 2 lap chi`.

No other equation, CLASS forcing, metric reconstruction, initial state, parameter, or tag normalization is changed. This produces 18 runs.

Total new integrations: `18 + 6 + 6 + 6 + 18 = 54`.

## Stored source decomposition

For every new run the tagged Fourier coefficient at the target physical `k` is stored for

- total Weyl field `W_total`,
- CLASS Weyl contribution `W_CLASS`,
- metric-correction Weyl contribution `W_corr`,
- effective-fluid `delta_A`,
- effective-fluid `Theta_A`,
- canonical `alpha`, `chi`, `P_chi`, `S`,
- elliptic field `E`.

For every signed pair the normalized tagged response is formed with the same amplitude and phase convention as the locked tagged-mode chain.

The identity

`T[W_total] = T[W_CLASS] + T[W_corr]`

is audited directly.

## Gates

### SL-G1 — provenance and frozen identity

Require all locked ancestry, exact coefficient hash, exact parent NPZ hash, active physical-k repair, original-R2 mask identity, exact target lists, and exactly 54 planned new runs.

### SL-G2 — baseline reproduction and numerical health

Require all 54/54 runs finite. Across all variants require

- canonical residual `<= 1e-10`,
- Hamiltonian, momentum, and shear residuals each `<= 1e-8`.

For the full nonlinear variants C0--C3, broadband saturation must remain `<= 2e-2`.

The C0 nine-node tagged response must reproduce the frozen parent `bg=0` response with

- global relative L2 `<= 1e-8`,
- per-k relative L2 max `<= 3e-8`.

The Weyl decomposition identity must have global relative residual `<= 1e-12`.

### SL-G3 — time convergence

Comparing C1 (`8192`) with C0 (`4096`) at the three centers:

- tagged-response global relative L2 `<= 5e-3`,
- tagged-power global relative L2 `<= 1e-2`,
- per-center tagged-response relative L2 `<= 1e-2`.

### SL-G4 — epsilon convergence

Comparing C2 (`epsilon=0.025`) with C0 (`epsilon=0.05`) at the three centers:

- tagged-response global relative L2 `<= 1e-2`,
- tagged-power global relative L2 `<= 2e-2`,
- per-center tagged-response relative L2 `<= 2e-2`.

### SL-G5 — same-k box invariance

Comparing C3 with C0 at the same three physical wavenumbers:

- tagged-response global relative L2 `<= 1e-4`,
- tagged-power global relative L2 `<= 2e-4`,
- per-center tagged-response relative L2 `<= 3e-4`.

This gate tests the already repaired physical-k projection in the more extreme quarter-grid box geometry. It does not alter the earlier repair PASS.

### SL-G6 — saturated-surrogate mechanism

C4 is compared with C0 over all nine local nodes. The saturated-mode mechanism is supported only if all are true:

- tagged-response global relative L2 `<= 5e-2`,
- tagged-power global relative L2 `<= 1e-1`,
- Pearson correlation of `Re T(k,z=0.2)` across the nine nodes `>= 0.95`,
- relative power difference at each of the three spike centers at `z=0.2` `<= 0.25`.

These thresholds are mechanistic, not production-power accuracy gates.

## Classification rule

If SL-G1 through SL-G5 pass and SL-G6 passes, classify

`FULLJ_STOCHASTIC_TAGGED_SPIKE_SOURCE_LOCALIZATION_SATURATED_MODE_SUPPORTED`.

If SL-G1 through SL-G5 pass but SL-G6 fails, classify

`FULLJ_STOCHASTIC_TAGGED_SPIKE_SOURCE_LOCALIZATION_NONLINEAR_RESIDUAL_REQUIRED`.

If provenance is valid but any of SL-G2 through SL-G5 fails, classify

`FULLJ_STOCHASTIC_TAGGED_SPIKE_SOURCE_LOCALIZATION_NUMERICAL_CONTROL_FAIL`.

If frozen provenance or required inputs are incomplete, classify

`FULLJ_STOCHASTIC_TAGGED_SPIKE_SOURCE_LOCALIZATION_INCOMPLETE`.

No classification from this audit licenses a bounded continuous power interpolant, 3D/evolving Weyl power, LOS lensing, ACT likelihood use, or observational claims.

## Decision after the audit

- If the saturated-mode classification is obtained, stop radial grid-halving and derive a mode-by-mode saturated transfer/dispersion representation before returning to production `P_W(k,z)`.
- If the nonlinear-residual classification is obtained, use the stored component responses to localize the first field in which the spike contrast appears and audit that dynamical sector directly.
- If a numerical-control FAIL is obtained, repair the identified control first. Do not interpret the spikes physically and do not relax any gate.
