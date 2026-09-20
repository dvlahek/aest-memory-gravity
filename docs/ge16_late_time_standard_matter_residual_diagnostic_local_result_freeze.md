# GE16 late-time standard-matter residual diagnostic — local result freeze

## Status

Local execution of the locked GE16 diagnostic over the frozen GE08 Repair01 artifact reproduces all parent diagnostics.

Terminal classification:

`GE16_LATE_TIME_STANDARD_MATTER_RESIDUAL_DIAGNOSTIC_PASS`.

This is diagnostic only and does not yet accept an effective-dust approximation.

## Parent provenance

Frozen parent:

`GE08_REPAIR01_FULL_FIRST_ORDER_STATE_BRIDGE_PASS_MATTER_INCOMPLETE`.

Artifact:

- ID `10598944561`;
- digest
  `sha256:d237aaf4b8f7314992de8dc1a0b432b4fb81eb80fe08352ac3f9d95cfc54982d`.

Frozen parent NPZ SHA-256:

`807833b6692f91f10d4716be1f59baee8f7376d1569fbabec9d76d3e35bbe8fd`.

The diagnostic contains exactly:

- 48 selected rows;
- six k modes;
- eight native redshifts.

## Matched effective-dust residual

Define the matched effective dust to retain the **full standard-sector density and momentum** exactly and omit only standard pressure and scalar shear.

Global perturbative residuals are:

`||delta p_std|| / ||delta rho_std|| = 4.0296809261404915e-7`;

`||shear_std|| / ||delta rho_std|| = 5.717716788656946e-10`.

Worst pointwise values over all 48 frozen samples are:

`max |delta p_std/delta rho_std| = 2.7446222891988022e-6`;

`max |shear_std/delta rho_std| = 4.179059587179661e-9`.

These quantities are outputs, not acceptance thresholds.

## k dependence

For increasing frozen k, the global pressure/density ratios are:

- 0.03 h/Mpc: `2.2629518787119277e-6`;
- 0.05 h/Mpc: `1.064026234251766e-6`;
- 0.08 h/Mpc: `4.789167666683782e-7`;
- 0.10 h/Mpc: `3.1801899217457596e-7`;
- 0.15 h/Mpc: `1.342915183358011e-7`;
- 0.20 h/Mpc: `7.030269523206914e-8`.

The corresponding shear/density ratios are:

- `3.076965506855465e-9`;
- `1.5259570208288047e-9`;
- `7.03294962569688e-10`;
- `4.725100935750045e-10`;
- `2.1015267227905805e-10`;
- `1.0985068117228276e-10`.

Thus the stress residual decreases with k across this signal band.

## redshift dependence

From low to high redshift, the global pressure/density ratio increases smoothly:

- z=0.24762: `2.0002881966440073e-7`;
- z=0.31201: `2.0573174351157664e-7`;
- z=0.45116: `2.2912003589536618e-7`;
- z=0.60419: `2.641392456754786e-7`;
- z=0.77247: `3.074717732043599e-7`;
- z=0.95756: `3.5787279329737154e-7`;
- z=1.16117: `4.1543805090222735e-7`;
- z=1.38524: `4.810141461856898e-7`.

The shear/density ratio remains below `7.67e-10` at every native redshift.

No sharp transition is present in the frozen window.

## Why baryon-only is not the correct reduction

If the full standard sector is replaced by baryons only, the global mismatches are:

- density relative L2:
  `1.3238516018121685e-3`;
- momentum relative L2:
  `2.755072263227075e-3`.

The non-baryon residual therefore carries nonzero standard-sector density and momentum even though its pressure/shear are tiny.

The correct reduced candidate is consequently **not baryon-only dust**.

It is a matched effective dust built from the total standard-sector density and momentum.

Relative to the non-baryon residual density itself:

`||delta p_std||/||delta rho_non-baryon|| = 3.0439068250734597e-4`;

`||shear_std||/||delta rho_non-baryon|| = 4.3190012995642316e-7`.

## Interpretation

Within the frozen perturbative window, the full standard sector is extremely close to a pressureless scalar stress tensor **once its total density and momentum are retained**.

This is substantially more accurate than identifying the standard sector with baryons alone.

However GE16 does not yet establish a complete H3 matter reduction because it has not certified the corresponding standard-sector **background pressure** and background effective-dust mapping.

That background check is required before selecting the reduced model.

## Next licensed step

Perform a lightweight pinned-CLASS background-only audit over `0.2<=z<=1.5` to extract:

- total standard background density after subtracting AeST effective dark and non-clustering vacuum terms;
- total standard background pressure;
- `|p_std/rho_std|`;
- the effective dust background density to be used by the GE07 action.

Then freeze a model-choice error budget using an inherited H3 numerical scale, not a threshold tuned to the GE16 outputs.

## Claim boundary

GE16 does not:

- accept the matched effective dust;
- relabel GE08;
- license Z20;
- introduce finite eta;
- make a nonlinear-collapse or observational claim.
