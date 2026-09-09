# NL1C3A result — finite-reference component variational generator

Final classification: **NL1C3A_COMPONENT_VARIATIONAL_GENERATOR_PASS**

Predata: `docs/nl1c3a_predata_component_variational_generator.md`.

Implementation commit: `2fe68dabf41a626f0cee94c04d389c3dc0d46cf5`.

Workflow commit: `25f527bd3619c342d5ca29cb8757f746a238c2fd`.

GitHub Actions run: `34337101448` — technical SUCCESS.

Artifact: `results_bundle_nl1c3a_component_variational_generator`, artifact ID `10098156154`, SHA256 `9c5197b562d60602d12c04a74a5e10dd100488e961f01f2ed21c16c61d8a11f9`.

Scope: exact scalar-longitudinal 1+1 ADM reduction of the already frozen NL0B memory action, together with screened/static AeST controls. No screened memory-survival observable, finite physical eta, halo calculation, likelihood, observational data, or full 3D cosmological prediction was produced.

## 1. Component reduction

Use the 1+1 ADM coframe

\[
\theta^0=N\,dt,\qquad \theta^1=L(dx+b\,dt),
\]

with orthonormal frame

\[
e_0=N^{-1}(\partial_t-b\partial_x),\qquad e_1=L^{-1}\partial_x.
\]

The unit aether is parameterized exactly by a rapidity field

\[
A=\cosh r\,e_0+\sinh r\,e_1,
\]

and the orthogonal unit spatial direction is

\[
s=\sinh r\,e_0+\cosh r\,e_1.
\]

Thus the unit-aether constraint is parameterized rather than discarded:

\[
A^2=-1,\qquad s^2=1,\qquad A\cdot s=0.
\]

For one normalized NL0B bath node, write `q_mu=q s_mu`. Then

\[
X=s(\phi),\qquad \mathscr D_A q=A(q),
\]

and the normalized memory Lagrangian is exactly

\[
\widehat{\mathcal L}_{\rm mem}
=\frac{NL}{4}
\left[
(Aq)^2-
\left(\omega q-\sqrt w\,X\right)^2
\right].
\]

The full bath is the frozen positive sum over nodes. No new physical coefficient was introduced.

## 2. Generated source blocks

Automatic Euler-Lagrange variation generates all source blocks required by the preregistration within this scalar-longitudinal sector:

- scalar source from variation of `phi`;
- spatial-aether source from variation of rapidity `r`;
- normalized retarded bath equation from variation of `q`;
- direct metric sources from independent lapse, shift and spatial-scale variations `N,b,L`;
- unit-aether/projector effects through the exact rapidity/frame parameterization.

The finite-reference metric source is explicitly nonzero. Its deterministic test-field L2 norms were

\[
\|S_N\|_2=0.4605863,\qquad
\|S_b\|_2=0.1226880,\qquad
\|S_L\|_2=0.2487100.
\]

Therefore NL1C3's conclusion is confirmed constructively: the direct eta-linear metric memory source that vanishes in the FLRW linear audit must be retained on a nonzero finite reference.

## 3. Independent action-variation check

The automatic/symbolic Euler-Lagrange sources were compared against independent central finite differences of the total periodic discrete action at three nonzero deterministic sites for every generated source block.

The worst relative mismatch was

\[
\boxed{1.0786\times10^{-7}},
\]

below the preregistered

\[
10^{-6}
\]

gate.

## 4. FLRW null and linear-stress recovery

On homogeneous FLRW, with a homogeneous scalar velocity allowed,

\[
r=0,\qquad X=0,\qquad q=0,
\]

the normalized memory Lagrangian and every direct source block vanish exactly in the symbolic audit.

The coefficient linear in perturbation amplitude of each direct metric source also vanishes exactly. Hence the preserved NL0B statements are recovered:

\[
\text{memory background correction}=0,
\]

\[
\text{direct linear memory Einstein stress}=0.
\]

The finite-reference direct metric source is therefore not a contradiction of v0.77. It starts beyond that FLRW first-order expansion.

## 5. Unit-aether/frame control

The deterministic nonzero frame test gives

\[
\max|A^2+1|=4.44\times10^{-16},
\]

\[
\max|A\cdot s|=1.11\times10^{-16},
\]

\[
\max|s^2-1|=5.55\times10^{-16}.
\]

## 6. Screened AeST controls

The already frozen high-gradient/static AeST equations were solved independently for all

\[
\beta_0\in\{1,0.5,0.1\}
\]

on periodic boxes whose integer Fourier modes reproduce the frozen physical k-grid.

The maximum normalized static/constraint residual was

\[
2.36\times10^{-13},
\]

well below both the `1e-8` static and `1e-6` scalar-constraint gates.

The eta=0 memory-off state identity was exactly zero to stored precision, and the two finest low-mode solutions differed by at most

\[
3.16\times10^{-15}
\]

against the `5e-3` resolution gate.

The full Simple/Exponential/Sharp saturation control also remains within the frozen `2e-6` bound, with maximum deviation

\[
1.0082\times10^{-6}.
\]

## Classification

Every preregistered NL1C3A source/variation/null/static/constraint/resolution gate passes:

\[
\boxed{\mathrm{NL1C3A\_COMPONENT\_VARIATIONAL\_GENERATOR\_PASS}}.
\]

## What this permits

The previous NL1C3 `INCOMPLETE` result identified the missing explicit finite-reference source system. NL1C3A now supplies and validates such a system in the controlled scalar-longitudinal periodic-box reduction directly from the frozen NL0B action.

This permits the next step: a first self-consistent screened scalar periodic-box baseline followed by its eta=0 memory tangent, with the scalar, aether and direct metric memory source blocks all retained.

It does **not** yet establish that the original v0.77 memory signal survives screening, nor does it constitute a full 3D cosmological/N-body result.

Historical v0.77/v0.78 PASS results, NL1C0-NL1C2, NL1C3 INCOMPLETE, and every earlier FAIL/INCOMPLETE classification remain unchanged.
