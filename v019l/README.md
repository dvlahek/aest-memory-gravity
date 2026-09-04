# v0.19l — passive complex-domain rational memory design

v0.19k showed that the existing N=16/N=20 conservative oscillator bath is correct but underresolved for oscillatory CMB frequencies. This campaign therefore replaces the real-axis optimized oscillator discretization by a **positive first-order rational approximation** designed directly on the retarded complex-frequency domain.

For locally constant

\[
h=H\tau,\qquad z=s\tau,
\]

the exact Hubble-dressed memory kernel is

\[
K_h(z)=\frac{\sqrt{z(z+3h)}}{1+\sqrt{z(z+3h)}}.
\]

The retarded branch is chosen by continuity from Re(z)>0.

## Exact passive diffusive representation

For fixed h, define

\[
a=3h,\qquad r_*=\frac{a+\sqrt{a^2+4}}{2},\qquad
c_*=\frac{2}{r_*\sqrt{a^2+4}}.
\]

Then

\[
K_h(z)=c_*\frac{z}{z+r_*}
+\int_0^a \mu_h(r)\frac{z}{z+r}\,dr,
\]

with

\[
\mu_h(r)=\frac{\sqrt{r(a-r)}}{\pi r\,[1+r(a-r)]}>0.
\]

Thus the fixed-H retarded kernel is a positive Debye/Stieltjes superposition. Every finite approximation with positive weights and positive rates is passive and has poles only on the negative real axis.

## Practical table design

For a CLASS-oriented local approximation we use a fixed normalized rate grid

\[
q_j\in[10^{-6},4],\qquad r_j(h)=h q_j,
\]

and fit non-negative weights at 97 logarithmic Hubble anchors

\[
1\le H\tau\le 10^3.
\]

The fit minimizes the complex **relative** residual on

\[
10^{-3}\le \omega/H\le10^3,
\qquad
\epsilon/H\in\{10^{-8},10^{-6},10^{-4},10^{-2},10^{-1}\}.
\]

Between Hubble anchors, the non-negative weights are linearly interpolated in log(H tau), preserving passivity.

The target gate for N=24 is

\[
p_{99}<10^{-3},\qquad \epsilon_{\max}<10^{-3}
\]

on both anchor and midpoint test grids.

## Important limitation

This v0.19l fit is an accurate **local constant-H retarded representation**. Because the fitted rates and weights vary with H(t), simply inserting them as time-dependent first-order auxiliaries is not yet proven equivalent to the original conservative continuum bath on a rapidly varying FLRW background.

Therefore v0.19l does not yet replace the CLASS bath. If the local rational fit passes, the next gate is a non-autonomous/time-varying-H audit against the high-order conservative bath before any finite-eta CMB interpretation.
