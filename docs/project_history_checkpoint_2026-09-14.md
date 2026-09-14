# Project history checkpoint — 2026-09-14

This is a post-data history checkpoint for the `fullj-evolving-weyl-bridge` branch. It records the result sequence without retroactive reclassification.

## Host-independent memory-gravity line

The MCMG line currently has three clean positive checkpoints:

1. `MCMG_CAUSAL_FIRST_MOMENT_UNIVERSALITY_PASS`
2. `MCMG_SELF_CONSISTENT_GROWTH_WEYL_MEMORY_PASS`
3. `MCMG_GROWTH_WEYL_MEMORY_GENERALITY_PASS`

The central first-order relation is

    d_eta(w-g)|_{eta=0} = [M[P_GR]-P_GR]/P_GR,

and, in the short-memory limit,

    (w-g)/(eta u) -> - d ln P_GR / d(H0 t).

The defensible physical interpretation at this stage is a causal gravitational response with finite relaxation time. This is a viscoelastic-type memory effect, not yet a demonstration of permanent softening or irreversible loss of stiffness.

## AeST forensic line

Historical results remain fixed in the order obtained:

1. `FULLJ_CORRECTED_CLASS_SPECTRAL_FRINGE_NUMERICAL_CONTROL_FAIL`
   - historical direct CLASS fringe test failed its numerical-control requirement.
   - this classification is never reclassified.

2. `FULLJ_CLASS_FRINGE_AEST_ULP_SENSITIVITY_CERTIFIED`
   - adjacent binary64 changes in serialized k produced order-one AeST response while GR remained stable.
   - this certified AeST-specific ULP sensitivity only, not physical instability.

3. `FULLJ_AEST_ULP_LATE_EVOLUTION_DIVERGENCE`
   - auxiliary trajectories differed by near-multiplicative rescaling.
   - the preregistered first-point amplitude-discontinuity criterion did not pass.

4. `FULLJ_AEST_ULP_E_RHS_COMPONENT_DISCONTINUITY`
   - instrumentation was neutral and initial states were continuous.
   - the early seed was localized to E_rhs components T1 and T3.
   - outer E_rhs cancellation was excluded because kappa_E and kappa_dy were approximately one.

5. Post-hoc mechanism localization
   - both T1 and T3 share

         chi_AeST = Q_AeST [a theta/k^2 + alpha].

   - the leading adiabatic initial condition imposes alpha = -a theta/k^2 and E=0, so chi is a small residual reconstructed from two nearly cancelling quantities.
   - raw traces gave an internal subtraction condition number of order 1e12.

6. `FULLJ_AEST_STABLE_CHI_REFERENCE_MISMATCH`
   - an algebraically equivalent redundant state

         s = a theta/k^2 + alpha,
         chi = Q s

     removed the adjacent-ULP pathology on all four known pathological pairs and all four held-out anchors.
   - however, calm-control trajectories differed materially from the historical subtraction-based solution, so the intervention was not accepted as a final stable host at this stage.

7. `FULLJ_AEST_STABLE_CHI_NOT_PRECISION_CONVERGED`
   - stable-coordinate tight-tolerance errors were already extremely small, but the preregistered monotonic-trend gate passed only 7/10 anchors instead of the required 8/10.
   - the classification remains a historical FAIL.

8. `FULLJ_AEST_STABLE_CHI_PRECISION_FLOOR_CERTIFIED`
   - preregistration: `4b7acaf908e91a83b2fa69260ae3dbd13ad2226b`.
   - all five precision-floor gates passed.
   - the three previously nonmonotone targets and one monotone control reached a Cauchy precision plateau at tolerances 1e-7 and 3e-8.
   - maximum relL2 change from 1e-7 to 3e-8: 9.092347260801674e-09.
   - maximum relL2 change from 3e-7 to 3e-8: 1.5500121286924154e-08.
   - maximum tight adjacent-ULP W relL2: 3.0999325079514408e-09.
   - maximum residual-state identity relL2: 1.1763716163231164e-13.
   - `stable_AeST_host_followup_licensed = true`.

## Current interpretation

The AeST fringe/ULP pathology is now supported as a numerical state-coordinate conditioning problem dominated by subtraction in the derived residual `chi`, rather than evidence for a physical unstable mode. The direct residual state `s` removes the ULP pathology and reaches a tight precision plateau while satisfying the algebraic identity at approximately 1e-13 relative L2.

Historical FAIL classifications remain part of the record and are not retroactively changed.

## Current project position

The clean scientific line is now

    host-independent causal memory gravity
        +
    independently stabilized relativistic AeST host.

The next licensed physics step is therefore a stable-AeST finite-memory test, with memory-off regression first, followed by a small-eta tangent response and comparison to the MCMG growth-Weyl consistency relation. No observational or new-physics claim is licensed by the numerical stabilization alone.
