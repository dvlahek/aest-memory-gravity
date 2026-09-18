# NL1C7B4 Repair14a — decoded v0.19 static-semantics parser repair

## Status

Pre-data / pre-run implementation repair preregistration.

Repair14 attempt01 is frozen as

`NL1C7B4_REPAIR14_IMPLEMENTATION_FAIL`

at result-freeze commit

`381bc30d6266b12c3590b9138c9f1a7bc07de9cc`.

The only failed gate was Repair14 G4, specifically the static check intended to establish that the frozen v0.19 effective-density line contains no explicit `E_aest` or `chi_aest` contribution.

## Exact failure mechanism

The frozen file `v019/apply_patch_v019.py` contains the replacement C block as the Python variable `new_stress`.

Its embedded C newlines are represented by literal `\n` escape sequences inside the Python string literal. A scan over physical Python source lines therefore sees the entire replacement block as one source line.

Repair14 attempt01 tested each physical source line containing `ppw->delta_rho +=` for the absence of the substrings `E_aest` and `chi_aest`. That test is representation-dependent and false because those substrings occur later in the same Python string literal, not in the decoded C `delta_rho` statement.

## Sole allowed change

Repair14a may change only the G4 static parser:

1. parse `v019/apply_patch_v019.py` with Python `ast`;
2. find the assignment to the variable `new_stress`;
3. require exactly one such assignment;
4. obtain its literal string value with `ast.literal_eval`;
5. split the decoded string into actual C lines;
6. select decoded C lines containing `ppw->delta_rho +=`;
7. require the active AeST effective-density line
   `ppw->delta_rho += rho_dark*y[ppw->pv->index_pt_delta_cdm];`;
8. require that no decoded C `ppw->delta_rho +=` line contains `E_aest` or `chi_aest`.

The original four positive static semantics checks remain unchanged.

## Frozen science path

Every other Repair14 expression and test remains byte-for-byte inherited in semantics from attempt01:

- exact symbolic E/X gauge identities;
- exact B3 first variations;
- density-Q closed form;
- six analytic scale/grid profile pairs;
- `1e-12` E-sector/K-correction cancellation limit;
- 54 corrected diagnostic cases;
- lambda values `1,1/2,1/4,1/8`;
- gated slope interval `[1.8,2.2]`;
- Hamiltonian and momentum slope gates;
- eta=0;
- all scale/grid/Y/beta cases retained;
- no official state write.

The already observed Repair14 attempt01 numerical payload may be reproduced, but no threshold may be changed in response to it.

## Additional Repair14a gate

Repair14a must verify the historical attempt01 output hash

`ea4f1d28330b22d6d3d64f5f6f6d27b3646a889fbee9cffc37c4e789282f0966`

and exact historical gate pattern:

- G1 true
- G2 true
- G3 true
- G4 false
- G5 true
- G6 true
- G7 true
- G8 true.

## Terminal classifications

PASS:

`NL1C7B4_REPAIR14A_DENSITY_Q_BRIDGE_OMISSION_IDENTIFIED`

only if:

- the decoded-string parser repair passes;
- all inherited Repair14 gates pass;
- the attempt01 hash/gate pattern is preserved;
- no science semantics changed.

Otherwise:

`NL1C7B4_REPAIR14A_IMPLEMENTATION_FAIL`.

A PASS identifies the finite-gradient density-Q bridge omission only. Historical Repair14 attempt01 remains an implementation failure and historical B4 remains FAIL.

Any actual corrected C7A/Repair08 state requires a separately preregistered next repair.
