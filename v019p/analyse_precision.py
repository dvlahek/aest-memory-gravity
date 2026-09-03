#!/usr/bin/env python3
from pathlib import Path
import argparse,json,math

PRIMARY_COLS=(2,3,4)  # TT, EE, TE for this CLASS output configuration
LEVELS=('p0','p1','p2','p3')


def load_numeric(path):
    rows=[]
    with open(path,'r',errors='replace') as f:
        for line in f:
            t=line.strip()
            if not t or t.startswith('#'):
                continue
            try:
                rows.append([float(x) for x in t.split()])
            except ValueError:
                pass
    if not rows:
        raise RuntimeError(f'no numeric rows in {path}')
    return rows


def find_one(out,prefix,suffix):
    matches=sorted(out.glob(prefix+'*'+suffix))
    if len(matches)!=1:
        raise RuntimeError(f'expected one {prefix}*{suffix}, found {len(matches)}')
    return matches[0]


def compare(ref_path,test_path):
    a=load_numeric(ref_path); b=load_numeric(test_path)
    if len(a)!=len(b):
        raise RuntimeError(f'row mismatch {ref_path.name} {test_path.name}')
    ncol=min(len(a[0]),len(b[0]))
    amps=[0.0]*ncol; diffs=[0.0]*ncol; rms=[0.0]*ncol; count=0; ellmis=0.0
    for ra,rb in zip(a,b):
        ell=ra[0]
        ellmis=max(ellmis,abs(ell-rb[0]))
        if ell<30 or ell>2500:
            continue
        count+=1
        for j in range(1,ncol):
            amps[j]=max(amps[j],abs(ra[j]))
            d=abs(rb[j]-ra[j])
            diffs[j]=max(diffs[j],d)
            rms[j]+=d*d
    cols=[]
    for j in range(1,ncol):
        amp=max(amps[j],1e-300)
        cols.append({
            'column':j+1,
            'reference_peak_abs':amp,
            'max_abs_difference':diffs[j],
            'max_difference_over_reference_peak':diffs[j]/amp,
            'rms_difference_over_reference_peak':math.sqrt(rms[j]/max(count,1))/amp,
        })
    primary=[c for c in cols if c['column'] in PRIMARY_COLS]
    return {
        'reference':ref_path.name,
        'test':test_path.name,
        'rows_used':count,
        'ell_grid_max_abs_mismatch':ellmis,
        'columns':cols,
        'primary_max':max(c['max_difference_over_reference_peak'] for c in primary),
        'all_columns_max':max(c['max_difference_over_reference_peak'] for c in cols),
    }


def model_pair(out,model_a,level_a,model_b,level_b):
    result={}
    for key,suffix in [('lensed','cl_lensed.dat'),('unlensed','cl.dat')]:
        pa=find_one(out,f'v019p_{model_a}_{level_a}_',suffix)
        pb=find_one(out,f'v019p_{model_b}_{level_b}_',suffix)
        result[key]=compare(pa,pb)
    result['primary_max']=max(result['lensed']['primary_max'],result['unlensed']['primary_max'])
    result['all_columns_max']=max(result['lensed']['all_columns_max'],result['unlensed']['all_columns_max'])
    return result


def safe_ratio(a,b):
    return a/b if b>0 else math.inf


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('output_dir')
    ap.add_argument('--json-out',default='results/v019p_precision.json')
    args=ap.parse_args()
    out=Path(args.output_dir)

    res={'primary_columns':list(PRIMARY_COLS),'ell_range':[30,2500],'levels':{}}
    for level in LEVELS:
        res['levels'][level]={
            'exp_vs_cdm':model_pair(out,'cdm',level,'exp',level)
        }

    res['cdm_self_convergence']={}
    res['exp_self_convergence']={}
    for level in LEVELS[:-1]:
        res['cdm_self_convergence'][f'{level}_vs_p3']=model_pair(out,'cdm','p3','cdm',level)
        res['exp_self_convergence'][f'{level}_vs_p3']=model_pair(out,'exp','p3','exp',level)

    res['cosh_control']={
        'p0':model_pair(out,'cdm','p0','cosh','p0'),
        'p3':model_pair(out,'cdm','p3','cosh','p3'),
    }

    exp0=res['levels']['p0']['exp_vs_cdm']['primary_max']
    exp3=res['levels']['p3']['exp_vs_cdm']['primary_max']
    cdm_floor0=res['cdm_self_convergence']['p0_vs_p3']['primary_max']
    exp_self0=res['exp_self_convergence']['p0_vs_p3']['primary_max']
    shrink=safe_ratio(exp3,exp0)
    floor_ratio=safe_ratio(exp3,max(cdm_floor0,1e-300))

    if shrink < 0.35 and exp3 <= 3.0*max(cdm_floor0,1e-300):
        classification='NUMERICAL_FLOOR_DOMINANT'
    elif shrink > 0.80 and floor_ratio > 3.0:
        classification='PERSISTENT_ETA0_PROXY_SIGNAL'
    else:
        classification='MIXED_OR_NOT_YET_CONVERGED'

    res['summary']={
        'exp_cdm_primary_p0':exp0,
        'exp_cdm_primary_p3':exp3,
        'exp_cdm_p3_over_p0':shrink,
        'cdm_p0_vs_p3_primary_floor':cdm_floor0,
        'exp_p0_vs_p3_primary_self_change':exp_self0,
        'exp_cdm_p3_over_cdm_floor':floor_ratio,
        'classification':classification,
        'strict_null_theory':False,
        'note':'Exp is a quasi-null background control; its eta=0 AeST perturbation closure remains active.'
    }

    finite=all(math.isfinite(x) for x in [exp0,exp3,cdm_floor0,exp_self0])
    res['gate_status']='PASS_DIAGNOSTIC' if finite else 'FAIL'
    p=Path(args.json_out);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(res,indent=2))
    print(json.dumps(res['summary'],indent=2))
    if not finite:
        raise SystemExit(1)

if __name__=='__main__':
    main()
