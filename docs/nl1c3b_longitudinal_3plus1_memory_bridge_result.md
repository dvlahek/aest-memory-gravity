# NL1C3B result — longitudinal 3+1 memory bridge

Final classification: **NL1C3B_LONGITUDINAL_3PLUS1_MEMORY_BRIDGE_PASS**

Predata commit: `74a23b29bce241c6ea0d875dd119eec0bf15a2cf`.

Implementation commit: `3a81de3727cf547d5815ed140ef3df6d49237110`.

Workflow commit: `0605c4fbaad1f1aafa0c3a702a86b52b71c711b8`.

GitHub Actions run: `34341591423` — technical SUCCESS.

Artifact: `results_bundle_nl1c3b_longitudinal_3plus1_memory_bridge`, ID `10099953397`, SHA256 `6d707a2bffb1d5b5a4e507d62eb623711cca4e2ebfc323e5fe5499926e4a9169`.

Scope: exact longitudinal 3+1 component reduction of the already frozen NL0B memory action. No finite physical eta, collapse statistic, observational data or likelihood was used.

## Component reduction

The coframe is

\[
\theta^0=Ndt,\qquad
\theta^1=L(dx+b\,dt),\qquad
\theta^2=Rdy,\qquad
\theta^3=Rdz,
\]

with

\[
A=\cosh r\,e_0+\sinh r\,e_1,
\qquad
s=\sinh r\,e_0+\cosh r\,e_1.
\]

For the longitudinal normalized bath field `q_j` and projected scalar gradient `X=s(phi)`, the frozen NL0B action reduces node-by-node to

\[
\widehat{\mathcal L}_j
=\frac{NLR^2}{4}
\left[(Aq_j)^2-(\omega_jq_j-\sqrt{w_j}X)^2\right].
\]

No new physical coefficient or interpolation function was introduced.

## Validation

Automatic/symbolic action variation agrees with an independent finite-difference action variation for scalar, aether, bath and all metric blocks. The maximum relative error is

\[
4.5884648604\times10^{-8},
\]

well below the preregistered `1e-6` gate.

The unit-frame identities are satisfied at approximately machine precision. The largest reported frame error is `5.55e-16`.

The FLRW null is exact: the homogeneous memory action/source is zero, and the direct metric memory source has no term linear in perturbations around FLRW.

## Expanding-volume bath identity

For

\[
N=1,\qquad L=R=a(t),\qquad b=r=0,
\]

the Euler-Lagrange equation reduces exactly to

\[
\ddot q_j+3H\dot q_j+\omega_j^2q_j
=\omega_j\sqrt{w_j}X.
\]

In conformal time this becomes

\[
q_j''+2\mathcal Hq_j'+a^2\omega_j^2q_j
=a^2\omega_j\sqrt{w_j}X.
\]

With

\[
X=(k/a)\chi,
\]

the drive is exactly

\[
ak\omega_j\sqrt{w_j}\chi,
\]

which is the frozen linear bath equation used in the certified chain.

## Consequence

NL1C3B closes the expanding-volume component bridge that was not represented by the earlier 1+1 audit. The full longitudinal memory source, including finite-reference direct metric terms, can now be evaluated on an expanding periodic-box reference without changing the historical linear theory.

This PASS is a theory/component result. It does not establish that memory survives a self-consistent screened AeST state reclosure or changes nonlinear collapse.

Historical v0.77/v0.78, NL0B, NL1C0-NL1C3A, and all historical FAIL/INCOMPLETE classifications remain unchanged.
