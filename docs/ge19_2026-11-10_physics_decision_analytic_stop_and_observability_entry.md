# GE19 — Physics decision, analytic-series closeout and observability entry

**Date:** 2026-11-10. **Project:** GravitationalElasticy / AeST Memory Gravity, branch \`physics-first-gravitational-elasticity\`. This is an explicit **research decision / theory-status freeze**, not a newly performed numerical analysis or a detection. The user agreed to stop incremental LW audits and shift to one decisive source-to-physical-observable decision. This note does **not** amend frozen original CLASS code, previous observations or historical files.

## 1. The actual last researcher run and immutable evidence

The original user-provided GE19 LW33 outputs are now archived byte-for-byte:
- [\`results/ge19_lw33_action_scalar_current_class_residual_20261110_r1.json\`](../results/ge19_lw33_action_scalar_current_class_residual_20261110_r1.json): 3451 bytes, SHA-256 \`b5dbfc9f0d5bcc8493d3fccb4ab0adcd731b6c5f0d7e07b0849cd986c41e62e6\`, Git blob \`d5c7bfd1038fee1ae63c1d03cd10802fc3744b47\`.
- [\`results/ge19_lw33_r1.log\`](../results/ge19_lw33_r1.log): 395 bytes, SHA-256 \`d2abce733a6ec53b61219a3105e5ba15e030ceb583f6ad01f993503f300ec3db\`, Git blob \`fe74b75a76cb5c0ec6c8fc62859a527797ff5fcc\`.

Both blobs have been fetched from GitHub after upload and match the *original* uploaded files. Genuine WSL outputs: **19/19 symbolic checks PASS, 7/7 source locks PASS**; classification \`...PASS_OLD_HALF_SOURCE_INCOMPATIBLE_CONDITIONALLY_FULL_3PLUS1_OPEN\`; \`GE19_LW33_PHYSICAL_OBSERVER_READY False\`. The repeated LW32 JSON and log are SHA-identical to their already-archived originals.

The LW33 derivation is documented in [the source audit](ge19_lw33_exact_scalar_action_to_CLASS_offshell_source_decision_2026-11-10.md). It is **post hoc mathematical analysis**, not an independent blind test. This closeout is an interpretation of that evidence, not a new symbolic PASS.

## 2. Decisive theoretical finding: a conditional source-normalization defect

For the original analytic GE06 AeST + GE05 NL0B **reduced longitudinal linear model**, the full scalar-current equation is an exact off-shell combination of the original CLASS-form effective-fluid density and aether evolution residuals, phase/density dictionary residuals and their time derivatives, plus

\[
\boxed{\mathscr S_{\phi,\mathrm{leftover}}=\frac{a\eta k^2B_\chi}{2}(1-4\gamma).}
\]

When **the same original reduced-action dictionary** and its evolution equations are enforced, generic nonzero memory source forces **\(\gamma=1/4\)**. The original frozen \`v019j/apply_memory_patch.py\` instead uses **\(\gamma=1/2\)**, so its source is not compatible with **that exact restricted action-to-CLASS dictionary** without a further independently action-derived source/field redefinition.

The old \(-\eta Q B_\chi/2\) is a **raw off-shell NL0B bath Euler force**; dividing by the full AeST kinetic Hessian \(2K_B\) yields the local E-evolution quarter coefficient. LW30 and LW31 established the original reduced action's Hamiltonian, momentum and scalar traceless Einstein equations, and LW32 demonstrated regular algebraic elimination of the unit-aether and auxiliary-normal constraints. These findings strengthen the restricted bridge; they do **not** by themselves establish complete full covariant 3+1 Einstein–AeST–nonanalytic-Y + standard-species equivalence.

**Research decision:** the old half-source CLASS response is a frozen **implemented model response**, not a certified physical \(\partial_\eta W\). **Do not** claim it is an observed detection, and do **not** silently repair original source code or post-hoc rescale its output by 1/2 (coupled evolution and normalization must be checked). Treat the *quarter* as the **leading action-consistent candidate**, not as yet a fully certified CLASS version.

## 3. Analytic campaign STOP: no LW34/LW35-style proliferation

The standalone, piecemeal symbolic campaign **ends at LW33**. Further generic Noether, scalar flux or free parameter sweeps are not a meaningful substitute for a one-time complete action-to-observable calculation. Historical results remain frozen.

The one permitted **physical acceptance gate**, specified in terms of deliverables rather than another series of tests, is:

**Input:** original *full* covariant quadratic scalar action (including unit timelike aether and auxiliary vector constraints, lapse/shift, spatial shear, time/space gauge, original nonanalytic-Y directional treatment and relevant standard fluid species).

**Output:** one coherent map from its complete Euler/constraint equations to the original CLASS states \((\delta_A,\theta_A,\alpha_A,E_A,\Phi,\Psi)\), including a verified physical \(\eta\) normalization of *all* source rows; explain whether the original state/dictionary survives and whether \(\gamma=1/4\) or an action-derived companion term is required. Check full constraint propagation and causal auxiliary initialization. A partial source match or arbitrary added density/velocity correction is a **FAIL**, not permission to start CLASS.

**Two outcomes only:**
- \`PHYSICS_GO\`: full map closes, source normalization is uniquely determined; version a **separate** action-consistent model candidate and run one tiny zero-\(\eta\)/source/constraint regression, then physically normalize the matter–Weyl tangent.
- \`PHYSICS_BLOCK\`: full map remains missing or contradictory; stop before observational significance and report the exact theorem/implementation mismatch. The *reduced* quarter-coefficient result itself is a viable transparent theoretical consistency paper.

Do not infer the full 3+1 outcome from the restricted 1+1/3D-scalar proofs. This is **one bounded decision**, not a promise that the full theory must pass.

## 4. Locked first observable once and only once the source is physical

The existing observational pivot is **DES Y3 galaxy–galaxy lensing**, not reopening failed full cosmic-shear LOS. Keep the source/foreground pairing previously frozen based on *geometry*, not fitted detection statistics:
- primary **MagLim lens bin 4 × source bin 4**;
- geometry-control **MagLim4 × source bin 3**;
- \(\ell=100,150,200\) as early *support checks only*, not final measurement bins or declared detections.

Original user WSL [LW22 evidence](ge19_lw22_actual_wsl_geometry_result_freeze_and_lw23_physics_gate_2026-11-10.md) gives full lens-weighted source efficiencies \(0.15070638368625014\) (source 4) and \(0.056512701041848266\) (source 3), ratio approximately \(2.667\). These are **geometric kernel efficiencies**, *not* memory shear amplitudes, observed significance, or lensing data.

Pre-register and implement only after \`PHYSICS_GO\`:
1. The **fully coupled causal** Einstein–AeST+NL0B and standard-species transfer for \(D_m(k,z)\), \(W=(\Phi+\Psi)/2\), and physically calibrated \(\partial_\eta P_{D_mW}(k,z)\) in one gauge/sign/unit normalization. *Do not* substitute the old numerical \(\lambda\) amplification as physical \(\eta\).
2. The real lensing forward: full MagLim4/source3,4 n(z), projected \(k,z\) support and radial quadrature, \(C_\ell^{g\kappa}\), measured DES binned \(\gamma_t(\theta)\) windows/scale cuts, actual covariance and tracer/IA/photo-z/magnification/calibration nuisance design. Avoid artificial zero padding or extrapolation across the original LW03 radial-failure or LW05 LOS-limited domains.
3. **First an Asimov nuisance-marginal identifiability test**, then—and only if physics and projection pass—test real observed shear. The memory signal must survive marginalization against galaxy bias, evolving dark-energy/background and a **predefined restricted instantaneous alternative**. Generic Weyl evolution and geometry-vs-matter tests already exist in the literature; neither alone constitutes a uniquely new memory signal.
4. Memory-specificity: identify physically allowed **different past histories** producing the same relevant instantaneous state but distinct causal auxiliary stress, then demonstrate an actually identifiable distinction in the coupled observables. A kernel dependence on past alone is not sufficient for observational uniqueness.

In formal notation, with physically computed data derivative \(t=\partial_\eta\mu\), nuisance columns \(D=\partial_\nu\mu\), released covariance \(V\), and fixed nuisance-prior precision \(P_\nu\), the first discriminability gate is

\[
F_{\eta\eta}^{\mathrm{marg}}=
t^TV^{-1}t-
(t^TV^{-1}D)(D^TV^{-1}D+P_\nu)^{-1}(D^TV^{-1}t).
\]

An amplitude-only tangent collinear with an unconstrained galaxy-bias direction gives zero Fisher information: report \`NO_IDENTIFIABLE_SIGNAL\` rather than forcing a detection. The original LW08 matter–Weyl *differential* tangent is UNRESOLVED (large cancellation and 74–199% disagreement among numerical amplifications), so present evidence does **not** yet support a distinctive memory signature.

Relevant prior [LW20 forward/forecast specification](ge19_lw20_des_y3_ggl_weyl_observer_forecast_route_2026-11-10.md) and [LW08 unresolved novelty test](ge19_lw08_observational_novelty_collision_and_relative_tangent_2026-11-09.md) are preserved; no new DES measurement was accessed in this closeout.

## 5. Single project-level status and termination rules

| Item | Decision |
|---|---|
| LW01–LW33 separate analytic test campaign | **STOP / archived**, final researcher LW33 PASS |
| Reduced-action scalar/aether E-source | **QUARTER physically selected within the frozen reduced dictionary** |
| Original v019j half-source physical equivalence | **NOT certified; conditionally inconsistent** |
| Full covariant action-to-CLASS source/constraint map | **OPEN; one decisive gate** |
| Separate action-consistent model candidate | **Not yet promoted to physical production** |
| LW22 DES Y3 source geometry | **PASS (geometry only)** |
| Fully physical \(\partial_\eta P_{D_mW}\) | **BLOCKED pending physical map** |
| Real DES Y3 \(\gamma_t\) likelihood / nuisance-identifiable memory | **NOT YET ATTEMPTED / NO DETECTION** |

**Go/no-go:** If the one joint full-action map does not close, no more rescue numerics: report the limited physics theorem and physically unresolved observation. If it closes, permit one constrained first observational forward campaign, then honor \`NO_IDENTIFIABLE_SIGNAL\` if the nuisance projection removes the effect.

This replaces the old practice of creating another symbolic LW stage after every PASS. No numerical job is started here; original historical branches, model and scientific results are untouched.
