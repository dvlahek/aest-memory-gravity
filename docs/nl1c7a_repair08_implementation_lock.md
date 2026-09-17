# NL1C7A Repair08 — implementation lock

## Locked sequence

- Repair07b result-freeze commit: `c32c77940b5a338fd6ca42f7251b3a1b57927fb7`.
- Repair07b result-freeze blob: `fa0d38dcce6902b224c8d5055a883ad163dab5bd`.
- Repair08 preregistration commit: `93807f46ea532849aaf3d4dc8efdd7f25d985bd2`.
- Repair08 preregistration blob: `258c74068d0f6bfb33867e07057b1977344c022c`.
- Repair08 implementation commit: `b99954cace654d7edac9d202b1db8537788dc92b`.
- Repair08 evaluator blob: `94fb3f42a7c819b0525860f7344d5dbaff93da19`.

## Frozen parent code

- `nl1c7a/a5_denominator_audit.py`: `47b486ca2defbd1db029df003b37909a9d4d170d`.
- `nl1c7a/a6_a10_spherical_reconstruction.py`: `ff383c1ddc2cb2a684e2b5dd11fde0ae811e4fac`.
- `nl1c7a/evaluate_dense_time_repair01.py`: `aa84b4892586a59455ec93b6dfdc0057adc20d38`.
- `nl1c7a/make_repair01_coverage_compat.py`: `db52f94e1b896b2d277bb306a9eb4a63ea412ead`.
- historical Repair01 evalfix workflow: `3e784644e92aea67c8adbc36139d72694052e5ae`.

## Retained artifacts

- certified C7A Repair01/evalfix artifact `10481526695`, digest `sha256:c2ede2e602e35bbd52afdc0a5eee22cb1bf5c6efc2e1063bf8f2b91a0554fb6c`;
- dense C7A trace artifact `10469031693`, digest `sha256:193325536405f9a21a238f5fbe71a772d2484a096dcbfec3d6007e825cc38f70`.

## Frozen science settings

- `a_i = 0.02`.
- `eta = 0`.
- scales `[5.0, 10.0, 20.0] h^-1 Mpc`.
- primary/control Fourier quadrature `256/512`.
- radial points `256`.
- scalar identity limit `1e-10`.
- A6/A7 limit `2e-2`.
- A8 limit `1e-4`.
- A9 limit `1e-6`.
- unchanged-state regression limit `1e-12`.
- metadata reproduction limit `1e-15`.

## Locked repair boundary

The canonical repaired scalar is `PCHIP(log(a), a Q theta_A/k^2)` after the composite is formed on each native k-group. The independent check is `PCHIP(log(a), chi-Q alpha_A)` formed on the same native grids.

The frozen parent C7A reconstruction is reused for all state quantities. Only `phi` is replaced by the canonical reconstructed scalar and `X_from_state` is deterministically recomputed from that `phi`. Every other parent state array must regress to the historical certified NPZ within `1e-12`.

A new NPZ is written only after every Repair08 gate passes. The historical C7A NPZ is never overwritten.

## Locked terminal classes

- `NL1C7A_REPAIR08_IDENTITY_PRESERVING_SCALAR_REPRESENTATION_CERTIFIED`;
- `NL1C7A_REPAIR08_SCALAR_IDENTITY_FAIL`;
- `NL1C7A_REPAIR08_TIME_INTERPOLATION_CONTROL_FAIL`;
- `NL1C7A_REPAIR08_K_INTERPOLATION_CONTROL_FAIL`;
- `NL1C7A_REPAIR08_RECONSTRUCTION_FAIL`;
- `NL1C7A_REPAIR08_BRIDGE_IDENTITY_FAIL`;
- `NL1C7A_REPAIR08_FREE_MODE_INJECTION_FAIL`;
- `NL1C7A_REPAIR08_STATE_REGRESSION_FAIL`;
- `NL1C7A_REPAIR08_IMPLEMENTATION_FAIL`.

A Repair08 certification is not a B4 PASS and is not an observational detection claim.
