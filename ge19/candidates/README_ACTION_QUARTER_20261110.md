# GE19 exploratory action-quarter *linear scalar* CLASS candidate

**Project branch:** \`candidate/ge19-action-linear-quarter-20261110\`  
**Physics stage:** \`EXPLORATORY_QUARTER_SOURCE_ONLY\`. **NOT** production PHYSICS_GO, not a DES forecast or a detection.  
**Original frozen branch:** \`physics-first-gravitational-elasticity\`; do not alter \`v019j\` or the original official CLASS checkout.

## Scientific justification, scope and limitations

The source-derived scalar action and exact reduced CLASS residual theorem favor the **one-quarter** coefficient rather than the historical **one-half** in the linear scalar E-equation **under the original AeST effective-fluid field dictionary**. The 2026-11-10 one-document [3D Fourier scalar embedding and covariant bath projection](../../docs/ge19_single_scalar_3plus1_embedding_and_candidate_source_2026-11-10.md) explains why one longitudinal Fourier direction represents the complete *linear scalar representation* on isotropic FLRW and why the NL0B projector derivative's longitudinal coframe term reduces exactly to original GE05 \`Aq\`.

This embedding is a **physical consistency argument** rather than a fully independently proven complete CLASS implementation with ordinary-species feedback, gauge switch and constraint propagation. **No observational inference is licensed.** The existing strict [PHYSICS_BLOCK](../../docs/ge19_physics_acceptance_decision_action_to_CLASS_2026-11-10.md) remains for production and DES.

## Exactly one C source delta (in a separate copied checkout)

\`ge19/candidates/prepare_action_quarter_candidate_20261110.py\` creates a new sibling directory from the **historical v019j-patched** pinned official CLASS source checkout. It checks the original patch's Git blob and the official v077 Git HEAD; changes **exactly**:

~~~diff
-          E_rhs_aest -= 0.5*Q_aest*Bchi_aest;
+          E_rhs_aest -= 0.25*Q_aest*Bchi_aest;
~~~

The original C variable \`Bchi_aest\` **already includes \`aest_eta\`**, and the final line dividing \`E_rhs_aest\` by \`aest_KB\` is unchanged. This encodes \(-a\eta QB_{\chi,\rm raw}/(4K_B)\), not a second division by \(K_B\).

Both original files \`v019/apply_patch_v019.py\` and \`v019j/apply_memory_patch.py\` remain byte-identical. The candidate script refuses any destination overwrite, checks unique anchors, creates a manifest and a one-line C diff, does **not** compile and does **not** run CLASS. The candidate copy contains potentially stale compiled binaries: **rebuild before any future regression.**

## Reproduce the source preparation (no CLASS numerical run)

~~~bash
cd ~/aest-memory-gravity
git fetch origin candidate/ge19-action-linear-quarter-20261110
if [ ! -d ../aest-memory-gravity-action-quarter ]; then
  git worktree add --detach ../aest-memory-gravity-action-quarter \
    origin/candidate/ge19-action-linear-quarter-20261110
fi

python3 ../aest-memory-gravity-action-quarter/ge19/candidates/prepare_action_quarter_candidate_20261110.py \
  --existing-v019j-class "$PWD/class_v077" \
  --candidate-copy "$PWD/class_v077_ge19_action_quarter_candidate" \
  --check-only

python3 ../aest-memory-gravity-action-quarter/ge19/candidates/prepare_action_quarter_candidate_20261110.py \
  --existing-v019j-class "$PWD/class_v077" \
  --candidate-copy "$PWD/class_v077_ge19_action_quarter_candidate"
~~~

Assumes the original already-v019j-patched checkout exists in \`~/aest-memory-gravity/class_v077\` with Git HEAD \`e85808324f51fc694d12e3ed7439552a3c3f9540\`. If it does not, **stop** rather than force patch application to a different source branch.

Expected source-only labels \`GE19_ACTION_QUARTER_SOURCE_AUDIT_PASS\`, \`GE19_ACTION_QUARTER_COPY_CREATED\` and \`GE19_ACTION_QUARTER_BUILD_STALE_REBUILD_REQUIRED\`; these are **source preparation**, not physics certification. The explicit `GE19_ACTION_QUARTER_` log prefix avoids confusion with the unrelated historical `v019q` research package.

**Next controlled action, only after source audit:** independent build of the copied CLASS checkout and one small \(\eta=0\) reproduction/constraint/retarded-initialization check. If those fail, no observational forward. No sweeps, GitHub Actions or observed-data fitting should be run in this candidate preparation.


## One bounded eta=0 candidate regression (after researcher source-copy PASS)

The researcher uploaded the successful source-copy diff and manifest. The original files are archived as
\`ge19/candidates/evidence/GE19_ACTION_QUARTER_CANDIDATE.diff\` (Git blob \`6049e86ccb1088b52600127f7f2b7d0824baf810\`) and
\`ge19/candidates/evidence/GE19_ACTION_QUARTER_CANDIDATE_MANIFEST.json\` (Git blob \`b8767523dc62256f7d1dbe9dbd69dd12d724411d\`).
GitHub readback confirms byte-identical uploads.

\`ge19/candidates/run_action_quarter_eta0_regression_20261110.py\` checks the exact two source SHA-256 hashes, original CLASS HEAD and uploaded evidence, and refuses any additional C differences. It rebuilds **only the copied** candidate with two compiler jobs, runs one AeST Exp \(\eta=0\) input in the already-built original and new candidate, and compares actual background and matter power-spectrum tables. It refuses missing or mismatched output.

**Limit:** this checks only the \(\eta=0\) invariance and source provenance. It does **not** measure Einstein constraint propagation or certify finite-\(\eta\) physical matter–Weyl/sky transfer. The output explicitly states those remain OPEN. No DES data, parameter sweeps or GitHub Actions.

### WSL

~~~bash
cd ~/aest-memory-gravity
source .venv/bin/activate
git -C ../aest-memory-gravity-action-quarter fetch origin candidate/ge19-action-linear-quarter-20261110
git -C ../aest-memory-gravity-action-quarter checkout --detach origin/candidate/ge19-action-linear-quarter-20261110
PYTHON=../aest-memory-gravity-action-quarter/ge19/candidates/run_action_quarter_eta0_regression_20261110.py

python3 "$PYTHON" \
  --historic-class "$PWD/class_v077" \
  --candidate-class "$PWD/class_v077_ge19_action_quarter_candidate" \
  --preflight || exit $?

set +e
set -o pipefail
python3 -u "$PYTHON" \
  --historic-class "$PWD/class_v077" \
  --candidate-class "$PWD/class_v077_ge19_action_quarter_candidate" \
  --out-dir "$PWD/results/ge19_action_quarter_eta0_r1" \
  2>&1 | tee results/ge19_action_quarter_eta0_r1_runner.log
~~~

Upload the runner log and \`results/ge19_action_quarter_eta0_r1/regression_result.json\`; on failure include the relevant \`candidate_build.log\`, \`historical_run.log\` or \`candidate_run.log\`. The runner will **not** edit or compile the historical original, and refuses to overwrite a previous output directory.
