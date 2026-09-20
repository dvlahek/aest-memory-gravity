# GE07 Repair01 — predata runner log-directory repair

## Status

Predata runner-only repair preregistration.

Parent run:

`35490505767`.

The locked GE07 science process completed and wrote

`GE07_PRESSURELESS_MATTER_DIRECTIONAL_SOURCE_GENERATOR_PASS`

with all science gates true.

The workflow nevertheless failed because `tee` attempted to open

`results/ge07_pressureless_matter_directional_source_generator.log`

before the `results/` directory existed.

Frozen parent artifact:

- ID `10599076721`;
- ZIP SHA-256 `006673bc76cd3d48a207728275dbb2087a113c9702355586d68e4098c618c249`;
- science JSON SHA-256 `3bcf6d295e5c5d5d1d0422e9b7ff588ec93fe96458d287f520ea8e47bdedb1d6`.

## Licensed change

Exactly one runner change is allowed:

`mkdir -p results`

before the locked Python+tee pipeline.

No science implementation, action, threshold, source list, grid or finite-difference step may change.

The repaired run must reproduce the same GE07 PASS classification and science payload within deterministic JSON equality apart from workflow provenance external to the JSON.

