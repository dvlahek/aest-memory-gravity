# GE19 Repair01 stable-Exp reduced-H3 implementation lock

## Status

Locked before the first GE19 Repair01 science execution.

Historical first GE19 execution remains

`GE19_WINDOW_RETARDED_REDUCED_H3_Z20_PARTICULAR_IMPLEMENTATION_FAIL`.

Its frozen failure record is

`docs/ge19_window_retarded_reduced_h3_z20_particular_implementation_fail_freeze.md`

with blob

`a5f4c1878b84b15643fea70a7c9f81ca22be7502`.

## Repair01 preregistration chain

Primary Repair01 predata:

- commit:
  `57148a617503d8bf06c51dbe8fba308a7531fc9d`;
- file:
  `ge19/repair01_predata_stable_exp_background_coordinate.json`;
- blob:
  `0ffceb5537e18d71c8a37ce3d41e7a967cfd7288`.

Native conserved-I0 amendment:

- commit:
  `2ba977a02781e46246b7daefd8f067e9fd93a648`;
- file:
  `ge19/repair01_predata_amendment01_native_I0_reconstruction.json`;
- blob:
  `17840209d46d8cda2f4042fce086faaadca17ef2`.

Stable symbolic re-lambdification amendment:

- commit:
  `807d207cfde68b62ccbbe474ea0b41ea524d38a1`;
- file:
  `ge19/repair01_predata_amendment02_stable_symbolic_relambdification.json`;
- blob:
  `288ff23a705fb8ac6d81a1b63a970e8b8ae74944`.

All three were frozen before any Repair01 science execution.

## Root cause being repaired

The physical Exp background uses

[
Q_0=10^{-4} {m Mpc^{-1}},
qquad
Z_0=10^{-17} {m Mpc^{-1}}.
]

The frozen GE06 symbolic source generator is analytically correct.

However its original `simplify/lambdify(cse=True)` representation can rewrite the finite factor

[
expleft[left(rac{Q_b-Q_0}{Z_0}ight)^2ight]
]

into products of individually enormous positive and compensating negative exponentials.

On the physical background this produces floating-point overflow/invalid operations before the first reduced-H1 LU factorization.

Repair01 changes only that numerical representation.

## Stable physical Exp background

From native GE15 accepted-step background rows,

[
K_Q=rac{3(ho_{m dark}+p_{m dark})}{Q_{m trace}}.
]

The conserved samples are

[
I_0(a)=a^3K_Q.
]

The frozen representative is

[
I_0={m median}[I_0(a)].
]

On every GE19 collocation grid,

[
K_Q(a)=I_0/a^3.
]

For the Exp branch define

[
x=rac{K_Q}{4K_2Z_0}.
]

Solve the positive branch

[
x=Ze^{Z^2}
]

with the same `y=Z^2` Newton equation used in pinned CLASS,

[
y+rac12ln y=ln x.
]

Then evaluate

[
Q_{m action}=Q_0+Z_0Z,
]

[
K=2K_2Z_0^2(e^{Z^2}-1),
]

[
K_{QQ}=4K_2e^{Z^2}(1+2Z^2).
]

The implementation reports native reconstruction of

[
ho=(QK_Q-K)/3,
qquad
p=K/3,
qquad
c_{m ad}^2=K_Q/(QK_{QQ}).
]

## Stable GE06 symbolic re-expression

The original GE06 file is not modified.

Repair01 imports the frozen GE06

`partial_map`

derived from the exact frozen Einstein+AeST plane-symmetric action.

Before taking the same directional derivatives, Repair01 inserts a symbolic background variable `Zb` through

[
p_t^{(0)}=Q_0+Z_0 Z_b.
]

The same GE06 epsilon substitutions are then used for all perturbation/local-jet variables.

Repair01 recomputes exactly

[
c_1=
left.rac{d}{depsilon}partialmathcal Light|_{epsilon=0},
]

[
c_2=
left.rac{d^2}{depsilon^2}partialmathcal Light|_{epsilon=0},
]

from the frozen GE06 `partial_map`.

No `simplify()` or CSE step is used in this stable re-lambdification.

Therefore the physical Exp background enters directly through finite `exp(Zb**2)` factors instead of numerically cancelling huge exponentials.

## Mandatory equivalence control

Before physical GE19 use, the stable re-expression is evaluated on the original benign GE06 deterministic audit regime.

Both source assemblies must agree with the frozen GE06 generator to

[
{m relative L2}le 10^{-10}
]

for:

- `coeff1` / linear source;
- `coeff2` / quadratic source.

All stable benign outputs must be finite.

This is a mandatory provenance/numerical-equivalence gate.

## Native background reconstruction gates

Unchanged from Repair01 predata/amendment:

- all stable background quantities finite;
- positive Exp coordinate;
- native `I0` samples relative L2 about median <= `1e-10`;
- native dark-density reconstruction relative L2 <= `1e-10`;
- native dark-pressure reconstruction relative L2 <= `1e-8`;
- native `cad2` reconstruction relative L2 <= `1e-8`.

## Original GE19 Stage-A gates remain unchanged

- linear-system relative L2 residual <= `1e-8`;
- shift constraint relative L2 <= `1e-6`;
- anisotropy constraint relative L2 <= `1e-6`;
- primary64/control32 state relative L2 <= `5e-3`;
- initial dynamic value/derivative mismatch <= `1e-10`;
- all outputs finite.

The mandatory Stage-A stop rule remains unchanged.

## Original GE19 Stage-B gates remain unchanged

- Nx1024/Nx2048 source low-mode relative L2 <= `5e-4`;
- primary linear-system relative L2 residual <= `1e-8`;
- shift constraint relative L2 <= `1e-6`;
- anisotropy constraint relative L2 <= `1e-6`;
- primary64/control32 state relative L2 <= `5e-3`;
- all three beta0 and all three C cases complete;
- all outputs finite.

No science threshold, mode, phase, beta0, C value, gauge condition, boundary condition, spatial resolution, time resolution or source normalization is changed.

## Final Repair01 implementation

Implementation commit:

`9b0d0626bd1a5bc0e2e070076283499000c666cb`.

File:

`ge19/repair01_window_retarded_reduced_h3_z20_particular.py`.

Frozen blob:

`930c658b7c135ba4bb31d783c65d330eaa8bfb7f`.

## Prelock audit

Hardened static audit workflow:

`ge19-repair01-static-prelock-audit.yml`.

Frozen workflow blob:

`23dfc50fda254c4a13e63820b5654bba9806ee1e`.

GitHub Actions run:

`35521971182`.

Conclusion:

`success`.

The audit verifies:

- Python compilation;
- Repair01 preregistration/amendment presence;
- stable Exp-coordinate helpers;
- stable symbolic GE06 re-lambdification wiring;
- unchanged numerical science thresholds;
- Stage-A stop before Stage-B construction.

## Terminal classifications

PASS:

`GE19_REPAIR01_WINDOW_RETARDED_REDUCED_H3_Z20_PARTICULAR_PASS`.

Science FAIL:

`GE19_REPAIR01_WINDOW_RETARDED_REDUCED_H3_Z20_PARTICULAR_FAIL`.

Implementation FAIL:

`GE19_REPAIR01_WINDOW_RETARDED_REDUCED_H3_Z20_PARTICULAR_IMPLEMENTATION_FAIL`.

## Historical integrity

The first GE19 implementation failure remains frozen and is not relabelled.

## Claim boundary

A Repair01 PASS has exactly the original GE19 scientific scope:

1. internally reclosed reduced H1 under the frozen matched-dust model;
2. one window-retarded reduced-matter directional Z20 particular state.

It does not certify the homogeneous/primordial Z20 mode, a full-species second-order state, finite eta, physical-amplitude nonlinear evolution, collapse, halo physics, lensing or observations.
