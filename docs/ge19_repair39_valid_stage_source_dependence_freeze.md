# GE19 Repair39 valid diagnostic — stage-source representation dependence freeze

## Status

Repair39 completed successfully as a valid diagnostic result.

Classification:

`GE19_REPAIR39_FROZEN_SOURCE_STAGE_INTERPOLATION_LOCALIZATION_COMPLETE`.

Frozen route:

`STAGE_SOURCE_REPRESENTATION_DEPENDENCE_CONFIRMED`.

Repair39 is diagnostic-only. It does not certify Z21 and does not license
lensing. Repair37 and Repair38 remain immutable and are not relabelled.

## Frozen artifacts

JSON:

- bytes: `5429`;
- SHA-256:
  `b058d4acb51dd4e0b964fcccb306b7eb105466941b5e0900ae0c84a29374624e`.

NPZ:

- bytes: `16163836`;
- SHA-256:
  `0bf5b0c2f26cc06b98eab1fb326757ed409cf91c86c23e995251dfd32571c451`.

FULL log:

- bytes: `5429`;
- SHA-256:
  `b058d4acb51dd4e0b964fcccb306b7eb105466941b5e0900ae0c84a29374624e`.

Outer runner log:

- bytes: `9098`;
- SHA-256:
  `d2470549728e2a34256753baa6330267ed1ba5df7d4ff23e8ffbbd1adf786504`.

Terminal marker:

`GE19_REPAIR39_DIAGNOSTIC_COMPLETE`.

## Frozen implementation controls

All implementation gates pass.

PCHIP factor4 reproduces Repair38 substep4:

- Z21 global relative L2:
  `3.7172606261726e-18`;
- active shift metric relative L2:
  `3.882369515821824e-12`.

All interpolation methods reproduce the frozen Nt128 source nodes with maximum
relative L2:

`3.1222622128280023e-16`.

All outputs are finite.

## Frozen method results

PCHIP:

- active Linf:
  `1.3797699672147026e-6`;
- active RMS:
  `1.2040175184158852e-6`.

CubicSpline:

- active Linf:
  `1.4170655920646319e-6`;
- active RMS:
  `1.2081776027435221e-6`;
- active shift-field difference from PCHIP RMS:
  `8.498302841004805e-8`;
- difference divided by the frozen Repair38 Radau factor2-to-factor4 scale:
  `3.4334457790648143`.

Akima:

- active Linf:
  `1.2068124462343292e-6`;
- active RMS:
  `9.931227636322887e-7`;
- active shift-field difference from PCHIP RMS:
  `3.782252303026137e-7`;
- difference divided by the frozen Repair38 Radau factor2-to-factor4 scale:
  `15.280884251999465`.

The Akima response therefore exceeds the preregistered representation-
dependence threshold by a large margin.

## Interpretation

Repair39 establishes that the remaining Repair38 shift floor depends
materially on how the frozen Nt128 H4 source is represented between source
nodes.

This is not evidence that Akima is physically correct or that PCHIP is
incorrect.

The diagnostic only localizes the remaining numerical sensitivity to the
source-at-stage representation.

Because PCHIP and Akima are nonlinear interpolation operators in their nodal
data, the difference between interpolating the already summed total source
and interpolating each H4 source component separately need not be additive.
A follow-up component localization must therefore retain an explicit
interpolation-coupling residual rather than attributing the entire effect to
the six physical source pieces.

## Next licensed step

A separately preregistered piecewise stage-source decomposition using the
frozen Repair37 primary component arrays:

- 2Q_GE06_cross;
- 2Q_GE07_cross;
- 2Q_Lambda_cross;
- 2DY2;
- 2M1_GE05_mapped;
- 2M2_GE05_mapped;

plus an explicit nonlinear interpolation-coupling residual.

The decomposition may identify the leading target for a later direct
fine-grid source reconstruction, but it cannot itself select a physically
preferred interpolant or certify Z21.

## Claim boundary

Z21 remains uncertified.

Lensing remains blocked.

No observational data or finite physical eta enters Repair39.
