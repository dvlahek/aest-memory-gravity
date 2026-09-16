# NL1C7A A3/A4 trace Repair02 — source-boundary audit fix

## Historical technical runs

- `35092490498`: original trace-helper anchor mismatch before CLASS build.
- `35093456930`: Repair01 successfully applied the post-v0.72 output-only trace extension, then stopped in the source-boundary audit before CLASS build.

For run `35093456930`, the Repair01 patch itself reported all of its output-only checks PASS, including retained v0.72 reload semantics and no new derivative assignment. The subsequent workflow assertion failed because the audit required several pre-existing source tokens to occur exactly once globally in `perturbations.c`. That uniqueness requirement is not a physics condition and was not part of the C7A science preregistration.

## Repair02 rule

Repair02 changes only the workflow source-boundary audit. The trace extension implementation blob remains frozen:

- `nl1c7a/apply_trace_extension.py` blob: `b1567b17245facbceb73f01aa21758968f69175b`
- `nl1c7a/trace_coverage_probe.py` blob: `5be7163070a7fa2709e3ac6cb5835206c8feb5ec`

The replacement audit must require:

1. every line containing `dy[` is byte-identical before vs after the C7A extension;
2. each frozen critical physics token exists before the extension and has exactly the same occurrence count after the extension;
3. the textual diff introduced by C7A contains none of `dy[`, `E_rhs_aest =`, `Pi_aest =`, or `metric_euler=`;
4. the Repair01 patch report remains `NL1C7A_OUTPUT_ONLY_TRACE_EXTENSION_REPAIR01` with all internal checks PASS.

Repair02 must not modify the CLASS equations, trace fields, k grid, `a_i`, solver tolerances, A4 gates, or A4 classification rule.

## Frozen provenance

- C7A prereg ancestor: `5399a2ca73165e8f97cea45934e50baf8ffb3629`
- Repair01 lock ancestor: `1c5bec98bc713c809e265aee7c7c74690015550d`
- A2 run: `35092206904` — SUCCESS
- A2 artifact: `10444488624`
- A2 digest: `sha256:05b36f93e272aebf04f9887b384c695b01b399ca4e816b1549a8e5d7f8189422`

No A4 science/coverage result exists from either historical technical run because CLASS build and the A4 probe were skipped.
