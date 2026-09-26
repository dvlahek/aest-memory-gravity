# GE19 H4F3d13 — original R1 signed one-sided bath parent: predata and static freeze

**Static classification:**
`GE19_H4F3D13_ORIGINAL_R1_SIGNED_BATH_STATIC_PASS_ACTUAL_PHYSICAL_OPEN`.

H4F3d12 is now archived in the GitHub branch with original
byte-exact prereg, failed r0, corrected r1, unchanged manifest
and the original D11-derived JSON losslessly in gzip.
Its original conditional background `E00*dchi F21` coefficient
is **not** a full H4 Ward smallness certificate.

The next original unclosed contribution is the GE05
memory-bath **actual** signed first-order parent
`+4 sum_j E_qj10*dchi q_j10`. The previous physical
H4F3d6 signed parent exists with original sampled
`H*FD4_ln(a)` derivative. H4F3d7r1 independently
decomposed its original per-node FD4 residual into
original R1 step **left/right** interval ODE residual
and the sampled derivative defect, but saved only
per-mode time norms of each. Time-norm arrays cannot
recover the phases needed for the signed mixed parent.
H4F3d13 reconstructs the original signed product
from **actual complex node/mode fields**, retaining
both original interval sides. It does not assume
a small bath Euler residual.

## Pre-registered exact physics and original parents

- Original GE05 per-node action:
  `NLR^2 [(A^mu d_mu q)^2-(omega q-sqrt(w) Xphi)^2]/4`.
- Original normalized R1 variables
  `omega_j=r_j/tau`,
  `q_j10=sqrt(w_j)/omega_j * z_j10`,
  `J_j=a^3 v_j10/tau`.
- Original sampled FD4 residual
  `R_j,FD4=H*FD4_ln(a)(J_j)+a^3 omega_j^2(z_j10-X10)`
  and original action Euler
  `E_qj10=-sqrt(w_j)/(2omega_j)*R_j,FD4`.
- For the exact frozen Repair24 interval step
  `h_mid(i)=sqrt(H_i H_{i+1})`, retain both
  distinct one-sided original R1 residuals
  `R_right(i)` and `R_left(i+1)`.
  The initial right and final left endpoint
  are retained; do not average two sides
  at an interior shared node.
- Convert each one-sided `R` to the original
  `E_qj10` and calculate **all positive and
  negative mode combinations** of
  `4 sum_j E_qj10*dchi q_j10` on original output
  `m=0..40`, original six input positive modes
  `3,5,8,10,15,20` and original `kfund`.
  The original sampled FD4 signed Ward
  and the original finite-difference derivative
  defect are separately archived at matching
  left/right times. Their sum is compared
  to original saved D6 FD4 signed bath Ward.
- Actual grid scope is all
  `C_min,C_star,C_max x Nt128,Nt64`
  with original `Nq2048` R1 history and
  independent `Nq1024` report-only quadrature
  control. Original D7r1 mode-time interval
  norms are verified in the Nq2048 cohort;
  no original per-node phase is reconstructed
  from saved norms.

**Original frozen physical hashes (unchanged):**
D6 JSON `4607edde17c6820c85f32c0bbd774d5a58148eb01bfd0c81ce592e8c1b907791`,
NPZ `17b50c6ee584b2a8886f7114a90ea9396a127172dd9e02976b0e6275fe2fedc0`;
D7r1 JSON `031229d570d29ae9c4ea0ab8e25222d94e9cda4520c991cd203e9d7b97e01dc9`,
NPZ `4f011c96c2c11165df6332eafc459c5d2c5e7bc5164a436bde3d1563696f0e13`;
actual H4F3b source JSON
`1ec88fd3fd6b81bf30614b0cb78d722a02dd4f745e1f22cb9b8f956a44bac6c1`,
NPZ `787d5d177838b05078057aa932f379dd529449ce203f5664c36cf723acb0116b`;
original Repair26 R1 history SHA
`608ee0b4c868a701db6976f756b9a551cd9ddffe1e8e4ab37c5cd2361405a6f8`,
26,643,162 bytes. The local runner and physical
driver independently require these exact bytes
before any new physical output.

## New source/runner and static proof

- Prereg `ge19/h4f3d13_predata_original_r1_interval_signed_bath_parent.json`,
  Git blob `ec07d6be5c267dcbbdb05395ea81cc5e7405781e`.
- Pure source-bound one-sided Euler/signed
  assembly `ge19/h4f3d13_original_r1_interval_signed_bath_assembly.py`,
  blob `64641d11c34a729508dbfa29d2fe65ccae3a031a`.
- Actual original-parent driver
  `ge19/h4f3d13_actual_original_r1_signed_interval_bath_parent.py`,
  blob `5cce06a82869d5b7ff70c12a92e70b9257073c42`.
- No-overwrite isolated user-local physical runner
  `ge19/run_local_h4f3d13_original_r1_signed_interval_bath_parent.sh`,
  blob `3eca153fb847aaa147be88a3c0ca21873f352b3c`.
- [Dedicated GitHub static CI run 36224232492](https://github.com/dvlahek/aest-memory-gravity/actions/runs/36224232492)
  completed **SUCCESS**. Its numerical test
  imports only AST-selected pinned original D6
  `fd4` and signed-convolution methods to avoid
  historical module-level result writers; it
  independently tests left/right exact R1
  interval Euler versus sampled FD4 defect,
  exact signed `+/-` mode convolution,
  negative control dropping negative modes,
  actual driver Python AST, frozen original
  source blobs and local runner `bash -n`.
  The static run uses manufactured arrays only.

**These static results do not verify the
actual R1 physical data.** The original
Repair26 R1 trace is private/local; GitHub CI
does not possess it. A physical `PASS` is
permitted only after actual original node/mode
data and original saved D6/D7r1 bytes are
hash-locked by the new local runner. All
source/identity gate tolerances are inherited
from frozen original D7r1, not fitted to a
new physical `E_q10` on-shell threshold.

## Next real physical execution

```bash
cd ~/aest-memory-gravity
git checkout physics-first-gravitational-elasticity
git pull --ff-only
source .venv/bin/activate

set -o pipefail
bash ge19/run_local_h4f3d13_original_r1_signed_interval_bath_parent.sh \
  2>&1 | tee results/ge19_H4F3D13_LOCAL_runner.log

echo "EXIT=${PIPESTATUS[0]}"
```

For an independently audited physical outcome
save/upload the four new files:
`results/ge19_h4f3d13_actual_original_r1_signed_interval_bath_parent.json`,
`results/ge19_h4f3d13_actual_original_r1_signed_interval_bath_parent.npz`,
`results/ge19_h4f3d13_actual_original_r1_signed_interval_bath_parent_FULL.log`,
`results/ge19_H4F3D13_LOCAL_runner.log`.
If the original local runner fails, keep its
failure and any partial artifacts; use a separate
versioned implementation-only repair rather
than rewriting original results or changing
the frozen source.

**Full original bath-on-shell error budget is
OPEN. Actual original F21 and L21/b21 lower
action boundary are OPEN. Complete integrated
H4 Noether, certified Z21 and lensing remain
BLOCKED. Repair37 SCIENCE_FAIL immutable.
No observational tuning.**
