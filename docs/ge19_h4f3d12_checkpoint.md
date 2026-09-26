# GE19 H4F3d12r1 — restored GitHub freeze and next physical route

**GitHub write access restored and confirmed.** The original D12 artifacts
are committed on `physics-first-gravitational-elasticity` with each
source/predata/report/manifest Git blob checked against its
pre-existing local source file. The original D12 report and freeze
manifest retain their historical pre-push statement
`NOT_PERFORMED_GITHUB_WRITE_REJECTED`. This newer record is
the separate, chronological verification of successful GitHub integration;
the original frozen scientific artifacts were not edited.

## Exact committed D12 artifact provenance

| Original frozen file | GitHub path | Exact Git blob |
| --- | --- | --- |
| Original predata (SHA256 `d704bd35c71f80133c7e5b3bb7b71423366f4a692be48fb5797526c2f31db183`) | `ge19/h4f3d12_predata_restricted_background_and_f21_bound.json` | `97b513c176f9de6e1ee55cc21d87cb23103fc707` |
| Historical initial implementation only (SHA256 `61912f04c5504bd173c86e0b143156c756aec7200801d9e468c16edbc7e6edbb`) | `ge19/h4f3d12_restricted_background_and_conditional_f21_bound.py` | `d5f3184f069738679ce7fe738836ef712f60b867` |
| Corrected r1 source (SHA256 `cc637acbe41941247bdf0382dfd1d517790795ba5e7c1562482e0ac0ca757017`) | `ge19/h4f3d12r1_restricted_background_and_conditional_f21_bound.py` | `794df05d6c2c7572a435ba617b0c22649a28b318` |
| Original manifest (SHA256 `e4a6030f85d1bfbe22c095c82ee572497de1c602e37d57c516373cf59be0bfea`) | `ge19/h4f3d12_freeze_manifest.json` | `b7b8a97ea9e27e6f31a85e7724532bb4dfc4fc4b` |
| Original scientific freeze report (SHA256 `ca2365d6134242b2b7ec550e52ed61af806f517a30af381b44faccf633d68046`) | `docs/ge19_h4f3d12_restricted_background_freeze_report.md` | `ec2a6ab2758777d6373623dd2d869a206080e84c` |
| Original physical D11-derived machine JSON, losslessly archived in gzip | `ge19/h4f3d12_actual_d11_conditional_f21_bound.json.gz` | `30cae15e4c2992484d96d3ba0f3f02e8ea8969b1` |

The compressed machine file is a deterministic gzip (mtime=0):
its gzip SHA256 is
`7f011e1f56e1e44708d4515b3593e8ad2f65921ef2cac56bdc0871e867530ef0`;
decompression returns the **byte-identical original 46,751-byte JSON**
with SHA256
`5d94ac19e3176e8e6d2948260b957718eba9620ea9fced2981fe2e6df2c5837e`.
Its eight-field actual D11 Fourier coefficients are `F21`-*conditional*
and the original `F21` field itself remains unavailable.

## Reproducibility and immutable claim boundary

The versioned local runner is
`ge19/run_local_h4f3d12r1_restricted_background_and_f21_bound.sh`;
Git blob `857765404ad013175d69be91c0f3d8428f647228`.
It checks the exact original frozen Git files, original actual
H4F3d10r1/D11 JSON/NPZ input hashes, and compares the user-local
recomputed D12 output **byte for byte** with the decompressed
GitHub archive. It refuses to overwrite any existing D12 result.
The original 23 symbolic gates and 12 cohort/scheme rows are
also verified in the [D12 GitHub static Actions workflow](https://github.com/dvlahek/aest-memory-gravity/actions/workflows/ge19-h4f3d12r1-restricted-background-static.yml).

Independent actual original-parent replay outside CI on the four
original user-uploaded D11 files reproduced the JSON SHA exactly;
no-overwrite and tampered-parent rejection checks passed.
GitHub Actions cannot perform a second **actual** original D11
numeric solve because the private raw D11 NPZ is intentionally
not stored in the GitHub source repository. The archived actual
output and source-bound algebra can still be independently
checked in Actions.

**Scope:** The analytic continuum cancellation applies to
homogeneous GE06/GE07/Lambda on the frozen original Friedmann,
scalar-charge, dust-charge and constant-Lambda background.
The D12 multiplier is conditional on unknown physical `F21`
and does not imply a small all-sector H4 Ward residual.
Only the unweighted full-period spatial zero mode of
homogeneous `E00*dchi F21` vanishes automatically.
Nonzero spatial modes, subwindows and the
`L21*E_L00-b21*E_b00` action boundary remain.

**Next independent physics stage:** evaluate the exact GE05
per-node memory bath first-order Euler
`E_qj10` on the frozen original R1 2048-node trace and
the retained `+4 sum_j E_qj10*dchi q_j10` mixed parent.
The prior H4F3d7r1 FD4/interval-ODE discrepancy is a
diagnostic, not bath-on-shell proof. Any new source/O.D.E.
certification must be registered before physical execution.
After that, evaluate the actual original
`F21` and the full action lower boundary and integrated
all-sector H4 Ward before licensing a window-local reduced
`Z21` or lensing. No observational fitting or new
post hoc science tolerance.

Original D10 FAIL, D10r1 known-source diagnostic PASS,
D11 background-array diagnostic PASS,
Repair37 SCIENCE_FAIL, R1 2048 nodes, original
shift and temporal-order gates all remain unchanged.
