# Dense radial CLASS-residual R2 provenance repair

The first local execution of the preregistered CLASS-residual R2 validation terminated as `FULLJ_DENSE_RADIAL_CLASS_RESIDUAL_R2_INCOMPLETE` before any new holdout integration was evaluated.

All provenance checks were true except `gaussian_1d_result_lock`, even though the GitHub branch graph confirms that commit `05e38b273f91eb04b7c8753731017d0ed839c1` is an ancestor of the current branch HEAD. The failure is therefore a local ancestry-query inconsistency, not a missing physical or numerical ancestor.

No equations, k nodes, redshifts, interpolation rules, tolerances, gates, or classification rules are changed.

The runtime repair accepts the Gaussian-1D provenance only if either:

1. the original direct `git merge-base --is-ancestor` check passes, or
2. the already required dense-radial FAIL result commit `55495cc968082f1cf6638785f7609c787971835c` is an ancestor **and** the completed locked dense-radial JSON simultaneously preserves:
   - classification `FULLJ_DENSE_RADIAL_WEYL_EXTENSION_FAIL`,
   - `ancestry.gaussian_1d_result_lock == true`, and
   - `gates.G1_locked_provenance_setup == true`.

The second route is a transitive provenance certificate through an already locked milestone. If either the dense result commit or its recorded Gaussian/G1 provenance is absent, the repair does not pass.

The historical `INCOMPLETE` execution is not reclassified. The repaired run must still execute the full preregistered 20-point independent holdout validation and satisfy the unchanged gates.
