# Pre-data declaration: local quarter-lattice tagged-power refinement

## Purpose

The repaired stochastic tagged power-lattice regression remained a formal FAIL only in the late-time radial power-adequacy gates. The physical-k metric projection repair is independently validated, the repaired low-k overlap is exact to numerical precision, all solver/metric/constitutive checks are clean, and the NPZ forensic audit shows that the remaining structure is reproducible across the two frozen Gaussian backgrounds and is almost purely real.

The dominant unresolved feature is a direct repaired midpoint spike around `k/h=0.0975` at `z=0.2`, with smaller unresolved structure in the `0.155--0.170` and `0.190--0.200` windows. Before any full fine-grid production campaign, this milestone asks one bounded question:

> Does a local `Delta k/h=0.0025` tagged-power lattice resolve the directly measured quarter-lattice power at `Delta k/h=0.00125` in the three preregistered problematic windows?

This is a pre-data declaration. No quarter-lattice result has been inspected when the windows, grid, gates and classification rules below are frozen.

Historical FAIL classifications remain FAILs and no earlier science threshold is relaxed.

## Required locked ancestry and local parent artifact

Required ancestors:

- repaired power-lattice regression FAIL result: `9f5218629901643574373e32c84d137c9cda2494`
- NPZ forensic addendum: `97d72584aa5ed26028e8e60e1e6ef0ccd1919a21`
- history through repaired regression FAIL and NPZ audit: `24292897672aea7a62620e766f014d7004e6d1d4`
- physical-k metric-projection repair PASS result: `20151ab785e923de20d720f3fdd8890576b6cc05`

Required local parent file:

`results/fullj_stochastic_tagged_power_lattice_kmask_regression.npz`

Frozen SHA256:

`83fb7462ec970bfef953e3804d11a81fd5843745347fe77c318c9e39b8e6e82d`

The NPZ must contain the frozen arrays `redshifts`, `K_full`, `selected_half`, `response_hybrid_B2`, and `response_half_new`, with the expected shapes from the repaired regression. No parent response value may be modified or regenerated inside this diagnostic.

## Frozen physics and stochastic setup

Identical to the repaired regression:

- reference nonlinear member: `sigma=0`, `kind=simple`, `beta0=1`
- Gaussian coefficient seed: `20260912`
- frozen coefficient SHA256: `9c511b09899cb874d09c0513b89b82c796769886ecba5dd6347c71678b19d200`
- backgrounds: `B2={0,1}`
- symmetric tag amplitude: `epsilon=0.05`
- redshifts: `z={6,5,4,3,2,1.5,1,0.5,0.2}`
- time integration: `NSTEP=4096`
- physical metric-projection cutoff: `0<|k|/h<=0.32`
- no reconstructed nonlinear metric feedback into the locked canonical trajectory.

## Frozen local windows

The three windows are fixed from the completed repaired-regression diagnostics before quarter-lattice data:

### Window W1 — dominant late-time feature

Existing `Delta k/h=0.0025` nodes:

`{0.0925,0.0950,0.0975,0.1000,0.1025,0.1050,0.1075,0.1100,0.1125}`.

New quarter-lattice nodes:

`{0.09375,0.09625,0.09875,0.10125,0.10375,0.10625,0.10875,0.11125}`.

### Window W2 — intermediate-k oscillatory region

Existing nodes:

`{0.1550,0.1575,0.1600,0.1625,0.1650,0.1675,0.1700}`.

New quarter-lattice nodes:

`{0.15625,0.15875,0.16125,0.16375,0.16625,0.16875}`.

### Window W3 — high-k feature

Existing nodes:

`{0.1900,0.1925,0.1950,0.1975,0.2000}`.

New quarter-lattice nodes:

`{0.19125,0.19375,0.19625,0.19875}`.

Total new quarter points: `18`.

## Quarter-lattice geometry

All 18 new points are run with a common geometry:

- `kF/h=0.00125 Mpc^-1`
- `NX=1024`
- `box=2*pi/(kF*h)`

Relative to the repaired half-lattice geometry (`kF/h=0.0025`, `NX=512`), the box and `NX` are both doubled, preserving the physical real-space grid spacing exactly.

Every new target is an exact integer Fourier mode on this geometry.

Cost:

`18 nodes x 2 backgrounds x 2 signs = 72` new R2 integrations.

## Parent local `Delta k/h=0.0025` lattice

For each window, construct the complete local parent response from the immutable repaired-regression NPZ:

- `0.005` nodes come from `response_hybrid_B2`;
- selected `0.0025` midpoints come from `response_half_new`.

The preregistered windows were chosen only where this union is complete at uniform `Delta k/h=0.0025`. If any expected parent node is absent or nonfinite, classify `INCOMPLETE`; do not interpolate across a missing parent node.

For each redshift, define the B2 mean direct parent power

`P_0025(k,z)=mean_B2 |T(k,z|G)|^2`.

Use PCHIP versus `ln k` separately inside each window to predict the newly computed quarter-lattice power.

Signed/complex transfer interpolation is stored only as a descriptive diagnostic.

## Frozen gates

### QL-G1 provenance and frozen identity

Require all ancestry locks, parent NPZ SHA256, Gaussian coefficient hash, backgrounds, epsilon, redshifts, NSTEP, physical-k cutoff, windows, quarter nodes and geometry to match this declaration exactly.

### QL-G2 solver/constraint health

All 72 new integrations must be finite. Across all runs:

- canonical residual `<=1e-10`
- Hamiltonian, momentum and shear metric constraints each `<=1e-8`.

### QL-G3 broadband saturated closure

Across all 72 runs and all redshifts:

`epsilon_sat <= 2e-2`.

### QL-G4 quarter-point stochastic/algebra sanity

- all direct quarter responses and powers finite
- direct power nonnegative
- `|T|^2 = Re(T)^2 + Im(T)^2` global relative residual `<=1e-12`
- B0-vs-B1 response relative L2 over all quarter points and redshifts `<=1e-3`
- B0-vs-B1 power relative L2 `<=1e-3`.

The stochastic thresholds are intentionally far looser than the `~1e-7` level already observed in the repaired NPZ audit and are only gross-regression guards.

### QL-G5 absolute quarter-lattice power interpolation accuracy

For each window and redshift, compare the direct B2 mean quarter power with the PCHIP prediction from that window's complete `Delta k/h=0.0025` parent lattice:

`E_P(W,z)=||P_pred-P_direct||_2 / max(||P_pred||_2,||P_direct||_2)`.

Also define

`E_peak(W,z)=max_i |P_pred_i-P_direct_i| / max_i P_direct_i`.

Require, across all three windows and all redshifts:

- `max E_P <= 5e-2`
- `median E_P <= 2.5e-2`
- `max E_peak <= 1e-1`
- predicted power finite and nonnegative at every quarter point.

These are the same absolute power-adequacy thresholds used in the preceding 0.005-lattice campaigns.

### QL-G6 no new unresolved quarter-point power spike

For every new quarter point and redshift, using its adjacent `Delta k/h=0.0025` parent endpoints,

`P_quarter <= 2*max(P_left,P_right) + 1e-14*Pmax_window(z)`.

This is the same factor-2 unresolved-spike veto used previously. A violation means the `0.0025` parent spacing is still insufficient locally.

### QL-G7 refinement improvement over the 0.005 parent representation

For the same new quarter points, also form a coarse prediction from the repaired hybrid `Delta k/h=0.005` lattice using the same power-PCHIP rule.

At each redshift, aggregate all 18 quarter points and compute `E_005(z)` and `E_0025(z)`.

Require strict non-worsening at every redshift within numerical tolerance,

`E_0025(z) <= E_005(z) + 1e-12`,

and strict improvement at both late-time checkpoints

`E_0025(0.5) < E_005(0.5)`

`E_0025(0.2) < E_005(0.2)`.

This gate prevents declaring success merely because the fine grid happens to satisfy an absolute threshold without demonstrating the expected refinement direction.

## Classification

PASS only if QL-G1 through QL-G7 all pass:

`FULLJ_STOCHASTIC_TAGGED_POWER_QUARTER_LATTICE_PASS`.

Otherwise:

`FULLJ_STOCHASTIC_TAGGED_POWER_QUARTER_LATTICE_FAIL`.

Use `INCOMPLETE` only for missing or inconsistent provenance/runtime/parent artifacts that prevent the frozen test from being executed.

## Scope and stop rule

A PASS establishes only that the preregistered problematic windows are locally resolved by the `Delta k/h=0.0025` parent lattice when challenged at quarter spacing `0.00125`.

A PASS licenses:

- `STOCHASTIC_TAGGED_LOCAL_QUARTER_LATTICE_TESTED=True`
- `STOCHASTIC_TAGGED_LOCAL_0025_POWER_RESOLUTION_SUPPORTED=True`.

It does **not** yet license the bounded production interpolant, 3D/evolving Weyl power, LOS lensing, ACT likelihood use, or observational claims.

If PASS, the next step is a bounded adaptive/fine production lattice built under the validated physical-k mask, using `Delta k/h=0.0025` in identified high-curvature regions and coarser spacing only where separately justified.

If FAIL because QL-G5 or QL-G6 remains materially violated, do **not** continue to `0.000625` by reflex. Preserve the FAIL and pivot to a targeted resonance/response-origin audit of the offending k-window(s). This is the preregistered stop rule.