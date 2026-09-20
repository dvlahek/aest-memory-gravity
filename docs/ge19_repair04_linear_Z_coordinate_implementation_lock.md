# GE19 Repair04 linear-Z-coordinate implementation lock

## Status

Locked before the first GE19 Repair04 science execution.

Historical GE19 Repair03 remains

`GE19_REPAIR03_WINDOW_RETARDED_REDUCED_H3_Z20_PARTICULAR_FAIL`.

Its Stage-A numbers are frozen but implementation-contaminated by the wrong stable-GE06 background coordinate in the active linear operator.

## Parent result freeze

File:

`docs/ge19_repair03_reduced_h1_result_freeze.md`.

Frozen blob:

`6542c64474361c734be9c9a217a719978afd478b`.

Freeze commit:

`ed177f28f72289d3389e17c3b2b0da0f42a1177a`.

## Repair04 preregistration

Commit:

`90d5131f8c835dea066aa78e0992b94af7462b5a`.

File:

`ge19/repair04_predata_linear_operator_Z_coordinate_and_provenance.json`.

Frozen blob:

`c16cb534db9215a057ffff93ab005f44284901ca`.

## Exact implementation defect

The Repair03 stable GE06 signature is

[
(a,dot a,Z_b,ldots).
]

The active H1/H3 linear operator nevertheless used

`Qb=bg["Q_action"][:,None]`

as its third GE06 argument.

This is dimensionally and numerically wrong for the stable re-lambdified generator.

The intended background coordinate in the frozen window is approximately

[
Z_b=4.45	ext{--}4.69,
]

while

[
Q_{m action}=O(10^{-4}) {m Mpc^{-1}}.
]

Repair04 changes the active linear operator only to

`Zb=bg["Z_action"][:,None]`

followed by

`vals6=(aa,adot,Zb,...)`.

The physical `Q_action` remains unchanged where the theory genuinely requires Q, notably

[
X_1=Q,u_1+partial_xphi_1/a.
]

## Secondary provenance repair

Repair03 also included an implementation-added condition

`GE15_background_mode_mismatch_max <= 1e-10`

inside `provenance_pass`.

This quantity compares independently interpolated copies of the same background carried inside six k-mode perturbation traces.

The Repair03 value was

`2.14156901519004e-6`.

It was not an original GE19 science gate.

Repair04 retains the quantity in the JSON under

`GE15_background_mode_mismatch_max`

and labels it

`diagnostic_only`.

It no longer determines provenance PASS/FAIL.

The stronger frozen provenance controls remain:

- exact GE15 dense SHA;
- GE15 frozen 64-node complete-jet abs-or-rel <= `1e-10`;
- exact GE18 Repair01 NPZ SHA;
- GE15/GE18 metric bridge <= `1e-10`;
- requested-k relative miss <= `1e-12`;
- all stable native Exp background gates;
- GE06 benign c1/c2 equivalence <= `1e-10`;
- physical-parameter stable GE06 c1/c2 finiteness.

## Repair04 implementation

Commit:

`3e1f2a7e66c8eac5aa220e041e8fd9279be1855e`.

File:

`ge19/repair04_window_retarded_reduced_h3_z20_particular.py`.

Frozen blob:

`35a8f4b6039e435e7d658e3b5cac34fdc7737f13`.

## Static compile audit

Existing GE19 static audit executed on the Repair04 implementation commit:

- run: `35527067629`;
- conclusion: `success`.

## Executable coordinate audit

Workflow:

`.github/workflows/ge19-repair04-prelock-audit.yml`.

Frozen blob:

`8107889c62a6abbbf5847337ac21685a4edd6847`.

GitHub run `35527091157` was queued at lock time.

The local science runner therefore contains an equivalent mandatory pre-science coordinate-wiring audit. Science execution is forbidden if that local audit fails.

The local audit must establish:

1. every stable GE06 c1 callback receives `bg["Z_action"]` as argument 3;
2. argument 3 is not `bg["Q_action"]`;
3. the deterministic linear main and constraint probe is finite;
4. Repair03 canonical Exp/physical-parameter controls remain valid.

## Unchanged science gates

Stage A remains exactly:

- linear-system relative L2 residual <= `1e-8`;
- shift constraint relative L2 <= `1e-6`;
- anisotropy constraint relative L2 <= `1e-6`;
- primary64/control32 state relative L2 <= `5e-3`;
- initial dynamic value/derivative mismatch <= `1e-10`;
- all outputs finite.

Stage B remains exactly:

- Nx1024/Nx2048 source low-mode relative L2 <= `5e-4`;
- primary linear-system relative L2 <= `1e-8`;
- shift constraint relative L2 <= `1e-6`;
- anisotropy constraint relative L2 <= `1e-6`;
- primary64/control32 state relative L2 <= `5e-3`;
- all beta0/C cases complete;
- all outputs finite.

## Forbidden changes

Repair04 does not change:

- frozen action;
- GE06/GE07 source files;
- stable Exp background;
- canonical Exp representation;
- H1/H3 equations;
- matter model;
- modes/phases;
- beta0/C values;
- resolutions;
- gauge;
- matching surface;
- window-retarded convention;
- any science threshold.

## Terminal classifications

PASS:

`GE19_REPAIR04_WINDOW_RETARDED_REDUCED_H3_Z20_PARTICULAR_PASS`.

Science FAIL:

`GE19_REPAIR04_WINDOW_RETARDED_REDUCED_H3_Z20_PARTICULAR_FAIL`.

Implementation FAIL:

`GE19_REPAIR04_WINDOW_RETARDED_REDUCED_H3_Z20_PARTICULAR_IMPLEMENTATION_FAIL`.

## Claim boundary

A Repair04 PASS retains the original GE19 scope: an internally reclosed reduced H1 and one window-retarded reduced-matter directional H3 particular state. It does not certify the homogeneous primordial Z20 component, a full-species second-order solution, finite eta or an observational signal.
