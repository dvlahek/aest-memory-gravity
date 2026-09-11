# ACT DR6 lensing exploratory local run

This stage evaluates the official ACT DR6 `act_baseline` standalone lensing likelihood on the fixed AeST+memory eta grid declared in `docs/obs_act_dr6_lensing_exploratory_scope.md`.

Historical D2C6H remains a formal FAIL. Therefore this run is exploratory and does not license a detection, posterior constraint, or final observational claim.

The linear CLASS calculation includes the physical finite-eta scalar-current memory closure with `tau H0=1` and bath order 39. The corrected R2/H direct metric stress is quadratic in perturbations and is not inserted as a first-order CLASS stress source.

Run locally:

```bash
cd ~/aest-memory-gravity
git pull
bash obs_act_dr6_lensing/run_local.sh
```

The runner uses/rebuilds the pinned zero-safe AeST+memory CLASS, installs `act_dr6_lenslike==1.2.1`, downloads the official likelihood data version `v1.2` through the likelihood package, checks the eta=0 memory-on/off lensing regression, and evaluates

```text
eta = 0, 1/256, 1/128, 1/64, 1/32, 1/16, 1/8
```

Outputs:

```text
results/act_dr6_lensing_exploratory.log
results/act_dr6_lensing_exploratory.json
results/act_dr6_lensing_exploratory.npz
results/act_dr6_lensing_exploratory_bundle.zip
```

Send `act_dr6_lensing_exploratory_bundle.zip` back for interpretation.

Successful execution is labeled

`ACT_DR6_LENSING_EXPLORATORY_SCAN_COMPLETE`.
