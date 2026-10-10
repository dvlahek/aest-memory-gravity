# GE19 D18 source-action Bernstein canonical H1 diagnostic

This package continues the frozen D17 canonical H1 reconstruction. **D18 does not certify true original H1**: it computes a mathematically justified quartic Bernstein residual envelope for an **affine endpoint-operator surrogate**, checks the action operator at every fine-interval midpoint only as a sampled difference, and reports affine-only Grönwall growth in log space. Real source-operator curvature and outward floating-point enclosures remain absent.

The runner is non-overwriting, source-hash locked and requires all frozen D17/D16R1 original files in the local physics-first branch. It does not edit any original source. The old D17 JSON and NPZ must have the exact SHA-256 recorded in the preregistration.

After copying this ZIP into `~/aest-memory-gravity`:

```bash
cd ~/aest-memory-gravity
unzip -n ge19_h4f3d18_source_action_Bernstein_conditional_package.zip \
  'ge19/*' 'docs/*' D18_SOURCE_MANIFEST.json README_D18.md
source .venv/bin/activate
set -o pipefail
bash ge19/run_local_h4f3d18_source_action_Bernstein_conditional_H1.sh \
  2>&1 | tee results/ge19_H4F3D18_LOCAL_runner.log
echo "EXIT=${PIPESTATUS[0]}"
```

**Important:** no existing repository source or README is overwritten. The new D18 files are SHA-locked, while original parents remain Git-locked; no Git commit is required for the D18 execution.

Send back the D18 runner log, JSON and NPZ. Preserve any failed log without rerunning over prior outputs.
