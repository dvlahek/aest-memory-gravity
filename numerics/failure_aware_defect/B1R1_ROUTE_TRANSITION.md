# B1R1 — certificate-route transition law

This note extends the gravity-independent B1 continuum benchmark. It derives a route-transition law using only the two rigorous B1 certificate formulas. No actual-error reference enters the decision.

## 1. Route metric

Let

\[
\Gamma(R,h)=\frac{B_T(R,h)}{B_D(R,h)},
\]

where `B_T` is the conventional FD8 ninth-derivative certificate and `B_D` is the direct continuum-defect certificate from B1.

The route rule is parameter free:

- `Gamma < 1`: the high-jet certificate is narrower
- `Gamma > 1`: the direct certificate is narrower
- `Gamma = 1`: route-transition boundary

This is not a fitted accuracy threshold. Both quantities are rigorous upper bounds for the same stencil defect.

## 2. Small-h transition scaling

Introduce the dimensionless spectral-resolution variable

\[
\rho=hR.
\]

For fixed \(\rho>1\), set \(R=\rho/h\) and let \(h\to0\). The Taylor certificate satisfies

\[
\frac{B_T(\rho/h,h)}{h^2}
\longrightarrow
\frac{\rho^6}{3780}.
\]

For the direct certificate, the low-frequency part contributes

\[
\frac{C_9}{6},
\]

while the two unresolved-spectrum tail terms give

\[
\frac12(1-\rho^{-2})
\]

and

\[
\frac{A}{3}(1-\rho^{-3}),
\]

respectively. Hence

\[
\frac{B_D(\rho/h,h)}{h^2}
\longrightarrow
D(\rho)
=
\frac{C_9}{6}
+\frac12(1-\rho^{-2})
+\frac{A}{3}(1-\rho^{-3}),
\]

with

\[
C_9=\frac{1957}{198450},
\qquad
A=\frac{25}{12}.
\]

The asymptotic crossover is therefore the nontrivial root \(\rho_*>1\) of

\[
\frac{\rho_*^6}{3780}=D(\rho_*).
\]

Numerically,

\[
\boxed{\rho_*\approx4.042760931785968}.
\]

Thus

\[
\boxed{R_{\mathrm{cross}}(h)\sim\frac{4.042760931785968}{h}}.
\]

The certificate magnitude at the crossover has the asymptotic form

\[
B_T\sim B_D\sim1.15498557706\,h^2.
\]

## 3. Uniqueness of the nontrivial asymptotic crossing

Define

\[
F(\rho)=\frac{\rho^6}{3780}-D(\rho).
\]

For \(\rho>1\),

\[
F'(\rho)=\frac{\rho^5}{630}-\rho^{-3}-A\rho^{-4}.
\]

Multiplication by \(\rho^4\) shows that the sign of \(F'\) is the sign of

\[
G(\rho)=\frac{\rho^9}{630}-\rho-A.
\]

Moreover,

\[
G'(\rho)=\frac{\rho^8}{70}-1,
\]

so `G` decreases once and then increases monotonically to infinity. Therefore `F` has a single minimum for \(\rho>1\). Since \(F(1)<0\) and \(F(\rho)\to\infty\), there is exactly one nontrivial crossover root.

## 4. Finite-h confirmation

`b1r1_phase_diagram.py` solves the exact finite-h equation

\[
B_T(R,h)=B_D(R,h)
\]

and compares \(hR_{\mathrm{cross}}\) with \(\rho_*\).

For the default sweep:

| h | R_cross | h R_cross |
|---:|---:|---:|
| 1e-1 | 40.3945686 | 4.03945686 |
| 5e-2 | 80.8386315 | 4.04193157 |
| 2e-2 | 202.131404 | 4.04262808 |
| 1e-2 | 404.272771 | 4.04272771 |
| 5e-3 | 808.550525 | 4.04275263 |
| 2e-3 | 2021.37979 | 4.04275958 |
| 1e-3 | 4042.76055 | 4.04276055 |

A log-log fit gives approximately

\[
R_{\mathrm{cross}}\approx4.03966\,h^{-1.00013},
\]

consistent with the analytical law.

## 5. Interpretation

The transition is governed by the dimensionless quantity \(hR\), not by an arbitrary numerical threshold. For this benchmark, the conventional high-jet certificate is preferred while the spectral range is sufficiently resolved. Once the stiffness/cutoff exceeds the resolution scale, the direct certificate becomes narrower and remains cutoff robust.

This result strengthens the failure-aware interpretation: route selection can be based entirely on independently valid certificate widths. It does not require the unknown true defect and does not infer solver or model failure from a wide high-jet bound.
