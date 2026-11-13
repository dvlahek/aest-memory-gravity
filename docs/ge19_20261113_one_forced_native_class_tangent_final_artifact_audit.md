# GE19 — final uploaded W1 artifacts: frozen native CLASS tangent and scientific disposition

**Date:** 2026-11-13  
**Status:** original numerical artifacts archived byte-exactly; **provisional implementation result, NOT physics-certified or detected**. No additional CLASS runs were initiated or requested.

## Archive and source integrity

- [Original `GE19_ONE_FORCED_TANGENT_SCREEN.json`](../results/ge19_one_forced_tangent_20261113/GE19_ONE_FORCED_TANGENT_SCREEN.json): **1,265 bytes**, SHA-256 `3bbaa3cb99292d90e15cfef5f643f1484b5d34a58475bc43f0221294383e936e`, Git blob `ca2770eaf5f02a82a8bf41ea60ca646e80c240e7`.
- [Original `forced_single_W1.csv`](../results/ge19_one_forced_tangent_20261113/forced_single_W1.csv): **971 bytes**, SHA-256 `41641f38d26f917216926e5d379b38fb7df23067745c12e4ec4a5f29e1cdb931`, Git blob `daa9ffaf532025ca74e2ce2c64666e5e7221510b`.
- [Original successful one-pass WSL log](../results/ge19_one_forced_tangent_20261113_runner.log) and earlier [passive baseline/null inspection](../results/ge19_existing_traces_inspection_20261113.log).

The JSON source linkage reports original baseline history SHA-256 `fbe1212cbc052343e283edae1c7496e631da6056ad983d575fd2d699e9bf2e19`, null SHA-256 `7cf0d48dd7bce488c81cdad7e3270ec258f8a4b1e954d574f87c2a1811a877ac`, parent modified v019j CLASS source SHA-256 `2b4d7be96b6ebf4149bef129e357a32571f69cfffb3be0b1792d578e82ad6e17`, and active patched C source SHA-256 `c41ad4cad9cc18d658f80841137094349657df6ac5d68fd3c0c75cfbbe092073`. These link to the previous independently reviewed logs; the baseline source CSV and null CSV are not part of the two new uploaded files.

## Independent non-execution CSV check

Exactly 13 finite monotone time/scale-factor records, all at k = 0.06732117 Mpc^-1 (0.1 h/Mpc). Range `a=0.4` (z=1.5) to `a=1` (z=0), with all 13 `W1` values **positive and increasing** as a increases:
- W1(a=0.4) = `5.4065143207400929e-11`
- W1(a=1) = `1.4533939028586851e-08`.
- The target `a=2/3` is **not** itself one of the samples. It lies between `a=0.65686093495437059, W1=1.6489809967774197e-9` and `a=0.72633277874737867, W1=2.995777116106528e-9`.
- Strict linear interpolation across these two original CSV rows yields **exactly** `W1(z=0.5)=1.839077022681828e-09`, identical to the uploaded JSON and previous WSL log.
- Using only the existing rows, local quadratic interpolation in neighboring triplets gives `1.80800054e-9` and `1.80169775e-9`; local cubic on four neighboring rows gives `1.80582234e-9` (**about 1.8% below** the reported linear value). This *illustrates interpolation-method sensitivity*, **NOT** an independent convergence bound or reliable 1.8% total numerical error estimate.

The native baseline inspection recorded `W0(z=0.5)=0.07009097715416947`; therefore `W1/W0 per unit eta = 2.6238427503110188e-08` is arithmetically verified. The linearized **illustrative** relative perturbation at eta=0.01 is about `2.623842750311019e-10`; this is *not* an independently evolved finite-eta model.

**Important interpretation guard:** the `Bchi` column in the **forced W1 CSV** is a structural placeholder set to `0` by `ge19_write_tangent_readout()`. It is NOT the physical forcing history and must not be misread as an unforced calculation. The actual source is the separate original 141,494-row primordial baseline trace; the previous WSL runner reported its maximum absolute `Bchi0 = 7837.613561516323`. A large historical source maximum does NOT imply a large present Weyl response.

## Interpretation and STOP decision

The full-species **patched CLASS implementation** demonstrably gives a nonzero, time-dependent derivative of the Weyl potential at eta=0 in this **fixed candidate model**. That establishes a computational source-to-response example beyond the reduced late-dust proxy, not a covariant-theory discovery or a survey prediction. The response is *very small* relative to native W0 at the one fixed k and z. Its late-time rise cannot be labeled as a physical growing mode without verifying the original action, primordial NLO initial state, complete all-species Einstein/charge Ward identities, CLASS approximation-state switch linearization, absolute numerical errors, and the actual gauge-invariant galaxy–Weyl observer projection.

**Full-physics flags in the submitted JSON are explicitly FALSE:** `full_Einstein_Ward_constraints_certified`, `full_covariant_action_consistency_certified`, `independent_numerical_convergence_certified`, `physical_Weyl_gain_certified`, `primordial_NLO_initial_state_certified`, `DES_detection`. Preserve them.

**No further numerical campaign is justified automatically by these artifacts.** Close the present implementation loop. Any next research stage should be a physically motivated analytic assessment of which retarded, Ward-compatible original-action mode could be observable, independently of tuning to DES. The accepted status is `GE19_ONE_FORCED_NATIVE_CLASS_TANGENT_PROVISIONAL_ONLY`; no measured detectability or discovery has been established.
