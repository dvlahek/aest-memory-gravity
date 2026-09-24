# GE19 H3G — valid local corrected-Y q20 science result freeze

## First result and scientific classification

`GE19_H3G_CORRECTED_Y_Q20_RECONSTRUCTION_PASS`.

The first local H3G science execution reported terminal
marker `GE19_H3G_CORRECTED_Y_Q20_SCIENCE_PASS`
and no failed gates. This certifies **only** the
separately versioned window-local particular
normalized-bath weighted q20 projection on the
already certified H3F action-completed-Y Z20
low-mode parent. The first-order full-history
bath remains the frozen Repair26 R1
cancellation-free trace.

There is no all-sector H4 Noether certificate,
no H4/Z21 science solve, no homogeneous or
primordial bath mode, no finite eta, no lensing
and no observational inference.

Historical Repair27 remains its own valid
q20 result on historical Repair22 Z20.
Historical Repair24 remains FAIL and Repair37
remains H4/Z21 science FAIL. All older
source-patch diagnostics remain immutable.

## Input/output provenance from user-uploaded files

The following **three** local H3G files were
uploaded and read independently:

| File | Bytes | SHA-256 |
|---|---:|---|
| `results/ge19_h3g_corrected_y_q20_reconstruction.json` | 9796 | `9b93534e3ee90e1ce588bdbd3f271afd041f738b8dc6f62c4ec0d1413c27f2c4` |
| `results/ge19_h3g_corrected_y_q20_reconstruction_FULL.log` | 9796 | `9b93534e3ee90e1ce588bdbd3f271afd041f738b8dc6f62c4ec0d1413c27f2c4` |
| `results/ge19_H3G_LOCAL_runner.log` | 6637 | `553ca1c357ea88c5922d7889415aa3fc0465b415cdd62c6bb2636f4c3a3e759a` |

The uploaded JSON and inner FULL log are
byte-identical. All 13 science gates in
the uploaded JSON are true. The runner
reports the NPZ file as:

`results/ge19_h3g_corrected_y_q20_reconstruction.npz`,
3550825 bytes, SHA-256
`9e1bf36e1d81122225ff8c03f663501de7601a8fc9376fd86312e0ae1d809452`.

**Important audit limitation:** H3G NPZ
was **not attached** to this conversation.
Its SHA and byte count above are reported by
the local runner, not independently
recomputed or inspected here. The science
classification is the result of the
hash-locked local code and uploaded
JSON/runner logs. A later independent
array audit must obtain the exact NPZ
before asserting byte-level independent
verification of every stored array.

## Frozen local science numbers

- full-history exact a0 partial-step mismatch: `0.0`;
- frozen Repair26 R1 full-history trace SHA-256:
  `608ee0b4c868a701db6976f756b9a551cd9ddffe1e8e4ab37c5cd2361405a6f8`;
- initial H1/X10 bridge:
  `3.981945660904338e-11` vs `1e-10`;
- GE05 G2 spatial Nx256/512 low-mode L2:
  `3.4518767056924556e-15` vs `1e-10`;
- q20 quadrature Nq1024/2048 weighted L2:
  `8.236842515117324e-05` vs `1e-2`;
- q20 time Nt64/Nt128 weighted L2:
  `3.2441966580106844e-05` vs `5e-3`;
- z10 time Nt64/Nt128 weighted L2:
  `2.567987045993896e-05` vs `5e-3`;
- normalized sqrt(w) symbol elimination: PASS;
- interval propagator selftest: `0.0`;
- all cases complete and all computed outputs
  reported finite.

The q20 projection uses `weighted_z20=sum_j w_j z20_j`.
The representative primary weighted-z20 L2
ranges from approximately `1.581832e7`
(C_max) to `1.582480e7` (C_min).
These are computational norms, not
physical perturbation amplitudes.

## Report-only historical comparison

The local runner independently verified the
original Repair27 JSON/NPZ artifact hashes.
H3G weighted q20 relative L2 differences
against historical Repair27 are:

- C_min: `3.285031309966995e-12`;
- C_star: `3.2845303492248713e-12`;
- C_max: `3.2835798677346295e-12`.

This comparator has no required sign or
magnitude; it is not a science gate.
The numerically very small difference
does not make the corrected parent
interchangeable with the historical one.

## Next structural gate

The corrected-H3F/H3G Z20/q20 parent pair
is available for a **separately versioned,
pre-registered complete all-sector H4
source/Noether compatibility derivation and
numerical audit**.

The old Repair37 source dictionary cannot
simply be relabelled. H4 sources must be
reconstructed on one corrected parent/time
representation, including GE06, GE07,
Lambda, DY2, GE05 M1 and M2, and the
action-derived u+phi Y mixed eta-tangent
source. Any revised canonical mapping
and all parent residuals must follow
the covariant action and its Noether
identity, not be fitted against shift.

The frozen H4 structural stop gate remains:
`docs/ge19_h4_source_constraint_noether_structural_stop_gate.md`.

Before a H4 Z21 numerical solve,
derive the full identity with the exact
source signs/factors, parent equations,
boundary and normalized constraint rows.
Preserve original active-shift target
`1e-6`. Do not patch isolated GE06
shift source row0 or fit an interpolator
to residuals.

**Z21 NOT CERTIFIED. Lensing blocked.**
