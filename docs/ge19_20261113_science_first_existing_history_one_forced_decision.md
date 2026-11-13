# GE19 — Science-first decision after full primordial CLASS baseline and null

Date: 2026-11-13. Branch: physics-first-gravitational-elasticity.

**Decision: ONE final predeclared forced-tangent screening pass from the EXISTING completed primordial history. NO restart of the expensive baseline, NO eta/parameter sweep, and NO additional automatic engineering campaign.**

## Original WSL evidence

[Exact researcher inspection log](../results/ge19_existing_traces_inspection_20261113.log) confirms:
- Source-locked full-class patch preflight PASS.
- 141,494 accepted dense baseline history records; a_min = 2.251984948309577e-6, a_max = 1, conformal-time range 1.0417779584818918 to 14150.279922065203 Mpc.
- Baseline W0(z=0.5,k=0.1 h/Mpc) = 0.07009097715416947 in CLASS's native primordial-transfer normalization. This is NOT a predicted memory signal and not an observable detection.
- Independently completed null-source CLASS process wrote 13 sparse W readouts on a=0.4..1; every recorded null W equals exactly zero; null W(z=0.5) = 0. The null test does not establish constraint preservation at early times or prove linearization of all approximation transitions.
- There is NOT YET any forced eta tangent W1. No eta-to-Weyl physical gain, no DES detection.
- The mere existence of the baseline deep into radiation era does not verify the *physical NLO adiabatic initial conditions*, action/Ward equivalence, the source normalization, or the independent stability of W1.

## One last rational diagnostic

The already saved `baseline_dt010.csv` is sufficient to construct a direct eta source Bchi0(tau,k), provided it is nonzero and finite. The exact-zero null trace permits a fast initial homogeneous-system control. There is no justification to repeat the whole five-pass batch before seeing even one forced response.

[Single-execution direct tangent continuation](../ge19/physics_gate/one_forced_tangent_from_existing_history_20261113.py):
- Imports the existing source-locked full CLASS runner utilities and reads already accepted WSL `base010` and `null` results.
- Requires full baseline early/late history, finite monotonic k, target z=0.5 coverage, strictly separated new output directory, source-locked original Exp input and CLASS patch, tiny homogeneous null and a nonzero finite Bchi0. If the source is identically zero, it stops **before running CLASS**.
- Invokes **one** existing, compiled, pinned native CLASS binary in force mode at frozen k = 0.06732117 Mpc^-1, eta=0, original cosmology and adiabatic initial state, forced only by the original recorded Bchi0.
- Saves W1(z=0.5) and W1/W0 per unit eta, source and null checksums and a JSON with **explicit physical/numerical uncertified flags**. No finite-eta subtraction, no CLASS recomputation of the 141,494-row history.
- **Does not** claim convergence from a single forced pass, nor certify Einstein/Ward constraints, primordial NLO state or DES. A single nonzero computed W1 is a candidate, not a discovery.

### One local WSL command

```bash
cd ~/aest-memory-gravity
git pull --ff-only
source .venv/bin/activate

set -o pipefail
python3 -u ge19/physics_gate/one_forced_tangent_from_existing_history_20261113.py \
  --class-root "$HOME/GE19_CLASS_TANGENT_v077" \
  --original-ini "$PWD/v019/ini/aest_exp.ini" \
  --existing-dir "$PWD/results/ge19_full_class_direct_tangent_20261113_r2" \
  --out-dir "$PWD/results/ge19_one_forced_tangent_20261113" \
  2>&1 | tee results/ge19_one_forced_tangent_20261113_runner.log
rc=${PIPESTATUS[0]}
echo "FORCE_EXIT=$rc"
```

If the forced run fails, **STOP** and preserve `results/ge19_one_forced_tangent_20261113/force_single.log`. Diagnose the first reason rather than launching another numerical sweep or changing eta.

If it succeeds, report the actual Bchi0 amplitude, W0, W1 and W1/W0 and discuss whether the projected Weyl channel justifies the substantial independent physicist-level action/IC/Ward/convergence investment. The result alone cannot yield a detectability bound, non-detection, or experimental significance.

**Research decision gate: only proceed to a separate, rigorously verified physical observability calculation if a meaningful, numerically resolvable candidate exists and we can establish action/primordial equivalence. Otherwise archive this GE19 observational branch as exploratory and prioritize a publishable theoretical memory paper.**
