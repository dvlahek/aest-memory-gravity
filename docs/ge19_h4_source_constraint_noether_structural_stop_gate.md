# GE19 H4 source/constraint structural stop gate — post-Repair44

## Decision

This document closes the isolated interpolator and one-source-row
diagnostic sequence at valid Repair44. It is an **audit plan and claim
boundary**, not a new science PASS, implementation preregistration or
permission to tune the H4 equation against its shift residual.

The next task is a structural compatibility audit of the *complete*
inhomogeneous H4 source with the unchanged linearized GE06/GE07/Lambda
operator. A new integrated science Z21 reclosure is not licensed until
the full-source compatibility audit is completed and separately frozen.

## What is actually established

Repair41 directly reconstructed M1 and GE06 Q-cross target source pieces
on Nt382 and Nt763; their aggregate source norms satisfied the inherited
parent time-resolution gates.

Repair42 applied the direct target corrections selectively to frozen
Repair37 PCHIP total source. Both combined variants exceeded the
unchanged 1e-6 active-shift target.

Repair43 localized the large mixed-representation sensitivity to the
two GE06 constraint-source rows together.

Repair44 split the rows and found the independent shift source row0
closer to the full two-row result at both direct resolutions. Crucially,
changing row0 alone leaves the propagated Z21 exactly unchanged.
At the registered m8/early-window hotspot, the shift residual change
equals minus the source-row0 change with a complex identity defect of
exactly zero. This is the algebraically expected result of changing
an independent constraint RHS without changing the state.

**Neither the native fine-grid GE06 physics nor a full common-grid H4
source has been shown to violate a constraint by this intervention.**
Repair41's global relative-L2 resolution controls also do not by
themselves certify the row0 source at 1e-6 of the very small local
constraint scale.

## Structural audit object

Use the original H4 equation, unchanged:

`L_total Z21 = -2Q_total(Z10,Z11) -2DY2[Z10;Z11] -2M1[Z20,q20] -2M2[(Z10,q10),(Z10,q10)]`.

The current Repair37 source dictionary contains all six pieces:

1. `2Q_GE06_cross`;
2. `2Q_GE07_cross`;
3. `2Q_Lambda_cross`;
4. `2DY2`;
5. `2M1_GE05_mapped`;
6. `2M2_GE05_mapped`.

Each contains six main-source rows and two constraint-source rows.
The two GE06 constraint rows are *shift source row0* and
*anisotropy source row1*. The shift row is independently checked, while
the anisotropy row contributes to canonical algebraic elimination.

Any compatibility statement must treat the complete dictionary and
the parent equations together. The precise Noether identity, its
normalization and its parent-equation residual terms must be derived
from the frozen covariant action and checked symbolically or
independently; they must not be guessed from a numerical desired result.

## Required audit sequence

### A. Analytical identity and source dictionary

Derive the relevant reduced perturbative diffeomorphism/Noether
identity through the H4 order from the *same* action and variable
conventions used by GE06, GE07, GE05, Lambda and the nonanalytic Y2
completion. Identify exactly which parent H1/H2/background/bath
equations enter the identity, including their equation-sign and
factor-of-two conventions.

Freeze a term-by-term source-row dictionary from all six pieces
to the full H4 main and constraint rows and to every parent-equation
residual appearing in the identity.

A formally zero source identity may be claimed only after the
necessary on-shell parent assumptions, time/spatial derivative
operations and boundary terms have been stated explicitly.

### B. One common parent/time representation

Evaluate the full H4 dictionary using mutually compatible Z10,
Z20, q10, q20 and Z11 fields and derivatives on one common time
representation, with the unchanged spatial/Fourier conventions.
In particular, do not mix a direct fine-grid GE06 shift source with
the frozen coarse-grid source and state from unrelated other pieces.

Compare the full assembled shift source to its action/Noether-derived
expression, including the source terms carried by GE07, Lambda,
DY2, M1 and M2. Include independent direct checks of the registered
C_max/beta0/m8/it3 point and the entire original active window.

Before any propagation, check the identity residual as an absolute
complex quantity and relative to the *original*, unchanged local
backward-error scale; report parent-equation residual contributions
separately. Global whole-source relative L2 is not a substitute for
the local shift-row check.

If parent/time resolution is insufficient at the local scale,
stop as unresolved and use a separately preregistered,
targeted *common-grid* refinement. Do not fit or smooth an isolated
constraint row toward zero.

### C. Integrated science reclosure (only after A/B)

If the full source passes its independently frozen structural audit,
preregister a single integrated H4/Z21 science reclosure with:

- the unchanged H4 equation and original 1e-6 active-shift threshold;
- unchanged projected p0 and specified physical homogeneous-mode
  choice;
- an independently generated time-control solution;
- the frozen canonical operator, full main and constraint-source
  dictionary and original active mask;
- separate absolute-residual, backward-error denominator,
  convergence and parent-residual diagnostics.

A genuine PASS must satisfy the *whole* preregistered science gate.
An attractive particular interpolant or a source-row cancellation
in isolation is not sufficient.

If the structural identity fails, record the specific failed
algebraic/source/parent relation, revise that theoretical component
under a separate version, and retain immutable Repair37--Repair44
history. The earlier results cannot be relabelled.

## Explicitly forbidden continuation

- Repair45 as another preferred PCHIP/Akima interpolant comparison.
- Injecting only GE06 shift row0 to manipulate the active-shift metric.
- Relaxing 1e-6 or masking the early-window m8 sample post hoc.
- Treating Repair41's aggregate relative-L2 resolution result as a
  certified local shift-constraint accuracy guarantee.
- Using lensing, CMB or any observational comparison to tune the
  theory or select the numerical source.

## Deliverable and exit criterion

The next deliverable is an independently inspectable **H4 source
compatibility certificate or a localized structural FAIL**. Its
derivation, frozen inputs, residual dictionary and claim boundary
must be sufficient to reproduce the conclusion without running
another sequence of selective H4 source patches.

Until then, window-local particular Z21 is NOT CERTIFIED and lensing
is blocked.
