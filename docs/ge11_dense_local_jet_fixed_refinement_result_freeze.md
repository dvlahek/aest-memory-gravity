# GE11 fixed dense local-jet refinement — result freeze

## Status

Frozen first locked GE11 execution.

Terminal classification:

`GE11_DENSE_LOCAL_JET_FIXED_REFINEMENT_FAIL`.

GitHub Actions run:

`35495077694`.

Execution HEAD:

`210a64cee9df6feac010c17b32c5294f56236d40`.

Artifact:

- ID: `10600443147`;
- name: `results_bundle_ge11_dense_local_jet_fixed_refinement`;
- ZIP SHA-256:
  `cfacfd970606accfcc7fc816ca0d754c4fc87321d1e793f1e0b1b7d90cbbf9d6`.

## Frozen output hashes

Result JSON:

- bytes: `11918`;
- SHA-256:
  `4dfe08700ca7a2ab46f9155049c06175d8ccb200c048b61780603210e7fa48ad`.

Result log:

- bytes: `11918`;
- SHA-256:
  `4dfe08700ca7a2ab46f9155049c06175d8ccb200c048b61780603210e7fa48ad`.

Result NPZ:

- bytes: `91562`;
- SHA-256:
  `01fab2ff3bdf297262a33d03d0242cd0c6593aeca315eb255a1c418361679986`.

R1 dense accepted-step trace:

- bytes: `12669112`;
- SHA-256:
  `96cac787a7d5d7b70b7a7b95ba04de28c2cbaa50c94f6818526a0ed96f28eb38`.

R2 dense accepted-step trace:

- bytes: `12669112`;
- SHA-256:
  `96cac787a7d5d7b70b7a7b95ba04de28c2cbaa50c94f6818526a0ed96f28eb38`.

R1 source-state trace:

- bytes: `1611070`;
- SHA-256:
  `3ee90a0cf6a281214b35f0eafe30efdd99bb540b80793eccf3dfa7c76f41c01a`.

R2 source-state trace:

- bytes: `1611070`;
- SHA-256:
  `3ee90a0cf6a281214b35f0eafe30efdd99bb540b80793eccf3dfa7c76f41c01a`.

The identical R1/R2 trace hashes are part of the frozen result.

## Science gate result

Both R1 and R2 reproduce the historical GE09 source-grid maximum exactly:

`1.0032254188771416e-4`

against the frozen single-level limit

`1e-4`.

Therefore both single-level gates fail.

All complete-jet internal controls pass.

R1/R2 complete-jet disagreement is exactly zero because the two runtime traces are identical.

GE11 therefore remains FAIL.

The `1e-4` source gate is not relaxed.

## Post-result implementation diagnosis

Pinned CLASS commit

`e85808324f51fc694d12e3ed7439552a3c3f9540`

defines the active precision parameters in

`include/precisions.h`

as

`tol_perturbations_integration`

and

`perturbations_sampling_stepsize`.

The frozen GE11 precision files instead used the historical singular names

`tol_perturb_integration`

and

`perturb_sampling_stepsize`.

The same historical singular names are present in

`v019p/pre/p3.pre`.

Thus the intended p3/R1/R2 perturbation precision values were not bound to the active pinned-CLASS precision fields.

This explains the exact R1/R2 trace identity.

The diagnosis does not relabel GE11.

## Provenance consequence

Historical GE09/GE10 numerical results remain valid as measurements of the runtime that actually executed.

However the earlier description of that runtime as using the intended p3 values

`tol_perturb_integration=5e-8`

and

`perturb_sampling_stepsize=0.0025`

is not valid for the pinned CLASS commit.

For provenance, the historical GE09/GE10 accepted-step representation must be treated as the **actual pinned-CLASS runtime representation with the singular precision keys ignored**, not as a certified p3-precision execution.

No historical PASS/FAIL classification is changed by this provenance correction.

## Licensed continuation

Exactly one implementation-only repair track is licensed.

It may:

1. keep the frozen GE11 numerical values unchanged:
   - R1: `2.5e-8`, `0.00125`;
   - R2: `1.25e-8`, `0.000625`;
2. replace only the two obsolete precision-key names by the active pinned-CLASS names:
   - `tol_perturbations_integration`;
   - `perturbations_sampling_stepsize`;
3. add static provenance checks that the corrected names exist in pinned `include/precisions.h`.

It may not:

- change either numerical precision pair;
- add R3;
- relax the `1e-4` gate;
- change the interpolation family;
- drop the historical worst source row;
- alter jet controls.

A repaired execution is a new GE11 Repair01 result and cannot retroactively relabel this GE11 FAIL.
