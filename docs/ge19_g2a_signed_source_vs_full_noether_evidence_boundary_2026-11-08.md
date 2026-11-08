# GE19 G2A — signed stage forcing is recoverable; full action Ward still requires signed Euler-state parents

**Date:** 2026-11-08. Repository `dvlahek/aest-memory-gravity`, frozen branch `physics-first-gravitational-elasticity`.

## New actually computed read-only result from previously uploaded R37-slim + Cr12abR2 final NPZ

User-provided `GE19_H4_R37_INITIAL_PARENT_SLIM.zip` and `GE19_H4_INITIAL_CONSTRAINT_EVIDENCE.zip` were directly inspected with Python. A new machine-readable report `GE19_H4_SIGNED_SOURCE_SCOPE_20261108.json` contains the original SHA-verified zip references and results below. No H4 simulation was rerun.

At frozen original C_star/primary Nt128 mode m40 beta-index1 node24 x=-0.7775878956385266:
```text
Original R37 complex shift RHS:         +8.661891918697527e-08 -1.4555159074168087e-07 i
Original R37 shift RHS magnitude:        1.6937562613479400e-07
Original R37 complex anisotropy RHS:    +1.4257665374969295e-08 +8.4848510319698460e-09 i
Stored Cr12abR2 raw shift Euler residual magnitude |Eb|: 2.7770076323913147e-13
Stored Cr12abR2 cancellation-safe shift denominator:    2.2807278924536992e-07
Frozen active normalized shift:         1.2175970845008160e-06
```

The signed R37 source at x0 is `+1.2535599816790281e-08 -2.1064410770312470e-08 i`. The original **R37 constraint source is bitwise identical across all three beta choices on the extracted nodes x0 and x24**. The **six-component final Cr12abR2 Z21 field** across beta1/beta0.5 and beta1/beta0.1 has relative L2 differences `1.552794622062892e-16` and `1.6041855363362247e-16`, respectively (primarily dominated by the huge aether component scale); this does NOT certify physical equality or remove the beta-specific input variation. Prior 120-mode beta failure masks remain identical in the frozen active mask.

**STRICT LIMITATION:** Signed complex **source** `S_b` is available, but signed complex residual `E_b=L_b w - S_b` is **not** recoverable from stored final Z21 six fields plus unsigned `|Eb|` and shift scale. The full 8D canonical states/momenta, exact physical derivatives, signed longitudinal residual `E_L` (including physical momentum time derivative), all-sector signed first-order parent `R_parent`, and signed lower boundary `B_parent` are not saved in the two uploaded original packages. Reconstructed post-elimination anisotropy is not an independent parent proof. This is an algebraic identifiability gap, not proof of action pathology. Do not infer the phase of Eb from the phase of S_b or pretend signed Ward closure.

## New read-only source recovery G2A — PREPARED, UNEXECUTED

New committed program `ge19/h4f3d_g2a_original_signed_h4_stage_source_readonly.py`, commit `c5701d90c6ae1547ac4500913a36287a33f46702`. It SHA-locks only four exact original **user-local** inputs:

- original full R37 NPZ `572d8937c1d742b10da66e34cc076377c1b2feb20b8f72eb25c3eaf31a59829f`;
- original Cr12u exact-stage GE06/GE07/Lambda/DY2 NPZ `9d85d9309c616092ab609b91dd72ea4d5d5fd5c97c851ded930a1339d340ef24`;
- original Cr12abR2 final NPZ `a12f4c1476edb1cd1c00625fffb9c2377ef63eeac1db90cbf4349f10cf278f49`;
- original unmodified Cr12abR2 source Python `6f569ba44c14f1727a020e389430decf4663385bf1389550567853e1c9ec60a9`.

It **imports the original package's `exact_source_functions` function**, reconstructing *exactly the original code's* signed complex 6 main + 2 constraint source rows at x0 and 254 fixed Radau stage points for all 40 output modes and all 3 beta choices. Source includes frozen original R37 baseline/M1 and original Cr12u Q6/Q7/Lambda/DY2 stage replacement + original Cr12abR2 sub48 M2; `x0` is inherited original R37 source as specified by original `stage_locator`. An independent single-hotspot original five-piece source sum crosschecks the result to roundoff. It emits a small original-source-only JSON and compressed signed source NPZ and never solves an H4 evolution equation, never re-integrates GE05, never adjusts coefficients. **It does not reconstruct signed Eb/EL or perform the full Noether Ward.** Therefore the output classification is intentionally `GE19_G2A_ORIGINAL_SIGNED_H4_STAGE_FORCING_RECOVERED_FULL_PARENT_WARD_OPEN`, not PHYSICAL_PASS.

### WSL (original result read only; no ODE)

```bash
cd ~/aest-memory-gravity
git pull --ff-only
source .venv/bin/activate
export PYTHONPATH="$PWD"
export OPENBLAS_NUM_THREADS=1
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
mkdir -p results
set -o pipefail

python3 -m py_compile ge19/h4f3d_g2a_original_signed_h4_stage_source_readonly.py &&
python3 -u -m ge19.h4f3d_g2a_original_signed_h4_stage_source_readonly \
  --json-out results/ge19_g2a_Cstar_allmodes_signed_h4_stage_source.json \
  --npz-out results/ge19_g2a_Cstar_allmodes_signed_h4_stage_source.npz \
  2>&1 | tee results/ge19_g2a_Cstar_allmodes_signed_h4_stage_source.log
echo "EXIT=${PIPESTATUS[0]}"
```

**Mathematical caveat:** finite exact-stage forcing samples are not a uniquely defined differentiable physical forcing between stages. Thus a stage-value comparison is *not a substitute* for the full continuous Noether relation `d_t Eb = Rparent - i k(a EL+Bparent)`. An independently specified common source extension, actual signed canonical Euler residuals and a verified FD4/FD8+roundoff/parent error budget remain necessary. If no signed canonical stages are stored, a strictly no-replay protocol cannot compute actual `Eb` phases; stop and explicitly report that identifiability limit rather than fabricating Ward closure or launching a long numerics repair campaign.

All original frozen science statuses immutable: D55Cr11f Cstar H-channel bath GE05 PASS in its scope; Cr12abR2 `IMPLEMENTATION_FAIL` (two M2 nested monotonicity failures) plus original `1.2175970845e-6 >1e-6` active H4 shift SCIENCE FAIL; Cr12ad formal campaign closeout. No certified full H4 Ward, Z21 or lensing. No observational tuning or threshold relaxation.
