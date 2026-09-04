# v0.19q — CLASS-trajectory source-weighted fixed bath

v0.19o showed that asking a finite conservative oscillator bath to approximate the continuum kernel uniformly over an enormous near-imaginary complex-frequency box is the wrong numerical objective. A finite undamped oscillator discretization necessarily develops narrow resonant structure near individual poles, even when its response is accurate on the actual cosmological trajectories.

v0.19q therefore measures the **actual eta=0 AeST driving history** seen by the memory sector inside CLASS and optimizes the positive fixed-frequency bath against those histories.

## 1. Trace the real CLASS source

The eta=0 Cosh and Exp CLASS runs use the validated v0.19i leading adiabatic initial condition. A test-only trace records, for representative CMB wavenumbers,

\[
a,\qquad H/H_0,\qquad k/(aH),\qquad \chi_A,
\]

plus `alpha_A`, `E_A`, and the AeST velocity state.

The representative requested wavenumbers are

```text
1e-4, 3e-4, 1e-3, 3e-3, 1e-2, 3e-2, 1e-1, 3e-1  Mpc^-1.
```

The trace is generated with one OpenMP thread and is used only for this numerical-design gate.

## 2. Use chi(t,k) as the bath drive

For each traced history and each tested `tau H0`, define

\[
h(N)=H(N)\tau,
\]

and use the normalized eta=0 CLASS trajectory `chi_A(N,k)` as the drive of the conservative bath.

The dense reference remains the original positive Drude oscillator continuum. No `H(t)`-dependent rational coefficients are introduced.

## 3. Source-weighted positive compression

A positive fixed-frequency candidate

\[
B_N=\sum_j w_j\,[\chi-q_j],\qquad w_j\ge0,
\]

is fitted in the time domain on a training subset of Cosh/Exp, k, and tau histories and validated on held-out histories.

The oscillator frequencies and weights are global constants. Therefore the reduced system preserves the original non-autonomous conservative structure.

## Primary gate

The held-out CLASS-trajectory bath response must satisfy

- dense-reference convergence better than `3e-4` normalized L2;
- validation median relative L2 `< 5e-4`;
- validation p95 `< 1e-3`;
- validation worst case `< 3e-3`;
- all retained weights non-negative;
- all retained frequencies fixed and positive.

If this passes, this is the bath representation to place back into CLASS for a tangent finite-eta response.

## Scope

v0.19q still does not interpret a finite-eta CMB spectrum. It is a source-informed reduction gate built from the already validated eta=0 AeST cosmology.
