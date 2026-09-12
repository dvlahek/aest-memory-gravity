# Result: repaired stochastic tagged power-lattice regression

## Classification

`FULLJ_STOCHASTIC_TAGGED_POWER_LATTICE_KMASK_REGRESSION_FAIL`

This is a formal FAIL of the preregistered repaired power-lattice regression. The physical-k metric-projection repair remains independently validated; this result does not alter that PASS. The failure is localized to the radial power-adequacy gates, not solver, metric-constraint, stochastic-background, overlap-reuse, or constitutive health.

## Frozen campaign

- total new integrations: 108
- overlap controls: `k/h={0.060,0.095,0.160}`
- repaired Stage-A high-k nodes: `k/h={0.165,0.170,0.175,0.180,0.185,0.190,0.195,0.200}`
- repaired half-lattice controls: 16 nodes selected by the frozen historical curvature algorithm
- backgrounds: `B2={0,1}`
- symmetric tag amplitude: `epsilon=0.05`
- physical metric-projection cutoff: `0<|k|/h<=0.32`
- redshifts: `z={6,5,4,3,2,1.5,1,0.5,0.2}`

All 108/108 integrations were finite.

## Numerical health

The non-radial diagnostics are clean:

- canonical residual max: `1.898119251620627e-14`
- broadband saturation max: `4.3492147920475385e-05`
- Hamiltonian residual max: `1.8575201213121864e-16`
- momentum residual max: `1.7752709980363756e-16`
- shear residual max: `0.0`
- direct power identity relative residual: `1.5145037872560905e-17`

The repaired overlap regression validates the limited low-k reuse assumption at numerical precision:

- response global relative L2: `8.565330963311704e-15`
- response per-k max: `9.234223552117672e-15`
- power global relative L2: `1.6815475556913675e-14`
- power per-k max: `1.7685802424226395e-14`

Thus KR-G1 through KR-G5 pass.

## Failed radial power gates

The repaired half-lattice interpolation still fails at late time:

| z | power L2 | peak-normalized error |
|---:|---:|---:|
| 6.0 | 6.6743975e-4 | 7.2243597e-4 |
| 5.0 | 6.7635294e-4 | 7.3019775e-4 |
| 4.0 | 7.0941721e-4 | 7.5095732e-4 |
| 3.0 | 9.5009255e-4 | 8.3426572e-4 |
| 2.0 | 3.3081255e-3 | 1.7886697e-3 |
| 1.5 | 9.1387362e-3 | 5.2280285e-3 |
| 1.0 | 2.9382349e-2 | 1.7048594e-2 |
| 0.5 | 9.3141965e-2 | 5.3514579e-2 |
| 0.2 | 2.5928455e-1 | 1.4626211e-1 |

Summary:

- `power_half_L2_max = 0.25928455420573615`
- `power_half_L2_median = 0.00330812554069321`
- `power_half_peak_max = 0.14626211283648557`

Therefore KR-G6 fails against the unchanged thresholds `0.05`, `0.025`, and `0.10`.

Two direct repaired midpoint spike violations remain:

1. `k/h=0.0975`, `z=0.2`: direct power `0.009340862382415507`, endpoint powers `0.0007443059626697503` and `3.8124310992891476e-05`, ratio `12.54976159120206`.
2. `k/h=0.1975`, `z=1.0`: direct power `0.003958412240180996`, endpoint powers `0.0018520051822525424` and `0.001372382073984246`, ratio `2.137365639207602`.

Therefore KR-G7 also fails.

## Interpretation

The independently validated physical-k repair was necessary and removes the box-dependent projection artifact, but it is not sufficient to make a `Delta k/h=0.005` radial power lattice adequate at late times. The repaired overlap regression is essentially exact, so stale low-k reuse is not the origin of the remaining failure. The direct repaired half-lattice measurements show real sub-0.005 radial structure within the frozen tagged broadband construction.

Compared with the historical power-lattice FAIL, the repaired aggregate late-time interpolation errors improve somewhat (`max power L2: 0.30864 -> 0.25928`; `max peak error: 0.18662 -> 0.14626`), but the dominant `k/h=0.0975, z=0.2` midpoint feature remains and its endpoint spike ratio is still very large. Hence the correct next step is radial refinement, not another metric-projection repair and not a relaxation of the power gates.

## Scope

- `METRIC_PROJECTION_PHYSICAL_KMASK_REPAIR_VALIDATED=True` remains valid.
- `STOCHASTIC_TAGGED_BOX_DOUBLING_INVARIANCE_REPAIRED=True` remains valid.
- `STOCHASTIC_TAGGED_POWER_LATTICE_KMASK_REGRESSION_TESTED=False` because the preregistered PASS condition was not met.

Still not licensed:

- `STOCHASTIC_TAGGED_BOUNDED_POWER_INTERPOLANT_TESTED=False`
- `THREE_D_BOUNDED_CONTINUOUS_WEYL_POWER_LICENSED=False`
- `THREE_D_CONTINUOUS_WEYL_POWER_LICENSED=False`
- `EVOLVING_WEYL_POWER_LICENSED=False`
- `ACT_LIKELIHOOD_LICENSED=False`
- `OBSERVATIONAL_CLAIM_LICENSED=False`

No threshold is relaxed and no historical FAIL is reclassified.
