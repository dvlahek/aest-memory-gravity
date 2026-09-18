# NL1C7B4 Repair15 — attempt01 harness failure freeze

## Status

Frozen first local WSL execution attempt of locked Repair15.

The runner lock passed at HEAD

`90e80561185f2d0466dc4c97261412aff2c6bf42`

with the expected frozen Repair14a JSON SHA-256

`d60398e2804222df70e8cd3acda5fb397e9cfdd2068415b9256af4d65a5c64ca`.

The evaluator then raised

`KeyError: 'KQ'`

before constructing any Repair15 state and before evaluating any Repair15 science gate.

Observed terminal return:

`SCIENCE_RC=1`

`EXIT=1`.

This is an implementation/harness failure only. It is not a Repair15 science result and no terminal Repair15 science classification is assigned to attempt01.

## Exact failure mechanism

The locked Repair15 evaluator called

`tv = rec.at_ai(gs,'pchip')`

from the frozen C7A reconstruction module and then attempted

`tv['KQ']`.

The frozen C7A module declares

`BG=['H_Mpc_inv','Q','rhoA','KQQ']`

and therefore intentionally does not return a `KQ` field.

The frozen B4 module declares

`BG=['H_Mpc_inv','Q','rhoA','KQQ','KQ']`

and its `b4.at_ai()` routine therefore provides the required frozen `KQ` background used by the already frozen stable `Q` inversion.

## State/output boundary

Because execution stopped before the Repair15 construction loop:

- no Repair15 gate was evaluated;
- no Repair15 result JSON was written;
- no Repair15 state NPZ was certified;
- no B4 retest was run;
- no action/state/threshold conclusion follows from attempt01.

## Licensed repair

A separately preregistered Repair15a may change only the background-field accessor used for the preregistered stable `Q_bg` reconstruction:

- retain the existing C7A `rec.at_ai()` object for CLASS transfers and the frozen `KQQ`/`rhoA` quantities already used by Repair15;
- additionally construct the frozen B4 `b4.at_ai()` object from the same dense trace;
- require the exact native k grids to agree;
- obtain only `KQ` from the B4 interpolation object for
  `qbg=b4.stable_q_from_kq(median(KQ))`.

No formula, coefficient, sign, transfer, quadrature, state-field rule, identity limit, regression limit, metadata rule, or claim boundary may change.

Historical Repair15 attempt01 remains a harness failure.
