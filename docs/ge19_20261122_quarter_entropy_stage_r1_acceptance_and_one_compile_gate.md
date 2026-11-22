# GE19 — First isolated quarter/enthalpy CLASS staging: researcher WSL PASS, ready for a single compile check

**Date 2026-11-22. No physical-transfer claim.**

Researcher's original WSL stage [JSON](../results/ge19_quarter_entropy_class_stage_20261122_r1.json) and [log](../results/ge19_quarter_entropy_class_stage_20261122_r1.log) have been archived byte-for-byte. Original Git blobs: `5add1a54d58078ba457c8b4a45f0ec109cf3e7a7` and `8b52a1accaa53fdda1e760a398e916de001ecedf`; original SHA-256: `ce00b0d8678d6e29792061a79cf5b1b90d5cbfe153b14370fd811f80f6eed6a4` and `d7aa4eb84e5ccce6e919143330600cd481069325ab76f1eb980022d75890654f`.

The output is `GE19_ISOLATED_CLASS_SOURCE_STAGE_PASS 3`. Pinned upstream CLASS HEAD `e85808324f51fc694d12e3ed7439552a3c3f9540`. The **actual input checkout already had the action-normalized quarter coefficient**, reported `original_action_quarter_force=already_quarter_no_change`. Two edits were applied in the isolated candidate: `adiabatic_sync_density_enthalpy=changed` and `newtonian_density_gauge_enthalpy=changed`. Thus the successful run does **not** provide new evidence that a historical one-point Weyl tangent was computed with original-action source; this checkout and any older tangent's provenance are separate questions.

Original C SHA-256 `c41ad4cad9cc18d658f80841137094349657df6ac5d68fd3c0c75cfbbe092073`. New candidate C SHA-256 `3aa1dde9eaf55a10a43f39192132fb606d4190ff3bb4b0490915d96870186b81`. Source dir `/home/dino/GE19_CLASS_TANGENT_v077` remains unchanged by the staging command; new candidate dir `/home/dino/GE19_CLASS_QUARTER_ENTHALPY_20261122`.

## Next ONE bounded engineering operation

Run a **read-only source diff with file-hash check**, then compile only the **`class` C executable** from the independent candidate. Do not invoke an evolving cosmology or use DES residuals. Original CLASS pinned [Makefile](https://github.com/lesgourg/class_public/blob/e85808324f51fc694d12e3ed7439552a3c3f9540/Makefile) has a `class:` target that builds the C executable without automatically building Python `classy`; use `make -j2 class`. The source staging tool deliberately omitted old object/build directories, so this is a clean compile (not a new scientific simulation). Verify both SHA-256 values against the archived JSON, show the source diff and confirm that only the two permitted AeST enthalpy lines changed. Full candidate compilation can reveal missing headers or source conflicts but it **cannot** certify the full covariant AeST primordial growing mode.

Report the new compile log under `results/ge19_quarter_entropy_class_compile_20261122_r1.log`; stop if source hashes do not match. Do not delete or reset any prior CLASS tree. If build succeeds, the *next physical task* remains the missing coupled finite-k action-consistent primordial mode and physically transported retarded q/p; do **not** run a physical DES prediction using only this staging repair.

## Scientific stop line

- **SOURCE_STAGE_GO=true:** source normalization was already quarter-correct; both leading enthalpy adiabatic corrections newly staged.
- **COMPILE_GO=unknown:** not executed by this stage.
- **FULL_PHYSICS_GO=false:** full finite-k k² growing mode and scalar Ward/effective Einstein/fluid closure not certified.
- **RETARDED_QP_TRANSPORTED=false:** actual physical primordial chi(k,t) history still absent.
- **DES_detection=false:** no observed test.
