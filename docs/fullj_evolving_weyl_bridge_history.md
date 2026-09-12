# Full-J evolving Weyl bridge history

This file records the main validation decisions and their scope. Historical FAIL classifications remain historical results and are not rewritten after later repairs.

## 2026-09-12 — box-doubling failure diagnosed as a physical-k projection bug

The stochastic tagged box-doubling audit failed despite clean solver and constitutive health. The failure pattern was traced to the evolving-Weyl metric projection mask inherited from the original R2 bridge:

```python
modes = np.minimum(np.arange(nx), nx - np.arange(nx))
mask = (modes >= 1) & (modes <= NMAX)
```

with `NMAX=32`. In the original R2 geometry, `kF/h=0.01`, so this index cutoff had the physical meaning `0 < k/h <= 0.32`. Later tagged-mode calculations changed the box size and therefore changed `kF`, but the literal index cutoff `n<=32` remained fixed. The physical metric-projection cutoff therefore changed with box size.

This exactly explains the audit pattern. For geometry A (`kF/h=0.005`) the old cutoff is `k/h<=0.16`; for geometry B (`kF/h=0.0025`) it is `k/h<=0.08`. Nodes for which both geometries included the mode, or both excluded it, agreed, while nodes included in A but excluded in B failed. The observed node pattern was therefore diagnostic of a box-dependent implementation artifact rather than solver instability or evidence against the retained nonlinear dynamics.

The historical box-doubling FAIL was locked in commit `f600b7e594e57ffbbd0f3044aa2fbf4da20e942b` and remains a FAIL.

A preregistered repair was then added that preserves the original physical meaning of the R2 projection cutoff, `0 < |k|/h <= 0.32`, independently of box size. No science threshold or physical parameter was relaxed. The repair chain is:

- `5313c734238363d1c2985446eddd35c2846e7aeb` — preregister physical-k repair audit
- `cda8dd02facbb2d2f7bed9b5d0d6f821b9aeab2e` — implement physical-k metric projection repair
- `29321d1d9c473a16363bedcd5ca9b46adb510963` — repaired A/B audit implementation
- `ef8f75d605ba7d69a61c0fffb55abaf2700d1fca` — local runner used for the repair audit

The repair audit was launched locally by the author on 2026-09-12.

## 2026-09-12 — physical-k metric projection repair PASS

The completed repair audit is classified

`FULLJ_METRIC_PROJECTION_PHYSICAL_KMASK_REPAIR_PASS`.

The repaired mask is exactly identical to the historical R2 mask in the original R2 geometry: `mismatch_count=0` with physical cutoff `k/h<=0.32`. Therefore the original R2 result is not altered by the repair.

The audit tested `k/h={0.06,0.095,0.16,0.195}`, two frozen Gaussian backgrounds, both tag signs, and both geometries A (`kF/h=0.005`, `NX=256`) and B (`kF/h=0.0025`, `NX=512`), for 32 repaired runs total. All 32/32 runs were finite and all eight preregistered gates passed.

Key numerical results:

- canonical residual max `1.8097824858362603e-14`
- broadband saturation max `4.288739111533391e-05`
- Hamiltonian residual max `1.8533251051449448e-16`
- momentum residual max `1.5283987431465636e-16`
- doubled-box repeat field max `8.079165690921655e-12`
- direct A/B field relative-L2 max `2.0111915213430488e-12`
- tagged-response global relative-L2 `6.6732360256820115e-15`
- tagged-power global relative-L2 `6.2923105961568036e-15`
- per-k power relative-L2 max `2.939406053885455e-14`
- per-z power relative-L2 max `1.4505558403050873e-14`

The A/B differences therefore collapse to numerical precision when the metric projection is defined by a fixed physical-k cutoff. This validates the diagnosis that the preceding box-doubling FAIL was caused by a box-dependent implementation artifact.

Result lock: `docs/fullj_metric_projection_physical_kmask_repair_result.md`, created in commit `20151ab785e923de20d720f3fdd8890576b6cc05`.

Validated scope:

- `METRIC_PROJECTION_PHYSICAL_KMASK_REPAIR_VALIDATED=True`
- `STOCHASTIC_TAGGED_BOX_DOUBLING_INVARIANCE_REPAIRED=True`

Still not licensed:

- bounded continuous tagged-power interpolant
- continuous/evolving 3D Weyl power
- line-of-sight lensing
- ACT likelihood use
- observational claims

The next bounded step is a repaired tagged-power regression/power-lattice rerun with the physical-k metric projection used consistently in both geometries. Only after that should the 3D/isotropic Weyl-power lift be reconsidered.
