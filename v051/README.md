# v0.51 / v0.52 certification plan

No AeST physics, locked parameter, nuisance finite-difference step, covariance definition, CLASS commit, parameter bound, trust cap, or certification threshold is changed in these tests.

## v0.51 objective reproduction audit

Re-evaluates the exact four reported v0.42 endpoint parameter vectors through the locked v0.31/v0.50 objective construction. No optimization is performed. The predeclared reproduction gate is relative difference < 1e-6 for every endpoint. A failure is diagnostic: it confirms that the old reported endpoint objective/reference state is not reproduced and prevents interpretation of the v0.50 bridge topology until provenance is resolved.

## v0.52 LM continuation certification

Starts only from the four exact verified v0.50 endpoints from run 34014387686 and reuses the v0.50 deterministic CV-normalized LM implementation verbatim for eight additional iterations. The certification gates remain exactly: all four finite, every final baseline CV S/N < 5, final four-start spread < 0.5, and maximum normalized condition < 1e8.

v0.52 is workflow-dispatch only so that v0.51 can be inspected first. The model is not to be tuned in response to either result.
