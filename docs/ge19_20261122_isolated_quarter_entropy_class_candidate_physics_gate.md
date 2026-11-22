# GE19 — isolated original-action CLASS repair stage: quarter-source and pressureful adiabatic density, no physical GO

**22 November 2026 | code implementation checkpoint.** Instead of starting another local symbolic/numerical campaign, this is a reproducible **non-destructive source repair of an independent CLASS v3.3.4 checkout**. It addresses two source-level incompatibilities already established in the exact 11 Nov/33 Ward audit, without silently inventing the physical finite-k growing eigenmode.

**Source-staging tool:** [stage_isolated_quarter_entropy_class_candidate_20261122.py](../ge19/physics_gate/stage_isolated_quarter_entropy_class_candidate_20261122.py). Its input is the **original v019+v019j patched CLASS root**, not the unpatched official CLASS. The tool rejects anything other than the precise upstream git HEAD `e85808324f51fc694d12e3ed7439552a3c3f9540` and exact v019 and v019j source-script Git blobs. It locates *three single-occurrence C anchors*, writes only to a newly copied independent CLASS directory, validates file hashes, and refuses existing outputs, nested source/target directories, or a symlinked C source. It does not run CLASS and it must not relabel existing results.

## Precisely three source edits in new `source/perturbations.c`

1. **Quarter action, not historical half**: original v019j `E_rhs_aest -= 0.5*Q_aest*Bchi_aest;` becomes `E_rhs_aest -= 0.25*Q_aest*Bchi_aest;`. The variable `Bchi_aest` already includes `aest_eta`, and `E_rhs` is later divided by `K_B`. This exactly implements the restricted original action's `-eta Q B_chi/(4 K_B)` cosmic-time electric source.
2. **Leading synchronous adiabatic AeST density**: with `w_A(t_i)` from background, replace the inherited CDM `delta_cdm^S=(3/4)delta_gamma^S` (in the *adiabatic* branch only) by `delta_A^S=(1+w_A)(3/4)delta_gamma^S`. Leave ordinary CDM behavior unchanged when `aest_enabled=FALSE`.
3. **Corresponding Newtonian gauge transformation**: `delta_A^N = delta_A^S -3(1+w_A)mathcal H alpha` instead of the inherited dust `-3mathcal H alpha`. Again preserve the old branch exactly if `aest_enabled=FALSE`.

These three anchors were cross-checked directly against the pinned official CLASS `source/perturbations.c` (Git blob `c78fe4376d2eeebfbf4ff0cfca13b048d4513fa0`) and the v019j original patch (Git blob `14796a5ed9e6265ed6810c792a93d7328a109364`). This is **not** proof of a compilable new CLASS tree until the original researcher runs it.

## Exact researcher WSL stage (no source overwrite, no DES)

The known prior local isolated patched CLASS tree for the original forced tangent was `/home/dino/GE19_CLASS_TANGENT_v077`. If it has been moved, update `CLASS_ROOT` to the checkout containing the original historical **half-source** C patch; the staging tool will fail closed otherwise.

```bash
cd ~/aest-memory-gravity
git switch physics-first-gravitational-elasticity
git pull --ff-only origin physics-first-gravitational-elasticity
source .venv/bin/activate

CLASS_ROOT="$HOME/GE19_CLASS_TANGENT_v077"
CANDIDATE_ROOT="$HOME/GE19_CLASS_QUARTER_ENTHALPY_20261122"

set -o pipefail
python -u ge19/physics_gate/stage_isolated_quarter_entropy_class_candidate_20261122.py \
  --source-root "$CLASS_ROOT" \
  --candidate-root "$CANDIDATE_ROOT" \
  --report results/ge19_quarter_entropy_class_stage_20261122_r1.json \
  --apply 2>&1 | tee results/ge19_quarter_entropy_class_stage_20261122_r1.log
echo "EXIT=\${PIPESTATUS[0]}"
```

**Expected, if source provenance and all C anchors match:** `GE19_ISOLATED_CLASS_SOURCE_STAGE_PASS 3`, with report flags `class_compiled=false, class_executed=false, FULL_PHYSICS_GO=false, DES_detection=false`. Report and candidate path must be audited before compilation or physical evolution. An already existing candidate path intentionally fails; do not delete or overwrite it blindly.


## 22 Nov 2026 first WSL staging failure and safe correction

The researcher executed the staging command and reported:

```text
RuntimeError: EXACT_ANCHOR_original_action_quarter_force_COUNT_0
EXIT=1
```

The original script did not create the candidate or change the source because it failed during `check_source()`, before `copytree()`. This is a **C source-version mismatch**, not a physics failure and not evidence of absent AeST memory. The original code required a literal `E_rhs_aest -= 0.5*Q_aest*Bchi_aest;`; the user's local checkout apparently uses some other text. **The actual line was not included in the traceback**, so do not claim it is already quarter-normalized.

The updated source stager [now](../ge19/physics_gate/stage_isolated_quarter_entropy_class_candidate_20261122.py) recognizes **only** a single explicit `E_rhs_aest -= (0.5 or 0.25)*Q_aest*Bchi_aest;` source line, allowing harmless whitespace and a trailing // comment. If `0.5`, it stages a change to `0.25`; if `0.25`, it records `already_quarter_no_change`. The two AeST adiabatic/gauge fixes can likewise be staged or recognized if already exactly present. It **does not infer** physical correctness from arbitrary renamed or restructured C logic. Any unrecognized variant prints `SOURCE_FORCE_LINES` (or `SOURCE_DENSITY_LINES`) with the actual source and SHA before failing without making a candidate.

A simple *read-only diagnostic* when still uncertain is:
```bash
grep -nE 'E_rhs_aest|Bchi_aest|index_pt_delta_cdm' "$HOME/GE19_CLASS_TANGENT_v077/source/perturbations.c" | head -n 35
```
No destructive operations, no reapplication of old patches, no `git reset`, and no deletion of existing candidates is appropriate. If a successful preflight/candidate appears, it remains **staging only** and no physical primordial mode/transfer is certified. The next output report includes per-anchor `repair_status`.

## The three remaining physical gates

**P0 — genuine finite-k growing state:** original covariant AeST scalar+aether+multiplier Euler equations and full Einstein constraints with actual `w_A(a),c_a²(a),Q(a)`; preserve standard photons, baryons, neutrinos and the full streaming/approximation hierarchy. Current leading adiabatic state `chi=E_A=0` at order k^0 does *not* fix their independent `O(k²)` coefficients; the 42-gate pressureless-proxy mixed series is not the complete pressureful action mode. Correcting only the leading `delta_A/(1+w_A)=3delta_gamma/4` does not establish higher-order regularity.

**P1 — physically transported retarded bath:** for an *already selected* `chi_0(k,t)` source, use the original `r_j=a omega_j sqrt(w_j)q_j/k` equation and its full-background retarded history to obtain finite CLASS `q_i` and conformal `p_i`, not a forced reset `q=p=0`. The radiation-only Bessel Green formula has no licence to propagate through matter equality.

**P2 — full source/metric closure and transfer:** prove original scalar Ward, Einstein Hamiltonian/momentum/shear and all-species propagation for the new physically selected state and quarter-source; then run exactly one controlled `(T_{\delta,1},T_{W,1})(k,z)` calculation and project it to the already selected DES MagLim4 Source4/Source3 26-row covariance, with proper nuisance model. Never reuse the historical half-source `W_1` as physical memory.

**Important:** Even a successful stage followed by a successful CLASS compilation is **not** `FULL_PHYSICS_GO`. This candidate is a necessary correction to known inconsistent source terms, not the still-missing physical initial mode or observational detection. No target shape was fitted and no observed DES residuals were used.

**Classification:** `ORIGINAL_ACTION_QUARTER_AND_LEADING_ENTHALPY_IC_SOURCE_PATCH_PREPARED / FINITE_K_PRIMORDIAL_MODE_NOT_SELECTED / BATH_PAST_NOT_TRANSPORTED / PHYSICAL_TRANSFER_NOT_STARTED / DES_DETECTION_FALSE`.
