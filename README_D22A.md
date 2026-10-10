# GE19 D22A — real D17/D19R1 dependent parent numerical reclosure

This package builds **new** C_star/Nt128 source-locked numerical candidates for `B10`, `Z11`, and `Z20` from actual D17 original-action canonical H1 and actual D19R1 physical bath. D20R1 and D21R1 actual archives are used for provenance and guardrails, **not** to reuse their old M1 source. `Z11` retains frozen R2 eta dynamic initial conditions; `Z20` gets a fresh source-aware Repair18 projected momentum initial condition. Full original H4/Z21 and q20 remain open.

All requirements are already in the repository/environment used to execute D21R1. Do **not** run this new script before copying its ZIP into the repository root. With WSL open, from `~/aest-memory-gravity`:

```bash
unzip -n ge19_h4f3d22a_original_action_parent_candidates_package.zip \
  'ge19/*' 'docs/*' D22A_SOURCE_MANIFEST.json README_D22A.md
source .venv/bin/activate
mkdir -p results
set -o pipefail
bash ge19/run_local_h4f3d22a_action_parent_reclosure.sh \
  2>&1 | tee results/ge19_H4F3D22A_LOCAL_runner.log
echo "EXIT=${PIPESTATUS[0]}"
```

Runner checks branch and SHA, makes a new isolated temp CWD, prints progress at each Z20 mode group, and never overwrites an existing JSON/NPZ/log. If Repair26 trace cannot be found, set `GE19_REPAIR26_R1_TRACE=/absolute/path/to/ge19_repair26_R1_full_history_trace.dat` before running. Runtime heavy symbolic generators may pause before `GE19_D22A_NEW_B10...`; parent SHA and subsequent mode progress remain printed. No asynchronous work is being promised.

Successful output files in `results/`:

* `ge19_h4f3d22a_actual_Cstar_action_B10_Z11_Z20_parent_candidates.json`
* `ge19_h4f3d22a_actual_Cstar_action_B10_Z11_Z20_parent_candidates.npz`
* `ge19_h4f3d22a_actual_Cstar_action_B10_Z11_Z20_parent_candidates_FULL.log`
* `ge19_H4F3D22A_LOCAL_runner.log` (from your outer tee)

Upload the four files for independent archive/physical audit. A diagnostic/numerical candidate PASS is not Z11/Z20 continuum certification or full H4. The next stage is D22B new q20 and B20 with D19R1 full bath and a phase-resolved GE05 second-order current test; it must not silently fall back to H3G q20.
