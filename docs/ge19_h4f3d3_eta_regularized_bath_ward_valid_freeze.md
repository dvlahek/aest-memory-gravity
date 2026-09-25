# GE19 H4F3d3 — exact eta-regularized bath parent Ward result

## Classification

`GE19_H4F3D3_ETA_REGULARIZED_BATH_WARD_PARENT_DERIVED`.

This closes the specifically open physical `sqrt(eta)`
regularization of the GE05 bath parent in the signed
mixed H4 spatial Ward identity. It is an exact action-level
result under the pre-existing, frozen NL0B and Repair32A
conventions. **It is not full H4F3d all-sector/actual-grid
Noether certification and it does not solve Z21.**

## Immutable provenance

Predata:
`ge19/h4f3d3_predata_eta_regularized_bath_ward_parent.json`,
blob `ff7720381ddd09c7c073e106b2f35065ac3d1d6f`.

Implementation:
`ge19/h4f3d3_eta_regularized_bath_ward_parent.py`,
blob `fb340b957c31e34d35f1ebd9404a53b59d29c102`.

Dedicated GitHub Actions
`.github/workflows/ge19-h4f3d3-eta-bath-ward.yml`:
run `36105927210`, job `107978300500`,
conclusion `success`, marker
`GE19_H4F3D3_ETA_REGULARIZED_BATH_WARD_PARENT_PASS`.
Result JSON SHA-256:
`1d59931e887d9c370398d198afae6c9c7197b8b65d6f375f3a047fbae247597b`.
Artifact ID `10850144579`.

Every pinned-source, frozen action, Euler chain-rule,
mixed epsilon/eta and negative-control gate passed.

## Exact physical Ward correction

Frozen NL0B completed-square physical field:

`U_j=sqrt(eta) q_j`,
`L_mem,phys=eta L_GE05,red(q_j,X_phi)`.

The frozen Repair32A relative raw GE05-to-GE06
Euler normalization is **2**. Consequently the
bath contribution to the GE06 raw spatial
off-shell Ward parent is

`W_q,GE06=+2 eta sum_j E_qj,GE05,red * partial_x q_j`.

With the frozen zero bath background,
`q_j=epsilon q_j10+O(epsilon^2)` and
`E_qj,red=epsilon E_qj10+O(epsilon^2)`,
the exact physical mixed derivative is

`partial_eta partial_epsilon^2 W_q|0
    = +4 sum_j E_qj10,GE05 * partial_x q_j10`.

There is **no direct** `q_j20`, `q_j11`,
`E_qj20` or `E_qj11` contribution
to this coefficient. Those variables can
still enter other H4 sources and E21 through
the full corrected parents. Do not replace
the full source by this parent coefficient.

The composite action Ward is continuously
differentiable from physical `eta->0+`,
even though the unrescaled physical field
`U_j=sqrt(eta)q_j` itself does not
admit an ordinary integer-power eta Taylor
series. The exact one-sided derivative,
action chain rule and direct regularized
eta derivative agree.

If every **first-order normalized bath**
Euler equation `E_qj10=0` holds exactly,
this explicit off-shell parent product vanishes.
Its numerical value under approximate frozen
first-order parents must be evaluated and
included in the final all-parent Ward
error budget, not silently dropped.

The earlier H4F3d2 formula for the bath
that treated the physical q field with
ordinary integer eta expansion was
explicitly labelled as not yet
eta-regularized. H4F3d3 supplies its
missing term without retrospectively
relabeling H4F3d2 or editing any
old source/solver.

## Next licensed structural action

Combine this signed bath term with the
frozen H4F3d1 **canonical operator Ward**,
the H4F3b actual six-piece physical-clock
source Ward, the H4F3d2 dust/bath currents
and all nonbath background/H1/Z11 parent
Euler and boundary terms in one full
action-level identity.

The actual H4F3b source NPZ and original
Repair32B Z11 were generated locally.
They are not automatically inside
the GitHub Actions checkout. A
manufactured test cannot be promoted
to physical all-sector certification.

The original active-shift target
`1e-6` and matched-order threshold
`>=2.5` are unchanged. Historical
Repair37 science FAIL and Repair38--44
diagnostics remain immutable.
**Z21 NOT CERTIFIED; lensing blocked.**
