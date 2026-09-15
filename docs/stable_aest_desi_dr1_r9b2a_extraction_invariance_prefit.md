# Stable AeST DESI DR1 R9b2a extraction-invariance audit (pre-result lock)

This is a theory-only technical audit motivated by the frozen historical R9b2 central-derivative FAIL. It does not read DESI data, residuals, covariance, or likelihood values and cannot reclassify R9b2.

Historical R9b2 post-data lock: `5f453a296d367556927cfa8e1e86b7ea103a9b52`.
Historical R9b2 classification remains `STABLE_AEST_DESI_DR1_R9B2_CENTRAL_DERIVATIVE_FAIL`.

## Question

R5b and its descendants inherit `k_output_values` from the earlier spectral-fringe/ULP diagnostic chain. The canonical coordinate is `k_h=0.165`, and the selected bit pattern is `4592669915990485346`. Pre-existing ULP-forensics code identifies the adjacent pair `(4592669915990485346, 4592669915990485347)` at this same coordinate.

`k_output_values` is an output/diagnostic sampling request. A physical broadband observable such as `sigma8(P)` must not depend materially on the serialization of this diagnostic request. R9b2 newly formed external continuous-k density and velocity spectra from `pk_cb_lin` and `get_transfer`, so this invariance must be checked before those spectra can be used in a DESI projection.

## Frozen theory setup

Use the same disposable direct-physical stable-chi CLASS build and the same source-active parameter constructor as R9b2. Set `eta=0`, request `mPk,mTk,vTk`, use `P_k_max_h/Mpc=5`, no nonlinear correction, and evaluate the six already frozen DESI effective redshifts only as theory coordinates:

`0.29536404346937617, 0.5096288678782911, 0.7057956472488681, 0.9185851971138159, 1.3170658832980264, 1.4905017757527006`.

No DESI observable values are loaded.

Evaluate these variants:

1. `locked_tau10`: exact R9b2 source-active eta=0 parameters with the locked `k_output_values` serialization and bit `4592669915990485346`.
2. `ulp_plus1_tau10`: identical except only the canonical `k_h=0.165` output token is changed to the adjacent bit `4592669915990485347`.
3. `no_kout_tau10`, `no_kout_tau5`, `no_kout_tau2p5`, `no_kout_tau1p25`: identical source-active eta=0 parameters except `k_output_values` is removed before CLASS is run. This removes a diagnostic output request, not a field equation or physical parameter.

For every redshift record:

- CLASS internal `sigma8` from `c.sigma(8,z,h_units=True)`;
- legacy integrated growth ratio `effective_f_sigma8/sigma8` as a diagnostic only;
- externally reconstructed `sigma8(Pdd)` from the same R9b2 dense `pk_cb_lin` path;
- externally reconstructed `sigma8(Ptt)` and direct `f=sigma8(Ptt)/sigma8(Pdd)` from `d_b,d_cdm,t_b,t_cdm` with `v_newtonian=-theta/Hconf`;
- finite/positive checks.

## Frozen gates

The numerical consistency tolerance is `5e-3`, inherited from the already locked CLASS-vs-CAMB velocity-adapter gate. The material-contamination threshold is `5e-2`, ten times that consistency tolerance. These values are frozen before this audit is run.

- **A1 provenance**: historical R9b2 post-data lock, corrected R9b2 preregistration, and validated GR velocity adapter are ancestors and have the expected classifications.
- **A2 internal request invariance**: between `locked_tau10` and `no_kout_tau10`, the maximum relative change in CLASS internal sigma8 and in the integrated legacy growth diagnostic is <= `5e-3`. This checks that removing the output request does not materially alter integrated physical observables.
- **A3 serialization-free density consistency**: for all six redshifts and all four no-kout tau values, external `sigma8(Pdd)` agrees with CLASS internal sigma8 to <= `5e-3`.
- **A4 serialization-free direct-velocity sanity**: all no-kout Pdd/Ptt spectra give finite positive sigma8 values and `0.05 < f_direct < 2.0` at every redshift.
- **A5 eta-zero tau invariance**: across the four no-kout tau values, external density sigma8 and direct f agree with the tau=10 no-kout values to <= `5e-3` at every redshift.
- **A6 material diagnostic-output contamination**: at least one of the following exceeds `5e-2`: locked-vs-no-kout external density sigma8, locked-vs-no-kout direct f, adjacent-ULP-vs-locked external density sigma8, or adjacent-ULP-vs-locked direct f. A6 is a contamination-identification gate, not a physics gate.

## Classification

If A1--A5 pass and A6 is true, classify
`STABLE_AEST_DESI_DR1_R9B2A_DIAGNOSTIC_OUTPUT_CONTAMINATION_CERTIFIED`.

If A2 fails, classify a deeper output-request dependence and do not license a repair. If A3--A5 fail, the serialization-free extraction remains unresolved and no DESI rerun is licensed. If A6 is false, the hypothesized diagnostic-output contamination is not reproduced.

## Allowed consequence

Only the contamination-certified classification licenses a future, separately preregistered R9b3/R9b2b science run in which `k_output_values` is removed before broadband direct-velocity extraction. It does not license filtering individual k points, changing epsilon values, relaxing G4, changing nuisance parameters, or using DESI residuals to select a repair.
