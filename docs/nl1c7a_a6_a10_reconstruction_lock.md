# NL1C7A A6-A10 spherical reconstruction lock

Status: **PRE-RESULT / LOCKED BEFORE OFFICIAL A6-A10 WORKFLOW**

Parent A4:
- run `35104087182`
- head `0762723606536b58b7db39d41608fcaefe8eebd4`
- artifact `10450205501`
- SHA256 `9b1a4f998af55ce594cbdd6db78b9b99944cd25a3f690c68bab49ffef290ffc6`
- classification `NL1C7A_NATIVE_TRACE_COVERAGE_PASS`

Parent A5:
- run `35105898962`
- head `d910b814631e0e18337ff6c280d797a658623e5a`
- artifact `10450715138`
- SHA256 `41b1eeab85725f4765cfe491411a4b2f14bd15e4566fd62ca410487af7e2c2cf`
- classification `NL1C7A_A5_FINITE_GROWING_MODE_DENOMINATOR_PASS`

Frozen implementation:
- `nl1c7a/a6_a10_spherical_reconstruction.py`
- blob SHA `ff383c1ddc2cb2a684e2b5dd11fde0ae811e4fac`

Frozen gates remain exactly those in `docs/nl1c7a_predata_growing_mode_bridge.md`:
- A6: PCHIP-ln(a) versus linear-ln(a), complete nonzero spherical state L2 relative difference `<=2e-2` for every scale.
- A7: PCHIP-ln(k) versus linear-ln(k), same `<=2e-2` criterion.
- A8: target-profile errors and 256/512 mismatch `<=1e-4`.
- A9: X and E bridge identities `<=1e-6`.
- A10: no independent free-mode amplitude/phase, no clipping, frozen scale ladder.
- fields with primary norm `<=1e-14` are reported but excluded only from the relative quotient.

Frozen reconstruction uses the exact Repair05 trace, the analytic compensated-Gaussian target, 256/512 logarithmic k quadratures, and 256 radial points on `x in [0,8]`. No threshold, interpolation method, scale, field, or quadrature may be changed after this lock.

The official workflow must evaluate all A6-A10 gates even if one gate fails. A scientific non-PASS classification is not a workflow/technical failure and must be preserved historically. It does not license nonlinear evolution or finite eta.
