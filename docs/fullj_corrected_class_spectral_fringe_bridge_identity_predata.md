# Full-J direct-CLASS spectral-fringe bridge-identity audit

Date: 2026-09-13

## Motivation

The completed extractor-equivalence audit classified

`FULLJ_CLASS_FRINGE_EXTRACTOR_MISMATCH_CERTIFIED`

with all five preregistered gates passing. The raw direct paths agree (`E1~E2`), the historical bridge path reproduces its frozen reference exactly (`E3=E4`), but the direct and bridge values differ materially and increasingly at late time. The historical R3 `NUMERICAL_CONTROL_FAIL` remains unchanged.

Before interpreting this discrepancy as equation-level physics, the present audit decomposes the bridge extraction chain into the remaining technical layers that can still mimic a structured physical mismatch.

## Frozen inputs

Preserve without modification:

- corrected CLASS head `e85808324f51fc694d12e3ed7439552a3c3f9540`;
- patched runtime `source/aest_memory.c` SHA `4d5ab5dc7066d4880f06fcfc731d6534ed0ff992e3cc15fb473dddccb25a594f`;
- memory forcing off (`aest_memory_enabled=no`, `aest_eta=0`);
- the same 15 anchors and redshifts `[6,5,4,3,2,1.5,1,0.5,0.2]`;
- locked R3 direct arrays and locked extractor-equivalence arrays;
- no change to any R3 gate, threshold, k value, CLASS source equation, cosmological parameter, or prior classification.

## Technical hypotheses to discriminate

For each frozen anchor `k/h`, let the historical bridge list be exactly `target_modes(k)`: the six baseline modes plus the target when it is not already one of them.

Evaluate:

- **B0**: locked R3 direct 15-list value at the anchor.
- **B1**: corrected CLASS run using the R3/direct parameter construction but the exact historical bridge k-list. Select the target history by its *reported physical k*, not by list position, and evaluate `phi+psi` at the frozen scale factors.
- **B2**: corrected CLASS run using the exact historical bridge parameter construction and the same bridge k-list. Again select the target history by reported physical k and evaluate at frozen scale factors.
- **B3**: from the same B2 run, select the history at the historical positional index implied by the requested bridge list and evaluate at frozen scale factors.
- **B4**: from the same correctly k-matched B2 history, evaluate `phi+psi` at the historical bridge `tau_check` values instead of directly at frozen scale factors.
- **B5**: locked historical bridge/tagged extractor E3 from the completed extractor-equivalence NPZ.

The audit must record the actual reported k of every returned history for every bridge-list run.

## Predeclared gates

All relative-L2 tolerances below are fixed before running.

### BI-G1 provenance and frozen identity

Exact runtime provenance, frozen arrays, 15 anchors, redshift grid, and historical classifications must match. All newly evaluated arrays must be finite.

### BI-G2 bridge-list invariance under direct parameters

B1 must reproduce B0:

- global relative L2 <= `2e-5`;
- maximum per-anchor relative L2 <= `5e-5`.

Failure identifies a requested-k-list dependence not covered by the earlier 51-versus-15 R3 control.

### BI-G3 parameter-construction identity on the same bridge list

B2 must reproduce B1:

- global relative L2 <= `2e-5`;
- maximum per-anchor relative L2 <= `5e-5`.

The audit must separately report static parameter-dictionary differences after excluding `k_output_values` and the intentionally different `P_k_max_h/Mpc` values. Any additional difference is provenance-significant.

### BI-G4 history-order identity

For every bridge-list run, the positional history used historically must report the same physical k as the requested target to absolute tolerance `5e-12 h/Mpc`. B3 must also reproduce B2 within the same global/per-anchor tolerances.

Failure certifies a history-order/index mapping defect.

### BI-G5 bridge time-coordinate identity

B4 must reproduce B2:

- global relative L2 <= `2e-5`;
- maximum per-anchor relative L2 <= `5e-5`.

Also report maximum `|a(tau_bridge)-a_target|` and maximum conformal-time offset between the bridge `tau_check` and the target-history `tau(a_target)`.

Failure identifies the historical common-time mapping as the source of the mismatch.

### BI-G6 basis/Fourier extraction identity

If BI-G2 through BI-G5 pass, B5 should reproduce B4 because the tagged +/- cosine/Fourier normalization is algebraically an identity for the target modal CLASS coefficient:

- global relative L2 <= `2e-5`;
- maximum per-anchor relative L2 <= `5e-5`.

Failure identifies the tagged basis/Fourier extraction layer itself.

## Predeclared classifications

Priority order:

1. If BI-G1 fails: `FULLJ_CLASS_FRINGE_BRIDGE_IDENTITY_INCOMPLETE`.
2. If BI-G2 fails: `FULLJ_CLASS_FRINGE_BRIDGE_KLIST_DEPENDENCE`.
3. If BI-G3 fails or unexpected parameter-dictionary differences are present: `FULLJ_CLASS_FRINGE_BRIDGE_PARAMETER_DEPENDENCE`.
4. If BI-G4 fails: `FULLJ_CLASS_FRINGE_BRIDGE_HISTORY_MAPPING_DEFECT`.
5. If BI-G5 fails: `FULLJ_CLASS_FRINGE_BRIDGE_TIME_MAPPING_DEFECT`.
6. If BI-G6 fails: `FULLJ_CLASS_FRINGE_BRIDGE_BASIS_EXTRACTION_DEFECT`.
7. If BI-G1 through BI-G6 all pass while the previously certified B0-versus-B5 discrepancy remains material: `FULLJ_CLASS_FRINGE_BRIDGE_TECHNICAL_CAUSE_NOT_FOUND`.

The last classification is the only outcome that licenses immediate equation-level mode/dispersion analysis of the discrepancy itself. It still does not establish new physics.

## Physics rule

A structured formal failure may be treated as a physics clue only after all relevant technical identities are independently closed. If this audit localizes the discrepancy to k-list dependence, parameter construction, history mapping, time mapping, or tagged extraction, the discrepancy is numerical even if its k/z pattern looks physical. If all such identities close and the direct AeST-versus-GR spectral structure remains independently converged, the next test must derive a mode/dispersion prediction and validate it on held-out k values before any new-physics claim.