# GE19 — science-first decision on the first nonzero full-CLASS Weyl eta tangent

**Date:** 2026-11-13  
**Repository branch:** `physics-first-gravitational-elasticity`  
**Evidence:** [original researcher WSL force-run log](../results/ge19_one_forced_tangent_20261113_runner.log) (427 bytes, SHA-256 `5efb80f8fc7acdc4a53cfb8e1d181b9cbd55548de078c1f304c1877dc5502f63`, Git blob `3576e0178c0337dc354e6870d66bae646833515b`), plus [prior completed baseline/null inspection](../results/ge19_existing_traces_inspection_20261113.log). The generated `GE19_ONE_FORCED_TANGENT_SCREEN.json`, `force_single.log`, and full numerical CSV have not yet been received for independent archival review.

## Fixed calculation and directly supported numbers

Original frozen Exp benchmark; separate source-locked original v077 CLASS with v019/v019j bath and action-motivated quarter candidate; Newtonian gauge, all native CLASS radiation and matter hierarchies, original selected `k = 0.06732117 Mpc^-1 = 0.1 h/Mpc`, `z=0.5`; tangent at `eta=0`, with original early adiabatic/no-free-bath prescription. Original 141,494-row baseline history starts at `a=2.251984948309577e-6` and ends at `a=1`. A native zero-source null has 13 sampled outputs all exactly zero. The only new numerical execution is **one** native full-hierarchy forced eta-tangent pass using the existing primordial `Bchi0(t,k)` history, without re-running baseline or scanning parameters.

The researcher's successful run prints:
- `max_abs_Bchi = 7837.613561516323` (maximum in the historical trace, not a pointwise value at z=0.5)
- `W0(z=0.5) = 0.07009097715416947` (from previous independent passive inspection; transfer normalization, **not** a physical matter-memory amplitude)
- `W1 = dW/deta|eta=0 = 1.8390770226818281e-09`
- `W1/W0 = 2.6238427503110188e-08` **per unit eta**.
- The ratio is independently arithmetically consistent with the quoted W0 and W1.
- `GE19_SINGLE_NATIVE_CLASS_FORCE_FINISHED` and `GE19_PHYSICS_GO False`.

The **first-order extrapolation** (not an independently computed finite-eta result) is
`[W(eta)-W0]/W0 approx eta * 2.6238427503110188e-08`.
For *illustration only*, at `eta=0.01`, `delta W approx 1.8390770226818281e-11` and `delta W/W0 approx 2.623842750311019e-10`. This is numerically tiny at this fixed k and z. It must not be misrepresented as a DES sensitivity bound; the physical range for eta, k dependence, integrated observer projection, primordial-normalization uncertainties, nonlinear finite-eta behavior and covariance have not been established.

## Physical interpretation

**Positive, limited advance:** There is a **nonzero calculated first-order response** in the source-locked, actually compiled and executed *native full-CLASS perturbation implementation*, sourced by a full early-time bath history. This passes a meaningful existence/sensitivity diagnostic beyond the former z=19-reset pressureless dust proxy. The default earlier reduced proxy ratio `~1.95e-20` is **not directly comparable** in physical normalization, initial history or matter/radiation content; a 12-order ratio comparison must not be advertised as a validated amplification of the physical model.

**Negative, decision-relevant evidence:** The observed **fractional response per unit eta** at the fixed observationally relevant k and z is roughly `2.6e-8`. Even granting an illustrative small `eta=0.01`, the leading relative response is only `2.6e-10`. This does not support a strong lensing-detectability or observation/discovery claim in the *current frozen Exp candidate*. A one-point transfer ratio can neither establish a survey signal-to-noise nor rule out responses elsewhere in k and z. The large historical peak `Bchi` alone is not an observable amplification.

**Still unverified:** numerical convergence of W1 under independently refined source sampling and solver; validation of interpolation error, potential cancellations and absolute error floor; genuinely action-derived source coefficient and full Einstein plus scalar Ward constraints for both baseline/tangent; next-order adiabatic/memory primordial IC and eta-independence; CLASS approximation-switch derivative maps and transfer-to-physical galaxy–Weyl observer; DES bias/IA/photo-z/covariance. The null output being exactly zero in 13 samples is a useful homogeneous-control check, not a rigorous all-interval Ward identity. In particular the current `eta=0` derivative and single runtime do not justify a statistical detection.

## Decision: STOP the automatic CLASS patch / numerical sweep cycle

The researcher explicitly called out the repetitive engineering loop. After achieving this first actual nonzero forced response, **stop automatic additional CLASS runs, retries, candidate parameter changes and GE19 micro-PASS projects**. Archive results and label the one-point full-CLASS derivative as `GE19_PROVISIONAL_FULL_CLASS_WEYL_TANGENT_NOT_PHYSICS_CERTIFIED`.

Research priority should shift to a concise theoretical/scientific audit of whether a *physically admissible original action + retarded Ward-consistent adiabatic mode* exists and can couple the memory bath strongly enough to a gauge-invariant observable. If this cannot be established from existing analytic evidence, publish only the justified theoretical/conditional memory result, not a claimed survey discovery. Do not use DES observations to tune the original source coefficient or `eta`. The only optional **administrative** follow-up is to read and archive the already generated local JSON/`force_single.log` and exact CSV; this requires **no new CLASS execution**.

**Final status at this checkpoint: calculated native full-CLASS W1 nonzero but tiny; full physical observability/GR consistency uncertified; no DES detection; no additional numerics authorized by this decision.**
