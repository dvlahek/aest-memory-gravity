# GE09 dense accepted-step local-jet bridge — result freeze

## Status

Frozen first science-reaching GE09 execution.

Terminal classification:

`GE09_DENSE_ACCEPTED_STEP_LOCAL_JET_BRIDGE_FAIL`.

GitHub Actions run:

`35494446296`.

Execution HEAD:

`4b753c38a6bd5b34492e1481c6ac3538863af382`.

Artifact:

- ID: `10600457104`;
- name: `results_bundle_ge09_repair01_native_cli_local_jet`;
- ZIP SHA-256:
  `494639b2074336e704e06cf18b8875bc88d71c62cebfdb687e8e4c3f5270da38`.

## Frozen output hashes

Result JSON:

- bytes: `5797`;
- SHA-256:
  `78001c9f1bf6c69a1f3826b7ca4639bf19ae2cdc3f3c4a6a89a06f3f1aa7f494`.

Result log:

- bytes: `5797`;
- SHA-256:
  `78001c9f1bf6c69a1f3826b7ca4639bf19ae2cdc3f3c4a6a89a06f3f1aa7f494`.

Result NPZ:

- bytes: `91676`;
- SHA-256:
  `70d9097069c2cc1808db39c605bb1f70d58be744ba5f5a22b525fe0a7f6a9967`.

Dense accepted-step trace:

- SHA-256:
  `96cac787a7d5d7b70b7a7b95ba04de28c2cbaa50c94f6818526a0ed96f28eb38`.

Accepted source-state trace:

- SHA-256:
  `3ee90a0cf6a281214b35f0eafe30efdd99bb540b80793eccf3dfa7c76f41c01a`.

Native CLASS log:

- SHA-256:
  `3b4b61c832e69af76f5c45070dec8f2401527cd6f99f4f535768ea5c0517b164`.

All six official CLASS scalar perturbation tables are present and reproduce the dense trace exactly.

## Science gate result

PASS:

- successful-step lifecycle identity;
- dense trace versus official CLASS CLI perturbation tables;
- at least 16 accepted endpoints per k in the frozen window;
- exact 64-node common grid;
- primary versus decimated global relative L2;
- primary versus decimated pointwise control;
- scalar pt closed/product-rule identity;
- finite complete jet.

FAIL:

- source-grid state validation.

Frozen limit:

`1e-4`.

Observed global maximum:

`1.0032254188771416e-4`.

The threshold is not relaxed.

## Source-grid field errors

Maximum abs-or-rel mismatches:

- phi: `1.0784256933293879e-7`;
- psi: `1.5016585419538875e-5`;
- delta_dark: `1.0032254188771416e-4`;
- theta_dark: `7.392193725697105e-6`;
- alpha_aest: `3.178787481547386e-6`;
- E_aest: `2.0040479833848133e-6`;
- Q: `2.710505431213761e-20`;
- H/H0: `1.558626763583445e-5`;
- rho_dark: `7.378907655892084e-12`;
- p_dark: `7.497562463514804e-26`;
- cad2_dark: `1.4859400166424919e-21`.

Only `delta_dark` exceeds the frozen gate.

The exceedance above the gate is

`3.225418877141567e-7`.

## Jet-control result

Every 15-entry local-jet control passes.

Global primary-versus-decimated relative-L2 maximum:

`2.36737979893189e-4`

against the frozen `5e-4` limit.

Pointwise abs-or-rel maximum:

`1.0147205819278222e-4`

against the frozen `2e-3` limit.

The largest global relative-L2 entry is `Nx`.

The exact scalar `pt` closed/product-rule identity error is

`2.168404344971009e-19`

against `1e-12`.

## Trace result

Dense trace rows:

`30755`.

Source-state rows:

`2904`.

Accepted points per k in `0.2<=z<=1.5`:

`{17,17,20,20,22,30}`.

Maximum ln(a) gaps per k are approximately

`0.037--0.0475`.

The dense trace and official CLASS perturbation tables agree exactly:

`0` abs-or-rel maximum.

## Scientific interpretation

GE09 establishes that the proposed dense accepted-step representation is internally stable and reconstructs the complete GE06 local jet with strong primary/control agreement.

However, under the preregistered independent accepted-source-state validation, the reconstructed `delta_dark` state misses the frozen `1e-4` gate by a small but real amount.

Therefore the complete GE06 local jet is not certified.

This FAIL is not a threshold-tuning invitation.

## Project boundary

Do not:

- relax the `1e-4` source-grid gate;
- relabel GE09 as PASS;
- proceed to `Z20`;
- infer that the complete local jet is certified.

A separate diagnostic may localize the `delta_dark` mismatch and characterize if it arises from the accepted-endpoint interpolation representation or from a physical/state inconsistency.

Such a diagnostic cannot retroactively change the GE09 classification.
