# GE19 H4F2f — second CI numeric truthiness aggregation failure (immutable)

## Frozen execution

- GitHub Actions run: `36031753394`.
- Job: `107741943016`.
- Head commit: `952af69b71d19c56708f579a02141bad66dcf012`.
- Tested implementation blob: `f9a673af77405e14fda893daef382d38c4bb6b70`.
- Preregistration blob: `551294c5763b086919c9f27076a922c29ca953e5`.
- Conclusion: `failure` (exit 3 from source-audit script).
- Uploaded artifact: `10822666379`.
- JSON and FULL log are byte-identical, each 4195 bytes and SHA-256
  `a86ebda89ef23b6a6663ab8fc4ba59c022494a108f6e836bef811a92bb4714b3`.

The unmodified original JSON classified this execution as
`GE19_H4F2F_GE06_ACTION_SHIFT_SOURCE_SUBSET_FAIL` with
`all_subset_gates_pass=false`.

## Exact isolated implementation error

The artifact reports **all** exact frozen blob controls,
all 10 unreduced coframe/spatial density checks, all frozen
GE06 action/source bindings and all four symbolic partial
checks in each of `b_f` and `b_x` as `true`.

Its frozen-generator numerical checks are also all true,
with direct-versus-polarization relative L2 differences
`b_f=0.0` and `b_x=1.6592729300491167e-16`,
both below the preregistered `1e-9` bound.

The final aggregate code incorrectly used

`all(all(g.values()) for g in numeric.values())`.

That expression converts the legitimate floating-point
zero error `0.0` to Boolean `False`; it therefore
forces the aggregate FAIL even when every named
Boolean gate is true. This is a **test aggregation
implementation failure**, not a failed physical
source equation, a failed symbolic identity or a
new H4/Z21 science result.

The first H4F2f run `36030973726` and its
separate frozen half/full derivative issue remain
immutable in
`docs/ge19_h4f2f_first_ci_half_derivative_gate_failure_freeze.md`.
An intermediate run `36031713914` stopped at
its stale static code-blob gate before executing
the source test.

## Narrow corrective action

Version a new implementation that:
- retains the exact frozen preregistration and
  all source physics, symbolic equations,
  15-direction controls, deterministic samples
  and the `1e-9` numerical threshold;
- aggregates named Boolean numeric gates as
  Boolean values and separately compares
  reported relative L2 numerical values to
  the frozen threshold;
- pins the revised code blob in the dedicated
  workflow and reruns from a new commit;
- preserves this raw failed artifact, all
  historical results and the original H4
  active-shift `1e-6` target.

No corrected-parent common-grid H4 evaluation
or numerical Z21 solve occurred. The full
six-piece H4 source/parent Ward identity remains
open; Z21 NOT CERTIFIED; lensing blocked.
