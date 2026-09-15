# Stable-AeST DESI DR1 R9b ShapeFit projection — pre-result repair03

Status: technical pre-result repair only. No DESI memory likelihood result has been produced.

The repaired R9b execution after repair02 reached the official DESI ShapeFit module import, but every worker failed before loading the ShapeFit data/theory vector because the execution virtual environment lacked the `cobaya` package required by the official DESI module:

`ModuleNotFoundError: No module named 'cobaya'`

This failure occurs before any successful `(tau_H0, eta)` CLASS/ShapeFit worker result, before construction of the DESI data vector, and before any matched-filter, GLS, eta-hat, sigma-eta or Delta-chi2 result. Therefore it is classified as an infrastructure/dependency failure and not a science outcome.

Repair03 is frozen before the executable repair and is limited to installing Cobaya from the exact upstream Git commit

`CobayaSampler/cobaya@b76b6fed2a6c8c5594c6f92d5058bef10079746a`

inside the already-used R9b virtual environment before invoking the existing repair02 runner. No R9b science code, DESI files, tau grid, eta grid, nuisance projection, ShapeFit mapping, thresholds, gates, parent classifications, or physical interpretation is changed.

Historical state is preserved:

- initial R9b execution: filename-encoding technical pre-result failure;
- repair02 execution: missing-Cobaya technical pre-result failure;
- neither execution licenses a DESI memory result or reclassification.
