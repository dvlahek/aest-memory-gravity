# IMPORTANT PROJECT HISTORY

This file is the durable continuation checkpoint for the AeST memory-gravity project. Read this before reopening the DESI direct-velocity / ShapeFit chain.

## 2026-09-15 — R9b2k native-k density breakthrough

**IMPORTANT: do not restart the investigation from R9b/R9b2/R9b2j. The main native-response numerical problem is already localized and closed.**

### What is now established

- Historical R9b2j remains `STABLE_AEST_DESI_DR1_R9B2J_CROSS_OPERATOR_FAIL` on the 108-node native CLASS grid.
- R9b2k increased the *actual solver grid*, not merely an interpolation grid:
  - historical default: 108 native k nodes
  - D1 `(k_per_decade_for_pk,k_per_decade_for_bao)=(80,560)`: 864 native k nodes
  - D2 `(160,1120)`: 1729 native k nodes.
- Every R9b2k Stage-A gate K1-K6 passed.
- D1 -> D2 response convergence passed.
- D2 epsilon consistency passed.
- D2 linear-vs-PCHIP signed-response agreement passed for every tau and both epsilon values.
- Typical D2 cross-operator values are E about 9.3e-4 and C about 0.999999991.
- Therefore the large R9b2j linear/PCHIP disagreement was caused by insufficient native CLASS k sampling at 108 nodes, not by an intrinsic physical instability of the source response.

### What failed next

R9b2k proceeded into DESI Stage B. Official DESI provenance passed, but the ShapeFit theory vector failed finiteness.

The failure is exactly localized:

- `qiso`: finite
- `qap`: finite
- `df`: finite
- `dm`: NaN in all six DESI bins

Thus only positions 3, 7, 11, 15, 19, 23 of the 24D vector fail.

The current adapter computes `dm = m - m_fid`, where `m` is the logarithmic slope of a BAO-smoothed bounded source-state Pdd. The adapter reused the fiducial `PowerSpectrumBAOFilter` object for source spectra. In cosmoprimo the filter's k grid is fixed at construction, while later `__call__` operations replace the input P(k) without rebuilding that k grid. This creates a support mismatch when a broad fiducial filter is called on the bounded D2 source-state Pdd and can produce non-finite smoothed values.

### Next authorized step

`R9b2k Repair01` only.

Repair requirements:

1. Do **not** rerun the 25 CLASS cases.
2. Reuse `results/stable_aest_desi_dr1_r9b2k_work/*.pkl` checkpoints.
3. Keep the R9b2k Stage-A result frozen.
4. Build one source-support peak-average BAO filter per redshift from the D2 eta=0 bounded source Pdd, with the same DESI fiducial cosmology as `cosmo_fid`.
5. Reuse that support-matched filter across eta/tau cases only after validating identical D2 k support.
6. Require finite positive smooth P(k) at the two ShapeFit pivot points before taking logarithms.
7. Preserve the exact `m`, `Ap`, `qiso/qap`, `df`, nuisance-projection, and GLS definitions.
8. Preserve all existing E/C/closure thresholds. No postdata threshold relaxation.
9. Only if repaired B2-B6 all pass may the compressed DESI projection be reported.
10. A PASS still does not license a full-EFT modified-gravity claim, a detection claim, or a tau bound.

### Frozen result identifiers

- R9b2k classification: `STABLE_AEST_DESI_DR1_R9B2K_SHAPEFIT_VECTOR_FAIL`
- R9b2k JSON SHA256: `f4323f84dfa93c5ac3ef449fbe666ce3add45a50331079fe66bd27beb2b30c7e`
- R9b2k science log SHA256: `5580e537971f38d7007eed66eb0b5ef8cb92a36583dad348d7afab07ad95d306`
- R9b2k postdata freeze commit: `dd3981b2fd838fb24a997af77f913c3d5dd8d07b`

Treat this checkpoint as high-priority project history. If future work on DESI direct velocity starts without mentioning the 108 -> 864 -> 1729 result and the six `dm` NaNs, stop and read this file first.
