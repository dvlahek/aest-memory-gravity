# Full-J corrected-CLASS spectral-fringe / GR-control preregistration

Date: 2026-09-13

## Motivation

The locked source-decomposition result `FULLJ_SPECTRAL_FRINGE_SOURCE_DECOMPOSITION_CORRECTED_CLASS_LINEAR_SECTOR_DOMINATED` shows that the late-time node/lobe curvature of the tagged Weyl response is dominated by the corrected CLASS linear sector. The shape correlation at `z=0.2` is `0.9999999998448602`, while the internal reconstructed correction contributes about `0.1125` of the total second-difference norm.

The next question is therefore no longer whether the nonlinear residual creates the sharp structure. The decisive question is whether the structure is a genuine, k-list-independent feature of the corrected AeST linear perturbation solution and whether it is absent or strongly suppressed in an otherwise matched GR/LambdaCDM control.

This audit is frozen before any GR-control or fine-grid result is inspected.

## Locked ancestry

Required ancestors:

- physical-k projection repair PASS: `20151ab785e923de20d720f3fdd8890576b6cc05`
- source-localization saturated-mode support: `86ab13ffa1048860731f65348074ede1b469c644`
- spectral-fringe geometry certification: `73fb42d64e61d69820d31a9c9f71c8d536b2376e`
- source-decomposition result: `0e4a3be830e2c6a5e87a7cb259a09bcb459f9d5f`

The corrected CLASS source/tree and cosmological parameters remain those of the already validated corrected baseline. No memory forcing is enabled: `aest_memory_enabled=no`, `aest_eta=0`.

## Direct-k design

No real-space tagged field, FFT projection, nonlinear evolution, radial interpolation, or power interpolation is used in this audit. The observable is the direct linear Weyl transfer

`W_CLASS(k,z) = phi(k,z) + psi(k,z)`

read from requested CLASS scalar histories.

Three windows are frozen, centered on the already observed structures:

- W1 center `k/h = 0.10125`
- W2 center `k/h = 0.16375`
- W3 center `k/h = 0.19625`

Each window contains 17 points with spacing

`Delta k/h = 0.000625`

and half-width `0.005`. The complete dense list therefore contains 51 requested k values and stays below the locally validated CLASS 64-history limit.

The already certified 15 common-geometry nodes are a strict subset of this 51-point list:

`[0.09875,0.10000,0.10125,0.10250,0.10375, 0.16125,0.16250,0.16375,0.16500,0.16625, 0.19375,0.19500,0.19625,0.19750,0.19875]`.

## Three CLASS calculations

1. **AeST dense**: corrected AeST, 51 requested k values.
2. **AeST sparse-anchor**: corrected AeST, only the 15 locked anchors.
3. **GR dense**: same baseline cosmological parameters and corrected CLASS executable, but `aest_enabled=no`, with the same 51 requested k values.

The GR run is a control for generic LambdaCDM transfer-function structure. It is not a cosmological refit.

Check redshifts remain

`z = [6,5,4,3,2,1.5,1,0.5,0.2]`.

## Frozen diagnostics

### DG-G1 — provenance and exact setup

All ancestry locks, corrected CLASS provenance, exact 51-point dense grid, exact 15-anchor subset, and memory-off settings must be confirmed.

### DG-G2 — direct AeST anchor reproduction

The 15 direct sparse-anchor AeST Weyl transfers must reproduce the locked `W_CLASS` component from the source-decomposition NPZ with

- global relative L2 <= `2e-5`
- per-anchor relative L2 max <= `5e-5`.

This threshold allows only interpolation/readout-level differences and is far below the observed node/lobe amplitudes.

### DG-G3 — requested-k-list invariance

At the same 15 physical anchor k values, the AeST dense-51 and sparse-15 runs must agree with

- global relative L2 <= `1e-6`
- per-anchor relative L2 max <= `5e-6`.

Failure means the spectral structure is not licensed as physical and the classification is numerical-control failure.

### DG-G4 — dense-grid health

All AeST and GR values must be finite over every frozen k and z. Each requested history must cover the complete `z=6..0.2` interval.

### DG-G5 — fine-grid spectral structure

For each 17-point window and each redshift define

`D2 W_i = W_{i+1} - 2 W_i + W_{i-1}`

and

`kappa = ||D2 W||_2 / max(||W||_2, 1e-300)`.

At `z=0.2`, corrected AeST must have at least two strict local extrema in each of the three 17-point windows. This gate tests that the previously observed node/lobe structure resolves into a coherent fine-grid function instead of disappearing when sampled between the old points.

### DG-G6 — AeST specificity against GR

At `z=0.2`, define the aggregate fine-grid curvature across the three windows by concatenating the windowwise second differences. The specificity ratio is

`R_spec = kappa_AeST / max(kappa_GR, 1e-300)`.

The predeclared strong-specificity threshold is

`R_spec >= 10`.

Additionally, `kappa_AeST >= 0.05` is required so a large ratio cannot be produced only by a numerically tiny GR denominator.

## Classification

If DG-G1 through DG-G6 all pass:

`FULLJ_CORRECTED_CLASS_SPECTRAL_FRINGE_AEST_SPECIFIC_SUPPORTED`

If DG-G1 through DG-G5 pass but DG-G6 fails:

`FULLJ_CORRECTED_CLASS_SPECTRAL_FRINGE_GENERIC_OR_NOT_SPECIFIC`

If DG-G2, DG-G3, or DG-G4 fails:

`FULLJ_CORRECTED_CLASS_SPECTRAL_FRINGE_NUMERICAL_CONTROL_FAIL`

Otherwise:

`FULLJ_CORRECTED_CLASS_SPECTRAL_FRINGE_INCOMPLETE`

## Scope

A PASS would establish only that the already observed fine spectral structure is a direct, k-list-invariant feature of the corrected AeST linear CLASS sector and is strongly suppressed in the matched GR control. It would not yet establish a new fundamental mode, a resonance, an observational detection, a continuous 3D nonlinear Weyl power spectrum, LOS lensing, or ACT likelihood use.

If AeST specificity is supported, the next milestone is an equation-level linear-mode/dispersion audit plus a held-out node prediction. No further blind radial interpolation campaign is authorized by this preregistration.