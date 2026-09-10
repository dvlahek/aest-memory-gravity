# D2C6F-R1 local run

This follow-up preserves the historical D2C6F FAIL and tests only the unresolved bath-source convergence question.

It evaluates the six original F6-failing members at `eta=0.125`, `Nx=128`, `Nstep=4096` with independent direct tan-Gauss-Legendre Drude baths of orders `128`, `256`, and `512`. The frozen PASS gate is direct `256 -> 512` source convergence `<=1e-2` for all four direct gravitational-source components and direct `256 -> 512` canonical-state/E convergence `<=1e-2`.

The old compressed orders `39` and `47` are rerun only as non-gating diagnostics against direct `512`; their disagreement cannot change the historical D2C6F classification.

Run from the repository root:

```bash
bash nl1c6d2c6f_r1/run_local.sh
```

The runner reuses the existing local Python environment and zero-safe CLASS installation when available. It does not create or run a GitHub Actions workflow.

Outputs:

- `results/nl1c6d2c6f_r1_direct_bath_source_convergence.log`
- `results/nl1c6d2c6f_r1_direct_bath_source_convergence.json`
- `results/nl1c6d2c6f_r1_local_bundle.zip`

After completion, the ZIP is the preferred file to return for analysis.

A PASS licenses only a separately preregistered self-consistent weak-field feedback stage, with direct `N=256` as primary bath and direct `N=512` as bath-order control. It does not by itself license observational inference or arbitrary-amplitude full nonlinear GR/AeST claims.
