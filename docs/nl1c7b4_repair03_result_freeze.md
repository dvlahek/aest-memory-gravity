# NL1C7B4 Repair03 source-localization result freeze

Date: 2026-09-17

This note freezes the completed Repair03 diagnostic before any Repair04 implementation.

## Frozen parent

- workflow run: `35217116467`
- head SHA: `27d0323f198720f14d82fb596923b93d232b081e`
- artifact ID: `10495093609`
- artifact name: `results_bundle_nl1c7b4_repair03_source_localization`
- artifact digest: `sha256:82900b1e2c85a63b9513841580c4ca71465d8adc03e58887d5f3ffdac3e11aca`
- evaluator blob: `nl1c7b/initial_constraint_certification_repair03.py` = `3c60d384de2a55b7b9f02ef48ec3eca1ce43be2f`
- classification: `NL1C7B4_REPAIR03_CONSTRAINT_SOURCE_LOCALIZATION_COMPLETE`

## Frozen observations

The diagnostic completed all 162 amplitude cases, 54 baseline cases, and 54 scaling comparisons. State reproduction, the symbolic K dictionary identity, Q-target preservation, finiteness, and decomposition closure all passed. The maximum decomposition-closure relative L2 error was `4.1434292184482434e-14`.

For the 54 lambda=1 baseline cases:

- `max_epsilon_H` lies in `[5.386807238534919e-06, 7.427971317516522e-05]`.
- `max_epsilon_M` lies in `[0.9990515559336562, 0.9999999999945085]`.
- `rms_epsilon_M` lies in `[0.8139968229289765, 0.9785286633259102]`.
- the term with the largest absolute contribution at the maximum-momentum-residual radius is `AeST_nonK_nonJ` in all 54 baseline cases.
- its fractional absolute contribution there lies in `[0.9817825326363093, 0.9990871352016745]`.

The lambda ladder `(1, 0.5, 0.25)` does not show the momentum residual falling with the behavior expected from a purely higher-order completion error: the `M_max` log2 slopes lie approximately in `[-1.97e-05, 2.59e-03]`. This is an observation only. Repair03 does not identify the precise leading-order interface term.

## Frozen interpretation boundary

Repair03 localizes the raw eta=0 constraint mismatch. It does not project the state, change the dust sign, add radial standard-species perturbations, fit a source term, change the AeST action, or execute nonlinear evolution.

No Repair04 result or implementation existed when this result freeze was committed.