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

## 2026-09-12 — repaired tagged power-lattice regression preregistered

After the physical-k repair PASS, the next bounded milestone was fixed before new repaired power-lattice data were inspected. The goal is to retest the two historical power-lattice failure gates under the validated physical-k metric projection without immediately paying for a full from-scratch production campaign.

The regression uses 108 new integrations:

- 12 repaired Stage-A overlap runs at `k/h={0.060,0.095,0.160}` to empirically certify limited historical Stage-A reuse;
- 32 repaired Stage-A high-k runs at `k/h={0.165,0.170,0.175,0.180,0.185,0.190,0.195,0.200}`;
- 64 fresh repaired Stage-B runs at 16 half-lattice controls selected by the unchanged historical adaptive power-curvature algorithm.

The overlap certification is explicitly empirical. Although target modes at or below `k/h=0.16` were themselves inside the historical Stage-A integer mask, the repaired metric projection also retains higher metric-correction harmonics through `k/h=0.32`. Therefore historical low-k responses are not assumed identical by construction. They may be reused for this regression only if the preregistered overlap response/power thresholds pass. A final production campaign must recompute the complete lattice under the repaired mask regardless of the regression outcome.

All historical PL-G6/PL-G7 numerical thresholds remain unchanged. A PASS licenses only the repaired regression diagnostic, not the bounded production interpolant, 3D/evolving Weyl power, LOS lensing, ACT likelihood use, or observational claims.

Regression preparation chain:

- `bef9e1304ebd838954635e624290696f08d33293` — initial regression preregistration draft
- `46397135c70f20ddb88900016d66836f66495b0e` — regression implementation
- `dde7ae43d974451b49f73df7473025812e906e83` — prereg wording clarified before data; no grid, threshold, equation or classification rule changed
- `49f4c25988ee8e1a28e08280eb27f58ecff82826` — implementation wrapper locks the clarified preregistration
- `a7278040ee869c5b7f30f4fcd73451004a4a0efd` — local 108-run regression runner

Target classification:

`FULLJ_STOCHASTIC_TAGGED_POWER_LATTICE_KMASK_REGRESSION_PASS`.

If the regression passes, the next milestone is a full from-scratch repaired power-lattice production campaign with no stale historical response reuse. If it fails, preserve the FAIL and diagnose the repaired direct controls without relaxing gates.

## 2026-09-13 — repaired tagged power-lattice regression FAIL

The 108-run repaired regression completed and is formally classified

`FULLJ_STOCHASTIC_TAGGED_POWER_LATTICE_KMASK_REGRESSION_FAIL`.

All 108/108 integrations were finite. KR-G1 through KR-G5 pass. The overlap reuse certification is at numerical precision, with response global relative L2 `8.5653e-15` and power global relative L2 `1.6815e-14`. Solver, metric, constitutive, and power-algebra diagnostics are all clean: canonical max `1.8981e-14`, broadband saturation max `4.3492e-05`, Hamiltonian max `1.8575e-16`, momentum max `1.7753e-16`, and tagged-power identity residual `1.5145e-17`.

Only the two radial adequacy gates fail:

- KR-G6: repaired half-lattice power interpolation accuracy
- KR-G7: unresolved selected-interval power spike veto

The late-time power interpolation errors are localized in time: `E_P=0.02938` at `z=1`, `0.09314` at `z=0.5`, and `0.25928` at `z=0.2`. The median over all redshifts remains only `0.00331`.

Two direct spike-veto failures remain. The dominant one is `k/h=0.0975`, `z=0.2`, where direct power `0.00934086` lies between endpoint powers `0.000744306` and `3.81243e-05`, giving ratio `12.5498`. The second is `k/h=0.1975`, `z=1`, ratio `2.13737`.

The complete NPZ was then inspected without changing any frozen gate. The two direct Gaussian backgrounds agree on the repaired half-lattice response at approximately `4.19e-08` global relative L2 and on power at approximately `3.31e-08`; at `z=0.2` the corresponding differences are about `1.27e-07` and `1.22e-07`. The response is almost purely real, with half-lattice `||Im T||/||Re T||≈4.99e-09` globally and `1.51e-08` at `z=0.2`. The remaining late-time radial structure is therefore not explained by B2 sampling noise or phase projection.

At `z=0.2`, direct signed responses near the strongest structure are `T(0.095)=+0.027282`, `T(0.0975)=+0.096648`, `T(0.100)=+0.0061745`, `T(0.1025)=-0.0018173`, `T(0.105)=-0.015708`, `T(0.1075)=-0.021294`, `T(0.110)=+0.117090`, `T(0.1125)=-0.032562`, and `T(0.115)=+0.075590`. Additional direct sign-changing structure occurs near `0.155--0.170`, and high-k interpolation errors near `0.190--0.200` materially contribute to the `z=0.2` error norm.

Result lock: `docs/fullj_stochastic_tagged_power_lattice_kmask_regression_result.md`; formal FAIL locked in commit `9f5218629901643574373e32c84d137c9cda2494`, with NPZ forensic addendum in commit `97d72584aa5ed26028e8e60e1e6ef0ccd1919a21`.

Interpretation: the physical-k repair solved the box-dependent implementation defect, but the repaired `Delta k/h=0.005` observable-facing power lattice remains genuinely under-resolved at late time within the frozen tagged construction. Do not relax the power gates and do not start the full repaired production lattice yet.

The next bounded diagnostic should be a local quarter-lattice refinement at `Delta k/h=0.00125` in the already half-lattice-complete windows `0.0925--0.1125`, `0.155--0.170`, and `0.190--0.200`. Only 18 quarter-offset nodes are new, so B2 and both signs require 72 integrations. This test should determine if the direct repaired response converges to a resolved oscillatory radial function before any full production campaign is attempted.

## 2026-09-13 — local quarter-lattice win-or-stop test preregistered

The bounded 72-run local refinement is now frozen before any quarter-lattice result is inspected.

Three repaired-regression windows are tested: `0.0925--0.1125`, `0.155--0.170`, and `0.190--0.200`. Their complete existing local parent spacing is `Delta k/h=0.0025`. Eighteen new quarter-offset nodes are inserted at `Delta k/h=0.00125`, using `kF/h=0.00125` and `NX=1024`; the box and grid size are both doubled relative to the previous half-lattice geometry, preserving physical `dx`.

The parent regression NPZ is frozen by SHA256 `83fb7462ec970bfef953e3804d11a81fd5843745347fe77c318c9e39b8e6e82d`. No parent response is regenerated or modified inside this diagnostic.

The absolute power gates remain the prior thresholds: maximum local-window/redshift power L2 `<=0.05`, median `<=0.025`, peak-normalized error `<=0.10`, plus the same factor-2 unresolved-spike veto. An additional refinement gate requires the `0.0025` prediction to be no worse than the repaired `0.005` prediction at every redshift and strictly better at `z=0.5` and `z=0.2`.

The stop rule is explicit: if the quarter-lattice test still materially fails the interpolation or spike gate, do not automatically continue to `Delta k/h=0.000625`; pivot to a targeted resonance/response-origin audit of the offending window(s).

Preparation chain:

- `3d309b51e44eb38569a7be263dbb14963ba4bd17` — preregister local quarter-lattice test
- `8ad36d4df4b4d20c981f7b475e558a5a1400a354` — implement 72-run quarter-lattice diagnostic
- `4a26681601da46d52aaa1b2105138024a1005f31` — local runner with parent-NPZ hash and physical-mask guards

Target classification:

`FULLJ_STOCHASTIC_TAGGED_POWER_QUARTER_LATTICE_PASS`.
