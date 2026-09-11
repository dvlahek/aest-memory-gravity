# Full-J Jacobian dense-background regression correction

The first execution of the preregistered mode-coupling Jacobian exposed an implementation mismatch before the diagnostic was completed.  The Jacobian script replaced the dense-map ten-redshift CLASS request by the reduced set `z={0.25,0.5,1}` before extracting `d_b`.  The resulting frozen backgrounds did not reproduce the completed dense-map realization: for example, at `z=0.25`, `delta_rms` changed from `2.871804732026e+01` to `3.100933239241e+01`, and the previously observed `k=0.6 Mpc^-1` source node changed from a ratio `0.116538718275...` to approximately `1.002`.

This is an orchestration/regression error, not a change in the full-J equations or in any preregistered diagnostic threshold.  The correction keeps the original dense ten-redshift CLASS extraction exactly as used in `fullj-dense-reclosure-map`, filters to the three Jacobian redshifts only after extraction, and adds hard pre-solve regression checks against the completed dense run:

- `delta_rms(z=0.25) = 2.871804732026e+01`
- `delta_rms(z=0.5)  = 1.053860907840e+01`
- `delta_rms(z=1.0)  = 1.754686661334e+00`
- source-node ratio at `z=0.25`, `k=0.6 Mpc^-1`: `0.1165387182751355`

The original Jacobian implementation, tangent equations, physical parameters, and gates remain unchanged.  A corrected run is admissible only if the new `FULLJ_JAC_DENSE_BASELINE_REGRESSION_PASS` guard is printed before nonlinear/Jacobian solves.  Results from the mismatched partial run are retained only as debugging evidence and must not be used for physical interpretation.