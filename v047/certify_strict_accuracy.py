#!/usr/bin/env python3
from pathlib import Path
import argparse, json

V046_BASELINE_MAXSIN=0.08281951252056863

ap=argparse.ArgumentParser(); ap.add_argument('input_json'); ap.add_argument('--json-out',required=True)
z=ap.parse_args()
q=json.load(open(z.input_json))
strict=float(q['max_sin_principal_angle'])
q['v047']={
  'classification':'V047_STRICT_ACCURACY_PASS' if all(q['gates'].values()) else 'V047_STRICT_ACCURACY_FOLLOWUP',
  'precision_profile':{'tol_perturb_integration':5e-8,'perturb_sampling_stepsize':0.0025},
  'v046_p2_reference_max_sin_principal_angle':V046_BASELINE_MAXSIN,
  'strict_max_sin_principal_angle':strict,
  'relative_change_vs_v046':(strict-V046_BASELINE_MAXSIN)/V046_BASELINE_MAXSIN,
  'gate_unchanged':0.05,
  'all_original_v046_gates':q['gates'],
  'purpose':'test whether the residual nuisance-projector rotation is set by CLASS numerical accuracy; no physics, parameter, stencil, or threshold retuning'
}
Path(z.json_out).write_text(json.dumps(q,indent=2)); print(json.dumps(q['v047'],indent=2))
if not all(q['gates'].values()): raise SystemExit(2)
