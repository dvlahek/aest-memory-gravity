# GE19 Repair10 reduced-background vacuum on-shell audit result freeze

## Status

Frozen first locked Repair10 local diagnostic execution.

Terminal classification:

`GE19_REPAIR10_REDUCED_BACKGROUND_VACUUM_ONSHELL_AUDIT_COMPLETE`.

Repair10 is diagnostic only and does not alter GE19 H1/H3.

## Frozen local outputs

Science JSON:

- bytes: `5335`;
- SHA-256: `0903363695f071e635f91875903893041bfe728d9ff6c85b424604b933c8baa5`.

Inner FULL log:

- bytes: `5335`;
- SHA-256: `0903363695f071e635f91875903893041bfe728d9ff6c85b424604b933c8baa5`.

Outer runner log:

- bytes: `8284`;
- SHA-256: `e6d65ce9b6154443de312cc839fb544bc705cd31ecc241ad6615603883e21e8a`.

## Main result

The full known non-AeST CLASS background closes the frozen GE06 homogeneous equations:

- density relative L2: `6.573879942279e-7` against limit `5e-5`;
- pressure relative L2: `1.4104702011835305e-4` against limit `5e-3`.

All controls pass.

The current reduced dust-only background is strongly off shell with respect to the frozen CLASS/AeST background:

- density relative L2 across C cases: approximately `0.6657--0.6663`;
- pressure relative L2: `1.0`.

Adding the frozen CLASS cosmological-constant sector reduces these residuals to:

- density: `2.2140572687093913e-4` to `5.055895961766399e-4`;
- pressure: `6.59413790521801e-4`.

The corresponding improvement factors are:

- density: `1317.932121862554` to `3008.2797771949495`;
- pressure: `1516.4984632922062`.

The preregistered reference factor was `10`.

## Frozen routing

`lambda_density_dominant=true`

`lambda_pressure_dominant=true`

`next_route=OMITTED_LAMBDA_DOMINANT_OFFSHELL_MECHANISM`

This is the frozen Repair10 interpretation.

## Exact action normalization

Frozen vacuum action:

`L_lambda = -6 rho_lambda N L R^2`.

Homogeneous contributions:

- lapse: `-6 rho_lambda a^3`;
- longitudinal scale: `-6 rho_lambda a^2`;
- transverse scale: `-12 rho_lambda a^2`;
- shift: `0`.

## Consequence for Repair11

Repair11 is licensed to add only the frozen CLASS vacuum action first-order directional metric coefficients to the reduced H1 operator and repeat Stage A with all Repair07 gates unchanged.

Repair11 must not:

- change GE06 or GE07;
- change the pressureless-dust C values;
- change the canonical/Noether partition;
- change Radau;
- change any threshold;
- construct H3/Z20 before Stage A passes;
- relabel Repair06/07 historical FAIL results.

## Claim boundary

Repair10 is a background/action diagnosis only. It does not itself certify H1, H3/Z20, finite eta, nonlinear physical amplitude, collapse, lensing, or observational detection.
