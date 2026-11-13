# GE19 — Experimental full CLASS direct-tangent implementation, one fixed campaign

**12 November 2026. Status: SOURCE CODE COMMITTED; ORIGINAL CLASS STATIC ANCHORS 7/7; WSL CLASS BUILD/EXECUTION NOT PERFORMED; PHYSICS_GO=false; NO DES DETECTION.**

This is now a concrete experimental source patcher and runner, not merely a proposed calculation. The code has not been compiled against the researcher's isolated CLASS checkout or physically qualified. Do not describe this artifact as a demonstrated full CLASS Weyl result until the actual local source-locked run returns evidence.

## 13 November 2026 — first native run stopped at input_init; corrected lensing switch

The first native `run` entered `base010` then returned CLASS exit=1 before any perturbation integration or physical memory evaluation. In the user-provided `base010.log`, the decisive source error is `input_read_parameters_lensing(L:5101)`: lensed CMB Cls were requested without `tCl/pCl` and `lCl` output.

**Exact cause:** the frozen [aest_exp.ini](../v019/ini/aest_exp.ini) specifies `lensing = yes` for its original `tCl,pCl,lCl,mPk` outputs. The experimental [runner](../ge19/physics_gate/run_full_class_two_pass_tangent_20261112.py) changed `output` to `mTk` but initially failed to disable this inherited *lensed angular-spectrum output*. It is an output/input consistency issue, not an AeST equation failure.

**Corrected and committed in runner only:** every generated `mTk` ini now sets `lensing = no`; the generator independently verifies one `output = mTk`, `lensing = no`, `gauge = newtonian` and `aest_eta = 0` before invoking CLASS. The original benchmark source, native CLASS C code, primordial species, background and physical parameter inputs remain unchanged. The WSL wrapper's nested runner log now uses the basename of the selected output directory, preserving the first failure log.

**Single retry** in a fresh output directory (retain the old `base010.log` evidence); no new compile/prepare/clone:

    cd ~/aest-memory-gravity
    git pull --ff-only
    source .venv/bin/activate
    set -o pipefail
    GE19_TANGENT_OUT_DIR="$PWD/results/ge19_full_class_direct_tangent_20261113_r2" \
      bash ge19/run_local_full_class_direct_tangent_20261112.sh run \
      2>&1 | tee results/ge19_full_class_tangent_run_20261113_r2.log
    rc=${PIPESTATUS[0]}
    echo "RUN_EXIT=$rc"

**Pending:** no post-fix WSL runtime confirmation; no baseline source history or direct W1 result. `BUILD_PASS / INPUT_INIT_FIX_COMMITTED_NOT_RUN / PHYSICS_GO_FALSE / DES_NOT_DETECTED`.

---

## 13 November 2026 — WSL `prepare r2`: CLASS C++ build **PASS**

The original [researcher WSL build log](../results/ge19_full_class_tangent_prepare_20261113_r2.log) is archived **byte-identically** (SHA-256 `b9f4ecda4b737317c99835ef08f2a04c2b42dd1665d8a9fcef41da58e455e42a`, Git blob `f96ffa4307c14bc37e262918c867496d9f8421fc`, 12367 bytes). The logger captures complete `GE19_TANGENT_AEST_HEADER_ORDER_REPAIR_PASS`, including modified source SHA-256 `c41ad4cad9cc18d658f80841137094349657df6ac5d68fd3c0c75cfbbe092073`, followed by successful `g++` compilation of `source/perturbations.c`, native `class` executable link, static `libclass.a`, and successful `classy` wheel installation. The closing `GE19_FULL_CLASS_SOURCE_PATCH_PREFLIGHT_PASS` and `GE19_FULL_CLASS_PATCH_COMPILE_PREFLIGHT_COMPLETE_NOT_PHYSICS_GO` are present. One GCC truncation warning in the unrelated `source/distortions.c` did not prevent the build.

**Meaning:** The native experimental full CLASS code is now *actually compiled* and source-prefight-validated in the researcher's **isolated pinned v077 checkout**. No real `baseline_dt010`, force, null-control, convergence, or physical observable has run yet. `PHYSICS_GO=false`, DES detection absent.

**Additional code reading before native run:** Original CLASS `perturbations_vector_init` sets all `used_in_sources` perturbation coordinates to true by default; it disables only specified higher photon/neutrino multipoles, not the appended AeST `q_j`/`p_j` coordinates. Thus the dense-output baseline record callback receives interpolated bath coordinates from the native evolver. **However, for the single selected k the recorder replaces the normal `perturbations_sources` callback**, so standard native `mTk` source tables from that *baseline recorder* are **not valid transfer products**. The meaningful outputs from that pass are only `GE19_TANGENT_TRACE` (`Bchi0, W0`) and the associated source history. The full forced pass still runs the original `perturbations_sources` callback for its own transfer tables. This baseline transfer caveat is an engineering limitation and must not be mistaken for a constraint/physics result.

**One next native test:** the wrapper's `run` step, with fixed `k,z` and no finite-`eta` sweep, is the **first actual experiment**. If any selected-k source-table or interpolation error occurs, stop and treat as an implementation issue. Do not infer physical null signal from a failed run. Even if it passes numerically, independently validate true primordial initial conditions, approximation switching, Einstein/Ward residuals, and original action equivalence before `PHYSICS_GO` or DES claims.

---

## 13 November 2026 — second WSL prepare: first C++ build blocker resolved in source

The original WSL `prepare` rerun **passed** the Python syntax preflight, full pinned-source SHA and C-patch anchor checks, then printed `GE19_FULL_CLASS_TANGENT_PATCH_APPLIED_NOT_VALIDATED 856ba9feeda5a6c7de9d13441755303ade38b685138091b2bca533630112b0b3`. The build entered actual `g++` compilation of `source/perturbations.c` and stopped with **three not-declared errors** in `ge19_record_callback`: `aest_memory_active_count`, `aest_memory_node_order` and `aest_memory_weight_order`. No native CLASS baseline, tangent or DES run occurred.

**Exact source-level diagnosis:** Original `v019/apply_patch_v019.py` inserts `#include "aest_memory.h"` immediately following `#include "parallel.h"`. The original `v019j/apply_memory_patch.py` appends the three declarations to that header, inside the original `extern "C"` protection. Our initial tangent patcher instead inserted the helper and its `ge19_record_callback` immediately after `parallel.h`, **before** the existing `aest_memory.h` include. In the C++ translation unit the functions were therefore not declared when referenced. This is an ordinary header-order bug and **not** a failed memory physical equation.

**Permanent and existing-tree fixes:**

- The [GE19 tangent patcher](../ge19/physics_gate/patch_full_class_tangent_two_pass_20261112.py) now inserts its C helper **after both original CLASS/AeST includes**.
- The [strict single-source header-order repair](../ge19/physics_gate/repair_full_class_tangent_header_order_20261113.py) handles the **already-patched** WSL file. It requires the exact observed old modified-source SHA-256 `856ba9feeda5a6c7de9d13441755303ade38b685138091b2bca533630112b0b3`, original unpatched v019j backup SHA-256 `2b4d7be96b6ebf4149bef129e357a32571f69cfffb3be0b1792d578e82ad6e17`, the original pinned CLASS HEAD/blob, one exact callback marker and one existing memory header. It moves **only that include** before the helper, takes a snapshot, updates the existing source manifest SHA, and preserves all physical C equations. On a correctly ordered source and consistent manifest, it performs a no-op.
- The [isolated WSL prepare wrapper](../ge19/run_local_full_class_direct_tangent_20261112.sh) now runs this repair automatically **only after the original patch/manifest is present**, before `make -j2`. It performs Python syntax preflight on the repair script as well.

**Next action:** preserve the existing `~/GE19_CLASS_TANGENT_v077` and run the existing single `prepare` command after `git pull --ff-only`. **Do not clone, reset, delete the original backup, or rerun historical v019/v019j patches.** If the next compile succeeds, further full physical and numerical checks are still required. As of this change, **new C compilation has not been reexecuted** after the fix; `PHYSICS_GO=false`, `DES_detection=false`, and the five-pass `run` must wait for `PREPARE_EXIT=0`.

---

## 13 November 2026 — first original WSL prepare diagnosis and source-hash repair

Original [researcher prepare log](../results/ge19_full_class_tangent_prepare_20261112.log) was supplied directly in the current conversation, and has now been **byte-exactly archived** at the linked path (1510 UTF-8 bytes, SHA-256 `f072487becd79a747d6007237428ab5436f5546532440a175f6a0c127b63ba18`, Git blob `97b27f4c0d96027afae63aec7430abc3ae06980a`). It establishes: `GE19_PYTHON_SYNTAX_PREFLIGHT_PASS`, isolated pinned CLASS checkout at `e8580832`, successful original v019 and v019j patches with all their original source-audit checks, then **`GE19_UNRECOGNIZED_CLASS_SOURCE_SHA256=2b4d7be96b6ebf4149bef129e357a32571f69cfffb3be0b1792d578e82ad6e17`**. No experimental tangent source patch had been applied, and no C compilation or full CLASS integration started.

**Cause:** original patcher had an incomplete allowlist of expected generated v019j `perturbations.c` SHA-256 values; the produced WSL source was NOT one of its two prelisted candidate files. The C anchor audit 7/7 was on **original CLASS** source, not proof that this particular source hash should be rejected or accepted without verification.

**Repair committed:** experimental [source patcher](../ge19/physics_gate/patch_full_class_tangent_two_pass_20261112.py) now recognizes **exactly** the observed new SHA as an explicit additional allowed candidate, but additionally requires (i) pinned CLASS HEAD `e85808324f51fc694d12e3ed7439552a3c3f9540`, (ii) pinned original `source/perturbations.c` Git blob `c78fe4376d2eeebfbf4ff0cfca13b048d4513fa0` from HEAD, and (iii) unchanged `v019/apply_patch_v019.py` and `v019j/apply_memory_patch.py` source blob IDs `c78484eb916bfee2730759c0bdc813a706bf9a68` and `14796a5ed9e6265ed6810c792a93d7328a109364`. The [runner](../ge19/physics_gate/run_full_class_two_pass_tangent_20261112.py) enforces the same source SHA allowlist and requires the original HEAD/blob provenance reported in the manifest. This is an **implementation acceptance repair**, not a new physics result.

**Next step:** on the **existing** isolated checkout, `git pull --ff-only` the research repo and rerun only `bash ge19/run_local_full_class_direct_tangent_20261112.sh prepare`. Do not reset or reclone the isolated CLASS directory. The runner itself skips original v019/v019j patches when their original markers are already present. This will attempt the experimental tangent source patch, build, and preflight. **Until its WSL compile result is supplied, the true status is `PREPARE_SHA_LOCK_REPAIRED / CLASS_C_BUILD_NOT_YET_PROVEN / PHYSICS_GO_FALSE`.** Do NOT run the five-pass `run` stage if prepare fails.

---

## Committed implementation

- [Full CLASS source-locked two-pass patcher](../ge19/physics_gate/patch_full_class_tangent_two_pass_20261112.py): accepts only historical AeST v019j perturbations.c SHA-256 276646d913348824bddf9e24138e4213ecc3fb8b605d21525bf9280474dbca80 or separately frozen quarter candidate SHA-256 75bf9fe85f2aae85031edc109e131c6b5d1745dca8497300237e16e57c99f883. Refuses unexpected sources and reruns; creates an original-source backup and manifest. It changes the historical half coefficient to the action-motivated quarter ONLY in an isolated CLASS copy, leaving the historical sources intact.
- [Five fixed native-CLASS experiment runner](../ge19/physics_gate/run_full_class_two_pass_tangent_20261112.py): source patch/hash checks, frozen input Git blob f9a2bde8921a148e063f9657a8ede0a51c6a629d, original Exp cosmology and real photon, baryon, UR/ncdm species, Newtonian adiabatic IC, positive order-16 bath, eta=0, single k=0.06732117 Mpc^-1 (0.1 h/Mpc), single z=0.5, bounded k range. Refuses a stale CLASS executable or preexisting results.
- [Isolated local WSL prepare/run script](../ge19/run_local_full_class_direct_tangent_20261112.sh): original pinned CLASS v077 at commit e85808324f51fc694d12e3ed7439552a3c3f9540, then original v019 and v019j patches and experimental tangent patch on a SEPARATE local checkout. No GitHub Actions.

The original CLASS source/perturbations.c pinned Git blob c78fe4376d2eeebfbf4ff0cfca13b048d4513fa0 was inspected: seven stable insertion anchors each occur exactly once (header, native vector initialization, Einstein source readout, solve locals, approximation interval, evolver callback sampling, and allocation release). The original AeST v019 and v019j patch source strings were also inspected. **Seven static anchor checks do not certify Python syntax, C compilation, exact modified source SHA, nonlinear/approximation switching or complete physical action closure.**

## Method: TWO passes through native full hierarchy

**Baseline record pass:** With eta=0 but normalized q/p oscillator states active, evolve the original full CLASS scalar state from its original early-universe start. At the one selected k, sample the *accepted/interpolated CLASS state* densely from tau_initial, not only the often later native source tau_sampling array. Record tau, scale factor, baseline W=(Phi+Psi)/2 and the normalized Bchi0 force. This retains the retarded q/p history which was discarded by the previous z=19 dust proxy.

**Forced tangent pass:** Restart the same full native CLASS equations at eta=0 with the selected-k tangent initial vector set to zero (conditional on eta-independent primordial IC). Linear source forcing is introduced ONLY in the native conformal-time E equation as minus a*Q*Bchi0/(4*K_B). The rest of CLASS evolves all actual photons, baryons, neutrinos, metric and approximation transitions using its original vector state. Native Einstein shear evaluates W1=(Phi1+Psi1)/2. This never differences two nearly equal finite-eta runs. The continuously retarded bath is evaluated at eta=0 through the selected normalized eta->0+ prescription; its physical legitimacy still requires source/action acceptance.

**Fixed checks, not eta sweeps:** baseline source sampling at 0.1 Mpc, forced no-source null control with Y1 initial zero, forced tangent from 0.1 Mpc baseline, baseline at 0.05 Mpc with tighter tolerance, forced tangent from 0.05 Mpc baseline. All five passes have the same original physical parameters and selected k/z; zero forcing must return zero W1, and source interpolation plus integration changes must converge. This is a NUMERICAL SCREEN, not full physical proof.

## Two local WSL stages

From the normal project checkout on branch physics-first-gravitational-elasticity and with local virtual environment:

    cd ~/aest-memory-gravity
    git pull --ff-only
    source .venv/bin/activate
    set -o pipefail
    bash ge19/run_local_full_class_direct_tangent_20261112.sh prepare \
      2>&1 | tee results/ge19_full_class_tangent_prepare_20261112.log
    rc=$?
    echo "PREPARE_EXIT=$rc"

This clones a SEPARATE pinned CLASS checkout into ~/GE19_CLASS_TANGENT_v077, applies the two original patches and the experimental source patch, then compiles locally and runs a non-executing source/manifest preflight. It DOES NOT run the five-pass experiment. A source-hash error, wrong C anchor or compile error means stop and inspect: do not change the original historical CLASS.

Only if PREPARE_EXIT=0, run the fixed experiment:

    cd ~/aest-memory-gravity
    source .venv/bin/activate
    set -o pipefail
    bash ge19/run_local_full_class_direct_tangent_20261112.sh run \
      2>&1 | tee results/ge19_full_class_tangent_outer_20261112.log
    rc=$?
    echo "RUN_EXIT=$rc"

If cloning is unavailable, manually copy a pinned, CLEAN original CLASS checkout to ~/GE19_CLASS_TANGENT_v077 and restart prepare. The user must NOT patch their original CLASS checkout. Run only one such campaign locally, no Actions. Native logs and trace/results will be under results/ge19_full_class_direct_tangent_20261112; the optional generated GE19_TANGENT_EXPERIMENT_REPORT.json is experimental and always marks PHYSICS_GO false.

## Mandatory physical acceptance STILL OPEN

- A compiled patch and numerical convergence do **not** demonstrate full original covariant Einstein–AeST–NL0B action equivalence. In particular the source-normalized quarter coefficient is currently a restricted action-derived candidate, not a full general all-species proof.
- Confirm that native RHS and every CLASS approximation-vector rebuild are truly homogeneous/linear for the tangent; a zero-source null helps but does not independently certify all transition matrices.
- Verify the original full growing adiabatic eigenvector beyond its leading superhorizon coefficient, including eta independence of the primordial IC and no-free-bath branch; if initial data depend on eta, the tangent initial vector must not be assumed zero.
- Independently evaluate full finite-k Einstein Hamiltonian, momentum, shear, trace and LW33 scalar Ward residuals for baseline AND tangent, not only identities used to construct them.
- Quantify actual interpolation, solver and roundoff errors against absolute W1; if the tangent cannot be resolved, classify INCONCLUSIVE. A failed build, null check or source gap is IMPLEMENTATION_BLOCK, not a physical null.
- Only after physics and numerical acceptance, construct a physically defined galaxy–Weyl P_gW with tracer/bias, redshift projection and DES Y3 covariance; CLASS native d_m is not independently valid for repurposed pressureful CDM slot.

**Scientific stop:** a numerically successful W1 from this runner is only a full-species experimental tangent, not yet a certified observable or DES detection. No claim of a physical discovery is justified before those independent checks.
