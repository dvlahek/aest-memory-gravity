# NL1C6D2N corrected CLASS baseline — first result

Status: **LOCKED HISTORICAL RESULT**.

Classification produced by the first preregistered implementation:

```text
NL1C6D2N_CORRECTED_CLASS_BASELINE_FAIL
```

Result-producing repository head:

```text
6f23f2e5c8aa62baf05ad6ad58b98154b4c05b33
```

The run is interpreted as an **instrumentation/provenance FAIL, not a physical corrected-model FAIL**.

Observed gates:

```text
B1 clean-build provenance: FAIL
B2 background charge health: FAIL
B3 baryon continuity: PASS
B4 finite linear trajectory: PASS
B5 native/dense closure: PASS
B6 TT/TE/EE spectra health: PASS
```

The physical/numerical outputs that were actually evaluated were healthy:

```text
max baryon continuity normalized L2 = 1.1886887877887696e-06  (gate 2e-3)
max dense/native d_b relative L2    = 1.3548654267873833e-07  (gate 2e-4)
max dense/native t_b relative L2    = 3.2998201762131005e-07  (gate 2e-4)
all six dense trajectories finite   = true
TT/TE/EE finite through ell=2500    = true
```

## Why B1 failed

The first implementation required the SHA-256 of the **final fully patched CLASS** `source/aest_memory.c` to equal the SHA-256 of the repository's base corrected v0.19 source file.

That identity is not a valid provenance condition because later frozen patches in the already declared patch chain modify the installed source after the v0.19 source has been copied. The run itself records:

```text
pinned CLASS git head = e85808324f51fc694d12e3ed7439552a3c3f9540  [correct]
repository corrected source SHA = 89eb9ce01c957b0c6fcdc1a761e21983a2676acd96662f9069d0cbbc1b519fb6 [correct]
final patched CLASS source SHA   = 4d5ab5dc7066d4880f06fcfc731d6534ed0ff992e3cc15fb473dddccb25a594f [different after later patches]
```

R1 therefore retains the exact pinned CLASS-head and repository-source checks, but tests the final installed source by explicit corrected/old formula anchors rather than by an invalid whole-file SHA equality.

## Why B2 failed

The first implementation expected `classy.get_background()` to expose custom AeST fields `Q`, `KQ`, `p`, `w`, and `cad2`. The actual public background dictionary exposes standard fields including `z`, `H`, and `(.)rho_cdm`, but not those custom internal AeST columns.

The frozen AeST implementation reuses the CLASS CDM background slot for the effective AeST dark density. R1 therefore checks the same physical background law independently by:

1. reading public `(.)rho_cdm(a)` from the corrected CLASS trajectory;
2. calibrating the corrected analytic Exp `K(Q)` to the `a=1` effective-dark density;
3. enforcing `K_Q(a)=I0/a^3` with the already frozen corrected inverse map;
4. reconstructing `rho_AeST(a)=[Q K_Q-K]/3`;
5. comparing the reconstructed density to CLASS `(.)rho_cdm(a)` on `0<=z<=6`.

The R1 density agreement gate is `1e-10`, equal in strictness to the original charge-spread gate. No physical parameter or cosmological parameter changes.

## Historical boundary

This first FAIL remains immutable. R1 is a technical instrumentation remediation and receives a distinct result label. No memory, nonlinear branch selection, refit, or likelihood was inspected in the failed first baseline.
