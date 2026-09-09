# NL1B result — second-order AeST+memory dynamical closure

Final classification: **NL1B_SECOND_ORDER_DYNAMICAL_CLOSURE_INCOMPLETE**

Predata file: `docs/nl1b_predata_second_order_dynamical_closure.md`.

Scope: analytic theory audit only. No observational data and no weakly nonlinear growth outcome were used.

This result does **not** modify any historical classification. In particular, v0.77, v0.78, NL0B, NL0C and NL1A remain PASS, and all historical FAIL results remain FAIL.

## Summary

The frozen covariant AeST action plus the NL0B local conservative memory completion is sufficient to define a unique nonlinear theory. However, the preregistered NL1B gate asked for something stronger than theory existence: an explicit second-order scalar FLRW evolution system, including every `O(eta epsilon^2)` memory vertex, the second-order constraint/Noether reduction, and a deterministic numerical state ready for a CLASS-matched weakly nonlinear evolution.

That component-level reduction is not yet present in the repository or in the cited AeST literature. The published literature supplies the full covariant action, the linear cosmological system, the weak-field quasistatic limit, and a full nonperturbative Hamiltonian constraint analysis, but it does not provide the specific second-order FLRW scalar equations required by B4/B5/B8.

The correct preregistered classification is therefore **INCOMPLETE**, not FAIL.

## B1 — first-order AeST reduction

**Status: ESTABLISHED AS A CONTROL, but not sufficient to close NL1B.**

The memory-off first-order equations are the same frozen AeST scalar bridge already used in v0.77/v0.78. The variables and closure are

\[
\chi=Q(u_A+\alpha),
\]

\[
\Pi_A=c_{ad}^2\delta_A+
\frac{c_{ad}^2 k^2}{3a^2\rho_A}
[K_BE+(2-K_B)\chi],
\]

with the preserved `delta_A`, `Theta_A`, `alpha`, and `E` evolution. This is also the linearization target of the frozen covariant action.

## B2 — first-order memory reduction

**Status: PASS by NL0B.**

The local auxiliary-vector completion reduces exactly to

\[
q_j''+2\mathcal Hq_j'+a^2\omega_j^2q_j
=ak\omega_j\sqrt{w_j}\chi,
\]

and

\[
\Delta E_{rhs}=-\frac{\eta Q}{2}B_{\chi,raw}.
\]

No new first-order Einstein stress or independent first-order scalar constraint is generated.

## B3 — NL0C Y-sector vertex

**Status: PASS by NL0C/NL1A.**

The first nonzero Y-sector field-equation contribution is

\[
\Delta\mathcal E_\phi^{(2)}=
\frac{2(2-K_B)}{(1+\beta_0)a_0}
\nabla_{phys}\cdot
(|\nabla_{phys}\chi|\nabla_{phys}\chi).
\]

Its pseudospectral implementation passed the NL1A operator tests.

## B4 — all quadratic memory vertices

**Status: INCOMPLETE.**

The NL0B action fixes these vertices uniquely, but the complete component expansion through `O(eta epsilon^2)` has not yet been written out. At this order the result receives contributions from the perturbations of

- `X_mu = h_mu^nu nabla_nu phi`;
- the aether-orthogonal projector;
- the projected aether derivative `D_A`;
- the metric used in the auxiliary kinetic and completed-square terms;
- the invariant volume element;
- the orthogonality constraint `A.U_j=0`;
- the direct memory stress tensor, which begins precisely at second perturbative order.

It would be incorrect to retain only a nonlinearized Fourier `k chi` source. The preregistered B4 gate therefore cannot be declared closed yet.

## B5 — second-order constraint / Noether closure

**Status: INCOMPLETE AT COMPONENT LEVEL.**

Diffeomorphism invariance of the combined frozen action guarantees a Noether identity for the exact equations, and the published Hamiltonian analysis shows that nonlinear AeST has a consistent constrained phase space. However, the scalar projection of that identity around FLRW has not yet been explicitly reduced together with the new memory auxiliary fields through second order.

Therefore we cannot yet state which second-order scalar equation is redundant in the exact numerical variable set without performing this reduction.

## B6 — static weak-field control

**Status: PASS AS A THEORY LIMIT.**

With memory off, the frozen AeST branch reduces to the published two-potential weak-field system

\[
\Phi=\tilde\Phi+\chi,
\]

\[
\nabla^2\tilde\Phi+\mu^2\Phi
=\frac{4\pi G_N}{1+\beta_0}\rho_b,
\]

\[
\nabla^2\tilde\Phi=
\nabla\cdot(\mathcal J_Y\nabla\chi),
\]

and the NL0C deep-MOND asymptote produces the already frozen quadratic gradient source.

## B7 — no new free nonlinear coefficient

**Status: PASS AT THE ACTION LEVEL.**

No new coefficient is required through the requested order. The analytic sector is fixed by the frozen AeST action and Exp `K(Q)` branch, the nonanalytic Y-sector by `a0` and the co-primary `beta0={1,0.5,0.1}`, and the memory sector by the NL0B action and preserved positive Drude spectrum.

This means the obstacle is algebraic/implementation closure, not missing physics freedom.

## B8 — deterministic numerical initial-value state

**Status: INCOMPLETE.**

A full exact Hamiltonian formulation of memory-free AeST exists, but the repository does not yet contain the second-order FLRW scalar reduction of that system augmented by the NL0B memory variables. Consequently the exact evolution/constraint solve order required by the preregistered gate has not yet been frozen.

A GR/Poisson toy replacement is explicitly rejected: it would not satisfy B1 and would discard the time-dependent Q/aether dynamics that produced the certified linear signal.

## B9 — linear numerical cross-check

**Status: NOT REACHED.**

The CLASS comparison must be performed only after the reduced NL1B evolution system exists. No tolerance was inspected and no growth result was generated.

# Classification

Because B4, B5 and B8 remain unresolved at the explicit component/implementation level, and B9 therefore cannot yet be executed,

\[
\boxed{\text{NL1B\_SECOND\_ORDER\_DYNAMICAL\_CLOSURE\_INCOMPLETE}}
\]

This is not evidence against the nonlinear AeST+memory physics. It means the originally preregistered full second-order FLRW component reduction was too large to treat as a single undocumented algebraic step.

## Clean continuation

The next gate must not weaken the physics by inserting a phenomenological Poisson closure. Instead, it will formulate the **directional second-order eta=0 tangent hierarchy directly from functional derivatives of the frozen covariant action**. This is sufficient for the first strong nonlinear question — the memory derivative of the weakly nonlinear response at eta=0 — and avoids choosing any finite physical eta before the weakly nonlinear response itself is controlled.

The directional formulation also treats the nonanalytic `Y^(3/2)` term correctly: it uses its homogeneous directional second-order operator instead of pretending that a universal bilinear `F2` kernel exists.

References used for scope checking:

- C. Skordis and T. Zlosnik, Phys. Rev. Lett. 127, 161302 (2021).
- C. Skordis and T. Zlosnik, *Aether scalar tensor theory: Linear stability on Minkowski space*, Phys. Rev. D (2022).
- M. Bataki, C. Skordis and T. Zlosnik, Phys. Rev. D 110, 044015 (2024).
- P. Verwayen, C. Skordis and C. Boehm, MNRAS 531, 272–289 (2024).
