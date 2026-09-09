# NL1C5 result — screened quasistatic reclosure

Final preregistered classification:

**NL1C5_SCREENED_RECLOSURE_TRANSITION_REQUIRES_FULL_J**

Diagnosis:

**SATURATED_HIGH_GRADIENT_ASSUMPTION_NOT_SELF_CONSISTENT**

Predata commit: `56b16c289c10e1bcb6acefeb8685e6409f1be03f`.

Implementation commit: `d4920d938e71ff4d9e177f6e41b1c10ea91f47db`.

Workflow commit: `07c650009f5d0fba8d9389d17c67c426e757f28c`.

GitHub Actions run: `34342816385` — technical SUCCESS.

Artifact: `results_bundle_nl1c5_screened_quasistatic_reclosure`, ID `10100440618`, SHA256 `7fb4aec6c45ec6b83e00c0b5e00ebde188e490e040f02a836c8aa7069ec3d933`.

No observational data and no finite physical eta were used.

## Frozen test and numerical closure

NL1C5 applied the published high-gradient Helmholtz branch to the preregistered fixed **total-matter** `d_m` state from the certified v0.77 artifact. All purely numerical controls passed. Across all three co-primary `beta0` values,

- the Helmholtz residual is at most `1.49e-12`;
- the `chi=beta0/(1+beta0) Phi` identity is at machine precision;
- the `Nx=256` versus `Nx=512` field/gradient comparison is at machine precision;
- the native `k` and `z` grids close to the frozen v0.77 reference.

Thus the transition result is not caused by a numerical failure.

## Saturation self-consistency fails decisively

The preregistered rule required the reclosed field itself to satisfy

\[
x_{\rm rms}\ge10
\]

at every native time used for the retarded bath. Instead, every branch returns `x_rms << 1`.

For `beta0=1`, over `0.2<=z<=1.5`,

\[
5.20\times10^{-3}
\lesssim x_{\rm rms}\lesssim
9.35\times10^{-3}.
\]

For `beta0=0.5`,

\[
3.38\times10^{-3}
\lesssim x_{\rm rms}\lesssim
6.19\times10^{-3},
\]

and for `beta0=0.1`,

\[
9.04\times10^{-4}
\lesssim x_{\rm rms}\lesssim
1.68\times10^{-3}.
\]

The saturated high-gradient approximation therefore does not define a self-consistent fixed point for this particular frozen reclosure test. In accordance with the preregistration, the saturated memory-survival calculation was **not** executed or promoted.

The comparison with the historical linear `chi` gradient is correspondingly enormous: the reclosed saturated-field gradient is roughly `1e-11` to `1e-9` of the historical linear-gradient amplitude over the evaluation window, depending on `beta0` and time. This comparison is descriptive only; the two fields arise from different expansion/reclosure assumptions.

## Important source-convention qualification

After this run, the published AeST quasistatic equations were checked again at the source level. Their weak-field system is written with the minimally coupled baryonic density `rho_b` on the right-hand side, while NL1C5 had explicitly preregistered the certified CLASS **total-matter** transfer `d_m` as its fixed source.

Therefore NL1C5 remains an honest and reproducible **fixed-total-matter diagnostic under its preregistered scope**, and its historical classification is unchanged, but it is **not promoted as the final physical AeST quasistatic reclosure**.

The correction is theory-defined, not outcome-driven: the next step must extract the frozen native CLASS baryon transfer `d_b` and repeat the full quasistatic system with the published source convention. The full `J(Y)` operator is required because even the more strongly sourced NL1C5 total-matter diagnostic already lands far below the high-gradient branch.

## Consequence

The previous NL1C0 statement remains true only about the amplitude of the historical linear `chi` state: interpreted directly, that state has `x>>1`. NL1C5 shows that a separate finite-amplitude Helmholtz reclosure does **not** reproduce that high-gradient state. It therefore prevents us from treating `J_Y=1/beta0` as a self-consistent nonlinear closure without solving the full published quasistatic equations.

Next: freeze the correct baryonic source from the same CLASS model, then solve the full coupled `tildePhi`/`chi` equations for all three published interpolation functions and all three `beta0` values.
