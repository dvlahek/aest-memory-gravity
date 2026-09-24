# GE19 H4 structural Stage B — reduced spatial-Ward primitive audit freeze

## Result and scope

The restricted analytic GE19 H4 Stage B subset completed successfully:

`GE19_H4_STAGEB_GEOMETRIC_WARD_PRIMITIVES_COMPLETE`.

GitHub Actions successful audit:
`35979279801`, job `107567029986`,
head `35343dddaf7d8ceae889fd6c344e772f26f18a7f`.

The job log includes terminal marker
`GE19_H4_STAGEB_REDUCED_WARD_PRIMITIVES_AUDIT_PASS`.

Frozen successful job artifact:

- artifact name: `ge19_h4_stageb_reduced_ward_primitives`;
- artifact ID: `10799212488`;
- JSON: `results/ge19_h4_stageb_geometric_ward_primitives.json`;
- JSON SHA-256:
  `53feb4cad6da7d86edfe2dc1eeecbc932c26d81063951e1a9e52bf1db676da44`;
- JSON bytes: `3323`.

Script:
`ge19/h4_structural_stage_b_geometric_ward_primitives.py`,
blob `5695cf064dcc32bf4385687cbe6052521f2e36b4`.

Workflow:
`.github/workflows/ge19-h4-structural-stageb-primitives.yml`,
blob `72d00a341ede3bfd39ca06dbf8a0a236e01555ff`.

Preregistration:
`ge19/h4_structural_stage_b_predata_action_noether_identity.json`,
blob `11123763b2f5bf06ac6f704acffdea0b4eb34f1d`.

Source-row ledger:
`docs/ge19_h4_structural_stage_a_source_row_ledger.md`,
blob `44d4f01a05aba26926d6a8e13a2b7aac995258d5`.

An earlier workflow attempt `35979244415` failed **before the
symbolic test ran**, because shell output redirection targeted the
missing `results/` directory. Commit
`35343dddaf7d8ceae889fd6c344e772f26f18a7f`
added `mkdir -p results`, and the subsequent run completed all
symbolic and claim-boundary checks successfully. The failed setup
attempt remains part of the workflow history.

## What the symbolic audit established

Under an arbitrary reduced spatial diffeomorphism `xi(t,x)`,
using `N,R,u,phi,T,rho` as spatial scalars,
`L` as a longitudinal density, and

`delta b = partial_t xi + xi partial_x b - b partial_x xi`,

the following ten frozen reduced action building blocks transform
exactly as scalar invariants or, for the volume, a spatial density:

1. `N L R^2` (spatial density);
2. GE06 `kL`;
3. GE06 `kR`;
4. GE06 scalar derivative `sigma`;
5. GE06 `Qinv`;
6. GE06 `Xinv`;
7. GE06 aether `E`;
8. GE05 reduced per-node bath derivative `Aq`;
9. GE07 dust `W`;
10. GE07 dust `V`.

The GE05 check treats the frozen reduced per-node `q` variable
as a spatial scalar. **It does not certify the full NL0B
covariant bath-vector/projector transformation.**

The formal Euler-Lagrange spatial-Ward integration-by-parts identity
has the verified reduced geometric sign structure:

`E_N N_x + E_L L_x + E_R R_x + E_b b_x
 + sum E_field field_x
 - partial_x(L E_L - b E_b)
 - partial_t E_b = 0`

*if the full reduced action is invariant under the stated
transformations, with boundary terms accounted for*.

The isotropic/anisotropy projection is exact:

`E_L = (E_isotropic + 2 E_anisotropy)/3`,
`E_R = (2 E_isotropic - 2 E_anisotropy)/3`.

The frozen GE05 per-node memory action also gives an exact
independent shift variation:

`dL_mem/db = -(L R^2/2)[Aq cosh(u) q_x
 + (omega q - sqrt(w) X_phi) sqrt(w) sinh(u) phi_x]`.

Its second directional FLRW coefficient is exactly

`-a^3 dqt dqx`.

Hence the mapped M2 source has a genuine shift-row contribution
before bath summation and Fourier projection. This is an
action-derived fact, not a fitted numerical cancellation.

All twelve reduced transformation/formal-projection checks,
both exact GE05 shift identities and all frozen source-blob
controls passed.

## What remains unproved

**The full H4 source/Noether identity is NOT CERTIFIED.**

The successful restricted audit is not an action-by-action,
covariant all-sector H4 proof. Before any integrated H4 science
reclosure, the next analytic work must:

- derive and check the correct NL0B bath-vector/projector
  transformation, including bath EOM and boundary terms;
- incorporate the nonanalytic Y2 sector and any zero-set subtleties;
- derive the complete off-shell spatial Ward relation from the
  frozen GE06+GE07+Lambda+Y2+NL0B action before imposing
  the isotropic `L=R` reduction;
- extract the exact mixed H4 coefficient and all terms proportional
  to certified background/H1/H2/bath/dust parent residuals;
- give the signed contribution of each of the six frozen H4 source
  pieces to the independent shift and other row terms;
- only then evaluate the complete identity in one common parent/time
  representation with the unchanged original local science scale.

Existing Repair06 Noether-regularized algebraic rank diagnostics are
not a substitute for this complete source identity.

No numerical H4/Z21 solve was performed by Stage B.
Repair37 remains immutable science FAIL.
Repair44 remains diagnostic-only.
Z21 remains NOT CERTIFIED; lensing remains blocked.
