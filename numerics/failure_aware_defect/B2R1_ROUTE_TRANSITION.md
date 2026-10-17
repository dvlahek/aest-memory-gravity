# B2R1 — Maxwell certificate-route transition

B2R1 extends the generalized-Maxwell benchmark across grid spacing `h` and relaxation cutoff `R` using only the two rigorous B2 certificate formulas.

## Route coordinate

The natural dimensionless stiffness-resolution coordinate remains

\[
\rho=hR.
\]

For `rho<=1`, the direct-split route has not yet opened its unresolved tail, so it coincides exactly with the conventional high-jet certificate.

For `rho>1`, define

\[
\Gamma(h,R)=\frac{B_T(h,R)}{B_D(h,R)}.
\]

Then `Gamma<1` means the high-jet certificate is narrower, `Gamma>1` means the direct-split certificate is narrower, and the nontrivial transition solves `Gamma=1` above `rho=1`.

## Asymptotic transition

As `h->0` with `R=rho/h`, the B2 certificates satisfy

\[
\frac{B_T}{h}\to\frac{\rho^7}{4410},
\]

and

\[
\frac{B_D}{h}\to
\frac1{4410}
+\frac{A_{\rm tail}}2(1-\rho^{-2})
+e^{-4}(1-\rho^{-1}).
\]

The unique nontrivial crossover is

\[
\rho_*=2.1305793530674104.
\]

Therefore

\[
R_{\rm cross}(h)\sim\frac{2.1305793530674104}{h}.
\]

The certificate at the crossover obeys

\[
B_{\rm cross}(h)\sim
0.045190319200393\,h.
\]

This should be compared with B1, where the same route coordinate `hR` controls the transition but the crossover certificate is `O(h^2)`. The shared `R_cross proportional to h^-1` law is therefore not tied to one source construction, while the certificate amplitude scaling retains model-specific regularity information.

## Expected finite-h confirmation

For the standard sweep

`h = 0.1, 0.05, 0.02, 0.01, 0.005, 0.002, 0.001`,

the expected crossover products are approximately

- `4?` no: B2 has `h R_cross` approaching `2.1305793531`
- at `h=0.1`: `2.1295969861`
- at `h=0.05`: `2.1303325467`
- at `h=0.02`: `2.1305398093`
- at `h=0.01`: `2.1305694652`
- at `h=0.005`: `2.1305768810`
- at `h=0.002`: `2.1305789575`
- at `h=0.001`: `2.1305792540`

The corresponding log-log fit from the reference implementation is expected to be close to

\[
R_{\rm cross}\approx2.12965814\,h^{-1.00007525}.
\]

## Claim boundary

B2R1 is a certificate-route phase diagram, not an empirical error phase diagram. Route selection uses only the rigorous closed-form B2 certificate formulas. QUADPACK actual-defect values do not enter the route rule or the transition constant.
