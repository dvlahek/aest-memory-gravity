# Full-J evolving Weyl metric-projection physical-k mask repair — pre-data lock

## Purpose

The stochastic tagged box-doubling audit formally failed even though all solver, constraint and constitutive-saturation gates passed. Source-level forensics identified that the evolving Weyl metric correction retained Fourier modes by a fixed integer mode number `1<=|n|<=NMAX`, with `NMAX=32`, while later tagged campaigns changed the periodic box length. This changes the physical k cutoff and exactly predicts the observed same-k box-dependence pattern.

This milestone repairs only that geometry dependence and validates it before any further radial/power inference.

No science threshold from any historical campaign is loosened. Historical PASS/FAIL classifications remain historical records.

## Required ancestry

The run requires:

- evolving R2 bridge PASS `1f42f88e9724c58d2d242a65ca7266a207e4a0f8`;
- tagged POC PASS `aff670fa8551163f5cde2b5146e0e5840d53b424`;
- response-kernel POC PASS `2a5f884a50b7b30b90ddff01721914626dbde20f`;
- power-lattice FAIL lock `b1a66aaa6e1a37919c8287908995ee2aea79eb4e`;
- box-doubling FAIL lock `f600b7e594e57ffbbd0f3044aa2fbf4da20e942b`.

## Frozen repair

Historical metric projection used

```python
modes = np.minimum(np.arange(nx), nx - np.arange(nx))
mask = (modes >= 1) & (modes <= NMAX)
```

with `NMAX=32`.

The original R2/static geometry has

```text
kF/h = 0.01
```

because `static.BOX = 2*pi/(0.01*h)`. Therefore the original index mask has the physical meaning

```text
0 < |k|/h <= 0.32.
```

The repair is frozen as

```python
kh = abs(kk) / h
mask = (kh > 0) & (kh <= 0.32 + roundoff_tolerance)
```

where `kk=2*pi*fftfreq(nx,d=BOX/nx)` is the physical Fourier grid in Mpc^-1.

No field equation, source term, background quantity, nonlinear constitutive law, RK4 step count, Gaussian coefficient, tag amplitude or CLASS history is changed.

## Original-R2 identity requirement

Before nonlinear reruns, the implementation must verify algebraically that on the original R2 geometry (`kF/h=0.01`) and original `NX=128`, the repaired physical-k mask is elementwise identical to the historical `1<=|n|<=32` mask.

Frozen gate:

```text
MASK_ORIGINAL_R2_MISMATCH_COUNT = 0
```

This ensures the locked original R2 PASS is not redefined by the repair.

## Geometry-generalized mask requirement

For geometry A (`kF/h=0.005`, `NX=256`) and geometry B (`kF/h=0.0025`, `NX=512`), the repaired masks must represent the same physical interval `0<|k|/h<=0.32`.

The four primary physical audit nodes are

```text
k/h = {0.060, 0.095, 0.160, 0.195} Mpc^-1.
```

They deliberately span all historical mask categories:

- `0.060`: included in both old A and old B masks;
- `0.095`: historically included only in A;
- `0.160`: historical A boundary and excluded in B;
- `0.195`: historically excluded in both.

Use frozen Gaussian backgrounds `bg={0,1}`, seed `20260912`, coefficient SHA256 `9c511b09899cb874d09c0513b89b82c796769886ecba5dd6347c71678b19d200`, central nonlinear member `sigma=0`, `kind=simple`, `beta0=1`, symmetric tag `epsilon=0.05`, and both tag signs.

Run both geometries directly through the repaired code path:

- A: `kF/h=0.005`, `NX=256`, `L=2*pi/(0.005*h)`;
- B: `kF/h=0.0025`, `NX=512`, `L=2*pi/(0.0025*h)`.

Total new integrations: `4 k * 2 backgrounds * 2 signs * 2 geometries = 32`.

Use the locked corrected CLASS dense-k64 environment and `NSTEP=4096`.

## Diagnostics

For every repaired run record solver health, canonical constraint, Hamiltonian/momentum/shear residuals and broadband saturation.

For every A/B pair compare:

1. tagged response at the same physical input mode;
2. tagged power `|T_tag|^2`;
3. full canonical fields `(alpha,chi,Pchi,S)` at every checkpoint, comparing A to the first half of B;
4. directly evolved fluid fields `(delta_A,Theta_A)`;
5. reconstructed Weyl field;
6. internal repeat symmetry of every B field by comparing its first and second spatial halves.

The field comparisons are performed sign-by-sign before forming the symmetric tagged derivative.

## Frozen gates

### KM-G1 provenance/frozen identity

All required ancestry locks, coefficient hash, physical nodes, backgrounds, epsilon, geometries, member, CLASS environment and step count must match this pre-data document.

### KM-G2 original-R2 mask identity

The repaired and historical masks must be exactly identical on original R2 geometry/NX.

Gate: mismatch count `=0`.

### KM-G3 all 32 repaired runs healthy

- 32/32 finite;
- canonical residual `<=1e-10`;
- Hamiltonian, momentum and shear residual each `<=1e-8`.

### KM-G4 broadband saturated closure

Maximum saturation residual across all repaired runs/checkpoints `<=2e-2`.

### KM-G5 doubled-box repeat symmetry

Across canonical, fluid and Weyl fields, the maximum relative L2 mismatch between the first and second halves of geometry-B fields must be `<=1e-10`.

### KM-G6 direct A/B field invariance

Across canonical, fluid and Weyl fields, the maximum relative L2 mismatch between geometry A and the first half of geometry B at matched checkpoints/sign/background/k must be `<=1e-8`.

### KM-G7 tagged-response box invariance

For the symmetric tagged response:

- global relative L2 `<=1e-6`;
- maximum per-k relative L2 `<=1e-5`;
- maximum per-z relative L2 `<=1e-5`.

Near-zero pointwise relative metrics are descriptive only.

### KM-G8 tagged-power box invariance

For `|T_tag|^2`:

- global relative L2 `<=1e-6`;
- maximum per-k relative L2 `<=1e-5`;
- maximum per-z relative L2 `<=1e-5`.

## Classification

PASS label:

`FULLJ_METRIC_PROJECTION_PHYSICAL_KMASK_REPAIR_PASS`

FAIL label:

`FULLJ_METRIC_PROJECTION_PHYSICAL_KMASK_REPAIR_FAIL`

INCOMPLETE label:

`FULLJ_METRIC_PROJECTION_PHYSICAL_KMASK_REPAIR_INCOMPLETE`

A PASS licenses only:

```text
METRIC_PROJECTION_PHYSICAL_KMASK_REPAIR_VALIDATED=True
STOCHASTIC_TAGGED_BOX_DOUBLING_INVARIANCE_REPAIRED=True
```

It does not immediately restore any historical tagged radial/power license. Those observable-facing tagged results must be rerun under the repaired metric projection because some earlier changed-box campaigns crossed the historical integer cutoff.

The following remain false after this repair audit alone:

```text
STOCHASTIC_TAGGED_BOUNDED_POWER_INTERPOLANT_TESTED=False
THREE_D_BOUNDED_CONTINUOUS_WEYL_POWER_LICENSED=False
THREE_D_CONTINUOUS_WEYL_POWER_LICENSED=False
EVOLVING_WEYL_POWER_LICENSED=False
ACT_LIKELIHOOD_LICENSED=False
OBSERVATIONAL_CLAIM_LICENSED=False
```
