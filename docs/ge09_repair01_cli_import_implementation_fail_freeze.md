# GE09 Repair01 native CLI — import implementation-fail freeze

## Status

Workflow run `35493087897` passed lock, build and predata audits but failed before the native CLASS CLI process was launched.

Classification:

`GE09_REPAIR01_PRE_SCIENCE_IMPORT_IMPLEMENTATION_FAIL`.

This is not a GE09 local-jet science FAIL. No representation gate was evaluated.

Execution HEAD:

`a593ddba5c3ca25e67d17cbd9698a2a271534ff4`.

Artifact:

- ID: `10600000939`;
- ZIP SHA-256:
  `039bd27030a0914401b0e9fb2f006ada91a1630ec4d8716057378ae203666f88`.

## Failure

The locked Repair01 driver contains the already preregistered native CLI call

`subprocess.run(...)`

and the official perturbation-table parser uses

`re.search/re.findall`.

However the final driver header did not import either Python standard-library module.

Execution stopped at

`NameError: name 'subprocess' is not defined`

before CLASS was launched.

Therefore no:

- dense accepted-step trace;
- accepted source-state trace;
- standard CLASS perturbation table;
- GE09 science JSON;
- GE09 science NPZ

was produced.

## Licensed continuation

A separately preregistered implementation-only repair may add exactly

`import re`

and

`import subprocess`

to the unchanged Repair01 driver.

No other driver line, physics choice, p3 precision value, trace hook, interpolation rule, gate, threshold, classification or claim boundary may change.
