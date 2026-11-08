# GE19 — R37 original projected initial parents versus Cr12abR2; late shift drift (read-only)

**2026-11-08.** Action/Noether source-frozen branch `physics-first-gravitational-elasticity`. No new H4 integration; no source changes.

**User evidence**: `GE19_H4_R37_INITIAL_PARENT_SLIM.zip` (SHA256 `25ce7899f2eafc22bd99da77dcde90fd2bc1950d0f4490111613390148cb2b04`) compared to already independently verified `GE19_H4_INITIAL_CONSTRAINT_EVIDENCE.zip` (SHA256 `f2977ca9157bd574178313e4d616adbb28a5d0e349e43f532752e39c8658ecc1`). R37 full JSON SHA exact `da8f2f00c22c866ec3f82381d23f69bf036e630fe2a29c5c44657984b760f61a`; **full original R37 NPZ** not uploaded, so its stated SHA `572d8937c1d742b10da66e34cc076377c1b2feb20b8f72eb25c3eaf31a59829f` is **not independently checkable from the slim extract**. Cr12abR2 four constituent original files pass 4/4 independent archive manifest SHA-256 and byte checks. Independently saved read-only report `GE19_H4_R37_INITIAL_PARENT_AUDIT_20261108.json` SHA `8c97641cfcf9f580058c398a8eaffbc7a18750c43752f4883e4538fc37bdab92`, and methodological Markdown SHA `c68d76f990605a9476be46a5278c9527e68e5d5e420f34c50da3545e9d5ffec0`.

## Actual initial condition (Cstar primary Nt128, 40 modes, three betas)

R37 original `solve_controls.primary_per_C.C_star.per_mode[].initial_boundary` supplies for **all 120** beta-mode pairs the original initial Repair18 projected-momentum and independent lapse/shift diagnostics. Maximum across the 120:

```text
projected momentum scaled residual  2.220513810852107e-16
initial lapse backward error        1.9435452879063478e-16
initial shift backward error        2.699647501850278e-16
reported initial anisotropy error   2.1806576726723925e-16
initial algebraic relative error    1.973675540862791e-16
```

Full original `Cr12abR2.final_shift_metric[:,:,0]` equals R37 `initial_boundary.shift_backward_error` **bitwise for every 120 pair**, max abs difference exactly `0.0`. Original R37 initial `C_star_projected_p0_primary` (shape `(3,40,4)`) is **bitwise identical across all 3 beta values** despite source main scalar beta differences. Original action Cr12abR2 driver `run_final_h4` explicitly inherits R37 p0 and builds `y0=(0,0,0,0,p0)`, no retuning. Its `exact_source_functions` uses base R37 interpolated source at x0 because `stage_locator(x0)=-1`; first Radau stage is 0.0019264282810503852 after x0. Original stage rights `stage_x[1::2]` equal all original x[1:] **bitwise**. Thus **the large later shift drift is not an unprojected initial shift boundary residual** in the executed discrete H4 scheme.

**Critical independence limitation:** `Repair18.evaluate_candidate` constructs `w=WY@y+WR@source`, where the Noether-regularized `Calg` **uses anisotropy** as one algebraic row. The reported tiny anisotropy is therefore **a reconstruction consistency check, not an independent test of an alternate provisional trial state** or the true physical H4 parent. Do not overstate the result as proof of every initial full Euler/Noether constraint. The earlier speculative anisotropy trial mismatch formula has not been evaluated and does not explain the measured later drift.

## Source-change arithmetic at actual hotspot (m40, beta-index 1, original time-node 24)

From the Cr12abR2 original `.npz`:
```text
peak frozen active normalized shift = 1.217597084500816e-6 (>1e-6)
peak |raw signed shift Euler row residual| = 2.7770076323913147e-13
peak cancellation-safe normalization scale = 2.2807278924536992e-7
```

At the **same** original right Radau stage `stage_x[47]=x[24]`, new fine48 M2 minus original historical M2:
- Main M2 stage `||new-old||_2 / max(||new||_2,||old||_2)=4.3928223810500074e-6` globally, hotspot max component difference `1.1707838085300944e-13`.
- Constraint M2 stage global relative L2 `2.3660537091520757e-5`, hotspot max component difference `3.069767746884057e-15`.

These signed stage M2 differences are valid original-file arithmetic, **not a physical shift error bound**: a complete coupled parent/action source response and phase are required to relate them to raw signed `E_b`. Other stage replacements Q6/Q7/QL/DY2 are not contained in the R37 slim package; Cr12abR2's source code consumes additional frozen Cr12u NPZ data not yet inspected here. The code defines a source prescription at x0 and the fixed Radau stages; it does **not independently certify a single differentiable physical H4 source across all x**. Do not insert such stage-only data directly into a continuous Noether differential identity and claim on-shell Ward.

## Additional measured beta-invariant failure masks

For the three original beta values (1.0, 0.5, 0.1), the full original Cr12abR2 active-mask arrays are **bitwise identical**, with **2,650 active cells per beta**. Their >1e-6 failing mask arrays are also **bitwise identical**, **816 failing cells per beta** (21 output modes), despite nonidentical scalar main source terms. Among active cells, the **maximum difference of normalized shift metrics** between beta1 and beta0.5 is `6.608821575625581e-16`, and between beta1 and beta0.1 it is `5.844222404193661e-16`. This is strong evidence that **the sampled normalized active H4 failure is beta-independent in the tested family**; it does **not** identify which sector is responsible or imply absence of beta effects in the theory.

## Original classifications and science decision

- `R37`: `GE19_REPAIR37_CANCELLATION_SAFE_FD8_H4_Z21_RECLOSURE_FAIL`, initial backward errors small but final active shift gate FAIL.
- `Cr12abR2`: `GE19_D55CR12ABR2_FINE48_M2_COHERENT_CSTAR_H4_IMPLEMENTATION_FAIL`; both frozen **M2 nested decrease** implementation flags false, and separate active shift `1.217597084500816e-6` vs unaltered `1e-6` FAIL.
- `Cr12ad`: independently frozen closeout last-best `1.2175965417947408e-6`, **H4 campaign CLOSED**, cannot be reclassified using R37 initial metrics.
- `D55Cr11f`: original continuum GE05 bath H-channel PASS for C_star primary six modes only, not a full H4 parent Ward.

**This newly uploaded R37 evidence materially disfavors the earlier initial-shift root-cause hypothesis.** One physical task now remains: obtain independently signed complex raw shift `E_b`, full `E_L` with momentum derivative, parent `R_parent`, lower-boundary `B_parent` and common physical clock, covering at least x0→x24 original m40 and the failure window (modes 2..40), with verified FD4/FD8/roundoff/error. Do not invert absres/scale to infer phase, nor use the algebraically enforced anisotropy to pretend independent parent on-shell. If the original source packages lack these fields, explicitly record the missing evidence rather than launch more small numerical repair variants. **No new H4 source, coefficient fit, relaxed `1e-6` target, new Z21 certification or lensing claim.**
