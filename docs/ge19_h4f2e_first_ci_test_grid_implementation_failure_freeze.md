# GE19 H4F2e — first CI deterministic-grid implementation failure (immutable)

## Outcome

First H4F2e attempt: `GE19_H4F2E_FIRST_CI_DETERMINISTIC_GRID_IMPLEMENTATION_FAIL`.

- Workflow `.github/workflows/ge19-h4f2e-shift-action.yml`, blob
  `5f0f8281ca7258330a2e0cd138e8fd34082eb44e`.
- Run `36027249827`, job `107726804297`, conclusion `failure`.
- First implementation `ge19/h4f2e_dust_m2_lambda_shift_action_audit.py`,
  blob `0c6aa6539b8a1a2d18b9ba09e87e5fe578c691e5`.
- Preregistration `ge19/h4f2e_predata_dust_m2_lambda_shift_action.json`,
  blob `a48ea8b15bf1c1141d9407c7400f416171f4b22b`.
- Failed run artifact ID `10819826655` contains the FULL log.
  No complete H4F2e result JSON was produced.

Traceback: `finite_fourier` failed at construction of
`phase=(jj+1)*xx+0.17*tt+0.2*jj` because test node/space
shape `(3,1,256)` could not broadcast with time
shape `(5,1,1)`.
The time dimension had been placed on axis 0 rather
than the preregistered node/time/space axis 1.
The error occurred before deterministic Fourier
and final source/physics gates were evaluated.

This is an **implementation/test-grid failure**,
not evidence for or against the GE07, GE05 M2 or
Lambda shift action identity, and not a new H4 science FAIL.

## Narrow repair

Change **only** the deterministic test time
index from `np.arange(nt)[:,None,None]` to
`np.arange(nt)[None,:,None]` so the intended
node/time/space grid is `(3,5,256)`.
Keep preregistration, all source physics,
frozen SHA controls, action/polarization
formulae, factors, source signs, Fourier
normalization, science targets and gate
definitions unchanged.

Subsequent valid results require a new
implementation blob and a new dedicated
workflow run; this first failed attempt
must remain visible in provenance.
No corrected-parent common-grid evaluation,
H4/Z21 solve or lensing result is licensed.
