# NL1C6D2C6H final self-consistent metric-feedback tangent — pre-data declaration

Date: 2026-09-11

This is the final numerical/theory certification step before returning to cosmological observables and observational likelihoods. No further intermediate numerical bridge is licensed or implied by a PASS of this stage.

## Frozen ancestry

D2C6H inherits, without changing their historical status:

- D2C6C/R7 eta=0 nonlinear memory tangent PASS;
- D2C6D finite-positive-eta retained scalar-current PASS;
- D2C6E larger-eta retained scalar-current PASS;
- D2C6F original direct-source FAIL;
- D2C6F-R1 direct-bath source convergence PASS;
- D2C6F-R2 corrected signed-gradient vector-source PASS;
- D2C6G eta=0 direct metric-tangent calibration PASS.

The D2C6F historical FAIL remains a FAIL. D2C6F-R2 is the corrected direct gravitational source definition used here.

## Question

Does the already certified eta=0 memory tangent remain finite and numerically controlled when the corrected direct memory metric response is fed back into the nonlinear longitudinal scalar-current evolution?

The feedback is the one present in the certified nonlinear box. The base equation is

\[
\alpha'=a(E-\Psi).
\]

Therefore its eta=0 variational equation is closed as

\[
v_\alpha'=a(v_E-v_\Psi),
\]

where \(v_\Psi\) is obtained from the corrected D2C6F-R2 unit-eta direct memory stress using the same Newtonian-gauge weak-field metric projection certified in D2C6G.

All other tangent equations are the already certified D2C6C eta=0 equations. No new phenomenological Poisson term, free coefficient, fitted normalization, or new completion parameter is introduced.

## Frozen numerical setup

- physical trajectory: eta = 0 exactly;
- ensemble: the same 27 members, sigma in {-1,0,+1}, kind in {simple, exponential, sharp}, beta0 in {1,0.5,0.1};
- primary direct bath: tan-Gauss-Legendre order 256;
- bath control: direct order 512 on the three frozen sentinels
  - sigma=+1, kind=simple, beta0=0.1;
  - sigma=0, kind=exponential, beta0=0.5;
  - sigma=-1, kind=sharp, beta0=1;
- Nx=128;
- main integration steps=4096;
- same CLASS background, modes, box, checkpoints, prehistory convention, KB=0.0665 and tau H0=1 used by D2C6G;
- metric projection retains Fourier harmonics n=1..32, exactly as D2C6G.

The corrected direct source is evaluated at unit eta on the eta=0 trajectory. This is the coefficient dT_mem/deta|0. The physical direct stress remains exactly zero at eta=0.

Metric feedback is applied throughout the retained prehistory and the main z=6-to-late-time evolution, not only at output checkpoints.

## Frozen controls and gates

H1 provenance and exact ensemble:
- all required ancestor commits are ancestors of the executed HEAD;
- exactly 27 primary members and the three frozen sentinels are present.

H2 structural eta=0 identity:
- physical direct memory source at eta=0 is zero to <=1e-12;
- base eta=0 trajectory is not modified by the tangent feedback implementation.

H3 primary health:
- all 27 feedback tangents are finite;
- base constraint <=1e-10;
- tangent constraint <=1e-10;
- min(1+j_eff)>0;
- corrected completed-square energy identity <=1e-12.

H4 feedback actually active:
- unit-eta v_Psi is finite and non-zero for every member;
- the feedback-on tangent differs from the feedback-off tangent on each of the three frozen sentinels. This is an activity/implementation check only; there is no sign or amplitude gate.

H5 direct-bath convergence:
- for the three frozen sentinels, the maximum relative low-band difference between feedback order 256 and order 512 is <=1e-2 across
  delta_alpha, delta_chi, delta_Pchi, delta_Palpha, delta_E, and delta_Psi.

H6 scope clean:
- no observational likelihood;
- no physical finite eta;
- no change of KB, tau H0, completion ensemble, background, box or source normalization;
- no claim of arbitrary-amplitude nonlinear GR/AeST.

## Classification

PASS label:

`NL1C6D2C6H_FINAL_SELF_CONSISTENT_METRIC_FEEDBACK_TANGENT_PASS`

FAIL label:

`NL1C6D2C6H_FINAL_SELF_CONSISTENT_METRIC_FEEDBACK_TANGENT_FAIL`

Technical exception label:

`NL1C6D2C6H_FINAL_SELF_CONSISTENT_METRIC_FEEDBACK_TANGENT_INCOMPLETE`

A PASS licenses return to the cosmological observable/likelihood pipeline using the certified eta=0 tangent and, where required, separately controlled finite-eta amplitudes. It does not license a claim of arbitrary-amplitude fully nonlinear GR/AeST.

No additional intermediate numerical certification stage is preregistered after D2C6H.
