# D2C6C-R7 pre-data declaration — full all-27 certification with corrected frozen-metric C3 reference

## Status and purpose

This is a formal repair/certification stage for the already preregistered D2C6C eta=0 nonlinear-memory tangent test. It does not redefine the D2C6C physics, trajectory family, numerical resolutions, or acceptance thresholds.

Historical D2C6C R2/R3/R4/R5 FAIL results remain immutable. In particular, they are not reclassified after the fact. The separate R6 diagnostic/correction run `34500820787` established that the C3 reference must implement the same frozen-metric/frozen-external-matter variational problem specified by the original D2C6C preregistration. R6 itself is not a full D2C6C PASS because it evaluated only the corrected C3 linear reference gate.

The sole scientific repair licensed in R7 is replacement of the previously inconsistent C3 full-feedback CLASS reference by the R6 frozen-metric CLASS-variable tangent reference. All other D2C6C components remain unchanged.

## Frozen implementation scope

The full nonlinear certification continues to use the existing D2C6C implementation:

- `nl1c6d2c6c/r3_modewise_full_prehistory.py`,
- the underlying `nl1c6d2c6c/eta0_nonlinear_memory_tangent.py`,
- the same stable canonical state `y=(alpha,chi,P_chi,S_c)`,
- the same tangent variables and direct memory source,
- the same modewise retarded prehistory,
- the same nonlinear constitutive family and all 27 Cartesian members.

No equation in the nonlinear base, bath, or tangent evolution is changed in R7.

The corrected linear C3 reference is rebuilt inside the R7 workflow using `nl1c6d2c6c_r6/build_frozen_metric_reference.py`. It is not copied from, selected from, or tuned to the successful R6 artifact. The reference therefore remains reproducible from the frozen repository code.

The isolated CLASS build uses the already validated R5 eta=0 passive-bath decoupling repair so that physically decoupled bath states do not contaminate the CLASS core trajectory at `eta=0`. This does not alter the finite-positive-eta closure or any positive-eta physics. R7 itself evaluates only `eta=0`.

## Frozen physical and numerical settings

All original D2C6C settings remain unchanged:

- physical `eta=0`,
- `tau H0=1`,
- primary bath order 39 and control order 47,
- six frozen Fourier modes and phases,
- nine frozen checkpoints from `z=6` to `z=0.2`,
- all 27 members from `sigma in {-1,0,+1}`, `kind in {simple,exponential,sharp}`, `beta0 in {1,0.5,0.1}` with `epsilon_mix=0.25`,
- primary `Nx=128`, `Nstep=4096`,
- time control `Nx=128`, `Nstep=8192`,
- spatial control `Nx=256`, `Nstep=4096`,
- full modewise retarded prehistory without a reset at `z=6`.

The external CLASS metric/matter fields are held fixed at eta=0 exactly as specified in the original D2C6C preregistration. The corrected C3 reference therefore does not include an Einstein/matter feedback tangent that is absent from the preregistered offline problem.

## Locked gates

The original C1-C8 gates and thresholds are retained exactly, without loosening:

- C1: provenance and exact 27-member coverage,
- C2: stable-canonical memory bridge `<=1e-10` and nonlinear flux Jacobian FD `<=1e-6`,
- C3: relative L2 errors in `alpha`, `E`, and `chi` each `<=5e-3`,
- C4: finite all-27 trajectories, tangent constraint `<=1e-10`, and inherited positive `1+j_eff`,
- C5: order-39/order-47 bath convergence `<=1e-2`,
- C6: time convergence `<=2e-3`,
- C7: spatial convergence `<=5e-3`,
- C8: eta0-only scope clean.

No sign, ordering, response-amplitude, monotonicity, or preferred-member condition is introduced.

## Binding continuation rule

R7 PASS requires all original C1-C8 gates to pass in the single all-27 run. Only then may the existing D2C6C implementation's own output

`FINITE_POSITIVE_ETA_NONLINEAR_MEMORY_LICENSED=True`

be treated as the formal license for a separately preregistered finite-positive-eta nonlinear-memory stage.

If any C1-C8 gate fails, R7 is a formal FAIL and finite positive eta remains unlicensed. If the workflow encounters a purely technical execution fault before the gates are evaluated, the run is INCOMPLETE and may be repaired only by a separately identified technical repair that does not change the frozen physics or thresholds.

No finite-positive-eta run, likelihood evaluation, parameter refit, observational selection, or post-data threshold/member change is permitted in R7.
