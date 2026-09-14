# Stable AeST growth–Weyl memory R2a — post-data milestone

Date: 2026-09-14
Branch: `fullj-evolving-weyl-bridge`

## Formal classification

R2a completed with

    STABLE_AEST_GROWTH_WEYL_MEMORY_R2A_SEPARATION_UNRESOLVED

and exit code 1.

R2 remains historically

    STABLE_AEST_GROWTH_WEYL_MEMORY_R2_TANGENT_FAIL

and R1c remains

    STABLE_AEST_FINITE_MEMORY_R1C_LONG_RELAXATION_CERTIFIED.

No historical result is reclassified.

## Gate outcome

Passed:

- R2A-G1 provenance and parent lock
- R2A-G2 transfer-basis and numerical regularity
- R2A-G3 extended individual G/L linearity

Failed:

- R2A-G4 high-leverage separation resolution
- R2A-G5 tight individual-response reproducibility
- R2A-G6 tight separation reproducibility

The finite-memory total-matter and Weyl responses remain individually smooth through eta=0.04 at the primary tolerance.

## Individual-response result

At tol_perturbations_integration=3e-8, both

    G_eta = [D_m(eta)-D_m(0)]/[eta D_m(0)]
    L_eta = [W(eta)-W(0)]/[eta W(0)]

remain highly linear across eta in {0.01,0.02,0.04}.

The maximum individual tangent inconsistency over all anchors and adjacent eta pairs is

    1.8594849258219968e-3.

Thus the R2a failure is not a breakdown of the finite-memory response itself.

## Separation result

The difference

    R_eta = L_eta - G_eta

remains unresolved at all three anchors.

At high leverage, comparing eta=0.02 and eta=0.04:

    k_h=0.09875: E_R_hi=0.5124, Q_hi=1.1384
    k_h=0.16125: E_R_hi=0.5575, Q_hi=0.7940
    k_h=0.19500: E_R_hi=0.5007, Q_hi=0.9972

No anchor satisfies the preregistered resolved-separation criterion.

The independent 1e-8 tolerance check also fails to reproduce R:

    C_R_tol = 1.0010, 1.0772, 0.5319

with corresponding cosines

    -0.6293, -0.7336, 0.8566.

Therefore no physical growth–Weyl separation is certified.

## Differential-floor diagnostics

The strongest floor-like anchor remains k_h=0.195. The undivided differential response

    P_eta = eta R_eta

is almost eta independent:

    ||P_0.01|| = 3.0365903839e-12
    ||P_0.02|| = 3.0391221185e-12
    ||P_0.04|| = 3.0348869304e-12.

The corresponding vector comparisons are

    C_P_12 = 9.6308e-3, cosine = 0.9999539
    C_P_24 = 4.5736e-3, cosine = 0.9999905.

This anchor cleanly exhibits a fixed differential numerical floor.

The lower-k anchors do not satisfy the preregistered floor classification simultaneously, because their residuals are even smaller and change direction/shape under eta and tolerance variation. Consequently the formal project-level outcome remains `SEPARATION_UNRESOLVED`, not `DIFFERENTIAL_FLOOR_SUPPORTED`.

## Direct-ratio post-data check

Computing the differential observable directly through the same-run ratio

    Xi = W / D_m

and then forming

    [Xi(eta)/Xi(0)-1]/eta

does not remove the instability. At the low-k anchor the direct ratio already changes at about the 1e-13 level, while k_h=0.195 retains the same approximately 1/eta residual scaling. Therefore the issue is not caused by algebraically forming L-G after extraction; the physical differential observable itself has reached the double-precision cancellation floor of this finite-difference strategy.

## Interpretation

The certified long-relaxation AeST memory response is real and individually reproducible in both total matter and Weyl channels.

However, within direct finite-eta differencing, those two responses are nearly common-mode and their difference cannot be distinguished from the numerical differential floor.

This result does not license the MCMG bridge, an observational claim, or a detected growth–Weyl lag.

## Next step

Do not extend eta further and do not continue tightening the same finite-difference calculation.

The memory closure has the form

    E' = F_0(y) + eta F_mem(y,q).

At eta=0 the bath trajectory q_0 is driven by the baseline AeST solution but does not feed back into it. Hence the exact first-order forcing is available directly as

    dE'/deta|_0 = - a Q B_chi,raw / (2 K_B).

The repository already contains the historical v0.19w signed variational-forcing machinery implementing this idea. The correct next test is to adapt that machinery to the stable residual state `s`, tau H0=10 and order 20, then amplify the frozen eta=0 forcing with signed lambda probes. This avoids subtracting two almost identical physical eta runs.
