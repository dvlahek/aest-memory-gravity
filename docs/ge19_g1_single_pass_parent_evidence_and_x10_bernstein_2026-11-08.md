# GE19 G1 — one-pass parent evidence with an exact-rational X10 Hermite bridge

Date: 2026-11-08  
Branch: `physics-first-gravitational-elasticity`  
Classification: `GE19_G1_SINGLE_PASS_PREPARED_NUMERICAL_PARENT_CERTIFICATION_OPEN`

## Scientific decision, not another Ward replay

The canonical GE06+GE07+Lambda **continuum linear Ward syzygy is already proven 16/16**. G1B proves exact H3F/Repair22 H1/H1dot *nodal* identity. G1C2 replaces an invalid p-vs-dot(q) comparison and proves correct **physical** D17–H3F *nodal* diagnostics.

Researcher-uploaded frozen G1C2 result `ge19_g1c2_d17_h3f_physical_20261107.json` SHA256 **`99b21b3c52d550b3f93348b401d9abe22383c93415aeb47d56099b0742da46c4`**; associated log SHA256 **`625025bab5bf03173000ee98a4d07423457b386c7b2440ab3ac2f06036ffc9ca`**. Exact executed local classification: `GE19_G1C2_D17_H3F_COMPARABLE_PHYSICAL_FIELD_AND_X10_NODAL_DIAGNOSTIC_PASS_CONTINUOUS_OPEN`. All original initial physical field differences vanish on first node. Six-mode global relative nodal L2 max:
- `S,u,phi,T`: **`2.083331381227907e-6`**.
- `X10=Q*u+ik*phi/a`: **`2.083498430076084e-6`**.
- `X10_x`: **`1.0971121105527938e-6`**.

These relative differences are *not* absolute source norm, Euler enclosure, error-vs-exact action trajectory, original H4 shift threshold or FD4/FD8 numerical budget. Previous old G1C 8D 4.7–34.1% ratios were **invalid physical metrics** because that script compared canonical conjugate momenta `p` with `H1dot` (physical clock derivatives).

## New mathematical result: exact-rational polynomial bridge, not numerical sampling

For each of the 127 original `C_star` primary time intervals `[x_j,x_{j+1}]` and for each one of six frozen modes `m in {3,5,8,10,15,20}`, define two **precisely specified numerical representations** from the unmodified frozen D17 output:

1. `H3Fcoarse`: cubic Hermite in `x=ln(a)` defined by the original H3F action `X10` and `X10_x` at the 128 original H1 nodes, saved as `X10_original_H3F_knots` and `X10_x_original_H3F_H1dot_knots` in D17 NPZ.
2. `D17fine`: cubic Hermite in `x=ln(a)` from the D17 original-action `X10_original_action_dense_sub4` and `X10_x_original_action_dense_sub4` at 509 Radau stored nodes. Four fine intervals lie within each original H3F interval.

On fine interval `[a,b]`, both polynomials (the restriction of the coarse Hermite and the fine Hermite) are cubics. Let `d0,d1` be their complex **value** differences and `v0,v1` their **x-derivative** differences at `a,b`, with `h=b-a`. The degree-three Bernstein controls of their difference are **exactly**:

```text
B0 = d0
B1 = d0 + (h/3) v0
B2 = d1 - (h/3) v1
B3 = d1
```

Because `P(t)=sum_{k=0}^3 binom(3,k) t^k (1-t)^(3-k) Bk` and the Bernstein basis is nonnegative and sums to one for `0<=t<=1`, the convex-hull inequality gives

```text
sup_{x in [a,b]} |H3Fcoarse(x)-D17fine(x)|
     <= max_{k=0..3} |Bk|.
```

The new script evaluates `d0,d1,v0,v1` by exact rational arithmetic, interpreting all original stored binary64 real/imaginary values as exact rationals. To upper-bound each complex modulus without floating rounding, it computes the **integer square root** of `(|Re B|^2+|Im B|^2)*10^60` in exact rational arithmetic and rounds **up** to the next multiple of `10^-30`:

```text
U(B) = [floor(10^30 |B|)+1] / 10^30 > |B|, for B != 0.
```

Taking the maximum over 508 fine intervals and four controls gives an exact-input ideal-polynomial **global L_infty_x difference majorant** for each of the six modes and their common C_star domain. This is a **continuous-in-x certificate about two specified polynomial representations**, substantially stronger than comparing 128 nodes. It uses no new H1 dynamics and **no observed full H4 Ward defect**.

### What the polynomial proof does *not* certify

- Whether the D47 R5g8 error certificate uses precisely the *same fine-Hermite polynomial* as its nominal reference. The earlier D47 certification applies to its declared continuous original-action reference, not automatically to an arbitrary reconstructed polynomial.
- Whether H4F3B's actual source interpolation equals the **coarse Hermite** `X10` representation. H4F3B consumes H1/H1dot at nodes; it may use PCHIP and nonlinear Fourier operations. Identity of the source interpolation and a certified interpolation-error bound are separate obligations.
- The difference between either polynomial and the **exact continuous original-action H1**. G1C's source/theory contact, D47's original certified norm, other C tags and 40-mode pair coupling must be handled independently.
- Input floating-point storage error, original Ode/Radau integration error, physical clock conversion, Jacobian and GE05 memory/bath transfer beyond the exact stored-data polynomial statement.
- Z11 all-interval first-order Euler residual, original GE05 continuous q-node Euler contribution for **all actual H4 cohorts**, or the original D9 FD4/FD8 physical-budget `B_total`.

Thus the exact Bernstein calculation is an independently scoped **representation theorem**, not a new formal H4 G1 PASS or tolerance relaxation.

## One local execution — one decision report

New read-only `ge19/h4f3d_g1_single_pass_physical_parent_evidence.py`, commits `706f7c3` (initial), `636a3d0` (corrected Hermite h*d0 and pinned D12R3 blob). The exact rational cubic identity was checked on `f(x)=x^3` with derivatives on five points, and a separate one-mode 508-interval synthetic-performance smoke check ran; the new project script is **not yet executed on actual frozen D17/H3F NPZ files**.

The script:
- locks source Git blobs for frozen D17, H4F3B, Repair07, G1C2 and D12R3 preregistration;
- SHA-locks original D17/H3F NPZ, the executed G1B 14/14 PASS JSON and G1C2 physically comparable PASS JSON;
- computes exact-rational, all-508-subinterval Bernstein bounds of the two declared `X10` Hermite representations, rather than relying on sampled interpolation differences;
- checks original D47 R5g8 reports for `C_star`, `Nt128`, modes 3/5/8/10/15/20 with their declared continuous and endpoint flags and D17 input SHA identity;
- reads original prelocked `D55CR11F` GE05/continuous-X10 PASS, `H4F3B` corrected six-source PASS and `Repair32C` artifact Z11 PASS **in their original limited scope**. Missing results are reported as `MISSING`, never imputed;
- outputs a **single machine-readable scientific decision**, `G1_PHYSICAL_CLOSED=false`, describing precisely what is proved and what remains; does not re-evaluate actual H4 total Ward or solve Z21.

The earlier G1C check found **five local D47 JSONs** for m=3/5/8/10/15, but did not locate `d47_r5g8_primary_cstar_m20_n256_continuous_h1_final.json` in the specified directory. Absence is a provenance gap, not a physics failure; the new program deliberately retains that distinction.

## WSL runner

```bash
cd ~/aest-memory-gravity
git pull --ff-only
source .venv/bin/activate
export PYTHONPATH="$PWD"
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
mkdir -p results
set -o pipefail

python3 -u -m ge19.h4f3d_g1_single_pass_physical_parent_evidence \
  --results-dir results \
  --d47-dir results/d47_offclock_first_interval \
  --json-out results/ge19_g1_single_pass_20261108.json \
  2>&1 | tee results/ge19_g1_single_pass_20261108.log
echo "EXIT=${PIPESTATUS[0]}"

# Search only for the missing historical certificate, do NOT rerun R5g8:
find results -type f -name 'd47_r5g8_primary_cstar_m20_n256_continuous_h1_final.json' -print
```

If any SHA/source mismatch is found, stop and resolve original provenance rather than silently regenerating or substituting physical parents. The output is a **new G1 analysis report**, not the original prelocked D12R3 `B_total` and not a new H4 science certificate.

## Scientific go/no-go after the one-pass report

A **legitimate G1 PASS** requires compatible **continuous** physical Euler residual envelopes for H1, Z11 and GE05 and their boundary projections, across every H4 source cohort, with a source-representation and nonlinear memory transfer bound. G1B/G1C2 nodal checks, the polynomial representation bridge, and a previously valid D55 source/quadrature certificate are separate inputs that can help but cannot be combined into an unsupported all-sector/whole-window theorem.

If the D47 relative continuous-H1 error bound (historically reported at the few-percent scale) is too loose in the *correct original absolute norm*, the next method must specifically tighten that physics interval enclosure or establish a valid independent weak Ward theorem. Do not introduce more algebraic Cmat micro-tests, never fit a Ward error budget to observed defects and do not use the 1e-6 shift gate as a threshold for nodal `X10` relative differences.

**Unchanged:** `G1_PHYSICAL_CLOSED=false`, `G3_B_total_frozen=false`, `full_H4_Ward_certified=false`, `Z21_certified=false`, `lensing_licensed=false`.
