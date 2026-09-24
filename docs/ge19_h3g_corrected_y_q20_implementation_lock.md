# GE19 H3G — corrected-Y q20 implementation lock

## Status

H3F is certified for its separately versioned action-completed
Y u+phi low-mode window-local Z20. H3G is the next
separately preregistered q20 normalized-bath reconstruction.

**H3G has no numerical science result yet.**
Its preexecution audit passed; no H3G q20 state
has been constructed or certified by the audit.

## Frozen new parent and local H3F proof

- H3F result freeze:
  `docs/ge19_h3f_corrected_y_z20_valid_local_science_result_freeze.md`,
  blob `e69fd766a36c219ecf46aa7bbf547a38c244f482`;
- H3F science JSON SHA-256:
  `0616188d2bb7a6c09b2b56433a1f8a1860f360b2e54d2cb84e1ae214a407866b`;
- H3F science NPZ SHA-256:
  `90840755fa9febb1d8cb84609d9e58f67dec2a0a01cd6bf8e47685b45caa4542`;
- H3F classification:
  `GE19_H3F_CORRECTED_Y_H3_Z20_CERTIFIED`.

The new H3F Z20 includes the action-completed
Y aether and scalar raw RHS rows and source-aware
projected p0. The old Repair22 Z20 is historical
only.

## H3G immutable preregistration and implementation

- predata:
  `ge19/h3g_predata_corrected_y_q20_reconstruction.json`;
  commit `5f9c52348164bbe515f1c32e066e98c033e1dff2`;
  blob `09fc1bd7fc06459d90fc6f6ba37a84adba757d37`;
- H3G source-parameter adapter and numerics:
  `ge19/h3g_corrected_y_q20_core.py`;
  commit `8c511ad42e3f6967347f18af527808b64746b280`;
  blob `688920e840a0a13bc85a6f416c2573cf0472eaa3`;
- frozen R1 parent/provenance wrapper:
  `ge19/h3g_corrected_y_q20_reconstruction.py`;
  commit `ece773cc53636b19b6fad32aa6e4142796bd163b`;
  blob `de929ae025e3ce58e60e6d229682cf885e7b1007`.

Inherited old physical core:
`ge19/repair24_q20_construction.py`,
blob `fc271987d1bddcd023cc9c057ddcad036b1d72fb`.

The new wrapper performs an exact AST comparison
of **every non-main helper function** against
Repair24 and asserts all unchanged science constants.
The only changed core main-level parent path,
parent hashes, parent classification and reporting
are explicitly versioned. The actual bath equations,
normalization, source G2, R1 full-history retarded
boundary, time/space/quadrature algorithms and
tolerances are unchanged.

Old Repair27 remains its original certified result.
The old Repair27 weighted-z20 may be compared
after its file hashes are verified, but its
numerical difference is report-only with no
required magnitude or sign.

## Preexecution CI

- workflow:
  `.github/workflows/ge19-h3g-corrected-y-preexecution.yml`;
- blob:
  `a6a60064cb8d979ee2c466a8a05a656d80fc6b45`;
- workflow commit:
  `1857a95ba45822fbe29e457ebc3e7dfb89b167f8`;
- run: `36013702448`;
- job: `107680654924`;
- conclusion: `success`;
- terminal marker:
  `GE19_H3G_CORRECTED_Y_Q20_PREEXECUTION_AUDIT_PASS`.

No q20 numerical solver was executed by CI.

## Exact science boundary

Only the second-order metric source Z20 parent
changes, from Repair22 to the H3F Z20.
The first-order full-history bath remains the
certified Repair26 R1 trace (SHA-256
`608ee0b4c868a701db6976f756b9a551cd9ddffe1e8e4ab37c5cd2361405a6f8`,
26643162 bytes).

In particular:
`G1[Z20_H3F,z20_H3G]+G2[(Z10,z10),(Z10,z10)]=0`;
`z20(a0)=0` and `dz20/dxi(a0)=0`;
the physical retained projection is
`weighted_z20=sum_j w_j z20_j`.

Unchanged Repair27 controls are H1 initial
bridge <=1e-10, GE05 G2 Nx256/512 <=1e-10,
q20 quadrature Nq1024/2048 <=1e-2,
q20 Nt64/128 <=5e-3, z10 Nt64/128 <=5e-3,
exact full-history a0 bracket and partial
step <=1e-15, normalized sqrt(w) elimination,
interval propagator selftest <=1e-12,
finiteness and complete C/beta/m cohorts.

An H3G PASS licenses only the new window-local
particular normalized q20 weighted projection.
It does **not** establish full H4 Noether,
Z21, finite eta, lensing or an observable.
The complete all-sector H4 source/Noether
identity remains a separate prerequisite.
