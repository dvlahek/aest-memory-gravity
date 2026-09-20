# GE19 Repair03 canonical-Exp-product implementation lock

## Status

Locked before the first GE19 Repair03 science execution.

Historical parent classifications remain unchanged:

- original GE19:
  `GE19_WINDOW_RETARDED_REDUCED_H3_Z20_PARTICULAR_IMPLEMENTATION_FAIL`;
- Repair01:
  `GE19_REPAIR01_WINDOW_RETARDED_REDUCED_H3_Z20_PARTICULAR_IMPLEMENTATION_FAIL`;
- Repair02:
  `GE19_REPAIR02_WINDOW_RETARDED_REDUCED_H3_Z20_PARTICULAR_IMPLEMENTATION_FAIL`.

No parent is relabelled.

## Repair03 preregistration

Commit:

`3b4f616da93d3da4f4c8af7b27f868cfba90d238`.

File:

`ge19/repair03_predata_canonical_exp_product_evaluation.json`.

Frozen blob:

`a70ca4ef4ef208256913cde842d0238178ab44bb`.

## Root cause repaired

After the Repair02 frozen-symbol capture and the stable background substitution

[
Q_b=Q_0+Z_0Z_b,
]

the frozen GE06 `partial_map` still contained algebraically separated exponential products such as

[
e^{Q_0^2/Z_0^2}
e^{(Q_0+Z_0Z_b)^2/Z_0^2}
e^{-2Q_0(Q_0+Z_0Z_b)/Z_0^2}.
]

This product is exactly

[
e^{Z_b^2},
]

but separate floating-point evaluation overflows at the physical frozen ratio
`Q0/Z0=1e13`.

## Repair03 symbolic canonicalization

After the already frozen background substitution and epsilon differentiation, Repair03 operates independently on each top-level additive term.

For each term:

1. combine multiplicative exponential factors using
   `sympy.powsimp(..., force=True, combine="exp")`;
2. for every resulting `exp(arg)`, normalize
   `arg -> cancel(expand(arg))`;
3. repeat the exponential combine and argument normalization once.

No global `simplify()` is used.

No numerical substitution is used during canonicalization.

The Repair02 frozen symbolic argument tuple remains unchanged.

## Mandatory symbolic audit

Every remaining exponential atom in every c1 and c2 local partial must satisfy:

[
{m exponent}=Z_b^2
]

exactly under `cancel(expand(...))`.

No remaining exponent may contain `Q0` or `Z0`.

The successful prelock audit found:

- c1 exponential atoms: `7`;
- c2 exponential atoms: `7`;
- every c1 exponent: exactly `Zb**2`;
- every c2 exponent: exactly `Zb**2`;
- no bad exponential arguments.

The seven affected partials in both orders are:

- `N_f`;
- `L_f`;
- `R_f`;
- `b_f`;
- `u_f`;
- `phi_t`;
- `phi_x`.

## Benign GE06 equivalence

The canonical Repair03 generator was executed on the original frozen GE06 deterministic audit.

Observed source relative L2 differences:

[
epsilon_{c_1}
=
1.013732536430478	imes10^{-15},
]

[
epsilon_{c_2}
=
1.3343678633575401	imes10^{-15}.
]

All benign outputs are finite.

These are far below the frozen `1e-10` equivalence requirement.

## Physical-parameter overflow probe

The prelock audit also evaluated every c1 and c2 local partial with the frozen physical parameter scales

- `KB=0.0665`;
- `C=1.9335`;
- `K2=9500`;
- `Q0=1e-4 Mpc^-1`;
- `Z0=1e-17 Mpc^-1`;

and deterministic nonzero probes over

- `a={0.4,0.55,0.7,0.8333333333333334}`;
- `Zb={0.01,0.1,0.5,1.0}`.

Result:

- every c1 local partial finite;
- every c2 local partial finite;
- c1 finite maximum absolute value:
  `134217727.98421885`;
- c2 finite maximum absolute value:
  `4.056481920730334e31`.

These magnitudes are diagnostic only. The gate is finiteness.

## Repair03 implementation

Commit:

`1795d627668b3e301f65df91deece007a6409cfb`.

File:

`ge19/repair03_window_retarded_reduced_h3_z20_particular.py`.

Frozen blob:

`123750fbb4db21e36d8baeb7947a381ccb2bb43e`.

## Executable prelock audit

Workflow:

`.github/workflows/ge19-repair03-prelock-audit.yml`.

Frozen workflow blob:

`ed6bf61253058b4432e7771ed11a99b330c76de8`.

GitHub Actions run:

`35526570761`.

Audited HEAD:

`5e27feb8daafa05add9f366b0e245b9f31ebcaf4`.

Conclusion:

`success`.

The workflow actually imported the frozen GE06 generator, built the Repair03 canonical generator, executed the symbolic audit, executed the benign-equivalence test and executed the physical-parameter finite probe.

## Parent Repair02 failure provenance

Frozen parent failure file:

`docs/ge19_repair02_exp_product_implementation_fail_freeze.md`.

Frozen blob:

`6da644078429014f36626d0849723b5c488f0343`.

## Inherited stable-background and symbol-capture chain

Unchanged:

- Repair01 stable physical Exp background reconstruction;
- native conserved-I0 reconstruction;
- stable positive Exp `Z` solution;
- Repair01 stable symbolic re-lambdification intent;
- Repair02 frozen-symbol tuple capture;
- exact 23-symbol signature.

## Science gates

No GE19 science threshold changes.

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

The mandatory Stage-A stop rule remains unchanged.

## Forbidden changes

Repair03 does not change:

- the frozen action;
- GE06 or GE07 source-generator files;
- reduced-H1/H3 equations;
- matter model;
- modes or phases;
- beta0 or C values;
- time/spatial grids;
- gauge;
- matching surface;
- window-retarded convention;
- any numerical science threshold.

## Terminal classifications

PASS:

`GE19_REPAIR03_WINDOW_RETARDED_REDUCED_H3_Z20_PARTICULAR_PASS`.

Science FAIL:

`GE19_REPAIR03_WINDOW_RETARDED_REDUCED_H3_Z20_PARTICULAR_FAIL`.

Implementation FAIL:

`GE19_REPAIR03_WINDOW_RETARDED_REDUCED_H3_Z20_PARTICULAR_IMPLEMENTATION_FAIL`.

## Claim boundary

A Repair03 PASS retains the original GE19 scope:

1. internally reclosed reduced H1 under the frozen matched-dust model;
2. one window-retarded reduced-matter directional H3 particular state.

It does not certify the omitted homogeneous/primordial Z20 mode, a full-species second-order state, physical-amplitude nonlinear evolution, finite eta, Z21, collapse, lensing or observational evidence.
