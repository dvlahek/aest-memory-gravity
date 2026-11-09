# GE19 LW06 — first signed native matter–Weyl cross transfer: archived-parent numerical PASS

**Date:** 2026-11-09. **Scientific classification:** \`GE19_LW06_NATIVE_MATTER_WEYL_SIGNED_CROSS_NUMERICAL_PASS_OBSERVATIONAL_OPEN\` for a **read-only numerical replay of the archived parent arrays**. This is **not** an observed galaxy–galaxy lensing measurement, certified survey forward model, or Nature-level discovery. The canonical new GitHub runner has been committed but has **not yet been run in the researcher's WSL**; the initial calculation was an independently coded archive replay.

## Provenance and time ordering

- Preregistered BEFORE the first new LW06 computation: \`ge19/lw06_native_matter_weyl_cross_predata_20261109.json\`, commit \`15e6d9282c8c410b9dd931353a517ce960621ae2\`, Git blob \`5b9811d04ad934d3c1a1c3fcad18505fd79ea6ff\`. Original physical model: \`KB=0.0665, tauH0=10, p=0\`, original pinned modified CLASS HEAD \`e85808324f51fc694d12e3ed7439552a3c3f9540\`. Four original numeric source amplitudes \`[10,5,2.5,1.25]\`, **not physical finite eta values**.
- Canonical WSL executable: \`ge19/lw06_native_matter_weyl_cross_20261109.py\`, code correction commit \`c5bb8019cc126c842e4ec9ddc274389fbe947ee1\`.
- Archived parent byte locks: LW01 JSON SHA256 \`ae49cb0d1e63d82080c092ca938beec4608afe2a0e30650b7d47b0513512014b\`, LW01 NPZ SHA256 \`56172ff827d5314cbe066deaeec520f2062b4e4a646de7cb9fe509ae03c9dac9\`, LW05 geometry JSON SHA256 \`40dd40e7476816dae7f4ff81b32c72d5778ac6c8ca5c308956dd4330ef32a04a\`.
- Independently replayed in the analysis container using exactly these mounted source archives and the preregistered numerical limits, with **zero new CLASS solves or DES/ACT observed data reads**. Actual archived replay outputs (not yet binary-committed to Git): \`ge19_lw06_native_matter_weyl_cross_20261109_archive_replay.json\` SHA256 \`b8d3dce8531519aa08822aa88525a4f5bae5de25ae6a801258b2fc67feca705a\`; \`ge19_lw06_native_matter_weyl_cross_20261109_archive_replay.npz\` SHA256 \`de93e118ec8f4b012aeab0511aa57d75b87a78e6b25896235382798c9e56bdfa\`. Reproducibility source \`ge19_lw06_archive_replay.py\`, SHA256 \`f37508e743c9fc9a537af3a2a0fbde6dc1fad6ac7ab2f637d0790ff80173234b\`. Plot \`ge19_lw06_signed_cross_native.png\`, SHA256 \`c3f99e28bcbe8f68229efaa76b1f5e9631d3a7d5aea5056734fc86be989f7ac9\`.

The original \`LW01\` transfer data and source calibration have **not** been modified. The numerical result has been frozen now rather than retuning source shape/gates.

## Exact source-level object

On the original 322 native k × 8 native z mask (2,576 shared nodes) in the original **Newtonian gauge**, define real transfer amplitudes \`D=T_delta\` and \`W=(phi+psi)/2\`, for an original common adiabatic primordial mode. The primordial dimensionful factor is

\[
\mathcal P_\mathcal R^{3D}(k)
=\frac{2\pi^2}{k^3}A_s(k/0.05\,\mathrm{Mpc}^{-1})^{n_s-1},
\quad k=h k_h,\ h=0.673324639084866.
\]

Then the signed native cross power and tangent are

\[
P_{\delta W}=\mathcal P_\mathcal R^{3D}\,D W,\qquad
\partial_\eta P_{\delta W}
=\mathcal P_\mathcal R^{3D}\left[
T_{\delta,\eta}W+D T_{W,\eta}\right].
\]

The four \`T_{\delta,\eta}^{(lambda)}\` and \`T_{W,\eta}^{(lambda)}\` come from **the exact archived symmetric ±lambda source runs**, and the signed cross tangent is evaluated for each lambda and then averaged. No local ratio \`T/W\`, \`delta/W\` or sign/phase inferred from power alone. This is a transfer product, not a new independent perturbation evolution.

## Preregistered gate outcome: all six PASS

| Gate | Executed archive metric | Frozen criterion | Outcome |
|---|---:|---:|---|
| \`W=(phi+psi)/2\` native source dictionary | relative L2 0 | ≤1e-12 | PASS |
| Exact mean-product-rule reconstruction | relative L2 1.25387e-16 | ≤1e-12 | PASS |
| Four-lambda signed cross affinity | max 3.08571e-4 | ≤0.005 | PASS |
| Signed cross tangent norm over baseline cross norm | 0.0035170220 | ≥1e-12 | PASS |
| Single-common-mode algebraic cross-power bound | 1.34208e-16 | ≤1e-12 | PASS |
| All transfer and derived power arrays finite | true | true | PASS |

**Exact four lambda affinity values**, descending lambda 10,5,2.5,1.25: \`0.000198115423, 0.000167490795, 0.000188418455, 0.000308571030\`. These are dimensionless **native-grid numerical self-consistency metrics**, not observed lensing percentage or statistical significance.

The original Newtonian-gauge \`P_{delta W}\` is negative at all 2,576 primary nodes under this CLASS transfer sign convention. The formal signed tangent is positive at 429 nodes and negative at 2,147. **The baseline negative sign is not the sign of observed galaxy–galaxy tangential shear**; the actual observable requires the correct lensing kernel/gauge/galaxy sourcing and window conventions.

The exact single-common-mode power identity \`|P_delta,W|²=P_delta,delta P_W,W\` is an **algebraic check**, not evidence that matter and Weyl were statistically independently measured. Most of the physics is established at the archived LW01 parent level.

## Exploratory diagnosis: the two source-derivative terms are nearly identical

A read-only **post-result exploratory diagnostic**, explicitly **not** a preregistered science gate, compared \`A=P_R*T_delta,eta*W\` and \`B=P_R*T_delta*T_W,eta\` on the same primary mask. Their global L2 norms are \`0.0451960172181\` and \`0.0451948078358\`, respectively; Euclidean cosine \`0.9999999980960941\`, and normalized difference \`||A-B||/||A+B||=3.36298022174e-5\`.

Thus for the archived configuration the two summands are **almost the same signed field**, not obviously independent signatures. This is a major caution when proposing that merely combining a galaxy-density transfer and Weyl transfer provides a unique observational discriminator. It could arise naturally from their related linear evolution and the Einstein/Poisson-type constraints, and needs an independently validated gauge/physics interpretation before a causal-memory claim.

A second exploratory native-grid check projected the derivative off a **single global amplitude-rescaling direction** \`P_delta,W\`, leaving 98.97% of its unweighted L2 norm. This is **not** a noise-weighted forecast: scale-dependent galaxy bias, intrinsic alignments, baryons, modified-gravity competitors, source selection and incomplete k,z support could mimic or erase this shape. Do NOT use it as evidence that DES/ACT can identify memory.

The exploratory JSON \`ge19_lw06_readonly_identifiability_diagnostics.json\` has SHA256 \`fee02e561d405685288bcf8dc3b4a865f8c6d444e9af06b7bce899de22b29caa\`.

## Scientific status and new decision

- \`LW01\` **PASS** remains the source of the signed Weyl/matter transfer. \`LW03\` 17/33/65 radial quadrature **FAIL** remains frozen. \`LW04\` source-time refinement **PASS** remains frozen. \`LW05\` full cosmic-shear LOS k/z support **BLOCKED** remains frozen.
- \`LW06\` confirms that a numerically robust **native matter–Weyl cross-power tangent** can be assembled with the original source-level physics and a stable lambda amplification in exactly the already certified window; it does not cure previous radial, redshift-domain, physical coupling, gauge or data-model issues.
- The next worthwhile scientific gate is NOT another CLASS run. Before any DES likelihood, independently validate the **observed galaxy density / Weyl cross** in a consistent gauge, choose a **real lens n(z)** and true angular bandpower/window function that are contained in the certified domain (or stop). Then assess whether a restricted history-dependent model provides independent observable information relative to alternative instant-response physics and conventional nuisance parameters.
- Do **not** claim gravitational memory detected, finite physical eta identified, galaxy–galaxy lensing computed, or Nature-level phenomenology.

## Re-run on the researcher's WSL checkout (optional strict predata check)

\`\`\`bash
cd ~/aest-memory-gravity
set +e
git pull --ff-only
source .venv/bin/activate
python3 -u -m ge19.lw06_native_matter_weyl_cross_20261109 --self-test
set -o pipefail
python3 -u -m ge19.lw06_native_matter_weyl_cross_20261109 \
  --output-prefix results/ge19_lw06_native_matter_weyl_cross_20261109_original \
  2>&1 | tee results/ge19_lw06_native_matter_weyl_cross_20261109_original.log
echo "EXIT=\${PIPESTATUS[0]}"
\`\`\`

No CLASS root is needed. The runner checks the full original preregistered Git object and both original parent hashes. If the user's local LW05 JSON differs in content from the independent read-only archive hash, execution must halt rather than substitute a different source file.
