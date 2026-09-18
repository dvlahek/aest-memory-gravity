# NL1C7B4 Repair14 — implementation lock

## Status

Locked after Repair14 implementation and before any Repair14 execution.

## Preregistration

- commit: `117d227737a1a78dfe5055878d703a90cbf74bd3`
- file: `docs/nl1c7b4_repair14_predata_hamiltonian_esector_density_q_bridge.md`
- blob: `875aaef1b262811988b37f338119fc04fc0ad5ea`

## Implementation

- commit: `517535978defec9d8ca04e289315d79b4acbc981`
- file: `nl1c7b/initial_constraint_certification_repair14.py`
- blob: `c67aa9f8c64ba2dcb499216feb405a7a339b7b06`

## Frozen parent chain

- Repair13a result-freeze commit: `cb6440383eac99001369e976fae035d74adf30fc`
- Repair13a result-freeze blob: `914a8aed85a87d45496c9bd05e03be4bc37bbeba`
- Repair13a JSON SHA-256:
  `cad6cb2b49b3b20a0b6346390f8536fb90da8d5000ceed82ac0de86b912679b3`
- Repair13 JSON SHA-256:
  `ef6791edd595a2bd8b44e52a703915385a1e2c4d98345ff4cc509a5d22a61a9b`
- Repair12 JSON SHA-256:
  `99c963dc65cca35c90c6b892fb4192bed1a8c03776664c9da532a5702c62767c`
- Repair11 JSON SHA-256:
  `48c8caf0c5758b089318bcd18885c87725bc244ed5a47862ac841b37b834742d`
- Repair10 JSON SHA-256:
  `f1fc1a86d2d488f5e88f0d32b0d3d1d5ce9dab22f52e51fa69801948aeb6de9d`
- Repair08 JSON SHA-256:
  `054851decab71e79a05aca2bc9fb287bb1239c8fb425989f40920004c3d88453`
- Repair08 NPZ SHA-256:
  `4639f3b5c0afcddb2f98c8b9f6a9dbbf8661dac685b12d235c09075a106dafa7`

## Frozen imported-code/document blobs

- Repair13a evaluator: `c6aa6f781b4a581db73b2dc4be38f0217dbb4a6b`
- Repair12 evaluator: `2199f8221bf341515301887de2f9fbf5a28b68a8`
- Repair01 exact source dictionary: `253a0ae2a19a597f06358704ea276c9005973af3`
- base B4 evaluator: `8559120dc273be3174eca130ca313ed6ff5acb25`
- C7A preregistration: `6d281c34c8545b3b4f2a3ab0864a684c2364ff67`
- C7A gauge bridge audit: `dd9612552eed874fa4ab4b00091e5d46c22751be`
- v0.19 CLASS bridge patch: `c78484eb916bfee2730759c0bdc813a706bf9a68`
- Repair08 evaluator: `94fb3f42a7c819b0525860f7344d5dbaff93da19`
- C7A reconstruction: `ff383c1ddc2cb2a684e2b5dd11fde0ae811e4fac`

## Locked analytic identities

Repair14 may certify only the preregistered first-order Hamiltonian identities

`C_H,E2^(1)=-2 K_B a^2 d_r(r^2 E_1)`

`C_H,EX^(1)=-2 C a^2 d_r(r^2 X_1)`

and

`delta rho_A=Q K_QQ deltaQ + (a r^2)^-1 d_r[r^2(K_B E_1+C X_1)]`.

With the frozen C7A bridge:

`delta rho_A(k)=Q K_QQ deltaQ(k)-k^2/a^2[K_B E_A(k)+C chi(k)]`.

No alternate coefficient, sign, normalization, or source grouping is allowed.

## Locked numerical audit

- analytic E-sector / induced K-correction relative-L2 limit: `1e-12`
- diagnostic lambda values: `1,1/2,1/4,1/8`
- gated intervals: `1/2->1/4`, `1/4->1/8`
- accepted H and M slope interval: `[1.8,2.2]`
- scales: `5,10,20 h^-1 Mpc`
- radial grids: `256,512`
- Y families: `Simple,Exponential,Sharp`
- beta values: `1.0,0.5,0.1`
- all 54 cases retained
- all non-center radial points retained
- center value of diagnostic `Delta deltaQ` is a finite placeholder only and is excluded from every gate
- eta: `0`

The diagnostic corrected `deltaQ` path exists only in memory and is never written as an official state.

## Claim boundary

Historical Repair08, B4, Repair12, Repair13, and Repair13a results remain unchanged.

No action coefficient/sign/source change, official-state write, threshold change, point/scale/Y/beta selection, nonlinear evolution, finite eta, B4-PASS relabel, or observational-detection claim is licensed.

Allowed terminal classes:

- `NL1C7B4_REPAIR14_DENSITY_Q_BRIDGE_OMISSION_IDENTIFIED`
- `NL1C7B4_REPAIR14_HAMILTONIAN_ESECTOR_INTERFACE_MISMATCH`
- `NL1C7B4_REPAIR14_IMPLEMENTATION_FAIL`
