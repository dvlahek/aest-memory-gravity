# NL1C6R3C pre-data: corrected-source R3 blocking snapshot

## Purpose

Before spending compute on a full corrected-source NL1C6R3 reclosure, re-evaluate the historically blocking constitutive case using the newly certified corrected baryonic source.

This is not a new solver repair. The historical NL1C6R3 solver, equations, tolerances, continuation rules, endpoint validity test, and both co-primary constitutive routes remain unchanged.

## Prerequisites

- `NL1C5BC_CORRECTED_BARYON_SOURCE_FREEZE_PASS`.
- `NL1C6D2AC_CORRECTED_BARYON_MATTER_SECTOR_AUDIT_PASS`.
- Corrected source is regenerated in the same workflow from the corrected isolated CLASS model.
- No historical baryon-source NPZ may be substituted.

## Frozen test

Use `nl1c6r3.fixed_source_constitutive_homotopy` unchanged.

Select:

- interpolation: `sharp`;
- `beta0 = 1.0`;
- highest-redshift native snapshot in the corrected frozen source;
- the same six requested Fourier modes and primary spatial resolution used by NL1C6R3;
- both preregistered anchor routes: `screened` and `mass`.

For each route, call the existing `anchor_route_solve` and then the existing `endpoint_valid` test if the route reports success. Do not alter GMRES tolerances, Newton tolerances, arclength settings, step-size rules, maximum accepted points, or endpoint criteria.

## Decision rule

`NL1C6R3C_CORRECTED_BLOCKING_SNAPSHOT_NONBLOCKING`

if at least one of the two routes reaches a residual-valid physical `theta=1` endpoint.

`NL1C6R3C_CORRECTED_BLOCKING_SNAPSHOT_BLOCKING`

if neither route reaches a residual-valid physical `theta=1` endpoint.

A BLOCKING result stops the corrected full R3 run and is interpreted as a numerical/static reclosure blocker under the existing frozen solver, not proof that the physical full-J AeST equations have no solution. No R4/R5 tolerance or continuation repair is authorized.

A NONBLOCKING result licenses a full corrected-source R3 run with the existing NL1C6R3 algorithm and preregistered co-primary route logic.

## Scope

No memory forcing, finite eta, observational likelihood, cosmological refit, nonlinear FLRW branch evolution, or NL1C7 is performed here. Historical R3 results remain unchanged.
