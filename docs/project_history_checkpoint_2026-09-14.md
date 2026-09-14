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

## Stable AeST finite-memory line

9. `STABLE_AEST_FINITE_MEMORY_R1_ETA_SMOOTHNESS_FAIL`
   - all 18 finite-memory runs were numerically regular and the eta=0 memory-enabled system reproduced the stable host within the preregistered regression tolerance.
   - the raw response was measured against `memory_enabled=no`; this mixed the physical coupling response with a solver offset from integrating the enlarged bath state vector.
   - the small-eta smoothness and raw material-response gates therefore failed.
   - this historical FAIL is not reclassified.

10. `STABLE_AEST_FINITE_MEMORY_R1B_ETA_TANGENT_FAIL`
   - introduced the matched-bath response

         Delta^M W(eta,tau) = W(eta,tau)-W(0,tau)

     with `memory_enabled=yes` in both terms.
   - tau H0=10 showed a clean eta tangent and tight-tolerance reproduction on all three anchors.
   - tau H0=1 remained unresolved and failed both the eta-tangent and tolerance-reproducibility gates.
   - the overall preregistered R1b classification therefore remains FAIL.

11. `STABLE_AEST_FINITE_MEMORY_R1C_LONG_RELAXATION_CERTIFIED`
   - preregistration: `68a9341a9648cd490dfb9b599577ae3e1e296086`.
   - certified regime: tau H0=10, tolerance 3e-8, eta in {0,0.005,0.01}, held-out k_h in {0.09875,0.16125,0.19500}.
   - both bath orders 16 and 20 were tested.
   - all 18 runs were finite.
   - all six `(k,order)` cells passed the strict eta-tangent gate.
   - maximum eta-tangent discrepancy: 8.544617938092112e-3.
   - order-16/order-20 tangent discrepancies: 9.2941e-3, 8.5469e-3, 3.2757e-3.
   - minimum order cosine: 0.9999593224903045.
   - all nonzero matched-response gates passed.
   - `long_relaxation_growth_Weyl_followup_licensed = true`.
   - tau H0=1 remains explicitly uncertified.

## Current interpretation

The historical AeST fringe/ULP pathology is supported as a numerical state-coordinate conditioning problem dominated by subtraction in the derived residual `chi`, rather than evidence for a physical unstable mode. The direct residual state `s` removes the ULP pathology and reaches a tight precision plateau.

Within this stabilized host, the positive finite-bath memory sector has now been independently certified in the long-relaxation branch. The matched Weyl response is nonzero, first-order in eta, stable under tighter integration tolerance, reproduced on held-out k modes, and insensitive at the percent level to changing the finite-bath discretization from order 16 to order 20.

Historical FAIL classifications remain part of the record and are never retroactively changed.

## Current project position and roadmap

The clean scientific line is now

    host-independent causal-memory theorem (MCMG)
        +
    numerically stabilized relativistic AeST host
        +
    certified long-relaxation finite-memory Weyl tangent in AeST.

The next test is no longer numerical host forensics. It is the first direct physics bridge:

    R2: stable AeST total-matter growth vs Weyl memory separation
        -> R3: compare the redshift shape with the MCMG first-moment relation
        -> R4: project the certified response into f sigma8 and lensing observables
        -> data/forecast only after the theory-side bridge is established.

For R2 the growth observable must be the CLASS total-matter transfer `d_m`, not the internal AeST `delta_cdm` proxy. The Weyl observable is taken consistently from the same CLASS transfer basis through `phi+psi`. No observational, permanent-elasticity-loss, or new-physics claim is licensed at this checkpoint.