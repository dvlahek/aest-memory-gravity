# D2C6E local larger-eta scan

This stage is intentionally local-only. No GitHub Actions workflow is provided.

The preregistered physical positive eta ladder is fixed to:

- 0.03125
- 0.0625
- 0.125

Do not edit the eta values, gates, completion ensemble, or resolutions before the first result.

## Run

From an existing clone of `dvlahek/aest-memory-gravity`:

```bash
git checkout v053-exp-normalization-corrected
git pull
bash nl1c6d2c6e/run_local.sh
```

The runner automatically reuses a valid local zero-safe CLASS build. If none exists, it builds one first.

## Outputs

The run writes:

- `results/nl1c6d2c6e_larger_eta_retained.log`
- `results/nl1c6d2c6e_larger_eta_retained.json`
- `results/nl1c6d2c6e_local_bundle.zip`

Send `results/nl1c6d2c6e_local_bundle.zip` back for analysis.

Exit code 0 means the preregistered E1--E7 certification gates all passed. Exit code 2 means a scientific/numerical gate failed. Exit code 3 means the run was technically incomplete. The ZIP is produced for all three cases so the result can be audited without rerunning or changing the preregistered test.

The tangent remainder, dyadic quotient changes, 1% visible-nonlinearity onset, and 5% strong-departure onset are diagnostic only and do not affect PASS/FAIL.
