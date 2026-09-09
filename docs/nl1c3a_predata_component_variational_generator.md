# NL1C3A predata — finite-reference component variational generator

Classification before implementation: **NL1C3A_PREDATA_COMPONENT_VARIATIONAL_GENERATOR**

This gate is created after `NL1C3_SCREENED_RESUMMED_DYNAMICAL_BRIDGE_INCOMPLETE` and before any component-level screened memory source or memory-survival result is inspected.

Historical classifications remain immutable.

## Target

Generate the scalar/metric/aether/auxiliary source system obtained by varying the already frozen covariant action

\[
S_{\rm AeST}+S_{\rm mem}^{\rm NL0B}
\]

around a nonzero finite-amplitude screened reference. No new physical function or fitted coefficient is allowed.

Use the normalized bath field

\[
U_j=\sqrt\eta\,q_j,
\qquad
S_{\rm mem}=\eta\,\widehat S_{\rm mem}[g,A,\phi,q].
\]

The eta=0 tangent sources are the Euler-Lagrange derivatives of `S_hat_mem` evaluated on the memory-off finite reference.

## Frozen scope

The first implementation may use the scalar, weak-field/subhorizon, periodic-box sector needed for the first structure-growth test, but every retained term must descend from the covariant action. Standard matter continuity/Euler nonlinearities follow from minimal coupling. No GR/Poisson modified-gravity closure may be substituted for the AeST field equations.

`beta0={1,0.5,0.1}` remain co-primary. In the certified physical-amplitude regime use the NL1C2 saturated Y coefficient `1/beta0`, with the preserved `2e-6` saturation/stiffness control.

## Required source blocks

The generated eta-linear system must contain, as applicable to the chosen scalar gauge/reduction,

1. scalar-field memory source `delta S_hat_mem / delta phi`;
2. spatial-aether memory source `delta S_hat_mem / delta A_i`;
3. direct metric memory stress `-2/sqrt(-g) delta S_hat_mem/delta g^{mu nu}`;
4. normalized retarded bath equation `delta S_hat_mem/delta q_j=0`;
5. unit-aether constraint terms and projector variations;
6. the memory-off screened AeST Y source from the same action-level reduction.

No source block may be dropped solely because it vanished in the FLRW first-order audit.

## Locked validation gates

Before any memory-survival observable is computed:

- symbolic/automatic variation and independent finite-difference variation agree with relative error `<=1e-6` for scalar, aether and metric source blocks on deterministic nonzero test fields;
- FLRW null test gives direct memory background and linear direct stress consistent with the preserved NL0B audit to normalized absolute error `<=1e-12`;
- finite-reference direct metric memory stress is retained and finite;
- static high-gradient AeST reduction reproduces the frozen Helmholtz equations with normalized residual `<=1e-8`;
- eta=0 memory-off state identity relative L2 `<=1e-10`;
- normalized scalar constraint residual `<=1e-6`;
- all three beta0 values pass independently;
- two finest spatial resolutions agree in preregistered low-mode/state observables within relative L2 `<=5e-3`.

## Classification

All required source blocks are generated with no new physical freedom and all validation gates pass:

**NL1C3A_COMPONENT_VARIATIONAL_GENERATOR_PASS**

A frozen action/source inconsistency is found:

**NL1C3A_COMPONENT_VARIATIONAL_GENERATOR_FAIL**

The action is consistent but an explicit source block or deterministic closure still cannot be generated without an additional theory choice:

**NL1C3A_COMPONENT_VARIATIONAL_GENERATOR_INCOMPLETE**

A PASS permits construction of the first self-consistent screened physical-amplitude baseline and its eta=0 memory tangent. It is not itself a memory-survival, collapse or observational result.
