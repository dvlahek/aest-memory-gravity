# AeST adjacent-ULP E-RHS decomposition audit — pre-data declaration

Date: 2026-09-13
Branch: `fullj-evolving-weyl-bridge`
Parent science result: `FULLJ_AEST_ULP_LATE_EVOLUTION_DIVERGENCE`
Parent branch commit at lock preparation: `013c59addf8d2a4de3d58a9a021575fb8357a529`

This declaration is fixed before any E-RHS decomposition result is inspected.

## Question

Adjacent binary64 changes in requested k produce material late-time AeST differences while matched GR remains continuous. The previous raw-history audit showed that the exact AeST initial conditions are not materially different, but the auxiliary sector later approaches a common multiplicative rescaling. The present audit asks where the seed first enters the AeST evolution equation.

The target is the Newtonian-gauge AeST auxiliary equation already present in the frozen CLASS/AeST source,

    dy_E = a E_rhs / K_B - (aH) E,

with

    E_rhs = K_Q chi
          -(2-K_B) [ Q Pi/(1+w) + (H+Q) chi - 3 c_a^2 H Q alpha ].

No memory term is active in this audit (`aest_memory_enabled=no`, `aest_eta=0`).

## Frozen adjacent-ULP pairs

Use exactly the four pairs certified in the parent audit:

- k_h=0.10125: bits 4589576883704929730 / 4589576883704929731
- k_h=0.10250: bits 4589637531396803372 / 4589637531396803373
- k_h=0.16500: bits 4592669915990485346 / 4592669915990485347
- k_h=0.19750: bits 4593959187948552946 / 4593959187948552947

Other requested-k tokens remain frozen to the R3/direct 15-digit list.

## Diagnostic build

The frozen CLASS/AeST runtime is commit

    e85808324f51fc694d12e3ed7439552a3c3f9540

with frozen `aest_memory.c` SHA256

    4d5ab5dc7066d4880f06fcfc731d6534ed0ff992e3cc15fb473dddccb25a594f.

Create a separate diagnostic clone. The only permitted source modification is read-only tracing of already computed scalar quantities in the AeST RHS. The dynamics, assignments, branches, solver tolerances, precision parameters, requested k values, and equations must not be changed.

The trace must record at each RHS evaluation for the selected target k:

- k, tau, a
- alpha, E, delta_cdm, theta_cdm
- Q, K_Q, H, c_a^2, w, rho
- chi
- Pi and its three additive pieces when available
- T1 = K_Q chi
- T2 = -(2-K_B) Q Pi/(1+w)
- T3 = -(2-K_B) (H+Q) chi
- T4 = +(2-K_B) 3 c_a^2 H Q alpha
- E_rhs = T1+T2+T3+T4
- D1 = a E_rhs/K_B
- D2 = -(aH) E
- dy_E = D1+D2.

## Evaluation window

The primary localization window is the early radiation-era interval from the first RHS evaluation through a<=3e-4. The full trace may be retained, but no late-time criterion is needed for classification.

For comparing the two ULP traces, interpolate only continuous diagnostic quantities onto the common overlap in ln(a), using no extrapolation. Report both the first common point and a dense common grid.

## Cancellation metric

Define

    kappa_E = (|T1|+|T2|+|T3|+|T4|) / max(|E_rhs|, tiny).

Also define the derivative cancellation metric

    kappa_dy = (|D1|+|D2|) / max(|dy_E|, tiny).

These are diagnostics of subtraction conditioning, not physical instability measures by themselves.

## Gates

### ER-G1 provenance and parent lock

Require frozen CLASS/AeST provenance, frozen adjacent pairs, the parent classification `FULLJ_AEST_ULP_LATE_EVOLUTION_DIVERGENCE`, and all required trace fields.

### ER-G2 instrumentation neutrality

For every selected pair, the diagnostic build must reproduce the corresponding uninstrumented AeST raw-history W solution from the parent NPZ with relative L2 <= 2e-5 for both endpoints. If this fails, no source-level inference is allowed.

### ER-G3 exact-initial-state continuity

At the first common early point require alpha, delta_cdm, theta_cdm, Q, K_Q, H, c_a^2 and w to be pairwise continuous at <=1e-8 relative for at least 3/4 pairs. E is allowed to be near zero and is not used in this continuity gate.

### ER-G4 material E-RHS seeding

At least 2/4 pairs must develop a relative E_rhs or dy_E difference >1e-3 before a=3e-4, while matched state/background quantities in G3 remain continuous at the onset point.

### ER-G5 cancellation localization

For at least 2/4 materially seeded pairs, at the first point where the E_rhs relative difference exceeds 1e-3, require either

    kappa_E >= 1e6

or

    kappa_dy >= 1e6.

This gate tests a cancellation-amplified seed.

### ER-G6 component continuity

At the same onset point, each large additive term Ti must remain continuous between the adjacent-ULP pair at <=1e-5 relative after normalization by max(|Ti_A|,|Ti_B|,sum_j|Tj|*1e-15). A failure indicates a component-level discontinuity instead of smooth cancellation sensitivity.

## Classification priority

1. G1 fail:
   `FULLJ_AEST_ULP_E_RHS_AUDIT_INCOMPLETE`
2. G2 fail:
   `FULLJ_AEST_ULP_E_RHS_INSTRUMENTATION_NONNEUTRAL`
3. G1-G3 pass and G4 fails:
   `FULLJ_AEST_ULP_E_RHS_SEED_NOT_LOCALIZED`
4. G1-G4 pass and G6 fails:
   `FULLJ_AEST_ULP_E_RHS_COMPONENT_DISCONTINUITY`
5. G1-G4 and G6 pass, G5 fails:
   `FULLJ_AEST_ULP_E_RHS_SMOOTH_NONCANCELLATION_SEED`
6. G1-G6 pass:
   `FULLJ_AEST_ULP_E_RHS_CANCELLATION_SEED_CERTIFIED`

## Interpretation lock

No outcome reclassifies historical R3, licenses a new-physics claim, or establishes a physical instability. A cancellation-seed PASS only establishes an equation-level numerical/conditioning mechanism in the frozen AeST linear implementation. A component-discontinuity result licenses a source-level branch/index audit. A smooth non-cancellation seed licenses a dedicated linear-mode/stability analysis.