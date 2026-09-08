# Preserved interpretation of v0.67 and v0.68

This note is result-informed and was added after completion of v0.67 and v0.68. It does not alter, relabel, rerun, or rescue either historical classification.

## Historical classifications retained unchanged

- v0.67: `V067_GROWTH_KERNEL_CLOSURE_AFFINITY_FAIL`
- v0.68: `V068_LINEAR_SCALE_MEMORY_RESPONSE_MAP_FAIL`

These FAIL labels remain authoritative for the preregistered numerical gates used in those runs.

## v0.67 result retained

v0.67 established that the formally integrated sigma8 tangent response is dominated by high-k support in the frozen linear AeST implementation. The 8--16 h/Mpc shell still carried a substantial fraction of the manual sigma8^2 integral, so the preregistered UV-closure gate failed. The four-lambda integrated tangent response itself was highly stable. This result is therefore retained as evidence for a strong scale-dependent small-scale response of the linearized AeST memory sector, not as a certified late-time sigma8 prediction.

A physically relevant interpretation to test in later work is that the high-k enhancement may indicate approach to the model's nonlinear regime rather than a disposable numerical artifact. Linear theory cannot determine the nonlinear saturation or final small-scale power.

## v0.68 result retained

v0.68 directly sampled the previously fixed v0.63 low-k grid. It failed its interpolation and global lambda-affinity gates, so the reported fixed-grid matter/Weyl amplitudes are not promoted as certified measurements of the tangent map.

Nevertheless, the run is retained because it showed a structured transition: very small responses at k=0.03--0.05 h/Mpc, larger responses by k=0.08 h/Mpc, and much stronger scale dependence around k=0.1--0.2 h/Mpc. The Weyl response was often substantially more lambda-stable than the matter response at the same points. These observations motivate a new direct-evaluation test that does not use the failed native-grid interpolation step.

## Guardrail for follow-up

Later versions may test hypotheses suggested by these results, but must identify themselves as result-informed follow-ups and must not modify the v0.67/v0.68 frozen model, historical classifications, or stored result artifacts. In particular, a later nonlinear-onset diagnostic must not be described as evidence that nonlinear dynamics have already been simulated; it can only test where the linear solution reaches conventional dimensionless-power thresholds and how the eta=0 tangent shifts those thresholds.
