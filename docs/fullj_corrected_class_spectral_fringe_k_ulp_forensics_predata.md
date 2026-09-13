# Full-J direct-CLASS spectral-fringe k-ULP forensic audit

Date: 2026-09-13

## Motivation

The completed parameter-factorization audit classified

`FULLJ_CLASS_FRINGE_K_SERIALIZATION_DEPENDENCE`

with all five preregistered gates passing. Changing `P_k_max_h/Mpc` from 0.30 to 2.0 has exactly zero effect at the frozen anchors, while replacing the 15-significant-digit `k_output_values` serialization by the historical high-precision serialization reproduces the entire previously observed direct-versus-bridge mismatch. The maximum physical displacement between the parsed k lists is only `4.996003610813204e-16 h/Mpc`.

This audit does not reinterpret the historical R3 failure or the bridge-identity result. It asks a narrower numerical question: is the serialization dependence localized to the target k token itself, and is the resulting sensitivity generic to CLASS or specific to the AeST linear sector?

## Frozen inputs

Preserve without modification:

- corrected CLASS head `e85808324f51fc694d12e3ed7439552a3c3f9540`;
- patched runtime `source/aest_memory.c` SHA `4d5ab5dc7066d4880f06fcfc731d6534ed0ff992e3cc15fb473dddccb25a594f`;
- memory off (`aest_memory_enabled=no`, `aest_eta=0`);
- `P_k_max_h/Mpc=0.30` throughout this audit;
- the frozen 15 anchors and redshift grid `[6,5,4,3,2,1.5,1,0.5,0.2]`;
- the completed parameter-factorization C00 and C01 arrays;
- no change to any earlier gate or classification.

## Part A: target-token versus list-context factorization

For each of the 15 anchors, construct the historical bridge k list and let `p00` be the R3/direct parameter set with 15-significant-digit serialization. Let `p01` denote the same parameter set with the full historical serialization.

Evaluate two new hybrid serializations:

- **T**: keep all tokens from `p00` except the target token, which is replaced by the corresponding historical token from `p01`;
- **O**: keep the target token from `p00`, but replace every other token by its historical representation.

The target positional index is the already certified historical positional index.

### UF-G1 provenance and parent identity

The parent parameter-factorization result must be `FULLJ_CLASS_FRINGE_K_SERIALIZATION_DEPENDENCE`, diagnostic-complete, with all PF gates true. C00 and C01 must be finite and have the frozen shape `(15,9)`.

### UF-G2 target-token locality

If the serialization effect is local to the target token, then:

- T must reproduce C01 with global relative L2 <= `2e-5` and maximum per-anchor relative L2 <= `5e-5`;
- O must reproduce C00 within the same tolerances.

Failure classifies the effect as list-context dependence and blocks a target-ULP interpretation.

## Part B: representable-double ULP ladder

Use the following five anchors, fixed before this run:

`[0.10125, 0.10250, 0.16250, 0.16500, 0.19750] h/Mpc`.

They include one low-sensitivity control (`0.10250`) and four serialization-sensitive anchors spanning all three windows.

For each selected anchor:

1. Parse the target token from the 15-digit and historical serializations as IEEE-754 binary64 values in `1/Mpc`.
2. Build an ordered ladder of representable binary64 values covering both endpoints and one ULP beyond each side. If this contains more than 17 values, use at most 17 bit-uniform representative values while always retaining both endpoints and both outward neighbors.
3. Keep every non-target token fixed to the 15-digit baseline serialization.
4. Evaluate the target history at every ladder point for:
   - AeST (`aest_enabled=yes`),
   - matched GR (`aest_enabled=no`).
5. Record `phi`, `psi`, and `W=phi+psi` at the frozen redshifts. For AeST, also record `alpha_aest` and `E_aest` when present.

### UF-G3 matched-GR ULP continuity

For every selected anchor, the maximum relative L2 change of GR `W` over the entire ULP ladder relative to the 15-digit endpoint must be <= `1e-6`.

Failure classifies the effect as generic CLASS/grid ULP sensitivity.

### UF-G4 AeST material ULP sensitivity

At least one selected anchor must show AeST `W` relative L2 change > `5e-3` over the ULP ladder relative to the 15-digit endpoint.

This is diagnostic only. Passing it does not establish physical sensitivity because the mechanism may still be a discrete implementation branch or an ill-conditioned numerical mode.

### Step-concentration diagnostic

For each selected anchor, sort ladder points by IEEE-754 bit pattern and compute relative L2 changes between adjacent AeST `W` histories. Define

`jump_concentration = max(adjacent_change) / sum(adjacent_changes)`.

Values near one indicate a step-like transition concentrated in one representable-double interval; distributed values indicate sensitivity spread across several adjacent ULPs. This quantity is reported but is not itself a gate.

## Predeclared classifications

Priority order:

1. UF-G1 fail: `FULLJ_CLASS_FRINGE_K_ULP_FORENSICS_INCOMPLETE`.
2. UF-G2 fail: `FULLJ_CLASS_FRINGE_K_LIST_CONTEXT_DEPENDENCE`.
3. UF-G3 fail: `FULLJ_CLASS_FRINGE_GENERIC_CLASS_ULP_SENSITIVITY`.
4. UF-G2 and UF-G3 pass, UF-G4 pass: `FULLJ_CLASS_FRINGE_AEST_ULP_SENSITIVITY_CERTIFIED`.
5. Otherwise: `FULLJ_CLASS_FRINGE_AEST_ULP_SENSITIVITY_NOT_REPRODUCED`.

## Physics rule

No outcome of this audit licenses a new-physics claim or restores the historical R3 support classification. If AeST-specific ULP sensitivity is certified while GR remains continuous, the next step must identify if the amplification is caused by a discrete AeST/CLASS branch, an exact-k lookup, or a genuinely ill-conditioned linear mode. Equation-level dispersion interpretation is deferred until that source-level or stability mechanism is resolved.