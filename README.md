# AeST Memory Gravity

[![v018 CLASS compile and zero regression](https://github.com/dvlahek/aest-memory-gravity/actions/workflows/v018-class-compile.yml/badge.svg)](https://github.com/dvlahek/aest-memory-gravity/actions/workflows/v018-class-compile.yml)

Research code and validation harness for an AeST-based history-dependent gravitational memory model.

## Current status

**v0.18 — CLASS source integration and zero-regression: PASS.**

The workflow pins official CLASS v3.3.4 at commit `e85808324f51fc694d12e3ed7439552a3c3f9540`, compiles pristine and patched trees, verifies that the AeST-memory module is linked, and runs the same Planck-2018 CLASS baseline in both trees.

All nine generated CLASS `.dat` outputs are byte-identical between pristine and patched builds. This freezes the software-integration baseline before the AeST cosmological perturbation path is enabled.

## Next gate

**v0.19:** add the published AeST Cosh/Exp background and scalar perturbation states

`delta_A`, `theta_A`, `alpha_A`, `E_A`

with memory still fixed to `eta = 0`. The finite memory bath is not switched on until the AeST-only CLASS baseline is validated.

See `THEORY_v018.md` and `.github/workflows/v018-class-compile.yml`.
