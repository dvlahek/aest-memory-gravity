# C3-R4 pre-data declaration — dense full-history CLASS variational reference repair

## Status and motivation

This repair is preregistered after the completed C3 forensic audit run `34475691607` on commit `ce153d5acfc8a17c0175a20cfbf0435b5bf5bc79`, and before any R4 repaired-reference result is generated.

The historical D2C6C-R3 result remains an immutable FAIL because C3 failed. The forensic audit is diagnostic only and did not license finite positive physical eta.

The forensic audit established two relevant facts before this repair:

1. the offline nonlinear/tangent machinery is numerically healthy and the modal reconstruction audit passes;
2. the old CLASS variational reference is generated from a forcing table traced on the accepted `perturbations_sources` grid. For the six frozen output modes, that table begins only near the z=6 interval, while the dense `k_output_values` perturbation histories and the eta=0 bath begin much earlier. The external forcing loader returns zero before the first tabulated tau. Therefore the old C3 reference omits early retarded forcing history by construction.

R4 repairs only that reference-history truncation. It does not alter the D2C6C equations, bath definition, nonlinear family, physical eta, or any gate.

## Frozen physics and numerical inputs

R4 retains exactly:

- CLASS v3.3.4 SHA `e85808324f51fc694d12e3ed7439552a3c3f9540`;
- the existing AeST patches and patch order used by D2C6C;
- physical `eta=0`;
- tau-H0 = 1;
- bath order 39 for the C3 reference;
- the same six frozen modes `k_h = [0.03,0.05,0.08,0.10,0.15,0.20] h/Mpc`;
- the same nine checkpoints `z = [6,5,4,3,2,1.5,1,0.5,0.2]`;
- central signed-lambda reference with lambda = +/-10, where signed lambda is not physical eta;
- the same D2C6C-R3 stable-canonical offline eta=0 tangent equations and modewise full prehistory;
- offline C3 discretization `Nx=128`, `Nstep=4096`;
- the original D2C6C C3 acceptance threshold: alpha, E and chi relative L2 must each be <= `5e-3`.

No threshold is changed or added to determine D2C6C PASS/FAIL.

## Frozen R4 reference repair

The repaired reference is generated in two CLASS stages.

### Stage A — unforced eta=0 dense bath history

Run corrected CLASS with memory representation enabled, bath order 39, tau-H0=1 and physical eta exactly zero. Since the physical closure multiplies the bath residual by eta, the bath states evolve while the base eta=0 AeST trajectory remains unchanged.

Instrumentation exposes, for each of the six exact `k_output_values`, the already-evolved instantaneous variational forcing

`F_eta0(k,tau) = -a Q B_chi_raw / (2 K_B)`

on the dense perturbation history returned by CLASS. `B_chi_raw` is computed directly from the CLASS bath states `q_j` and the same normalized positive bath definition already used in the compiled equations. No offline bath solver is used to generate this forcing history.

The dense force table must report, for each of the six modes, its first tau, last tau, row count and maximum absolute forcing. The earliest retained dense history for each mode is used without resetting at z=6.

### Stage B — frozen central signed-lambda response

Run fresh CLASS subprocesses for lambda=+10 and lambda=-10 with physical memory disabled and physical eta=0. The external variational forcing is read from the Stage-A six-mode dense table and linearly interpolated in tau.

For k values not equal to one of the six frozen `k_output_values`, the external force is exactly zero. This sparse-k behavior is instrumentation for the reference-only run: linear scalar k modes are independent, and only the six output modes enter C3. A k miss must not abort the run.

For each of the six frozen modes, forcing before its first dense Stage-A point remains zero; no backward extrapolation is permitted. This preserves the regular leading bath IC and avoids inventing pre-output data.

The repaired CLASS tangent is the central derivative `(X(+10)-X(-10))/20` for alpha, E and theta at the same nine checkpoints.

## Predeclared audits

Before interpreting C3, R4 must verify:

1. exactly six dense force histories are present and mapped to the frozen six k values;
2. every dense history has at least 100 finite rows, strictly increasing unique tau after normalization, and begins before the common z=6 time;
3. the Stage-A run uses memory enabled with physical eta=0 and bath order 39;
4. the Stage-B runs use physical memory disabled, physical eta=0 and signed lambda +/-10;
5. the sparse-k loader changes only unmatched-k behavior from abort to zero forcing and leaves exact-k interpolation unchanged;
6. the original D2C6C `reference_compare` function is used unchanged to evaluate the repaired C3 gate against the R3 offline tangent.

Failure of any audit yields `C3_R4_REFERENCE_REPAIR_INCOMPLETE`.

## Classification frozen before output

R4 reports:

- `R4_C3 alpha=<...> E=<...> chi=<...> pass=<bool>` using the unchanged D2C6C metric and threshold;
- a per-mode forensic audit using the already preregistered C3 forensic diagnostics;
- `CLASSIFICATION=C3_R4_DENSE_FULLHISTORY_REFERENCE_PASS` only if all R4 audits pass and all three unchanged C3 errors are <= `5e-3`;
- otherwise `CLASSIFICATION=C3_R4_DENSE_FULLHISTORY_REFERENCE_FAIL` if the run is technically complete but the unchanged C3 gate still fails;
- `FINITE_POSITIVE_ETA_NONLINEAR_MEMORY_LICENSED=False` in either R4 outcome.

Even an R4 PASS does not retroactively convert historical D2C6C-R3 into PASS and does not by itself license finite eta. It only establishes that the historical C3 failure was caused by the truncated reference construction. A subsequent D2C6C repair/revalidation, with its own pre-data declaration, is required before any finite-positive-eta nonlinear-memory stage can be licensed.
