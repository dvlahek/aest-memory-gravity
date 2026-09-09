# NL1C3B predata — longitudinal 3+1 memory bridge

Classification before implementation: **NL1C3B_PREDATA_LONGITUDINAL_3PLUS1_MEMORY_BRIDGE**

This gate is frozen after `NL1C3A_COMPONENT_VARIATIONAL_GENERATOR_PASS` and before inspecting any 3+1 longitudinal component result.

Historical classifications remain immutable.

## Target

Extend the exact scalar-longitudinal NL0B memory-action reduction from the 1+1 ADM audit to a 3+1 geometry with two homogeneous transverse directions, so that the cosmological volume factor and Hubble friction are represented correctly before any screened physical-amplitude evolution is attempted.

Use the coframe

\[
\theta^0=Ndt,\qquad
\theta^1=L(dx+b\,dt),\qquad
\theta^2=Rdy,\qquad
\theta^3=Rdz,
\]

with

\[
A=\cosh r\,e_0+\sinh r\,e_1,
\qquad
s=\sinh r\,e_0+\cosh r\,e_1.
\]

For the longitudinal bath and projected scalar gradient,

\[
U_{j\mu}=q_j s_\mu,\qquad
X_\mu=X s_\mu,\qquad X=s(\phi),
\]

the frozen NL0B action must reduce node-by-node to

\[
\widehat{\mathcal L}_j
=\frac{NLR^2}{4}
\left[(Aq_j)^2-(\omega_j q_j-\sqrt{w_j}X)^2\right].
\]

No new physical coefficient or interpolation function is allowed.

## Locked validation gates

Before any physical-amplitude memory source or survival observable is computed:

- automatic/symbolic action variation and an independent centered finite-difference action variation agree for scalar, aether, bath and all metric blocks `(N,b,L,R)` with maximum relative error `<=1e-6` on deterministic nonzero periodic fields;
- the unit-aether and orthogonal-frame identities satisfy absolute error `<=1e-12`;
- the exact homogeneous FLRW null test has zero memory background action/source and zero direct linear metric stress;
- under `N=1`, `L=R=a(t)`, `b=r=0`, the bath Euler-Lagrange equation reduces exactly to

\[
\ddot q_j+3H\dot q_j+\omega_j^2q_j
=\omega_j\sqrt{w_j}\,X,
\]

with no fitted friction coefficient;
- the corresponding conformal-time form is exactly

\[
q_j''+2\mathcal H q_j'+a^2\omega_j^2q_j
=a^2\omega_j\sqrt{w_j}\,X;
\]

and with `X=(k/a)chi` this reproduces the frozen linear bath drive `a k omega_j sqrt(w_j) chi`;
- all generated source blocks are finite;
- no observational data, finite physical eta, collapse statistic or likelihood is used.

## Classification

All gates pass with no new theory freedom:

**NL1C3B_LONGITUDINAL_3PLUS1_MEMORY_BRIDGE_PASS**

A frozen action/source inconsistency is found:

**NL1C3B_LONGITUDINAL_3PLUS1_MEMORY_BRIDGE_FAIL**

The covariant action remains consistent but a required component block cannot be generated without an additional theory choice:

**NL1C3B_LONGITUDINAL_3PLUS1_MEMORY_BRIDGE_INCOMPLETE**

A PASS permits the first action-derived expanding periodic-box memory-source trajectory. It is not itself a nonlinear structure-formation or observational result.
