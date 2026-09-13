# Full-J corrected CLASS spectral-fringe capacity repair — post-INCOMPLETE preregistration

## Status before this repair

The direct CLASS spectral-fringe + matched-GR control science design remains frozen by `docs/fullj_corrected_class_spectral_fringe_gr_control_predata.md` and commit `0e26b4688eeeedd522b8dd153f84a76137d7e43c`.

The provenance repair and transfer-only input repair were executed before any direct spectral-fringe science diagnostics were available. The R2 launch reached the first corrected-AeST dense-51 CLASS calculation but stopped before constructing any `W(k,z)` array with

```text
RuntimeError: history count 49 != requested 51
```

Therefore R2 is preserved as historical `FULLJ_CORRECTED_CLASS_SPECTRAL_FRINGE_INCOMPLETE`. No DG-G2, DG-G3, DG-G5, or DG-G6 result exists from that launch, and no physical conclusion is licensed.

## Diagnosed implementation-capacity cause

The frozen CLASS source at `e85808324f51fc694d12e3ed7439552a3c3f9540` defines

```c
#define _ARGUMENT_LENGTH_MAX_ 1024
```

in `include/parser.h`. The 51-point preregistered `k_output_values` serialization at 17 significant digits is about 1080 characters, while the first 48 values occupy about 1017 characters. Thus the dense-51 parameter exceeds the frozen CLASS argument capacity and the observed 49-history return is consistent with argument truncation at the parser/classy boundary.

In addition, the frozen Cython declaration `python/cclassy.pxd` hard-codes the original perturbation-output capacity 30 in the `k_output_values`, `index_k_output_values`, perturbation-data-pointer, and perturbation-data-size arrays. The earlier dense-k64 repair increased only the C header macro. The C and Cython capacity declarations must be made consistent before a 51-history Python retrieval is treated as a valid numerical control.

## Frozen technical repair

The next run may change only runtime capacity declarations in a newly rebuilt isolated corrected CLASS environment:

1. Preserve exact CLASS git head `e85808324f51fc694d12e3ed7439552a3c3f9540`.
2. Preserve the already validated corrected-AeST patch chain and exact `source/aest_memory.c` SHA-256 `4d5ab5dc7066d4880f06fcfc731d6534ed0ff992e3cc15fb473dddccb25a594f`.
3. Preserve `_MAX_NUMBER_OF_K_FILES_=64` in `include/perturbations.h`.
4. Increase only `_ARGUMENT_LENGTH_MAX_` in `include/parser.h` from `1024` to `4096`. `_LINE_LENGTH_MAX_` is not changed because this run passes parameters through classy's in-memory `file_content`, not an `.ini` line.
5. In `python/cclassy.pxd`, change only the eight perturbation-output array capacities associated with k-output histories from `[30]` to `[64]`:
   - `k_output_values`
   - `index_k_output_values`
   - scalar/vector/tensor perturbation data pointers
   - scalar/vector/tensor perturbation data sizes.
6. Rebuild/reinstall classy after these capacity changes.
7. Require a pre-science runtime audit proving the exact CLASS head, corrected AeST source SHA, C k-file capacity 64, argument capacity 4096, and all eight Cython k-output capacities 64.
8. Require the serialized preregistered dense-51 `k_output_values` string to be longer than 1023 and shorter than 4096 bytes, demonstrating that this repair addresses the observed capacity boundary without changing the grid.

No equation, cosmological parameter, AeST parameter, GR-control parameter, requested physical k value, redshift, interpolation rule, observable definition, science threshold, gate, or classification rule may change.

The direct spectroscopy still uses the transfer-only input repair (`output=mTk,vTk` with inherited `l_max_scalars` removed) and the same 51 dense values / 15 sparse anchors.

## Interpretation rule

A successful capacity audit merely licenses re-running the already preregistered science test. It does not itself satisfy any spectral-fringe science gate.

If the repaired runtime still returns a history count different from the exact requested count, the result remains a numerical-control failure/incomplete diagnostic and must be localized before any physical interpretation.

Historical R1 and R2 INCOMPLETE launches remain unchanged and are not reclassified.
