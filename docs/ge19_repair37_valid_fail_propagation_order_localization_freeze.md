# GE19 Repair37 cancellation-safe FD8 H4/Z21 — valid FAIL propagation-order localization freeze

## Status

The first valid Repair37 science execution is frozen exactly as emitted.

Classification:

`GE19_REPAIR37_CANCELLATION_SAFE_FD8_H4_Z21_RECLOSURE_FAIL`.

Repair37 is not relabelled and must not be rerun as the same science test.

Repair37 successfully closes the cancellation-dominated Lambda audit defect from
Repair36 and replaces the frozen fourth-order GE06/GE07 nonlinear
Euler-Lagrange `Dt @ partial` source derivative by the preregistered
degree-8 exact 9-point operator.

Exactly one preregistered science gate remains false:

`H4_active_shift_Nt128_Linf_le_1e6`.

The remaining failure is localized as a convergent third-order propagation
floor, not evidence for a physical H4 inconsistency.

## Frozen local artifacts

Science JSON:

- SHA-256:
  `da8f2f00c22c866ec3f82381d23f69bf036e630fe2a29c5c44657984b760f61a`;
- bytes:
  `461461`.

Science NPZ:

- SHA-256:
  `572d8937c1d742b10da66e34cc076377c1b2feb20b8f72eb25c3eaf31a59829f`;
- bytes:
  `27183628`.

Inner FULL log:

- SHA-256:
  `da8f2f00c22c866ec3f82381d23f69bf036e630fe2a29c5c44657984b760f61a`;
- bytes:
  `461461`.

Outer runner log:

- SHA-256:
  `e3ca1f3c049b45b320c5cdd7db752fa790ed5969de1f9ef350eed0ca72e64522`;
- bytes:
  `467156`.

Terminal marker:

`GE19_REPAIR37_VALID_SCIENCE_FAIL_FREEZE_REQUIRED`.

## Gates

All Repair37 gates pass except one.

The single false gate is:

`H4_active_shift_Nt128_Linf_le_1e6`.

All of the following pass:

- frozen parent hashes and classifications;
- Repair32C H4 licence;
- exact GE05 -> GE06 factor-two dictionary;
- Repair11 Lambda operator installation and finite stage evaluation;
- direct symbolic GE06/GE07 bilinear identity;
- direct GE06/GE07 swap symmetry;
- cancellation-safe Lambda direct-vs-expanded identity;
- Lambda direct swap symmetry;
- FD8 degree-8 polynomial exactness;
- DY2 spatial control;
- total H4 spatial-source control;
- memory quadrature control;
- Nt64/Nt128 total-source control;
- canonical Radau/algebraic linear residual;
- Nt64/Nt128 H4 state control;
- near-null absolute residual control;
- matched active-shift Linf order;
- matched active-shift RMS order;
- anisotropy;
- all boundary controls;
- finiteness.

## Repair37 source/audit closure

The cancellation-safe Lambda controls are now:

- direct-vs-exact-expanded relative L2:
  `1.9148071003126113e-16`;
- direct swap symmetry relative L2:
  `9.727642209636082e-17`.

The historical subtractive Lambda polarization remains report-only:

`4.9812967098147326e-08`.

The complete Lambda cross source remains numerically negligible:

`||2Q_Lambda_cross||_2 = 4.2444071395688146e-24`.

The FD8 audit reports:

- stencil points:
  `9`;
- polynomial exact degree:
  `8`;
- polynomial test maximum absolute error:
  `1.0658141036401503e-13`.

Therefore the two explicit Repair37 numerical changes were executed as
preregistered.

## Remaining matched-shift failure

Frozen values:

- Nt128 active Linf:
  `1.1749387207106255e-06`;
- Nt64 matched Linf:
  `1.1134127189405345e-05`;
- observed Linf order:
  `3.2077474489146236`;
- Nt128 active RMS:
  `1.0515104304068532e-06`;
- Nt64 matched RMS:
  `8.780910986609813e-06`;
- observed RMS order:
  `3.027380898364344`.

Worst Nt128 active sample:

- C:
  `C_min`;
- beta0:
  `1.0`;
- mode:
  `6`;
- time index:
  `91`;
- ln a:
  `-0.3903758111473973`;
- metric:
  `1.1749387207106255e-06`;
- absolute residual:
  `2.8833875256448104e-16`;
- row scale:
  `2.4540748166856586e-10`.

The worst absolute residual is already at floating-point roundoff scale.

However, the active failure is not a single isolated small-scale sample.
Analysis of the frozen NPZ gives:

- active samples:
  `23850`;
- samples above the frozen `1e-6` gate:
  `16929` (~71.0%);
- fraction of active samples improving Nt64 -> Nt128:
  ~`99.72%`;
- fraction of still-failing Nt128 samples improving Nt64 -> Nt128:
  `100%`;
- median active Nt128 metric:
  approximately `1.088e-6`.

Thus the remaining floor is systematic but strongly convergent.

## Third-order localization

For each active sample the frozen Nt64 metric was PCHIP-matched to the Nt128
grid and a pointwise convergence order was computed using the frozen grid
spacing ratio.

Among Nt128 samples that still fail the `1e-6` gate, the pointwise order is
approximately:

- minimum:
  `2.9504`;
- median:
  `2.9721`;
- 90th percentile:
  `2.9921`;
- maximum:
  `3.0280`.

Across the ordinary active Fourier modes the median per-mode order is
approximately

`2.98055`.

This is a much cleaner third-order signature than Repair36.

The frozen Repair07 propagation path uses:

1. `PchipInterpolator` for the continuous H4 stage source;
2. a two-stage Radau IIA canonical march.

The two-stage Radau IIA method is third order. Therefore an approximately
`O(h^3)` propagated-constraint floor is expected once the lower-order source
assembly defect has been removed.

Repair37 improved the Repair36 Nt128 matched-shift Linf by approximately
33.3% and the RMS by approximately 25.7%, but did not alter the frozen
third-order propagation architecture.

## Diagnostic extrapolation

Using only the observed third-order convergence and no threshold change, a
factor-two reduction of the propagation step predicts

- conservative order-3 Linf:
  approximately `1.47e-7`;
- using the observed global Linf order:
  approximately `1.27e-7`.

Both are well below the frozen `1e-6` target.

This is diagnostic only. It is not a Repair37 PASS claim.

## Interpretation

Repair37 remains a historical valid FAIL.

The result does not support a physical H4 inconsistency.

Instead, Repair37 closes the two numerical issues it was designed to address
and exposes the next numerical limiter: the frozen third-order propagation
path.

The physical H4 equation, parent states, Lambda sector, memory normalization,
Repair18 boundary and observational independence remain unchanged.

## Licensed next step

A separately preregistered follow-up may localize and remove the propagation
floor without changing physics or the science threshold.

The minimal diagnostic should keep the frozen Repair37 source arrays and
parents and vary only the canonical propagation accuracy, for example by
internal Radau substepping on each frozen source interval. This directly
tests if the observed third-order floor is generated by the Radau march.

If substepping removes the defect, a later locked science reclosure may use
the preregistered higher-accuracy propagation path.

If substepping plateaus, the next localization target is the frozen
`PchipInterpolator` stage-source representation.

No Repair37 rerun, threshold relaxation, fitted normalization, finite eta,
primordial Z21, full-species extension or observational tuning is licensed.

## Canonical status

**Repair37 = historical valid FAIL. Lambda audit and FD4 source-assembly
defects are closed. The sole remaining failure is a strongly convergent,
approximately third-order propagated-shift floor. Z21 remains uncertified
pending a separately preregistered propagation-accuracy reclosure.**
