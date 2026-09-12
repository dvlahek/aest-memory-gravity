# Full-J stochastic tagged box-doubling audit — locked result

## Classification

`FULLJ_STOCHASTIC_TAGGED_BOX_DOUBLING_AUDIT_FAIL`

This historical result remains a formal FAIL. All solver, constraint and broadband-saturation gates passed. The two same-k box-invariance gates failed.

## Frozen setup

The audit compared the same physical tagged modes on two periodic embeddings with the same real-space spacing:

- geometry A: `kF/h=0.005`, `NX=256`, `L=1866.3167638478922 Mpc`;
- geometry B: `kF/h=0.0025`, `NX=512`, `L=3732.6335276957843 Mpc`.

Audited physical nodes were `k/h={0.03,0.06,0.095,0.10,0.12,0.16,0.195,0.20}`, with Gaussian backgrounds 0 and 1 and symmetric `epsilon=0.05` tags.

## Numerical result

All 32/32 new runs were finite and constraint-clean. The broadband saturation maximum was `4.349214792060783e-05`, the canonical residual maximum was `1.5061342189977616e-14`, and metric constraint residuals remained at machine precision.

Nevertheless:

- response global relative L2 = `0.020425009589428292`;
- power global relative L2 = `0.012374467277230837`;
- response per-k maximum = `0.09555342657705197`;
- power per-k maximum = `0.23445283225314748`;
- response per-z maximum = `0.06247574998143056`;
- power per-z maximum = `0.04664933736978254`.

The discrepancy was strongly localized in physical k:

| k/h | response relL2 | power relL2 |
|---:|---:|---:|
| 0.030 | 2.04e-14 | 1.53e-14 |
| 0.060 | 5.77e-15 | 6.68e-15 |
| 0.095 | 2.985e-2 | 1.180e-2 |
| 0.100 | 3.558e-2 | 9.780e-3 |
| 0.120 | 5.676e-2 | 6.065e-2 |
| 0.160 | 9.555e-2 | 2.345e-1 |
| 0.195 | 6.50e-15 | 7.79e-16 |
| 0.200 | 1.89e-14 | 1.74e-15 |

The discrepancy also grew continuously toward late time: power relative L2 was at machine precision at z=6, `7.52e-4` at z=1, `4.27e-3` at z=0.5, and `4.665e-2` at z=0.2.

## Source-level forensic diagnosis

The audit exposed a geometry-dependent Fourier cutoff in the evolving Weyl metric correction. The locked bridge implementation contains

```python
modes = np.minimum(np.arange(nx), nx - np.arange(nx))
mask = (modes >= 1) & (modes <= NMAX)
```

with `NMAX=32`.

On the original R2 geometry, `static.BOX=2*pi/(0.01*h)`, so this index cutoff represented the physical interval `0 < k/h <= 0.32`. On later embeddings the same integer cutoff was retained while `static.BOX` changed. Therefore its physical meaning changed:

- geometry A (`kF/h=0.005`): old cutoff `k/h <= 0.16`;
- geometry B (`kF/h=0.0025`): old cutoff `k/h <= 0.08`.

This predicts the observed failure pattern exactly:

- `k/h=0.03,0.06`: included by the old metric-projection mask in both geometries -> machine-precision invariance;
- `k/h=0.095,0.10,0.12,0.16`: included in geometry A but excluded in geometry B -> box dependence;
- `k/h=0.195,0.20`: excluded in both geometries -> machine-precision invariance.

The initial tagged/background fields themselves are periodic repeats between the two geometries, the physical grid spacing is unchanged, and the RK4 timestep count is unchanged. The integer-mode cutoff is therefore a concrete implementation confound and must be repaired before interpreting the earlier half-lattice spikes as physical radial structure.

## Repair rule

Do not loosen any science gate. Preserve all historical classifications. For geometry-generalized runs replace the fixed integer-index projection cutoff by the **same frozen physical cutoff represented by the original R2 setup**:

`0 < |k|/h <= 0.32`.

The original R2 calculation must be algebraically unchanged because, on its original `kF/h=0.01` geometry, the repaired physical mask is exactly identical to the historical `1<=|n|<=32` mask.

Before re-running the power lattice, perform a bounded preregistered repair audit that reruns both geometries through the same repaired code path and verifies repeated-field/cross-geometry invariance.

## Scope

This audit does **not** invalidate the original R2 PASS on its original geometry. It does require revalidation of later tagged campaigns that changed `static.BOX`, especially comparisons across different box lengths and nodes whose Fourier index crossed the historical `NMAX=32` boundary.

No continuous Weyl-power, ACT-likelihood, or observational license is granted by this FAIL.