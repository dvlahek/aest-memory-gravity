#!/usr/bin/env python3
from pathlib import Path
import argparse, json, math
import numpy as np

KB_GRID=np.array([0.1,0.09,0.08,0.07,0.06,0.05,0.04,0.035,0.03,0.025,0.02,0.015,0.01,0.0075,0.005,0.003,0.002,0.001],dtype=float)
A_TARGETS=np.array([1e-4,3e-4,1/1100.0,3e-3,1e-2,1e-1,1.0],dtype=float)


def load(path):
    z=np.genfromtxt(path,names=True)
    if z.size==0: raise RuntimeError('empty critical trace')
    if z.ndim==0: z=np.array([z],dtype=z.dtype)
    return z


def intrinsic_matrix(row,kb):
    k=float(row['k']); a=float(row['a']); H=float(row['H']); H0=float(row['H0'])
    rho=float(row['rho']); w=float(row['w']); c=float(row['cad2']); Q=float(row['Q']); KQ=float(row['KQ'])
    if not all(np.isfinite([k,a,H,H0,rho,w,c,Q,KQ])) or k<=0 or a<=0 or H<=0 or H0<=0 or rho<=0 or abs(1+w)<1e-10:
        return None
    k2=k*k; aH=a*H
    chi=np.array([0.0,Q*a/k2,Q,0.0],dtype=float)
    P=np.array([
        c,
        c*(2-kb)*Q/(3*a*rho),
        c*k2*(2-kb)*Q/(3*a*a*rho),
        c*k2*kb/(3*a*a*rho)
    ],dtype=float)
    A=np.zeros((4,4),dtype=float)
    A[0,:]=-3*aH*P
    A[0,0]+=3*aH*w
    A[0,1]-=(1+w)
    A[1,:]=k2*P/(1+w)
    A[1,1]+=(3*c-1)*aH
    A[2,3]=a
    ialpha=np.array([0.0,0.0,1.0,0.0])
    B=KQ*chi-(2-kb)*(Q*P/(1+w)+(H+Q)*chi-3*c*H*Q*ialpha)
    A[3,:]=a*B/kb
    A[3,3]-=aH
    # similarity scaling to dimensionless state coordinates: delta, theta/H0, H0*alpha, E
    S=np.diag([1.0,H0,1.0/H0,1.0])
    Sinv=np.diag([1.0,1.0/H0,H0,1.0])
    At=Sinv@A@S
    Ct=chi@S
    return At,Ct,aH


def select_epochs(z):
    out=[]
    ks=np.unique(z['k'])
    for k in ks:
        idx=np.where(z['k']==k)[0]
        aa=z['a'][idx]
        if len(idx)==0: continue
        loga=np.log(np.maximum(aa,1e-300))
        for at in A_TARGETS:
            j=int(np.argmin(np.abs(loga-math.log(at))))
            ii=idx[j]
            # Require the accepted-grid point to be reasonably close in scale factor.
            if abs(math.log(max(float(z['a'][ii]),1e-300)/at))<0.35:
                out.append((float(k),float(at),ii))
    return out


def safe_metrics(row,kb):
    m=intrinsic_matrix(row,kb)
    if m is None: return None
    A,C,aH=m
    if not np.all(np.isfinite(A)) or aH<=0: return None
    Ah=A/aH
    try:
        eig=np.linalg.eigvals(Ah)
        sv=np.linalg.svd(Ah,compute_uv=False)
        sigma_min=float(np.min(sv)); sigma_max=float(np.max(sv))
        cond=sigma_max/max(sigma_min,1e-300)
        b=np.array([0.,0.,0.,1.])
        # Dimensionless zero-frequency transfer from additive E' forcing to chi,
        # normalized to one Hubble-time forcing amplitude.
        x=np.linalg.solve(-Ah,b)
        gain=abs(complex(C@x))
        return {'max_real':float(np.max(np.real(eig))),
                'spectral_radius':float(np.max(np.abs(eig))),
                'sigma_min':sigma_min,'condition':cond,'dc_gain':float(gain),
                'eig':[[float(v.real),float(v.imag)] for v in eig]}
    except np.linalg.LinAlgError:
        return {'max_real':math.nan,'spectral_radius':math.inf,'sigma_min':0.0,'condition':math.inf,'dc_gain':math.inf,'eig':[]}


def qstats(vals):
    a=np.asarray([v for v in vals if np.isfinite(v)],dtype=float)
    if a.size==0: return {'n':0}
    return {'n':int(a.size),'median':float(np.median(a)),'p90':float(np.quantile(a,.90)),
            'p99':float(np.quantile(a,.99)),'max':float(np.max(a)),'min':float(np.min(a))}


def log_power_fit(kbs,ys):
    k=np.asarray(kbs,float); y=np.asarray(ys,float)
    mask=(k>0)&(y>0)&np.isfinite(k)&np.isfinite(y)
    k=k[mask]; y=y[mask]
    if len(k)<3: return None
    X=np.column_stack([np.ones(len(k)),-np.log(k)])
    beta=np.linalg.lstsq(X,np.log(y),rcond=None)[0]
    pred=X@beta; rms=float(np.sqrt(np.mean((np.log(y)-pred)**2)))
    return {'C':float(np.exp(beta[0])),'alpha':float(beta[1]),'log_rms':rms,'n':int(len(k))}


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('trace'); ap.add_argument('--json-out',required=True)
    z=ap.parse_args(); data=load(z.trace); picks=select_epochs(data)
    if len(picks)<100: raise RuntimeError(f'too few epoch samples: {len(picks)}')
    per_kb={}; top=[]
    for kb in KB_GRID:
        by_epoch={}; all_gain=[]; all_sig=[]; all_rad=[]; all_growth=[]
        for at in A_TARGETS:
            rows=[]
            for k,t,ii in picks:
                if t!=at: continue
                met=safe_metrics(data[ii],float(kb))
                if met is None: continue
                rows.append((k,ii,met))
                if np.isfinite(met['dc_gain']): all_gain.append(met['dc_gain'])
                if np.isfinite(met['sigma_min']): all_sig.append(met['sigma_min'])
                if np.isfinite(met['spectral_radius']): all_rad.append(met['spectral_radius'])
                if np.isfinite(met['max_real']): all_growth.append(met['max_real'])
                score=met['dc_gain'] if np.isfinite(met['dc_gain']) else 1e300
                top.append((score,float(kb),float(k),float(at),int(ii),met))
            by_epoch[f'a{at:.8g}']={
                'dc_gain_Hubble_normalized':qstats([r[2]['dc_gain'] for r in rows]),
                'sigma_min_A_over_aH':qstats([r[2]['sigma_min'] for r in rows]),
                'condition_A_over_aH':qstats([r[2]['condition'] for r in rows]),
                'spectral_radius_over_aH':qstats([r[2]['spectral_radius'] for r in rows]),
                'max_real_eigenvalue_over_aH':qstats([r[2]['max_real'] for r in rows]),
                'fraction_positive_intrinsic_growth':float(np.mean([r[2]['max_real']>0 for r in rows])) if rows else None,
            }
        per_kb[f'{kb:.6g}']={'KB':float(kb),'epochs':by_epoch,
                              'all_epoch_dc_gain':qstats(all_gain),'all_epoch_sigma_min':qstats(all_sig),
                              'all_epoch_spectral_radius':qstats(all_rad),'all_epoch_max_real':qstats(all_growth)}

    # Structural low-KB scaling at recombination using median and p90 DC gain and spectral radius.
    rec_key=f'a{(1/1100.0):.8g}'
    fit_k=[]; fit_med=[]; fit_p90=[]; fit_rad=[]
    for kb in KB_GRID:
        if kb>0.03: continue
        e=per_kb[f'{kb:.6g}']['epochs'].get(rec_key,{})
        g=e.get('dc_gain_Hubble_normalized',{}); r=e.get('spectral_radius_over_aH',{})
        if g.get('n',0)>0 and r.get('n',0)>0:
            fit_k.append(kb); fit_med.append(g['median']); fit_p90.append(g['p90']); fit_rad.append(r['median'])
    fits={'recombination_low_KB_median_dc_gain_vs_KB':log_power_fit(fit_k,fit_med),
          'recombination_low_KB_p90_dc_gain_vs_KB':log_power_fit(fit_k,fit_p90),
          'recombination_low_KB_median_spectral_radius_vs_KB':log_power_fit(fit_k,fit_rad)}

    top.sort(key=lambda x:x[0],reverse=True)
    hot=[]
    for score,kb,k,at,ii,met in top[:30]:
        row=data[ii]
        hot.append({'KB':kb,'k_Mpc_inv':k,'a_target':at,'a_actual':float(row['a']),
                    'z_actual':float(1/row['a']-1),'dc_gain':met['dc_gain'],
                    'sigma_min':met['sigma_min'],'condition':met['condition'],
                    'spectral_radius_over_aH':met['spectral_radius'],
                    'max_real_over_aH':met['max_real'],'eigenvalues_over_aH':met['eig']})

    res={'classification':'V033_INTRINSIC_KB_SINGULAR_PERTURBATION_MAP',
         'definition':'frozen-coefficient 4x4 intrinsic AeST scalar block (delta,theta,alpha,E), metric perturbations treated as external; eigenvalues are invariant under the state rescaling used for conditioning',
         'equation_note':'Eprime=a E_rhs/KB-aH E; eta-tangent memory enters Eprime directly as -a Q Bchi/(2 KB), so KB->0 is a singular-perturbation boundary',
         'KB_grid':KB_GRID.tolist(),'a_targets':A_TARGETS.tolist(),'selected_rows':len(picks),
         'per_KB':per_kb,'low_KB_power_fits':fits,'largest_DC_gain_locations':hot,
         'interpretation_gate':{'finite_KB_pole_not_assumed':True,
             'purpose':'test whether the CMB amplitude rise correlates with loss of intrinsic normal hyperbolicity/large resolvent gain as KB approaches the kinetic boundary'},
         'scope':'diagnostic only: frozen intrinsic AeST block, not the full Einstein-Boltzmann Jacobian; must be compared with v0.32 full CLASS transition scan'}
    Path(z.json_out).write_text(json.dumps(res,indent=2)); print(json.dumps(res,indent=2))

if __name__=='__main__': main()
