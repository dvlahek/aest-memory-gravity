# GE19 Repair02 frozen-symbol-tuple implementation lock

## Status

Locked before the first GE19 Repair02 science execution.

Historical parent classifications remain unchanged:

- first GE19:
  `GE19_WINDOW_RETARDED_REDUCED_H3_Z20_PARTICULAR_IMPLEMENTATION_FAIL`;
- GE19 Repair01:
  `GE19_REPAIR01_WINDOW_RETARDED_REDUCED_H3_Z20_PARTICULAR_IMPLEMENTATION_FAIL`.

Neither parent is relabelled.

## Repair02 purpose

Repair02 changes only the symbol capture used by the already preregistered stable GE06 re-lambdification.

Frozen GE06 constructs the correct symbolic

`direction_args`

tuple before its module-level deterministic audit.

Later, the module executes

`T,X,dt,dx,a,adot,qb,direction=deterministic_grid()`,

which overwrites mutable module globals such as `adot` with numerical arrays.

Repair01 rebuilt its signature from those mutable globals and therefore inserted a numerical array into `sympy.lambdify`, causing

`SyntaxError: cannot assign to literal`.

## Repair02 preregistration

Commit:

`6ed94ecefc5c2834012606ea092a84a8572f1d97`.

File:

`ge19/repair02_predata_frozen_symbol_tuple_capture.json`.

Frozen blob:

`286891c23de22bdf58a6d0a11684b5d43d857f9e`.

## Frozen symbolic contract

The authoritative GE06 signature is

`tuple(mod6.direction_args)`.

It must have 23 unique SymPy symbols in the frozen order

`aa, adot, Qb, dN, dL, dR, db, du, dLt, dLx, dRt, dRx, dbx, dut, dux, dpt, dpx, dNx, KB, C, K2, Q0, Z0`.

Repair02 constructs the stable signature as

`(frozen[0], frozen[1], Zb, *frozen[3:])`.

The stable scalar-time expansion is

[
p_t^{(0)}=Q_0+Z_0Z_b
]

with directional perturbation

[
p_t=Q_0+Z_0Z_b+epsilon,delta p_t.
]

Here `dpt`, `Q0` and `Z0` are taken from frozen tuple indices 15, 21 and 22, not from mutable module globals.

## Inherited Repair01 stable-Exp construction

Unchanged:

1. native GE15 accepted-step rows reconstruct

[
K_Q=rac{3(ho_{m dark}+p_{m dark})}{Q_{m trace}};
]

2. conserved samples

[
I_0=a^3K_Q
]

are represented by their median;

3. collocation background uses

[
K_Q(a)=I_0/a^3;
]

4. positive Exp coordinate solves

[
rac{K_Q}{4K_2Z_0}=Ze^{Z^2};
]

5. stable action background is

[
Q_{m action}=Q_0+Z_0Z.
]

The GE06 frozen `partial_map` is unchanged.

The same first and second epsilon derivatives are re-lambdified with `cse=False`.

## Repair02 implementation

Commit:

`9a747d9347309712c83a0054299c6afd9d4b784b`.

File:

`ge19/repair02_window_retarded_reduced_h3_z20_particular.py`.

Frozen blob:

`915b7883e30c4bd124154bee34c66ba5bc0f81cb`.

## Executable prelock audit

Workflow:

`.github/workflows/ge19-repair02-prelock-audit.yml`.

Final frozen workflow blob:

`d1f89eb123f81c2d3a88d4f86a18ecc7968b9a69`.

Successful executable audit:

- run: `35525545851`;
- audited HEAD:
  `b2fa89f5b934d55c527293a9f8068cff1c1f79e6`;
- conclusion: `success`.

The audit actually imports the frozen GE06 generator, constructs the Repair02 stable generator, executes the lambdified functions and evaluates the frozen benign GE06 deterministic audit.

### Symbol-contract result

- frozen argument count: `23`;
- stable argument count: `23`;
- all frozen arguments SymPy symbols: `true`;
- all stable arguments SymPy symbols: `true`;
- frozen symbols unique: `true`;
- stable symbols unique: `true`.

### Benign-equivalence result

Stable versus frozen GE06 source assembly:

[
epsilon_{c_1}^{L2}
=
1.028882209897549	imes10^{-15},
]

[
epsilon_{c_2}^{L2}
=
1.3610778770829969	imes10^{-15}.
]

All stable outputs are finite.

Both are far below the preregistered `1e-10` equivalence gate.

## Inherited provenance chain

Unchanged Repair01 predata:

- `ge19/repair01_predata_stable_exp_background_coordinate.json`
  blob `0ffceb5537e18d71c8a37ce3d41e7a967cfd7288`;
- `ge19/repair01_predata_amendment01_native_I0_reconstruction.json`
  blob `17840209d46d8cda2f4042fce086faaadca17ef2`;
- `ge19/repair01_predata_amendment02_stable_symbolic_relambdification.json`
  blob `288ff23a705fb8ac6d81a1b63a970e8b8ae74944`.

Repair01 implementation-failure freeze:

- `docs/ge19_repair01_stable_exp_background_implementation_fail_freeze.md`;
- blob `7cb06c432eee7b3b842582384e8e3c7266537184`.

## Science gates

No GE19 science gate is changed.

Stage A remains:

- linear-system relative L2 residual <= `1e-8`;
- shift constraint relative L2 <= `1e-6`;
- anisotropy constraint relative L2 <= `1e-6`;
- primary64/control32 state relative L2 <= `5e-3`;
- initial dynamic value/derivative mismatch <= `1e-10`;
- all outputs finite.

Stage B remains:

- Nx1024/Nx2048 source low-mode relative L2 <= `5e-4`;
- primary linear-system relative L2 residual <= `1e-8`;
- shift constraint relative L2 <= `1e-6`;
- anisotropy constraint relative L2 <= `1e-6`;
- primary64/control32 state relative L2 <= `5e-3`;
- all three beta0 and all three C cases complete;
- all outputs finite.

The mandatory Stage-A stop rule is unchanged.

## Forbidden changes

Repair02 does not change:

- the action;
- GE06 or GE07 frozen source files;
- the reduced-H1 or H3 equations;
- the matter model;
- modes or phases;
- beta0 or C values;
- time/spatial grids;
- gauge;
- matching surface;
- window-retarded convention;
- any numerical science threshold.

## Terminal classifications

PASS:

`GE19_REPAIR02_WINDOW_RETARDED_REDUCED_H3_Z20_PARTICULAR_PASS`.

Science FAIL:

`GE19_REPAIR02_WINDOW_RETARDED_REDUCED_H3_Z20_PARTICULAR_FAIL`.

Implementation FAIL:

`GE19_REPAIR02_WINDOW_RETARDED_REDUCED_H3_Z20_PARTICULAR_IMPLEMENTATION_FAIL`.

## Claim boundary

A Repair02 PASS retains the original GE19 scope:

1. internally reclosed reduced H1 under the frozen matched-dust model;
2. one window-retarded reduced-matter directional H3 particular state.

It does not certify the omitted homogeneous/primordial Z20 mode, a full-species second-order state, physical-amplitude nonlinear evolution, finite eta, Z21, collapse, lensing or observational evidence.
