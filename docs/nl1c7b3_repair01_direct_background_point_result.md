# NL1C7B3 Repair01 — direct background-point reconciliation result

Status: **OFFICIAL RESULT / FROZEN**

Classification:

`NL1C7B3_REPAIR01_DIRECT_BACKGROUND_POINT_PASS`

## Provenance

- official run: `35196289353`
- workflow head: `03b8f454ed8749dcfb8185647bd78d85b3728578`
- pinned CLASS: `e85808324f51fc694d12e3ed7439552a3c3f9540`
- historical B3 parent run: `35195633648`
- historical B3 result freeze: `4fb8679f84585c4008008d7043ac0b5f4ca33eeb`
- Repair01 preregistration: `58a5dc4d22fe83d8b2eadae35a313050e6c7df43`
- Repair01 implementation lock: `287e7fa8b6e1f315e5978e17c2f8f4bdb92046aa`
- artifact: `10486515383`
- artifact SHA256: `12f3157fa05e7c0c4fc431005a506cbfa6347aa78dafd1a1dedf4328b193d3ec`

## Result

All preregistered Repair01 gates pass. All homogeneous components are evaluated on the same direct CLASS background point at `a_i=0.02` (`z_i=49`) without fitting a remainder.

The direct C6-normalized components are

- `3 H^2 = 0.006048695270400684 Mpc^-2`,
- `rhoA_C6 = 0.005009723008430343 Mpc^-2`,
- `varrho_b = 0.0009336821113982245 Mpc^-2`,
- `rho_std_C6 = 0.00010529015057211754 Mpc^-2`.

The full homogeneous closure error is

`epsilon_direct = 1.3891536043947618e-16`,

against the frozen limit `1e-7`. The independent CLASS density-sum relative error is `2.1509475164822117e-16`. The direct baryon normalization agrees with the frozen baryon normalization to `4.644845003453563e-16` relative error.

The source-declared standard sector at `z=49` consists of photons, ultra-relativistic species, one non-cold species, and the cosmological constant. Their fractions of the standard-sector density are approximately `0.4899960705`, `0.2276823443`, `0.2813380262`, and `0.0009835590`, respectively. The exported CLASS `rho_tot` column is an aggregate diagnostic and is not treated as an independent species.

## Interpretation

The historical B3 failure is retained. It arose from mixing retained/source-trace quantities with an interpolated exported background table and from treating `rho_tot` as if it were an additional species. The common direct-point evaluation removes that representation mismatch without changing the cosmological model, the physical sector sum, solver tolerances, or the `1e-7` homogeneous-closure threshold.

Therefore the eta=0 homogeneous background entering the spherical program is now reconciled to machine precision using AeST, baryonic dust, photons, ultra-relativistic species, non-cold matter, and Lambda already present in the frozen CLASS model.

## Claim boundary

This result certifies homogeneous background reconciliation only. It does **not** certify the radial Hamiltonian or radial momentum constraints, does not project or modify the C7A growing-mode initial state, and does not execute nonlinear spherical evolution, turnaround, collapse, or finite-memory dynamics. A separate pre-result checkpoint is required before any trajectory is licensed.