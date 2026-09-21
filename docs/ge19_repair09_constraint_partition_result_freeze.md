# GE19 Repair09 exact canonical-constraint partition result freeze

## Status

Frozen exact symbolic structural result.

Terminal classification:

`GE19_REPAIR09_SHIFT_PARTITION_STRUCTURALLY_SINGULAR`.

No alternative-partition science evolution was executed.

Repair07 remains historical FAIL. Repair08 remains the frozen shift-localization diagnostic.

## Provenance

Repair08 result freeze:

- commit `f08f3d076e58240766afa21df5df6b927146d67c`.

Repair09 preregistration:

- commit `d4d280748ff5f6140833ed876c484f7a6497d550`.

Initial dual-partition implementation:

- commit `d5312a74be737646739a0220c0414c44551f3577`.

Pre-result singularity amendment:

- commit `a9ac79a0e658431fc4b55ea5574e0890b8997870`.

Exact symbolic audit implementation:

- commit `780fa4f960177bc03a5c036ea2d707f3525af1f0`.

Exact symbolic workflow:

- commit `51b5ed9f9358e9842d4a6aa72106b16701760ff0`.

Workflow run:

- `35566754670`.

Job:

- `106230017067`.

Conclusion:

- `success`.

Artifact:

- ID `10623859759`;
- name `ge19_repair09_symbolic_partition_rank`;
- ZIP digest `sha256:bb73b397e7dba66103c7fa0841c433722d5988ffdefeda928991a62cf2e3a260`.

Terminal workflow marker:

`GE19_REPAIR09_SYMBOLIC_PARTITION_RANK_PASS`.

## Exact structural result

The local canonical algebraic unknown order is

`(N, delta_varrho, Sdot, udot, phidot, Tdot)`.

The five common rows are

`(pS, pu, pphi, pT, dust_density)`.

Using the **shift constraint** as the sixth row gives

- generic rank: `5`;
- determinant: `0`.

Therefore the shift-enforced six-by-six block is exactly rank deficient.

Using the **anisotropy equation** as the sixth row gives

- generic rank: `6`;
- determinant:
  `384*KB*KQQ*a^13*k^2`.

For the frozen Exp branch,

`KQQ = 4*K2*exp(Z^2)*(1+2*Z^2)`,

hence

`det = 1536*K2*KB*a^13*k^2*(1+2*Z^2)*exp(Z^2)`.

This is nonzero on the frozen domain because `K2>0`, `KB>0`, `a>0`, all solved modes have `k>0`, and `KQQ>0`.

It is algebraically the same determinant already frozen in Repair06 Amendment01 after writing `Z=(Q-Q0)/Z0`.

## Interpretation

The large prelock numerical condition number of the alternative block,

`1.5521269268870098e16`,

was the floating-point image of this exact rank deficiency.

Therefore the Repair07 choice to use anisotropy as the gauge-closing algebraic row is structurally necessary within this canonical variable set.

The shift equation must remain an independently propagated constraint. It cannot replace anisotropy to determine the six local algebraic unknowns.

The proposed Repair09 dual-partition local evolution is therefore invalid as a continuum test and was stopped before science execution.

The previously created local dual-partition runner is explicitly blocked on the branch.

## Combined Repair08 + Repair09 conclusion

Repair08 showed:

- the prescribed initial surface satisfies shift at `3.93e-8 < 1e-6`;
- the shift violation appears immediately under reduced propagation;
- full-standard CLASS momentum has the correct sign and closes the GE15 gravitational+AeST shift contribution;
- reduced dust develops a smaller off-shell mismatch;
- sign flips are excluded.

Repair09 now excludes the remaining simple DAE-partition alternative.

The next target is therefore the on-shell status of the **reduced background and omitted background sectors**, not a constraint-row swap or solver tuning.

## Claim boundary

This result is an exact structural DAE diagnosis only.

It does not alter GE06/GE07 equations, signs, thresholds, background, reduced matter, or historical results.

It licenses no H3/Z20 construction, finite eta, finite-amplitude nonlinear evolution, collapse, lensing or observational claim.
