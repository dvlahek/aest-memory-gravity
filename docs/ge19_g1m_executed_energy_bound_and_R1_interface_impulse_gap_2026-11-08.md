# GE19 G1M — executed positive-bath energy proof; physical R1 interface-impulse qualification

Date: 2026-11-08. Active branch: `physics-first-gravitational-elasticity`.

## Original user-executed results: analytic PASS, not G1 physical closure

- `results/ge19_g1m_memory_energy_ge05_bridge_20261108.json`: **2,599 bytes**, SHA256 **`7b0a71de66949c3f0907acfb266ea1b10156ed3810b82ecf4d363368e208f2a3`**.
- `results/ge19_g1m_memory_energy_ge05_bridge_20261108.log`: **94 bytes**, SHA256 **`84897ea57cfdd1f7ae709502c9310d213c1fc3f22e0cc2250a4b79f21663dc98`**.
- Actual classification: `GE19_G1M_SOURCE_LOCKED_NL0B_MEMORY_ENERGY_TO_GE05_ERROR_BRIDGE_ANALYTIC_PASS_PHYSICAL_G1_OPEN`.
- Exactly 7/7 analytic checks PASS for the complex normalized bath energy identity, approximate-source residual error identity, positive two-mode Cauchy identity, original Repair32B factor-two GE05 mapping, source vector 2-norm gain, physical→x clock transform, and eta=0 edge. Source locks exact at script execution. SymPy `1.14.0`.
- Scope: analytic conditional theorem for a positive mode bath with finite `W=sum_j w_j`, common nonnegative background `H`, physical time and constant positive `omega_j,w_j`. No numerical initial error, H1 scalar-gradient derivative error, bath residual error, original G3 budget, true Z11 trajectory error or H4 Ward inferred.

## Exact physics-first derivation (smooth/absolutely continuous bath)

For `j`, original normalized positive auxiliary mode obeys
```text
q_j''+3H q_j'+omega_j² q_j = omega_j sqrt(w_j) X .
e_j = omega_j q_j - sqrt(w_j) X
B = -sum_j sqrt(w_j) e_j
E = 1/4 sum_j (|q_j'|²+|e_j|²).
```
Then `E'=-(3H/2)sum|q'|²+Re(conj(B)X')/2`. For `delta q=qtrue-qh`, `delta X=Xtrue-Xh`, `R_j=qh''+3H qh'+omega_j² qh-omega_j sqrt(w_j)Xh`, `H>=0`, define the same positive `Eerr` using delta variables. The *exact* error work balance adds `-Re(sum conj(delta q')R_j)/2`. For a genuinely absolutely continuous numerical trajectory on the whole time domain, Cauchy–Schwarz and the square-root inequality give the conditional
```text
|Btrue-Bh|(t)
 <= 2 sqrt(W Eerr(t0))
    + W INT_t0^t |delta X'(s)| ds
    + sqrt(W) INT_t0^t ||R(s)||_ell2 ds.
```

For `x=ln(a)` expanding `H=dx/dt>0`:
```text
INT |d_t delta X| dt = INT |d_x delta X| dx
INT ||R|| dt = INT ||R||/H dx.
```

Original frozen Repair32B GE05 raw-Euler source for same true/approximate background and Fourier k:
```text
S_u = a³ Q B ; S_phi = -i k a² B .
||delta S||_2 = a² sqrt(a²Q²+k²) |delta B| .
```
The source gain is an exact mathematical identity for the **common original action background**, not an independently bounded true-source error. If H/a/Q differ, use explicit background error terms.

## IMPORTANT additional physical caveat found in frozen D15a/D15a1 original R1 source

The historical frozen `ge19/h4f3d15a1_original_GE05_interface_current_jump.py` and `docs/ge19_h4f3d15a_original_clock_consistent_GE05_conditional_freeze.md` explicitly demonstrate that the original Repair24/D15a `R1` bath embedded in the physical clock is **piecewise smooth but may have nonzero internal interface current jumps**: `z` is continuous while the physical velocity `z_t=gamma v/tau` jumps at knots because left and right `hmid` can differ. **The G1M smooth-bath residual norm alone cannot be applied directly to that R1 representation if those jumps exist.**

Let `t_i` be internal knots, `z_j` the original frozen R1 normalized node state and `q_j=(sqrt(w_j)/omega_j)z_j`. At an interface with `gamma_plus-minus = tau H_i (1/hmid_plus-1/hmid_minus)`, original D15a1 defines
```text
Delta J_z,j,i = a_i³ (gamma_plus-gamma_minus) v_j,i /tau.
```
Therefore, for fixed `omega_j>0`,
```text
[ qh_j' ]_i = sqrt(w_j)/omega_j * Delta J_z,j,i /a_i³ .
```
The distributional residual of the piecewise-smooth approximate qh contains `[qh_j']_i delta(t-t_i)` in addition to its smooth part. The jump of the **true-minus-approximate** velocity is `-[qh_j']_i` (assuming the actual true solution has continuous q'). Thus for continuous qh, Xh and Xtrue, and nonnegative H, the same energy proof applies on smooth segments and the triangle inequality across interfaces yields the *correct conditional BV/measure extension*:
```text
|Btrue-Bh|(t)
 <= 2 sqrt(W Eerr(t0))
    + W INT_t0^t |delta X'(s)| ds
    + sqrt(W) [
        INT_t0^t ||R_smooth(s)||_ell2 ds
        + SUM_{t0<t_i<=t} ||[qh']_i||_ell2
      ] .
```
Here the `INT` terms are over the smooth open step interiors, and the sum uses the Euclidean norm over **physical bath modes** (also include Fourier/harmonic aggregation only under appropriate separate common-norm assumptions). This is a safe *upper* bound for finite baths with finite total jump variation. If `Xh` or true X itself jumps, the driver variation `INT|delta X'|` must also include corresponding total-variation jump terms; do not silently assume their continuity. For an infinite bath, all sums and the interface variation must converge in the original weighted Hilbert space.

This extension is **an analytical consequence**, and it is directly relevant to the original existing D15a1 impulse provenance. It must not be confused with adding a sampled, knot-index L2 diagnostic to a smooth-time L2 residual. In particular, the `Delta J_z` array is **NOT** itself `[qh']`; first divide by `a_i³` and multiply by `sqrt(w_j)/omega_j` before evaluating the physical `ell2` jump variation. Summation across *time* is L1 (sum of norms), not L2 across knots. The D15a1 signed mixed Ward impulse and its unsigned source-mode envelope are **different data** from this energy jump variation.

This corrected physical assumption does **not** invalidate the original G1M symbolic 7/7 smooth-energy identities, nor promote G1 physical closure.

## What can actually be assembled from available repo evidence now?

Source-read `ge19/h4f3d15a_original_GE05_clock_embedded_source.py`, `ge19/h4f3d15a1_original_GE05_interface_current_jump.py`, `ge19/h4f3d15a_actual_original_R1_clock_conditional.py` confirms that code exists to *compute* the original current-jump arrays on actual original frozen R1 data, and D15a actual driver can save `prefix+interior_original_J_jump_node_mode_L2` and other arrays. `docs/ge19_h4f3d15a_original_clock_consistent_GE05_conditional_freeze.md` explicitly says that its original R1 physical execution and true continuous H1 drive enclosure were **OPEN** at freeze. GitHub's current tracked tree exposes **no D55 file path by name**, consistent with D55 local outputs being outside versioned repository scope, not evidence that such outputs never existed or failed. Do not invent missing actual local D55 evidence.

**Missing independently certified inputs for a numerical G1M application:**
1. Physical error initial energy `Eerr(t0)` of the same true-vs-approximate bath state and same original H1 drive.
2. Original continuous H1 driver derivative-error integral `INT |d_x(Xtrue-Xh)| dx` (not just two interpolation differences or solver tolerances).
3. Original full physical-clock bath residual `INT ||R_smooth||/H dx`, with its original mode+positive-bath normalization.
4. If original R1 representation is used, **the additional interior velocity jump variation** `SUM_i ||[qh']_i||_ell2`, and the true H1 driver continuity/jumps if applicable; no implicit assumption that R1 is C1 across interval interfaces.
5. Transfer of these terms to exact `C_min/C_star/C_max`, `Nt128/Nt64`, all original modes and actual H4F3B parent lineage.

**No extra exploratory IVP, no retuning.** The next physical operation is to locate/read the already-created local D55 and D15a1 actual result artifacts (JSON/NPZ) if present, identify which of the five fields above they genuinely certify, and then run one correct original-bath memory error budget. If missing, report missing evidence; avoid manufacturing a certificate from a PCHIP representation.

## Unchanged scientific status

```text
G1M_SOURCE_LOCKED_ANALYTIC_ENERGY_AND_GE05_GAIN = EXECUTED_PASS_CONDITIONAL
R1_INTERFACE_JUMP_BV_CORRECTION = ANALYTIC_DERIVED_UNQUANTIFIED
TRUE_PHYSICAL_GE05_BATH_ERROR_BOUND = OPEN
TRUE_CONTINUOUS_Z11_IVP_ERROR_BOUND = OPEN
G1_PHYSICAL_CLOSED = false
G3_ORIGINAL_FD4_FD8_M5_M9_B_TOTAL_FROZEN = false
FULL_H4_WARD_CERTIFIED = false
Z21_CERTIFIED = false
LENSING_LICENSED = false
```

No changes to original H4 1e-6 active-shift gate or temporal order >=2.5, no fitted physical coefficients, no reinterpretation of historical science FAIL, and no observational tuning.
