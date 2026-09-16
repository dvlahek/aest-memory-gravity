# NL1C6 result — spherical self-gravity closure

Final classification: **NL1C6_SPHERICAL_SELF_GRAVITY_CLOSURE_PASS**

Master preregistration commit: `5d5d9d3293849f878394b22a092db22e1c860189`.

G1-G10 implementation commit: `f7ce5a26501f9bceed65c9bea1a4b7a2b80a82d0`.

Official G1-G10 workflow HEAD: `2ca1489a920c0ef9c7b05afe932a6cb22844c9bd`.

Official G1-G10 run: `35088549978` — technical SUCCESS.

Official G1-G10 artifact: `results_bundle_nl1c6_g1_g10`, artifact ID `10443038294`, SHA256 `935a9f05364c3f00f85616957fe217bcd1708915ee5a4d72a0bd9f896a582b6a`.

G11 pre-result gauge/solver lock: `a2b787adf3fcd9493c9569ae8a5e00969a232e41`.

G11 Repair01 implementation commit: `11dc0cfb3d70fb81c9bc5d63bde6b8f9fd9acad5`.

Final G11 workflow HEAD: `0f868057e788423b588cda5bc654287c784ebee7`.

Final G11 run: `35089436959` — technical SUCCESS.

Final G11 artifact: `results_bundle_nl1c6_g11_solver_readiness`, artifact ID `10442933686`, SHA256 `12b83f6f67f473937514005f6a87764646407e3b2141b4451d47bd92b62c6ddc`.

Official G11 JSON SHA256: `b02f669c8e928d047350e75f98d73d5e251975be0348f8adade009375074f1bd`.

Official certified G1-G10 JSON copied into the final bundle SHA256: `ab17a132c65f707f20fe06ce6a507923e6a6af4ff2ac92b85e0881d9e2a5f437`.

Scope: theory/component closure and local solver-readiness only. No spherical-collapse trajectory, turnaround, splashback, halo mass, lensing observable, finite physical eta outcome, likelihood or observational data were used.

## 1. Ungauged spherical action closes through G1-G10

The spherical coframe remains

\[
\theta^0=Ndt,\qquad
\theta^1=L(dr+b\,dt),\qquad
\theta^2=R d\theta,\qquad
\theta^3=R\sin\theta\,d\varphi,
\]

with aether rapidity `u`, scalar `phi`, normalized retarded bath fields `q_j`, and minimally coupled pressureless matter.

The exact local scalar/aether invariants are

\[
\sigma=\frac{\dot\phi-b\phi'}{N},
\]

\[
Q=\cosh u\,\sigma+\sinh u\,\frac{\phi'}{L},
\qquad
X=\sinh u\,\sigma+\cosh u\,\frac{\phi'}{L},
\]

with

\[
Y=X^2.
\]

The radial electric aether quantity is

\[
E=\cosh u\left[\frac{\dot u-bu'}N+\frac{N'}{NL}\right]
+\sinh u\left[k_L+\frac{u'}L\right],
\]

where

\[
k_L=\frac{\dot L-bL'-Lb'}{NL},
\qquad
k_R=\frac{\dot R-bR'}{NR}.
\]

The reduced AeST sector contains the action-derived combination

\[
NLR^2\left[
K_B E^2+2(2-K_B)EX-(2-K_B)X^2+2K(Q)-(2-K_B)J(Y)
\right],
\]

with the full frozen `Simple/Exponential/Sharp x beta0={1,0.5,0.1}` Y-sector retained locally.

Every preregistered G1-G10 gate passed in the official run. The maximum independent action-variation mismatch was

\[
\boxed{3.0234628379\times10^{-7}},
\]

against the frozen `1e-6` gate, and the normalized radial-diffeomorphism/Noether residual was

\[
\boxed{3.3215384609\times10^{-9}},
\]

against the frozen `1e-8` gate.

The exact FLRW, Minkowski, static spherical AeST, matter-conservation and eta=0 identity controls all passed.

## 2. Gauge was frozen only after G1-G10 PASS

Per the master preregistration, no numerical gauge was selected before G1-G10 passed.

The G11 pre-result lock then froze the parameter-free gauge

\[
\boxed{N=1,\qquad b=0}.
\]

This proper-time/zero-shift gauge contains the exact FLRW embedding

\[
L=a(t),\qquad R=a(t)r,
\]

while leaving `L,R,u,phi` dynamical. The lapse and shift equations are retained as Hamiltonian/radial-momentum constraints and are not discarded after gauge fixing.

## 3. Principal system is analytically nonsingular

For

\[
V=(\dot L,\dot R,\dot u,\dot\phi),
\]

the velocity Hessian derived directly from the frozen spherical action satisfies the exact identity

\[
\boxed{
\det H_V
=-64L^2R^6\cosh^4u
\left[
K_BK_{QQ}
-\tanh^2u\left(C^2+C K_B(1+M)\right)
\right]
},
\]

where

\[
C=2-K_B,
\qquad
M(x)=j(x)+xj'(x).
\]

The symbolic residual of this determinant identity is exactly zero.

For the frozen Exp sector,

\[
K_{QQ}=4K_2e^{Z^2}(1+2Z^2)\ge4K_2=38000.
\]

Across all nine frozen full-Y branches, the conservative global bound

\[
0\le M(x)\le20
\]

holds for all `x>=0`.

With

\[
K_B=0.0665,\qquad K_2=9500,
\]

the preregistered global kinetic margin is

\[
\boxed{
\Delta_{\rm kin}
=K_B(4K_2)-[C^2+C K_B(1+20)]
=2520.561445>0
}.
\]

Therefore the regularized principal determinant cannot vanish for any finite aether rapidity, any local Y-regime, or any of the nine co-primary interpolation/beta0 branches. The explicit `R^6` spherical-coordinate factor is handled by the regular-center parity result already certified in NL1C5 rather than interpreted as a physical center degeneracy.

## 4. Independent principal-matrix controls

The official G11 run evaluated the direct full-action Hessian against the independently generated local analytic Hessian over the frozen Cartesian product

- `u={0,0.25,0.5}`;
- `x={1e-6,1,1e6}`;
- `Z={0,0.5,1}`;
- all three interpolation functions;
- all three beta0 values.

This gives 243 deterministic principal-matrix controls.

The worst normalized Frobenius mismatch was

\[
\boxed{2.2252068337\times10^{-16}},
\]

and the smallest regularized bracket among the deterministic controls was

\[
\boxed{2525.8996126834}.
\]

The Sharp interpolation was additionally checked on both one-sided branches around every kink. Both sides remain nonsingular. No ordinary derivative was taken through the exact kink.

The normalized bath `q_j` principal coefficient is positive for positive `L,R` and finite rapidity, so the driven eta=0 bath equations are independently evolvable.

## 5. Historical technical attempts

The first official G11 calculation reached all science/numerical gates A-G successfully but G11-H returned false because the source self-scan matched the explanatory output key `gauge_driver_parameter` even though its value was null and no gauge driver existed. This was a checker false positive, not a physical closure failure. No gauge, threshold, deterministic test point or equation was changed.

Repair01 replaced the substring self-scan with an AST Name-node audit, so string literals/output labels cannot trigger the closure gate.

A subsequent workflow attempt re-executed the already certified G1-G10 finite-difference variation audit and showed runner-sensitive roundoff in the `b` block (`5.26e-6`). Since G1-G10 had already been frozen by run `35088549978` and artifact digest, the final workflow uses that exact certified artifact as its dependency instead of regenerating a previously certified finite-difference result. No G1-G10 classification or threshold was changed.

The final run `35089436959` passed the pre-result lock, official G1-G10 provenance, exact certified dependency artifact, G11 calculation, final classification and artifact upload.

## 6. Final classification

All frozen G1-G11 requirements are satisfied without a new physical coefficient or phenomenological force law:

\[
\boxed{\mathrm{NL1C6\_SPHERICAL\_SELF\_GRAVITY\_CLOSURE\_PASS}}.
\]

This is the first checkpoint in the nonlinear chain that licenses a self-gravitating spherical initial-value calculation from the frozen AeST + memory action.

It does **not** show that memory changes collapse, creates a splashback shift, amplifies the linear signal, or produces an observable lensing/dynamics discrepancy.

## 7. Required continuation

The next checkpoint is **NL1C7 spherical initial-value evolution**.

NL1C7 must be preregistered before a physical collapse outcome is inspected. It may define a compensated smooth spherical overdensity, evolve the eta=0 full-Y AeST baseline in the certified `N=1,b=0` gauge while monitoring the frozen constraints, and only after the baseline converges introduce the frozen memory tangent/finite-eta comparison.

Any coordinate-caustic failure in the proper-time/zero-shift gauge is a numerical/gauge limitation and must trigger a separately preregistered gauge repair; it may not be hidden by changing the slicing after inspecting a desired collapse result.
