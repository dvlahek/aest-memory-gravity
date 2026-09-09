# NL1C5BC pre-data: corrected Exp baryon-source freeze

## Purpose

Freeze the baryonic transfer source for the corrected Exp-normalization model on branch `v053-exp-normalization-corrected` before any corrected-model nonlinear full-J reclosure is attempted.

This is a new corrected-model source block. Historical `NL1C5B_BARYON_SOURCE_FREEZE_PASS` remains unchanged and is not reused as a physical source for the corrected model.

## Frozen model

- CLASS commit: `e85808324f51fc694d12e3ed7439552a3c3f9540`.
- Corrected Exp normalization already certified by `NL1C6D2N_EXP_NORMALIZATION_AUDIT_PASS`.
- Same cosmological and AeST parameter values as the corrected no-refit R1 baseline.
- Memory disabled; `eta=0`.
- No observational likelihood, refit, nonlinear branch selection, or memory forcing.

## Extraction configuration

Use the same source-oriented transfer configuration as historical NL1C5B:

- `output = mPk,mTk`;
- `lensing = no`;
- requested `k_h = [0.03,0.05,0.08,0.10,0.15,0.20] h/Mpc`;
- `P_k_max_h/Mpc = 2.0`;
- `z_max_pk = 5.0`;
- `k_per_decade_for_pk = 80`;
- `k_per_decade_for_bao = 560`.

The primary frozen source is CLASS `d_b`. `d_m` and available massive-neutrino transfer fields are retained as context.

## Gates

C1 provenance:

- isolated corrected CLASS tree is pinned to the CLASS commit above;
- final `aest_memory.c` contains the corrected Exp normalization and not the historical factor-2 Exp normalization.

C2 source existence:

- `d_b` and `d_m` exist and are finite on the full returned native grid.

C3 requested modes:

- each requested `k_h` has a native grid point with relative miss <= `1e-12`.

C4 time coverage:

- at least 8 native redshift samples lie in `0.2 <= z <= 1.5`.

C5 deterministic duplicate extraction:

Run the same corrected CLASS source extraction twice with identical parameters in the same environment. Require:

- identical array shapes;
- `k_h` relative mismatch <= `1e-12`;
- `z` absolute mismatch <= `1e-12`;
- relative L2 difference of `d_b` <= `1e-12`;
- relative L2 difference of `d_m` <= `1e-12`.

No gate compares the corrected source to historical v0.77 or historical NL1C5B, because the Exp normalization has intentionally changed the perturbation theory and the grid-aligned impact audit showed order-unity transfer differences.

## Classification

PASS only if all C1-C5 pass:

`NL1C5BC_CORRECTED_BARYON_SOURCE_FREEZE_PASS`

otherwise:

`NL1C5BC_CORRECTED_BARYON_SOURCE_FREEZE_FAIL`

A PASS licenses corrected-model D2A matter-sector validation and corrected source-dependent full-J reclosure tests. It does not license memory/likelihood claims or NL1C7 by itself.
