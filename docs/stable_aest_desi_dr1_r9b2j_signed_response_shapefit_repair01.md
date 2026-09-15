# Stable AeST DESI DR1 R9b2j signed-response ShapeFit Repair01

## Status of the interrupted invocation

The first R9b2j local invocation did not produce a scientific or numerical classification. The shell returned exit code 143 (`SIGTERM`) during the first requested model, `tau_H0=10, eta=0`, before any Stage-A gate, result JSON, or DESI projection was produced.

Therefore the interrupted invocation is a technical non-result. It is not recorded as an R9b2j scientific FAIL and it does not modify any historical R9b/R9b2/... classification.

## Identified implementation problem

The original R9b2j implementation constructed the DESI fiducial/CAMB cache and ShapeFit BAO-filter objects *inside every CLASS model run*, while the CLASS object was still live. This was not required for the preregistered Stage-A signed-response test and unnecessarily increased peak memory and repeated expensive fiducial/filter initialization.

The exact external cause of SIGTERM is not inferred from exit code 143 alone. Repair01 therefore treats the issue as process robustness/peak-resource isolation rather than assigning an unverified OOM cause.

## Frozen science construction

Repair01 changes no scientific definition or threshold from the R9b2j preregistration `dbf354f4ef3122fff44b1b389f1adc839e9e7f9d` and implementation `342ab7d85366e4f4521a7e3e2d19741e878aec3a`:

- same corrected stable-AeST CLASS source;
- same six theory redshifts;
- same tau grid `{10,5,2.5,1.25}`;
- same eta grid `{0,+/-0.025,+/-0.05}`;
- same `E <= 0.05`, `C >= 0.995`, and value/closure thresholds;
- same bounded source-state `Pdd` and `Ptt`;
- same signed central response `dP/deta` formed before integration;
- same 4096/8192/16384 linear-in-log-k response-resolution test;
- same PCHIP signed-response independent control;
- same corrected source-state ShapeFit construction;
- same official DESI DR1 data, covariance, nuisance columns, physical eta interval, matched-filter/GLS algebra.

## Technical repair only

Repair01 makes three execution changes.

1. Each `(tau,eta)` CLASS case runs in its own Python subprocess and writes a checkpoint. Process exit therefore releases CLASS memory completely between cases.
2. Checkpoints are reused on restart after validation of their frozen `tau`, `eta`, redshift grid, and finite state arrays. An interrupted invocation can resume without recomputing completed cases.
3. Stage-A workers compute only the CLASS/source-state quantities required by the signed-response gate. DESI fiducial/CAMB and BAO-filter objects are constructed exactly once, only after Stage A passes and after all CLASS worker processes have exited. ShapeFit scalars are then derived from the saved bounded source-state `Pdd` plus saved background metadata; no live CLASS object is held concurrently.

No DESI data vector or likelihood is evaluated if Stage A fails.

## Interpretation

A technical process/checkpoint repair may change runtime and peak memory only. It is forbidden to change a science gate or to reclassify the interrupted exit-143 invocation. The first completed Repair01 result is the R9b2j scientific result.