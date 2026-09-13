# Full-J direct-CLASS spectral-fringe transfer-input repair

Date: 2026-09-13

## Historical incomplete attempt

The repaired runtime-provenance launch reached the first science call

`FULLJ_DIRECT_CLASS_FRINGE_RUN aest_dense_51`

but stopped before CLASS produced any AeST-dense, AeST-sparse, or GR-dense perturbation history. No `W(k,z)`, anchor-reproduction statistic, k-list-invariance statistic, fine-grid curvature, extrema count, `kappa`, or `R_spec` value was produced.

The historical classification therefore remains

`FULLJ_CORRECTED_CLASS_SPECTRAL_FRINGE_INCOMPLETE`.

The CLASS exception was

`Class did not read input parameter(s): l_max_scalars`.

## Diagnosis

`nl1c6d2n.corrected_class_baseline.build_params()` is a baseline parameter builder designed for a calculation with

`output = tCl,pCl,mTk,vTk`

and therefore includes

`l_max_scalars = 2500`.

The direct spectroscopy audit intentionally replaces the output request by

`output = mTk,vTk`

because the audit reads direct scalar perturbation histories only and does not calculate angular C_l spectra.

In frozen CLASS commit

`e85808324f51fc694d12e3ed7439552a3c3f9540`,

`l_max_scalars` is read only when scalar C_l output is active. With transfer-only output, retaining this inherited C_l-only parameter causes CLASS to reject the input as unread. This occurs before any perturbation solution used by the science audit is evaluated.

This is an input-activation bookkeeping defect, not a physics or numerical result.

## Frozen technical repair

Before any direct fine-grid AeST/GR spectrum is evaluated, the repair is fixed as follows:

1. Preserve the original direct-CLASS preregistration unchanged, including the 51-point dense grid, 15 anchors, three windows, all redshifts, all thresholds, DG-G1 through DG-G6, and all classifications.
2. Preserve the historical provenance-INCOMPLETE launch and the present transfer-input-INCOMPLETE launch unchanged.
3. Continue to build the cosmological/AeST parameter dictionary from the already validated corrected baseline.
4. Continue to set `output = mTk,vTk` for this direct perturbation-history audit.
5. Remove only the inherited C_l-only key `l_max_scalars` before calling `Class.set()`.
6. Assert in the repaired runner that the science output remains exactly `mTk,vTk` and that `l_max_scalars` is absent from the final direct-run parameter dictionary.
7. Do not add C_l calculations merely to activate an otherwise irrelevant baseline parameter.

No equation, CLASS source patch, cosmological parameter, AeST parameter, memory setting, requested k value, redshift, interpolation rule, observable definition, science threshold, gate, or classification rule is changed.

## Interpretation rule

If the transfer-only input is accepted, the original DG-G1 through DG-G6 rules remain the only science classification criteria. Any later science result must be interpreted under the original preregistration. A failure before all three CLASS calculations complete remains `FULLJ_CORRECTED_CLASS_SPECTRAL_FRINGE_INCOMPLETE` unless the original preregistered rules explicitly classify it otherwise.
