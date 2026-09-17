# NL1C7B3 predata — standard background sector identification

Status: **PRE-RESULT / FROZEN BEFORE CLASS BACKGROUND EXTRACTION**

Classification before evaluation:

`NL1C7B3_PREDATA_STANDARD_BACKGROUND_SECTOR_IDENTIFICATION`

## Purpose

NL1C7B2 Repair01 established that the frozen AeST scalar energy is internally consistent to machine precision, while the homogeneous spherical action containing AeST plus baryonic pressureless dust leaves a nonzero background remainder at `a_i=0.02`.

This checkpoint identifies that remainder using only standard homogeneous species already present in the frozen CLASS parameterization. No remainder is fitted and no new source is added to the spherical equations here.

## Frozen parent

NL1C7B2 Repair01:

- run `35193003807`
- head `6804934c12b7fa02bbec3c5e1d06ec31466f1c44`
- artifact `10484278813`
- artifact SHA256 `76f24778c432b018724c90cdbb3c6a586dd37698fa9ae4eb644cf8acd0b99059`
- classification `NL1C7B2_REPAIR01_HOMOGENEOUS_BACKGROUND_SECTOR_INCOMPLETE`
- result-freeze commit `a932bd4a3d25b21e2e665ed53d0e09a48febf1b4`
- signed remainder `0.00010529789814922824 Mpc^-2`
- remainder fraction `0.01740837590930068`.

## Frozen cosmological model

Use the exact `v063/theory_response_map.py::class_params()` model and pinned CLASS commit `e85808324f51fc694d12e3ed7439552a3c3f9540`.

The standard non-AeST species already frozen there are:

- photons, from the CLASS default CMB temperature;
- `N_ur=2.046` ultra-relativistic species;
- one non-cold species, `N_ncdm=1`, `m_ncdm=0.06 eV`, `T_ncdm=0.7137658555036082`;
- the standard CLASS cosmological-constant background selected by the frozen model's flatness closure, if present.

Baryons are excluded from the B3 standard-sector sum because they are already represented by the B1 dust action. The CLASS `rho_cdm` slot is excluded because in the frozen AeST bridge it is the effective AeST scalar-dark density already represented by `rhoA`.

## Background extraction

Build the same pinned CLASS/AeST eta=0 stack and obtain `Class.get_background()` from the frozen parameter dictionary. Evaluate all required background columns at exactly `a_i=0.02` (`z_i=49`) using PCHIP in `ln a`; linear interpolation in `ln a` is the frozen control.

No observational data and no nonlinear perturbation output are used.

## Locked gates

### B3-G1 — provenance

The Repair01 parent, pinned CLASS commit, frozen parameter source and relevant AeST source blobs must match exactly.

### B3-G2 — parent reproduction

At `a_i`, the fresh CLASS background must reproduce the retained B2 quantities before the new standard-sector test:

- `H [1/Mpc]` agrees with the Repair01 `H_Mpc_inv` to relative error `<=1e-8`;
- CLASS `rho_b` agrees with `varrho_b/3` to relative error `<=1e-8`;
- CLASS `rho_cdm` agrees with the retained effective `rhoA_trace_CLASS` to relative error `<=1e-8`.

### B3-G3 — standard species are source-declared

The pinned CLASS source must explicitly identify/output the background densities used in the sum. The primary sum is

`rho_std_CLASS = rho_g + rho_ur + sum(rho_ncdm[i]) + rho_lambda`

with absent source-declared species contributing zero. `rho_fld`, `rho_idr`, decaying species or other sectors may not be silently included; if any such additional background sector is present and nonzero, report `INCOMPLETE`.

### B3-G4 — remainder closure

Map CLASS density units to the C6 normalization as

`rho_std_C6 = 3 * rho_std_CLASS`.

PASS requires

`abs(rho_rem - rho_std_C6) / max(3H^2,1e-300) <= 1e-7`.

The B2 remainder is fixed from the parent artifact and must not be refitted.

### B3-G5 — full homogeneous closure

Using only AeST, baryons and the source-declared standard sector,

`epsilon_full = abs(3H^2 - rhoA_C6 - varrho_b - rho_std_C6) / max(3H^2,1e-300)`

must satisfy `<=1e-7`.

### B3-G6 — interpolation control

Replacing PCHIP with linear interpolation in `ln a` must change `epsilon_full` by `<=2e-2`. No nearest-neighbour substitution is allowed.

## Classification

All B3-G1 through B3-G6 pass:

`NL1C7B3_STANDARD_BACKGROUND_SECTOR_IDENTIFIED_PASS`.

The pinned CLASS background contains additional non-negligible source-declared species outside the frozen primary sum, or the primary standard sum does not close the fixed remainder:

`NL1C7B3_STANDARD_BACKGROUND_SECTOR_INCOMPLETE`.

A provenance/source-convention failure is

`NL1C7B3_STANDARD_BACKGROUND_IDENTIFICATION_FAIL`.

## Claim boundary

B3 identifies the missing homogeneous stress-energy sector only. It does not yet license a radial initial constraint or trajectory. A separate checkpoint must decide and certify how the identified standard sector enters the inhomogeneous spherical evolution without fitting or phenomenological forcing.