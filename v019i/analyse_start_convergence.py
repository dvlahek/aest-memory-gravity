#!/usr/bin/env python3
from pathlib import Path
import argparse,json,math

LEVELS=('s0','s1','s2','s3')
PRIMARY_COLS=(2,3,4)


def load_numeric(path):
    rows=[]
    with open(path,'r',errors='replace') as f:
        for line in f:
            t=line.strip()
            if not t or t.startswith('#'):continue
            try:rows.append([float(x) for x in t.split()])
            except ValueError:pass
    if not rows:raise RuntimeError(f'no numeric rows in {path}')
    return rows


def find_one(out,prefix,suffix):
    m=sorted(out.glob(prefix+'*'+suffix))
    if len(m)!=1:raise RuntimeError(f'expected one {prefix}*{suffix}, found {len(m)}')
    return m[0]


def compare(a_path,b_path,ell_cut=True):
    a=load_numeric(a_path);b=load_numeric(b_path)
    if len(a)!=len(b):raise RuntimeError(f'row mismatch {a_path.name} {b_path.name}')
    ncol=min(len(a[0]),len(b[0]));amps=[0.0]*ncol;diffs=[0.0]*ncol;rms=[0.0]*ncol;n=0
    for ra,rb in zip(a,b):
        if len(ra)<ncol or len(rb)<ncol:continue
        if ell_cut:
            x=ra[0]
            if x<30 or x>2500:continue
        n+=1
        for j in range(1,ncol):
            amps[j]=max(amps[j],abs(ra[j]));d=abs(rb[j]-ra[j]);diffs[j]=max(diffs[j],d);rms[j]+=d*d
    cols=[]
    for j in range(1,ncol):
        amp=max(amps[j],1e-300)
        cols.append({'column':j+1,'peak':amp,'max_abs':diffs[j],
                     'max_over_peak':diffs[j]/amp,'rms_over_peak':math.sqrt(rms[j]/max(n,1))/amp})
    primary=[c for c in cols if c['column'] in PRIMARY_COLS]
    return {'reference':a_path.name,'test':b_path.name,'rows':n,'columns':cols,
            'primary_max':max((c['max_over_peak'] for c in primary),default=0.0),
            'all_columns_max':max((c['max_over_peak'] for c in cols),default=0.0)}


def cl_pair(out,ma,la,mb,lb):
    ans={}
    for key,suf in [('unlensed','cl.dat'),('lensed','cl_lensed.dat')]:
        ans[key]=compare(find_one(out,f'v019i_{ma}_{la}_',suf),find_one(out,f'v019i_{mb}_{lb}_',suf),True)
    ans['primary_max']=max(ans['unlensed']['primary_max'],ans['lensed']['primary_max'])
    ans['all_columns_max']=max(ans['unlensed']['all_columns_max'],ans['lensed']['all_columns_max'])
    return ans


def scalar_file_pair(out,model,la,lb,suffix):
    try:
        return compare(find_one(out,f'v019i_{model}_{la}_',suffix),find_one(out,f'v019i_{model}_{lb}_',suffix),False)
    except Exception as e:
        return {'error':str(e)}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('output_dir');ap.add_argument('--json-out',default='results/v019i_start_convergence.json');args=ap.parse_args()
    out=Path(args.output_dir)
    res={'levels':{},'self_convergence':{}}
    for lev in LEVELS:
        res['levels'][lev]={
          'exp_vs_cdm':cl_pair(out,'cdm',lev,'exp',lev),
          'cosh_vs_cdm':cl_pair(out,'cdm',lev,'cosh',lev),
        }
    for model in ('cdm','exp','cosh'):
        res['self_convergence'][model]={
          's0_vs_s3_cl':cl_pair(out,model,'s0',model,'s3'),
          's0_vs_s3_pk':scalar_file_pair(out,model,'s0','s3','pk.dat'),
          's0_vs_s3_background':scalar_file_pair(out,model,'s0','s3','background.dat'),
          's0_vs_s3_thermodynamics':scalar_file_pair(out,model,'s0','s3','thermodynamics.dat'),
        }

    exp0=res['levels']['s0']['exp_vs_cdm']['primary_max'];exp3=res['levels']['s3']['exp_vs_cdm']['primary_max']
    cosh0=res['levels']['s0']['cosh_vs_cdm']['primary_max'];cosh3=res['levels']['s3']['cosh_vs_cdm']['primary_max']
    exp_self=res['self_convergence']['exp']['s0_vs_s3_cl']['primary_max']
    cosh_self=res['self_convergence']['cosh']['s0_vs_s3_cl']['primary_max']
    cdm_self=res['self_convergence']['cdm']['s0_vs_s3_cl']['primary_max']
    exp_drift=abs(exp3-exp0)/max(exp0,1e-300)
    cosh_drift=abs(cosh3-cosh0)/max(cosh0,1e-300)

    if exp_self<1e-5 and cosh_self<1e-5 and exp_drift<0.02 and cosh_drift<0.02:
        classification='LEADING_ADIABATIC_START_CONVERGED'
        gate='PASS_START_CONVERGENCE'
    elif exp_self>1e-4 or cosh_self>1e-4 or exp_drift>0.10 or cosh_drift>0.10:
        classification='FINITE_GRADIENT_IC_CORRECTION_REQUIRED'
        gate='NEEDS_FROBENIUS_K2'
    else:
        classification='MIXED_START_CONVERGENCE'
        gate='CHECK'

    res['summary']={
      'exp_cdm_primary_s0':exp0,'exp_cdm_primary_s3':exp3,'exp_residual_fractional_drift':exp_drift,
      'cosh_cdm_primary_s0':cosh0,'cosh_cdm_primary_s3':cosh3,'cosh_residual_fractional_drift':cosh_drift,
      'cdm_s0_s3_primary_self':cdm_self,'exp_s0_s3_primary_self':exp_self,'cosh_s0_s3_primary_self':cosh_self,
      'classification':classification,'gate_status':gate,
      'meaning':'Tests omitted finite-gradient corrections to the derived chi=E=0 leading adiabatic mode by moving the CLASS start farther outside the horizon.'
    }
    res['gate_status']=gate
    p=Path(args.json_out);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(res,indent=2))
    print(json.dumps(res['summary'],indent=2))

if __name__=='__main__':main()
