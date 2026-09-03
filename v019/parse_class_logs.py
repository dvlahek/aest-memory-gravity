#!/usr/bin/env python3
from pathlib import Path
import argparse,re,json
PATTERNS={'age_Gyr':r'age =\s*([0-9.eE+-]+) Gyr','conformal_age_Mpc':r'conformal age =\s*([0-9.eE+-]+) Mpc','z_equality':r'radiation/matter equality at z =\s*([0-9.eE+-]+)','z_recombination':r'recombination \(maximum of visibility function\) at z =\s*([0-9.eE+-]+)','theta_s_100':r'sound horizon angle 100\*theta_s =\s*([0-9.eE+-]+)','sigma8_total':r'sigma8=([0-9.eE+-]+) for total matter'}
def parse(path):
 s=Path(path).read_text(errors='replace');d={}
 for k,pat in PATTERNS.items():
  m=re.search(pat,s);d[k]=float(m.group(1)) if m else None
 return d
def main():
 ap=argparse.ArgumentParser();ap.add_argument('results_dir');ap.add_argument('--json-out',default='results/v019_log_diagnostics.json');a=ap.parse_args();r=Path(a.results_dir);models={n:parse(r/f'v019_{n}.log') for n in ['cdm','cosh','exp']};ref=models['cdm'];comp={}
 for name in ['cosh','exp']:
  dif={}
  for k,v in ref.items():
   if v is None or models[name].get(k) is None: continue
   t=models[name][k];dif[k]={'absolute':t-v,'relative':(t-v)/v if v!=0 else None}
  comp[name]=dif
 out={'models':models,'relative_to_cdm':comp}
 age_rel=abs(comp['cosh'].get('age_Gyr',{}).get('relative',0.) or 0.); eq_rel=abs(comp['cosh'].get('z_equality',{}).get('relative',0.) or 0.)
 out['Cosh_background_nontrivial']=age_rel>1e-14 or eq_rel>1e-14;out['gate_status']='PASS' if out['Cosh_background_nontrivial'] else 'CHECK'
 p=Path(a.json_out);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
if __name__=='__main__':main()
