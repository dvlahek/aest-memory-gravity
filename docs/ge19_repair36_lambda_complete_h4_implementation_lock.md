# GE19 Repair36 Lambda-complete H4/Z21 reclosure — implementation lock

## Status

Repair36 is frozen before its first science execution.

Repair35 remains the historical valid FAIL and is not relabelled.

Repair36 changes only the Lambda-sector implementation omissions localized
from Repair35:

1. installs the exact frozen Repair11 first-directional Lambda operator on
   every Repair13 Nt128/Nt64 reduced background;
2. adds the exact Repair14-derived symmetric mixed Lambda quadratic source
   `-2 B_lambda(Z10,Z11)`.

No other H4 physics, source normalization, boundary rule, propagator, grid,
or numerical threshold is changed.

## Frozen Repair35 FAIL parent

Localization freeze:

`docs/ge19_repair35_h4_z21_valid_fail_lambda_omission_freeze.md`.

Blob:

`578510ab2cf270edc518f0cbbe90c8e0ef50f4cd`.

Commit:

`73dd25c9512256100e5a2e6391cd6d5cea822117`.

Frozen Repair35 science artifacts:

- JSON SHA-256:
  `5b9a785d3dc1005968e91d8e5a36646001d2fea788c9e1c4a0130c4c450d4b93`;
- NPZ SHA-256:
  `c2d00ba5395134752222cef197e05d074824f94599cfcfb0d20d53925273a59a`;
- FULL SHA-256:
  `5b9a785d3dc1005968e91d8e5a36646001d2fea788c9e1c4a0130c4c450d4b93`;
- outer runner SHA-256:
  `00be66cdaa28ebff66de8628650ee9e62ac1d61853c01134c6cad41dfa131ff7`.

## Frozen preregistration

File:

`ge19/repair36_predata_lambda_complete_h4_z21_reclosure.json`.

Blob:

`89ec97f3b3e92d1077c9faf174a308ea73dce339`.

Commit:

`fa5f6766bdc4df5f05147a57de292638a90af998`.

## Frozen implementation

File:

`ge19/repair36_lambda_complete_h4_z21_reclosure.py`.

Blob:

`cf2caafd5ae2399cd3e6f6db7716aece20e8bb6c`.

Final prelock implementation commit:

`6b12114ff89be6b954f2dbcb5c09e0424e666a0c`.

Static audit:

- run `35824180835`;
- conclusion `success`.

## Dedicated Repair36 prelock

Workflow:

`.github/workflows/ge19-repair36-prelock-audit.yml`.

Blob:

`7d268babcf468ba1e150bc8030cb3f6d0df428c4`.

Workflow commit:

`f4b949166deb0830d219913d334964636f3646f0`.

Run:

`35824217854`.

Job:

`107062334933`.

Conclusion:

`success`.

The prelock verifies:

- exact Repair11 Lambda linear coefficients;
- exact zero Lambda shift and anisotropy rows;
- exact symbolic Repair14 Lambda mixed-bilinear polarization identity;
- exact Lambda mixed swap symmetry;
- explicit installation of the Repair11 Lambda operator from
  `bg["rho_lambda_action"]`;
- explicit `2Q_Lambda_cross` source insertion;
- direct Lambda-vs-polarization and symmetry gates at `1e-12`;
- byte-identical Repair35 implementations for the unchanged canonical
  propagator, projected boundary, matched-shift monitor, GE06/GE07 direct
  bilinear cross, DY2, M1/M2, interpolation, time-resolution controls and
  save machinery;
- all frozen numerical constants and thresholds unchanged.

## Frozen Lambda-inclusive H4 equation

`L_total(GE06+GE07+Lambda) Z21 = -2 Q_total(GE06+GE07+Lambda; Z10,Z11) - 2 DY2[Z10;Z11] - 2 M1_GE05[Z20,q20] - 2 M2_GE05[(Z10,q10),(Z10,q10)]`.

## Frozen Lambda operator

From Repair11 and

`L_lambda = -6 rho_lambda N L R^2`:

- lapse/S:
  `-18 rho_lambda a^2`;
- isotropic/N:
  `-18 rho_lambda a^2`;
- isotropic/S:
  `-36 rho_lambda a`;
- shift:
  exactly zero;
- anisotropy:
  exactly zero.

The operator is installed for every reconstructed Repair13 background before
any canonical H4 matrix evaluation.

## Frozen mixed Lambda Q source

From the exact Repair14 second-directional source:

- `B_lambda,N(d,e) = -36 rho_lambda a S_d S_e`;
- `B_lambda,iso(d,e) = -36 rho_lambda a (N_d S_e + N_e S_d) - 36 rho_lambda S_d S_e`;
- all other main rows and both constraint rows are zero.

Repair36 inserts `-2 B_lambda(Z10,Z11)`.

## Stop rule

The first Repair36 execution that emits a valid Repair36 science JSON is
frozen as PASS or FAIL.

An implementation/execution failure before a valid science JSON may be
repaired without changing this contract.

A PASS certifies only the canonical window-local particular reduced Z21
state. It does not certify a primordial homogeneous Z21 mode, a full-species
nonlinear cosmology, finite eta, or an observational signal.
