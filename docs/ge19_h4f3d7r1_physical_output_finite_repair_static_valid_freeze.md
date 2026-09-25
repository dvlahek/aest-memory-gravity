# GE19 H4F3d7r1 — exact single-expression physical output finiteness implementation repair

## Original observed implementation failure

The user-supplied original local physical
`ge19_h4f3d7_physical_r1_fd4_vs_interval_ode_FULL.log` ended
with an `AttributeError: 'list' object has no attribute 'values'`
in the original H4F3d7 `physical_run` final `valid` gate
(lines 422–423 of the frozen source). It attempted
`stored.values()` after constructing `stored` as a Python list
of all arrays in `outputs`.

This is an **IMPLEMENTATION_FAIL** after reaching the physical
runner's final completion check, not a failed R1 bath science gate.
There is no original physical result JSON/NPZ or verified scientific
decomposition to classify from the uploaded traceback alone.
The earlier original [H4F3d7 manufactured compiler PASS
36148151670](https://github.com/dvlahek/aest-memory-gravity/actions/runs/36148151670)
is separately immutable and does not test this physical branch.

## Versioned exact one-expression repair

**Current classification:
`GE19_H4F3D7R1_EXACT_SINGLE_FINITE_GATE_REPAIR_STATIC_PASS_PHYSICAL_OPEN`.**

- Immutable original H4F3d7 implementation:
  `ge19/h4f3d7_bath_fd4_vs_original_r1_interval_ode.py`,
  original Git blob
  `b598a5cc49b3d87827b4758c55d3ce7f3a1198a8`.
- Immutable original physical runner:
  `ge19/run_local_h4f3d7_physical_r1_fd4_vs_interval_ode.sh`,
  blob `6fe12ef99f9a469da8f5913121d3301df519aae2`.
- Immutable original preregistration:
  `ge19/h4f3d7_predata_bath_fd4_vs_original_r1_interval_ode.json`,
  blob `ccf3185b4f790d9d6068f80beb39a442b186158c`.
- Versioned implementation-repair preregistration:
  `ge19/h4f3d7r1_predata_physical_output_finite_check_repair.json`,
  blob `f404c1b910e9dbcb342fbc4d3403fb83108697f7`.
- Versioned repaired physical module:
  `ge19/h4f3d7r1_physical_output_finite_check_repair.py`,
  blob `e4cb9d6638b427368647a29b86ccf5445b43d7a2`.
- Versioned hash-locked, temp-isolated, no-overwrite runner:
  `ge19/run_local_h4f3d7r1_physical_output_finite_check_repair.sh`,
  blob `6bdee189cf795a04e4d1b19822af6ed778b5af46`.
- Regression workflow:
  `.github/workflows/ge19-h4f3d7r1-physical-finite-output-repair-static.yml`,
  final blob `f0452ff9667e734bd39d45c692020ebe49e913eb`.
- Dedicated [GitHub Actions 36153973088](https://github.com/dvlahek/aest-memory-gravity/actions/runs/36153973088),
  job `108133895719`, completed **success**.
  Exact-terminal marker:
  `GE19_H4F3D7R1_EXACT_SINGLE_FINITE_GATE_REPAIR_STATIC_PASS_PHYSICAL_OPEN`.

The regression CI proves that the new Python source is *exactly*
the original immutable 22-kB source with this single final `valid`
expression replaced:

```python
valid=bool(len(cases)==6 and all(v["pass"] for v in cases)
           and all(np.isfinite(arr).all()
                   for arr in outputs.values()))
```

Every original source term, ODE, FD4 stencil, one-sided interval
classification, output content, phase bin, node, frequency and
original threshold remains unchanged. The workflow extracts
the **actual new physical `valid` AST expression** without
running/manufacturing physical parents and tests that six passing
cases plus finite stored arrays are accepted and that NaN, plus
or minus infinity in *any* stored array, a missing case or a
failed case is rejected. It checks immutable Git source blobs,
both runner Bash syntax and inline Python, worktree isolation,
actual original parent-hash preflight and distinct result names.

The first regression workflow
[36153886957](https://github.com/dvlahek/aest-memory-gravity/actions/runs/36153886957)
failed on YAML heredoc indentation in its static test fixture.
Only the regression workflow fixture was corrected; the physical
repair source and versioned runner were never altered after their
initial exact single-expression commits. Only subsequent
run `36153973088` is static-PASS.

## Exact local physical rerun and artifact boundary

Run only from the scientific local checkout with the exact
original certified H4F3b/H4F3d6/H3F/H3G/Repair32B Z11/
Repair32C/Repair13/Repair26 R1 source bytes. The existing
versioned runner automatically preflights every frozen hash,
activates the project's venv when available, moves into an
isolated temporary working directory **before** historical
generator imports, and uses absolute file paths.

```bash
cd ~/aest-memory-gravity
git checkout physics-first-gravitational-elasticity
git pull --ff-only
source .venv/bin/activate
set -o pipefail
bash ge19/run_local_h4f3d7r1_physical_output_finite_check_repair.sh \
  2>&1 | tee results/ge19_H4F3D7R1_LOCAL_runner.log
echo "EXIT=${PIPESTATUS[0]}"
```

The original failed `ge19_h4f3d7_physical_r1_fd4_vs_interval_ode_FULL.log`
remains untouched. New versioned physical outputs, if execution
reaches its completed write, are

- `results/ge19_h4f3d7r1_physical_r1_fd4_vs_interval_ode.json`;
- `results/ge19_h4f3d7r1_physical_r1_fd4_vs_interval_ode.npz`;
- `results/ge19_h4f3d7r1_physical_r1_fd4_vs_interval_ode_FULL.log`.

Independently verify JSON/NPZ/FULL/runner-log bytes and hashes,
original six case gates, both original interval sides and all
phase bins before freezing any *physical* outcome.
A compiler/static PASS is not a physical bath on-shell PASS.
The original H4F3d6 near-unit sampled GE05 bath Euler
remains an open diagnostic until this real physical
R1/FD4 decomposition is evaluated.

No new on-shell smallness gate; no source fitting; no
old Repair22/27/32, Repair37 SCIENCE_FAIL or Repair38–44
relabel; unchanged original active shift `1e-6` and
matched time order `>=2.5`.
**Full actual H4 Noether NOT CERTIFIED; Z21 NOT CERTIFIED;
lensing blocked.**
