# GE19 Repair38 local frozen-source Radau substep diagnostic runner — lock

## Status

The first local Repair38 diagnostic execution path is frozen.

Runner:

`ge19/run_local_repair38_frozen_source_radau_substep_localization.sh`.

Runner blob:

`37a66d1027db3aee6f6e4937d2ab502ac3fe95c4`.

Runner commit:

`f586668150edc28954b371b2884b3ef4ea281748`.

Global static audit:

- run:
  `35839298259`;
- job:
  `107110252414`;
- conclusion:
  `success`.

Dedicated Repair38 prelock:

- run:
  `35839113490`;
- job:
  `107109657750`;
- conclusion:
  `success`.

## Bound contract

Repair38 preregistration:

- final commit:
  `a3c5ac84c7a0769f91f26fd3ead17445549bc964`;
- blob:
  `41a2925cf4f705c4bf8418cbcc2cee48af4a673d`.

Repair38 implementation:

- commit:
  `7ac789069eda7af0f86ff8a7003428cc5c4d0c24`;
- blob:
  `fd0c80f73f0e1b485ecb895566bef078a12ba957`.

Repair38 implementation lock:

- commit:
  `a569565c380605717fb7360d245224a4c2ffb4e6`;
- blob:
  `00d6f1deda247c82cf0847333965acbb97b5672d`.

Repair38 prelock workflow:

- commit:
  `07606e314310d77cad1d04a0234997be1dc10f3a`;
- blob:
  `dd88bc6ef75003b927869b4e900e7071368b2d23`.

Repair37 valid-FAIL localization:

- freeze commit:
  `8ef52885d33aac1f91bc75261d53ce8b3b4c54dc`;
- freeze blob:
  `d120915221b5fc1b0860c682cb8edac876571e83`.

Frozen Repair37 science artifacts:

- JSON/FULL SHA-256:
  `da8f2f00c22c866ec3f82381d23f69bf036e630fe2a29c5c44657984b760f61a`;
- NPZ SHA-256:
  `572d8937c1d742b10da66e34cc076377c1b2feb20b8f72eb25c3eaf31a59829f`.

## Execution rule

Repair38 is a diagnostic-only execution.

It must not rebuild the H4 source, resolve the projected boundary, alter the
`1e-6` science target, relabel Repair37 or certify Z21.

Only the number of internal Repair07 two-stage Radau IIA substeps per frozen
Repair37 Nt128 interval varies: `1,2,4`.

Factor 1 must reproduce Repair37 before the finer-substep result can be
interpreted.

A completed diagnostic routes to one of:

- `RADAU_PROPAGATION_FLOOR_CONFIRMED`;
- `PROPAGATION_ACCURACY_DEPENDENCE_CONFIRMED`;
- `PCHIP_OR_OTHER_FLOOR_REMAINS`.

An implementation/reproduction failure may be repaired without changing this
frozen diagnostic contract.

No Repair38 outcome itself licenses lensing.
