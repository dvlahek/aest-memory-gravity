# Dense radial CLASS-residual R2 CLASS k-output limit repair

A repaired local execution of the preregistered CLASS-residual R2 validation reached the actual 41-node K3 CLASS request and then terminated before any new holdout integration was evaluated.

The failure was the stock CLASS compile-time perturbation-output capacity:

`#define _MAX_NUMBER_OF_K_FILES_ 30`

while the frozen K3 grid contains 41 requested `k_output_values`. CLASS therefore aborted in `input_read_parameters_output` before the R2 holdout calculation started.

This is a technical array-capacity limit only. It is not a physical, numerical, interpolation, or convergence result.

## Frozen repair

For this dense residual-R2 milestone only, build a separate corrected CLASS environment from the same pinned CLASS commit

`e85808324f51fc694d12e3ed7439552a3c3f9540`

and apply exactly the same already frozen AeST patches as the certified D2C6 corrected environment. Then change only

`_MAX_NUMBER_OF_K_FILES_ : 30 -> 64`

in `include/perturbations.h` before compiling `classy`.

The value 64 is a capacity choice, not a sampled data choice. The preregistered K3 grid remains exactly 41 nodes and no additional k node is introduced by this repair.

The dense environment uses separate local directories so the historical corrected CLASS installation is not modified.

No cosmological parameter, AeST source term, R2 equation, redshift, k node, interpolation rule, tolerance, gate, or classification rule is changed.

The existing corrected-CLASS provenance audit remains applicable because it verifies the pinned CLASS git HEAD and the corrected AeST source anchors; this repair changes only the perturbation-output array capacity header.

The historical aborted execution remains an execution abort and is not reclassified. The repaired run must still execute all 20 independent H3 holdout integrations and satisfy the unchanged preregistered gates.