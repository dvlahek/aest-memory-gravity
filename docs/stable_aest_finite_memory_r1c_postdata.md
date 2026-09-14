# Stable AeST finite-memory R1c — post-data milestone

Date: 2026-09-14
Branch: `fullj-evolving-weyl-bridge`

## Formal classification

R1c completed with

    STABLE_AEST_FINITE_MEMORY_R1C_LONG_RELAXATION_CERTIFIED

and exit code 0.

All preregistered gates passed:

- R1C-G1 provenance and parent lock
- R1C-G2 numerical regularity
- R1C-G3 held-out eta-tangent consistency
- R1C-G4 bath-order tangent consistency
- R1C-G5 resolved nonzero response

Historical R1 and R1b classifications remain unchanged. In particular,

    STABLE_AEST_FINITE_MEMORY_R1_ETA_SMOOTHNESS_FAIL

and

    STABLE_AEST_FINITE_MEMORY_R1B_ETA_TANGENT_FAIL

remain historical results and are not reclassified.

## Certified regime

The certified finite-memory regime is

    tau H0 = 10,
    tol_perturbations_integration = 3e-8,
    k_h in {0.09875, 0.16125, 0.19500},
    eta in {0, 0.005, 0.01},
    memory_order in {16,20}.

The three k values were held out from the R1b primary anchor set.

## Eta-tangent consistency

For each held-out k and both bath orders, the matched-bath Weyl tangent

    Q_W(eta) = [W(eta)-W(0)]/eta

was consistent between eta=0.005 and eta=0.01.

Maximum eta-tangent discrepancy:

    max E_eta = 8.544617938092112e-3.

All six `(k,order)` cells passed the strict preregistered eta-consistency gate.

Resolved matched response amplitudes at eta=0.01 were in the range

    A_M_W = 5.250515580565734e-12 ... 1.3813516700371713e-10.

## Bath-order consistency

The order-16 and order-20 tangent estimates agreed at all three held-out k anchors.

Per-anchor tangent discrepancies were approximately

    k_h=0.09875: E_order = 9.2941e-3, cosine = 0.9999593225
    k_h=0.16125: E_order = 8.5469e-3, cosine = 0.9999751797
    k_h=0.19500: E_order = 3.2757e-3, cosine = 0.9999992946

Thus the certified long-relaxation tangent is not specific to the order-16 finite-bath discretization.

## Post-data diagnostic physics pattern

Inspection of the saved order-20 eta=0 and eta=0.01 histories shows that the relative matched Weyl tangent grows strongly toward late times. At z=0.2,

    (Delta W / eta) / |W_0| approximately
      1.74e-9  at k_h=0.09875,
      1.89e-8  at k_h=0.16125,
      4.57e-8  at k_h=0.19500.

The internal AeST `delta_cdm` proxy has the opposite late-time sign on the same cells. At z=0.2 its relative tangent per unit eta is approximately

     -2.06e-9,
     -2.23e-8,
     -5.43e-8,

respectively.

Therefore the difference between metric/Weyl and internal growth-proxy response is late-time enhanced in the certified branch. This is a post-data diagnostic only. `delta_cdm` is an internal AeST effective-dark-component perturbation and is not the final total-matter growth observable.

## Interpretation

R1c certifies only the long-relaxation branch. It does not certify tau H0=1.

The formal interpretation flag is

    long_relaxation_growth_Weyl_followup_licensed = true.

This licenses the next science test: construct a physically appropriate total-matter growth observable in the stable AeST host and compare its matched memory tangent with the matched Weyl tangent, using the certified tau H0=10 branch.

The next test should not use the internal `delta_cdm` proxy as the final growth observable. The target quantity should be the total matter growth response extracted consistently from CLASS perturbations. The primary science question is then if the stable AeST long-memory branch produces a reproducible growth-Weyl lag structure compatible in sign and late-time activation with the host-independent MCMG first-moment result.

No observational detection, permanent elasticity loss, or new-physics claim is licensed by R1c alone.
