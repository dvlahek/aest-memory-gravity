# GE19 — Historical delayed-only Weyl tangent: signed source-response result and boundaries

**2026-11-21.** Physical status decision on an original researcher-run one-k delayed-only CLASS perturbation tangent. Exactly one new CLASS forced run was executed by the researcher. The present audit uses only the uploaded JSON, log and CSV, the older frozen total-response CSV and the previously locked source equations. **This is a historical implementation result, not physical/observed gravity memory or DES detectability.**

## 1. Immutable researcher evidence

Three researcher-uploaded UTF-8 files are now archived with byte-exact Git blobs:

| Source | Git blob SHA-1 | SHA-256 |
|---|---|---|
| [GE19_DELAYED_ONLY_WEYL_SCREEN.json](../results/ge19_one_delayed_weyl_20261121_r1/GE19_DELAYED_ONLY_WEYL_SCREEN.json) | \`d7db920bf44dc118802338c32166035384744e4a\` | \`26646889d3da0808847537483428bd7a9edfc5ca869bbaa415db96c1e456ccdc\` |
| [delayed_only_CLASS.log](../results/ge19_one_delayed_weyl_20261121_r1/delayed_only_CLASS.log) | \`ba373dd745614e90ebbbb4c87750272144937945\` | \`0e41c880fdb2b6db0e0be8c27e30fa6750db6ab63006073c38da0f65f57189ad\` |
| [delayed_only_W1.csv](../results/ge19_one_delayed_weyl_20261121_r1/delayed_only_W1.csv) | \`96b858850bb011e0de9372ae7a57d5bfc7a619ca\` | \`8a12e325ff35af18c3b29049b0054ed6d3d31111b57696f83b26c3b3a4fee897\` |

The CLASS log confirms \`GE19_TANGENT_TRACE_LOADED 141494\`, CLASS v3.3.4, finite cosmological background and source calculation. The JSON asserts \`single_new_CLASS_run_complete: true\`, frozen patch SHA \`c41ad4cad9cc18d658f80841137094349657df6ac5d68fd3c0c75cfbbe092073\`, exact delayed-source CSV SHA \`1c6ab7c5f7f80ec6c17edf5b11ef8f20dd4d83e38e36c8d10e23a744c675f3d9\`, frozen source-split report SHA \`aefa147ed929db0bfb53892ea6f2b1c276d57aa355b79a1701ea40f0d814f591\` and previous total response report SHA \`3bbaa3cb99292d90e15cfef5f643f1484b5d34a58475bc43f0221294383e936e\`. The actual delayed history input and whole C binary are not independently uploaded or recompiled in this audit. Source hash provenance and prior controls are inherited.

## 2. A signed delayed Weyl source-to-response map has actually been evaluated

For preselected \`k=0.06732117 Mpc^-1\`, \`z=0.5\`, define \`W=(Phi+Psi)/2\`. The original eta=0, fixed benchmark provides \`W0=0.07009097715416947\`. From the original total-\`Bchi\` first-order forced CLASS tangent \`W1_total=+1.839077022681828e-9\`. The researcher ran **one** CLASS response to the isolated original \`Bdelayed\` source, obtaining the **signed** result

\`\`\`math
\boxed{W_{1,\rm delayed}=-1.2006039315857457\times10^{-10},\qquad
\frac{W_{1,\rm delayed}}{W_{1,\rm total}}=-0.06528296078839421.}
\`\`\`

The history-dependent forcing *opposes* the dominant instantaneous contribution in this **historical patched model**. By linear superposition in the same frozen eta=0 tangent operator, the **inferred** instantaneous contribution is \`W1_inst = W1_total - W1_delayed = 1.9591374158404028e-9\`, signed fraction \`1.0652829607883942\`; **no separate CLASS instantaneous tangent was run**. Thus this inference is conditional on the linear response operator behaving identically under both source histories.

The absolute fractional response relative to the actual zero-memory baseline is extremely small:
\`\`\`math
\boxed{\frac{W_{1,\rm delayed}}{W_0}=-1.712922233834667\times10^{-9}\quad\hbox{per unit }\eta.}
\`\`\`
This is a ratio of model perturbative derivatives, **not** an observed lensing-shear fraction or survey signal-to-noise. No selected nonzero eta has been evolved.

## 3. Raw W1 CSV audit, all 13 sampled epochs

The uploaded delayed-only CSV contains exactly 13 finite monotone \`tau\`, \`a\` records, all with \`k=0.06732117 Mpc^-1\`, aligned in (tau,a) to the archived original total-response CSV. All 13 delayed W1 values are **strictly negative**, with magnitude increasing in later samples:

| Epoch | Delayed W1 | Delayed/total W1 at same epoch |
|---|---:|---:|
| \`z=1.5\` | \`-1.6889778977076821e-12\` | \`-3.12396823%\` |
| \`z=0.5\` (linear \`a\` interpolation) | \`-1.2006039315857457e-10\` | \`-6.52829608%\` |
| \`z=0\` | \`-1.5657314098883352e-9\` | \`-10.77293228%\` |

The sampled signed fraction decreases monotonically from -3.12% at z=1.5 to -10.77% at z=0. This trend is a property of the **sampled historical forced CLASS implementation**, not an observational redshift dependence demonstrated in nature.

The target \`a=2/3\` lies between sampled \`a=0.65686093495437059\` and \`a=0.72633277874737867\`. Independent interpolation of the uploaded delayed CSV reproduces \`-1.2006039315857472e-10\`, matching the report. A local 4-node cubic interpolation gives \`-1.1638991044921391e-10\` (3.06% less negative in magnitude relative to linear), while SciPy full cubic gives \`-1.1639797201120245e-10\`. These are **interpolation-method sensitivity estimates, not rigorous total numerical error bounds**. The original total W1 displayed about 1.8% local cubic-versus-linear difference in the 2026-11-13 prior audit; neither component has an independent error-controlled CLASS convergence series.

## 4. What was proven by which check

- \`source_additivity_max_abs=9.094947017729282e-13\` is the **input forcing** check \`Btotal=Binstant+Bdelayed\` across 141494 rows; it is **not** an independent numerical check \`Wtotal=Winstant+Wdelayed\`. In particular, \`W1_inst\` is calculated **by subtraction**.
- The old inverse source split had extremely good **internal** RK4 1x/2x time-step refinement (\`7.73e-12\` in maximum absolute forcing difference), but its source interpolation, numerical inverse conditioning and unknown exact bath q/p state at the first saved timestamp were **not independently validated**.
- The source partial derivative is evaluated in a selected eta→0+ normalized-bath branch. The historical CLASS source and initial conditions are not yet derived as a verified finite-k primordial growing eigenvector of the full Einstein–AeST–NL0B action.
- The full scalar/aether Ward identity, action-to-CLASS equivalence, original expanding background plus all-species finite-k mode, independent numerical convergence and physical galaxy–Weyl projection remain **uncertified**.
- The nonzero delayed term supplies a **numerically realized historical source-to-metric response** beyond the previously proved isolated oscillator memory and the original total-only W1. It **cannot be upgraded to observed gravitational memory, physical Weyl-memory detection or DES detectability**.

**Current classification: GE19_HISTORICAL_CLASS_DELAYED_ONLY_WEYL_TANGENT_PROVISIONAL; FULL_PHYSICS_GO = FALSE; DES_detection = FALSE.**

## 5. Decision that prevents another purely numerical loop

Retain the demonstrated sign and smallness of the delayed CLASS tangent as a *conditional exploratory finding*. Do **not** treat the -6.53% number as a relative gravitational potential, fitted observation or physical new parameter. Do **not** expand a k/eta/z grid or tune the bath to improve detectability.

Next essential physics step: build and certify **one** complete action-normalized, radiation-to-late-time Einstein–AeST–NL0B growing state, including Exp \`w_A,c_a²\`, photon–baryon tight coupling, free-streaming neutrino stress, the exact one-quarter original memory source, selected/propagated bath history, and independent scalar/Noether Ward residual. Then compute a physical normalized derivative \`W1_delayed\` under that same linear propagator and confront **predeclared** DES Y3 lensing geometry, if the physical signal exists. An extra isolated historical instantaneous CLASS run would only check additivity of a *provisional implementation* and is **not** a substitute for action/primordial certification.

## Verified links
- [Researcher-run delayed-only tangent code](../ge19/physics_gate/one_delayed_only_weyl_tangent_from_split_20261121.py)
- [Original total CLASS response](../results/ge19_one_forced_tangent_20261113/GE19_ONE_FORCED_TANGENT_SCREEN.json)
- [Previous full action Noether and one-sided selected-branch theorem](ge19_20261114_noether_constraint_and_eta0_retarded_branch_theorems.md)
- [Successful 16/16 leading coupled radiation–matter proxy](ge19_20261120_r2_confirmed_coupled_radiation_backreaction.md)
