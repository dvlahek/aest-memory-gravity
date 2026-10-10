# D23 — One targeted action-constraint boundary and transport decision

D22R3 proved that the original Repair28 R2 physical tangent and the previous
Z11 initial jet are numerically equivalent. Repeating that solve unchanged
would not fix the D22A shift failure. D23 takes a different path, without
new bath quadrature, H3 source generation or a new 40-mode Z20 solve.

**H2 / Z11:** Retain the genuine SHA-verified Repair28 R2 first-order tangent
from D22R3 as an independent reference. At the original-action initial knot,
form the exact nonzero-`q=(S,u,phi,T)` affine canonical lapse and shift rows.
Use the *unchanged* Repair18 doubly-equilibrated min-norm solver on the
canonical momentum correction `delta p`, not the historical zero-q source
boundary. Check lapse, shift and anisotropy with the unchanged 1e-6 local
backward-error gate. Record physical `qdot` and `p` deviation from the R2
reference. If the initial projection passes, integrate only the six Z11
modes to test subsequent constraint propagation. The correction has NO
certified independent R2 uncertainty budget, so the output remains an
uncertified numerical diagnostic even if the gates pass.

**H3 / Z20:** Without reintegration, reconstruct the canonical shift defect
`g=C_shift(WY*y+WR*S)-S_shift` and its first-interval time derivative under
the frozen original-action operator and actual archived H3F source PCHIP.
Use the archived failed `beta=0.1, m=14` first step plus m1/m40 controls,
with two right-difference steps for derivative stability. Reproduce the
frozen D22AR2 worst-node value to catch accidental mode/source swaps.
This is a necessary constraint-transport diagnostic, not proof of full
source Ward/Noether identity. It does not change the original H3 source.

No claims of physical H2/H3 certification, q20/B20, H4 Ward, Z21,
lensing, or observations. The frozen D22A SCIENCE FAIL is unchanged.

The package reads D22A and D22R3 actual JSON/NPZ already in results;
**the Repair28 R2 file is not searched or required again** because the
fresh true-R2 reference is already SHA-bound inside the D22R3 archive.

Run from the project root after copying this ZIP there:

```bash
cd ~/aest-memory-gravity
unzip -n ge19_h4f3d23_action_constraint_boundary_transport_package.zip \
  'ge19/*' README_D23.md D23_SOURCE_MANIFEST.json 'docs/*'
source .venv/bin/activate
mkdir -p results
set -o pipefail
bash ge19/run_local_h4f3d23_action_constraint_boundary_transport.sh \
  2>&1 | tee results/ge19_H4F3D23_LOCAL_runner.log
echo "EXIT=${PIPESTATUS[0]}"
```

Upload `results/ge19_h4f3d23_action_constraint_boundary_transport.json` and
`results/ge19_H4F3D23_LOCAL_runner.log` after this one run. NPZ is optional
for initial diagnosis; keep it for subsequent physical reclosure.
