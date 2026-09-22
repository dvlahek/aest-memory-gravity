# GE19 Repair32C first local execution — implementation failure freeze

## Status

The first local Repair32C invocation stopped before producing any valid
Repair32C science JSON.

Runner terminal classification:

`GE19_REPAIR32C_IMPLEMENTATION_OR_EXECUTION_FAILURE`.

Therefore the Repair32C artifact-only certification result is still unconsumed
and the frozen certification contract may receive an implementation-only fix.

## Failure

Exception:

`ModuleNotFoundError: No module named 'ge19'`.

The failure occurred at module import time:

`import ge19.repair07_window_retarded_reduced_h3_z20_particular as r7`.

The Repair32C script defined

`ROOT=Path(__file__).resolve().parents[1]`

but did not insert `ROOT` into `sys.path` before importing the `ge19`
package.

The dedicated GitHub prelock imported the module from repository root, where
the repository root was already present on Python's import path. The local
runner instead executes the script directly as

`python3 ge19/repair32c_artifact_only_reduced_z11_certification.py`

for which Python places the `ge19/` script directory, not the repository
root, at the front of `sys.path`.

Thus the prelock did not exercise the direct-script invocation mode used by
the runner.

## Local log provenance

FULL log supplied by the failed local invocation:

- SHA-256:
  `68c70fe4f70b2fc29ba5232714ec322aeb710cbe5596e65409ea83d0bc0d9e21`;
- bytes:
  `272`.

Runner exit:

`1`.

## Allowed implementation repair

The only permitted Repair32C Repair01 change is:

1. import `sys`;
2. insert the repository root into `sys.path` immediately after computing
   `ROOT`;
3. strengthen the dedicated Repair01 prelock so it executes the script entry
   point far enough to prove direct-script imports work, without running
   certification against science artifacts.

No certification formula, input hash, threshold, operator diagnostic, gate,
source, state or routing change is permitted.

## Scientific status

No Repair32C PASS/FAIL science JSON exists yet.

Reduced Z11 remains NOT CERTIFIED.

H4/Z21 remains BLOCKED.
