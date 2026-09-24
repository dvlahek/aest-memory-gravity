# GE19 H4F2f — third CI workflow-only numeric truthiness failure (immutable)

The repaired H4F2f source audit successfully generated a **PASS**
result in run `36036837437`, job `107758916646`,
head `1e7ce63a99940c3df6edc7df6adcd6ad4c52c150`.
The workflow's **post-audit assertion** then failed, so the
Actions run conclusion is `failure`.

The artifact `10825037826` contains exact byte-identical JSON
and FULL logs, each 4200 bytes and SHA-256
`b6aca9808ae36eaebea2356c0f3443e571e6ede8a4c0436be7cd80bf2bc3eb40`.

The JSON classification is
`GE19_H4F2F_GE06_SPATIAL_WARD_SHIFT_SOURCE_SUBSET_PASS`,
with `all_subset_gates_pass=true`. All frozen blob,
GE06 coframe/jet/density, action/source binding, and
both b_f/b_x symbolic and numerical gates are true.
The exact numerical errors are b_f `0.0` and b_x
`1.6592729300491167e-16`; both are inside the
original `1e-9` threshold.

The script's aggregate code was already corrected at blob
`49e7546e5ccb76d27436486f8baddd2a4d17956e`.
The workflow separately had the obsolete assertion
`all(all(x.values()) for x in d["source_only_frozen_generator_numeric"].values())`.
It converts the legitimate b_f error `0.0` to false.
The traceback is `AssertionError` at the inline
workflow's line 10. The source-audit command itself
returned successfully; no physical gate failed.

Narrow repair: modify only the workflow post-audit
numeric assertion to require every named Boolean gate
to be `True` and every relative-L2 numerical error
to be at most `1e-9`. Retain the corrected script
blob, preregistration, frozen source files, outputs
and full H4 claim boundary unchanged. Rerun from a
new workflow commit.

This CI orchestration failure is not an H4/Z21 science FAIL.
Complete all-sector H4 source-parent Noether and
common corrected-parent grid remain open.
Z21 NOT CERTIFIED; lensing blocked.
