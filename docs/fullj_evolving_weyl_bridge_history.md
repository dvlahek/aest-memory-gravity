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
- `ef8f75d605ba7d69a61c0fffb55abaf2700d1fca` — local runner; branch HEAD at launch

The repair audit was launched locally by the author on 2026-09-12 and is currently running. Target classification:

`FULLJ_METRIC_PROJECTION_PHYSICAL_KMASK_REPAIR_PASS`

Critical checks are that the repaired mask is exactly identical to the historical R2 mask in the original R2 geometry, and that A/B repeated-box field, tagged-response, and tagged-power differences collapse to numerical precision under the same physical cutoff.

Scope remains narrow until the run finishes: this repair does not by itself license continuous/evolving 3D Weyl power, line-of-sight lensing, ACT likelihood use, or observational claims.
