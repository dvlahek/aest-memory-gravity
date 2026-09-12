# Full-J evolving-FLRW Weyl bridge predata

Status: **PREREGISTERED BEFORE EVOLVING-WEYL OUTPUT**.

Frozen label:

`FULLJ_EVOLVING_WEYL_BRIDGE_PREDATA`

## Scientific question

The static/fixed-a full-J program is now locked through the dense map, local Jacobian, static Weyl identity, local covariance diagnostic, and finite phase-robustness PASS. The remaining blocker for cosmological lensing is not another static robustness test. It is the metric bridge from the already action-derived evolving nonlinear AeST scalar-current trajectories to the evolving Newtonian-gauge Weyl field

`W = Phi + Psi`.

This stage asks if the D2C5 action-derived longitudinal FLRW system and its existing D2C6 trajectory variables contain a parameter-free, constraint-consistent reconstruction of `Phi`, `Psi`, and `W` that (i) reproduces corrected linear CLASS in the linear limit and (ii) reproduces the locked static full-J Weyl identity in the fixed-a/static limit.

No observational data or ACT likelihood is used.

## Frozen upstream

Required ancestors/results:

1. `NL1C6D2C5_ACTION_LEVEL_FLRW_LONGITUDINAL_REDUCTION_PASS`.
2. `NL1C6D2C6B_ALL27_PHYSICAL_NONLINEAR_TRAJECTORIES_PASS` lineage, which evolves the action-derived nonlinear scalar-current sector.
3. `NL1C6D2C6G_ETA0_DIRECT_METRIC_TANGENT_CALIBRATION_PASS`, which already fixes the Newtonian-gauge metric projection convention and defines `W=Phi+Psi`.
4. `FULLJ_MODE_COUPLING_JACOBIAN_NODE_COUPLING_SUPPORTED`.
5. `FULLJ_PHASE_ROBUSTNESS_PASS`.
6. Static full-J Weyl identity `W=2 Phi` is licensed **only** in the static/fixed-a dust limit and is used only as a regression target.

Physical memory coupling remains `eta=0` in this stage.

## No-new-physics rule

The bridge must be derived from the retained D2C5 weak-field action/constraints and the existing canonical variables. The following are forbidden:

- imposing `Phi=Psi` at finite time,
- promoting the static identity `W=2 Phi` to evolving FLRW,
- inserting a GR/Poisson closure in place of the AeST constraints,
- fitting an arbitrary gravitational-slip function,
- introducing a new amplitude, damping, interpolation, or lensing parameter,
- modifying the already locked nonlinear scalar-current trajectories to improve the metric result.

If the retained action/order does not determine all terms required for evolving `Phi`, `Psi`, and `W`, the correct classification is an incomplete bridge, not an ad hoc completion.

## Frozen metric convention

Newtonian gauge is retained. The evolving Weyl field is

`W = Phi + Psi`.

The metric reconstruction must use the Hamiltonian, momentum, and shear constraints in the same normalization/convention already used by the D2C6G metric projection. Any canonical-to-effective-source mapping must be explicitly derived and recorded.

## Audit and regression gates

### G1. Canonical source traceability

Every term entering the Hamiltonian density source, momentum source, and scalar shear source must be traceable to the D2C5 reduced action/canonical equations or an already locked corrected matter source. No term may be inferred from desired lensing behavior.

Gate: symbolic/algebraic normalized mismatch `<=1e-12` for all identities with a closed analytic reference.

### G2. Linear CLASS regression

Turn off the nonlinear constitutive departure so that the trajectory is in the corrected linear AeST limit. Reconstruct `Phi`, `Psi`, and `W` from the bridge and compare to the corrected Newtonian-gauge CLASS histories on the existing D2C6 calibration grid.

Frozen relative-L2 gate for each of `Phi`, `Psi`, and `W`:

`<=5e-3`.

This uses the already established D2C6 linear-regression accuracy scale; it is not refit after seeing the result.

### G3. Static/fixed-a full-J regression

Freeze the background scale factor and remove explicit time derivatives/momentum flow so that the bridge reduces to the locked static dust problem. For the same full-J constitutive state, require

`Psi -> Phi`,

`W -> 2 Phi`,

and require the reconstructed static `Phi` operator to match the locked full-J static operator.

Frozen normalized regression gate:

`<=1e-10`.

### G4. Constraint closure

On the primary evolving nonlinear trajectories, evaluate the reconstructed Hamiltonian, momentum, and shear constraints after metric reconstruction.

Frozen maximum normalized residual gate:

`<=1e-8` for each reconstructed metric constraint family.

The scalar-current canonical constraint already has its own tighter upstream controls and is not weakened here.

### G5. Finite evolving Weyl output

For all 27 co-primary nonlinear trajectory members, reconstructed `Phi`, `Psi`, and `W` must be finite at all retained checkpoints and Fourier modes used by the D2C6 trajectory grid.

No sign, amplitude, or proximity-to-GR gate is imposed. This stage certifies the bridge, not agreement with data.

### G6. Static-versus-evolving distinction

The implementation must explicitly report the evolving gravitational slip

`slip = Psi - Phi`

and must fail the audit if it silently enforces zero slip away from the static regression limit.

## Primary output

If all gates pass, store the evolving Fourier histories

`Phi_k(t), Psi_k(t), W_k(t)`

for every retained D2C6 mode and all 27 trajectory members, plus constraint residuals and linear/static regression diagnostics.

These histories are an intermediate theory object. They are not yet a continuous cosmological Weyl power spectrum and are not yet a lensing `C_L` prediction.

## Classification

All source-traceability, linear CLASS, static full-J, constraint, finite-output, and slip-distinction gates pass:

`FULLJ_EVOLVING_WEYL_BRIDGE_PASS`

The retained weak-field action/order is insufficient to reconstruct one or more required metric source terms without an extra closure assumption:

`FULLJ_EVOLVING_WEYL_BRIDGE_INCOMPLETE_METRIC_CLOSURE`

A derived bridge exists but violates one or more frozen regression/constraint gates:

`FULLJ_EVOLVING_WEYL_BRIDGE_FAIL`

## Scope after a PASS

A PASS licenses construction of a separately preregistered evolving Weyl covariance/power diagnostic on the same theory grid. It does **not** by itself license ACT likelihood evaluation.

Always:

- `EVOLVING_WEYL_BRIDGE_TESTED=True`
- `ACT_LIKELIHOOD_LICENSED=False`
- `OBSERVATIONAL_CLAIM_LICENSED=False`
- `NO_STATIC_W_EQUALS_2PHI_PROMOTION=True`
