# GE10 GE09 source-interpolation localization — result freeze

## Status

Frozen first science-reaching GE10 diagnostic execution.

Terminal classification:

`GE10_GE09_SOURCE_INTERPOLATION_LIMIT_CONFIRMED`.

Historical GE09 remains:

`GE09_DENSE_ACCEPTED_STEP_LOCAL_JET_BRIDGE_FAIL`.

GE10 does not relabel it.

## Execution provenance

GitHub Actions run:

`35494855845`.

Execution HEAD:

`6bfe0ae6fd6829294616001bd234097f7099387a`.

Artifact:

- ID: `10599869532`;
- name: `results_bundle_ge10_ge09_source_interpolation_localization`;
- ZIP SHA-256:
  `6c9301e9dc5d1a49a2849f2f36d901acfec4c43744ab38f70ba3eecec3a327b9`.

Frozen parent:

- GE09 run `35494446296`;
- GE09 artifact `10600457104`;
- digest
  `sha256:494639b2074336e704e06cf18b8875bc88d71c62cebfdb687e8e4c3f5270da38`.

## Exact reproduction

GE10 reproduces the frozen GE09 source-grid maximum exactly:

`1.0032254188771416e-4`.

Absolute reproduction error:

`0`.

Frozen dense rows:

`30755`.

Frozen selected source rows:

`48`.

Requested-k relative miss:

`0`.

## Endpoint-density convergence

Using the unchanged cubic-Hermite construction and deterministically retaining
accepted endpoints at strides `{4,2,1}`, the global `delta_dark`
source-grid maximum is

- stride 4: `1.8646993939260902e-2`;
- stride 2: `6.018193732160642e-4`;
- stride 1: `1.0032254188771416e-4`.

The fitted log-log convergence order is

`p=3.7690767281332573`

against the preregistered diagnostic floor `2.5`.

The error decreases strictly with accepted-endpoint density.

## Historical worst row

The frozen worst source row is

- `k=0.1009986958627299 1/Mpc`;
- `k=0.15 h/Mpc`;
- `a=0.6233680777840971`;
- `z=0.604188657774595`;
- `tau=11859.011366097753 Mpc`.

Frozen source value:

`delta_dark=157.19535783072047`.

Cubic-Hermite prediction:

`157.17958759284994`.

Absolute error:

`0.01577023787052667`.

Relative / abs-or-rel error:

`1.0032254188771416e-4`.

The row lies at fractional position

`0.4592776972413067`

inside the accepted-endpoint interval.

Neighboring endpoints:

left:

- `a=0.6131888151210685`;
- `delta_dark=-777.1767521064793`;
- fresh `delta_dark_prime=10.654221135457444`.

right:

- `a=0.6355692474653603`;
- `delta_dark=1380.3681159719883`;
- fresh `delta_dark_prime=13.175478946990145`.

The local ln(a) gap is

`0.03584814336990111`.

The absolute interpolation error normalized by the local endpoint amplitude/swing scale is only

`7.309344108598684e-6`.

Thus the historical gate is maximized near a rapid sign-changing interval where the local source value is small compared with the endpoint excursion.

## Alternative interpolants — descriptive only

At the same historical worst row:

state-only PCHIP gives

- prediction `158.67608559619066`;
- abs-or-rel error `9.331763888091149e-3`.

Linear interpolation gives

- prediction `213.7354865993981`;
- abs-or-rel error `0.26453318383507424`.

The frozen cubic-Hermite representation is therefore retained.

GE10 does not license an interpolation-family change.

## Gate result

Every GE10 diagnostic gate passes:

- exact parent artifact provenance;
- exact parent FAIL classification;
- exact dense/source row counts;
- exact reproduction of the historical maximum;
- same worst field `delta_dark`;
- strict stride convergence;
- fitted order above `2.5`;
- Hermite better than PCHIP and linear at the worst row;
- worst row strictly interior to an accepted-step interval;
- finite outputs.

## Interpretation

The frozen GE09 failure behaves as a convergent accepted-endpoint interpolation-resolution limit.

There is no evidence in GE10 for:

- an incorrect AeST state dictionary;
- a wrong `delta_dark` evolution equation;
- a failure of the dense trace;
- a failure of the official CLASS perturbation output;
- a need to change the Hermite representation.

## Project boundary

GE09 remains FAIL and its `1e-4` gate remains unchanged.

GE10 does not certify the complete GE06 local jet and does not license `Z20`.

A new representation-refinement track may increase accepted-endpoint density under a separately preregistered fixed refinement design.

No iterative tolerance tuning is licensed.
