# GE08 full first-order state bridge — result freeze

## Status

Frozen first locked GE08 execution.

Historical terminal classification:

`GE08_FULL_FIRST_ORDER_STATE_BRIDGE_FAIL`.

GitHub Actions run:

`35490987917`.

Execution HEAD:

`a25e0d1769ba2f0b4eb77ac2bde96490bf83a644`.

Artifact:

- ID: `10599311741`;
- name: `results_bundle_ge08_full_first_order_state_bridge`;
- ZIP SHA-256:
  `13720bd03b0db0da3f5c02642e93feb23bf0d36cb9ced787888b36ab1b2c3bc0`.

## Frozen output hashes

Result JSON:

- bytes: `2807`;
- SHA-256:
  `b0ef0d80d16700f2eca7ef9ead05d83027d5c79b3832ff15ed8394c7c3aab531`.

Result log:

- bytes: `2807`;
- SHA-256:
  `b0ef0d80d16700f2eca7ef9ead05d83027d5c79b3832ff15ed8394c7c3aab531`.

Result NPZ:

- bytes: `13230`;
- SHA-256:
  `807833b6692f91f10d4716be1f59baee8f7376d1569fbabec9d76d3e35bbe8fd`.

Legacy chi trace:

- bytes: `350249`;
- SHA-256:
  `aed5ed209239f35adaaa35be7114df7dbd440f01f830b26cddc33d8b34aefcbf`.

Full-state trace:

- bytes: `1611070`;
- SHA-256:
  `3ee90a0cf6a281214b35f0eafe30efdd99bb540b80793eccf3dfa7c76f41c01a`.

Diagnostic patch report:

- bytes: `489`;
- SHA-256:
  `b61f1f2747b44f577cf1bf54b58033d036211a409877344cd0ec4af378a8c7fa`.

Preregistration JSON:

- bytes: `4535`;
- SHA-256:
  `6935f30caf8f48435390d83690d078b00185994d7b3974205285f14ae5473089`.

Implementation lock:

- bytes: `3629`;
- SHA-256:
  `6ef7506d0a9dcacf66696564adb921e9789c0d907f66493d8e6e5555c100b99d`.

## Frozen result

Trace counts:

- legacy rows: `2904`;
- full-state rows: `2904`;
- selected rows in the frozen signal/redshift window: `48`;
- distinct native times: `8`.

Exact or machine-level successful controls:

- legacy/full k-tau grid error: `0`;
- reconstructed chi versus historical chi trace: `0`;
- native traced delta_m versus CLASS source: `0`;
- requested k miss: `0`;
- native tau mismatch: `0`;
- all values finite.

Failed preregistered controls:

- alpha-prime numerical dy identity:
  `2.2022065445364682e-4`;
- phi-prime numerical dy identity:
  `1.18987731579593e-8`.

Both exceed the frozen `1e-12` limits.

Therefore the historical GE08 classification remains FAIL.

## Matter diagnostic from the failed run

This information is descriptive only because the bridge itself did not certify.

After subtracting the frozen AeST effective-dark contribution from the CLASS total scalar stress:

- standard pressure / standard density relative L2:
  `4.0296809261404915e-7`;
- standard shear / standard density relative L2:
  `5.717716788656947e-10`;
- standard density versus baryon-only relative L2:
  `1.3238516018121685e-3`.

Thus the exact `1e-12` single-pressureless-fluid readiness condition would not pass even if the bridge gates had certified.

No approximate pressureless closure is licensed by this result.

## Post-result implementation diagnosis

Inspection of the pinned CLASS NDF15 evolver establishes the source-callback derivative semantics.

At exact source points the output callback can receive the integrator derivative workspace. At overshot source points NDF15 explicitly computes

`yinterp, ypinterp, yppinterp`

from the backward-difference interpolation polynomial and calls

`output(t_vec[next], yinterp+1, ypinterp+1, ...)`.

Therefore the `dy` argument of `perturbations_sources()` is not guaranteed to be a freshly evaluated physical RHS at the interpolated source state.

The two failed GE08 gates compared:

- `dy[index_pt_phi]` with the freshly reconstructed Einstein `phi_prime`;
- `dy[index_pt_alpha_aest]` with the exact AeST RHS `a(E-psi)`.

At interpolated source nodes these compare an interpolating-polynomial derivative with a freshly evaluated physical RHS. Equality at `1e-12` is not a valid source-callback invariant.

This diagnosis is consistent with the result pattern:

- state/grid quantities that depend only on the current source state pass exactly;
- only the two gates using callback `dy` fail.

## Claim boundary

This freeze does not relabel GE08.

It does not certify the first-order state bridge and does not license `Z20`.

It licenses at most one narrowly scoped follow-up preregistration addressing the source-callback derivative semantics without changing:

- the physical model;
- the trace grid;
- the state dictionary;
- the accepted `chi`, `delta_m`, k or tau controls;
- the exact matter-completeness threshold.

Any repaired bridge must still classify the full CLASS pressureless-matter readiness independently.
