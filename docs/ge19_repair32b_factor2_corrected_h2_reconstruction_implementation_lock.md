# GE19 Repair32B canonical factor-two corrected H2 reconstruction — implementation lock

## Status

Canonical Repair32B path:

`GE19_REPAIR32B_PREDATA_FACTOR2_CORRECTED_REDUCED_H2_Z11_RECONSTRUCTION`.

No Repair32B science result exists yet.

## Repair32A parent

Classification:

`GE19_REPAIR32A_GE06_GE05_RAW_RESIDUAL_NORMALIZATION_DICTIONARY_PASS`.

Frozen JSON:

- SHA-256:
  `adef8fad50233c7fa5df3d57e7f21df80ed99228402831b2861ad06256519725`;
- bytes:
  `2121`.

Derived exact dictionary:

`GE05_M1_to_GE06_raw_residual_scale = 2`.

No fitted normalization.

## Canonical preregistration

File:

`ge19/repair32b_predata_factor2_corrected_reduced_h2_z11_reconstruction.json`.

Blob:

`cce721ac498f84ffd084111065056fef86b5c719`.

Commit:

`2bc93cad7aaee8210b4779cd92839946dafa4fbb`.

Static audit:

`35758446046` PASS.

## Canonical implementation

File:

`ge19/repair32b_factor2_corrected_reduced_h2_z11_reconstruction.py`.

Blob:

`6ece578e8a30f48faaded8808687a9bd5c114608`.

Commit:

`189ce1a9381de277bc5d2a2cf0ead324a9f43b77`.

Static audit:

`35758540985` PASS.

## Dedicated canonical prelock

Workflow:

`.github/workflows/ge19-repair32b-reconstruction-prelock-audit.yml`.

Blob:

`25c5332ad654d517d76564cf1b0d8343a4e56c32`.

Commit:

`cb06051bfa3359ff10681fa4eefac4fae17c25e7`.

Run:

`35758781356`.

Conclusion:

`success`.

The prelock verifies that all inherited Repair30 H2 construction helpers remain unchanged except:

- `source_from_B`, which is exactly `2 × Repair30`;
- state-time reporting, which adds Repair31-motivated global diagnostics;
- result/report routing.

## Exact science change

Repair30:

`L_GE06 Z11 = -M1_GE05`.

Repair32B:

`L_GE06 Z11 = -2 M1_GE05`.

Therefore:

- aether RHS:
  `+Q a^3 B10`;
- scalar RHS:
  `-a^2 partial_x(B10)`.

No direct metric M1 source.

No dust M1 source.

No other source change.

## Repair32B validation

Certification gates for the reconstruction:

- parent hashes exact;
- Repair32A factor exactly 2;
- GE05 symbolic M1 identities exact;
- B10 Nt128/Nt64 <= 0.005;
- linear-system residual <= 1e-8;
- inherited dynamic boundary mismatch <= 1e-8;
- full six-field global Nt128/Nt64 <= 0.005;
- dynamic S,u,varphi,T global Nt128/Nt64 <= 0.005;
- chi11 vs Repair29B R2 parent <= 0.005;
- chi11 C-envelope <= 0.005;
- all outputs finite.

Historical Repair30 componentwise shift/anisotropy and max-per-field time metrics are report-only.

## Claim boundary

Repair32B can only validate the corrected H2 reconstruction.

Even on PASS:

- `Z11_certified = false`;
- `H4_Z21_licensed = false`.

A separately preregistered artifact-only Repair32C is required before reduced Z11 certification.

## Superseded duplicate

The later Repair32B `*_reclosure` preregistration, implementation and prelock were removed from the active branch before any science execution.

Their failed prelocks are historical implementation/audit events only and carry no science classification.
