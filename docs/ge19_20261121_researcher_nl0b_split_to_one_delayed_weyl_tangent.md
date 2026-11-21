# GE19 — WSL native bath source split accepted; one delayed-only Weyl tangent preflight

21 November 2026. **Physics-first STOP/GO**: existing eta=0 historic CLASS trace was split into instantaneous and delayed NL0B forces without recomputing the 141,494-row baseline. Researcher result is archived byte-exactly; no physical delayed Weyl claim is made.

## 1. Accepted actual WSL output

Original user-submitted report: [archived GE19_BCHI_SOURCE_SPLIT_RESEARCHER_20261121.json](../results/GE19_BCHI_SOURCE_SPLIT_RESEARCHER_20261121.json), SHA-256 \`aefa147ed929db0bfb53892ea6f2b1c276d57aa355b79a1701ea40f0d814f591\`, original Git blob \`ea535ef17b9c050ad4e6c90af4f99c2088281c17\`. Duplicated user uploads agree byte-for-byte.

Researcher WSL evidence:
\`\`\`
GE19_FAST_HISTORY_SYNTHETIC_PASS 1.49243382e-06
GE19_FAST_HISTORY_PARENT_LOCK_PASS
GE19_HISTORY_INVERSE_SOURCE_LOCKS_PASS 4
GE19_FAST_HISTORY_TRACE_ACCEPTED 141494
GE19_FAST_HISTORY_FIRST_PASS_COMPLETE 141493
GE19_FAST_HISTORY_SECOND_PASS_COMPLETE 282986
GE19_FAST_HISTORY_REFINEMENT 7.73070497e-12 9.86359547e-16 3.12146082e-15
GE19_FAST_HISTORY_SPLIT_REFINEMENT_PASS
EXIT=0
\`\`\`
The report has \`instant_plus_delayed_algebraic_sum_pass=True\`, independent source locks and the correct archived baseline hash \`fbe1212cbc052343e283edae1c7496e631da6056ad983d575fd2d699e9bf2e19\`.

At fixed k = 0.06732117 Mpc^-1, 15 active bath nodes and the full historical time grid:
\`\`\`math
B_{\chi,0}=B_{\rm inst,0}+B_{\rm delayed,0},
\quad
\max|B_{\rm total}|=7837.613561516323,
\quad
\max|B_{\rm inst}|=10314.244030348073,
\quad
\max|B_{\rm delayed}|=2476.6304688317496.
\`\`\`
The maximum cancellation indicator is \`(max|Binst|+max|Bdelayed|)/max|Btotal|=1.6319858588\`. This is a global conservative descriptive ratio of separately occurring maxima, **not** same-time cancellation, Weyl projection ratio, or percent of lensing memory.

The RK4 first/second pass maximum delayed-force difference is \`7.730704965e-12\`, \`9.863595e-16\` of \`max|Btotal|\` and \`3.121461e-15\` of \`max|Bdelayed|\`. These compare the numerical integrations on a **fixed interpolated source**, not an independently recorded original oscillator state or independent convergence of input sampling. Hence original \`q_j,p_j\` at the *first saved* time, full initial-value mode, inverse low-frequency conditioning and independent convergence all remain explicitly **NOT CERTIFIED**. Do not retroactively change false flags.

CSV files remain on the researcher's WSL in \`results/ge19_bchi_split_fast_20261120_r1/\`. Their SHA-256 values are frozen in the archived JSON. They are not GitHub-uploaded and no derived W1 has been computed yet.

## 2. Exactly one action: reuse original CLASS tangent operator for delayed-only source

The original already obtained source-to-Weyl eta tangent in the SAME historical CLASS implementation is
\`\`\`math
W_{1,\rm total}(k=0.06732117,z=0.5)=1.8390770226818281\cdot 10^{-9},
\quad W_0=0.07009097715416947.
\`\`\`
These are a historical provisional one-point tangent, not an observed signal, independently converged total or original full Ward/adiabatic proof. We can now use **one new CLASS forcing run only**, on the *same* pinned compiled original tangent patch, with \`delayed_Bchi.csv\` as input and all other benchmark parameters, eta=0 operator, k, z and integration tolerance unchanged. The delayed source is
\`\`\`math
-\frac{aQ}{4K_B}B_{\rm delayed,0}
\`\`\`
in conformal E evolution. This is one source decomposition of the same eta=0 tangent; it is NOT a new alternative background or unrelated physics model. If this run passes, the signed instantaneous tangent inferred by linearity is
\`\`\`math
W_{1,\rm inst}^{\rm inferred}=W_{1,\rm total}^{\rm archived}
-W_{1,\rm delayed}^{\rm newly\ computed}.
\`\`\`
Do not describe this inferred value as an independent instantaneous CLASS run. Because the historical total itself was evaluated by a sparse 13-point readout at z=.5 (linear interpolation with ~1.8% variation under another local interpolation), do not attribute more relative precision to the split Weyl fraction than the underlying archived evidence.

The new fail-closed runner is
[one_delayed_only_weyl_tangent_from_split_20261121.py](../ge19/physics_gate/one_delayed_only_weyl_tangent_from_split_20261121.py).
It requires exact baseline and null SHA, exact historic patch SHA and frozen ini, source-locked inverse implementation, exact 2,546-byte source-split report SHA, both CSV output SHA, 141,494 exact time/a/k/W coordinate matches and additivity at all records, plus the original one-point total W1 report SHA. It provides a **dry-run preflight by default**; \`--run\` launches only one CLASS process. It does NOT change original C source, edit cosmic background, refit data, force more eta/k/z points or rerun the primordial baseline. It writes to a separate, previously nonexistent output directory.

## 3. Status and interpretation

Accept **successful separation of historical total bath force into instantaneous and delayed pieces** under the specified no-free-bath initial-state hypothesis, with excellent *internal* integration refinement. Do not claim the delayed part has been found in the real Weyl metric or that its sign is known. This requires an actual delayed-only tangent result. Even after that result, physical Weyl memory remains unproved until finite-k pressureful Exp AeST, photons/baryons/neutrinos, the true covariant Noether/Ward map, full Cauchy mode and observer response are certified; the original v019j half source and preliminary IC must not be silently promoted as correct physics. All working outputs and classifications remain **PROVISIONAL / PHYSICS_GO False / DES_detection False**.

The main goal remains **a genuinely retarded, history-dependent difference in the physical Weyl potential**, not simply additional dark-matter density or instantaneous elastic stiffness.
