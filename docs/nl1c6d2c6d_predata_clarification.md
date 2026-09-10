# NL1C6D2C6D pre-data clarification — control health

This clarification is committed before any D2C6D finite-positive-eta workflow exists or any finite-positive-eta result is generated.

The primary pre-data file `docs/nl1c6d2c6d_finite_positive_eta_predata.md` defines D4 health on all 81 primary trajectories and D5-D7 using order/time/space control trajectories at the largest eta.

The implementation applies one additional conservative requirement: every D5-D7 control trajectory must itself remain finite, satisfy the same full stable-canonical constraint threshold `<=1e-10`, and keep `min(1+j_eff)>0`. Failure of this control health makes D4 false.

This only strengthens the frozen numerical certification. It does not change eta values, equations, members, thresholds, resolution choices, response diagnostics, or any PASS-favoring condition. No response sign, ordering, or amplitude requirement is introduced.
