# AeST + memory v0.18
## CLASS source integration and zero-regression gate

The patch is pinned to official CLASS `v3.3.4` at commit
`e85808324f51fc694d12e3ed7439552a3c3f9540`.

A new translation unit

```text
source/aest_memory.c
include/aest_memory.h
```

is inserted into the CLASS `SOURCE` object list. It contains only metadata,
the positive 20-node finite-bath representation selected in v0.17, a dimensionless
kernel evaluator,

\[
R_N(A)=\sum_j w_j \frac{A^2}{r_j^2+A^2},
\]

and a standalone self-test.

It does not alter `background.c`, `input.c`, or `perturbations.c` in v0.18.

The central software gate is

\[
C_\ell^{\rm patched,off}=C_\ell^{\rm pristine}
\]

up to bit-level or machine-level numerical identity.

If this fails, v0.19 is blocked.

Only after this gate passes will v0.19 add the AeST parameters

\[
K_B,Q_0,{\cal K}_2,Z_0
\]

and scalar states

\[
\delta_A,\theta_A,\alpha_A,E_A
\]

with memory still fixed to \(\eta=0\).
