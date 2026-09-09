# NL1C1 predata — full AeST Y-sector interpolation/operator bridge

Classification before result: **NL1C1_PREDATA_FULL_Y_OPERATOR_BRIDGE**

This preregistration is created after `NL1C0_LINEAR_STATE_HIGH_GRADIENT_REGIME` and before any full-interpolation operator result or physical-amplitude nonlinear evolution.

It is explicitly result-informed by NL1C0. Historical classifications remain immutable.

## 1. Reason for this gate

NL1C0 found that the frozen linear cosmological state in the certified late-time band has

\[
x_{\rm rms}=\sqrt{\mathcal Y}_{\rm rms}/a_0\sim10^7-10^8,
\]

so the deep-MOND `Y^(3/2)` expansion validated in NL0C/NL1A is not amplitude-consistent for the physical primordial amplitude of that state.

The next operator must therefore retain the full published transition between

\[
j(x)\equiv\frac{d\mathcal J}{d\mathcal Y}
\simeq\frac{x}{1+\beta_0}
\quad(x\ll1)
\]

and

\[
j(x)\rightarrow\frac1{\beta_0}
\quad(x\gg1).
\]

No one interpolation is selected after the NL1C0 result.

## 2. Frozen co-primary interpolation family

Use all three functions employed in the published AeST quasistatic study, with

\[
x=\sqrt{\mathcal Y}/a_0.
\]

### Simple

\[
j_{\rm S}(x)=\frac{x}{1+\beta_0+\beta_0x}.
\]

### Exponential

\[
j_{\rm E}(x)=\frac1{\beta_0}
\left[1-\exp\left(-\frac{\beta_0 x}{1+\beta_0}\right)\right].
\]

### Sharp

\[
j_{\rm H}(x)=
\frac{\beta_0x+(1+\beta_0)-|\beta_0x-(1+\beta_0)|}
{2\beta_0(1+\beta_0)}.
\]

All three are co-primary. The already frozen

\[
\beta_0\in\{1,0.5,0.1\}
\]

are also co-primary. Thus the operator audit reports all nine function/`beta0` combinations.

No combination may be promoted by outcome-dependent selection.

## 3. Integrated J(Y) is fixed, not a new function

For later action-level work, choose the unique additive normalization

\[
\mathcal J(0)=0.
\]

Since `dY=2 a0^2 x dx`,

\[
\mathcal J(x)=2a_0^2\int_0^x s j(s)\,ds.
\]

For `A=1+beta0`, this fixes

### Simple

\[
\mathcal J_{\rm S}(x)=2a_0^2\left[
\frac{x^2}{2\beta_0}-\frac{Ax}{\beta_0^2}
+\frac{A^2}{\beta_0^3}\ln\left(\frac{A+\beta_0x}{A}\right)
\right].
\]

### Exponential

With `c=beta0/A`,

\[
\mathcal J_{\rm E}(x)=\frac{2a_0^2}{\beta_0}\left[
\frac{x^2}{2}-\frac{1-(1+cx)e^{-cx}}{c^2}
\right].
\]

### Sharp

For `x_t=A/beta0`,

\[
\mathcal J_{\rm H}(x)=
\begin{cases}
\displaystyle\frac{2a_0^2x^3}{3A}, & x\le x_t,\\[1ex]
\displaystyle\frac{a_0^2x^2}{\beta_0}
-\frac{a_0^2A^2}{3\beta_0^3}, & x\ge x_t.
\end{cases}
\]

These expressions are algebraic integrals of the frozen published `j(x)` and introduce no new freedom.

## 4. Full spatial operator

The scalar Y-sector operator to validate is

\[
\mathcal O_{j,\beta}[\chi]
=\nabla\cdot\left[
 j\left(\frac{|\nabla\chi|}{a_0}\right)\nabla\chi
\right].
\]

The common covariant field-equation prefactor `2(2-K_B)` is factored out of the numerical operator audit.

Spatial derivatives are pseudospectral; the nonlinear flux is formed pointwise in real space and dealiased with the same 2/3 rule as NL1A.

## 5. Locked analytic coefficient checks

For every interpolation and every co-primary beta0:

1. `j(0)=0`.
2. `j(x)>0` for `x>0`.
3. `j(x)<=1/beta0`.
4. the deep limit satisfies
   \[
   j(x)/(x/(1+\beta_0))\to1;
   \]
5. the high-gradient limit satisfies
   \[
   \beta_0 j(x)\to1;
   \]
6. `J(0)=0` and numerical differentiation of the integrated `J(Y)` reproduces `j(x)` away from the Sharp kink.

Use fixed coefficient test points

\[
x\in\{10^{-8},10^{-6},10^{-4},10^{-2},1,10^2,10^4,10^8,10^{10}\}.
\]

Deep-limit relative error at `x=1e-8` must be `<1e-7`; high-limit relative error at `x=1e10` must be `<2e-9`.

## 6. Locked operator checks

Use the deterministic NL1A 1D and 3D seed families. Rescale the field amplitude by a deterministic factor computed **before** evaluating the operator so that the RMS gradient-regime variable is the requested control value.

### O1. Variational sign identity

For each function/beta0,

\[
\langle\chi\,\mathcal O[\chi]\rangle
=-\langle j(x)|\nabla\chi|^2\rangle.
\]

Relative error gate: `<1e-10`.

### O2. Translation invariance

Relative error gate: `<1e-10`.

### O3. Constant-field null

Maximum absolute source `<1e-12` in dimensionless audit units.

### O4. 3D axis permutation

Relative error gate: `<1e-10`.

### O5. Resolution convergence

For the deterministic 1D multimode seed at `x_rms=1`, compare low Fourier modes `m=0..32` between `N=512` and `N=1024`.

Global normalized RMS gate: `<5e-4` for all nine co-primary combinations.

### O6. Deep-MOND reduction to NL1A

At `x_rms=1e-6`, compare the full operator with

\[
\frac{1}{1+\beta_0}\nabla\cdot(|\nabla\chi|\nabla\chi)/a_0.
\]

Global normalized RMS gate: `<1e-4`.

### O7. High-gradient coefficient saturation

This is tested at the **coefficient level**, not by assuming every real-space point of a periodic field has large gradient. At `x=1e10`, every interpolation must satisfy the high-limit gate in Section 5.

## 7. Classification

All analytic and operator gates pass for all nine co-primary combinations:

**NL1C1_FULL_Y_OPERATOR_BRIDGE_PASS**

Otherwise:

**NL1C1_FULL_Y_OPERATOR_BRIDGE_FAIL**

A PASS validates the full published Y-sector interpolation operator. It does not yet establish a self-consistent physical-amplitude cosmological solution, a finite-eta nonlinear prediction, halo formation, or observational agreement.

## 8. Continuation rule

If NL1C1 passes, the next strong-path task is no longer the deep-MOND second-order source. It is to construct a self-consistent physical-amplitude AeST baseline with the full Y-sector active, then compute the eta=0 memory tangent around that baseline using the frozen NL0B memory action.

No GR/Poisson toy closure is allowed to substitute for that baseline.
