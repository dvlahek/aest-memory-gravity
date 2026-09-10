# NL1C6D2C6A pre-result clarification: fixed-grid endpoint bookkeeping

Status: **LOCKED BEFORE ANY I1--I8 D2C6A RESULT**.

The first D2C6A execution that entered the physical integrator completed the preregistered fixed-step linear-control evolution far enough to expose a checkpoint bookkeeping defect, but it did not emit or classify I1--I8. The integrator stored 8 of the 9 frozen redshift checkpoints and then `linear_class_compare()` raised `IndexError` when requesting the ninth.

Inspection shows that the initial `z=6` state is explicitly stored before the RK4 loop. The missing checkpoint is the final `z=0.2` endpoint. The implementation advanced the bookkeeping variable by repeated floating-point addition `t = t + h`. After 4096 fixed steps, accumulated roundoff can leave the final numerical label slightly below the preregistered `t1`, so the final checkpoint test can miss `tau_check[-1]` even though the RK4 trajectory has completed all 4096 steps.

This is not a change to the physical or numerical design. Classical fixed-step RK4 is defined on the grid

`tau_n = tau_0 + n h`,  `h = (tau_1-tau_0)/Nstep`.

The corrected implementation therefore computes each step label from that fixed grid rather than by cumulative addition, and sets the final step label exactly to the already frozen `tau_1`. The RK4 equations, right-hand side, `Nx`, `Nstep`, physical interval, initial state, completion member, CLASS forcing, and all preregistered I1--I8 thresholds remain unchanged.

No trajectory value, convergence value, linear-control error, nonlinear response, or gate result was inspected before this clarification. The failed workflow is classified as an implementation/checkpoint-bookkeeping failure, not as `NL1C6D2C6A_PHYSICAL_TIME_SCALAR_CURRENT_INTEGRATOR_FAIL`.
