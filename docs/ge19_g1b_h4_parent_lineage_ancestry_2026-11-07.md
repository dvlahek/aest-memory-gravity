# GE19 G1B — exact H1 parent lineage into H4F3B versus Z11

Date: 2026-11-07  
Classification: `GE19_G1B_PARENT_LINEAGE_PROVENANCE_IDENTIFIED_NODAL_EQUALITY_NOT_YET_TESTED`  
Branch: `physics-first-gravitational-elasticity`.

**The source-provenance question now matters more than repeated Cmat/shift tests.** We already proved the 16/16 actual source-bound linear Ward syzygy, and G1A derived a physical parent-Euler-residual-based a priori projected H4 source-Ward bound. Neither guarantees that all *stored parents actually used by H4F3B* are precisely the trajectories covered by earlier D47–D55 continuous interval certificates.

## Actual source-bound ancestry, not inferred from filenames

`ge19/h4f3b_actual_corrected_six_piece_source.py` (blob `0423cbc64f6cda3b2a9aeb67c734935ef3ae7f9`) consumes:

- H1 state `h1 = h3f[f"{tag}_H1_{label}"]` and H1dot from the **H3F corrected-Y science NPZ**, SHA256 `90840755fa9febb1d8cb84609d9e58f67dec2a0a01cd6bf8e47685b45caa4542`.
- Z11 state and Z11dot from frozen **Repair32B** NPZ (the `Repair32C` artifact-only Z11 certification is checked separately).
- The actual first GE05 bath (q_{10}) forcing for M2 from the **Repair26 R1 full-history trace**, using 2048 quadrature nodes.
- Corrected Z20 and normalized q20 from **H3F/H3G**; those feed H4 physical sources but do not enter the direct first-order (P_{\rm lower}) product in H4F3D4.

`ge19/repair32b_factor2_corrected_reduced_h2_z11_reconstruction.py` (blob `6ece578e8a30f48faaded8808687a9bd5c114608`) explicitly constructs its first GE05 forcing from `z22[f"{tag}_H1_{label}"]` in the **Repair22 NPZ**, SHA256 `3020e0d040f902ab2609e05705f4508d9919665b1344fa0e641644ea8fc41a16`. It also inherited R27 bath reconstruction in its preregistered route.

`ge19/h3f_corrected_y_z20_science_reclosure.py` calls the action-completed `h3f_corrected_y_parent_core.py`, which recomputes the older Repair21 H1 pipeline, and saves its H1/H1dot arrays to the H3F NPZ. `ge19/repair22_on_shell_parent_z20_certification.py` likewise saves H1/H1dot arrays with the **same explicit key convention**.

**What is proven by reading these source files:** shared time axes are explicitly checked by H4F3B. The fact that H3F H1 and Repair22 H1 (or later D47 R5g H1) are identical as arrays or continuous trajectories is **NOT automatically established** by a shared clock or success classification. No discrepancy is claimed; equivalence is a falsifiable prerequisite.

## One targeted frozen-data comparison: no new solver

New read-only program `ge19/h4f3d_g1b_frozen_h1_parent_lineage_identity.py`:

1. Checks exact frozen Git blob sources for H4F3B, H3F, Repair22 and Repair32B; fails closed on a changed parent route.
2. Checks SHA256 for the two original immutable H3F / Repair22 NPZ arrays.
3. Compares every common `{tag}_H1_{primary/control}` and `{tag}_H1dot_{primary/control}` array plus original x axes, **without any fitted tolerance**; reports exact `array_equal`, max absolute difference and relative global L2 per component.
4. Distinguishes exact nodal-array equality from true **continuous off-clock Euler enclosure equivalence**. It does NOT transfer R5g/D55 certificates, change the H4 sources or produce new physical Noether residuals.

An exact match would remove a data-lineage ambiguity between H4F3B H1 and the H1 used to build Repair32B Z11. A mismatch would isolate a real ancestry difference to reconcile before bounding cross-parent products. Either result is **only provenance evidence**.

## Local execution on frozen project artifacts

```bash
cd ~/aest-memory-gravity
git pull --ff-only
source .venv/bin/activate
export PYTHONPATH="$PWD"
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
set -o pipefail

python3 -u -m ge19.h4f3d_g1b_frozen_h1_parent_lineage_identity \
  --results-dir results \
  --json-out results/ge19_g1b_h1_parent_lineage_20261107.json \
  2>&1 | tee results/ge19_g1b_h1_parent_lineage_20261107.log
echo "EXIT=${PIPESTATUS[0]}"
```

This local command does not consume GitHub Actions. Both old NPZ files remain read-only; if either is missing or SHA mismatches, stop rather than substituting a different result.

## What remains even if exact nodal equality passes

- Compare continuous provenance of the actual H4F3B H1 and Repair22 H1 with the specifically certified D47 R5g trajectory/interval scope. Nodal equality does not prove off-clock identity under PCHIP/ODE reconstruction.
- Independently bound the Repair32B/Repair32C Z11 **continuous** first-order Euler residual and trace compatibility, not just node/time-global diagnostics.
- Independently control the **actual Repair26 R1 bath** as used by H4F3B under the D55 continuum GE05 certificate, including q-node normalization, cohort, source-map factor and full relevant interval.
- Bound parent lower boundary and residual norms, then freeze genuine physical G3 numerical budget (or separately preregister a new mathematical weak-form route without rewriting the original D12R3).

**Hard flags unchanged:** `full_H4_Ward_certified=false`, `Z21_certified=false`, `lensing_licensed=false`. Original shift gate `<=1e-6`, original time order `>=2.5`, and old frozen fails immutable.
