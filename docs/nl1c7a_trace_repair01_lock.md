# NL1C7A A3/A4 trace Repair01 — post-v0.72 helper anchor lock

## Historical technical failure

- failed run: `35092490498`
- failing step: `Apply locked output-only C7A trace extension`
- failure class: technical patch-anchor mismatch before CLASS build and before any A4 science/coverage result
- exact error: `trace helper: expected exactly one v0.23 trace anchor, found 0`

The validated eta=0 stack applies `v023/apply_source_grid_trace_patch.py` and then `tools/apply_v072_offline_trace_runtime_reload_patch.py` before the C7A output extension. v0.72 intentionally rewrites the same trace helper to support successive `Class` instances and therefore the original v0.23 helper text is no longer present when C7A applies its extension.

## Repair01 rule

Repair01 may change only the textual anchor and the replacement helper so that C7A extends the **post-v0.72** `aest_offline_trace_state` implementation. The replacement must retain all v0.72 runtime-path semantics:

- `active_path[4096]`
- runtime `AEST_OFFLINE_TRACE_FILE` refresh
- close/reopen when `strcmp(active_path,path) != 0`
- flush after header and each trace row
- no permanent `disabled` state

The C7A extension may add only the preregistered diagnostic output fields. It must not modify any evolution equation, solver tolerance, CLASS physical parameter, k grid, time/redshift coverage gate, or A4 classification rule.

## Frozen items unchanged

- C7A prereg ancestor: `5399a2ca73165e8f97cea45934e50baf8ffb3629`
- A2 certified run: `35092206904`
- A2 artifact: `10444488624`
- A2 artifact digest: `sha256:05b36f93e272aebf04f9887b384c695b01b399ca4e816b1549a8e5d7f8189422`
- coverage probe blob: `5be7163070a7fa2709e3ac6cb5835206c8feb5ec`
- CLASS commit: `e85808324f51fc694d12e3ed7439552a3c3f9540`
- eta = 0, memory disabled
- k grid: 128 log-spaced modes, `0.0015 <= k/(h Mpc^-1) <= 1.2`
- `a_i = 0.02`
- A4 gates and classification unchanged

No result from failed run `35092490498` is scientific evidence for or against the growing-mode bridge.
