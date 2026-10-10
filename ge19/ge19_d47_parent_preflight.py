#!/usr/bin/env python3
"""D47 read-only parent/provenance preflight. No H1 evolution or physics certification."""
import argparse, hashlib, json, os, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
EXPECTED={
 'ge19_h4f3d22a_actual_Cstar_action_B10_Z11_Z20_parent_candidates.npz':'6952a2cde9a39367d29b75b63aca53a97a8feb622e7cbe7b33a468ae2b9a1632',
 'ge19_repair13_self_consistent_reduced_background_h1_reclosure.npz':'011c0ae54fd21d70c0e2c695ce62e7b74a3c5529a07c9023c882a447d5b40ca3',
 'ge19_h4f3d33_direct_ge07_paired_first_interval.npz':'41c75b883b7df7b1f57b72f0309d71e1c7c3779f291e524f33fa7532861eb264',
 'ge19_h4f3d45_h1_offclock_source_audit.npz':'44757665c4c058ae10a9dca28aa6d58a4a71bec081eecdc7abddb3f82ae67796',
}
SCRIPTS=['ge19/h4f3d33_direct_ge07_paired_first_interval.py','ge19/h4f3d45_h1_offclock_source_audit.py','ge19/h4f3d46r1_source_interpolation_counterfactual.py']
def digest(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
 return h.hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--results',default='results');args=ap.parse_args()
 if Path.cwd().resolve()!=ROOT.resolve():raise SystemExit('D47_PREFLIGHT_WRONG_WORKDIR')
 rd=ROOT/args.results
 report={'classification':'GE19_D47_READ_ONLY_PARENT_PREFLIGHT','physics_certified':False,'original_action_modified':False,'parent_files':{},'source_scripts':{},'missing':[],'sha_mismatch':[]}
 for name,want in EXPECTED.items():
  p=rd/name
  if not p.is_file():report['missing'].append(str(p));continue
  got=digest(p);report['parent_files'][name]={'sha256':got,'expected':want,'match':got==want,'size_bytes':p.stat().st_size}
  if got!=want:report['sha_mismatch'].append(name)
 for name in SCRIPTS:
  p=ROOT/name
  if not p.is_file():report['missing'].append(str(p));continue
  report['source_scripts'][name]={'sha256':digest(p)}
 report['pass']=not report['missing'] and not report['sha_mismatch']
 report['next_step']='Inspect original H1 evolution/GE06/GE07/Lambda offclock interfaces; no interpolation-as-independent-truth.'
 out=rd/'ge19_d47_parent_preflight_v1.json'
 if out.exists():raise SystemExit('D47_PREFLIGHT_OUTPUT_EXISTS '+str(out))
 with out.open('x') as f:json.dump(report,f,indent=2,sort_keys=True);f.write('\n')
 print('GE19_D47_PARENT_PREFLIGHT_'+('PASS' if report['pass'] else 'INCOMPLETE'))
 for n,v in report['parent_files'].items():print('PARENT',n,'SHA_MATCH',v['match'],'BYTES',v['size_bytes'])
 for n in report['missing']:print('MISSING',n)
 for n in report['sha_mismatch']:print('SHA_MISMATCH',n)
 print('REPORT',out)
 return 0 if report['pass'] else 3
if __name__=='__main__':sys.exit(main())
