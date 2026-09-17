# NL1C7B4 Repair03 pre-data — constraint source localization

Status: **PRE-DATA / LOCKED BEFORE REPAIR03 EVALUATION**

Pre-result classification: `NL1C7B4_REPAIR03_PREDATA_CONSTRAINT_SOURCE_LOCALIZATION`.

## Motivation

Repair02 exactly completed the nonlinear Q dictionary and restored a finite Exp K(Q) sector, but the unchanged raw constraints still failed all 54 frozen cases. The remaining failure is strongly dominated by the radial momentum gate, while the Hamiltonian residual is much smaller. Repair03 is diagnostic only. It must identify the source and perturbative order of the residual before any new state completion, radial source, or constraint projection is considered.

## Frozen parent

Repair02 official run: `35216284867`.

Repair02 head: `2791ba272e8a587bfe2ead747b54596631527627`.

Repair02 artifact: `10495377062`.

Repair02 artifact SHA256: `f74795d3c57ba6f307655b1ec15513b57babc7eadbe0c81c4f62bf1949643d49`.

Repair02 result freeze commit: `9c1f5c6a17467467bcf82e134f21793a3f63d0d4`.

All C7A, B1, B3, B4 and Repair02 physical constants, fields, scales, Y branches, beta0 values, radial grids, finite-difference operator, action-term normalization and the `1e-7` historical constraint threshold remain unchanged.

## Frozen state

Use exactly the Repair02 state. In particular,

`Q_target = Q_bg + deltaQ_C7A`

and

`phidot_completed = [Q_target - sinh(u) phi_r/L] / cosh(u)`.

No field may be solved from a constraint in Repair03.

The dust rapidity convention remains the B1/C7A convention already frozen in B4:

`v = atanh(dust_vr)`.

Repair03 must not test the opposite sign as an alternative model choice.

## R3-D1 — term-by-term constraint decomposition

For every `3 scales x 9 Y branches x 2 radial grids`, evaluate the same Hamiltonian and radial-momentum Euler-Lagrange contributions used by Repair02, retaining separate arrays for at least:

- GR,
- AeST non-K/non-J sector,
- AeST J(Y),
- AeST K(Q),
- pressureless dust,
- homogeneous standard background.

For each term and each constraint report:

- maximum absolute contribution over `r>0`,
- relative L2 magnitude with respect to the sum of absolute term L2 magnitudes,
- signed inner-product projection onto the total residual,
- value and fractional absolute contribution at the radius of the maximum normalized total residual.

The decomposition must sum back to the Repair02 total constraint to relative L2 error `<=1e-12`.

## R3-D2 — radial localization

For each case report the radius of maximum normalized Hamiltonian residual and maximum normalized momentum residual, both in Mpc and in `x=r/(R_sigma/h)`. No radial interval may be removed after inspection.

## R3-D3 — frozen amplitude-scaling diagnostic

Use co-primary perturbation multipliers

`lambda = {1, 1/2, 1/4}`.

For each lambda, multiply **all C7A perturbations together** before exact Repair02 completion:

- `L-a`, `R-ar`, `Ldot-aH`, `Rdot-aHr`,
- `u`, `udot`, `phi`, `deltaQ`,
- `delta_b`, `dust_vr`.

Background quantities remain fixed. Recompute the exact nonlinear `phidot_completed` from the scaled target and scaled fields. No individual field may be rescaled separately.

Evaluate the same constraints for all scales, both grids and all nine Y branches.

For each case report `max epsilon_H`, `max epsilon_M`, `RMS epsilon_H`, and `RMS epsilon_M` for all three lambda values, plus log2 slopes between adjacent amplitudes when finite.

Interpretation is diagnostic and is frozen before data:

- a normalized residual that decreases approximately proportional to lambda is consistent with a residual entering one perturbative order above the leading cancelling terms;
- a normalized residual that remains approximately constant as lambda decreases indicates a leading-order/interface or missing-source mismatch;
- stronger or irregular scaling is reported without reclassification or threshold adjustment.

No slope is used to select a Y branch, scale, grid, or repair.

## R3-D4 — standard-sector boundary

The homogeneous standard background remains exactly the B3-certified lapse contribution with zero radial momentum because no radial photon/UR/ncdm/Lambda transfer profiles are present in the frozen C7A artifact.

Repair03 must not invent such profiles. If the source decomposition and amplitude scaling are compatible with a missing leading-order radial source, the result may identify `STANDARD_SECTOR_RADIAL_SOURCE_CANDIDATE`, but this label is only a localization result. A separate preregistered CLASS transfer extraction would be required before adding that sector.

## Forbidden operations

Repair03 must not:

- modify or project any state field beyond the co-primary global amplitude diagnostic described above,
- reverse the dust velocity sign as a post-result alternative,
- add radial standard-species perturbations,
- fit any source term,
- change any physical coefficient or constraint threshold,
- clip or linearize Q, K(Q), or J(Y),
- drop any scale, Y branch, beta0, grid, or radial region except the already frozen analytic center point.

## Classification

If decomposition closure is `<=1e-12`, all diagnostic cases are finite, and all frozen cases/amplitudes are retained:

`NL1C7B4_REPAIR03_CONSTRAINT_SOURCE_LOCALIZATION_COMPLETE`.

If the diagnostic cannot reproduce the Repair02 totals or requires a new physical prescription:

`NL1C7B4_REPAIR03_LOCALIZATION_IMPLEMENTATION_FAIL`.

Repair03 cannot by itself license nonlinear evolution. Its only purpose is to determine the next preregistered closure repair from frozen evidence.
