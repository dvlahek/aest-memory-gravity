# D2C6H local run

D2C6H is the final preregistered numerical/theory certification step before returning to cosmological observables and observational likelihoods.

It keeps the physical trajectory at eta=0 and closes the longitudinal memory-metric tangent loop in the certified nonlinear box:

`memory tangent -> corrected direct memory metric source -> delta Psi -> v_alpha'=a(v_E-v_Psi) -> memory tangent`.

The physical eta=0 direct source remains exactly zero; the unit-eta source is only the coefficient dT_mem/deta|0.

Frozen setup:

- 27 completion members;
- direct tan-GL bath order 256 primary;
- direct order 512 on three frozen sentinels;
- Nx=128, 4096 main steps;
- same CLASS/background/modes/box/checkpoints as D2C6G;
- no likelihoods and no physical finite-eta run.

Run locally:

```bash
cd ~/aest-memory-gravity
git pull
bash nl1c6d2c6h/run_local.sh
```

Outputs:

- `results/nl1c6d2c6h_final_self_consistent_metric_feedback_tangent.log`
- `results/nl1c6d2c6h_final_self_consistent_metric_feedback_tangent.json`
- `results/nl1c6d2c6h_local_bundle.zip`

PASS classification:

`NL1C6D2C6H_FINAL_SELF_CONSISTENT_METRIC_FEEDBACK_TANGENT_PASS`

On PASS the code prints:

`OBSERVATIONAL_IMPLEMENTATION_STEP_LICENSED=True`

and

`FURTHER_INTERMEDIATE_NUMERICAL_BRIDGE_PREREGISTERED=False`.

A PASS returns the project to observables/likelihood implementation. It is not a claim of arbitrary-amplitude fully nonlinear GR/AeST.
