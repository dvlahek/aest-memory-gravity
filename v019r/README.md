# v0.19r — stable CLASS-trajectory Drude quadrature

v0.19q successfully traced the actual eta=0 AeST source histories inside CLASS, but its continuum reference was not numerically reliable. The problem was numerical rather than physical.

Two corrections are made here.

## 1. Exact Drude measure on a finite interval

For the positive Drude continuum used by the conservative bath,

\[
 d\mu(\omega)=\frac{2}{\pi}\frac{d\omega}{1+\omega^2}.
\]

With

\[
 \omega=\tan\theta,\qquad 0<\theta<\frac{\pi}{2},
\]

this becomes

\[
 d\mu=\frac{2}{\pi}d\theta.
\]

The continuum is therefore evaluated by positive Gauss–Legendre quadrature on the finite theta interval. The transformed quadrature weights are strictly positive and sum to unity.

## 2. Exact linear-drive oscillator stepping

The v0.19q reference froze the CLASS drive over each time bin. At high bath frequency this introduces artificial jumps in the forcing and produces spurious ringing. v0.19r instead treats the drive as linear over each interval and propagates every damped oscillator analytically.

The overdamped small-frequency branch is evaluated with cancellation-safe characteristic roots,

\[
 \lambda_+=-\frac{\omega^2}{d+\sqrt{d^2-\omega^2}},\qquad
 \lambda_-=-d-\sqrt{d^2-\omega^2},
\]

where \(d=3H/2\). This avoids the catastrophic subtraction in \(-d+\sqrt{d^2-\omega^2}\) and the corresponding large-particular-solution cancellation.

## CLASS source domain

As in v0.19q, the source is the measured eta=0 AeST combination \(\chi_A(N,k)\) from the validated v0.19i CLASS solution. The representative requested wavenumbers are

```text
1e-4, 3e-4, 1e-3, 3e-3, 1e-2, 3e-2, 1e-1, 3e-1  Mpc^-1.
```

and the memory timescale tests are

```text
tau H0 = 1, 0.1, 0.01, 0.001.
```

## Primary gate

Reference convergence is tested on interlaced held-out CLASS trajectories by comparing N=8192 and N=16384 positive theta-quadratures. The convergence gate is

```text
max relative L2 < 2e-4.
```

A direct positive fixed bath is then chosen from

```text
N = 512, 1024, 2048, 4096
```

against the N=16384 reference. The smallest bath that satisfies all of

```text
median relative L2 < 5e-4
p95 relative L2    < 1e-3
worst relative L2  < 3e-3
all frequencies > 0
all weights > 0
sum(weights) = 1 within numerical tolerance
```

passes the v0.19r gate.

No source-weighted NNLS refit is used in this gate. The selected finite bath is a direct positive quadrature of the original conservative continuum, so positivity and fixed frequencies are structural rather than fitted constraints.

## Scope

A v0.19r pass validates a finite conservative representation on actual eta=0 AeST CLASS source histories. It does not yet constitute a finite-eta CMB prediction. The next step after a pass is to insert the selected fixed bath into CLASS and perform a tangent finite-eta convergence test.