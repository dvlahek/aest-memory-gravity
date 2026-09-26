# GE19 H4F3d14 — original-source R1 phase-weighted signed GE05 bath: predata and static freeze

**Current status:** H4F3d14 SOURCE / SYNTHETIC STATIC PASS, actual original R1 physical output OPEN. H4F3d13 actual original signed one-sided interval bath diagnostic PASS, **first-order bath on-shell and full H4 Ward OPEN**.

## Original physical problem

Independent actual H4F3d13 analysis found the signed interval bath parent converges from original Nq2048 to Nq1024 by at most `7.661e-8` relative, but the original sampled signed FD4 bath W changes by as much as `0.0135477` relative because its interval and derivative-defect components nearly cancel. The primary C_star/Nt128/Nq2048 interval signed W is `1.41322e-12` L2 on the left, with signed FD4 derivative defect `1.36645e-12`, while the final original sampled FD4 W is `4.84224e-14`. Some high-frequency original R1 nodes have original step phases much larger than pi, but unweighted phase counts alone say nothing about their signed, source-weighted contribution.

D14 therefore measures the source-weighted phase tail before interpreting original signed-W smallness. It does **not** set `E_q10=0`, modify R1 or original GE05 action, introduce an observationally tuned gate, or assert original first-order GE05 bath on-shell.

## Frozen sources and exact original signed physics

- Immutable D13 original physical JSON SHA256 `2b4dfbd30ec6466292e0dcf62eeed8b723555d1890a127a5e0a6ff761d2ebe76`.
- Immutable D13 original physical NPZ SHA256 `1608fe98dd924b2b235ecf0f8fce768f2f3a2fa4a2854de04a56fe622ad3df89`.
- Immutable D13 postrun independent archive audit Git blob `886ac54bd7ad6f802895145fd7776f2ebd6c64d1`.
- Original Repair26 R1 full history 26,643,162-byte trace SHA256 `608ee0b4c868a701db6976f756b9a551cd9ddffe1e8e4ab37c5cd2361405a6f8`.
- Original GE05 action, original Repair24 R1 z/v state and drive X10, original H3F/H3G/Z11/Repair13 parent inputs, original FD4 time derivative, left/right interval ODE, and signed `+4 sum_j E_qj10 partial_chi q_j10` with original six `m=[3,5,8,10,15,20]` and their conjugate negative modes remain unchanged.
- Original output signed Fourier modes `m0..40` are the complete *six-input-mode convolution* but not the full Nyquist m0..64 Euler-field archive from D10r1.

The **preregistered** D14 diagnostic partitions the original R1 per-node, per-interval phase
`r_j Delta ln(a)/(tau sqrt(H_i H_{i+1}))` into `[0,.25), [.25,.5), [.5,1), [1,pi), [pi,infinity)`.
This only divides the original D7r1 `[1,infinity)` report-only bin into two and preserves all original D7r1 phase counts and original physical parent arrays.

For each bin, each original side and every original m0..40 mode/time coefficient, save **three distinct signed complex W arrays** (original interval ODE, sampled FD4 derivative defect and sampled FD4 total) and three conservative unsigned componentwise envelopes. The envelope adds absolute values of each original signed source-node/mode-pair term before summation, so it does not hide phase cancellation. Recombine all bins to reproduce the exact frozen original D13 signed interval, derivative defect and sampled FD4 arrays. Use the original same-R1-trace Nq2048 versus Nq1024 quadrature for both the signed arrays and unsigned envelopes, with both absolute and relative differences. All such differences are **report-only** and do not constitute a bath physical-smallness tolerance.

## Source and static validation

Preregistered code and frozen hashes:

| Artifact | Git blob |
| --- | --- |
| `ge19/h4f3d14_predata_original_r1_phase_weighted_signed_bath_error.json` | `321217d3661bf09fe67f1359606a5296faa4d304` |
| `ge19/h4f3d14_original_r1_source_weighted_phase_bath_partition.py` | `727a8abb63a4aaa314d09e3396d7e2fbeb03bd71` |
| `ge19/h4f3d14_actual_original_r1_source_weighted_phase_bath.py` | `cb823960e9b2cf1b82b1accd458ec75f4acf4547` |
| `ge19/run_local_h4f3d14_original_r1_source_weighted_phase_bath.sh` | `50dd92494e53dcc6adca63ab3e4ea399de4448a6` |
| `.github/workflows/ge19-h4f3d14-source-weighted-bath-static.yml` | `bd8393b6839ead2d11239ff04a4c4e91c6b7064f` |

[Static original-source signed phase-bin and unsigned-envelope CI 36225513503](https://github.com/dvlahek/aest-memory-gravity/actions/runs/36225513503) **SUCCESS**. This checks exact original source-code blobs, frozen original D13 actual-audit provenance, no-overwrite runner syntax, the independent five-bin partition and noncancelling componentwise upper bounds using synthetic signed complex GE05 states, algebraic recomposition of the original FD4 signed expression and explicit OPEN flags. CI does not have the original user-local Repair26 R1 history and did not physically run D14 on original certified backgrounds.

## Local original physical execution

```bash
cd ~/aest-memory-gravity
git checkout physics-first-gravitational-elasticity
git pull --ff-only
source .venv/bin/activate

set -o pipefail
bash ge19/run_local_h4f3d14_original_r1_source_weighted_phase_bath.sh \
  2>&1 | tee results/ge19_H4F3D14_LOCAL_runner.log
echo "EXIT=${PIPESTATUS[0]}"
```

The runner refuses any existing D14 result and SHA-checks original D13 actual JSON/NPZ, the unchanged original Repair26 trace and locked original source code. The actual physical driver also rechecks the previous D13 signed physical outputs, original frozen six-source/D6/D7r1 physical parents, original H3F/Z11/Repair13 clocks and SHA locks before saving any new result.

If executed successfully on original user-local physical inputs, provide *all four* new files: `results/ge19_h4f3d14_actual_original_r1_source_weighted_phase_bath.json`, corresponding `.npz`, `_FULL.log`, and `results/ge19_H4F3D14_LOCAL_runner.log`, for an independent postrun source/phase/noether-scope audit.

**Science STOP:** D14 does not certify the original continuous-time GE05 bath on-shell error budget, full original H4 Ward, unknown `E_i00 partial_chi F_i21`, `a E_L21` or `L21 E_L00-b21 E_b00` full action boundary. Original Repair37 SCIENCE_FAIL, original D10 FAIL and previous D10r1/D11/D12/D13 restricted PASS classifications are immutable; `Z21_certified=false`; `lensing_licensed=false`. Lensing cannot be used to tune the theoretical source.
