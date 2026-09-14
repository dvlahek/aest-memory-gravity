# Stable AeST growth–Weyl memory R4 — pre-result repair 2

Date: 2026-09-14
Branch: `fullj-evolving-weyl-bridge`

This note is fixed before any successful R4 physical finite-eta run.

The second R4 attempt completed the frozen-parent provenance check and the certified stable-chi patch audit, then exited before `STABLE_AEST_GROWTH_WEYL_MEMORY_R4_SINGLE_CHANNEL_SOURCE_PASS` and before any R4 eta run.

The cause is infrastructure-only. The frozen parent commit `e85808324f51fc694d12e3ed7439552a3c3f9540` already carries one historical v0.19w diagnostic statement

```c
dy[pv->index_pt_E_aest] += aest_tangent_external_force(k,tau);
```

from the earlier variational-diagnostic development line. With all `AEST_TANGENT_*` environment variables unset, that historical diagnostic hook contributes zero and is not part of the physical finite-memory closure. However, the R4 source-topology audit intentionally requires no diagnostic forcing statement in the final disposable R4 source so that the claimed physical single-channel topology is literal.

Allowed repair: in the disposable R4 CLASS source only, after copying the frozen parent and applying the certified stable-chi patch, require exactly one occurrence of the historical diagnostic hook and remove exactly that one statement. Do not modify the runtime helper implementation, the physical memory closure, any bath equation, any coefficient or sign, any eta value, observable, threshold, anchor, redshift, or R4 science gate.

After the repair the final R4 source must contain:
- exactly one `Bchi_aest *= pba->aest_eta;`,
- exactly one `E_rhs_aest -= 0.5*Q_aest*Bchi_aest;`,
- zero `dy[pv->index_pt_E_aest] += aest_tangent_external_force(k,tau);` statements,
- the certified stable residual marker and `chi=Q*s` source.

The first and second failed R4 attempts remain pre-result technical failures. The R4 preregistration commit `f742cfb33bd00ec8e1b637d7d1e7201d464fc433` remains unchanged.