# AeST UV continuum-envelope decision path

This note isolates the continuum issue left open by the finite B2C2A regularized-UV diagnostic. It does not modify the frozen gravity science branch or any science threshold.

## 1. Continuum measure behind the frozen quadrature

The positive Drude continuum uses

\[
r=\tan\theta,\qquad \theta\in(0,\pi/2),
\]

with normalized measure

\[
d\mu(r)=\frac{2}{\pi}\frac{dr}{1+r^2}.
\]

The Gauss-Legendre implementation maps `z in [-1,1]` to
`theta=pi(z+1)/4` and therefore uses weights `w_GL/2`.

## 2. Regularized first-order bath variables

For the first-order bath mode write

\[
u=z-X,
\qquad
u_s=v-X_s,
\qquad
q=\frac{u_s}{r^2}.
\]

The frozen interval dynamics corresponds to

\[
u_{ss}+3h\,u_s+r^2u=-F,
\qquad
F=X_{ss}+3hX_s,
\]

or

\[
u_s=r^2q,
\qquad
q_s=-3hq-u-\frac{F}{r^2}.
\]

With

\[
E=r^2|u|^2+r^4|q|^2
  =r^2|u|^2+|u_s|^2,
\]

one obtains, for expanding backgrounds with `h>=0`,

\[
\frac{d}{ds}\sqrt{E}\le |F|.
\]

This estimate is useful only if the initial `E` is uniformly bounded in `r`.

## 3. Earliest-boundary obstruction

The frozen full-history bath integration starts from

\[
z(s_0,r)=0,
\qquad
v(s_0,r)=0.
\]

Therefore

\[
u(s_0,r)=-X(s_0),
\qquad
u_s(s_0,r)=-X_s(s_0).
\]

If `X(s0) != 0`, then

\[
E(s_0,r)=r^2|X(s_0)|^2+|X_s(s_0)|^2
\]

is not uniform in `r`. More importantly, the large-`r` homogeneous solution has the generic leading form

\[
u_s^{\rm hom}(s,r)
 = r A(s)\sin(r\Phi(s)+\varphi)+O(1),
\]

with a nonzero amplitude proportional to the initial displacement mismatch unless that mismatch vanishes exactly.

Against the Drude measure,

\[
|u_s^{\rm hom}|\,d\mu
\sim \frac{|\sin(r\Phi+\varphi)|}{r}\,dr,
\]

so a naive absolute `L1` tail bound diverges logarithmically. A small finite-quadrature proxy cannot remove this continuum obstruction.

If `X(s0)=0`, the `O(r)` displacement-mismatch term is absent. A nonzero velocity mismatch `X_s(s0)` contributes only `O(1)` to `u_s`, which is absolutely integrable under `dmu`.

## 4. Two mathematically valid continuation branches

### Branch A: no position mismatch

If the frozen trace gives `X(s0)=0` exactly for the target mode, use the energy inequality. Piecewise-linear changes in `X_s` across frozen history intervals contribute known finite jumps to `u_s`; they do not increase the derivative order. The target is then a uniform bound

\[
|u_s(s,r)|\le C(s)
\]

for all sufficiently large `r`, which implies

\[
\int_{R_0}^{\infty}|u_s|\,d\mu
\le
\frac{2C(s)}{\pi}
\left(\frac{\pi}{2}-\arctan R_0\right).
\]

This is an absolute continuum certificate.

### Branch B: nonzero position mismatch

If `X(s0) != 0`, do not attempt to certify the complete tail by an absolute envelope. Instead split

\[
u=u^{\rm bdry}+u^{\rm forced},
\]

where `u_bdry` is the exactly known homogeneous response to the earliest boundary mismatch and `u_forced` has zero initial data.

Then:

1. certify `u_forced` by the absolute energy estimate;
2. certify the signed Drude integral of `u_bdry` using its oscillatory structure, integration by parts / Dirichlet-type bounds, or an exact interval transfer representation;
3. combine the signed boundary-transient enclosure with the absolute forced-remainder enclosure.

This preserves the frozen science initial condition. Replacing the initial bath state by an adiabatic state would change the scientific model and is not allowed in this methods case study.

## 5. Claim boundary

Until one of the two branches is completed, the existing B2C2A result remains a finite-quadrature diagnostic only. It does not establish an absolute continuum `B10_x` bound.
