# R9b DESI DR1 ShapeFit implementation audit — pre-result

Date: 2026-09-15
Branch: `fullj-evolving-weyl-bridge`

Science preregistration: `f19f7ddb85ee37d86a516ebdf41d73b96aef311e`.

Pre-result nuisance-repair lock: `76f2a9002b9fde5e568670d3ea2f638f999cef74`.

Implementation head audited: `d7ea7f50b8f412ebb616b4e2608f67c89295d9c9`.

No R9b DESI result had been executed or inspected before this audit.

`git compare 76f2a900...d7ea7f50...` contains exactly two added files:

1. `fullj_weyl/stable_aest_desi_dr1_r9b_shapefit_projection.py`;
2. `fullj_weyl/run_local_stable_aest_desi_dr1_r9b_shapefit_projection.sh`.

No preregistration, parent result, historical classification, tau grid, eta interval, gate threshold, or previous post-data file was modified after the repair lock.

The runner pins:

- official DESI Key Project likelihood repository commit `7d51f4f86dc3bee6bf10f1a684913c943a89a844`;
- `lsstypes` commit `53f048e610bcb008548f66822b0879ce9df58cb1`;
- `cosmoprimo` commit `2e59c963c9b8e7cba1a4c8f161e978c6f4d80c2d`;
- official DESI DR1 v1.0 likelihood download through the pinned repository's `dr1/cobaya/download.py`.

The runner performs a fresh DESI likelihood download, records SHA-256 hashes for the six ShapeFit HDF5 files used, rebuilds a disposable stable-AeST CLASS source from the frozen parent, removes exactly one dormant historical external tangent hook, applies the certified live-epoch physical closure with `full` mode, and then evaluates the R9b driver.

The initial per-bin nuisance design from the first preregistration is not implemented. The explicitly preregistered repair is implemented: exactly one global `df` scale nuisance and one global `dm` offset nuisance across all six bins.

This audit freezes the implementation before the first R9b data result.
