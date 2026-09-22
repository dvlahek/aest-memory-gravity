# GE19 Repair32B parallel reclosure prelock failure — implementation-only freeze

## Status

A parallel Repair32B `...reclosure` path was created after the canonical
Repair32B `...reconstruction` path had already been preregistered and
implemented.

The parallel path is **not** a science result and is not licensed for local
execution.

## Failed prelock

Workflow:

`.github/workflows/ge19-repair32b-prelock-audit.yml`

Run:

`35758640313`

Job:

`106850736492`

Conclusion:

`failure`.

Failure occurred at:

`python3 -m py_compile ge19/repair32b_factor2_corrected_reduced_h2_z11_reclosure.py`.

Exact error:

`SyntaxError: unexpected character after line continuation character`.

The source contained literal `\n` text in the constant block. The dedicated
prelock stopped before import, source comparison, or science execution.

The same parallel implementation also had not yet applied the factor-two
change inside `source_from_B()`, so it is not a valid implementation of the
Repair32A dictionary result.

## Canonical Repair32B path

Use only:

- preregistration:
  `ge19/repair32b_predata_factor2_corrected_reduced_h2_z11_reconstruction.json`;
- implementation:
  `ge19/repair32b_factor2_corrected_reduced_h2_z11_reconstruction.py`.

The canonical reconstruction path treats Repair32B as validation of the
factor-two corrected H2 reconstruction only. It does not silently replace
the two Repair30 monitor pathologies and does not certify Z11 or license
H4/Z21.

## Scientific status

No Repair32B science run has occurred.

Repair32A remains PASS.

Reduced Z11 remains NOT CERTIFIED.

H4/Z21 remains BLOCKED.
