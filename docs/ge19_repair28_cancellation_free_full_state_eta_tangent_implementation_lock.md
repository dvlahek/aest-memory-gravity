# GE19 Repair28 cancellation-free full-state eta tangent — implementation lock

## Frozen scope

Repair28 certifies the complete first-order eta tangent required as the future H2/Z11 parent.

It does not solve reduced Z11 and does not solve H4/Z21.

The retarded forcing is built only from the already certified Repair26 R1 cancellation-free full-history trace.

## Frozen files

Preregistration:

- file:
  `ge19/repair28_predata_cancellation_free_full_state_eta_tangent.json`;
- blob:
  `690e6a60b2d3a8369edf03ce2782c1c61db404d0`;
- prereg commit:
  `b1b992c98f17e38bb0c4e957c5bdf2b08e63a3eb`.

Implementation:

- file:
  `ge19/repair28_cancellation_free_full_state_eta_tangent.py`;
- blob:
  `b5cb15b46e49c38e1388b6b754d4fa349aa36d5b`;
- implementation commit:
  `45324821f4ef898e218f115033f2dbe3d561d6a3`.

Dedicated prelock:

- workflow:
  `.github/workflows/ge19-repair28-prelock-audit.yml`;
- workflow blob:
  `9f50c54340e735bc145adf36cfb81c895b58421a`;
- workflow commit:
  `f32a1c861d067042821409a707aa2c9cd38b865f`;
- successful run:
  `35723784434`;
- job:
  `106732480492`.

Global GE19 static audits passed for both preregistration and implementation commits.

## Frozen parent

Repair26 R1 cancellation-free full-history trace:

- workflow run:
  `35721220889`;
- artifact:
  `10690709843`;
- SHA-256:
  `608ee0b4c868a701db6976f756b9a551cd9ddffe1e8e4ab37c5cd2361405a6f8`;
- bytes:
  `26643162`.

Repair27 q20 remains certified and unchanged.

## Frozen tangent design

Signed lambda values:

`10, 5, 2.5, 1.25`.

These are numerical tangent amplitudes, not physical negative eta values.

Estimator:

`[state(+lambda)-state(-lambda)]/(2 lambda)`.

Precision pair:

- R1:
  `tol_perturbations_integration=2.5e-8`,
  `perturbations_sampling_stepsize=0.00125`;
- R2:
  `tol_perturbations_integration=1.25e-8`,
  `perturbations_sampling_stepsize=0.000625`.

Common output representation:

- `0.4 <= a <= 0.8333333333333334`;
- 128 nodes uniform in ln(a);
- PCHIP interpolation applied to each signed trajectory before central differencing.

Retarded forcing quadrature:

- primary: 2048;
- control: 1024.

## Frozen gates

No threshold may be changed after execution.

- forcing control relative L2 <= `1e-2`;
- forcing cosine >= `0.9999`;
- requested-k mismatch <= `1e-12`;
- background-grid mismatch <= `1e-12`;
- lambda affinity <= `5e-3`;
- lambda cosine >= `0.9999`;
- even residual <= `5e-3`;
- R1/R2 consensus-state relative L2 <= `5e-3`;
- R1/R2 chi11 relative L2 <= `5e-3`;
- a=0.4 R1/R2 state abs-or-rel <= `5e-3`;
- all outputs finite.

## Stop rule

The first execution that emits a valid Repair28 JSON is the science result and must be frozen as PASS or FAIL.

No reduced Z11 solve is performed here.

No H4/Z21 solve is performed here.
