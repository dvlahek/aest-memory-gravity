# NL1C7A A3/A4 trace Repair04 — diagnostic k-output capacity lock

## Historical technical failure

- failed run: `35093879845`
- failing step: `Run locked A4 native coverage probe`
- failure class: CLASS input/output capacity limit before any A4 trace-coverage classification
- exact CLASS error: requested 45 `k_output_values`, exceeding `_MAX_NUMBER_OF_K_FILES_ = 30`

Repair03 successfully passed provenance, the validated eta=0 AeST stack, the output-only source-boundary audit, and the full CLASS/classy build. The failure occurred when CLASS parsed the diagnostic `k_output_values` request. No A4 coverage result was produced.

## Repair04 rule

Repair04 may change only the compile-time storage capacity for requested perturbation-output k values:

`#define _MAX_NUMBER_OF_K_FILES_ 30` -> `#define _MAX_NUMBER_OF_K_FILES_ 160`

The value 160 is chosen only to exceed the preregistered 128-point C7A k grid with margin. This macro controls the size of the diagnostic `k_output_values` array and does not alter the physical k grid, perturbation equations, background equations, solver tolerances, source sampling, transfer functions, initial conditions, or A4 gates.

The workflow must verify before build that exactly one original macro was replaced and that no other line in `include/perturbations.h` changed in this Repair04 step.

## Frozen items unchanged

- C7A prereg ancestor: `5399a2ca73165e8f97cea45934e50baf8ffb3629`
- A2 certified run: `35092206904`
- A2 artifact: `10444488624`
- A2 artifact digest: `sha256:05b36f93e272aebf04f9887b384c695b01b399ca4e816b1549a8e5d7f8189422`
- CLASS commit: `e85808324f51fc694d12e3ed7439552a3c3f9540`
- trace extension blob: `21147e873e6cdee8b55260189eafb8c0e612f02b`
- coverage probe blob: `5be7163070a7fa2709e3ac6cb5835206c8feb5ec`
- eta = 0, memory disabled
- k grid: 128 log-spaced modes, `0.0015 <= k/(h Mpc^-1) <= 1.2`
- `a_i = 0.02`
- all A4 gates and classification rules unchanged

No result from run `35093879845` is evidence for or against the growing-mode bridge; it ended before A4 could be evaluated.
