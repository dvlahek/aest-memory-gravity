# AeST E-RHS trace newline repair

Date: 2026-09-13
Parent science preregistration: `0c8dce2022626e194fa90aafe45242f2ed1fc8a7`
Failed instrumentation runner parent: `1f116cc4778a8514136d01f357f48c222f028201`

The first execution of the preregistered E-RHS decomposition audit terminated before any scientific classification. The diagnostic CLASS build succeeded and the trace hook created the target trace file, but `numpy.loadtxt` reported no data.

Inspection of the committed trace patch identified a pure output-format defect. The Python patch used a raw string containing the C format suffix `\\n`. In the generated C source this writes a literal backslash followed by `n`, not a newline. Therefore the header and all numerical trace records were concatenated onto a single physical line beginning with `#`. `numpy.loadtxt(..., comments='#')` consequently treated the complete trace as a comment and returned an empty array.

This repair changes only the diagnostic output formatting from the generated C string `\\n` to `\n` and increments the trace marker from `FULLJ_AEST_ERHS_TRACE_V1` to `FULLJ_AEST_ERHS_TRACE_V2` so the runner is forced to rebuild the isolated diagnostic CLASS copy.

No equations, state assignments, requested k values, ULP pairs, solver settings, gate definitions, thresholds, interpolation rules, or classification logic are changed. The original failed execution remains an incomplete technical run and is not assigned a scientific classification.
