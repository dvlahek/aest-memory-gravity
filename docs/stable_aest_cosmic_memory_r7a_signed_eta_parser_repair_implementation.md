# Stable AeST cosmic-memory R7a — signed-eta parser repair implementation checkpoint

Date: 2026-09-15
Branch: `fullj-evolving-weyl-bridge`

Repair preregistration / pre-data note:

`d91067389d73cc3afd1857df5fb3bee851844420`

Implementation commit immediately after the repair note:

`3d500d7de4c77b687d83695a046f819041266af4`

The diff from the repair note to the implementation contains exactly one modified file:

`fullj_weyl/apply_stable_aest_r7a_live_epoch_patch.py`

No R7a science constants, eta magnitudes, epoch boundaries, observable definitions, gate thresholds, parent classifications, or driver logic were changed.

The patch now additionally requires the frozen parent `source/input.c` to contain exactly one AeST nonnegative-eta parser guard, neutralizes that guard exactly once in the disposable R7a build, and verifies a dedicated signed-diagnostic marker. The physical perturbation equations remain unchanged except for the already preregistered live epoch multiplier.

The first R7a `STABLE_AEST_COSMIC_MEMORY_R7A_RUN_FAIL` remains a historical technical pre-result attempt and is not reclassified.
