# GE19 H4 structural Stage C — Y-action density versus GE19 source conventions

## Classification

`GE19_H4_STAGEC_RAW_Y_VOLUME_FACTOR_ESTABLISHED_GLOBAL_NORMALIZATION_OPEN`.

This is a **valid restricted symbolic/convention audit**, not a
complete all-sector H4 source certificate, H3/H4 state solve or physics
correction. A full global NL0C-to-GE06 action prefactor is not
independently fixed by this audit.

Frozen preregistration:
`ge19/h4_structural_stage_c_predata_y_raw_ge19_conventions.json`,
blob `cc43754e92eef83d025475a9c5f893aa6dd81ce4`.

Audited implementation:
`ge19/h4_structural_stage_c_y_raw_ge19_convention_audit.py`,
blob `80e79006613f6067926adf39995fa08bffe51534`.

Successful GitHub Actions:
- run `35982602472`;
- job `107577815881`;
- conclusion `success`;
- marker `GE19_H4_STAGEC_Y_RAW_GE19_CONVENTION_AUDIT_PASS`;
- artifact ID `10800767849`, name
  `ge19_h4_stagec_y_raw_ge19_convention_audit`.

Frozen result JSON:
- path `results/ge19_h4_stagec_y_raw_ge19_convention_audit.json`;
- bytes `4759`;
- SHA-256
  `76f6af0ec5f765c2cf6cf9f33a6cb35d3bd0b8dbfbdec18832955cd8cf5ccb55`.

All frozen-source bindings, exact branchwise symbolic identities,
and source-assembly convention controls pass.

## Exact raw-versus-physical geometric relation

Write the frozen NL0C action-density sector, omitting its
still-unbound *relative global action prefactor*, as

`L_Y = -(2-K_B) c_beta N L R^2 |X|^3`,

where

`c_beta = 2/[3(1+beta)a0]`,
`X=sinh(u)(phi_t-b phi_x)/N + cosh(u) phi_x/L`,
`g=Q u10+phi10_x/a`.

Define the physical-space flux coefficient already present in
`y2_source`:

`kappa=2(2-K_B)/[(1+beta)a0] = 3(2-K_B)c_beta`.

For both strict-sign branches, extended continuously across
`g=0`, the raw reduced second directional Euler rows are:

`E_phi,raw^(20) = +2 a^2 kappa partial_x(|g|g)`,

`E_u,raw^(20) = -2 a^3 Q kappa |g|g`.

The frozen GE19 `y2_source` uses

`y2_code = kappa/a * partial_x(|g|g)`.

Consequently, exactly,

`E_phi,raw^(20) = 2 a^3 y2_code`.

The matching *candidate* same-volume-normalized Y aether
coefficient would be

`Y2_u = -Q kappa |g|g`.

Its eta-tangent, again as a **conditional action-to-GE19
mapping** with unchanged background Q, is

`DY2_u = -2 Q kappa |g10|g11`.

The same `a^3` geometric ratio applies to the scalar
eta-tangent source.

The action-level aether/scalar-flux identity

`E_u^(2,Y) + a Q F_phi^(2,Y) = 0`

holds identically. That algebraic relation alone does not fix the
overall relative normalization of the NL0C term inside the full
frozen GE06 action.

## Exact source-code convention control

`GE06` constructs its raw analytic action and Euler partials
with the `N L R^2` density. Its
`assemble_ga_local` applies time/spatial derivatives to those
raw partials, with no `a^{-3}` division.
`main_and_constraints` stacks raw aether and scalar rows
without an `a^{-3}` division.

Both H3 source constructors instead add

`rhs[3] += -2*y`

directly after `rhs=-qmain`, where `y` is the physical
divergence `y2_source`. The H4 constructor analogously adds
`main[3]=-2*fft_low(dy)` and leaves the Y aether row empty.

This is an **explicit convention/row coverage discrepancy** in
the frozen implementation relative to the action-density
dictionary. There is no hidden `a^{-3}` conversion in the
audited source-assembly functions.

## Strict scientific boundary

Do not directly modify the frozen H3/H4 RHS by multiplying the
scalar Y term by `a^3` or adding the candidate aether term.
The exact relative global action normalization (including the
GE06 GR+AeST sector conventions) has not been independently
derived and versioned here.

A common constant sector prefactor cannot by itself eliminate
a time-dependent geometric `a^3` ratio, but the full field
equations may carry a separately documented common row
normalization. The next audit must bind those conventions
from the *same frozen action*, not from the desired Repair37
constraint residual.

Existing Repair22/Repair32B--32C certifications remain
immutable for the previously implemented equations. They
cannot certify a newly completed variational NL0C parent
without a separately preregistered appropriate H3/H2
reclosure. Repair37 remains immutable science FAIL.
Repair38--Repair44 remain diagnostics.

No physical eta or observational inputs were used.
Window-local particular Z21 is NOT CERTIFIED;
lensing remains blocked.

## Next action

Derive the global NL0C/GE06 action prefactor and the exact
time-dependent Euler-row normalization from the frozen
full action. Freeze the complete Y scalar+aether source
dictionary, then separately preregister parent
compatibility and new integrated H4/Z21 science checks.
Do not resume selective GE06 source patches.
