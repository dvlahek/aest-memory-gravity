# GE19 Repair32B canonicalization lock

## Status

Before any Repair32B science execution, two preregistered/implemented candidate paths existed on the branch:

1. the earlier `*_reconstruction` path;
2. a later `*_reclosure` path.

No Repair32B science result exists for either path.

The earlier `*_reconstruction` path is canonical because it better preserves causal isolation after Repair31:

- the only physics/dictionary change is the exact Repair32A factor two;
- the historical Repair30 local shift and max-per-field state monitors are retained as report-only;
- corrected H2 reconstruction is validated with preregistered global state and chi controls;
- Repair32B does **not** certify Z11 and does **not** license H4/Z21;
- a separately preregistered artifact-only Repair32C must certify the frozen Repair32B state before H4.

The later `*_reclosure` path is superseded before science execution.

## Canonical preregistration

File:

`ge19/repair32b_predata_factor2_corrected_reduced_h2_z11_reconstruction.json`

Blob:

`cce721ac498f84ffd084111065056fef86b5c719`

Preregistration commit:

`2bc93cad7aaee8210b4779cd92839946dafa4fbb`

Static audit:

- run `35758446046`
- conclusion `success`

## Canonical implementation

File:

`ge19/repair32b_factor2_corrected_reduced_h2_z11_reconstruction.py`

Blob:

`6ece578e8a30f48faaded8808687a9bd5c114608`

Implementation commit:

`189ce1a9381de277bc5d2a2cf0ead324a9f43b77`

Static audit:

- run `35758540985`
- conclusion `success`

## Exact single science change

Relative to Repair30:

`GE05_M1_to_GE06_raw_residual_scale: 1 -> 2`

derived by Repair32A.

Therefore:

- aether RHS becomes `+Q a^3 B10`;
- scalar RHS becomes `-a^2 partial_x(B10)`.

No fitted normalization is used.

## Canonical Repair32B validation

Frozen gates:

- parent hashes exact;
- Repair32A dictionary factor exactly 2;
- B10 Nt128/Nt64 relative L2 <= 0.005;
- linear-system relative L2 <= 1e-8;
- inherited dynamic boundary abs-or-rel <= 1e-8;
- full six-field global Nt128/Nt64 relative L2 <= 0.005;
- dynamic S,u,varphi,T global Nt128/Nt64 relative L2 <= 0.005;
- reduced chi11 vs Repair29B R2 parent relative L2 <= 0.005;
- chi11 C-envelope relative L2 <= 0.005;
- all outputs finite.

Historical Repair30 componentwise shift/anisotropy and max-per-field time metrics are report-only in Repair32B.

## Pass consequence

A Repair32B PASS validates the corrected H2 reconstruction but does not certify reduced Z11.

Required next step:

`Repair32C` artifact-only certification of the frozen Repair32B state.

No H2 reintegration in Repair32C.

H4/Z21 remains blocked until Repair32C certification.

## Superseded pre-science duplicate

The later files

- `ge19/repair32b_predata_factor2_corrected_reduced_h2_z11_reclosure.json`;
- `ge19/repair32b_factor2_corrected_reduced_h2_z11_reclosure.py`;
- `.github/workflows/ge19-repair32b-prelock-audit.yml`

are superseded before any Repair32B science run and are not licensed for execution.

Their historical commits/audits remain in repository history.
