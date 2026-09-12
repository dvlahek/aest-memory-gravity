# Full-J dense radial Weyl extension — locked result

## Classification

`FULLJ_DENSE_RADIAL_WEYL_EXTENSION_FAIL`

This is a completed numerical/physics result, not an implementation abort. The earlier 21-history loader issue was repaired before this run; all 21 direct K2 nodes were then evolved successfully.

## Locked direct-grid health

All 21 direct single-mode runs are finite at all nine checkpoints. Canonical residuals are O(1e-15), metric Hamiltonian/momentum residuals are O(1e-16), and shear residual is zero. The maximum dense saturated-closure residual is

`1.4804539211489309e-03`,

well below the frozen `2e-2` gate.

The zero-safe phase audit on the dense grid gives

- global quadrature relL2: `8.511017478625061e-10`,
- max absolute imaginary transfer: `1.5898928732366847e-09`,
- max real-projection power change: `2.129244965659623e-15`.

Initial corrected-CLASS normalization closes to

`4.095817310098092e-15` max relative error.

Anchor recovery against the previously licensed six-node result gives

- median relative difference: `2.939577912506729e-10`,
- max relative difference: `1.0426170916101378e-06`.

Power-node identity closes to `4.6173796186140965e-17`.

Therefore G1-G6 and G10 PASS.

## Failed interpolation/convergence gates

The only failures are the continuous signed-transfer interpolation gates:

- G7 level-1 direct holdout accuracy: FAIL,
- G8 refinement improvement: FAIL,
- G9 fine-grid K1->K2 convergence: FAIL.

Frozen summary values include

- holdout level-1 transfer L2 median: `3.968921323485272e-03`,
- holdout level-1 transfer L2 max: `2.9980606152934963e-01`,
- holdout level-1 power L2 median: `5.707821361102729e-03`,
- holdout level-1 power L2 max: `1.1377228775215022e-01`,
- holdout level-1 power peak max: `1.1116740948319719e-01`,
- holdout transfer improvement count: `9/9`,
- holdout power improvement count: `0/9`,
- fine K1->K2 transfer L2 median: `2.5771411165036863e-03`,
- fine K1->K2 transfer L2 max: `1.5749734494038972e-01`,
- fine K1->K2 power L2 median: `3.6256623973301002e-03`,
- fine K1->K2 power L2 max: `6.996685305312153e-02`,
- fine K1->K2 power peak max: `5.721011594461192e-02`.

## Interpretation

The direct dense R2 transfer nodes themselves are certified numerically healthy over the tested domain. The FAIL is specifically a failure of the preregistered representation

`PCHIP[ signed Re(T_W) vs ln k ]`

as a uniformly converged continuous radial model over all redshifts.

The failure is concentrated at low redshift, where both the corrected-CLASS Weyl transfer and the R2 transfer develop multiple extrema and zero crossings in k. Thus the direct K2 grid is informative, but the original six/eleven-node signed-transfer interpolation does not resolve the radial oscillatory structure well enough.

A post-data diagnostic shows that the correction field

`Delta T_W = T_W_R2 - T_W_CLASS`

is substantially smoother than the full transfer because the rapidly varying/zero-crossing structure is already present in the corrected-CLASS reference. This diagnostic is not used to alter the present classification.

## Scope lock

The present FAIL preserves:

- `THREE_D_DENSE_RADIAL_WEYL_NODES_LICENSED=False`
- `THREE_D_BOUNDED_CONTINUOUS_WEYL_POWER_LICENSED=False`
- `THREE_D_CONTINUOUS_WEYL_POWER_LICENSED=False`
- `EVOLVING_WEYL_POWER_LICENSED=False`
- `ACT_LIKELIHOOD_LICENSED=False`
- `OBSERVATIONAL_CLAIM_LICENSED=False`

The next milestone, if pursued, must be separately preregistered and independently validate a CLASS-residual radial representation on new direct k holdouts. The historical FAIL must remain preserved.