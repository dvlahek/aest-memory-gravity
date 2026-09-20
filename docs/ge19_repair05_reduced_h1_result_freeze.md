# GE19 Repair05 reduced-H1 result freeze

## Historical result

Repair05 science execution is frozen as

`GE19_REPAIR05_WINDOW_RETARDED_REDUCED_H3_Z20_PARTICULAR_FAIL`.

Failure stage: `Stage_A_reduced_H1_reclosure`.

Historical Repair05 must not be relabeled.

## Frozen local result hashes

- science JSON: SHA256 `73fce46fca03659e48b904cafef949ffd83d6ca54fc06f8839ff336b413ef166`, 33333 bytes;
- inner FULL log: same SHA256 and byte count;
- outer runner log: SHA256 `56c4963e2e38a6cc027cb5971ae44e8917ee8ed7680f181598acdac1d5a9c186`, 35706 bytes.

## What Repair05 established

The lock, Python environment, frozen-parent checks and synthetic numerical self-audit all passed.

The synthetic scaled solve reached O(1e-17) original-system residual, so the Repair05 equilibration code itself works in its preregistered test regime.

On the actual Stage-A matrices, however:

- maximum row dynamic range reached `4.2495246473679423e24`;
- maximum post-row column scaling range reached `541.0511439718944`;
- primary 64-node original-system residual remained `1.0`;
- 32-node residuals remained approximately `1.0`;
- primary64/control32 state relative L2 remained approximately `1.0`;
- shift and anisotropy monitors remained O(1);
- 32-node initial dynamic match was O(1e-18), while 64-node initial match degraded to at most `0.003908138519607954`;
- all outputs remained finite.

Thus deterministic diagonal equilibration does not repair the real Stage-A discretization.

## Diagnosis boundary for Repair06

The failure pattern is consistent with the global centered-collocation realization becoming numerically singular/stiff under the corrected physical Z coordinate. It is not licensed as evidence against gravitational memory or against the continuum reduced-H1 equations.

Repair06 may replace only the **time discretization / state representation** of the same frozen Euler-Lagrange system.

The licensed formulation is a canonical-momentum initial-value realization:

- dynamic coordinates: `S,u,phi,T`;
- canonical momenta: `pS = L_t + R_t`, `pu = u_t`, `pphi = phi_t`, `pT = T_t` at the level of the frozen first-order directional partials;
- nondynamical variables: `N, delta_varrho`, solved algebraically at each time;
- the same lapse and dust-density equations remain algebraic;
- the same isotropic, aether, scalar and dust-potential Euler-Lagrange equations evolve the momenta;
- the same frozen initial dynamic values and cosmic-time derivatives at z=1.5 are used;
- the same physical source, gauge, C values, beta values, modes and thresholds remain unchanged.

No Repair05 science threshold may be relaxed.
