# Full-J direct-CLASS spectral-fringe parameter-factorization audit

Date: 2026-09-13

## Motivation

The completed bridge-identity R1 audit classified

`FULLJ_CLASS_FRINGE_BRIDGE_PARAMETER_DEPENDENCE`.

It closed the requested-k-list, history-order, common-time, and tagged/Fourier extraction hypotheses. The entire direct-versus-historical mismatch appears when switching from the R3/direct CLASS parameter family to the historical bridge CLASS parameter family. After excluding `k_output_values` and the intentionally different `P_k_max_h/Mpc`, the audit found zero unexpected parameter-dictionary differences.

This audit factorizes those two remaining differences without changing any science grid, AeST equation, cosmological parameter, redshift, or prior classification.

## Frozen inputs

Preserve:

- corrected CLASS head `e85808324f51fc694d12e3ed7439552a3c3f9540`;
- runtime `source/aest_memory.c` SHA `4d5ab5dc7066d4880f06fcfc731d6534ed0ff992e3cc15fb473dddccb25a594f`;
- memory off (`aest_memory_enabled=no`, `aest_eta=0`);
- the same 15 anchor wavenumbers and redshifts `[6,5,4,3,2,1.5,1,0.5,0.2]`;
- historical bridge list `target_modes(k)` independently for each anchor;
- locked B1 direct-parameter bridge-list array and B2 historical-parameter array from bridge-identity R1;
- all prior formal classifications unchanged.

## Factorial parameter corners

For each anchor use the exact historical bridge mode list and its already-certified positional target index.

Define:

- **C00**: R3/direct parameter family, R3 15-significant-digit `k_output_values`, `P_k_max_h/Mpc=0.30`.
- **C01**: same as C00 but replace only `k_output_values` by the exact historical bridge serialization.
- **C10**: same as C00 but replace only `P_k_max_h/Mpc` by the historical value `2.0`.
- **C11**: both historical settings together. The complete dictionary must equal the historical bridge parameter dictionary after string-normalized comparison.

No other parameter may differ among corners.

The audit must also parse both k strings and report the maximum physical `|delta(k/h)|` introduced by the serialization change.

## Predeclared gates

Use the inherited bridge-identity tolerances:

- global relative L2 <= `2e-5`;
- maximum per-anchor relative L2 <= `5e-5`.

Material dependence means failure of either tolerance.

### PF-G1 frozen baseline reproduction

C00 must reproduce locked B1 within the inherited tolerances.

### PF-G2 historical-corner reproduction

C11 must reproduce locked B2 within the inherited tolerances, and C11 must be dictionary-identical to the historical bridge parameter family.

### PF-G3 serialization-only isolation

Compare C01 with C00 and report global and maximum per-anchor relative L2, together with maximum physical serialized-k displacement.

### PF-G4 Pkmax-only isolation

Compare C10 with C00 and report global and maximum per-anchor relative L2.

### PF-G5 factorial closure

Compare C11 with C10 and C11 with C01. These differences quantify the same two factors on the opposite factorial edge. The two-factor corner C11 must reproduce the previously observed B2-versus-B1 discrepancy to within the inherited tolerances.

## Predeclared classifications

After PF-G1 and PF-G2 pass:

1. serialization material, Pkmax not material -> `FULLJ_CLASS_FRINGE_K_SERIALIZATION_DEPENDENCE`;
2. Pkmax material, serialization not material -> `FULLJ_CLASS_FRINGE_PKMAX_DEPENDENCE`;
3. both individually material -> `FULLJ_CLASS_FRINGE_MULTI_PARAMETER_DEPENDENCE`;
4. neither individually material but C11 materially differs from C00 -> `FULLJ_CLASS_FRINGE_PARAMETER_INTERACTION_DEPENDENCE`;
5. C11 does not reproduce B2 or C00 does not reproduce B1 -> `FULLJ_CLASS_FRINGE_PARAMETER_FACTORIZATION_INCOMPLETE`;
6. no material dependence despite the locked B1-B2 mismatch -> `FULLJ_CLASS_FRINGE_PARAMETER_FACTORIZATION_INCONSISTENT`.

## Physics rule

This is a numerical-cause audit, not a physics discovery test. In particular, `P_k_max_h/Mpc` is a CLASS numerical/output-range control. If changing it materially alters a fixed low-k linear perturbation history, the fine-k node locations are not physically certified. A subsequent convergence scan in `P_k_max_h/Mpc`, with matched GR control, is required before equation-level or observational interpretation. Historical R3 and extractor classifications remain unchanged.