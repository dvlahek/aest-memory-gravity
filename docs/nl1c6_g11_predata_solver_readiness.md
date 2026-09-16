# NL1C6 G11 predata — proper-time zero-shift solver-readiness

Classification before G11 result: **NL1C6_G11_PREDATA_SOLVER_READINESS**

This lock is created only after the official G1-G10 checkpoint passed. No G11 numerical outcome, spherical-collapse trajectory, turnaround, splashback statistic or finite physical eta result is used to choose the gauge or gates below.

## Frozen provenance

- NL1C6 master preregistration: `5d5d9d3293849f878394b22a092db22e1c860189`;
- G1-G10 implementation: `f7ce5a26501f9bceed65c9bea1a4b7a2b80a82d0`;
- G1-G10 workflow HEAD: `2ca1489a920c0ef9c7b05afe932a6cb22844c9bd`;
- official G1-G10 run: `35088549978`, technical SUCCESS;
- official G1-G10 artifact: `10443038294`;
- artifact digest: `sha256:935a9f05364c3f00f85616957fe217bcd1708915ee5a4d72a0bd9f896a582b6a`;
- official classification: `NL1C6_G1_G10_PASS_PENDING_G11`;
- official maximum action-variation mismatch: `3.0234628378725663e-07`;
- official radial-diffeomorphism Noether residual: `3.321538460904162e-09`.

Historical classifications and G1-G10 are immutable.

## Gauge frozen before the G11 result

Use the parameter-free proper-time / zero-shift gauge

\[
N=1,\qquad b=0.
\]

Reasons fixed before the G11 outcome:

1. it introduces no gauge-driver coefficient that could be tuned;
2. it contains the exact homogeneous FLRW embedding `L=a(t), R=a(t) r`;
3. it leaves `L(t,r), R(t,r), u(t,r), phi(t,r)` dynamical;
4. it does not impose areal gauge `R=r`, aether-comoving gauge or matter-comoving gauge;
5. the already derived lapse and shift equations remain Hamiltonian/radial-momentum constraints and are monitored after gauge fixing rather than discarded.

A G11 PASS certifies local solver-readiness in this gauge. It does not certify freedom from late-time synchronous-coordinate caustics during a later collapse run. Any later gauge repair would require a separate pre-result lock.

## Principal variables

For the eta=0 self-gravitating baseline, test the second-time-derivative block for

\[
V=(\dot L,\dot R,\dot u,\dot\phi).
\]

The normalized retarded bath variables `q_j` are driven auxiliary fields at eta=0. Their equations are tested separately. They must have a strictly positive coefficient multiplying `ddot q_j` for every node. They do not alter the eta=0 physical-field Hessian because backreaction is disabled at this stage.

Pressureless matter remains a first-order conservation/geodesic subsystem and is not part of this second-order Hessian.

## Frozen analytic principal test

Write

\[
C=2-K_B,\qquad c=\cosh u,\qquad s=\sinh u,
\]

and

\[
M(x)=j(x)+x\,\frac{dj}{dx},\qquad x=\sqrt{Y}/a_0.
\]

For the frozen Exp Q-sector,

\[
K_{QQ}=4K_2 e^{Z^2}(1+2Z^2)\ge 4K_2.
\]

The implementation must derive the gauge-fixed physical-field velocity Hessian directly from the already frozen spherical action and verify the exact determinant identity

\[
\det H_V
=-64 L^2R^6\cosh^4u\,
\left[
K_BK_{QQ}-\tanh^2u\left(C^2+C K_B(1+M)\right)
\right].
\]

No determinant formula may be inserted without an independent symbolic Hessian calculation from the action.

The spherical-coordinate factor `R^6` is not used as a center invertibility test. The regularized determinant is obtained by dividing by `L^2 R^6 cosh^4 u`; the center itself is handled by the regular parity/center result already certified in NL1C5.

## Full-Y bound locked before evaluation

All nine co-primary `Simple/Exponential/Sharp x beta0={1,0.5,0.1}` cases remain active.

For the frozen functions, use the analytic global bounds

- `j(x) <= 1/beta0`;
- Simple: `x j'(x) <= 1/(4 beta0)`;
- Exponential: `x j'(x) <= 1/(e beta0)`;
- Sharp: `M(x) <= 2/beta0` on both one-sided branches, with the exact kink treated as a piecewise/semismooth point rather than differentiated through.

Therefore a common conservative bound is

\[
0\le M(x)\le 20
\]

for every `x>=0` and all nine co-primary cases.

With the frozen physical values

\[
K_B=0.0665,\quad K_2=9500,
\]

the G11 analytic margin is defined before evaluation as

\[
\Delta_{\rm kin}
=K_B(4K_2)-\left[C^2+C K_B(1+20)\right].
\]

**Gate G11-A:** `Delta_kin > 0`. This proves the regularized physical-field principal determinant cannot vanish for any finite rapidity `u`, any local `x>=0`, and any of the nine full-Y branches.

## Independent symbolic/numerical controls

The official implementation must also pass all of the following without changing the gauge or bounds:

1. **G11-B — symbolic identity:** Hessian determinant derived by SymPy from the frozen reduced action minus the formula above simplifies exactly to zero after replacing local second derivatives by `K_QQ` and `M`.
2. **G11-C — bath principal coefficient:** for every normalized bath node, the coefficient of `ddot q_j` in `N=1,b=0` is positive for `L>0`, `R>0` and finite `u`.
3. **G11-D — FLRW gauge compatibility:** `N=1,b=0,L=a,R=ar,u=0` is admitted without imposing an extra physical equation.
4. **G11-E — constraints retained:** the lapse and shift Euler-Lagrange equations from G1-G10 remain explicitly identified as monitorable constraints after gauge fixing.
5. **G11-F — deterministic principal solve:** on a fixed smooth test family spanning `u={0,0.25,0.5}`, local regime controls `x={1e-6,1,1e6}`, all three interpolation functions and all three beta0 values, the direct numerical Hessian and analytic Hessian must agree to normalized Frobenius error `<=1e-10`. The regularized determinant must have the sign predicted by G11-A at every point.
6. **G11-G — Sharp kink policy:** no ordinary derivative is evaluated exactly at `x=(1+beta0)/beta0`; the two one-sided principal matrices must both be nonsingular. This is a numerical nonsmooth-interface rule, not an interpolation selection.
7. **G11-H — no physical closure added:** implementation contains no Poisson/GR substitute, memory drag, shell force, finite eta, artificial pressure, viscosity or gauge-driver parameter.

## Classification

All G11-A through G11-H pass:

**NL1C6_G11_SOLVER_READINESS_PASS**

Combined with the frozen official G1-G10 PASS, this yields

**NL1C6_SPHERICAL_SELF_GRAVITY_CLOSURE_PASS**.

Any contradiction of a frozen action identity gives

**NL1C6_SPHERICAL_SELF_GRAVITY_CLOSURE_FAIL**.

If the principal system cannot be closed in the frozen gauge without an additional physical closure, the classification is

**NL1C6_SPHERICAL_SELF_GRAVITY_CLOSURE_INCOMPLETE**.

## Claim boundary

A PASS licenses a separate NL1C7 preregistration of a spherical initial-value/evolution problem. It does not itself establish collapse, turnaround, splashback, a nonlinear memory amplification, an observational signal or a finite-eta bound.
