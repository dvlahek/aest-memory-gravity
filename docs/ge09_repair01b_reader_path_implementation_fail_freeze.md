# GE09 Repair01b native CLI — reader-path implementation-fail freeze

## Status

Workflow run:

`35494325084`.

Execution HEAD:

`d5299dbf3983d109dd68242f21314776b42e726a`.

The run passed the Repair01b lock, pinned CLASS build, native CLI execution and produced all six official CLASS scalar perturbation tables.

It terminated before GE09 science gates because the Python reader omitted the separator underscore in the file path.

Classification:

`GE09_REPAIR01B_PRE_SCIENCE_READER_PATH_IMPLEMENTATION_FAIL`.

This is not a GE09 local-jet science FAIL.

## Artifact

Artifact ID:

`10599643436`.

Artifact ZIP SHA-256:

`46d9a3c012e30c09b4b62fd6671120c222d46a7529a9dad530d2519e6d94fbbe`.

Official CLASS perturbation tables were produced successfully:

- k0 SHA-256:
  `291a75f3803bf4d139baa457ca2ee01b67d6ed262da3d968e9025a59aa75d990`;
- k1:
  `ee23af0b3b7d7e982f35062526b53892d6432ec0358fe61e397b4fa2c341b30c`;
- k2:
  `f311bfe703bda8f37f9e6e6b08b233b9d7dd4a2cd5b48b8f74341e46057b0933`;
- k3:
  `958f56b0af74b2211c2ccf7beeb252f77e5b1c5c8b62246250e19b06ca2d7515`;
- k4:
  `8a8d8618d1dd82ad81c4a0cfb3647c9858b911be1a135741065032b917cf3037`;
- k5:
  `29653331994eea64e17da253455819ca80b1e3f310feee2998207b4f254ccde6`.

The dense accepted-step trace and source-state trace were also reproduced.

No science JSON or NPZ was produced.

## Failure

Repair01b correctly supplied the explicit CLASS root

`.../results/ge09_cli`.

Pinned CLASS canonicalized this to

`.../results/ge09_cli_`

and wrote the expected files

`ge09_cli_perturbations_kN_s.dat`.

However the unchanged Python cleanup/reader paths concatenated

`str(prefix) + "perturbations_kN_s.dat"`

which resolves to

`ge09_cliperturbations_kN_s.dat`.

The driver therefore raised `FileNotFoundError` before parsing the already existing official CLASS tables.

## Licensed continuation

A separately preregistered implementation-only repair may change exactly the two filename constructions in

`ge09/repair01_dense_accepted_step_local_jet_bridge.py`

from

`str(prefix)+f"perturbations_k{i}_s.dat"`

to

`str(prefix)+f"_perturbations_k{i}_s.dat"`.

These are:

1. the pre-run stale-file cleanup path;
2. the post-run official CLASS perturbation-table reader path.

No other driver line, physics setting, precision value, trace hook, interpolation rule, gate, threshold or claim boundary may change.
