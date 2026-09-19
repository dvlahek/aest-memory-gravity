# NL1C7B4 Repair19c3 — local result freeze

## Status

Frozen local WSL science result from the first locked Repair19c3 execution.

Terminal classification:

`NL1C7B4_REPAIR19C3_SELECTED_JACOBIAN_NONLINEAR_CLOSURE_FAIL`

with

`SCIENCE_RC=2`.

Execution HEAD:

`8317c38c1f6f3df18dcb4106c9b81f7bc543ceaa`.

This is a local WSL result, not an official GitHub Actions run.

## Frozen output hashes

- result JSON:
  - bytes: `258335`
  - SHA-256:
    `aa19480ce4d41f649368f192f27d85b823e0247aa6f9bcc9eb7a9d23b60ac5b0`
- evaluator log:
  - bytes: `258781`
  - SHA-256:
    `2483f37b8184783710b0f6e616d57c856e0291a3d136c3b682e58636754202b9`
- local runner log:
  - bytes: `269298`
  - SHA-256:
    `79933aa6817daf52a084cb0fecb6c05ba673954f8583c1767befb5100de1c4f1`.

No corrected-state NPZ was written.

## Gate result

PASS:

- G1 exact frozen provenance
- G2 orthonormal constrained basis
- G3 exact parent reproduction
- G4 selected first-step reproduction
- G7 two-grid correction amplitude
- G9 field-freeze invariant
- G10 output integrity
- G11 claim boundary.

FAIL:

- G5 exact canonical nonlinear closure
- G6 second-order correction scaling
- G8 all-branch lambda1 exact closure.

This is a science FAIL, not an implementation failure.

## Canonical result

- canonical PASS: `0/24`
- lambda=1 PASS: `0/6`
- maximum accepted iterations: `9`
- maximum exact epsilon_H:
  `1.1001073764772177e-06`
- maximum exact epsilon_M:
  `0.014197406485527293`.

Every canonical failure terminates through `backtracking_failed`.

## Lambda=1 exact constraint result

Final lambda=1 values:

- scale 5, Nr=256:
  - H `1.6180379166721286e-12`
  - M `6.054823142882067e-05`
- scale 5, Nr=512:
  - H `9.986339584518987e-13`
  - M `3.8593573410128915e-04`
- scale 10, Nr=256:
  - H `3.9191482059008666e-11`
  - M `1.8859803814742773e-04`
- scale 10, Nr=512:
  - H `4.773403030915984e-12`
  - M `4.113001684219245e-04`
- scale 20, Nr=256:
  - H `7.743932006594966e-11`
  - M `6.2117247534723366e-06`
- scale 20, Nr=512:
  - H `9.490012441715728e-12`
  - M `2.5047685697887067e-05`.

The failure remains momentum dominated.

## First-step certification

All six lambda=1 first steps reproduce the Repair19c2-selected `3-point, abs_step=3e-6` one-step probes exactly under the frozen tolerance.

For scale 5, Nr=256 the first selected step reproduces:

- rank: `508`
- predicted relative residual:
  `1.622885849080986e-12`
- max |yL|:
  `3.4723189539127793e-07`
- max |qRt|:
  `1.9009019632815645e-06`
- exact full-step frozen residual ratio:
  `6.52392742470065e-05`.

Thus the frozen Repair19c2 derivative choice is implemented exactly.

## Post-first-step stagnation

The important new feature is a severe scale separation after the first accepted step.

Representative scale 5, Nr=256:

- first physical step L2:
  `1.0912911463022467e-05`
- second direct step L2:
  `6.415431464959965e-12`
- third:
  `3.2117144296402627e-12`
- fourth attempted:
  `1.6298189828602541e-12`.

The selected finite-difference absolute step remains fixed at `3e-6`.

Thus after the first step the requested Newton corrections are approximately six orders of magnitude smaller than the finite-difference probe used to reconstruct the local Jacobian.

The same pattern appears in the other lambda=1 cases:

- scale 5, Nr512: step L2 drops from `1.55e-5` to `3.03e-11`, then to about `1e-13`;
- scale 10, Nr256: from `1.54e-4` to `1.23e-9`, then about `1e-13`;
- scale 10, Nr512: from `2.19e-4` to `1.65e-9`, then about `1e-13`;
- scale 20, Nr256: from `1.90e-4` to `1.92e-9`, then about `1e-13`;
- scale 20, Nr512: from `2.69e-4` to `2.72e-9`, then about `1e-13`.

The selected Jacobian fixed the first-step directional-fidelity problem, but a new post-step finite-difference scale floor remains.

## Scaling and grid controls

Five of six correction-scaling paths pass.

The only failure remains:

- scale 10, Nr512
- final gated slope:
  `2.2059249637207086`

against the frozen upper limit `2.2`.

This is a marginal excess and remains secondary because canonical closure already fails.

Two-grid lambda=1 correction amplitudes remain highly stable, with ratios close to `1.003`.

## Branch retests

All 54 branch rows are skipped due to canonical lambda=1 failure.

The reported `0/54` is therefore not 54 independently evaluated branch failures.

## Scientific interpretation

Repair19c3 establishes:

1. the Repair19c2-selected Jacobian is reproduced exactly;
2. the first nonlinear step is materially more faithful than the original default-Jacobian step;
3. the physical correction remains small and grid stable;
4. Hamiltonian closure is extremely strong;
5. momentum remains above the historical threshold;
6. after the first accepted step, the Newton correction collapses to `1e-9` to `1e-13` while the finite-difference Jacobian probe remains fixed at `3e-6`;
7. backtracking then stagnates.

Therefore Repair19c3 does not establish physical infeasibility of the `(L,R_t)` ansatz.

It does establish that a single fixed absolute finite-difference scale selected at the parent state is not sufficient to maintain derivative fidelity throughout the nonlinear iteration.

## Project decision boundary

This result is the stopping point for open-ended nonlinear solver repair.

At most one separately preregistered post-first-step derivative-scale diagnostic is licensed before a project-level decision.

In parallel, observational/data-side infrastructure may proceed immediately. The observational pipeline must not claim a tested AeST prediction until a finite-eta prediction is available and the nonlinear-state limitations are stated explicitly.

No additional chain of solver-tuning repairs is licensed by this freeze.
