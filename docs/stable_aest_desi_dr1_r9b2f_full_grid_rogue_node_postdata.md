# Stable AeST DESI DR1 R9b2f full-grid post-result record

## Certified result

R9b2f completed with `EXIT=0` and the preregistered classification

`STABLE_AEST_DESI_DR1_R9B2F_HIGH_K_EXTRAPOLATION_DEFECT_CERTIFIED`.

This is a theory-only numerical-localization result. No DESI data vector, covariance, likelihood, eta preference, or tau constraint was evaluated. No historical R9b/R9b2/R9b2a/R9b2b/R9b2c/R9b2d/R9b2e result is reclassified.

## Frozen provenance

- preregistration: `8413ed74450e387b3dee543ff67b39bf2cbb31bc`
- implementation: `1c1cbbbdc2fcb43441c1659f7282ae40c3b18487`
- runner: `0a304537472818b0906b551b896cf426c5d7febb`
- parent R9b2e postdata: `f1f2bfd032065360ec7a18c080403d6e39f54dc7`
- parent R9b2e JSON SHA-256: `3deb9cf8b946f56727b4f10af70dababefda2b31098e1039b15ac21d03c5d255`.

## Primary Stage-A result

The historical pathology was exactly reproduced by the old `PowerSpectrumInterpolator1D(k,P).sigma8()` defaults on the 108-node DEFAULT CLASS transfer grid extending to `k_max = 4.182301935446609 h/Mpc`.

At the first three theory redshifts:

- z=0.295364043: default `f=1778.1642650195856`; bounded `f=0.6812675558559022`; log-linear bounded `f=0.6811806956033798`; internal proxy `0.6810541276379364`.
- z=0.509628868: default `f=16898989.557820328`; bounded `f=0.7623953787041418`; log-linear bounded `f=0.7623925963775807`; internal proxy `0.7628875726910158`.
- z=0.705795647: default `f=88.90748958451566`; bounded `f=0.8174091235933907`; log-linear bounded `f=0.8174058700808504`; internal proxy `0.8182626338213397`.

At z>=0.918585197 the old default happened to be numerically benign, and all three methods remained near the internal proxy.

Across all six redshifts:

- maximum relative default-vs-bounded f difference: `0.99999995488515`;
- maximum relative bounded-vs-loglinear-bounded f difference: `1.274980024745674e-4`;
- all bounded source-state rows were finite and physical;
- bounded source-state sigma8_dd agreed with internal sigma8 within the frozen `5e-3` gate;
- bounded f agreed with the internal growth proxy within the frozen `5e-3` gate.

This certifies the preregistered high-k extrapolation branch. The pathological factors of 10^2-10^7 arise only when the generic power-spectrum interpolator extrapolates the AeST velocity spectrum beyond the actual CLASS transfer support. Constraining the same interpolator to the true transfer support removes the pathology, and an independent bounded log-linear integration reproduces the same healthy result.

## Exact-k raw control

The deterministic Stage-B candidate set contained ten automatic-grid nodes around `0.1745 <= k/h <= 0.2346`, where the sigma8 kernel gives the largest ordinary contribution.

For these exact k values:

- automatic-grid transfer vs exact-k rerun transfer maximum discrepancy: `0.0`;
- exact-k raw-history vs rerun-transfer maximum discrepancy: `1.2135790530924706e-6`;
- exact-k transfer k mismatch: `0.0`.

Thus no automatic-grid rogue-node defect was found on the deterministic candidate set, and the raw solver -> transfer mapping remains numerically clean.

## Reporting defect in secondary F6 gate

The generated Stage-B JSON contains `NaN` for the internal `sigma8` and growth proxy in the exact-k rerun. The implementation's `max(current, NaN)` accumulation leaves the stored internal Stage-A-vs-Stage-B maximum at zero, so the emitted `R9B2F_F6_internal_solution_invariance=true` is a reporting artefact and must not be interpreted as a valid Stage-B internal-invariance measurement.

This does **not** alter the certified R9b2f classification. The preregistered priority rule for `STABLE_AEST_DESI_DR1_R9B2F_HIGH_K_EXTRAPOLATION_DEFECT_CERTIFIED` depends on the independently completed Stage-A facts:

1. historical `COSMO_DEFAULT` pathology reproduced;
2. `COSMO_BOUNDED` healthy at all six redshifts;
3. default-vs-bounded difference material (>=0.05).

Those conditions were satisfied before any Stage-B classification branch. Stage B is therefore corroborative for the high-k result, not logically required for it. No post-result gate or threshold is changed.

## Consequence

The next extraction validation must use DEFAULT CLASS k sampling and prohibit extrapolation beyond the actual finite CLASS transfer support. It must independently compare the bounded cosmoprimo integral with a direct bounded log-linear sigma8 integral across the complete preregistered tau/eta theory grid before any DESI likelihood is re-run.
