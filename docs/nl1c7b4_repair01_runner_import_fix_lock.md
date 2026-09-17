# NL1C7B4 Repair01 runner import fix lock

Status: **TECHNICAL REPAIR LOCKED AFTER RUNNER FAILURE, BEFORE RE-EVALUATION**

Historical failed run: `35211762938` on head `aaca131bba8f8fca986e69994dbabcf6d8b5baf9`.

The run did not produce a scientific B4 Repair01 classification. Provenance verification and retained-input download passed, but execution stopped before the evaluator started with:

`ModuleNotFoundError: No module named 'nl1c7b'`.

The uploaded artifact `10491684790` (SHA256 `12514b8a0ede194c145ee4cd4e1a3bfb92f10d3404e677eb2c1f4f4e9898aaa0`) contains only the technical traceback/log and no valid science JSON.

## Allowed repair

Only the workflow execution environment may change so the repository root is visible to Python package imports. The frozen evaluator blob remains exactly:

`253a0ae2a19a597f06358704ea276c9005973af3`

for `nl1c7b/initial_constraint_certification_repair01.py`.

The runner must execute the same script and arguments with `PYTHONPATH=$PWD` (or an exactly equivalent repository-root import-path setup).

## Frozen science content

The repair must not change:

- the C7A state or retained artifacts;
- the B4 historical parent artifact;
- the exact nonlinear Q definition;
- the Exp K(Q) model or its log-domain treatment;
- any Y branch or beta value;
- the 3-scale / 2-grid / 9-branch test matrix;
- the `1e-7` constraint threshold;
- state reproduction tolerance `1e-12`;
- proof subset, lower-bound construction, or classification logic;
- any action, source, normalization, clipping, projection, or physical parameter.

A subsequent green CI run may still return the preregistered scientific classification `NL1C7B4_REPAIR01_RAW_INITIAL_CONSTRAINT_FAIL`; that outcome is scientifically distinct from this runner failure.
