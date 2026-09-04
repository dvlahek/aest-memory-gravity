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


def differential_signal_change(out,model,level):
    """Compare [model-CDM] at `level` with [model-CDM] at s0.

    This cancels the common CLASS shift caused solely by moving the integration
    start. The normalization is the s0 CDM peak in each CMB column.
    """
    ans={};primary_max=0.0;all_max=0.0
    for key,suf in [('unlensed','cl.dat'),('lensed','cl_lensed.dat')]:
        c0=load_numeric(find_one(out,'v019i_cdm_s0_',suf))
        m0=load_numeric(find_one(out,f'v019i_{model}_s0_',suf))
        cL=load_numeric(find_one(out,f'v019i_cdm_{level}_',suf))
        mL=load_numeric(find_one(out,f'v019i_{model}_{level}_',suf))
        if not (len(c0)==len(m0)==len(cL)==len(mL)):
            raise RuntimeError('row mismatch in differential signal comparison')
        ncol=min(len(c0[0]),len(m0[0]),len(cL[0]),len(mL[0]))
        amps=[0.0]*ncol;diffs=[0.0]*ncol;n=0
        for r0,rm0,rL,rmL in zip(c0,m0,cL,mL):
            ell=r0[0]
            if ell<30 or ell>2500:continue
            n+=1
            for j in range(1,ncol):
                amps[j]=max(amps[j],abs(r0[j]))
                d0=rm0[j]-r0[j]
                dL=rmL[j]-rL[j]
                diffs[j]=max(diffs[j],abs(dL-d0))
        cols=[]
        for j in range(1,ncol):
            q=diffs[j]/max(amps[j],1e-300)
            cols.append({'column':j+1,'max_delta_signal_change_over_cdm_peak':q})
        p=max((c['max_delta_signal_change_over_cdm_peak'] for c in cols if c['column'] in PRIMARY_COLS),default=0.0)
        a=max((c['max_delta_signal_change_over_cdm_peak'] for c in cols),default=0.0)
        ans[key]={'rows':n,'columns':cols,'primary_max':p,'all_columns_max':a}
        primary_max=max(primary_max,p);all_max=max(all_max,a)
    ans['primary_max']=primary_max;ans['all_columns_max']=all_max
    return ans


def scalar_file_pair(out,model,la,lb,suffix):
    try:return compare(find_one(out,f'v019i_{model}_{la}_',suffix),find_one(out,f'v019i_{model}_{lb}_',suffix),False)
    except Exception as e:return {'error':str(e)}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('output_dir');ap.add_argument('--json-out',default='results/v019i_start_convergence.json');args=ap.parse_args()
    out=Path(args.output_dir)
    res={'levels':{},'self_convergence':{},'differential_signal_stability':{}}
    for lev in LEVELS:
        res['levels'][lev]={
          'exp_vs_cdm':cl_pair(out,'cdm',lev,'exp',lev),
          'cosh_vs_cdm':cl_pair(out,'cdm',lev,'cosh',lev),
        }
    for model in ('cdm','exp','cosh'):
        res['self_convergence'][model]={}
        for lev in LEVELS[1:]:
            res['self_convergence'][model][f's0_vs_{lev}_cl']=cl_pair(out,model,'s0',model,lev)
        res['self_convergence'][model]['s0_vs_s3_pk']=scalar_file_pair(out,model,'s0','s3','pk.dat')
        res['self_convergence'][model]['s0_vs_s3_background']=scalar_file_pair(out,model,'s0','s3','background.dat')
        res['self_convergence'][model]['s0_vs_s3_thermodynamics']=scalar_file_pair(out,model,'s0','s3','thermodynamics.dat')
    for model in ('exp','cosh'):
        res['differential_signal_stability'][model]={lev:differential_signal_change(out,model,lev) for lev in LEVELS[1:]}

    exp0=res['levels']['s0']['exp_vs_cdm']['primary_max']
    cosh0=res['levels']['s0']['cosh_vs_cdm']['primary_max']
    reference_signal=max(exp0,cosh0,1e-300)

    # A start level is usable as an IC convergence control only while matched CDM
    # itself remains stable. If CDM moves substantially, the test has entered a
    # CLASS start/sampling regime and cannot be attributed to AeST IC physics.
    control_limit=max(1e-5,0.10*reference_signal)
    valid_levels=[];rejected_levels=[]
    per_level={}
    for lev in LEVELS[1:]:
        cdm_self=res['self_convergence']['cdm'][f's0_vs_{lev}_cl']['primary_max']
        exp_r=res['levels'][lev]['exp_vs_cdm']['primary_max']
        cosh_r=res['levels'][lev]['cosh_vs_cdm']['primary_max']
        exp_drift=abs(exp_r-exp0)/exp0
        cosh_drift=abs(cosh_r-cosh0)/cosh0
        exp_ds=res['differential_signal_stability']['exp'][lev]['primary_max']/exp0
        cosh_ds=res['differential_signal_stability']['cosh'][lev]['primary_max']/cosh0
        valid=cdm_self<=control_limit
        (valid_levels if valid else rejected_levels).append(lev)
        per_level[lev]={
          'cdm_self_primary':cdm_self,
          'control_limit':control_limit,
          'control_valid':valid,
          'exp_residual':exp_r,'exp_residual_fractional_drift':exp_drift,
          'cosh_residual':cosh_r,'cosh_residual_fractional_drift':cosh_drift,
          'exp_differential_signal_fractional_change':exp_ds,
          'cosh_differential_signal_fractional_change':cosh_ds,
        }

    valid_drifts=[];valid_signal_changes=[]
    for lev in valid_levels:
        valid_drifts += [per_level[lev]['exp_residual_fractional_drift'],per_level[lev]['cosh_residual_fractional_drift']]
        valid_signal_changes += [per_level[lev]['exp_differential_signal_fractional_change'],per_level[lev]['cosh_differential_signal_fractional_change']]
    max_valid_drift=max(valid_drifts,default=math.inf)
    max_valid_signal_change=max(valid_signal_changes,default=math.inf)

    if len(valid_levels)>=2 and max_valid_drift<0.01 and max_valid_signal_change<0.05:
        classification='LEADING_ADIABATIC_START_CONVERGED_CONTROLLED_WINDOW'
        gate='PASS_CONTROLLED_START_CONVERGENCE'
    elif len(valid_levels)>=1 and (max_valid_drift>0.05 or max_valid_signal_change>0.20):
        classification='FINITE_GRADIENT_IC_CORRECTION_REQUIRED'
        gate='NEEDS_FROBENIUS_K2'
    else:
        classification='START_CONVERGENCE_INCONCLUSIVE'
        gate='CHECK'

    res['summary']={
      'exp_cdm_primary_s0':exp0,
      'cosh_cdm_primary_s0':cosh0,
      'control_limit':control_limit,
      'valid_earlier_start_levels':valid_levels,
      'rejected_common_mode_levels':rejected_levels,
      'per_level':per_level,
      'max_valid_residual_fractional_drift':max_valid_drift,
      'max_valid_differential_signal_fractional_change':max_valid_signal_change,
      'classification':classification,'gate_status':gate,
      'meaning':'Earlier-start levels are interpreted only while the matched CDM control remains stable. Levels where CDM itself shifts are classified as CLASS start/sampling common-mode breakdown, not evidence for AeST finite-gradient IC terms.'
    }
    res['gate_status']=gate
    p=Path(args.json_out);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(res,indent=2))
    print(json.dumps(res['summary'],indent=2))

if __name__=='__main__':main()
