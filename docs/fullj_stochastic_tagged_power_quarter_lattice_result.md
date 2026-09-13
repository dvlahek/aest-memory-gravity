# Result: stochastic tagged quarter-lattice refinement

## Classification

`FULLJ_STOCHASTIC_TAGGED_POWER_QUARTER_LATTICE_FAIL`

This is a formal FAIL of the preregistered local quarter-lattice refinement. The result is diagnostic and complete. The independently validated physical-k metric-projection repair remains valid.

## Frozen campaign

- parent repaired-regression NPZ SHA256: `83fb7462ec970bfef953e3804d11a81fd5843745347fe77c318c9e39b8e6e82d`
- three preregistered local windows: `W1=[0.0925,0.1125]`, `W2=[0.155,0.170]`, `W3=[0.190,0.200]` in `k/h`
- 18 quarter-offset nodes at spacing `Delta k/h=0.00125`
- `B2={0,1}` Gaussian backgrounds
- symmetric tag amplitude `epsilon=0.05`
- geometry `kF/h=0.00125`, `NX=1024`, same physical real-space spacing as the coarser tagged geometries
- physical metric-projection cutoff `0<|k|/h<=0.32`
- total new integrations: 72

All 72/72 integrations were finite.

## Numerical health

The solver and constitutive diagnostics remain clean:

- canonical residual max: `1.631133162814778e-14`
- broadband saturation max: `4.261909001175596e-05`
- Hamiltonian residual max: `1.856358936790672e-16`
- momentum residual max: `1.8151553433031094e-16`
- shear residual max: `0.0`
- tagged-power identity relative residual: `6.794372476143193e-17`
- B0/B1 tagged-response relative L2: `8.345968998058182e-08`
- B0/B1 tagged-power relative L2: `2.0163934279407358e-07`

Therefore QL-G1 through QL-G4 pass.

## Failed refinement gates

The local `Delta k/h=0.0025` representation does not predict the direct quarter points at late time:

- maximum quarter-point power L2 error: `0.9927930753322448`
- median over redshifts: `0.028484510823650118`
- maximum peak-normalized error: `1.68052437725093`

Seven direct quarter-point spike-veto violations occur. The strongest are:

- `W2`, `k/h=0.16375`, `z=0.2`: direct power `0.034905543303345485`, neighboring `0.0025`-grid powers `0.00036550823477113955` and `0.00036404196739259643`, ratio `95.49865087226105`
- `W1`, `k/h=0.10125`, `z=0.2`: direct power `0.0030411604625048116`, neighboring powers `3.8124310992891476e-05` and `3.302698266713616e-06`, ratio `79.76958490008792`
- `W1`, `k/h=0.10625`, `z=0.2`: ratio `12.058183865122993`
- `W2`, `k/h=0.15875`, `z=0.5`: ratio `6.6541710282397935`

The refinement comparison also fails. `Delta k/h=0.0025` is better than `0.005` at `z=0.5`, but worse at `z=0.2` (`E_0025=0.6687467657857125` versus `E_005=0.5567493140048367`) and is not non-worse at all redshifts.

Thus:

- `QL_G5_absolute_quarter_power_interpolation_accuracy=False`
- `QL_G6_no_new_unresolved_quarter_power_spike=False`
- `QL_G7_refinement_improves_over_005=False`

## Interpretation

The quarter-lattice test falsifies the hypothesis that simple radial grid refinement from `0.005` to `0.0025` is sufficient to resolve the late-time tagged-power structure. Solver health, metric constraints, saturation, power algebra, physical-k projection, and two-background consistency remain clean, so the formal failure is localized to the late-time radial response itself or to a response-level numerical mechanism not probed by those health metrics.

This result does **not** license another blind grid halving to `Delta k/h=0.000625`. The next milestone must localize the origin of the sharp response. In particular it should distinguish:

1. a time-integration phase/convergence effect,
2. finite tag-amplitude/tangent contamination,
3. structure already present in the linear R2 bridge / CLASS-driven initialization,
4. structure generated only by the nonlinear scalar-current evolution,
5. the canonical-state contribution from the directly evolved effective-fluid / metric-correction contribution.

A small fixed-k source-localization audit should be used before any further radial production campaign.

## Scope

Remain true from earlier locks:

- `METRIC_PROJECTION_PHYSICAL_KMASK_REPAIR_VALIDATED=True`
- `STOCHASTIC_TAGGED_BOX_DOUBLING_INVARIANCE_REPAIRED=True`

Remain false:

- `STOCHASTIC_TAGGED_LOCAL_QUARTER_LATTICE_TESTED=False`
- `STOCHASTIC_TAGGED_LOCAL_0025_POWER_RESOLUTION_SUPPORTED=False`
- `STOCHASTIC_TAGGED_BOUNDED_POWER_INTERPOLANT_TESTED=False`
- `THREE_D_BOUNDED_CONTINUOUS_WEYL_POWER_LICENSED=False`
- `THREE_D_CONTINUOUS_WEYL_POWER_LICENSED=False`
- `EVOLVING_WEYL_POWER_LICENSED=False`
- `ACT_LIKELIHOOD_LICENSED=False`
- `OBSERVATIONAL_CLAIM_LICENSED=False`

No historical PASS or FAIL is reclassified and no threshold is relaxed.
