#!/usr/bin/env python3
from pathlib import Path
import argparse,json,math

def load_numeric(path):
    rows=[]
    with open(path,'r',errors='replace') as f:
        for line in f:
            t=line.strip()
            if not t or t.startswith('#'): continue
            try: rows.append([float(x) for x in t.split()])
            except ValueError: pass
    return rows

def find_one(out,prefix,suffix):
    matches=sorted(out.glob(prefix+'*'+suffix))
    if not matches: raise FileNotFoundError(f'no {prefix}*{suffix} in {out}')
    return matches[0]

def compare_cl(ref_path,test_path):
    a=load_numeric(ref_path); b=load_numeric(test_path)
    n=min(len(a),len(b)); ncol=min(len(a[0]),len(b[0]))
    amps=[0.0]*ncol; diffs=[0.0]*ncol; rms=[0.0]*ncol; count=0; ellmis=0.
    for i in range(n):
        ell=a[i][0]; ellmis=max(ellmis,abs(ell-b[i][0]))
        if ell<30 or ell>2500: continue
        count+=1
        for j in range(1,ncol):
            amps[j]=max(amps[j],abs(a[i][j])); d=abs(b[i][j]-a[i][j]); diffs[j]=max(diffs[j],d); rms[j]+=d*d
    metrics=[]
    for j in range(1,ncol):
        amp=max(amps[j],1e-300)
        metrics.append({'column':j+1,'reference_peak_abs':amp,'max_abs_difference':diffs[j],
                        'max_difference_over_reference_peak':diffs[j]/amp,
                        'rms_difference_over_reference_peak':math.sqrt(rms[j]/max(count,1))/amp})
    return {'reference':ref_path.name,'test':test_path.name,'rows_used':count,'ell_grid_max_abs_mismatch':ellmis,
            'columns':metrics,'max_normalized_difference':max((m['max_difference_over_reference_peak'] for m in metrics),default=0.)}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('output_dir');ap.add_argument('--json-out',default='results/v019_eta0_spectra.json');args=ap.parse_args();out=Path(args.output_dir)
    ref_l=find_one(out,'v019_cdm_','cl_lensed.dat'); ref_u=find_one(out,'v019_cdm_','cl.dat'); result={}
    for model,prefix in [('Cosh','v019_cosh_'),('Exp','v019_exp_')]:
        l=compare_cl(ref_l,find_one(out,prefix,'cl_lensed.dat'));u=compare_cl(ref_u,find_one(out,prefix,'cl.dat'));mx=max(l['max_normalized_difference'],u['max_normalized_difference']);result[model]={'lensed':l,'unlensed':u,'max_normalized_difference':mx}
    cosh=result['Cosh']['max_normalized_difference']; exp=result['Exp']['max_normalized_difference']
    result['classification']='REGULAR_CHI0_PROXY_NOT_PUBLISHED_AEST_IC'
    result['criteria']={'finite_and_below_5_percent':True,'Cosh_path_nontrivial_threshold':1e-13}
    result['gate_status']='PASS_DIAGNOSTIC' if (math.isfinite(cosh) and math.isfinite(exp) and cosh<.05 and exp<.05 and cosh>1e-13) else 'CHECK'
    p=Path(args.json_out);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
if __name__=='__main__':main()
