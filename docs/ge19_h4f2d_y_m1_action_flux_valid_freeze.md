# GE19 H4F2d — exact action-flux subset for Y and GE05 M1

Classification:
`GE19_H4F2D_Y_AND_M1_FLUX_SUBIDENTITY_PASS`.

This is an analytic and deterministic **two-piece
source-local** control within the full H4F2
preregistration, not a complete six-piece
spatial Ward/source-parent certificate or
an H4/Z21 science result.

## Frozen provenance

Preregistration:
`ge19/h4f2d_predata_y_m1_flux_compatibility.json`.

Implementation:
`ge19/h4f2d_y_m1_action_flux_audit.py`,
blob `c2e6d74ba332cd3b083cecce170fa0de1e8d3f61`.

Dedicated GitHub Actions workflow:
`.github/workflows/ge19-h4f2d-y-m1-flux.yml`.

Successful run `36026024031`, job
`107722650441`,
terminal marker
`GE19_H4F2D_Y_M1_FLUX_SUBIDENTITY_PASS`.
Artifact ID `10819324031`.
JSON
`results/ge19_h4f2d_y_m1_action_flux.json`,
SHA-256
`132e8589c1793bf5591beb2c638fe0d5cefb83713df561e4586d011dedec15c6`.

All frozen blob/source-action bindings, exact
symbolic identities, and deterministic Fourier
gates passed for beta0=1,0.5,0.1.
No corrected H3F/H3G fields were propagated
or used to fit coefficients.

## Exact Y and GE05 M1 relation

With `a=a(t)`, `Q=Q(t)` and
`kappa=2(2-KB)/[(1+beta)a0]`,
the action-derived H4 Y source is

`S_u,Y=+2 a^3 Q kappa P[2|g10|g11]`,
`S_phi,Y=-2 a^2 kappa d_x P[2|g10|g11]`.

The frozen GE05 M1-to-GE06 raw Euler scale
is exactly two (Repair32A). Thus the frozen
implemented M1 H4 source is

`S_u,M1=+a^3 Q B20`,
`S_phi,M1=-a^2 d_x B20`,

where `B20=X20-weighted_z20`.
The verified action-flux identity in **each**
of these sectors is

`d_x S_u+a Q S_phi=0`.

Both sources have exactly zero Y/M1
metric and independent shift/anisotropy
constraint rows at this perturbative
order. The identity uses the *same*
2/3-projected flux in both Stage E
Y main rows and the original complex
Fourier k convention for M1.

The H3G NPZ stores the certified
`weighted_z20`, so it is sufficient
for **implemented** M1. H3G nodal
q20 evolution must not be represented
by a single weighted scalar inside
a complete off-shell bath parent
variation, even though the reduced
implemented M1 depends only on B20.

## Remaining full H4 identity

The two flux identities constrain the
relative Y/M1 aether and scalar source
signs. They do not assert that any
independent shift source vanishes and
do not prove the six-piece source Ward
compatibility. In particular,
GE06, GE07 and GE05 M2 contribute
nontrivial independent constraint
source families; parent bath/dust,
boundary and discrete FD4/FD8 terms
must be kept explicitly.

The original Repair37 science FAIL
is unchanged. The full H4F2 source/
parent identity and common corrected
parent/time-grid structural audit
remain open. No H4/Z21 solve was
performed. The original 1e-6
shift target remains unchanged.

Z21 NOT CERTIFIED; lensing blocked.
