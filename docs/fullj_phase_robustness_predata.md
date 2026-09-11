# Full-J phase/background robustness — predata

Date: 2026-09-11

Status: **PREREGISTERED BEFORE ANY NEW PHASE-REALIZATION RESULT**

Frozen label:

```text
FULLJ_PHASE_ROBUSTNESS
```

## Motivation

The locked full-J mode-coupling Jacobian established local UV-stable diagonal response and source-node/off-diagonal coupling on one deterministic multimode phase realization. The derived local Weyl covariance showed that, in the certified phase-aligned tangent basis, off-diagonal response materially changes the local output variance and dominates the z=0.25, k=0.6 Mpc^-1 node.

The remaining eta=0 statistical question is whether these conclusions are tied to the particular frozen phase realization. This phase performs one finite robustness test and then closes the phase-sensitivity question at this level. It is not an open-ended ensemble-convergence program.

## Locked ancestors

```text
full-J Jacobian lock:
8b6655d875ad04ab478da320ec42445a58ce4413
FULLJ_MODE_COUPLING_JACOBIAN_NODE_COUPLING_SUPPORTED

static Weyl identity result:
d0701d292ca794dc63f6ec4ba5f731e1184fbd7a
FULLJ_STATIC_SNAPSHOT_WEYL_OPERATOR_IDENTITY_PASS

local Weyl covariance result:
e01ed9340cea4d78867776062c1455026b61ca16
FULLJ_LOCAL_WEYL_COVARIANCE_DERIVED_COMPLETE
```

The already observed original phase realization is retained only as a historical reference and is **not counted toward the new phase gate**.

## Frozen cosmological/source grid

Exactly the locked Jacobian setup is retained:

```text
z = {0.25, 0.5, 1.0}
k [Mpc^-1] = {0.025, 0.05, 0.075, 0.10, 0.15, 0.20, 0.30,
               0.40, 0.60, 0.80, 1.00, 1.20, 1.50}
Nx = 384
interpolations = {simple, exponential, sharp}
beta0 = {1.0, 0.5, 0.1}
eta = 0
memory = disabled
```

CLASS transfer extraction must use the same full ten-redshift dense request before selecting z={0.25,0.5,1.0}, exactly as in the corrected locked Jacobian run.

No matter re-evolution, likelihood, observational data, or new physical parameter is introduced.

## Frozen new phase realizations

The original phase vector is not rerun. Three new phase vectors are fixed explicitly below. They were generated once from NumPy PCG64 seeds only to define deterministic phase tables; the explicit numbers below, not the RNG implementation, are authoritative.

### phase_A

```text
[4.167214657924744,
 2.672432702480094,
 3.5341498149062374,
 5.077383887606448,
 4.573110704763701,
 3.4622005659026267,
 4.753835493961269,
 1.89751356616761,
 1.9121953637074844,
 0.38760824402413774,
 5.154893423159532,
 3.8118014091722583,
 2.8996246080357104]
```

### phase_B

```text
[1.3870680736241223,
 5.8019639397798555,
 3.783486433172698,
 6.170369078715129,
 0.26412149706240456,
 0.16866257796458514,
 0.1985986345216254,
 3.7862899814080397,
 2.948633738603995,
 5.712223751710549,
 4.863919196461439,
 4.932350924441611,
 2.5646666361967436]
```

### phase_C

```text
[1.3473795964124813,
 2.219831228060226,
 1.8723801211612567,
 3.428988935765355,
 1.2614275369065642,
 3.7339560520169823,
 5.845364428719217,
 1.7325476776444173,
 3.3708921682007578,
 2.0113011776860024,
 4.326327283744503,
 0.28834099458887397,
 3.445328907327752]
```

The source-mode amplitudes are unchanged. Only phases are changed.

## Workload

Three new phase realizations x three redshifts x nine co-primary branches give

```text
81 new nonlinear backgrounds
1053 new tangent solves
```

The original locked realization is not recomputed.

## Tangent and Weyl definitions

For each converged nonlinear background, compute the same certified local Jacobian

\[
K^\Phi_{ij}=\partial\Phi_{k_i}/\partial S_{k_j}
\]

using one tangent direction phase-aligned with the source phase at each input mode.

Within the same static/fixed-a closure,

\[
K^W=2K^\Phi.
\]

The local diagonal UV slope is fitted over

\[
k\ge0.4\;\mathrm{Mpc}^{-1}.
\]

For the node-coupling robustness metric at z=0.25, k_out=0.6 Mpc^-1, use the frozen-source-shape tangent covariance

\[
C^S_{j\ell}\propto |S_j|^2\delta_{j\ell},
\qquad
C^W=K^W C^S K^{W\dagger}.
\]

Define

\[
f^{\rm off}_{0.6}=1-\frac{|K^W_{0.6,0.6}|^2C^S_{0.6,0.6}}
{(C^W)_{0.6,0.6}}.
\]

## Frozen numerical gates

Every one of the 81 new backgrounds must satisfy:

```text
baseline solver reaches lambda=1
R2 <= 1e-8
R1 <= 1e-10
all 13 tangent solves converge
tangent relative residual <= 1e-8
all quantities finite
```

Because exact Fourier amplitudes are phase-independent, each new realization must reproduce the locked absolute source-mode amplitudes at the same z and beta0 to relative tolerance `1e-12`. This is a hard orchestration regression.

## Frozen physical robustness gates

### UV stability

All 81 new backgrounds must satisfy

\[
\boxed{s_{\rm diag}\le -1}.
\]

This is the same local-UV stability condition used by the locked Jacobian diagnostic.

### Node coupling

There are 27 **new** z=0.25 branch x phase cases. The node-coupling robustness gate is

\[
f^{\rm off}_{0.6}>0.5
\]

for at least

\[
\boxed{21/27}
\]

new cases (at least 75%).

This means off-diagonal tangent directions supply the majority of the local Weyl variance at the source node. The already known original phase realization is excluded from this count.

Raw `T_Phi` bump size is reported but is not a gate, because phase-dependent interference can change the output amplitude even when the operator remains strongly mode-coupled.

## Classification

If any numerical/identity gate fails:

```text
FULLJ_PHASE_ROBUSTNESS_INCONCLUSIVE_SOLVER
```

If all numerical gates pass but any new background has `s_diag > -1`:

```text
FULLJ_PHASE_ROBUSTNESS_LOCAL_UV_STRUCTURE_CHANGED
```

If all numerical/UV gates pass but fewer than 21/27 new z=0.25 cases have `f_off > 0.5`:

```text
FULLJ_PHASE_ROBUSTNESS_NODE_COUPLING_PHASE_SENSITIVE
```

If all numerical/UV gates pass and at least 21/27 new node cases have majority off-diagonal variance:

```text
FULLJ_PHASE_ROBUSTNESS_PASS
```

## Scope and closure rule

A PASS licenses the statement that the tested local UV stability and node-coupling mechanism are robust across this frozen four-realization phase quartet (one locked historical + three new), within the one-dimensional static full-J setup.

It does not establish a converged cosmological random-phase ensemble, nonlinear matter power spectrum, evolving FLRW Weyl spectrum, or lensing likelihood.

No further phase-count ladder is preregistered after this test. A PASS closes phase robustness at this diagnostic level; the next step must change the physics/statistical level rather than merely add more phase seeds.

```text
ACT_LIKELIHOOD_LICENSED=False
OBSERVATIONAL_CLAIM_LICENSED=False
```
