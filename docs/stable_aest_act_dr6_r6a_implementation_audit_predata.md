# R6a ACT DR6 implementation audit — pre-result checkpoint

Date: 2026-09-14

This checkpoint was committed after R6a implementation but before the first R6a ACT data result.

Final amended R6a pre-data lock:

`05d338e1dde7719cc78b132cd146a408c6a90d62`.

R5b post-data parent lock:

`3242335ece23fbeb743f075a1df1aa70acaab211`.

Audit findings:

- comparing the final R6a pre-data lock to implementation HEAD changed only two new files: the R6a Python driver and local runner;
- no historical v0.62/v0.65 ACT script is imported or used;
- official ACT likelihood source is frozen to `ACTCollaboration/act_dr6_lenslike` commit `b386ddbb5821c1216c709f051c9289292f174d30`;
- the upstream v1.2.1 tag metadata mismatch (`__version__ = 1.2.0`) is explicitly handled and was preregistered before implementation;
- `variant=act_baseline`, `lens_only=True`, `like_corrections=False`, `nsims_act=796`, and `trim_lmax=2998` are explicit;
- the R6a physical memory grid is only eta = 0, 0.01, 0.025, 0.05;
- no Planck lensing combination, ACT extended variant, Halofit/nonlinear path, or historical ACT result is used;
- the runner creates a dedicated Python environment and a fresh exact official ACT source checkout;
- the official ACT fiducial lens-only chi-square control is evaluated before R5b template projection;
- R5b parent JSON/NPZ files are SHA-256 locked;
- ACT data and likelihood files consumed at runtime are SHA-256 manifested;
- ACT bandpower support outside the R5b certified L=40..2000 domain is a hard gate;
- the signed matched-filter coefficient is diagnostic only and is not interpreted as a physical negative eta;
- measured eta, delta-chi-square, Fisher norm, and template S/N do not enter PASS/FAIL.

No R6a science result existed when this audit was committed.
