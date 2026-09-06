#!/usr/bin/env python3
from pathlib import Path
import argparse, importlib.util, json, math, numpy as np

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('ana',ROOT/'v021'/'analyse_tau_point.py')
a=importlib.util.module_from_spec(spec); spec.loader.exec_module(a)
PARAMS=list(a.PARAMS)

# Predeclared effective survey specifications. These are intentionally simple
# TT/TE/EE Fisher forecasts: white map noise + Gaussian beam, no foreground
# residuals, no delensing gain, and the frozen ell range 30..2500.
SURVEYS={
  'SO_baseline': {
    'fsky':0.40, 'delta_T_uK_arcmin':6.0, 'delta_P_uK_arcmin':8.5,
    'beam_fwhm_arcmin':1.4, 'reference':'effective LAT-like baseline forecast'
  },
  'CMB_S4_wide': {
    'fsky':0.60, 'delta_T_uK_arcmin':1.5, 'delta_P_uK_arcmin':2.1,
    'beam_fwhm_arcmin':1.4, 'reference':'effective wide-survey reference forecast'
  },
  'CVL_fullsky': {
    'fsky':1.0, 'delta_T_uK_arcmin':0.0, 'delta_P_uK_arcmin':0.0,
    'beam_fwhm_arcmin':0.0, 'reference':'ideal full-sky cosmic-variance limit'
  },
}


def noise_Dl(ell, depth, beam):
    if depth<=0: return 0.0
    d=depth*math.pi/(180.0*60.0)  # uK-rad
    sig=beam*math.pi/(180.0*60.0)/math.sqrt(8.0*math.log(2.0)) if beam>0 else 0.0
    nl=d*d*math.exp(ell*(ell+1.0)*sig*sig)  # C_l noise in uK^2
    return ell*(ell+1.0)*nl/(2.0*math.pi)    # CLASS cl.dat stores D_l


def invcov_survey(ells,base,cfg):
    out=[]; fsky=float(cfg['fsky'])
    for l in ells:
        tt,ee,te=base[l]
        nt=noise_Dl(l,cfg['delta_T_uK_arcmin'],cfg['beam_fwhm_arcmin'])
        ne=noise_Dl(l,cfg['delta_P_uK_arcmin'],cfg['beam_fwhm_arcmin'])
        T=tt+nt; E=ee+ne
        f=1.0/((2*l+1.0)*fsky)
        C=[[2*f*T*T,2*f*te*te,2*f*T*te],
           [2*f*te*te,2*f*E*E,2*f*E*te],
           [2*f*T*te,2*f*E*te,f*(te*te+T*E)]]
        sc=max(abs(C[0][0]),abs(C[1][1]),abs(C[2][2]),1e-300); eps=sc*1e-14
        out.append(a.inv3([[C[i][j]+(eps if i==j else 0.0) for j in range(3)] for i in range(3)]))
    return out


def fisher_result(ells,base,s,D,cfg):
    W=invcov_survey(ells,base,cfg)
    qs,bdiag=a.orthonormalize([(p,D[p]) for p in PARAMS],W)
    res=a.project(s,qs,W)
    raw=a.wnorm(s,W); marg=a.wnorm(res,W)
    bands={'30-100':(30,100),'101-500':(101,500),'501-1000':(501,1000),'1001-2500':(1001,2500)}
    bs={}
    for name,(lo,hi) in bands.items():
        mask=[lo<=l<=hi for l in ells]
        bs[name]={'raw_per_eta':a.wnorm(s,W,mask),'marginalized_residual_per_eta':a.wnorm(res,W,mask)}
    return {
      'raw_SNR_per_eta':raw,
      'marginalized_SNR_per_eta':marg,
      'retained_fraction':marg/max(raw,1e-300),
      'sigma_eta_Fisher':1.0/marg if marg>0 else None,
      'eta_for_3sigma':3.0/marg if marg>0 else None,
      'eta_for_5sigma':5.0/marg if marg>0 else None,
      'nuisance_rank':len(qs),
      'nuisance_basis_independence':bdiag,
      'band_information':bs,
    }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('output_dir')
    ap.add_argument('--json-out',required=True)
    z=ap.parse_args(); out=Path(z.output_dir)
    tag='kb0p0665_tau10'
    fbase=out/f'v039_{tag}_base__cl.dat'
    fp=out/f'v039_{tag}_l10_p__cl.dat'; fm=out/f'v039_{tag}_l10_m__cl.dat'
    nuis={}
    for p in PARAMS:
        for q in ('m2','m1','p1','p2'):
            nuis[(p,q)]=out/f'v046_kb0p0665_tau10_p0_nuis_{p}_{q}__cl.dat'
    files=[fbase,fp,fm]+list(nuis.values())
    maps={str(p):a.load_cl(p) for p in files}
    ells=sorted(set.intersection(*(set(v) for v in maps.values())))
    if len(ells)<1000: raise RuntimeError(f'too few common multipoles {len(ells)}')
    base=maps[str(fbase)]
    s=a.vec(ells,maps[str(fp)],maps[str(fm)],20.0)
    D={}
    # Use the already-certified five-point nuisance stencil from v0.49.
    for p in PARAMS:
        h=a.delta(p)
        fm2=maps[str(nuis[(p,'m2')])]; fm1=maps[str(nuis[(p,'m1')])]
        fp1=maps[str(nuis[(p,'p1')])]; fp2=maps[str(nuis[(p,'p2')])]
        vp2=np.asarray(a.vec(ells,fp2,base,1.0)); vp1=np.asarray(a.vec(ells,fp1,base,1.0))
        vm1=np.asarray(a.vec(ells,fm1,base,1.0)); vm2=np.asarray(a.vec(ells,fm2,base,1.0))
        D[p]=((-vp2+8*vp1-8*vm1+vm2)/(12*h)).tolist()

    surveys={name:{'specification':cfg,**fisher_result(ells,base,s,D,cfg)} for name,cfg in SURVEYS.items()}
    cv=surveys['CVL_fullsky']['marginalized_SNR_per_eta']
    locked=0.1364941527698679
    gates={
      'all_nuisance_rank_6':all(v['nuisance_rank']==6 for v in surveys.values()),
      'CVL_reproduces_locked_v049_within_1pct':abs(cv-locked)/locked<0.01,
      'ordering_sigma_CVL_le_S4_le_SO':surveys['CVL_fullsky']['sigma_eta_Fisher'] <= surveys['CMB_S4_wide']['sigma_eta_Fisher'] <= surveys['SO_baseline']['sigma_eta_Fisher'],
    }
    result={
      'classification':'V057_FUTURE_CMB_MEMORY_FORECAST_PASS' if all(gates.values()) else 'V057_FUTURE_CMB_MEMORY_FORECAST_FOLLOWUP',
      'frozen_model':{'KB':0.0665,'tauH0':10.0,'p':0.0,'lambda':10.0,'eta_is_only_new_amplitude':True},
      'observable_scope':{'spectra':['TT','EE','TE'],'ell':[30,2500],'lensing':False,'foreground_residuals':False},
      'derivatives':'locked v0.49 memory tangent plus certified five-point six-parameter nuisance stencil',
      'survey_model':'Gaussian TT/TE/EE covariance with f_sky, white map noise, Gaussian beam; effective single-survey specifications, not a full multifrequency foreground forecast',
      'surveys':surveys,
      'locked_v049_CVL_marginalized_SNR_per_eta':locked,
      'gates':gates,
      'interpretation':'Forecast only. No post-Planck retuning of KB, tauH0, p, lambda, CLASS patch chain, ell range, or nuisance definition.'
    }
    Path(z.json_out).parent.mkdir(parents=True,exist_ok=True)
    Path(z.json_out).write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2))
    if not all(gates.values()): raise SystemExit(2)

if __name__=='__main__': main()
