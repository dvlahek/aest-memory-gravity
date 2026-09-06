#!/usr/bin/env python3
from pathlib import Path
import argparse, json, math, sys
import numpy as np
import emcee

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import v056.planck_highl_lowl_refit as v

SEED=5900665
WALKERS=48
STEPS=6000
BURN=1500
THIN=5
ETA_BOUNDS=(-40.0,40.0)
CENTER={
  'H0':67.29978079940001,
  'omega_b':0.022041716224516936,
  'omega_cdm':0.11939298177821148,
  'tau_reio':0.06624082364510152,
  'n_s':0.9611930331039573,
  'lnA_s':-19.967780399633433,
  'eta':8.521888498294636,
  'A_planck':1.0,
}
NAMES=v.PARAMS+['eta','A_planck']
BOUNDS=dict(v.BOUNDS); BOUNDS['eta']=ETA_BOUNDS
INIT_SCALE={
  'H0':0.08,'omega_b':8e-5,'omega_cdm':2e-4,'tau_reio':8e-4,
  'n_s':8e-4,'lnA_s':0.003,'eta':2.0,'A_planck':4e-4
}

def inside(x):
    for n,val in zip(NAMES,x):
        lo,hi=BOUNDS[n]
        if not (lo < float(val) < hi): return False
    return True

def qtiles(x):
    q=np.percentile(x,[2.5,16,50,84,97.5])
    return {'q2p5':float(q[0]),'q16':float(q[1]),'median':float(q[2]),'q84':float(q[3]),'q97p5':float(q[4])}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--class-root',required=True); ap.add_argument('--packages',required=True)
    ap.add_argument('--profile-json',required=True); ap.add_argument('--json-out',required=True)
    ap.add_argument('--chain-out',required=True)
    z=ap.parse_args()
    cr=Path(z.class_root).resolve(); packages=Path(z.packages).resolve()
    profile=json.load(open(z.profile_json))
    if profile['classification']!='V058_PLANCK_ETA_PROFILE_COMPLETE':
        raise RuntimeError('v0.58 profile comparison is not complete')

    text=v.BASE.read_text(); lt=v.LowTT(packages); le=v.LowEE(packages)
    # One frozen local CLASS spectral linearization around the independently obtained v0.56 free-fit state.
    hl,B,T,D,fb,ft,FD=v.generate(cr,packages,text,CENTER,59)
    x0=np.array([CENTER[n] for n in NAMES],dtype=float)

    def chi2(x):
        if not inside(x): return np.inf
        delta=np.asarray(x)-x0
        return float(v.total_chi2(hl,lt,le,B,T,fb,ft,CENTER,delta,D,FD,NAMES))
    def log_prob(x):
        c=chi2(x)
        return -0.5*c if np.isfinite(c) and c<1e90 else -np.inf

    rng=np.random.default_rng(SEED)
    p0=[]
    while len(p0)<WALKERS:
        x=x0+np.array([INIT_SCALE[n] for n in NAMES])*rng.normal(size=len(NAMES))
        if inside(x) and np.isfinite(log_prob(x)): p0.append(x)
    p0=np.asarray(p0)

    sampler=emcee.EnsembleSampler(WALKERS,len(NAMES),log_prob)
    sampler.run_mcmc(p0,STEPS,progress=True)
    chain=sampler.get_chain(discard=BURN,thin=THIN,flat=True)
    logp=sampler.get_log_prob(discard=BURN,thin=THIN,flat=True)
    np.savez_compressed(z.chain_out,chain=chain,log_prob=logp,names=np.array(NAMES,dtype='U32'))

    try:
        tau=sampler.get_autocorr_time(discard=BURN,tol=0)
        tau_map={n:float(t) for n,t in zip(NAMES,tau)}
        max_tau=float(np.max(tau)); eff=float((WALKERS*(STEPS-BURN))/max_tau)
    except Exception:
        tau_map=None; max_tau=None; eff=None

    acc=np.asarray(sampler.acceptance_fraction)
    summaries={n:qtiles(chain[:,i]) for i,n in enumerate(NAMES)}
    eta=chain[:,NAMES.index('eta')]
    ppos=float(np.mean(eta>0)); pneg=float(np.mean(eta<0))
    ib=int(np.argmax(logp)); best={n:float(chain[ib,i]) for i,n in enumerate(NAMES)}
    best_chi2=float(-2*logp[ib])

    pq=profile['quadratic_local_fit']
    prof_eta=float(pq['eta_hat']); prof_sig=float(pq['sigma_eta'])
    post_eta=summaries['eta']['median']; post_half68=0.5*(summaries['eta']['q84']-summaries['eta']['q16'])
    validation={
      'v058_profile_eta_hat':prof_eta,
      'v058_profile_sigma_eta':prof_sig,
      'posterior_eta_median':post_eta,
      'posterior_eta_half68':post_half68,
      'median_minus_profile_hat':float(post_eta-prof_eta),
      'width_ratio_posterior_to_profile':float(post_half68/prof_sig),
    }
    gates={
      'finite_chain':bool(np.all(np.isfinite(chain)) and np.all(np.isfinite(logp))),
      'acceptance_mean_between_0p15_0p65':bool(0.15<float(np.mean(acc))<0.65),
      'eta_not_prior_edge':bool(summaries['eta']['q2p5']>ETA_BOUNDS[0]+1 and summaries['eta']['q97p5']<ETA_BOUNDS[1]-1),
      'profile_location_consistent_with_posterior_68scale':bool(abs(post_eta-prof_eta)<max(post_half68,prof_sig)),
    }
    if max_tau is not None:
      gates['chain_length_gt_30tau']=bool((STEPS-BURN)>30*max_tau)

    res={
      'classification':'V059_PLANCK_LOCAL_LINEARIZED_POSTERIOR_COMPLETE' if all(gates.values()) else 'V059_PLANCK_LOCAL_LINEARIZED_POSTERIOR_FOLLOWUP',
      'sampler':{'method':'emcee','walkers':WALKERS,'steps':STEPS,'burnin':BURN,'thin':THIN,'seed':SEED,
                 'acceptance_mean':float(np.mean(acc)),'acceptance_min':float(np.min(acc)),'acceptance_max':float(np.max(acc)),
                 'autocorr_time':tau_map,'max_autocorr_time':max_tau,'rough_effective_samples':eff},
      'sampled_parameters':NAMES,
      'posterior':summaries,
      'eta_probability_positive':ppos,'eta_probability_negative':pneg,
      'best_sample':best,'best_sample_chi2':best_chi2,
      'v058_validation':validation,'gates':gates,
      'locked_model':{'KB':v.KB,'tauH0':v.TAUH0,'p':0.0,'lambda':v.LAMBDA,'CLASS_commit':'e85808324f51fc694d12e3ed7439552a3c3f9540'},
      'likelihood':'Planck 2018 Plik-lite TTTEEE native high-l + native low-l TT + native low-l EE; common A_planck Gaussian prior sigma=0.0025',
      'scope':'Eight-dimensional nuisance-marginalized posterior evaluated on one frozen CLASS spectral linearization centered at the v0.56 free-fit state. Native Planck likelihood functions are evaluated exactly on the linearized spectra. This is not an exact nonlinear CLASS-at-every-sample MCMC.',
      'anti_tuning':'Frozen v0.53 physics and predeclared v0.59 sampling choices unchanged after reading the result.'
    }
    Path(z.json_out).write_text(json.dumps(res,indent=2)); print(json.dumps(res,indent=2))
    if not all(gates.values()): raise SystemExit(2)

if __name__=='__main__': main()
