# v0.52 locked global-refit continuation

This directory contains the optimizer-only continuation test defined before inspecting its outcome.

The four starts are the exact verified v0.50 endpoints from GitHub Actions run 34014387686. The implementation imports and reuses `v050/refit_lm_multistart.py`; only its deterministic `STARTS` dictionary is replaced. Therefore the AeST model, KB=0.0665, reference KB=0.1, CLASS objective, finite-difference steps, parameter bounds, trust caps, damping ladder, line-search factors, and convergence logic remain unchanged.

The predeclared certification gates are unchanged from v0.50: every result finite, every final baseline CV S/N < 5, four-start spread < 0.5, and maximum normalized condition < 1e8.
