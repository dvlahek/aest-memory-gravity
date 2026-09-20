# GE09 Repair01a native CLI — output-root implementation-fail freeze

## Status

Workflow run:

`35494179971`.

Execution HEAD:

`cdda2fe9f455889d288aa06120e146b85840f869`.

The run passed:

- Repair01a lock audit;
- pinned CLASS checkout;
- validated AeST diagnostic patch chain;
- CLASS executable build;
- predata implementation audit;
- native CLASS CLI launch.

It then terminated before any GE09 science gate was evaluated.

Classification:

`GE09_REPAIR01A_PRE_SCIENCE_OUTPUT_ROOT_IMPLEMENTATION_FAIL`.

This is not a GE09 local-jet science FAIL.

## Artifact

Artifact ID:

`10600296908`.

Artifact ZIP SHA-256:

`fc14881ffb1b6a511f5b4b8f2d752ed507fc9dd7c1a9984e53dafe3f2152138b`.

Key files:

- dense accepted-step trace SHA-256:
  `96cac787a7d5d7b70b7a7b95ba04de28c2cbaa50c94f6818526a0ed96f28eb38`;
- accepted source-state trace SHA-256:
  `3ee90a0cf6a281214b35f0eafe30efdd99bb540b80793eccf3dfa7c76f41c01a`;
- native CLASS log SHA-256:
  `3b4b61c832e69af76f5c45070dec8f2401527cd6f99f4f535768ea5c0517b164`;
- GE09 science log is empty because the Python driver raised before science evaluation.

No GE09 science JSON or NPZ was produced.

## Failure

The Repair01a driver requested native CLASS perturbation output through

`k_output_values`

and set

`root = .../results/ge09_cli_`.

Pinned CLASS correctly interprets `k_output_values` as enabling stored/written perturbation tables.

However pinned `input_set_root()` canonicalizes an explicitly supplied root by appending one underscore:

`class_sprintf(pfc->value[index_root],"%s_",outfname)`.

Therefore the supplied root ending in `_` becomes

`.../results/ge09_cli__`

and the actual perturbation filenames are expected under the double-underscore prefix

`ge09_cli__perturbations_k*_s.dat`.

The locked driver instead searched for

`ge09_cli_perturbations_k*_s.dat`

and raised

`FileNotFoundError`

before reading any CLASS perturbation table or evaluating any GE09 science gate.

## Diagnosis boundary

This failure is not evidence for:

- a dense accepted-step trace failure;
- a local-jet interpolation failure;
- a source-grid state failure;
- a physical-RHS failure;
- a GE06 dictionary failure;
- a matter-closure result.

The dense and accepted source-state traces were produced successfully.

## Licensed continuation

A separately preregistered implementation-only repair may change exactly the native CLI root prefix from

`.../results/ge09_cli_`

to

`.../results/ge09_cli`.

The driver may continue to expect the canonical CLASS output names

`.../results/ge09_cli_perturbations_k*_s.dat`.

No other driver line, physical parameter, precision setting, trace hook, interpolation rule, gate, threshold or claim boundary may change.
