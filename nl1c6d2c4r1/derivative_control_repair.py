#!/usr/bin/env python3
from __future__ import annotations

import argparse, json, sys
from pathlib import Path
import subprocess

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))

from nl1c6d2c4 import derivative_bounded_completion_identity_audit as d4

PASS="NL1C6D2C4R1_DERIVATIVE_CONTROL_REPAIR_PASS"
FAIL="NL1C6D2C4R1_DERIVATIVE_CONTROL_REPAIR_FAIL"
HZ_SET=(1e-3,3e-4,1e-4)


def git_meta():
    try:
        h=subprocess.check_output(["git","rev-parse","HEAD"],text=True).strip()
        b=subprocess.check_output(["git","rev-parse","--abbrev-ref","HEAD"],text=True).strip()
    except Exception:
        h,b="unknown","unknown"
    return h,b


def derivative_repair():
    worst_y=0.0; worst_z=0.0; worst_y_case=None; worst_z_case=None
    per_step={str(h):0.0 for h in HZ_SET}
    all_ok=True
    for b in d4.BETAS:
      for kind in d4.KINDS:
       for sigma in d4.SIGMAS:
        for x in (1e-2,0.2,1.0,10.0,1e2):
          xt=(1+b)/b
          if kind=="sharp" and abs(x-xt)/xt<1e-3: continue
          y=x*x; Y=d4.Y0*y; z=0.7
          hy=max(1e-7*max(y,1.0),1e-9)
          if y<=hy: continue
          fy_num=(d4.F(d4.Y0*(y+hy),z,b,kind,sigma)-d4.F(d4.Y0*(y-hy),z,b,kind,sigma))/(2*hy)
          ey=d4.norm_err(fy_num,d4.Y0*d4.FY(Y,z,b,kind,sigma),d4.A*d4.Y0*1e-12)
          if ey>worst_y: worst_y,worst_y_case=ey,["FY",b,kind,sigma,x,hy]
          all_ok=all_ok and ey<=d4.FD_GATE

          for hz in HZ_SET:
            fq_num=(d4.F(Y,z+hz,b,kind,sigma)-d4.F(Y,z-hz,b,kind,sigma))/(2*hz)
            e=d4.norm_err(fq_num,d4.Z0*d4.FQ(Y,z,b,kind,sigma),d4.A*d4.Y0*1e-12)
            per_step[str(hz)]=max(per_step[str(hz)],e)
            if e>worst_z: worst_z,worst_z_case=e,["FQ",b,kind,sigma,x,hz]
            all_ok=all_ok and e<=d4.FD_GATE

            fyq_num=(d4.FY(Y,z+hz,b,kind,sigma)-d4.FY(Y,z-hz,b,kind,sigma))/(2*hz)
            e=d4.norm_err(fyq_num,d4.Z0*d4.FYQ(Y,z,b,kind,sigma),d4.A*1e-12)
            per_step[str(hz)]=max(per_step[str(hz)],e)
            if e>worst_z: worst_z,worst_z_case=e,["FYQ",b,kind,sigma,x,hz]
            all_ok=all_ok and e<=d4.FD_GATE

    return {
        "Y_direction_max_relative_discrepancy":worst_y,
        "Y_direction_worst_case":worst_y_case,
        "Z_direction_max_relative_discrepancy":worst_z,
        "Z_direction_worst_case":worst_z_case,
        "Z_step_maxima":per_step,
        "gate":d4.FD_GATE,
        "pass":bool(all_ok),
    }


def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--json-out",default="results/nl1c6d2c4r1_derivative_control_repair.json"); args=ap.parse_args()
    h=d4.homogeneous(); t=d4.tracking(); deep=d4.deep_mond(); cb=d4.constitutive_bound(); hg=d4.high_gradient(); fd=derivative_repair()
    gates={
        "R1_C4_1_homogeneous":h["pass"],
        "R1_C4_2_tracking_EL_slice":t["pass"],
        "R1_C4_3_deep_MOND":deep["pass"],
        "R1_C4_4_local_constitutive_bound":cb["pass"],
        "R1_C4_5_high_gradient_recovery":hg["pass"],
        "R1_derivative_control_all_fixed_steps":fd["pass"],
        "R1_scope_clean":True,
    }
    passed=all(gates.values()); cls=PASS if passed else FAIL; head,branch=git_meta()
    result={"classification":cls,"git":{"head":head,"branch":branch},"homogeneous":h,"tracking":t,"deep_MOND":deep,"constitutive_bound":cb,"high_gradient":hg,"derivative_repair":fd,"gates":gates,"historical_D2C4_classification_unchanged":True,"nonlinear_FLRW_evolved":False,"solver_changed":False,"memory_or_likelihood_evaluated":False,"branch_selection_performed":False,"action_derivation_licensed":passed}
    out=Path(args.json_out); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print("NL1C6D2C4R1_DERIVATIVE_CONTROL_REPAIR_START")
    print(f"R1_STRUCT background={h['pass']} tracking={t['pass']} deep={deep['pass']} bound={cb['pass']} high={hg['pass']}")
    print(f"R1_FD_Y max={fd['Y_direction_max_relative_discrepancy']:.12e} pass={fd['Y_direction_max_relative_discrepancy']<=d4.FD_GATE}")
    for hz in HZ_SET:
        e=fd['Z_step_maxima'][str(hz)]
        print(f"R1_FD_Z h={hz:.1e} max={e:.12e} pass={e<=d4.FD_GATE}")
    print(f"R1_FD_Z_WORST max={fd['Z_direction_max_relative_discrepancy']:.12e} case={fd['Z_direction_worst_case']}")
    print(f"CLASSIFICATION={cls}")
    print(f"ACTION_DERIVATION_LICENSED={passed}")
    print(f"JSON={out}")
    print("NL1C6D2C4R1_DERIVATIVE_CONTROL_REPAIR_END")
    return 0 if passed else 2

if __name__=="__main__": raise SystemExit(main())
