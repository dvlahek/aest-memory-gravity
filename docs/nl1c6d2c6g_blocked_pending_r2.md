# D2C6G status — blocked pending D2C6F-R2 vector-phase repair

Date: 2026-09-11

No D2C6G target result has been generated and no D2C6G implementation has been committed.

During the pre-implementation derivation of the action-source to metric-feedback map, a representation issue was identified in the inherited D2C6F direct-stress reconstruction. The offline bath field `z_j(x)` is a scalar Fourier/potential representation obeying

`z_j = omega_j q_{j,L}/(k sqrt(w_j))`

at the level of longitudinal Fourier amplitudes. The physical real-space longitudinal vector component must therefore carry the same spatial derivative phase as `X_x = d_x chi/a`:

`q_{j,x}(x) = sqrt(w_j)/omega_j * d_x z_j(x)`.

The D2C6F implementation instead reconstructed the vector amplitude with the positive spectral operator `|d_x| z_j`, while `X_x` used the signed derivative `d_x chi`. For a real cosine mode these objects are in quadrature (cosine versus sine), so the completed-square term `omega q_x - sqrt(w) X_x` cannot exhibit the pointwise cancellation required by the local NL0B/NL1C3B action.

This issue does not affect D2C6C/D2C6D/D2C6E retained scalar-current dynamics, because their bath residual uses the scalar amplitude identity directly and does not construct the local vector stress. It does affect the physical interpretation of D2C6F/R1 direct metric-stress amplitudes.

Therefore the previously recorded D2C6F-R1 numerical PASS remains a historical convergence result for the old stress reconstruction, but its `SELF_CONSISTENT_WEAKFIELD_FEEDBACK_STEP_LICENSED=True` output is superseded and may not be used to start D2C6G.

D2C6G is blocked until a separately preregistered D2C6F-R2 run replaces `|d_x| z_j` by the action-consistent `d_x z_j`, re-audits the completed-square vector identity, and recertifies direct-source convergence.

No D2C6G gate is relaxed or evaluated by this status note.
