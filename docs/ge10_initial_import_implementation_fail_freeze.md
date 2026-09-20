# GE10 initial execution — import implementation-fail freeze

## Status

Workflow run: `35494757012`.

Execution HEAD: `463b1dd7cde75ff271ec9d0ae059840add39d706`.

Classification:

`GE10_PRE_SCIENCE_IMPORT_IMPLEMENTATION_FAIL`.

No GE10 diagnostic classification was produced.

## Passed before failure

- lock audit;
- exact frozen GE09 artifact metadata;
- artifact download and digest verification;
- Python compilation.

## Failure

Direct execution

`python3 ge10/ge09_source_interpolation_localization.py`

sets the script directory `ge10/` on the import path, not the repository root.

The locked script imports

`ge09.repair01_dense_accepted_step_local_jet_bridge`

and therefore raised

`ModuleNotFoundError: No module named 'ge09'`

before reading the frozen parent artifact or evaluating any GE10 diagnostic gate.

## Artifact

Workflow artifact ID: `10600108006`.

Artifact ZIP SHA-256:
`402b7dd6788958b01e8c144c3459dffaa7b5ae221f34a8b725d00ef29ec01478`.

No result JSON exists.

## Licensed repair

One runner-only repair is licensed:

execute the unchanged locked GE10 script with repository root in `PYTHONPATH`, e.g.

`PYTHONPATH="$PWD" python3 ge10/ge09_source_interpolation_localization.py ...`.

No GE10 source, parent artifact, stride ladder, threshold, diagnostic gate or claim boundary may change.
