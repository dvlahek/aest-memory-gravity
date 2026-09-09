# NL1C6D2N-B predata — corrected CLASS no-refit baseline

Status: **PREREGISTERED BEFORE ANY CORRECTED CLASS COSMOLOGICAL TRAJECTORY OR SPECTRUM IS INSPECTED**.

Frozen label:

```text
NL1C6D2N_B_PREDATA_CORRECTED_CLASS_BASELINE
```

## 1. Purpose

`NL1C6D2N_EXP_NORMALIZATION_AUDIT_PASS` establishes only that the corrected Exp `K(Q)` implementation has the required local curvature and internal background identities. It does not establish that the resulting cosmological background or linear perturbation trajectory is numerically healthy, nor how much it differs from the historical v053 model.

D2N-B therefore computes the first corrected-model CLASS trajectory with **no cosmological refit** and no memory/likelihood inference.

The historical v053 results remain immutable.

## 2. Frozen code and patch provenance

Use CLASS repository/commit

```text
lesgourg/class_public
e85808324f51fc694d12e3ed7439552a3c3f9540
```

and the repository patch chain

```text
v019/apply_patch_v019.py
v019i/apply_ic_patch.py
v019j/apply_memory_patch.py
v019w/apply_variational_forcing_patch.py
v019y/apply_output_precision_patch.py
v023/apply_source_grid_trace_patch.py
```

from branch

```text
v053-exp-normalization-corrected
```

where the only corrected physical source expression relative to the historical branch is the Exp normalization already locked by D2N-A.

## 3. Frozen cosmological input — no refit

Use exactly the same no-memory parameter point used by the late v053 theory/source chain:

```text
H0         = 67.3324639084866
omega_b    = 0.022377376877682164
omega_cdm  = 0.12006705327635288
tau_reio   = 0.06174082364515668
n_s        = 0.9666229454895277
A_s        = 2.1308864352626987e-9
N_ur       = 2.046
N_ncdm     = 1
m_ncdm     = 0.06
T_ncdm     = 0.7137658555036082
YHe        = 0.2454006
```

AeST parameters:

```text
aest_enabled = yes
aest_model   = Exp
aest_KB      = 0.0665
aest_Q0      = 1e-4
aest_K2      = 9500
aest_Z0      = 1e-17
```

Memory is exactly off:

```text
aest_memory_enabled = no
aest_eta = 0
```

No parameter may be moved after inspecting the corrected trajectory.

## 4. Outputs to retain

### Background

Retain the CLASS background trajectory over the available range and explicitly report the interval `0 <= z <= 6` for

```text
a, H, rho_AeST, p_AeST, w_AeST, cad2_AeST, Q_AeST, KQ_AeST.
```

### Dense perturbation histories

Use the same six frozen low-k modes

```text
k = {0.03,0.05,0.08,0.10,0.15,0.20} h/Mpc
```

and retain, where exposed by the frozen CLASS interface,

```text
tau, a, phi, psi,
delta_b, theta_b,
delta_cdm, theta_cdm,
alpha_AeST, E_AeST.
```

### Native transfer/source block

Retain the native CLASS transfer grid including at minimum

```text
d_b, t_b, d_m, phi, psi
```

for later corrected D2A/source reconstruction.

### Linear CMB spectra

At the same fixed parameters retain unlensed

```text
TT, TE, EE
```

for `2 <= ell <= 2500` only as a corrected-vs-historical diagnostic. No likelihood is evaluated in D2N-B.

## 5. B1 — clean-build provenance

The run must verify the pinned CLASS commit and record the SHA-256 of the corrected `aest_memory.c` source. The corrected source must contain

```text
K   = K2*Z0^2*(exp(Z^2)-1)
KQ  = 2*K2*Z0*Z*exp(Z^2)
KQQ = 2*K2*exp(Z^2)*(1+2*Z^2)
```

and the Exp inverse denominator `2*K2*Z0`.

Failure to build the pinned corrected code is an environment/implementation FAIL, not a physical result.

## 6. B2 — finite background and charge-law regression

All retained background quantities must be finite over `0 <= z <= 6`.

The background shift-charge identity

\[
K_Q(a)a^3=I_0
\]

must satisfy

```text
max relative spread <= 1e-10.
```

Require

```text
Q > 0
rho_AeST > 0
KQQ > 0
cad2_AeST >= 0
```

where defined.

## 7. B3 — baryon continuity regression

On the dense histories and all six frozen modes test

\[
\delta_b'+\theta_b-3\phi'=0.
\]

Use the same normalized L2 convention as D2A. Frozen gate:

```text
max normalized residual <= 2e-3.
```

No empirical projection/correction is permitted.

## 8. B4 — finite linear trajectory

For all six retained modes over `0.2 <= z <= 6`, all retained perturbation variables must remain finite.

No NaN/Inf, integration abort, or sign/convention patch after output is allowed.

This is a health gate, not a requirement that the corrected trajectory equal the historical trajectory.

## 9. B5 — native/dense closure

Interpolate the dense `d_b` and `theta_b` histories to the native transfer redshifts at the six frozen modes and compare against native `d_b`/`t_b`.

Frozen maximum relative-L2 gate:

```text
max(d_b closure, t_b closure) <= 2e-4.
```

## 10. B6 — spectra health

The corrected unlensed TT/TE/EE arrays through `ell=2500` must be finite. No observational-fit or goodness-of-fit threshold is applied in this phase.

## 11. Historical impact diagnostics — reported, not used to tune

After all B1-B6 health gates are evaluated, compare the corrected no-refit outputs with the historical v053 no-refit outputs wherever exact common arrays are available.

Report at minimum:

```text
max and relative-L2 change in H(z)
max and relative-L2 change in Q(z)
relative-L2 change in d_b and t_b on the six frozen modes
relative-L2 change in phi and psi
max fractional change in TT, TE, EE where the historical denominator is numerically safe
```

These differences do not cause the corrected model to FAIL merely because they are nonzero.

They determine the scope of later formal reruns:

- downstream results that use a changed corrected-model CLASS quantity must be regenerated for the corrected model;
- an old result may be inherited only through a separately documented exact/numerical-equivalence regression, never by assumption;
- likelihood results are not inherited as corrected-model results without a corrected-model likelihood rerun.

## 12. Classification

All B1-B6 corrected-model health gates pass:

```text
NL1C6D2N_CORRECTED_CLASS_BASELINE_PASS
```

Any B1-B6 gate fails:

```text
NL1C6D2N_CORRECTED_CLASS_BASELINE_FAIL
```

A FAIL must distinguish environment/build failure from a finite-model numerical/physical failure.

## 13. Continuation

Only a D2N corrected-baseline PASS permits regeneration of the corrected D2A source block and the subsequent corrected-model D1/D2 consistency chain.

No nonlinear full-J branch selection, memory response, Planck/ACT/SPT likelihood, or NL1C7 result is authorized by this baseline phase.