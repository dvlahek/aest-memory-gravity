# NL1C6D2C6C-R3 repair declaration — modewise full retarded prehistory

## Status and reason for repair

This is a post-FAIL technical repair declaration written after the completed D2C6C-R2 run `34461467620` on commit `c3fe5332ff4450f247953a2a51e6c7504b16b4bc` and before any R3 output is generated.

The R2 result remains historical and unchanged:

`CLASSIFICATION=NL1C6D2C6C_ETA0_NONLINEAR_MEMORY_TANGENT_FAIL`.

R2 passed C1, C2 and C4--C8 and failed only the preregistered C3 linear eta=0 tangent regression. The observed C3 errors were approximately 8.8% in alpha/chi and 8.7% in E, against the frozen 0.5% gate.

Inspection after that FAIL identified a concrete implementation mismatch with the original D2C6C preregistration. The original declaration requires the eta=0 bath and first-order tangent at z=6 to retain the full regular retarded prehistory of the corrected linear AeST solution. The R2 implementation instead chose one common start

`tpre = max(mode_i.tau_lo)`

for the synthesized six-mode real-space field and initialized all bath/tangent states to zero there. Because the six CLASS perturbation histories may have different valid lower-time endpoints, this discards the earlier available retarded history of every mode whose `tau_lo` is smaller than that maximum.

## R3 repair frozen before rerun

R3 changes only the pre-z=6 initialization/propagation of the linear eta=0 bath and tangent.

For each of the six frozen CLASS modes `i` independently:

1. start at that mode's own `tau_lo[i]`;
2. impose the same regular early-time bath and first-order tangent initial condition used in D2C6C, namely zero bath coordinates/momenta and zero eta tangent at the earliest retained regular CLASS point for that mode;
3. propagate that mode's bath and linear tangent from `tau_lo[i]` to the common z=6 time using the same analytic/frozen-background bath step and the same stable-canonical tangent equations already frozen in D2C6C;
4. use that mode's own CLASS `a`, `alpha`, and `theta` history to form its `chi` source during its prehistory;
5. synthesize/sum the six modal bath and tangent contributions only after they have each reached the common z=6 time.

Because the prehistory system is linear at eta=0, modewise propagation followed by synthesis is algebraically equivalent to a full-field propagation from a common time only when all modes share that common valid start. R3 restores the original preregistered full-history requirement without changing the post-z=6 equations.

The base D2C6B trajectory at z=6 and afterwards is unchanged. No finite physical eta is introduced.

## Frozen quantities that R3 must not change

R3 retains exactly:

- corrected CLASS v3.3.4 SHA `e85808324f51fc694d12e3ed7439552a3c3f9540`;
- physical `eta=0`;
- `tau H0=1`;
- primary bath order 39 and control order 47;
- all 27 D2C6B members, with no member removal or selection;
- the stable canonical state and tangent equations;
- the nonlinear Frechet derivative `delta_N`;
- the direct source `M=a^2 Lap(B_chi^(0))`, with `delta_Pchi' += M` and `delta_Sc' += Q M`;
- primary `Nx=128, Nstep=4096`, time control `Nx=128, Nstep=8192`, spatial control `Nx=256, Nstep=4096`, and order-47 control at the primary discretization;
- the corrected CLASS central signed-lambda eta0 variational reference convention;
- the R1 tau1 parser compatibility value `aest_memory_order=39` in the memory-off base CLASS input;
- all original D2C6C gates and thresholds C1--C8 without relaxation or reinterpretation.

In particular C3 remains preregistered at

`alpha <= 5e-3`, `E <= 5e-3`, `chi <= 5e-3`.

No sign, amplitude, monotonicity or completion-order diagnostic is promoted into a gate.

## Interpretation rule

R3 is not licensed to PASS merely because it improves C3. It passes only if all unchanged C1--C8 gates pass. If C3 or any other gate remains false, that result is retained as the R3 FAIL and no finite-positive-eta nonlinear-memory step is licensed.

If R3 passes, the interpretation is limited to demonstrating that the original full-retarded-prehistory specification reconciles the eta=0 nonlinear-memory tangent implementation with the corrected CLASS linear variational reference while preserving the already demonstrated all-27 numerical robustness. It is not an observational detection or finite-eta result.
