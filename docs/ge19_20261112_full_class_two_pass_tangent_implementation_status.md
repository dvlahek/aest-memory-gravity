# GE19 — Experimental full CLASS direct-tangent implementation, one fixed campaign

**12 November 2026. Status: SOURCE CODE COMMITTED; ORIGINAL CLASS STATIC ANCHORS 7/7; WSL CLASS BUILD/EXECUTION NOT PERFORMED; PHYSICS_GO=false; NO DES DETECTION.**

This is now a concrete experimental source patcher and runner, not merely a proposed calculation. The code has not been compiled against the researcher's isolated CLASS checkout or physically qualified. Do not describe this artifact as a demonstrated full CLASS Weyl result until the actual local source-locked run returns evidence.

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
