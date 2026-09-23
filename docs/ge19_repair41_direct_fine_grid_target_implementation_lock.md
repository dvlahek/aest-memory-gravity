# GE19 Repair41 direct fine-grid target reconstruction — implementation lock

## Status

Repair41 is frozen before its first local execution.

Repair41 is diagnostic-only. It cannot relabel Repair37--Repair40, solve or
certify Z21, alter the frozen 1e-6 science target, introduce finite physical
eta, use observational data, or license lensing.

Its sole purpose is to directly reconstruct the two mandatory Repair40 source
targets on finer parent grids and compare them at exact original Nt128
factor-1 Radau stage coordinates.

## Frozen Repair40 parent

Valid freeze:

`docs/ge19_repair40_valid_piecewise_stage_source_decomposition_freeze.md`.

Freeze commit:

`bd9446feccb28779fa3f59bd0206e18d2ebaed4e`.

Freeze blob:

`d2dfd61d765a8fd3c96382bd19b89b7295c841f5`.

Frozen Repair40 artifacts:

- JSON/FULL SHA-256:
  `f5618344db31328dc4e680eb41bb6a715da3fbe7e54ddff3cb53bc027386bf44`;
- NPZ SHA-256:
  `06c7799787abcc510259c626bcb9ca925f96efce13c7949a89690f243fbf01b5`;
- outer runner SHA-256:
  `112bffc28a638bff5a1148795068111475ee4781a923432b6b52cd5a34ec72f4`.

Mandatory targets:

- `2M1_GE05_mapped`;
- `2Q_GE06_cross`.

## Frozen preregistration

File:

`ge19/repair41_predata_direct_fine_grid_target_source_reconstruction.json`.

Commit:

`70caf9cdc460c8b1123677ae4a669ae58445cc90`.

Blob:

`bc07d4130a22906496588f4bc539b19119b21885`.

## Frozen implementation

File:

`ge19/repair41_direct_fine_grid_target_source_reconstruction.py`.

Commit:

`71fd90acb593201294c02f1f435a3652edc0ed0b`.

Blob:

`b04d39d650afaa0a4657d4d96232ea67a35d725d`.

## Direct fine grids

Repair41 uses:

- coarse comparison grid:
  `Nt=128`;
- direct primary fine grid:
  `Nt=382 = 3*(128-1)+1`;
- direct control fine grid:
  `Nt=763 = 6*(128-1)+1`.

For the Repair07 two-stage Radau IIA factor-1 tableau:

- `c1=1/3`;
- `c2=1`.

Therefore every original Nt128 factor-1 stage coordinate is an exact integer
node of both direct fine grids.

The target-source direct values are extracted by integer index lookup only.
No target-source interpolation is used for the direct values.

## Direct parent chain

For each fine grid and each frozen C case:

1. `Z10` is re-solved with the Repair21 on-shell reduced H1 canonical
   equation;
2. `Z20` is re-solved from the Repair14 Lambda-inclusive H3 source with the
   unchanged Repair18 projected zero-coordinate boundary rule;
3. `q10/q20` are reconstructed with the Repair27 cancellation-free
   Repair26 full-history bath parent using the Repair24 normalized GE05 core,
   with:
   - quadrature order 2048;
   - spatial grid Nx=512;
4. `Z11` is re-solved using the Repair32B factor-two corrected H2 equation
   and the immutable Repair28 R2 tangent reference;
5. the two target H4 source pieces are then computed directly:
   - `2M1_GE05_mapped` from the fine-grid
     `B20_linear = X20 - weighted_z20`;
   - `2Q_GE06_cross` from the exact Repair37 GE06 bilinear cross using
     fine-grid `Z10,Z10dot,Z11,Z11dot` and the unchanged FD8 time assembly.

No frozen Repair22, Repair27 or Repair32B parent state is interpolated to
construct the fine-grid target sources.

## Frozen comparators

The only interpolated quantities in the target comparison are the already
frozen Nt128 target nodes, evaluated as:

- PCHIP;
- Akima.

These are comparators only.

The direct fine-grid target reference itself is not interpolated.

## Reproduction gates

Before direct-resolution interpretation:

- the Nt128 `2M1_GE05_mapped` formula adapter must reproduce the frozen
  Repair37 target with relative L2 <= `1e-12`;
- the Nt128 `2Q_GE06_cross` formula adapter must reproduce the frozen
  Repair37 target with relative L2 <= `1e-12`;
- exact fine-stage coordinate mismatch must be <= `1e-13`;
- all outputs must be finite.

## Resolution gates

The inherited parent time-resolution ceiling is `5e-3`.

Repair41 applies that unchanged ceiling to direct Nt382 versus Nt763 stage
comparisons for:

- Z10;
- Z20;
- weighted z20;
- Z11;
- `2M1_GE05_mapped`;
- `2Q_GE06_cross`.

The `5e-3` value is inherited from the certified parent time controls and
is not selected from Repair41 output.

## Routing

If all implementation and resolution gates pass:

`DIRECT_TARGET_REFERENCE_RESOLVED`.

If implementation gates pass but at least one direct-resolution gate fails:

`DIRECT_TARGET_REFERENCE_UNRESOLVED`.

If frozen binding, formula reproduction, exact stage-node mapping or
finiteness fails:

`IMPLEMENTATION_FAIL`.

Repair41 itself cannot perform an H4/Z21 reclosure.

## Audits

Static implementation audit:

- run:
  `35908724842`;
- conclusion:
  `success`.

Dedicated Repair41 prelock:

- workflow commit:
  `faf3fd436265325cfc50e7f3e9e3fd2f2f85d9c3`;
- workflow blob:
  `f1ab26164b565677f757edab9d02f078ece27743`;
- run:
  `35908804106`;
- job:
  `107343128775`;
- conclusion:
  `success`.

## Claim boundary

Repair41 reconstructs only the two mandatory source targets.

It does not solve H4/Z21, certify Z21, select a primordial homogeneous mode,
change a science threshold, introduce finite eta, use observational data or
license lensing.
