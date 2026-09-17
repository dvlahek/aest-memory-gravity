# NL1C7B3 Repair01 predata — direct background-point reconciliation

Status: **PRE-RESULT / FROZEN BEFORE REPAIR EVALUATION**

Classification before evaluation:

`NL1C7B3_REPAIR01_PREDATA_DIRECT_BACKGROUND_POINT`

## Historical parent

The historical B3 result remains unchanged:

- run `35195633648`
- head `43573a7c1eaf9090b0890297edcadde017bdb9bb`
- artifact `10484764897`
- artifact SHA256 `d6b80e99cb456314e130f5e7e65c15b4f608ac9fc8a8395263404045e9fa67e4`
- classification `NL1C7B3_STANDARD_BACKGROUND_IDENTIFICATION_FAIL`
- result-freeze commit `4fb8679f84585c4008008d7043ac0b5f4ca33eeb`.

The physical standard-sector identification from that run is retained:

`rho_std = rho_g + rho_ur + sum(rho_ncdm[i]) + rho_lambda`.

No extra sector is added and the B2 remainder is not fitted.

## Repair rationale

Historical B3 mixed two exported numerical representations at `a_i=0.02`:

- B2 retained values were reconstructed from the dense accepted-source trace;
- B3 values were reconstructed by PCHIP over the exported `get_background()` table.

The resulting representation mismatch was `O(10^-6)` in `H` and effective AeST density, larger than the original `10^-8` parent-reproduction gate and of the same order as the residual closure mismatch.

In addition, the historical implementation classified `rho_tot` as an extra density sector. `rho_tot` is an aggregate total-density diagnostic, not an independent species.

Repair01 changes only the numerical evaluation representation. It does not change the cosmological model, species content, AeST action, dust action, normalization, or closure threshold.

## Frozen model and point

Use exactly:

- pinned CLASS commit `e85808324f51fc694d12e3ed7439552a3c3f9540`;
- the same validated eta=0 AeST patch stack used by B3;
- `v063/theory_response_map.py::class_params()`;
- `a_i=0.02`, hence `z_i=49` exactly.

## Direct exact-point evaluation

Use CLASS methods that call the internal background interpolation at the requested redshift for

- `H(z_i)`;
- `Omega_b(z_i)`;
- effective `Omega_cdm(z_i)` (the frozen AeST dark slot);
- `Omega_ncdm(z_i)`.

Convert component densities by `rho_i_CLASS(z_i)=Omega_i(z_i) H(z_i)^2`.

For source-analytic species use the pinned CLASS background identities at exactly `a_i`:

- `rho_g = Omega0_g H0^2 / a_i^4`;
- `rho_ur = Omega0_ur H0^2 / a_i^4`, with `Omega0_ur` determined by the frozen `N_ur` input relation in CLASS;
- `rho_lambda = Omega0_lambda H0^2`.

The direct ncdm contribution is `Omega_ncdm(z_i) H(z_i)^2`.

The primary standard sum remains

`rho_std_CLASS_direct = rho_g + rho_ur + rho_ncdm + rho_lambda`.

`rho_tot`, `rho_crit`, baryons and the effective `rho_cdm`/AeST slot are not independent standard-sector additions.

## Locked gates

### R1 — provenance

Historical B3 run/artifact/freeze, pinned CLASS commit, parameter source and Repair01 implementation blob must match exactly.

### R2 — direct API/source semantics

The pinned CLASS source/bindings must support direct `background_at_z`-based `Hubble`, `Om_b`, `Om_cdm` and `Om_ncdm` evaluation, and the source identities for photons, ultra-relativistic species and Lambda must be present.

`rho_tot` must be recorded as an aggregate diagnostic and excluded from the species sum.

### R3 — common-point component consistency

At `z_i=49`, all primary terms must be finite and non-negative. The direct baryon density must also agree with the independently frozen physical normalization

`3 rho_b_CLASS = 3 (100/c)^2 omega_b a_i^-3`

to relative error `<=1e-10`.

### R4 — direct homogeneous closure

Define in C6 normalization

- `rhoA_C6_direct = 3 rho_cdm_CLASS_direct`;
- `varrho_b_direct = 3 rho_b_CLASS_direct`;
- `rho_std_C6_direct = 3 rho_std_CLASS_direct`.

Then

`epsilon_direct = abs(3H^2-rhoA_C6_direct-varrho_b_direct-rho_std_C6_direct)/max(3H^2,1e-300)`

must satisfy the unchanged physical closure threshold `<=1e-7`.

### R5 — independent CLASS total diagnostic

If `get_background()` exposes `rho_tot`, it is used only as a consistency diagnostic. The direct primary sum

`rho_b + rho_cdm + rho_std`

must agree with `H(z_i)^2` to `<=1e-7`. No use of `rho_tot` as an added source is allowed.

### R6 — historical representation diagnostic

Report, but do not refit or gate the direct result to, the differences relative to the retained B2/B3 PCHIP values and the fixed historical B2 remainder. The historical B3 FAIL remains valid for its frozen representation.

## Classification

R1-R5 all pass:

`NL1C7B3_REPAIR01_DIRECT_BACKGROUND_POINT_PASS`.

The direct common-point background still fails physical homogeneous closure or source semantics:

`NL1C7B3_REPAIR01_DIRECT_BACKGROUND_POINT_FAIL`.

## Claim boundary

A Repair01 PASS certifies only the homogeneous standard-background composition at the initial epoch in a common numerical representation. It does not yet prescribe how radiation/neutrino/Lambda stress-energy is represented in the inhomogeneous spherical evolution, does not execute radial initial constraints, and does not execute nonlinear evolution.
