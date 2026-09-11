# D2C6F-R2 local run

This stage recertifies the direct gravitational stress after replacing the old positive spectral `|d_x| z_j` bath-vector reconstruction by the local-action signed derivative `d_x z_j`.

It does not alter D2C6D/E retained finite-memory dynamics and it does not run an observational likelihood.

Run from the repository root:

```bash
bash nl1c6d2c6f_r2/run_local.sh
```

The runner reuses `.local/d2c6e_venv` and the existing zero-safe CLASS build when available. It does not use GitHub Actions.

Expected outputs:

- `results/nl1c6d2c6f_r2_vector_phase_direct_source.log`
- `results/nl1c6d2c6f_r2_vector_phase_direct_source.json`
- `results/nl1c6d2c6f_r2_local_bundle.zip`

The run evaluates the corrected source for all 27 completion members at `eta=0.125` with direct bath 256. Direct-512, doubled-time and doubled-space controls are restricted to the three preregistered sentinels. It also reports a one-way Newtonian-gauge metric projection as a non-gating physics diagnostic.

Only a formal R2 PASS re-licenses the separately preregistered self-consistent metric-feedback stage.
