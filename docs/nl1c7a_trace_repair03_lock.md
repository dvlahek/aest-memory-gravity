# NL1C7A A3/A4 trace Repair03 — CLASS metric-index ownership fix

## Historical technical runs

- `35092490498`: original v0.23 trace-helper anchor mismatch.
- `35093456930`: Repair01 applied successfully; workflow source-boundary audit was too strict.
- `35093652714`: Repair02 source-boundary audit PASS; CLASS compile then failed because the output-only trace extension referenced `index_mt_phi_prime` and `index_mt_psi` through `ppt` instead of the CLASS perturbation workspace `ppw`.

Pinned CLASS `e85808324f51fc694d12e3ed7439552a3c3f9540` defines `index_mt_psi` and `index_mt_phi_prime` as members of `struct perturbations_workspace`, alongside `pvecmetric`. Repair03 therefore changes only the two diagnostic reads:

- `ppw->pvecmetric[ppt->index_mt_phi_prime]` -> `ppw->pvecmetric[ppw->index_mt_phi_prime]`
- `ppw->pvecmetric[ppt->index_mt_psi]` -> `ppw->pvecmetric[ppw->index_mt_psi]`

No evolution equation, solver tolerance, physical parameter, trace field list, k grid, `a_i`, A4 gate, or classification rule may change.

## Frozen items

- C7A prereg: `5399a2ca73165e8f97cea45934e50baf8ffb3629`
- Repair01 lock: `1c5bec98bc713c809e265aee7c7c74690015550d`
- Repair02 lock: `cfdb171c376c0d4e7b72bec6a12af84d3e66954c`
- pre-Repair03 trace-extension blob: `b1567b17245facbceb73f01aa21758968f69175b`
- coverage-probe blob unchanged: `5be7163070a7fa2709e3ac6cb5835206c8feb5ec`
- A2 run/artifact unchanged: `35092206904` / `10444488624`

No A4 science/coverage result exists from the historical technical runs because the A4 probe was never executed.
