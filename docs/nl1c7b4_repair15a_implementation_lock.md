# NL1C7B4 Repair15a — implementation lock

## Status

Locked after Repair15a implementation and before any Repair15a execution.

## Historical attempt01

- freeze commit: `1a1bd3716af19d5ba3b1a76c04f68c00ae730b1f`
- freeze blob: `cb665f9c07f3b068cbd704d51bf2182a927763bf`
- historical locked Repair15 evaluator blob:
  `b455d72d768aec2ea2835e967418574de678be2d`

Attempt01 stopped with `KeyError: 'KQ'` before any Repair15 science gate.

## Repair15a preregistration

- commit: `893d42f083123f08b52df1225d0e01e49b687c61`
- file: `docs/nl1c7b4_repair15a_predata_kq_background_accessor_repair.md`
- blob: `dd0f9a930cf835640f9f045b6dc17b84f78f710a`

## Repair15a implementation

- commit: `52505918435b6a713046eb982141ad9d6b12ca43`
- file: `nl1c7b/initial_constraint_certification_repair15a.py`
- blob: `d30b74e1b8a17d4f058896e052ec4e1f6efa25e9`

## Frozen imported blobs

- Repair15 evaluator:
  `b455d72d768aec2ea2835e967418574de678be2d`
- base B4 evaluator:
  `8559120dc273be3174eca130ca313ed6ff5acb25`
- C7A spherical reconstruction:
  `ff383c1ddc2cb2a684e2b5dd11fde0ae811e4fac`

## Sole repair

Repair15a wraps the frozen Repair15 evaluator and changes only the source of the missing `KQ` background field.

The wrapper:

- reads the same frozen dense trace independently through C7A and B4 helpers;
- requires exact equality of the 128 native k modes;
- obtains finite `KQ` from frozen `b4.at_ai()`;
- temporarily augments the frozen `rec.at_ai(...,'pchip')` return dictionary with that `KQ` array;
- executes the frozen Repair15 evaluator unchanged;
- restores the original accessor after execution.

No Repair15 formula, gate, threshold, quadrature, transfer, source, sign, coefficient, state-change rule, or metadata rule is changed.

## Terminal classes

PASS:

`NL1C7B4_REPAIR15A_DENSITY_Q_COMPLETED_STATE_CERTIFIED`

FAIL:

`NL1C7B4_REPAIR15A_IMPLEMENTATION_FAIL`.

A PASS licenses only a separately preregistered exact nonlinear B4 retest at the historical `1e-7` raw-constraint threshold.
