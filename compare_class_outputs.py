#!/usr/bin/env python3
from pathlib import Path
import argparse, json, math

ap=argparse.ArgumentParser()
ap.add_argument("pristine_output")
ap.add_argument("patched_output")
ap.add_argument("--rtol",type=float,default=2e-13)
ap.add_argument("--atol",type=float,default=1e-30)
ap.add_argument("--json-out",default="results/off_baseline_compare.json")
args=ap.parse_args()

def load_numeric(path):
    rows=[]
    for raw in path.read_text(errors="replace").splitlines():
        line=raw.strip()
        if not line or line.startswith("#"):
            continue
        vals=[]
        for token in line.split():
            vals.append(float(token))
        rows.append(vals)
    return rows

def numeric_compare(pa,pb):
    xa=load_numeric(pa); xb=load_numeric(pb)
    if len(xa)!=len(xb):
        return {"numeric_ok":False,"rows_a":len(xa),"rows_b":len(xb)}
    max_abs=0.0; max_rel=0.0
    for i,(ra,rb) in enumerate(zip(xa,xb)):
        if len(ra)!=len(rb):
            return {"numeric_ok":False,"row":i,"cols_a":len(ra),"cols_b":len(rb)}
        for j,(va,vb) in enumerate(zip(ra,rb)):
            if math.isnan(va) and math.isnan(vb):
                continue
            if math.isinf(va) or math.isinf(vb):
                if va!=vb:
                    return {"numeric_ok":False,"row":i,"col":j,"a":va,"b":vb}
                continue
            diff=abs(va-vb)
            scale=max(abs(va),abs(vb),args.atol)
            rel=diff/scale
            max_abs=max(max_abs,diff); max_rel=max(max_rel,rel)
            if diff>args.atol+args.rtol*max(abs(va),abs(vb)):
                return {"numeric_ok":False,"row":i,"col":j,"a":va,"b":vb,
                        "max_abs":max_abs,"max_rel":max_rel}
    return {"numeric_ok":True,"max_abs":max_abs,"max_rel":max_rel}

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
            rec.update(numeric_compare(fa[name],fb[name]))
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
