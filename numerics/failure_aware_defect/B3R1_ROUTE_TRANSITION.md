# B3R1 — Volterra certificate-route transition

B3R1 extends the manufactured Volterra ramp-memory benchmark across grid spacing `h` and spectral cutoff `R` using only the rigorous B3 certificate formulas.

## Route coordinate

The dimensionless stiffness-resolution coordinate is

\[
\rho=hR.
\]

For `rho<=1`, the direct-split route has no unresolved tail and therefore coincides with the conventional high-jet certificate. For `rho>1`, define

\[
\Gamma(h,R)=\frac{B_T(h,R)}{B_D(h,R)}.
\]

`Gamma<1` selects the high-jet certificate, while `Gamma>1` selects the direct-split certificate. The nontrivial transition solves `Gamma=1` above `rho=1`.

## Asymptotic law

As `h->0` with `R=rho/h`, the B3 certificates satisfy

\[
\frac{B_T}{h^2}\to\frac{\rho^6}{3780},
\]

and

\[
\frac{B_D}{h^2}\to
\frac1{3780}
+\frac{A_{\rm tail}}3(1-\rho^{-3})
+\frac{e^{-4}}2(1-\rho^{-2}).
\]

The unique nontrivial crossover is

\[
\rho_*=2.258910484064123.
\]

Therefore

\[
R_{\rm cross}(h)\sim\frac{2.258910484064123}{h}.
\]

The certificate at the transition obeys

\[
B_{\rm cross}(h)\sim0.03514813830095348\,h^2.
\]

## Finite-h confirmation target

For

`h = 0.1, 0.05, 0.02, 0.01, 0.005, 0.002, 0.001`,

the reference implementation gives approximately

- `h=0.1`: `hR_cross=2.2575333352`
- `h=0.05`: `hR_cross=2.2585644748`
- `h=0.02`: `hR_cross=2.2588550449`
- `h=0.01`: `hR_cross=2.2588966215`
- `h=0.005`: `hR_cross=2.2589070190`
- `h=0.002`: `hR_cross=2.2589099039`
- `h=0.001`: `hR_cross=2.2589101618`

The corresponding log-log fit is approximately

\[
R_{\rm cross}\approx2.25761916\,h^{-1.00009949}.
\]

## Numerical root-finding safeguard

Because the two certificate formulas coincide exactly at `rho=1`, direct subtraction immediately above the split can suffer floating-point sign noise when `h` is small. B3R1 therefore scans away from the exact equality before constructing the Brent bracket. This changes only the numerical root-finding safeguard. It does not alter either rigorous certificate or the asymptotic transition law.

## Comparison with B1 and B2

All three gravity-independent benchmarks produce

\[
R_{\rm cross}=O(h^{-1}),
\]

so `hR` is the recurring route-control coordinate. The crossover certificate amplitude is model dependent:

- B1 continuum spectral benchmark: `B_cross=O(h^2)`
- B2 generalized Maxwell initial-layer benchmark: `B_cross=O(h)`
- B3 manufactured Volterra ramp-memory benchmark: `B_cross=O(h^2)`

This supports a method-level interpretation: the route coordinate is governed by stiffness relative to grid resolution, while the certificate amplitude retains the regularity and initial-layer structure of the model.

## Claim boundary

B3R1 is a certificate-route phase diagram, not an empirical error phase diagram. Route selection uses only rigorous closed-form certificate formulas. QUADPACK actual-defect values are diagnostic and do not enter the route decision or transition constant.
