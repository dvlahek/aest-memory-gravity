# Stable AeST growth–Weyl memory R4 — common-mode mechanism post-data

Date: 2026-09-14

## Formal classification

`STABLE_AEST_GROWTH_WEYL_MEMORY_R4_SINGLE_AMPLITUDE_MODE_CERTIFIED`

R4 completed with `EXIT=0` and all preregistered gates G1–G7 passed.

## Frozen science context

- Parent host: corrected dense-k64 stable-chi AeST realization, CLASS head `e85808324f51fc694d12e3ed7439552a3c3f9540`.
- R4 pre-data lock: `f742cfb33bd00ec8e1b637d7d1e7201d464fc433`.
- R3 parent: `STABLE_AEST_GROWTH_WEYL_MEMORY_R3_SCALE_GENERALITY_CERTIFIED`.
- Physical memory settings: `tau H0 = 10`, memory order 20, `eta = {0, 0.005, 0.01}`, `tol_perturbations_integration = 3e-8`.
- Held-out scales: `k_h = {0.10000, 0.10125, 0.10250, 0.10375, 0.16500, 0.19750, 0.19875}`.
- Redshifts: `z = {6,5,4,3,2,1.5,1,0.5,0.2}`.
- Science method: direct physical finite-eta runs with separate transfer outputs `d_m`, `phi`, `psi`, and `W=phi+psi`; no diagnostic variational forcing in the R4 science source.

## Source topology

R4 used a fresh disposable source tree derived from the frozen parent. The historical dormant diagnostic `aest_tangent_external_force` injection was removed from that disposable tree before the science build. The final R4 source audit certified:

- stable-chi residual marker present;
- `chi = Q s` in the physical RHS;
- physical memory multiplier `Bchi_aest *= aest_eta` appears exactly once in `perturbations_derivs`;
- physical closure `E_rhs_aest -= 0.5*Q_aest*Bchi_aest` appears exactly once;
- `aest_eta` appears exactly once in the physical derivative block;
- diagnostic external forcing is absent from the science derivative block.

This licenses the statement that R4 probes one direct physical memory forcing channel in the scalar closure.

## Numerical result

All 21 direct physical runs were finite and transfer-basis clean. All seven scales passed strict finite-eta tangent consistency for each of `d_m`, `phi`, `psi`, and `phi+psi`.

The preregistered single-amplitude test passed on all seven scales. The maximum vector-L2 mismatches were:

- `max B_WD = 2.175482795441085e-3`,
- `max B_phiD = 2.1751970101664304e-3`,
- `max B_psiD = 2.175294393662142e-3`.

Thus the metric and matter fractional memory tangents agree to substantially better than the locked 1% strict bound over the held-out scale set.

The separate metric potentials also passed the slip-invariance test on all seven scales:

- `max B_slip = 5.583079362950966e-5`.

Hence the first-order memory response is not produced by a cancellation between substantially different `phi` and `psi` responses. Instead, `phi` and `psi` themselves follow the same fractional tangent to high precision.

At late time (`z=0.2`) the direct physical `eta=0.01` tangents grow smoothly with scale. Representative values are:

- `k_h=0.10000`: `T_D ≈ 1.85475e-9`, `T_phi ≈ 1.85510e-9`, `T_psi ≈ 1.85512e-9`, `T_W ≈ 1.85510e-9`;
- `k_h=0.19875`: `T_D ≈ 5.00745e-8`, `T_phi ≈ 5.00750e-8`, `T_psi ≈ 5.00750e-8`, `T_W ≈ 5.00750e-8`.

All seven scales passed the preregistered late-time activation test.

## Interpretation

R4 certifies a stable-AeST single-amplitude scalar response in the locked `tau H0=10` regime:

`d_eta ln d_m ≈ d_eta ln phi ≈ d_eta ln psi ≈ d_eta ln(phi+psi)`

within the registered tolerance across the seven held-out scales.

Combined with R2e and R3, this explains the previously observed growth–Weyl common mode as a coherent scalar-amplitude response rather than an accidental Weyl cancellation.

The result does **not** license a positive growth–Weyl separation, an observational detection, or a universal theorem outside the tested stable-AeST regime. Observable projection is licensed as the next step.

## Historical integrity

Earlier R2/R2a/R2b/R2c/R2d classifications remain unchanged. The R2b/R2c/R2d normalization mismatch history is preserved as the result of the then-current diagnostic double-hook implementation and is not retroactively reclassified.
