#!/usr/bin/env python3
from pathlib import Path
import json, zipfile

R=Path("results")
def load(n):
    p=R/n
    return json.loads(p.read_text()) if p.exists() else {}

apply=load("apply_patch_report.json")
off=load("off_baseline_compare.json")
selftest=load("module_selftest.json")
build=load("build_report.json")

gates=[
 {"id":"V18-1","name":"Pinned CLASS target/version","status":"PASS" if apply.get("target_version")=="v3.3.4" else "UNKNOWN"},
 {"id":"V18-2","name":"Standalone AeST-memory module self-test","status":selftest.get("gate_status","UNKNOWN")},
 {"id":"V18-3","name":"Pristine official CLASS build","status":build.get("pristine_build","UNKNOWN")},
 {"id":"V18-4","name":"Patched CLASS build and linked module","status":build.get("patched_build","UNKNOWN")},
 {"id":"V18-5","name":"AeST OFF zero-regression outputs","status":off.get("gate_status","UNKNOWN")},
 {"id":"V18-6","name":"AeST eta=0 CLASS physics path","status":"NEXT_V019"},
 {"id":"V18-7","name":"Memory C_l","status":"BLOCKED_AFTER_V019"}
]
out={
 "target":{"version":"v3.3.4","sha":"e85808324f51fc694d12e3ed7439552a3c3f9540"},
 "gates":gates,
 "scope":"Compile/link and zero-regression only; physics path remains deliberately inactive.",
 "next":"v0.19 wires Cosh/Exp AeST background and eta=0 scalar perturbation states into CLASS."
}
R.mkdir(exist_ok=True)
(R/"MASTER_V018_REPORT.json").write_text(json.dumps(out,indent=2))
lines=["AeST MEMORY CLASS PATCH v0.18","="*80]
for g in gates:
    lines.append(f'{g["id"]:7s}| {g["status"]:30s}| {g["name"]}')
lines += ["","NEXT: "+out["next"]]
(R/"MASTER_V018_REPORT.txt").write_text("\n".join(lines))
with zipfile.ZipFile("results_bundle_v018.zip","w",zipfile.ZIP_DEFLATED) as z:
    for p in sorted(R.glob("*")):
        if p.is_file(): z.write(p,arcname=p.name)
print((R/"MASTER_V018_REPORT.txt").read_text())
print("Created results_bundle_v018.zip")
