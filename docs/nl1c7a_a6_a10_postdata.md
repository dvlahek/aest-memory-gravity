# NL1C7A A6-A10 post-data freeze

Final classification:

`NL1C7A_TIME_INTERPOLATION_CONTROL_FAIL`

This is a numerical-interface certification failure at A6 only. It is not a failure of the eta=0 AeST growing solution, the spherical variational bridge, the self-gravity closure, the k-space reconstruction, or the bridge identities. It does not license nonlinear evolution or finite eta.

## Frozen provenance

- pre-data C7A prereg: `docs/nl1c7a_predata_growing_mode_bridge.md`
- A6-A10 implementation lock: `86a70318c60cc4c0dddea7012dcd5193db7b5f62`
- frozen implementation blob: `ff383c1ddc2cb2a684e2b5dd11fde0ae811e4fac`
- official Repair01 workflow run: `35106735707`
- workflow head: `8b02243fc0b1ea58f00466868d58170c73dbc4e4`
- artifact: `10450343358`
- artifact SHA256: `99b795389566a21b0438977af55bae21f92b428d52ad50ba2c9855bafda28fb5`

Parent A4 exact native trace:
- run `35104087182`
- artifact `10450205501`
- SHA256 `9b1a4f998af55ce594cbdd6db78b9b99944cd25a3f690c68bab49ffef290ffc6`

Parent A5 denominator PASS:
- run `35105898962`
- artifact `10450715138`
- SHA256 `41b1eeab85725f4765cfe491411a4b2f14bd15e4566fd62ca410487af7e2c2cf`

## Gate results

- A6 time-interpolation control: **FAIL**
- A7 k-interpolation control: **PASS**
- A8 target-profile reconstruction: **PASS**
- A9 bridge identities: **PASS**
- A10 no-free-mode injection: **PASS**

A6 failed only for the aether rapidity `u` under the frozen PCHIP-ln(a) versus linear-ln(a) control:

- `R_sigma=5 h^-1 Mpc`: relative L2 difference `0.03627035296651964`
- `R_sigma=10 h^-1 Mpc`: `0.0362778165143206`
- `R_sigma=20 h^-1 Mpc`: `0.036267373355685355`

Frozen A6 limit: `0.02`.

The corresponding `udot` differences remain below the limit:

- 5: `0.01665426502050646`
- 10: `0.016652814565335686`
- 20: `0.01665077347129382`

All metric, dust, scalar-phi and velocity fields pass A6. `phidot-Q` has primary norm about `1.64e-21` and is reported but excluded from the relative quotient under the pre-registered `1e-14` zero-norm rule.

## Passing controls

A7 maximum active PCHIP-ln(k) versus linear-ln(k) difference:

`0.0016264273714659244 < 0.02`.

A8 maximum target reconstruction error/mismatch:

`6.299255876536103e-07 < 1e-4`.

A9 maximum bridge-identity relative error:

`1.7994919681600752e-07 < 1e-6`.

A10 source audit passes: frozen scale ladder, no clipping, no independent free-mode amplitude/phase assignment, single baryon-target normalization.

## Interpretation and claim boundary

The failure is localized to temporal extraction of the aether growing-mode amplitude around `a_i=0.02`. The same reconstructed state is stable to the independent k-interpolation control, the analytic spherical-Bessel transform is highly converged, and both C6 bridge identities pass. Therefore this result does not support changing the A6 threshold or selecting a preferred time interpolator post-data.

The certified continuation must use a separate pre-registered numerical-interface repair that increases time information at `a_i` (for example an exact-`a_i` accepted diagnostic output or a denser accepted source-time grid) while preserving the original C7A failure historically. The current result does not certify unique eta=0 nonlinear initial data and therefore NL1C7 nonlinear evolution remains blocked.
