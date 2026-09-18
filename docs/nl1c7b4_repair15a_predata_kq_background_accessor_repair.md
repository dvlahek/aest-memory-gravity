# NL1C7B4 Repair15a — pre-data KQ background accessor repair

## Status

Pre-run implementation repair preregistration.

Repair15 attempt01 is frozen as a harness failure at commit

`1a1bd3716af19d5ba3b1a76c04f68c00ae730b1f`.

No Repair15 science gate was evaluated in attempt01.

## Sole bug

The locked Repair15 evaluator used the frozen C7A interpolation helper

`rec.at_ai(gs,'pchip')`

and then requested `tv['KQ']`.

The frozen C7A helper intentionally does not include `KQ` in its background field list.

The frozen B4 helper does include `KQ` and is already the canonical source for the stable background-Q inversion used throughout the B4 repair chain.

## Sole allowed implementation change

Repair15a may add:

`z_b4=b4.read_trace(trace)`

`ks_b4,gs_b4=b4.groups(z_b4)`

`tv_b4=b4.at_ai(gs_b4)`

and require

`np.array_equal(ks,ks_b4)`.

Then and only then replace

`median(tv['KQ'])`

by

`median(tv_b4['KQ'])`

for the preregistered call

`qbg=b4.stable_q_from_kq(kq_bg)`.

Everything else remains inherited from frozen Repair15:

- Repair08 and Repair14a provenance hashes/classes;
- C7A transfer interpolation;
- density-Q correction formula;
- `KQQ` and `rhoA` use;
- scales `5,10,20`;
- `NQ=256`;
- PCHIP log-k interpolation;
- Fourier identity limit `1e-12`;
- real-space identity limit `1e-12`;
- unchanged-field regression limit `1e-12`;
- only `phidot_minus_Q` may change;
- metadata/output rule;
- no B4 residual used in construction;
- no constraint projection;
- no coefficient/sign/source/threshold change;
- no nonlinear evolution;
- eta=0.

## Additional provenance requirement

Repair15a must statically verify that:

- frozen C7A reconstruction blob remains
  `ff383c1ddc2cb2a684e2b5dd11fde0ae811e4fac`;
- frozen B4 evaluator blob remains
  `8559120dc273be3174eca130ca313ed6ff5acb25`;
- historical Repair15 evaluator blob remains
  `b455d72d768aec2ea2835e967418574de678be2d`;
- historical attempt01 freeze remains in ancestry.

## Terminal classifications

PASS:

`NL1C7B4_REPAIR15A_DENSITY_Q_COMPLETED_STATE_CERTIFIED`

FAIL:

`NL1C7B4_REPAIR15A_IMPLEMENTATION_FAIL`.

A PASS still licenses only a separately preregistered exact nonlinear B4 retest under the unchanged `1e-7` raw-constraint limit.
