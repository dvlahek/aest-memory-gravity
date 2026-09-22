# GE19 Repair29A Repair28 even-residual localization — implementation lock

## Scope

Repair29A is an artifact-only diagnostic follow-up to frozen Repair28.

It does not run CLASS, does not regenerate a physical tangent, does not change any Repair28 threshold, and cannot relabel Repair28.

Its only purpose is to localize the frozen Repair28 R1 even-residual failure by field, lambda, k mode and ln(a), then select the only lambda values permitted for a later separately preregistered R3 precision follow-up.

## Frozen files

Preregistration:

- file:
  `ge19/repair29a_predata_repair28_even_residual_localization.json`;
- blob:
  `226ddc9232965368e7d8087a6ea15c19f3ec22bc`;
- commit:
  `a5a65ea93b8290c186a38330ccda23c54cf11d8d`.

Implementation:

- file:
  `ge19/repair29a_repair28_even_residual_localization.py`;
- blob:
  `57ef69a97a6c7dc3a3bf2172799f79f7ce7e7ad7`;
- commit:
  `8546bba08e28f2818e09e4baf762473ae1fde0a5`.

Dedicated prelock workflow:

- file:
  `.github/workflows/ge19-repair29a-prelock-audit.yml`;
- blob:
  `ad19380884f9d199b7921b4d4d48411af9822686`;
- commit:
  `b14d31dddde91236c87ba7bc18788de31e85256e`;
- successful run:
  `35740813854`;
- job:
  `106789772910`.

## Frozen Repair28 parent

- classification:
  `GE19_REPAIR28_CANCELLATION_FREE_FULL_STATE_ETA_TANGENT_FAIL`;
- workflow:
  `35723905248`;
- artifact:
  `10692716361`;
- artifact digest:
  `sha256:0549f84dc1313c7a34c7d6002939bdc34692b195881145489aa89023e9b9c34d`;
- JSON SHA-256:
  `1fd3a4310ea737f6da0d16fa37572c175c26005f6a3ee3f84e5e74f9c82b05a0`;
- NPZ SHA-256:
  `101c38d91344d12071ecb343c35769326f80975e013b7d159f573aae73879705`;
- FULL SHA-256:
  `694fda61ad3f460e79f32ea35ecf6fda0c2a5933f3230b766485518f82af8cc5`.

Repair29A verifies every raw full-state trace against the hashes already frozen inside the Repair28 JSON.

## Frozen metric

For each precision level, primary field and lambda:

[
e = x(+\lambda)+x(-\lambda)-2x(0)
]

and

[
R_{even} =
\frac{\|e\|_2}
{2|\lambda|\,\|\bar x_{,\eta}\|_2},
]

where the tangent consensus is the four-lambda mean of the same Repair28 central-difference tangents.

The historical Repair28 threshold remains

`5e-3`.

It is used only to identify which already-frozen R1 field/lambda pairs exceeded the parent gate.

## Frozen Repair29B selection rule

A later R3 precision follow-up may use only the union of:

1. lambda of the R1 global maximum;
2. lambda of the R2 global maximum;
3. every lambda for which any R1 primary-field global even metric exceeds `5e-3`.

This rule was frozen before Repair29A localization.

## Stop boundary

Repair29A defines no scientific PASS gate.

A successful execution only means:

`GE19_REPAIR29A_REPAIR28_EVEN_RESIDUAL_LOCALIZATION_COMPLETE`.

No reduced Z11 and no H4/Z21 solve is licensed by Repair29A alone.
