# NL1C6R3C corrected-source blocking snapshot result

## Classification

`NL1C6R3C_CORRECTED_BLOCKING_SNAPSHOT_BLOCKING`

GitHub Actions run: `34436720053`.
Run head: `3dad9b980d372db70f40b2bad073e375f3c22b77`.
Branch: `v053-exp-normalization-corrected`.

## Snapshot

- highest corrected native redshift: `z = 6.000000000000059`;
- `a = 0.1428571428571417`;
- interpolation: `sharp`;
- `beta0 = 1.0`;
- historical NL1C6R3 production solver reused unchanged;
- corrected NL1C5BC baryonic source regenerated in the same workflow.

## Route results

### Screened route

- success: false;
- reason: `theta1_gmres_failed_300`;
- residual-valid physical endpoint: false;
- final solver relative residual: `0.05797022809903863`;
- accepted points: 16;
- rejected points: 0;
- folds: 0;
- `theta_max = 1.011354092062178`.

### Mass route

- success: false;
- reason: `arclength_max_accepted_points`;
- residual-valid physical endpoint: false;
- final solver relative residual: `1.3162538328492669e-11` at the nonphysical continuation location;
- accepted points: 1200;
- rejected points: 0;
- folds: 0;
- `theta_max = 0.0049344685556935546`.

## Decision

Neither co-primary route reaches a residual-valid physical `theta=1` endpoint. Therefore the preregistered blocking condition is met and a full corrected-source R3 run is not licensed.

No solver repair, tolerance change, continuation retuning, memory forcing, likelihood, refit, or branch selection is authorized by this result.

This is a numerical/static reclosure blocker under the frozen R3 algorithm. It is not evidence that the physical full-J AeST equations have no solution. The corrected baryonic source did not remove the historical obstruction, so the next scientific step is not another R3 numerical repair but the already motivated covariant nonlinear FLRW completion/derivation on the corrected normalization.
