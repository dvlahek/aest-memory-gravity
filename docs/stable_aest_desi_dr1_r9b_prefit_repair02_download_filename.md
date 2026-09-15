# Stable-AeST DESI DR1 R9b — pre-result technical repair 02

## Status of first execution

The first R9b execution stopped before any CLASS theory run or DESI memory-likelihood result was produced. The official DESI downloader completed successfully and downloaded 67 likelihood products, including the six requested ShapeFit HDF5 files. The local filenames preserve URL encoding for the `+` character as `%2B`, while the R9b runner/driver expected the decoded `+` spelling. The run therefore stopped at the required-file existence check.

This is a technical pre-result infrastructure failure. It is not a science classification and does not modify or reclassify any previous R7/R8/R9 result.

## Frozen repair

Before rerunning, modify only the R9b runner to canonicalize downloaded DESI likelihood filenames by renaming `%2B` to `+` immediately after the official `download.py` completes and before the required-HDF5/hash manifest checks.

No changes are permitted to:

- DESI repository commit `7d51f4f86dc3bee6bf10f1a684913c943a89a844`;
- the official DESI download source or HDF5 file contents;
- R9b tracer selection, redshift bins, ShapeFit observable definition, or covariance use;
- tau grid `10, 5, 2.5, 1.25`;
- eta derivative points `0, ±0.025, ±0.05`;
- physical eta interval `[0, 0.05]`;
- global nuisance design (`global_df_scale`, `global_dm_offset`);
- derivative, likelihood, matched-filter, GLS, or certification gates;
- stable-AeST equations or source topology.

The rename must preserve file bytes. SHA-256 hashes are computed only after canonicalization, so the manifest continues to fingerprint the exact downloaded DESI products.

## Interpretation lock

A successful rerun licenses only the preregistered R9b DESI DR1 ShapeFit memory projection. It does not by itself license an observational detection or a modified-gravity full-shape claim.
