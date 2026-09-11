# Full-J Weyl / lensing closure audit

Date: 2026-09-11

Status: **THEORY / INTERFACE AUDIT FROZEN BEFORE STATIC-WEYL ARTIFACT GENERATION**

Parent locked full-J Jacobian result:

```text
8b6655d875ad04ab478da320ec42445a58ce4413
FULLJ_MODE_COUPLING_JACOBIAN_NODE_COUPLING_SUPPORTED
```

This audit fixes the metric and Weyl conventions that may be used after the locked full-J Jacobian result. It does not license an ACT likelihood or an observational claim.

## 1. Longitudinal metric convention

The project uses longitudinal/Newtonian-gauge weak-field potentials in the convention

\[
 ds^2=-(1+2\Psi)dt^2+a^2(t)(1-2\Phi)d\mathbf x^2.
\]

The full-J frozen quasistatic reclosure solved in the PoC, dense-map and Jacobian phases returns the total scalar potential

\[
\Phi=\widetilde\Phi+\chi.
\]

## 2. Static/fixed-a full-J closure

The D1A longitudinal weak-field reduction fixes the static dust gate as

\[
\Psi=\Phi,
\qquad E=\Phi,
\qquad U=-Q_0\Phi,
\]

and reduces exactly to the frozen full-J equations used by the current nonlinear solver.

Therefore, **within exactly this static/fixed-a snapshot approximation**, the project Weyl convention is

\[
W\equiv\Phi+\Psi=2\Phi.
\]

Consequently the local mode-coupling Jacobian obeys the zero-parameter identity

\[
\boxed{K^W_{ij}=2K^\Phi_{ij}}.
\]

This scaling preserves:

- all fitted log-slopes in `k`;
- all off-diagonal/diagonal coupling ratios;
- all local bump ratios;
- the node-coupling classification.

It only doubles the complex response amplitude and multiplies a power constructed from the same response by four.

This is a bookkeeping/theory mapping, not a new nonlinear solve.

## 3. Evolving FLRW closure is not `Psi = Phi` by assumption

D2C5 passed the action-level FLRW longitudinal reduction. At the retained MOND weak-field order, the nonlinear constitutive completion changes the scalar-current sector but does not introduce a new independent completion-dependent metric correction; the metric/effective-fluid forcing sector remains the corrected linear AeST one at that order.

D2C6G then passed the eta=0 direct metric-tangent calibration and explicitly projects separate `Phi`, `Psi`, and `Weyl` fields. Its implemented Fourier-space Newtonian-gauge metric projection uses the density-like, momentum-like and shear-like source pieces. In the implementation,

```python
ph[mask] = -1.5 * a**2 * (
    k2[mask] * rh[mask] + 3.0 * Hconf * qh[mask]
) / (k2[mask] * k2[mask])
ps[mask] = ph[mask] - 4.5 * a**2 * sh[mask] / k2[mask]
weyl = phi + psi
```

Thus the project convention is explicitly

\[
\boxed{W=\Phi+\Psi},
\]

and in evolving FLRW the slip is controlled by the retained metric/shear source rather than being set to zero by hand.

No free slip parameter, phenomenological Poisson factor, or ad hoc GR replacement is licensed.

## 4. D2C6H status

The final self-consistent metric-feedback tangent stage D2C6H is already preregistered and implemented:

```text
preregistration: 2f31fc65874bda220a651361b64d7255116709cf
implementation:  f8fdfb34a4c64b0677291662cdc569c439bdd553
```

It restores the missing coupled tangent feedback

\[
v_\alpha'=a(v_E-v_\Psi)
\]

for the finite-memory/eta response chain. No committed executed D2C6H result was found during this audit.

D2C6H is therefore the remaining preregistered self-consistency certification before the **finite-eta / memory metric-response chain** can be treated as closed. It is not required to establish the static eta=0 identity `W=2 Phi` above.

## 5. What the locked full-J Jacobian now licenses

For the frozen static snapshots only, the already certified 27 full-J response matrices may be transformed without refitting as

\[
K^W=2K^\Phi.
\]

The locked diagonal result therefore remains

\[
K^W_{ii}(k)\propto k^{-2}
\]

with exactly the same fitted slopes as the locked `Phi` Jacobian:

```text
diag_slope_min    = -2.081550211198209
diag_slope_median = -2.0056427140938844
diag_slope_max    = -1.9150696997181162
```

Likewise, the z=0.25 source-node / nonlinear mode-coupling interpretation is unchanged.

## 6. What this does NOT license

The static Weyl mapping does **not** yet produce a cosmological CMB-lensing prediction. In particular:

- the response was measured around a deterministic one-dimensional fixed-phase multimode source realization;
- the source amplitudes were constructed from linear CLASS baryon transfers rather than a self-consistent nonlinear matter evolution;
- the response is mode-coupled, so no scalar `T(k,z)` replacement is justified;
- a statistical source covariance / ensemble prescription is still required to turn a mode-coupled operator into a Weyl power spectrum;
- an evolving FLRW metric history must use the certified metric projection rather than extending `Psi=Phi` outside its static gate;
- no ACT likelihood is licensed at this stage.

## 7. Correct statistical operator structure

For a Weyl response matrix `K^W` and source covariance `C^S`, the discrete power mapping is

\[
P_{W,i}=\sum_{j\ell}K^W_{ij}\,C^S_{j\ell}\,K^{W*}_{i\ell}.
\]

Only when the source covariance is diagonal does this reduce to

\[
P_{W,i}=\sum_j |K^W_{ij}|^2P_{S,j}.
\]

Because the locked Jacobian demonstrates material off-diagonal mode coupling, replacing this operator by a scalar transfer multiplier would discard the very effect that resolved the dense-map node anomaly.

## 8. Frozen next-step decision

The immediate eta=0 next step is therefore **not ACT** and not another UV/Jacobian sweep. It is:

1. generate the deterministic static snapshot Weyl response artifact `K^W=2K^Phi` from the locked Jacobian, with exact regression checks;
2. formulate a controlled source-covariance / ensemble test for the mode-coupled operator;
3. only after a statistically meaningful Weyl-power construction is certified, consider a line-of-sight lensing projection.

Separately, D2C6H may be executed as the one already-preregistered outstanding certification for the finite-eta/memory metric-feedback chain.

```text
STATIC_SNAPSHOT_WEYL_MAPPING_LICENSED=True
EVOLVING_FLRW_WEYL_POWER_LICENSED=False
ACT_LIKELIHOOD_LICENSED=False
OBSERVATIONAL_CLAIM_LICENSED=False
```
