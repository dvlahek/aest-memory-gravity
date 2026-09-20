# GE14 chi-cancellation stiff-seed audit — implementation lock

## Status

Implementation locked before first GE14 execution.

GE14 is diagnostic only and uses the frozen GE11 Repair01 artifact.

## Parent provenance

GE11 Repair01:

`GE11_REPAIR01_DENSE_LOCAL_JET_FIXED_REFINEMENT_FAIL`.

GE13 Repair01:

`GE13_AEST_MODE_AMPLITUDE_ONSET_LOCALIZED`.

Frozen GE11 artifact:

- ID `10600652596`;
- digest
  `sha256:b35a3a0c8bbd22483bd04c006b20ceb97d3c7f263e178382026cba2983628ecc`.

Frozen dense hashes:

- R1
  `c50aae91fee94f00e1cbb5bd3c4d9352f15d892e91b230fad690f06c43e25fbd`;
- R2
  `5a9480f69744db59ab8ca7fbdef56398c5fe38493730976d92b25873f46379b1`.

## Preregistration

Commit:

`bd6bbdbbe64aa35fc17bfdb403c8768d36250f65`.

File:

`ge14/predata_chi_cancellation_stiff_seed.json`.

Frozen blob:

`67677bbee68c9b99f540246f2aef7b74171b1358`.

## Implementation

Commit:

`a96219dd52279d268d356bd6592b8a0a79506cd0`.

File:

`ge14/chi_cancellation_stiff_seed_audit.py`.

Frozen blob:

`94692ff867def90c0d0ab5f0271307fb076398d1`.

## Frozen equations

At the first accepted endpoint of each mode,

`v=a theta/k^2`;

`s=v+alpha`;

`chi=Q s`.

The background identity used is

`KQ=3(rho+p)/Q`

in the frozen CLASS units.

The full E equation is reconstructed from the frozen eta=0 bridge:

`E'=a/KB[KQ chi-(2-KB)(Q Pi/(1+w)+(H+Q)chi-3 cad2 H Q alpha)]-(aH)E`.

The direct finite-gradient source evaluated separately is

`T_grad=-(a/KB)(2-KB)Q cad2[delta/(1+w)-3H alpha]`.

## Frozen gates

Require:

- exact parent artifact metadata;
- exact R1/R2 dense trace hashes;
- all six k modes;
- cancellation residual <= 8 machine-epsilon units relative to max(|v|,|alpha|);
- stiff term alone reproduces traced E-prime to relative error <= `1e-6`;
- complete reconstructed E-prime agrees with trace to abs-or-rel <= `1e-12`;
- all values finite.

No ratio between the finite-gradient and stiff seed is a PASS gate.

## Cancellation-free variable documented by GE14

Define

`s = v+alpha = chi/Q`.

Then

`alpha=s-v`

and, using

`Q'/Q=-3 cad2 (aH)`,

the exact eta=0 evolution is

`s' = a[E+Pi/(1+w)] + 3 cad2 (aH) v`.

This form does not recover `chi` by subtracting two nearly equal O(1e-7) states.

GE14 does not yet implement this variable change.

## Terminal classes

Pass:

`GE14_CHI_CANCELLATION_STIFF_SEED_LOCALIZED`.

Fail:

`GE14_CHI_CANCELLATION_STIFF_SEED_DIAGNOSTIC_FAIL`.

## Claim boundary

A PASS localizes the initial numerical seed mechanism.

It does not:

- relabel GE11;
- prove that all late-time mode growth is numerical;
- modify the IC;
- implement the new state variable;
- license Z20 or Z21.
