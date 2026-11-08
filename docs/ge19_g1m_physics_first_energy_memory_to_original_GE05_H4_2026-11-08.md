# GE19 G1M — physics-first NL0B energy-to-GE05 source error bridge

**Date:** 2026-11-08.  
**Active repo/branch:** `dvlahek/aest-memory-gravity` / `physics-first-gravitational-elasticity`.  
**Action:** unchanged covariant positive-Drude NL0B Maxwell gravitational elasticity, corrected original GE06+GE07+Lambda and GE05 Euler-source dictionary.  
**Script:** `ge19/h4f3d_g1m_memory_energy_ge05_error_bridge.py` committed `51fc689`, source-lock check and exact SymPy proof available. **Not yet executed on researcher's WSL**; its algebra was independently rechecked with local SymPy, yielding `LOCAL_G1M_SYMBOLIC_IDENTITY_CHECKS_PASS`.  
**Classification until WSL run:** `G1M_SOURCE_LOCKED_ENERGY_GE05_ANALYTIC_PROOF_PREPARED` (not a true physical parent or full H4 Ward PASS).

## 1. Why change route now?

The user-executed G1L test on exact same `C_star`, primary `Nt128`, original `m20`, first coarse interval `j0` succeeded 4/4 with original GE06/GE07+Lambda operator and frozen GE05 PCHIP input:

- G1K continuous upper `max||r||inf=7.612339727225005e-4`; integral upper `4.3250371852215285e-6`; per-column algebraic interval radius `0.2563083637573321`.
- G1L fused joint algebraic upper `max||r||inf=6.766661241775515e-4`; integral upper `3.84598888812954e-6`; joint physical-state interval radius `2.045247785843688e-7`.
- G1L gains only about **11.1%** in total peak residual upper (and 11.1% in integral), despite over a million-fold improvement in the individual algebraic correction radius. Thus another isolated G1N/G1O interval-enclosure retuning campaign is not justified. Both bounds are **surrogate mathematical defect upper bounds**, not measured physical Z11 error or the H4 shift threshold.
- G1J has already certified 127/127 original-action Noether `Az` invertibility intervals in the defined exact-input Cstar/m20 model; G1I proves continuous size of numerical PCHIP GE05 source, **not its true physical bath error**.

The real missing physical object is the **error of the history-dependent bath backreaction** `B` under actual first-order parent errors. Instead of redoing interval multiplication of the same Z11 surrogate, derive a source-locked *a priori physical energy error theorem*.

## 2. Original positive-bath action and exact energy identity

The original normalized NL0B bath for each fixed frequency `omega_j>0` and weight `w_j>0` in an expanding FLRW background obeys, in physical time `t`:

```text
q_j'' + 3 H(t) q_j' + omega_j^2 q_j = omega_j sqrt(w_j) X(t).

e_j = omega_j q_j - sqrt(w_j) X
B_j = w_j X - omega_j sqrt(w_j) q_j = -sqrt(w_j) e_j
B = sum_j B_j
E = (1/4) sum_j (|q_j'|^2+|e_j|^2) >= 0 .
```

For real physical fields or complex Fourier coefficients (using Hermitian complex products and taking real parts) and **positive H(t)**, differentiate the energy exactly:

```text
dE/dt
   = - (3H/2) sum_j |q_j'|^2
     + (1/2) Re(B* X').
```

Thus gravitational memory is not an ad-hoc extra static gravity term. Energy is stored in the covariant auxiliary mismatch and exchanged with the changing scalar-gradient driver; expansion dissipates/dilutes the bath mode kinetic energy through the 3H term. For time-independent `X`, no new energy is pumped in and the internal normalized kinetic energy is nonincreasing (though conservative oscillations can persist when H=0).

This exact work/energy identity is **a derived analytical consequence of the original frozen action**, not a fit or new field equation. Normalized E is independent of eta; the physical action energy carries its original eta factor.

## 3. Rigorous bound for true-vs-approximate bath backreaction

Suppose `q_true, X_true` solve the original bath equations with shared `H(t)`, while `q_h,X_h` are numerical representations with **physical-time differential residual**

```text
R_j = q_h'' + 3H q_h' + omega_j^2 q_h
      - omega_j sqrt(w_j) X_h.
```

Set `delta q=q_true-q_h`, `delta X=X_true-X_h`, `delta e_j=omega_j delta q_j - sqrt(w_j) delta X`, `delta B = -sum_j sqrt(w_j) delta e_j` and `W=sum_j w_j`. Assume finite `W`, square-summable residual `R=(R_j)`, integrable `delta X'`, finite initial error energy

```text
Eerr = (1/4) sum_j (|delta q_j'|^2+|delta e_j|^2).
```

The **exact error energy identity**, with the sign of the approximate residual carried unchanged, is

```text
dEerr/dt
   = -(3H/2) sum_j |delta q_j'|^2
     + Re( conj(delta B) delta X' )/2
     - Re( sum_j conj(delta q_j') R_j )/2 .
```

Cauchy–Schwarz on the positive bath implies

```text
|delta B| <= sqrt(W) sqrt(sum_j |delta e_j|^2)
           <= 2 sqrt(W Eerr).

sum_j |delta q_j'|^2 <= 4 Eerr.
```

Since H>=0, this gives

```text
dEerr/dt
  <= sqrt(Eerr) [ sqrt(W) |delta X'| + ||R||_ell2 ] .
```

Using `sqrt(Eerr+eps)` and letting `eps -> 0+` avoids dividing by zero and yields the **a priori bath-response error theorem**:

```text
|delta B(t)|
   <= 2 sqrt(W Eerr(t0))
      + W integral_t0^t |delta X'(s)| ds
      + sqrt(W) integral_t0^t ||R(s)||_ell2 ds.     (★)
```

This is **not a computed error certificate**. It becomes quantitative only when certified initial `Eerr(t0)`, driver derivative error and actual continuous physical-time oscillator residual are supplied. The frozen NL0B positive weights and fixed-frequency assumption must hold; a continuum positive bath is allowed only with finite W and justified energy integrability. Source-generation roundoff, uncertainties in H/omega/w must be incorporated in R or controlled separately.

## 4. Exact bridge from physical time into the original GE19 x=ln a clock

For an expanding background with `H=dx/dt>0`:

```text
delta X' = H d(delta X)/dx
dt = dx/H
=> integral_t0^t |delta X'| dt
     = integral_x0^x |d_x delta X| dx,

integral_t0^t ||R||_ell2 dt
     = integral_x0^x ||R||_ell2/H dx.
```

No extra `1/H` factor appears in the **driver variation term**. Therefore on the exact original `C_star` background where G1J provides a positive lower bound for H on all 127 intervals, the right side of (★) can in principle be assembled from original H1 scalar-gradient derivative errors and bath residual errors in the same x-coordinate already used by D55. **G1J's positive H bound alone does not provide these error integrals.**

## 5. Exact action-normalized GE05 → Z11 Euler-source error gain

The original Repair32B `source_from_B(bg,B)` is a frozen factor-two dictionary from `-2 M1_GE05` to original GE06 raw Euler residual rows:

```text
source_order = [lapse,isotropic,aether,scalar,dust_potential,dust_density]
RAW_RESIDUAL_DICTIONARY_SCALE = 2
S_u = 2 * (1/2) a^3 Q B   = a^3 Q B
S_phi = 2 *(-1/2) a^2 i k B = -i k a^2 B .
```

For **the same exact-input action background and the same k**, with real a>0,Q,k, the common-background absolute source error norm is **exactly**

```text
||delta S_GE05(x,k)||_2
  = sqrt( a^6 Q^2 + k^2 a^4 ) |delta B(x,k)|
  = a^2 sqrt(a^2 Q^2+k^2) |delta B(x,k)|.
```

Combine with (★) to obtain a physical route to a **certified bound on the original GE05→Z11 driver** without reconstructing 8D Z11 numerical trajectories first. It is a conditional finite-positive-bath theorem, not a verified actual-research numerical result.

If true and reconstructed backgrounds differ, avoid silently substituting the common-background formula: use for example

```text
|delta S_u|
  <= |a_true^3 Q_true| |delta B|
     + |a_true^3 Q_true - a_h^3 Q_h| |B_h|,

|delta S_phi|
  <= |k| [ a_true^2 |delta B|
     + |a_true^2-a_h^2| |B_h| ].
```

Those extra background terms require independent parent enclosures.

## 6. Why this matters for original H4 physics

This step provides **a theorem linking the original covariant memory mismatch energy to the original physical Euler source in the Z11 parent**. It does **not** by itself enclose the true GE05 bath, H1 scalar-gradient error, original 8D IVP error, first-order all-parent Euler/Noether residual, D9/D12R3 FD4/FD8 M5/M9 and roundoff budget B_total, or the final mixed H4 Ward. The old H4 shift threshold and all previous historical science FAILs remain unchanged.

The sensible next calculation is **one targeted original-parent physical error evaluation**, not 127 G1L repetitions:

- Read the actual D55 first-order bath residual/error reports and original H1 source driver to identify what bounds on `Eerr(t0)`, `int |d_x delta X|`, `int ||R||/H` are presently available. Do **not** infer missing bounds from a solver tolerance or a zero-looking node residual. If all are certified, instantiate (★) per original C, clock, mode and bath; if any term is missing, freeze its absence explicitly and work only on the missing *physical* parent envelope.
- Feed the resulting **true GE05→Z11 source error** into a verified local stability/trajectory error propagation for the frozen original 8D equation. G1J exact-input Noether Az is available, but its conservative norm `||M||` must not be used naively as a global Grönwall exponent.
- Combine all actual parent Euler, dust, bath and boundary terms under the already proven 16/16 actual Cmat continuum syzygy and exact D12R2 background elimination. The existing source-only six-piece H4F3B PASS is **not** sufficient by itself.
- Only after G1 physical + D9/D12R3 G3 physical budget are closed, attempt **one original integrated H4 Ward test**. If and only if full Ward PASS, solve original H4 `Z21` with unchanged active-shift `<=1e-6` and temporal order `>=2.5`; only then compute a gauge-invariant lensing observable. No observation-based tuning.

## 7. Local lightweight analytic check (no ODE or Actions)

```bash
cd ~/aest-memory-gravity
git pull --ff-only
source .venv/bin/activate
export PYTHONPATH="$PWD"
mkdir -p results
set -o pipefail

python3 -m py_compile ge19/h4f3d_g1m_memory_energy_ge05_error_bridge.py &&
python3 -u -m ge19.h4f3d_g1m_memory_energy_ge05_error_bridge --self-test &&
python3 -u -m ge19.h4f3d_g1m_memory_energy_ge05_error_bridge \
  --json-out results/ge19_g1m_memory_energy_ge05_bridge_20261108.json \
  2>&1 | tee results/ge19_g1m_memory_energy_ge05_bridge_20261108.log
echo "EXIT=${PIPESTATUS[0]}"
```

The script performs source Git-blob locking and exact symbolic checks of the complex energy identity, two-mode positive Cauchy identity, original Repair32B factor-two dictionary, exact Euler-source norm gain, physical-time↔log(a) integral conversion and eta=0 edge. An implementation error is **not** a theory failure. No physical numerical error bound is claimed until actual first-order bath/driver enclosures are produced.
