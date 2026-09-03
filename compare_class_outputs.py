#!/usr/bin/env python3
from pathlib import Path
import argparse, json
import numpy as np

ap=argparse.ArgumentParser()
ap.add_argument("pristine_output")
ap.add_argument("patched_output")
ap.add_argument("--rtol",type=float,default=2e-13)
ap.add_argument("--atol",type=float,default=1e-30)
ap.add_argument("--json-out",default="results/off_baseline_compare.json")
args=ap.parse_args()

a=Path(args.pristine_output); b=Path(args.patched_output)
fa={p.name:p for p in a.glob("*.dat")}
fb={p.name:p for p in b.glob("*.dat")}
common=sorted(set(fa)&set(fb))
missing_a=sorted(set(fb)-set(fa)); missing_b=sorted(set(fa)-set(fb))
details={}; all_ok=(not missing_a and not missing_b and len(common)>0)

for name in common:
    ba=fa[name].read_bytes(); bb=fb[name].read_bytes()
    exact=(ba==bb)
    rec={"byte_identical":exact}
    if exact:
        rec.update(max_abs=0.0,max_rel=0.0,numeric_ok=True)
    else:
        try:
            xa=np.loadtxt(fa[name]); xb=np.loadtxt(fb[name])
            if xa.shape != xb.shape:
                rec.update(numeric_ok=False,shape_a=list(xa.shape),shape_b=list(xb.shape))
            else:
                diff=np.abs(xa-xb)
                denom=np.maximum(np.abs(xa),args.atol)
                rec["max_abs"]=float(np.max(diff))
                rec["max_rel"]=float(np.max(diff/denom))
                rec["numeric_ok"]=bool(np.allclose(xa,xb,rtol=args.rtol,atol=args.atol,equal_nan=True))
        except Exception as e:
            rec.update(numeric_ok=False,error=str(e))
    all_ok &= bool(rec["numeric_ok"])
    details[name]=rec

out={
 "common_dat_files":common,
 "missing_from_pristine":missing_a,
 "missing_from_patched":missing_b,
 "all_outputs_equivalent":bool(all_ok),
 "rtol":args.rtol,"atol":args.atol,
 "details":details,
 "gate_status":"PASS" if all_ok else "FAIL"
}
op=Path(args.json_out); op.parent.mkdir(parents=True,exist_ok=True); op.write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
raise SystemExit(0 if all_ok else 1)
