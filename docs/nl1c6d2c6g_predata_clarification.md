# D2C6G pre-data clarification — feedback-off diagnostic scope

Date: 2026-09-11

This clarification is committed before the D2C6G implementation and before any D2C6G target output. It does not change any physics equation, parameter, member coverage, or PASS/FAIL threshold in the parent D2C6G preregistration.

The primary feedback run still covers all 27 frozen completion members at `eta=0.125`, direct bath 256, `Nx=128`, `Nstep=4096`.

To keep this first gravitational-feedback stage focused on physics rather than duplicating the entire no-feedback computation, the explicit feedback-off rerun is restricted to the same three preregistered sentinel members already used by gate G3 and the convergence controls:

1. `sigma=+1 | kind=simple | beta0=0.1`;
2. `sigma=0 | kind=exponential | beta0=0.5`;
3. `sigma=-1 | kind=sharp | beta0=1`.

For those three sentinels, feedback-on versus feedback-off state/E displacement is reported and G3 remains unchanged.

For all 27 primary members, report the feedback-on metric response (`delta_phi_mem`, `delta_psi_mem`, `delta(phi+psi)_mem`), health, stress decomposition and completion-family spread. The earlier parent D2C6E/F no-feedback result remains the scientific reference for the retained sector, but no additional 27-member no-feedback rerun is required as a D2C6G diagnostic.

This clarification only narrows a non-gating duplicated diagnostic and reduces unnecessary computation. It does not relax G1-G9.
