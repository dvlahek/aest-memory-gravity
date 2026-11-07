# GE19 G1C — correct physical interpretation of D17–H3F bridge (2026-11-07)

**Classification:** `GE19_G1C_ORIGINAL_8D_MOMENTUM_DERIVATIVE_COMPARISON_INVALID_DIAGNOSTIC_ONLY_G1C2_PREPARED`  
**Status:** local G1C completed and original source/file locks PASS, but its *8D numerical difference* used non-equivalent quantities, and **one D47 certificate file was missing locally**. No physical H4 or G1 interval certification promoted.

## Frozen local evidence from user's completed G1C

- `results/ge19_g1c_d17_h3f_bridge_20261107.json` SHA-256 `378b5cc59bd22babaa9e1f8e775b30a1fc4b50dd20d021b2f1492932e17500c2`, 14,631 bytes.
- `results/ge19_g1c_d17_h3f_bridge_20261107.log` SHA-256 `6df9f91eea5294aac89e411b7818cfca27ff3ae28d0f06bd42db75857d3dd537`, 872 bytes.
- Original classification `GE19_G1C_D17_H3F_NODAL_BRIDGE_EXACT_SOURCE_PASS_D47_CERT_PROVENANCE_INCOMPLETE`.
- D17 NPZ SHA256 `cd3bcf8cf5ac9ab14385baa4d90bd53400daae9f2bb89d4d22bfa2a581846359`; H3F NPZ SHA256 `90840755fa9febb1d8cb84609d9e58f67dec2a0a01cd6bf8e47685b45caa4542`.
- Six source blob checks and all source bindings PASS; original H3F clock exactly embedded in D17's original dense clock.
- D47 R5g8 primary Cstar N256 m=3,5,8,10,15 JSON reports present: classification exact, `case_mode_continuous_H1_error_enclosed=true`, and original D17 NPZ SHA present in each report. The m20 report `d47_r5g8_primary_cstar_m20_n256_continuous_h1_final.json` was **absent from the specified local directory**, not a demonstrated failure of that certification. Therefore only 5/6 locally verified.

## G1C implementation bug: non-equivalent 8D variables

The G1C script assembled

```text
H3F8 = [H1(S,u,phi,T), H1dot(Sdot,udot,phidot,Tdot)]
D17Y = [D17(S,u,phi,T), D17(pS,pu,pphi,pT)]
```

then compared `D17Y - H3F8` as if these eight entries represented the same physical state. This is **invalid**: in frozen `ge19/repair07_window_retarded_reduced_h3_z20_particular.py`,

```text
w[6:10] = v0 = (Sdot, udot, phidot, Tdot)
p = Cmat[0:4] @ w
y0 = concatenate([q0, p])   # p is canonical conjugate momentum
```

Thus *even at the initial node*, `p-physical_time_dot(q)` need not be zero. The source-derived D17 canonical state definition is correct; the **new bridge test comparison was wrong**, not the frozen D17 or H3F data.

G1C's reported 8D `global_relative_L2_difference_at_nodes` values

```text
m=3:  0.047333536
m=5:  0.090376390
m=8:  0.143818341
m=10: 0.178668965
m=15: 0.262736041
m=20: 0.341247716
```

are descriptive values of **incommensurate variables**, and MUST NOT be described as physical H1 trajectory discrepancies, G1 parent Euler defects, Ward evidence or D47 theorem invalidation. They are not eligible for an error budget, not even as conservative H1 physical bounds.

Indeed the same G1C JSON's componentwise maximum **physical field** deltas are much smaller in absolute units:

```text
                     S             u           phi             T
m=3      4.00e-14     6.46e-08    1.13e-14     1.13e-10
m=5      3.40e-14     3.96e-07    9.57e-15     9.57e-11
m=8      1.84e-14     1.25e-06    5.19e-15     5.19e-11
m=10     1.29e-14     2.20e-06    3.62e-15     3.62e-11
m=15     8.35e-15     6.66e-06    2.35e-15     2.35e-11
m=20     3.68e-15     8.74e-06    1.03e-15     1.04e-11
```

These are **nodal absolute differences only**, measured in the original physical component normalization; their small numerical sizes are not an interval certificate and must not be compared to the original 1e-6 H4 shift tolerance without an independently justified physical map and norms. In particular the aether `u` difference could matter because the actual `X10=Q u + i k phi/a` involves the model coefficient Q.

## Correct next test: G1C2 versioned, no new solver

A separately versioned read-only `ge19/h4f3d_g1c2_d17_h3f_physical_field_bridge.py` (commit `f1f3a9aa322f1522b5355667013019a4a4a5104a`) replaces this logically invalid comparison with **only matching original physical variables**:

1. `D17Y[0:4,::4]` against `H3F H1[[1,2,3,4],:]` for the six primary/`C_star` modes on the original Nt128 nodes.
2. D17 original-action `X10` vs original H3F `X10` calculated on those same nodes, both frozen in the D17 NPZ.
3. Original D17 physically source-derived `X10_x` vs H3F `X10_x` from original H1dot endpoint jets (not canonical momenta).
4. Locks original D17 and H3F SHA256, original Repair07 canonical state definition, source code ancestry and output layout.

G1C2 contains **no D47 numerical integration**, does not read/alter the old G1C report and does not replace D47's frozen norm/relative scale. It is NOT yet locally executed.

Safe WSL:

```bash
cd ~/aest-memory-gravity
git pull --ff-only
source .venv/bin/activate
export PYTHONPATH="$PWD"
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
set -o pipefail

python3 -u -m ge19.h4f3d_g1c2_d17_h3f_physical_field_bridge \
  --results-dir results \
  --json-out results/ge19_g1c2_d17_h3f_physical_20261107.json \
  2>&1 | tee results/ge19_g1c2_d17_h3f_physical_20261107.log
echo "EXIT=${PIPESTATUS[0]}"
```

Find missing D47 m20 certificate **without regenerating or substituting**:

```bash
find results -type f -name '*r5g8*m20*n256*json' -print
```

Do not interpret absence from a directory as failure of certified physics. If the exact report exists at another path, check classification, source NPZ SHA and `case_mode_continuous_H1_error_enclosed` before using it.

## Hard scientific claim boundary

- G1B 14/14 H3F vs Repair22 **same arrays** remains a real PASS.
- Original G1C lineage provenance with five D47 reports remains useful.
- Original G1C 8D percentages are **invalid physical metrics** and are explicitly superseded for scientific interpretation by G1C2; preserve old JSON/log as historical evidence.
- Even an exact G1C2 nodal physical-field match **does not** certify off-clock `H3F(x)`, all-interval original Euler residuals or transfer of D47 enclosure.
- G1 Z11 continuous Euler, G3 physical FD4/FD8 budget, H4 Noether, Z21 and lensing remain OPEN; no source tuning or altered science gates.

```text
G1C2_PHYSICAL_NODAL_METRICS_VERIFIED = false
D47_CSTAR_PRIMARY_N256_ALL_SIX_LOCALLY_PRESENT = false
G1C_D47_TO_H3F_ALL_INTERVAL_TRANSFER_CERTIFIED = false
FULL_H4_WARD_CERTIFIED = false
Z21_CERTIFIED = false
LENSING_LICENSED = false
```
