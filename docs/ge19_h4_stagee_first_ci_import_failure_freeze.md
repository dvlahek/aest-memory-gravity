# GE19 Stage E — first CI preexecution import failure (immutable)

## Classification

`GE19_H4_STAGEE_FIRST_CI_PREEXECUTION_IMPORT_FAIL`.

First attempt:
- GitHub Actions run `35995106055`;
- job `107618051732`;
- execution commit `8a405b6c16776016e735eb544214e8b59715f2f7`;
- CI conclusion `failure`.

The pinned Stage E preregistration, source implementation and
selftest compiled, but the CI launched the selftest by its path:

`python3 ge19/h4_stagee_versioned_y_source_selftest.py`.

Because Python used `ge19/` as sys.path[0], the import

`import ge19.h4_stagee_versioned_y_source_rows as ys`

raised

`ModuleNotFoundError: No module named 'ge19'`.

No Stage E source test executed. There is no source-result JSON and no
scientific/numerical outcome to interpret. The failure is not a
test of Y rows or a new science FAIL.

Frozen source bindings:
- preregistration blob:
  `e5ff7d12e963fa7487a1dff42ce06053f4b8d82e`;
- standalone source blob:
  `282166ea5840d7fba4dbc328d40d7687afa6fa0f`;
- selftest blob:
  `05bbbb5d2dba2193adcbf468efc81eda6fb71ce6`.

## Repair rule

Retain this first attempt and change ONLY the CI invocation to

`python3 -m ge19.h4_stagee_versioned_y_source_selftest`

from the repository root. This makes the repository's namespace
package discoverable, without editing preregistration, source
physics, source arrays or selftest gates.

If subsequent tests fail, preserve their full gate values and
version fixes separately. Do not relabel earlier Repair37--44
or Stage D results.

Z21 remains NOT CERTIFIED and lensing remains blocked.
