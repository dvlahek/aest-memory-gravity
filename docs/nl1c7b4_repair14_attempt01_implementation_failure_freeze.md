# NL1C7B4 Repair14 — attempt01 implementation-failure freeze

## Status

Frozen local WSL result from the first locked Repair14 execution.

Terminal classification:

`NL1C7B4_REPAIR14_IMPLEMENTATION_FAIL`

Local execution HEAD:

`6ecf01bb221b31cd0bbe916a3a415cebf9ee7ccb`

This is a local WSL result, not an official GitHub Actions run.

## Frozen output hashes

- JSON SHA-256:
  `ea4f1d28330b22d6d3d64f5f6f6d27b3646a889fbee9cffc37c4e789282f0966`
- log SHA-256:
  `fb8cde7d572028177f4b8ccbbe19c899e92bf9d8743ef5246692f1a44e2d8be8`
- local runner log SHA-256:
  `f5b4d6544c5b38371b71e298386f1fe97c30a59f4e50c8374ec2b3e862c7af7b`

## Gate pattern

The exact observed gate pattern was:

- G1 frozen provenance: PASS
- G2 exact Hamiltonian E/X gauge identities: PASS
- G3 exact B3 first variations: PASS
- G4 frozen current bridge semantics: FAIL
- G5 analytic E-sector / K-correction cancellation: PASS
- G6 corrected diagnostic Hamiltonian second order: PASS
- G7 corrected diagnostic momentum second order: PASS
- G8 claim boundary: PASS

No science gate other than the static-interface parser gate failed.

## Science payload retained but not terminally certified by Repair14

All six scale/grid analytic profile pairs satisfy the preregistered cancellation gate.

Worst observed

`||A_Kcorr+A_E||_2 / max(||A_E||_2,||A_Kcorr||_2)`

was

`1.507283138497687e-14`

against the frozen `1e-12` limit.

The diagnostic corrected path contains all 54 cases.

Observed gated Hamiltonian slope range:

`1.975869030883205 .. 2.0453928575447495`

Observed gated momentum slope range:

`2.005505202700859 .. 2.0397779030678223`

All 54 Hamiltonian and all 54 momentum cases therefore satisfy the frozen second-order interval `[1.8,2.2]`.

These results are preserved as output of attempt01 but are not relabeled as a terminal Repair14 science PASS because G4 failed.

## Exact implementation failure

The only failed subcheck was

`CLASS_no_explicit_Echi_delta_rho_line = false`.

The check was implemented as a physical-line scan of the Python source file
`v019/apply_patch_v019.py`.

That source stores the replacement C block as a Python triple-quoted string whose embedded C newlines are represented by literal `\n` escape sequences on a single physical Python source line.

Therefore the selected physical source line containing

`ppw->delta_rho += rho_dark*...`

also contains later text containing `E_aest` and `chi_aest`, even though the actual decoded C `delta_rho` statement itself contains neither variable.

This is a static-parser representation bug. It does not alter the frozen v0.19 bridge semantics, action, state, numerical profiles, or any Repair14 science threshold.

## Licensed repair

A separately preregistered Repair14a may change only the static semantics parser so that it inspects the decoded value of the frozen `new_stress` Python string and then scans the decoded C lines.

The repair may not change:

- Repair14 analytic identities;
- any coefficients or signs;
- the Repair08 state;
- lambda values;
- scale/grid/Y/beta sets;
- radial masks;
- numerical tolerances;
- source evaluator;
- diagnostic `Delta deltaQ`;
- historical B4/Repair12/Repair13/Repair13a classifications.

The historical Repair14 attempt01 `IMPLEMENTATION_FAIL` must remain preserved.
