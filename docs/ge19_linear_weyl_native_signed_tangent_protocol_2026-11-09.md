# GE19 — one preregistered native linear Weyl + matter η-tangent test (no H4)

**Date:** 2026-11-09. **Branch:** `physics-first-gravitational-elasticity`. **Status:** PROGRAM + FROZEN PREDATA PREPARED, NOT EXECUTED against patched CLASS or researcher native data. No scientific PASS has been claimed.

## Why this is a different task

Frozen NL0B already supplies a retarded positive Drude bath, and `docs/gravitational_elasticity_canonical_nl0b_interpretation.md` proves its linear link to the aether/scalar. The constant-H continuum positive relaxation spectrum with a (t^{-1/2}) step tail is an **exact conditional bath-level theorem**, not automatically a sky observable. The correct bridge is via the signed *linear physical metric perturbations* and the original CLASS Einstein+AeST system, independently of the original failed H4/Z21 branch.

Past frozen results: v0.77 **PASS** for native matter state `d_m`, v0.78 **PASS** for diagnosing off-native power interpolation, and **v0.68 FAIL** for fixed-grid matter/Weyl power interpolation and affinity. Do not reinterpret v0.68 FAIL or use its power spectrum as a certified Weyl amplitude. Original Cr12ad H4 FAIL remains closed.

The original frozen code `v063/theory_response_map.py` already obtains `phi`, `psi` from CLASS native `get_transfer_and_k_and_z(output_format="class",h_units=True)` and forms `weyl=(phi+psi)/2` in Newtonian gauge. This is the **actual original CLASS transfer dictionary**. No new metric field, coupling, action or gauge definition is introduced.

## Locked predata, BEFORE execution

[`ge19/linear_weyl_native_tangent_predata_20261109.json`](../ge19/linear_weyl_native_tangent_predata_20261109.json), committed **before** code or any new numerical result at commit `51c5c3612fd2e0ea21ff1ddca16a83b198d0fe87`.

- Frozen model: original `KB=0.0665`, `tau H0=10`, `p=0`, exact `v063.START/class_params`, original pinned CLASS `e85808324f51fc694d12e3ed7439552a3c3f9540` with the historical validated AeST patches.
- Original v0.77 (R4) numerical density `k_per_decade_for_pk=80`, `k_per_decade_for_bao=560`; original `k_output_values` `0.03,0.05,0.08,0.10,0.15,0.20` h/Mpc converted to physical units.
- Original positive-Drude forcing recipe: initial patched CLASS trace plus original `v039/build_tau_forcing.py`, 512-node control and 1024-node primary, original v0.77 forcing gates `relative L2≤0.01`, `cosine≥0.9999`.
- Frozen `λ` numerical amplifications `[10,5,2.5,1.25]`, **not** finite physical `eta` values. One baseline and eight signed ± runs; zero nonlinear, finite-eta or observational fits.
- Primary native CLASS common window `0.03≤k≤0.20` h/Mpc, `0.2≤z≤1.5` on **all native nodes**, no `get_transfer(z)`, no interpolated `pk_lin`, no selection of favorable zeros.
- Signed native (W=(phi+psi)/2) and native (d_m) separately. Odd tangent (T_lambda=(W_{+lambda}-W_{-lambda})/(2lambda)), four-lambda additive mean, whole-window normalized L2 affinity (epsilon_lambda=|T_lambda-ar T|_2/|ar T|_2), even response (|W_++W_--2W_0|_2/(2|lambda||ar T|_2)). **No local division by (W), (d_m) or a power spectrum**, and no power-derived sign/phase.
- Preregistered both Weyl and matter `affinity≤0.005` and `even≤0.005`, same baseline/± native k,z exact grid tolerance and baseline native matter power source-to-Fourier closure `≤5e-5`. The signed Weyl mean must exceed `1e-12` × native baseline Weyl L2 norm before the status can say “numerically resolved”; otherwise report `UNRESOLVED`. This is a numerical definition of signal resolution, **not** observational SNR or a detection criterion.
- Original historical FAIL labels and all H4 thresholds are immutable.

## Source-locked implementation

[`ge19/linear_weyl_native_tangent_20261109.py`](../ge19/linear_weyl_native_tangent_20261109.py), prepared commit `fe6168412039870b85832af73102112468d5774b`. Exact original source Git blobs are checked against both `HEAD` and working tree; the original frozen `v019/ini/aest_exp.ini` is taken **from pinned HEAD rather than any historically lensing-modified worktree INI**. Official CLASS git HEAD must equal the original v0.77 pinned commit. The script produces **namespaced** GE19 trace/forcing plus final JSON/NPZ and does not overwrite v0.77 output. Synthetic `--self-test` exercises signed/odd/even test mathematics before any CLASS run. **Source code has not yet been run on the actual researcher WSL; report any implementation error as such, not a physics failure.**

[`ge19/run_local_linear_weyl_native_20261109.sh`](../ge19/run_local_linear_weyl_native_20261109.sh) locates an existing patched official CLASS checkout and runs the one campaign. If no patched CLASS is found, **stop before computing**; do not switch to a standard unpatched CLASS silently, because it cannot test the frozen AeST theory. GitHub Actions are NOT used.

### One pasteable WSL command

```bash
cd ~/aest-memory-gravity
git pull --ff-only
source .venv/bin/activate
bash ge19/run_local_linear_weyl_native_20261109.sh
```

If the historical patched CLASS directory is elsewhere, set e.g. `CLASS_ROOT=/absolute/path/to/class_v077` before calling the script. The runner looks in `./class_v077`, `~/class_v077`, `./class_public`, `~/class_public`, `./class`, `~/class`. If the CLASS checkout has not been installed locally, the runner gives an explicit preflight blocker; do not tell the researcher that a physical result was generated.

Expected generated files on a complete run:
```text
results/ge19_linear_weyl_native_tangent_20261109.log
results/ge19_linear_weyl_native_tangent_20261109.json
results/ge19_linear_weyl_native_tangent_20261109.npz
results/ge19_linear_weyl_native_tangent_20261109_forcing_*.dat/json/log
```

### Strict classifications

- `GE19_LINEAR_WEYL_NATIVE_SIGNED_TANGENT_NUMERICAL_PASS_OBSERVATIONAL_OPEN`: original-model native signed Weyl transfer tangent demonstrated as nonzero and `λ`-stable in the locked window; **NOT a lensing spectrum or detection**.
- `GE19_LINEAR_WEYL_NATIVE_TANGENT_UNRESOLVED`: transfer tangent passes stability criteria but lies under frozen numerical-resolution amplitude floor.
- `GE19_LINEAR_WEYL_NATIVE_SIGNED_TANGENT_NUMERICAL_FAIL`: actual original forcing passes but a preregistered original-model numerical state gate fails. Preserve FAIL; no retrospective threshold changes.
- Missing patched CLASS, missing parents, source hash mismatch, or aborted run: implementation/resource issue, **not** a physics verdict.

## What a PASS would license, and what it would not

A PASS would justify a **new, separately frozen first-principles linear line-of-sight lensing/ISW response calculation** based on the CLASS native signed Weyl transfer, with explicit projection kernels, foreground selection functions, covariances and predeclared observed data **before looking at measurements**. It would not by itself prove nonlinear (Z_{21}), a measured lensing modification or gravitational-memory detection. Distinguish bath-level constant-H (t^{-1/2}) theory from realistic evolving (H(t)) transfer. Do not tune (	au), (K_B), (eta) or initial conditions to force the observer gate.

**This is ONE new linear-science numerical test, not further H4 numerical repair.** If no patched CLASS is available or the run fails a frozen gate, stop and document what was learned rather than create a sequence of 50 small repairs.
