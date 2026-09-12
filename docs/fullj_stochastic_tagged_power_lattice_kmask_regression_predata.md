# Pre-data declaration: repaired stochastic tagged power-lattice regression

## Purpose

The historical stochastic tagged power-lattice campaign completed all 176 integrations with clean solver, metric-constraint, stochastic-background and constitutive diagnostics, but failed the two radial power gates. A subsequent same-k box-doubling audit isolated a deterministic implementation defect in the evolving-Weyl metric projection: the historical integer mask `1<=|n|<=32` was retained after the periodic box changed, so its physical cutoff changed with `kF`. The preregistered physical-k repair restored the original R2 meaning `0<|k|/h<=0.32` and then passed direct A/B box invariance at numerical precision.

This milestone is a bounded regression between that repair PASS and a full from-scratch repaired power-lattice production campaign. It tests the two previously failed observable-facing power gates under the repaired metric projection while using a narrowly certified subset of historical Stage-A data only as a regression accelerator.

No threshold from the historical power-lattice declaration is relaxed. Historical FAIL classifications remain historical FAILs.

## Required locked ancestry

- evolving R2 bridge PASS: `1f42f88e9724c58d2d242a65ca7266a207e4a0f8`
- tagged-mode POC PASS: `aff670fa8551163f5cde2b5146e0e5840d53b424`
- response-kernel POC PASS: `2a5f884a50b7b30b90ddff01721914626dbde20f`
- historical stochastic tagged power-lattice FAIL: `b1a66aaa6e1a37919c8287908995ee2aea79eb4e`
- physical-k metric-projection repair PASS result: `20151ab785e923de20d720f3fdd8890576b6cc05`
- history through repair PASS: `c2c275c396dc879d24fa5ca953b484dcc4ab4c03`

The local historical power-lattice JSON/NPZ and local repair-audit JSON are required runtime inputs. The historical power-lattice JSON must preserve G1--G5 true and G6--G7 false. The repair JSON must preserve all KM-G1--KM-G8 true and both repair scope flags true.

## Frozen physics and stochastic setup

Identical to the historical power-lattice campaign:

- reference nonlinear member: `sigma=0`, `kind=simple`, `beta0=1`
- Gaussian coefficient seed: `20260912`
- frozen coefficient SHA256: `9c511b09899cb874d09c0513b89b82c796769886ecba5dd6347c71678b19d200`
- regression backgrounds: `B2={0,1}`
- symmetric tag amplitude: `epsilon=0.05`
- redshifts: `z={6,5,4,3,2,1.5,1,0.5,0.2}`
- time integration: `NSTEP=4096`
- no reconstructed nonlinear metric feedback into the locked canonical trajectory.

The only implementation change relative to the historical campaign is the already validated physical-k metric projection mask `0<|k|/h<=0.32`.

## Historical Stage-A reuse boundary and certification

The historical Stage-A geometry was

- `kF/h=0.005 Mpc^-1`
- `NX=256`
- `box=2*pi/(kF*h)`.

Under the historical integer mask `|n|<=32`, this geometry projected metric-correction modes only through `k/h=0.16`. The repaired mask instead retains metric-correction modes through the original physical R2 cutoff `k/h=0.32`. Therefore even a tagged target with `k/h<=0.16` can in principle change through higher-harmonic or broadband coupling in the reconstructed metric/effective-fluid evolution. Historical low-k Stage-A data are **not** assumed unchanged by construction.

For this bounded regression only, historical Stage-A responses at `k/h<=0.16` may be reused if a fresh repaired overlap test demonstrates negligible change at three preregistered domain probes:

`K_overlap={0.060,0.095,0.160} h Mpc^-1`.

These probe the low/mid region, the previously problematic late-time region, and the old mask boundary. Each overlap node is freshly recomputed for B2 and both signs under the repaired mask and compared with the corresponding historical Stage-A B2 entry.

Frozen reuse-certification gates:

- response global relative L2 `<=1e-6`
- response per-node maximum relative L2 `<=1e-5`
- power global relative L2 `<=2e-6`
- power per-node maximum relative L2 `<=2e-5`.

This three-node test is an empirical regression certification only. It does not license the reused lattice as final production data. If any overlap gate fails, historical Stage-A reuse is not permitted and the regression FAILs. Do not substitute fresh nodes silently. A later full production campaign must recompute the complete lattice under the repaired mask regardless of this regression outcome.

## Stage A-R: repaired high-k completion

Freshly recompute all complete-lattice target nodes above the old Stage-A cutoff:

`K_repair={0.165,0.170,0.175,0.180,0.185,0.190,0.195,0.200} h Mpc^-1`.

Use B2 backgrounds and both tag signs in the historical Stage-A geometry. Cost:

`8 nodes x 2 backgrounds x 2 signs = 32` integrations.

Together with the 12 overlap-certification integrations, Stage A-R costs 44 integrations.

Construct a hybrid repaired B2 complete lattice on

`K_full={0.030,0.035,...,0.200} h Mpc^-1`

by using the historical Stage-A B2 responses for `k/h<=0.16` only if KR-G2 passes and replacing every node `k/h>0.16` with the fresh repaired response. This hybrid object is a regression diagnostic only and is not the final production lattice.

## Stage B-R: repaired half-lattice validation

Apply the exact historical adaptive-selection algorithm to the repaired hybrid B2 mean power lattice:

- candidates are all 34 half-lattice midpoints between adjacent 0.005 nodes;
- always include the six fixed domain controls nearest `{0.0325,0.0625,0.0925,0.1225,0.1625,0.1975}`;
- rank remaining intervals by the historical normalized power-curvature score evaluated over `z={1,0.5,0.2}`;
- select exactly 16 unique intervals, ties by increasing midpoint k.

No historical selected-half response is reused. All 16 selected midpoints are freshly run under the repaired mask in the half-lattice geometry

- `kF/h=0.0025 Mpc^-1`
- `NX=512`
- doubled box with the same physical real-space spacing as Stage A.

Use B2 and both signs. Cost:

`16 x 2 x 2 = 64` integrations.

Total new integrations in this regression:

`44 + 64 = 108`.

## Frozen power test

For each redshift, construct the same PCHIP interpolant of B2 mean direct power versus `ln k` on the repaired hybrid 0.005 lattice. Evaluate it at the 16 freshly computed repaired half-lattice points.

Signed/complex transfer interpolation remains descriptive only. The primary object is

`P_tag(k,z)=<|T_tag(k,z|G)|^2>_G`.

## Frozen gates

### KR-G1 provenance and frozen identity

All required ancestry locks, local historical classifications, coefficient hash, grids, backgrounds, epsilon, NSTEP, physical-k cutoff and adaptive-selection algorithm must match this declaration. The repair must reproduce the original R2 mask with mismatch count zero.

### KR-G2 overlap reuse certification

All 12 overlap runs finite and solver-clean, and the four overlap response/power regression thresholds above must pass.

### KR-G3 Stage A-R health and saturation

All 44 Stage A-R integrations finite. Across them:

- canonical residual `<=1e-10`
- Hamiltonian, momentum and shear metric constraints each `<=1e-8`
- broadband saturation residual `<=2e-2`.

### KR-G4 repaired hybrid power sanity

The complete B2 hybrid response/power lattice must be finite, direct power nonnegative, and

`|T|^2 = Re(T)^2 + Im(T)^2`

must hold with global relative residual `<=1e-12`.

### KR-G5 Stage B-R health and saturation

All 64 repaired half-lattice integrations finite with the same canonical/metric gates and broadband saturation residual `<=2e-2`.

### KR-G6 repaired half-lattice power interpolation accuracy

Use exactly the historical PL-G6 thresholds:

- `max_z E_P(z) <= 5e-2`
- `median_z E_P(z) <= 2.5e-2`
- `max_z E_peak(z) <= 1e-1`
- interpolated power finite and nonnegative at all selected controls.

### KR-G7 no unresolved repaired half-lattice power spike

Use exactly the historical PL-G7 veto at every selected midpoint and redshift:

`P_mid <= 2 * max(P_left,P_right) + 1e-14*Pmax(z)`.

No spike threshold is changed after seeing the repaired data.

## Classification

PASS only if KR-G1 through KR-G7 all pass:

`FULLJ_STOCHASTIC_TAGGED_POWER_LATTICE_KMASK_REGRESSION_PASS`.

Otherwise:

`FULLJ_STOCHASTIC_TAGGED_POWER_LATTICE_KMASK_REGRESSION_FAIL`.

Use `INCOMPLETE` only for missing provenance/runtime/input artifacts that prevent the frozen diagnostic from executing.

## Scope

A PASS establishes only that the previously failed bounded power-lattice gates pass after the independently validated physical-k projection repair and that limited historical Stage-A reuse is empirically adequate for this regression diagnostic.

A PASS licenses only:

- `STOCHASTIC_TAGGED_POWER_LATTICE_KMASK_REGRESSION_TESTED=True`.

Keep false until a full repaired production campaign is completed:

- `STOCHASTIC_TAGGED_BOUNDED_POWER_INTERPOLANT_TESTED=False`
- `THREE_D_BOUNDED_CONTINUOUS_WEYL_POWER_LICENSED=False`
- `THREE_D_CONTINUOUS_WEYL_POWER_LICENSED=False`
- `EVOLVING_WEYL_POWER_LICENSED=False`
- `ACT_LIKELIHOOD_LICENSED=False`
- `OBSERVATIONAL_CLAIM_LICENSED=False`.

If this regression PASSes, the next milestone is a full from-scratch repaired power-lattice production campaign with no stale historical K2/Stage-A response reuse. If it FAILs, preserve the FAIL and diagnose the repaired direct controls without loosening any threshold.
