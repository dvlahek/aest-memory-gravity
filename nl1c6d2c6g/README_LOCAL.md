# D2C6G local run

This stage calibrates the corrected direct-memory metric tangent on the certified eta=0 nonlinear trajectories. It does **not** close the feedback loop and does not use observational data.

Run locally:

```bash
cd ~/aest-memory-gravity
git pull
bash nl1c6d2c6g/run_local.sh
```

The runner reuses the existing `.local/d2c6e_venv` and zero-safe CLASS build when available. It creates no GitHub Actions workflow.

Outputs:

```text
results/nl1c6d2c6g_eta0_metric_tangent_calibration.log
results/nl1c6d2c6g_eta0_metric_tangent_calibration.json
results/nl1c6d2c6g_local_bundle.zip
```

A PASS reports `FEEDBACK_ETA_CAP_1PCT_BASE_PSI` and the preregistered feedback ladder `{cap/4, cap/2, cap}`. The cap is the most conservative eta over all 27 completion members and all nine checkpoints for which the one-way eta=0 metric tangent reaches 1% of the frozen CLASS baseline `Psi` RMS.

Expected PASS label:

```text
NL1C6D2C6G_ETA0_DIRECT_METRIC_TANGENT_CALIBRATION_PASS
```

A PASS licenses only a separately preregistered self-consistent feedback run on the reported ladder. It does not license an observational likelihood.
