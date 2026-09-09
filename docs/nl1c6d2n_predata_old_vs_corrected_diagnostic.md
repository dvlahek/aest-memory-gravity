# NL1C6D2N predata — historical versus corrected no-refit diagnostic

Status: **DECLARED BEFORE THE FIRST REGENERATED OLD-VS-CORRECTED COMPARISON OUTPUT**.

This diagnostic is run only after the corrected CLASS baseline R1 passes. It does not classify the corrected theory and does not authorize memory, nonlinear branch selection, or likelihood analysis.

The comparison uses the same pinned CLASS commit, same patch chain, same cosmological parameters, and `eta=0` in both cases. The only physics difference is the Exp normalization:

```text
historical: K=2 K2 Z0^2 (exp(Z^2)-1), KQ=4 K2 Z0 Z exp(Z^2), KQQ=4 K2 exp(Z^2)(1+2Z^2)
corrected:  K=  K2 Z0^2 (exp(Z^2)-1), KQ=2 K2 Z0 Z exp(Z^2), KQQ=2 K2 exp(Z^2)(1+2Z^2)
```

No cosmological refit is permitted in this diagnostic.

Report relative-L2 differences for

```text
d_b
t_b
d_m
phi
psi
TT
TE
EE
```

on the common native grids. Also compare the public effective-dark background density `(.)rho_cdm` and Hubble background after interpolation on the common `0<=z<=6` interval if their native background grids differ.

The comparison is descriptive: no similarity threshold is used to turn a changed corrected model into a PASS or FAIL. Its purpose is only to determine the rerun scope. Historical v053 results remain historical results of the factor-2 model irrespective of the measured difference.
