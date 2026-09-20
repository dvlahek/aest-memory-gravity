# GE09 Repair01 first attempt — predata-runner failure freeze

## Status

Workflow run `35492994926` did not execute the GE09 Repair01 science driver.

Classification:

`GE09_REPAIR01_PREDATA_RUNNER_FAIL`.

This is not a GE09 science FAIL.

Execution HEAD:

`25899d4afea97da9b696242524809d6fed2bb521`.

Artifact:

- ID `10599318068`;
- ZIP SHA-256
  `b65b8a63cf22acbd00283ed922c3953b3a2b30672823181632eb03df207a7f12`.

## Failure

The predata audit contained

`assert 'get_perturbations' not in src`.

The Repair01 driver no longer imports or calls classy, but the inherited
`class_trace_control()` error text still contained the phrase

`dense trace tau not found in CLASS get_perturbations`.

Therefore the runner aborted before the science step solely because the string
audit was broader than the execution-surface requirement.

## Licensed runner repair

Replace only the broad assertion with a direct implementation assertion that

`from classy import Class`

is absent from the Repair01 driver.

No driver blob, physical model, p3 precision value, trace hook, interpolation,
science threshold or classification rule may change.
