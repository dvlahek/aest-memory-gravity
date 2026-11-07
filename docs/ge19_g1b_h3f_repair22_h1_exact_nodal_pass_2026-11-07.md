# GE19 G1B — exact frozen H3F / Repair22 H1 lineage PASS

Date: 2026-11-07  
Classification: `GE19_G1B_H3F_REPAIR22_H1_NODAL_IDENTITY_EXACT_PASS_CONTINUOUS_OPEN`  
Branch: `physics-first-gravitational-elasticity`.  
Scope: immutable source-locked **nodal-data identity**, NOT physical all-interval Euler enclosure, H4 Ward certification, Z21 science solve or observational result.

## Actual local evidence supplied by the researcher

- `results/ge19_g1b_h1_parent_lineage_20261107_r1.json`: 5,061 bytes; SHA-256 `eb7de28b3c8640229d6fb24a104e97e3e4a9b41adf498b111ce2a0554ea9f300`.
- `results/ge19_g1b_h1_parent_lineage_20261107_r1.log`: 733 bytes; SHA-256 `2465f1ffbccaea4609d14cd8a89b620f615ea34835b44b782dfd0764fbac0c0e`.
- Exact source-bounded G1B script: `ge19/h4f3d_g1b_frozen_h1_parent_lineage_identity.py`, including correction to module-shadowing Python implementation error (fix commit `5aa6e02c7e26d21e89983f2b816381f51c8a41ba`). The original implementation crash did not test parent fields; this **r1 run** successfully evaluated them.
- Four original Git source blobs matched source pin values. Both immutable NPZ SHA values matched: H3F `90840755fa9febb1d8cb84609d9e58f67dec2a0a01cd6bf8e47685b45caa4542`, Repair22 `3020e0d040f902ab2609e05705f4508d9919665b1344fa0e641644ea8fc41a16`.

**PASS:** all **14 of 14** key arrays `array_equal == True`, `max_abs_difference == 0`, `relative_L2 == 0`:

- common `x_primary` (128 time nodes) and `x_control` (64 nodes);
- `C_min`, `C_star`, `C_max` H1 states at both Nt128 and Nt64 (six array comparisons);
- corresponding H1dot at both clocks (six additional comparisons).

The complete state arrays are shaped `(6,6,Nt)` and dynamic derivatives `(6,4,Nt)`. The output reports `all_fields_finite=true`. This proves that the corrected H3F H1 parent consumed by H4F3B is **exactly the same sampled H1/H1dot data** as the Repair22 H1 parent used to construct the Repair32B Z11.

## Scope of the closed question

**CLOSED (G1B nodal lineage):** no discrepancy, re-projection or hidden H1 data mismatch exists **in the tested saved time-node arrays** between the H3F and Repair22 ancestry routes. Thus there is no scientific reason to re-run H1 purely to reconcile these two frozen node datasets.

**NOT CLOSED (G1 continuous parent theory):**

1. Exact nodal equality is not a proof that the two off-clock interpolants, analytic backgrounds, integral representations or ODE stage histories are the same.
2. The D47 R5g / D55 continuous H1/X10/GE05 certificates have *different provenance and explicit scoped trajectories/cohorts*. They do **not** follow logically from this H3F-vs-Repair22 bitwise data equality alone.
3. `Z11` is separately reconstructed in Repair32B and certified via Repair32C **artifact-only** checks; the true continuous first-order Euler `E_i11` enclosure entering H4F3D4 is not certified by this G1B test.
4. The original Repair26 GE05 q10 bath and D55 physical bath closure must likewise be matched by exact representation/normalization, cohorts and intervals rather than a coincidental source hash.
5. D17 original-action dense numerical H1 reports sampled residuals, D18 Bernstein is *conditional* on an independent physical operator curvature and controlled rounding, and D45 off-clock PCHIP sensitivity explicitly does not certify the action H1 Euler all-interval residual. No transfer should be asserted without the physical source identity and interval certificate conditions.

The versioned mathematical G1A source-Ward bound in `docs/ge19_g1a_parent_to_h4_source_distributional_bound_2026-11-07.md` may be applied to the actual H4 source only once compatible continuous Euler residual and field/gradient bounds are known. It does not delete the original preregistered D9/D12R3 FD4/FD8 structural budget.

## Decision for the next research step

Do **not** repeat G1B, GE06/GE07 Cmat, the six-source H4 construction or a broad numerical V-series replay.

Work on a one-page **certificate transport theorem** that explicitly identifies sufficient conditions for transferring the locked R5g/D55 continuous first-order H1/GE05 certificate to the *identical frozen H4F3B H1 and Repair32B Z11 parent route*:

- same action-derived background and scalar charge/Exp branch over the same full interval;
- exactly matching initial data, Fourier modes, physical clock convention and boundary rules;
- same underlying ODE/DAE vector field (including GE05 coupling), with a uniqueness/stability theorem and independent error enclosure;
- controlled interpolation/reconstruction defect between continuous represented trajectory and saved array values;
- independent Z11 and GE05 q-node Euler residual enclosures on the actual corrected-H4 cohorts.

Nodal agreement is one necessary input, not a substitute for the other conditions. If the R5g certificates cannot be shown to apply to the H4F3B route in full, preserve their scope and certify only the genuinely missing modes/intervals. Do not declare a new G1 FAIL without a frozen contradiction.

**No science status change:** `full_H4_Ward_certified=false`; `Z21_certified=false`; `lensing_licensed=false`. Original `1e-6` and temporal-order `>=2.5` H4 gates and historical science FAILs remain intact.
