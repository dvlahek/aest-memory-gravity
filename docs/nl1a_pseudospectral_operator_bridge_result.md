# NL1A result — pseudospectral operator bridge

Final classification: **NL1A_PSEUDOSPECTRAL_OPERATOR_BRIDGE_PASS**

Predata commit: `f8eaac58e44782de0d67e6f4bbe8cbfdf323ae20`

Implementation commit: `24ed670a9445b04c4004bf2dec75f1648f047270`

Workflow commit: `cc052195ea06f7cec7a602f0ede8e93bbd4ee8bb`

GitHub Actions run: `34321913400` — technical SUCCESS.

Artifact: `results_bundle_nl1a_pseudospectral_operator_bridge`, artifact ID `10092177796`, SHA256 `ee8dfc8435038859e6b6f8c494475cc92870314ea8d1e4761c20d3ac767a4f3a`.

Scope: deterministic theory/operator implementation audit only. No observational data, no likelihood, no fit, and no physical nonlinear-growth result.

## Frozen operator

NL1A implements the exact leading weakly nonlinear Y-sector operator frozen by NL0C,

\[
\Delta\mathcal E_\phi^{(2)}
=\frac{2(2-K_B)}{(1+\beta_0)a_0}
\nabla_{\rm phys}\cdot
\left(|\nabla_{\rm phys}\chi|\nabla_{\rm phys}\chi\right).
\]

The periodic dimensionless-box audit factors out the common dimensional prefactor and evaluates

\[
\mathcal O_{\beta}[\chi]
=\frac{1}{1+\beta_0}\nabla\cdot(|\nabla\chi|\nabla\chi)
\]

with FFT derivatives, pointwise real-space products, and a 2/3 nonlinear-flux dealiasing mask.

The co-primary values remain

\[
\beta_0\in\{1,0.5,0.1\},
\qquad
K_B=0.0665,
\qquad
a_0=1.2\times10^{-10}\,{\rm m\,s^{-2}}.
\]

## Primary gates

All preregistered gates passed.

### 1D variational identity

For the deterministic multimode seed, periodic integration by parts requires

\[
\langle\chi\,\mathcal O_0[\chi]\rangle
=-\langle|\nabla\chi|^3\rangle.
\]

The relative errors were

- N=256: `0.0`;
- N=512: `1.9501e-16`;
- N=1024: `0.0`.

The preregistered limit was `1e-10`.

### Positive degree-two homogeneity

For amplitudes `0.25`, `0.5`, `2`, and `4`,

\[
\mathcal O[A\chi]=A^2\mathcal O[\chi]
\]

held to reported machine precision. Maximum relative error: `0.0`, versus gate `1e-12`.

### Translation invariance

A 37-grid-point translation produced relative error

`7.0152e-14`,

versus gate `1e-10`.

### Constant-field null

Maximum absolute source: `0.0`, versus gate `1e-12`.

### Spectral convergence

The low-mode `m=0..32` comparison gave

- N=256 vs N=1024: `2.2645e-4`;
- N=512 vs N=1024: `2.1347e-5`.

The primary N=512 vs N=1024 gate was `5e-4`.

### Single-mode harmonic structure

For `chi=cos(3x)`, forbidden low-harmonic leakage was

`7.9858e-6`,

versus gate `1e-4`.

### beta0 scaling

The measured operator-norm ratios were exactly the frozen coefficients:

- beta0=1: `0.5`;
- beta0=0.5: `2/3`;
- beta0=0.1: `10/11`.

Maximum relative scaling error: `0.0`, versus gate `1e-12`.

### 3D variational identity and axis permutation

At N=32,

- variational relative error: `1.6437e-16`;
- x/y axis-permutation relative error: `1.9156e-15`.

Both pass their `1e-10` gates.

# Classification

Every primary gate passed:

\[
\boxed{\text{NL1A\_PSEUDOSPECTRAL\_OPERATOR\_BRIDGE\_PASS}}
\]

## What this establishes

The exact NL0C leading MOND/Y-sector operator now has a controlled 1D/3D pseudospectral implementation. Its variational sign, degree-two homogeneity, beta0 dependence, translation invariance, axis symmetry, harmonic structure, and low-mode resolution behavior are numerically verified.

This closes the **operator implementation** part of NL1.

## What this does not establish

NL1A does not show that memory delays or accelerates nonlinear structure growth. It deliberately does not insert a GR/Poisson or phenomenological nonlinear gravitational closure around the AeST operator.

A physical weakly nonlinear growth calculation requires the next step, NL1B: freeze the second-order dynamical closure of the AeST+memory system, then use this already-validated pseudospectral operator inside that evolution. Historical linear PASS and FAIL classifications remain unchanged.
