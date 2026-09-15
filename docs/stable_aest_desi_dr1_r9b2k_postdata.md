# Stable AeST DESI DR1 R9b2k postdata freeze

## IMPORTANT STATUS

R9b2k is a completed scientific/numerical result and must not be reinterpreted after the fact.

Classification produced by the completed run:

`STABLE_AEST_DESI_DR1_R9B2K_SHAPEFIT_VECTOR_FAIL`

This label is caused only by the conditional Stage-B ShapeFit vector construction. It does **not** mean the native source response failed.

## Certified Stage A result

All preregistered Stage-A gates passed:

- K1 provenance: PASS
- K2 native grid refinement: PASS
- K3 eta=0 closure and tau invariance: PASS
- K4 epsilon consistency: PASS
- K5 native density convergence: PASS
- K6 cross-operator agreement: PASS

Actual native CLASS sampling was refined from the historical 108-node grid to

- D1: 864 nodes
- D2: 1729 nodes.

The D1 -> D2 response converged. At tau_H0=10 the relative tangent discrepancy was approximately 8.19e-3 for the linear operator and 1.10e-2 for PCHIP, with cosine similarity above 0.9999989.

At D2 the former linear-vs-PCHIP discrepancy disappeared. Across tau_H0={10,5,2.5,1.25} and epsilon={0.025,0.05}, cross-operator metrics were approximately

- E ~= 9.30e-4
- C ~= 0.999999991.

Therefore the historical R9b2j cross-operator failure is localized to insufficient native CLASS k sampling on the 108-node grid. Historical R9b2j remains a FAIL and is not reclassified.

## Stage B failure localization

DESI provenance passed and the official 24-dimensional ShapeFit vector was loaded. The constructed theory vector then failed finiteness only in the six `dm` components. The `qiso`, `qap`, and `df` components were finite.

The six failing positions are the fourth component of each bin, corresponding to indices 3, 7, 11, 15, 19, and 23 in the 24-vector.

The source is localized to the saved-source ShapeFit `m` extraction:

`dm = m - m_fid`,

with `m` obtained from the logarithmic slope of the BAO-smoothed source-state Pdd around the ShapeFit pivot. The existing adapter reused a `PowerSpectrumBAOFilter` object initialized on the broad fiducial power-spectrum support. In cosmoprimo, the filter k grid is set during construction; subsequent `__call__` updates the input spectrum but does not reset the k grid. Reusing that fiducial filter with the narrower bounded source-state Pdd can therefore evaluate the source interpolator outside its intended support and contaminate the smooth spectrum with non-finite values.

This is a Stage-B adapter/support issue. It is not evidence for renewed CLASS/source-response instability.

## Frozen interpretation

1. R9b2k Stage A is numerically certified and must not be rerun merely to revisit the 108-node interpolation problem.
2. The next action is a separately preregistered technical `R9b2k Repair01` restricted to ShapeFit `m/dm` extraction.
3. Repair01 must reuse the existing D2 checkpoints and must not rerun the 25 CLASS models.
4. Repair01 must initialize a peak-average BAO filter on the bounded D2 source support (one prepared filter per redshift), while retaining the same fiducial cosmology and the same ShapeFit definition.
5. The repair must explicitly verify finite positive no-wiggle values around the pivot before taking logarithms.
6. Stage-B epsilon/cross-operator/projection gates remain unchanged. No threshold may be relaxed postdata.
7. No observational detection, full-EFT, or tau-bound claim is licensed unless the repaired Stage B passes all frozen gates.

## Frozen local result hashes

- R9b2k JSON SHA256: `f4323f84dfa93c5ac3ef449fbe666ce3add45a50331079fe66bd27beb2b30c7e`
- R9b2k science log SHA256: `5580e537971f38d7007eed66eb0b5ef8cb92a36583dad348d7afab07ad95d306`

The historical R9b2k result is frozen exactly as produced. Repair01 is a new technical continuation and may not rewrite this classification.
