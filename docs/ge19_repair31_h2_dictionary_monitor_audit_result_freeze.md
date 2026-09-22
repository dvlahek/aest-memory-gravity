# GE19 Repair31 Repair30 H2 dictionary and monitor audit — result freeze

## Status

Classification:

`GE19_REPAIR31_REPAIR30_H2_DICTIONARY_AND_MONITOR_AUDIT_COMPLETE`

Repair30 remains historical FAIL and is not relabelled.

Repair31 performed no H2 reintegration and no H4/Z21 solve.

## Local output provenance

JSON:
- SHA-256: `569ad9b16a26989fd8a9c9c02d83b77eb4afe23d9962fa56b87166d78d0ea33a`
- bytes: `138692`

FULL log:
- SHA-256: `569ad9b16a26989fd8a9c9c02d83b77eb4afe23d9962fa56b87166d78d0ea33a`
- bytes: `138692`

Runner log:
- SHA-256: `39382281bd351b70674ff3ab86f8c2f05506ab0a018d8afeb97ec0c1c98f14c3`
- bytes: `152019`

The JSON and FULL log are byte-identical.

## Main findings

### 1. State time-resolution failure is a normalization artifact

The Repair30 max-per-field metric was dominated by the near-zero algebraic dust-density coordinate.

For C_star:
- N: 0.0018212508453560893
- S: 0.0016023936729083245
- u: 0.0003954887833823978
- varphi: 0.0005414034137820233
- T: 0.003267950727445378
- delta_varrho: 0.9549690055364972

However:
- full six-field global relative L2 = 0.0003954887835507251
- dynamic S,u,varphi,T global relative L2 = 0.0003954887833823978

Across all C:
- six-field global max = 0.00039552726534112983
- dynamic global max = 0.0003955272651727121

Thus the reported ~0.96 Repair30 state mismatch is not a global state divergence.

### 2. The old near-null rule does not classify the Repair30 shift samples as near-null

Repair31 reproduces:
- Nt128 active Linf = 0.9401687948604716
- Nt128 active L2 = 0.28831056827587886
- Nt64 active Linf = 0.8163314614242385
- near-null count = 0

The worst sample is at the first time node:
- C_min
- m=3
- ln(a)=-0.916290731874155
- absolute residual = 8.98647881622435e-23
- local row scale = 9.55836746055586e-23

Thus the Repair21/22 near-null rule alone does not rescue the frozen Repair30 shift gate.

At the global operator scale, however, the solved Repair30 state has:
- shift absolute L2 = 5.097286506902184e-21
- shift / operator scale = 2.3720316679601383e-17

The large local backward error is therefore a local cancellation/normalization symptom, not a large absolute violation of the complete operator scale.

### 3. Reduced versus R2 parent chi11 mismatch is highly coherent

Across C and k:
- max relative L2 = 0.40411983475468916
- minimum shape cosine = 0.9990744283033375
- mean best scale reduced->parent = 1.6724183017901846
- relative scale dispersion = 0.00017451675436083828
- max post-fit relative L2 = 0.04301495914632063
- initial-surface mismatch <= 2.134061856895356e-22

This is a systematic amplitude-level discrepancy, not random resolution noise.

### 4. Operator localization exposes an approximately exact factor-two source mismatch

For the saved Repair30 reduced solution under the unchanged Repair30 RHS:
- aether LHS/RHS = 0.9999961596269547
- scalar LHS/RHS = 1.0000041795942898
- aether global residual = 1.7539579225407827e-05
- scalar global residual = 2.789223283211168e-05

So the Repair30 solution solves its own frozen H2 source.

For the mapped Repair29B R2 parent under the same reduced operator and same RHS:
- aether LHS/RHS = 2.0002926513914643
- scalar LHS/RHS = 2.0004430883773
- aether relative residual = 0.50007317924901
- scalar relative residual = 0.5001332047550441

This is the central Repair31 result.

### 5. Repair31 automatic route must not be interpreted literally

The artifact reports `dominant_main_equation = lapse` and routes to a metric/matter closure audit because the lapse RHS is exactly zero, making its residual normalization return relative=1 by construction.

The relevant lapse absolute residuals are:
- solved state: 1.5714421044921866e-10
- R2 reference: 1.5580577383921985e-08

By contrast, the physically driven H2 rows are aether and scalar, where the R2 parent is almost exactly a factor two above the frozen Repair30 source.

Therefore the route string
`REFERENCE_DEFECT_DOMINATED_BY_METRIC_OR_MATTER_REDUCTION_CLOSURE_AUDIT_REQUIRED`
is retained as historical Repair31 output but is not adopted as the scientific diagnosis.

### 6. Drude and GE05 internal normalizations are clean

- GE05 symbolic partial_px identity: PASS
- GE05 symbolic partial_r identity: PASS
- 1024-node Drude weight sum = 1 exactly
- 2048-node Drude weight sum = 1 exactly
- all quadrature weights positive
- no fitted normalization adopted

The v0.22/v0.39 force builders and the frozen CLASS tangent patch independently use the preregistered physical forcing
`dE'/deta|0 = -a Q B_raw/(2 K_B)`.

Thus Repair31 does not support blaming the positive-Drude quadrature or the CLASS force-file amplitude.

## Scientific diagnosis

The leading hypothesis is now a relative raw-residual normalization mismatch between:

- the GE06 memory-off reduced operator convention used for `L_total`, and
- the separately generated GE05 memory Euler-Lagrange residual used for `M1`.

This relative normalization is invisible in source-free H1 and in blocks built entirely inside one generator. H2 is the first place where GE06 `L` and GE05 `M1` are inserted into the same reduced equation, so an overall residual-convention mismatch can first become observable here.

The empirical factor-two signature is strong but is not yet adopted as a correction factor.

## Next licensed step

Repair32A must be an outcome-independent normalization-dictionary audit.

It must derive the exact conversion between the physical CLASS E-equation memory forcing and the GE06 raw aether/scalar Euler-Lagrange residual convention, and separately compare that conversion with GE05 raw M1.

No H2 rerun is licensed before this exact dictionary factor is derived.

## Canonical status

**Repair31 = COMPLETE diagnostic audit. Repair30 remains historical FAIL. Reduced Z11 remains NOT CERTIFIED. H4/Z21 remains BLOCKED. The leading blocker is a candidate factor-two GE06/GE05 raw-residual normalization mismatch, to be derived exactly in Repair32A before any source change.**
