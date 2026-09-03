#!/usr/bin/env python3
from pathlib import Path
import json,zipfile
R=Path('results')
def load(n):
 p=R/n;return json.loads(p.read_text()) if p.exists() else {}
apply=load('apply_patch_v019_report.json');stand=load('v019_background_selftest.json');off=load('v019_off_compare.json');logs=load('v019_log_diagnostics.json');spec=load('v019_eta0_spectra.json');build=load('v019_build_report.json')
gates=[{'id':'V19-1','name':'v0.18 AeST-off zero regression retained','status':off.get('gate_status','UNKNOWN')},{'id':'V19-2','name':'Published Cosh/Exp background helper','status':stand.get('gate_status','UNKNOWN')},{'id':'V19-3','name':'AeST eta=0 CLASS compile','status':build.get('patched_build','UNKNOWN')},{'id':'V19-4','name':'Cosh/Exp full CLASS runs','status':build.get('aest_runs','UNKNOWN')},{'id':'V19-5','name':'AeST background path nontrivial','status':logs.get('gate_status','UNKNOWN')},{'id':'V19-6','name':'Regular chi_i=0 eta=0 C_l diagnostic','status':spec.get('gate_status','UNKNOWN')},{'id':'V19-7','name':'Published exact radiation-era AeST IC','status':'OPEN_NOT_IN_2021_PRL'},{'id':'V19-8','name':'Memory eta>0 CLASS states','status':'BLOCKED_UNTIL_V19_REVIEW'}]
out={'gates':gates,'scope':'First active AeST physics path in CLASS, eta=0. CDM delta/theta slots are reused for the effective AeST component; alpha and E are new states.','initial_condition_status':'chi_i=0,E_i=0 is a regular proxy only. It is not claimed as the unpublished exact AeST adiabatic radiation-era initial condition.','memory_status':'OFF: eta=0 by construction.','next':'If all executable gates pass and the spectra are physically sensible, freeze the eta=0 bridge. Then either derive exact AeST radiation ICs or add eta>0 only as a susceptibility pass, keeping the IC caveat explicit.'}
R.mkdir(exist_ok=True);(R/'MASTER_V019_REPORT.json').write_text(json.dumps(out,indent=2));lines=['AeST ETA=0 CLASS PHYSICS BRIDGE v0.19','='*86]
for g in gates:lines.append(f'{g["id"]:7s}| {g["status"]:34s}| {g["name"]}')
lines+=['','IC: '+out['initial_condition_status'],'MEMORY: '+out['memory_status'],'NEXT: '+out['next']];(R/'MASTER_V019_REPORT.txt').write_text('\n'.join(lines))
with zipfile.ZipFile('results_bundle_v019.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in sorted(R.glob('*')):
  if p.is_file():z.write(p,arcname=p.name)
print((R/'MASTER_V019_REPORT.txt').read_text());print('Created results_bundle_v019.zip')
