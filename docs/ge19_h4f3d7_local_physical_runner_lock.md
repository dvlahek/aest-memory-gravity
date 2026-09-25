# GE19 H4F3d7 — locked LOCAL PHYSICAL R1 ODE versus sampled FD4 runner

## Result of this lock

**Classification: `GE19_H4F3D7_PHYSICAL_LOCAL_RUNNER_STATIC_PASS_PHYSICAL_OPEN`.**

The dedicated GitHub Actions [static audit 36150787708](https://github.com/dvlahek/aest-memory-gravity/actions/runs/36150787708), job `108123212034`, completed **success** on 25 September 2026. This is a static Bash/Python-heredoc/provenance/isolation audit. It has **not** executed the original H4F3b/H4F3d6 physical binaries or made a bath-on-shell, all-parent H4 Noether or Z21 claim.

Locked immutable inputs:

- runner `ge19/run_local_h4f3d7_physical_r1_fd4_vs_interval_ode.sh`, Git blob `6fe12ef99f9a469da8f5913121d3301df519aae2`, initial commit `a6e1137b7d8e74c82466d98540c733aa72e1241f`;
- dedicated static workflow `.github/workflows/ge19-h4f3d7-physical-local-runner-static.yml`, blob `632aefa190722ad273beca15f3743c941a866372`, commit `fe69d9d834fbb21e8543febc25e8097794245a8d`;
- frozen H4F3d7 original R1/FD4 implementation `ge19/h4f3d7_bath_fd4_vs_original_r1_interval_ode.py`, blob `b598a5cc49b3d87827b4758c55d3ce7f3a1198a8`;
- H4F3d7 preregistration blob `ccf3185b4f790d9d6068f80beb39a442b186158c`;
- original H4F3d7 manufactured/compiler PASS [run 36148151670](https://github.com/dvlahek/aest-memory-gravity/actions/runs/36148151670) remains separately classified `GE19_H4F3D7_FROZEN_ODE_FD4_COMPILER_PASS_PHYSICAL_OPEN`.

## Exact physical input contract

The script reads `$ROOT/results` and requires the original certified bytes:

| File | SHA-256 |
| --- | --- |
| H4F3b actual corrected six-source JSON | `1ec88fd3fd6b81bf30614b0cb78d722a02dd4f745e1f22cb9b8f956a44bac6c1` |
| H4F3b actual corrected six-source NPZ | `787d5d177838b05078057aa932f379dd529449ce203f5664c36cf723acb0116b` |
| H4F3d6 actual bath-parent JSON | `4607edde17c6820c85f32c0bbd774d5a58148eb01bfd0c81ce592e8c1b907791` |
| H4F3d6 actual bath-parent NPZ | `17b50c6ee584b2a8886f7114a90ea9396a127172dd9e02976b0e6275fe2fedc0` |
| Original Repair26 R1 full-history trace, exactly 26,643,162 bytes | `608ee0b4c868a701db6976f756b9a551cd9ddffe1e8e4ab37c5cd2361405a6f8` |

The runner calls the existing frozen H4F3b `s.frozen_inputs(rd, trace)` to check original certified H3F Z20 JSON/NPZ, H3G q20 JSON/NPZ, Repair32B Z11 NPZ and Repair32C certification JSON, Repair13 background NPZ and GE15 dense trace against their **existing** original immutable SHA-256 values. The missing original Z11 binary is never manufactured or regenerated. The original Repair26 R1 trace is accepted only with exact hash and byte count.

**Side-effect isolation:** no historical Python generator is imported before entering a fresh `mktemp -d` working directory with its own `results/`. The runner uses an absolute `PYTHONPATH`, disables Python bytecode writes, uses absolute physical input and output paths, and deletes only its own isolated temporary directory. It refuses to overwrite any existing H4F3d7 physical JSON, NPZ or FULL log. The project's `.venv` is activated if it was not already active.

## Exact physical invocation

From the original scientific local checkout, with all exact files restored in `results/`:

```bash
cd ~/aest-memory-gravity
git checkout physics-first-gravitational-elasticity
git pull --ff-only
source .venv/bin/activate
# Only if the original R1 trace is not in results/ or frozen_repair26_repair27/:
# export GE19_REPAIR26_R1_TRACE=/absolute/path/to/ge19_repair26_R1_full_history_trace.dat
bash ge19/run_local_h4f3d7_physical_r1_fd4_vs_interval_ode.sh
```

The distinct physical outputs are `results/ge19_h4f3d7_physical_r1_fd4_vs_interval_ode.json`, `.npz`, and `_FULL.log`. After the physical run, preserve and independently hash all three before issuing any physical result freeze.

## Registered claim boundary

The unchanged physical CLI compares the sampled original GE05 `R_FD4` with **both original interval sides** of `R_ODE + D_FD4` at all available interior/end nodes, the full original 2048 R1 quadrature nodes, positive modes 3/5/8/10/15/20, all six C × Nt bath paths and the three preregistered beta duplicate views. All original fixed phase bins remain. It reproduces H4F3d6's original reported absolute Euler norm within the preregistered relative `1e-10` bound, and keeps the original algebraic `1e-11` identity control. No frequency exclusion, source fit, clock fit, altered FD4, original ODE modification or new on-shell smallness threshold is permitted.

The signed nonbath background/H1/Z11/H3F/H3G/GE06/GE07/Lambda/Y Euler parents, action boundary, canonical operator and independently preregistered FD4/FD8 structural error budget remain open. No full physical H4 Noether PASS, Z21 certification or lensing license follows from this static runner audit. Historical Repair22/27/32 classifications, Repair37 SCIENCE_FAIL and Repair38–44 diagnostics remain immutable; active-shift `1e-6` and temporal order `>=2.5` remain unchanged.
