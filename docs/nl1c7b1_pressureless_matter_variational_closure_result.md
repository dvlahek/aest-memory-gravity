# NL1C7B1 result — pressureless-matter variational backreaction closure

Status: **RESULT / FROZEN**

Final classification:

`NL1C7B1_PRESSURELESS_MATTER_VARIATIONAL_CLOSURE_PASS`

## Provenance

- parent matter-backreaction audit result commit: `6d663c661159744c44acfc919ea9d604fa6f7651`
- B1 preregistration commit: `3d41ff9b91921c8a35d8ad67048a7abd5e0384f1`
- implementation commit: `4c9ef42641b7de19e09f42d185cdfb8d305d7109`
- implementation blob: `485ed20a642ffe868b01c30196154b4834e18e10`
- implementation-lock commit: `9a367bc559b6acb5b3b1f9c9581d0e397e7af046`
- official run: `35185338047`
- workflow head: `6b555bc2ee3cba7c9e97706eb1a0949416e9932f`
- workflow conclusion: `success`
- artifact: `10481781728`
- artifact SHA256: `645d29e4e8ac7cfa4fff9833a4ef500d34fc667373bfac3073883155fac519a7`

## Certified dust action

The minimally coupled pressureless radial matter sector is represented by

\[
S_d=-\frac12\int d^4x\sqrt{-g}\,\rho_{\rm phys}
\left(g^{\mu\nu}\partial_\mu T\partial_\nu T+1\right),
\]

with the fixed gravitational normalization

\[
\varrho=8\pi G\rho_{\rm phys}.
\]

In the C6 spherical variables the reduced contribution is

\[
L_d=NLR^2\varrho\left[
\left(\frac{T_t-bT_r}{N}\right)^2-
\left(\frac{T_r}{L}\right)^2-1
\right].
\]

There is no free multiplicative matter-coupling coefficient.

## Exact certified identities

The density-multiplier equation gives the unit-timelike normalization exactly. On the future-directed branch

\[
W=\cosh v,\qquad V=-\sinh v,
\]

so

\[
T_r=-L\sinh v,\qquad T_t=N\cosh v-bL\sinh v.
\]

Variation with respect to `T` reproduces the already frozen C6 pressureless continuity equation exactly. Integrability of `T_t,T_r` reproduces the already frozen C6 radial geodesic equation exactly; the symbolic residual is `0`.

Metric/lapse/shift source identities all pass. On the dust shell:

- `dL_d/dN = -2 L R^2 varrho cosh(v)^2`;
- `dL_d/db = L^2 R^2 varrho sinh(2v)`;
- `dL_d/dL = 2 N R^2 varrho sinh(v)^2`;
- `dL_d/dR = 0`.

The pure-GR FLRW lapse control reduces exactly to

`3*H**2 - rho8 = 0`,

i.e. `3 H^2 = 8 pi G rho_phys`.

The dust contribution to the C6 `(Lt,Rt,ut,pt)` principal Hessian is the exact zero matrix, so the already certified C6 field-sector principal determinant is unchanged.

The dust transport speed is exactly

\[
\frac{dr}{dt}=-b+\frac{N}{L}\tanh v.
\]

The action contains no direct `u`, `phi`, `q`, `eta`, `Y`, or `Q` coupling.

## Independent variation audit

Frozen tolerance: `1e-6`.

Maximum finite-difference/component relative error:

`4.023122185815232e-08`.

All tested blocks `N,L,R,b,varrho,T` pass.

## Claim boundary

This PASS closes the pressureless-matter variational backreaction gap found by NL1C7B. No nonlinear trajectory, turnaround, collapse, shell crossing, finite eta, or observable was evaluated.

The full frozen CLASS/AeST homogeneous background constraint at `a_i=0.02` has not yet been certified. It is the next explicit checkpoint; no silent radiation/neutrino/background source is added here.
