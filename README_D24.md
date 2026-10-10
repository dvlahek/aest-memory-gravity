# GE19 D24 — original-action dense-H1 H3 first-interval source-resolution test

D23 projected the original-action H2 initial momentum and reduced the local
Z11 shift residual to about 1.62e-8. D23 also found a nonzero H3 shift
constraint derivative during the first step even though its initial source-aware
boundary passes. The original D22A source is sampled on Nt128 and interpolated
by PCHIP at the Radau stages. D24 directly evaluates the same frozen nonlinear
source on the first nine sub4 D17 original-action H1 knots (two Nt128 intervals)
using the source's native FD4 on the dense representation, then repeats **only
one** Radau step for each of the three preregistered (mode,beta) controls:
(14,0.1), (1,1), (40,0.1).

All source expressions, GE06/GE07/Lambda/Y rows, physical clock and original
linear operator remain locked. Initial source-aware momentum projection is
recomputed for the alternative dense source. The old coarse first-step Radau
is independently replayed and must reproduce the D23 forensic result.

This is an intentionally decisive numerical **diagnostic**, not certification
of original-action nonlinear continuum sources. FD4 on 9 dense nodes remains
an approximation; D17 H1 is numerical. D22A FAIL and Repair37 SCIENCE_FAIL are
immutable. No q20, H4, Z21, lensing or observational tuning.

Copy ZIP to `~/aest-memory-gravity`, unzip it and execute:

```bash
cd ~/aest-memory-gravity
unzip -n ge19_h4f3d24_dense_first_interval_H3_source_resolution_package.zip \
  'ge19/*' README_D24.md D24_SOURCE_MANIFEST.json
source .venv/bin/activate
mkdir -p results
set -o pipefail
bash ge19/run_local_h4f3d24_dense_first_interval_H3_source_resolution.sh \
  2>&1 | tee results/ge19_H4F3D24_LOCAL_runner.log
echo "EXIT=${PIPESTATUS[0]}"
```

Outputs:
`results/ge19_h4f3d24_dense_first_interval_H3_source_resolution.json`,
`.npz`, `_FULL.log`, and the runner log.
The short nine-knot H3 source cannot be inserted into a full Nt128 solve.
