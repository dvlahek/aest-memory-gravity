# GE19 H3F — valid action-completed Y source-adapter audit

## Classification

`GE19_H3F_COMPLETE_Y_SOURCE_ADAPTER_PASS`.

This is a source-replacement contract and deterministic source
audit **only**. It is not a corrected H3F state solution,
new Z20 certification, new q20 parent, full H4 Noether
certificate or Z21 result.

## Immutable sources and provenance

- preregistration:
  `ge19/h3f_predata_action_completed_y_z20_parent_reclosure.json`;
  blob `6ae1dd8c27ee1f94d85831cd5ae7b5ec21e3794e`;
- versioned H3F adapter:
  `ge19/h3f_corrected_y_source_adapter.py`;
  blob `395294868191111b9b01201315cd2e6a30e47578`;
- deterministic adapter selftest:
  `ge19/h3f_corrected_y_source_adapter_selftest.py`;
  blob `98f40f231fe691c8af91ce4ca20d1da665b606af`;
- parent Stage E source:
  `ge19/h4_stagee_versioned_y_source_rows.py`;
  blob `282166ea5840d7fba4dbc328d40d7687afa6fa0f`.

Dedicated CI:
- run `35997209177`;
- job `107624869369`;
- conclusion `success`;
- terminal marker `GE19_H3F_COMPLETE_Y_SOURCE_ADAPTER_PASS`;
- artifact ID `10806817157`;
- JSON: `results/ge19_h3f_corrected_y_source_adapter.json`;
- SHA-256
  `9f905b09ce4ba688410fe16e917e16724ec3b39cdb8af492a332a224a669bb9d`.

## Exact replacement contract

The source adapter builds the **historical unmodified**
Repair14 H3 source on each actual H1/time/spatial
representation, checks the independent analytic
non-Y identity, and then returns:

`S_H3F = Q_GA + Q_matter + Q_Lambda + S_Y,StageE`.

It removes the full old scalar-only Y contribution,
never adds both Y terms, and keeps both original
non-Y constraint rows unchanged.

Stage E supplies the fixed 2/3-projected common
real-space flux for the new raw action-density Y
aether and scalar rows. Source-mode output preserves
the original GE19 `fft/nx` convention and retained
modes 0..40. The historical Y source is retained
only in a report-only `Y_H3_legacy_report_only`
field.

All three preregistered beta cases passed the
source row, exact production wrapper, non-Y
preservation, zero constraint rows, invalid-input
and new-versus-Stage-E checks.

## Critical boundary and H3F status

The previous Repair18 **projection algorithm** is
retained, but its old numerical p0 is not an admissible
certification target for a source-corrected H3F
solution. The new total source must be used to
recompute and independently verify the projected p0.

The on-shell H1, full H3F source and projected p0
must be tested on Nt128/Nt64, Nx1024/Nx2048 and the
original C/beta/m cohorts. The active shift threshold
remains 1e-6 and matched convergence orders 2.5.

An H3F science PASS has **not** yet been produced.
Historical Repair22/27/32 classifications are
unchanged for their original implemented systems;
Repair37 remains immutable science FAIL;
Repair38--44 remain diagnostics. Z21 is NOT CERTIFIED;
lensing remains blocked.
