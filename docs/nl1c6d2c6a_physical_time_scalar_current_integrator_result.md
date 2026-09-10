# NL1C6D2C6A result: physical-time nonlinear FLRW scalar-current integrator

Status: **FORMAL RESULT LOCK**.

The preregistered D2C6A pilot was evaluated on corrected branch `v053-exp-normalization-corrected` with the fixed physical-time RK4 discretizations and corrected CLASS forcing.

Final classification:

`NL1C6D2C6A_PHYSICAL_TIME_SCALAR_CURRENT_INTEGRATOR_FAIL`

This is a numerical/reduced-system implementation FAIL under the preregistered gates. It is not evidence of physical nonexistence of an AeST cosmological branch.

## Gate results

- I1 corrected provenance/dense inputs: PASS.
- I2 initial-state gate: FAIL. Maximum initial metric = `2.469918916957e-10`, above the preregistered `1e-12` threshold.
- I3 independent linear control: PASS.
  - alpha relative L2 = `4.565964150143e-05`.
  - E relative L2 = `3.116399354910e-05`.
  - chi relative L2 = `4.583708027110e-05`.
- I4 nonlinear trajectory health: PASS.
  - maximum stored canonical-constraint residual = `7.011122354644e-11` <= `1e-10`.
  - minimum `1+j_eff` = `1.971701606536e+00` > 0.
- I5 fixed timestep convergence: PASS, maximum relative L2 = `9.087696189992e-08`.
- I6 spatial convergence: PASS, maximum relative L2 = `3.981068961137e-08`.
- I7 descriptive nonlinear response:
  - alpha = `1.763578355146e-01`.
  - E = `2.950975142425e-01`.
  - chi = `1.763578063729e-01`.
  - x_max = `1.767656649979e+08`.
- I8 scope remained clean.

Because I2 failed, `D2C6B_ALL27_LICENSED=False` remains binding.

## Interpretation

The trajectory itself is finite, converged in both time and space, and reproduces corrected CLASS in the independent linear control at the `~3e-5` to `5e-5` level. The only failed preregistered gate is the initial canonical-constraint metric.

The initial implementation stores `P_alpha` and later forms the elliptic combination `P_alpha + Q P_chi`. At the initial state, `P_alpha` is constructed as a large `-Q P_chi` contribution plus the much smaller spatial elliptic remainder. Forming the canonical combination therefore subtracts nearly equal floating-point numbers. The observed `~2.47e-10` residual is consistent with a potentially ill-conditioned diagnostic, but this interpretation does not retroactively alter the D2C6A FAIL.

Any repair must be separately preregistered and must not relax the original thresholds or physics.
