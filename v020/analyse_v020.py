#!/usr/bin/env python3
from pathlib import Path
import argparse, json, math

PARAMS=['H0','omega_b','omega_cdm','tau_reio','n_s','lnA_s']
BASE={'H0':67.32117,'omega_b':0.02238280,'omega_cdm':0.1201075,'tau_reio':0.05430842,'n_s':0.9660499,'A_s':2.100549e-09}
STEPS={
    'H0': {'kind':'fractional','full':0.005,'half':0.0025},
    'omega_b': {'kind':'fractional','full':0.01,'half':0.005},
    'omega_cdm': {'kind':'fractional','full':0.01,'half':0.005},
    'tau_reio': {'kind':'absolute','full':0.003,'half':0.0015},
    'n_s': {'kind':'absolute','full':0.006,'half':0.003},
    'lnA_s': {'kind':'log','full':0.02,'half':0.01},
}
LMIN,LMAX=30,2500


def load_cl(path):
    d={}
    with open(path,'r',errors='replace') as f:
        for line in f:
            t=line.strip()
            if not t or t.startswith('#'): continue
            p=t.split()
            if len(p)<4: continue
            try:
                ell=int(round(float(p[0]))); vals=(float(p[1]),float(p[2]),float(p[3]))
            except ValueError: continue
            if LMIN<=ell<=LMAX: d[ell]=vals
    if not d: raise RuntimeError(f'no Cl data in {path}')
    return d


def clpath(out,label):
    p=out/f'v020_{label}__cl.dat'
    if not p.exists(): raise RuntimeError(f'missing {p}')
    return p


def vec_from_maps(ells,A,B=None,den=1.0):
    v=[]
    if B is None:
        for l in ells: v.extend(A[l])
    else:
        for l in ells:
            v.extend([(A[l][j]-B[l][j])/den for j in range(3)])
    return v


def add(a,b,ca=1.0,cb=1.0): return [ca*x+cb*y for x,y in zip(a,b)]
def scale(a,c): return [c*x for x in a]
def sub(a,b): return [x-y for x,y in zip(a,b)]
def dot(a,b): return sum(x*y for x,y in zip(a,b))
def norm2(a): return math.sqrt(max(dot(a,a),0.0))


def inv3(A):
    M=[list(A[i])+[1.0 if i==j else 0.0 for j in range(3)] for i in range(3)]
    for col in range(3):
        piv=max(range(col,3),key=lambda r:abs(M[r][col]))
        if abs(M[piv][col])<1e-300: raise RuntimeError('singular covariance')
        if piv!=col: M[col],M[piv]=M[piv],M[col]
        z=M[col][col]
        M[col]=[x/z for x in M[col]]
        for r in range(3):
            if r==col: continue
            z=M[r][col]
            M[r]=[M[r][j]-z*M[col][j] for j in range(6)]
    return [row[3:] for row in M]


def make_invcov(ells,base):
    out=[]
    for l in ells:
        tt,ee,te=base[l]
        f=1.0/(2.0*l+1.0)
        C=[
            [2*f*tt*tt, 2*f*te*te, 2*f*tt*te],
            [2*f*te*te, 2*f*ee*ee, 2*f*ee*te],
            [2*f*tt*te, 2*f*ee*te, f*(te*te+tt*ee)],
        ]
        sc=max(abs(C[0][0]),abs(C[1][1]),abs(C[2][2]),1e-300)
        eps=sc*1e-14
        Creg=[[C[i][j]+(eps if i==j else 0.0) for j in range(3)] for i in range(3)]
        out.append(inv3(Creg))
    return out


def inner(a,b,invcov,mask=None):
    s=0.0
    for i,W in enumerate(invcov):
        if mask is not None and not mask[i]: continue
        x=a[3*i:3*i+3]; y=b[3*i:3*i+3]
        Wy=[sum(W[r][c]*y[c] for c in range(3)) for r in range(3)]
        s += sum(x[r]*Wy[r] for r in range(3))
    return s


def wnorm(a,invcov,mask=None): return math.sqrt(max(inner(a,a,invcov,mask),0.0))
def wcos(a,b,invcov):
    na,nb=wnorm(a,invcov),wnorm(b,invcov)
    return inner(a,b,invcov)/(na*nb) if na>0 and nb>0 else 1.0

def wrel(a,b,invcov): return wnorm(sub(a,b),invcov)/max(wnorm(b,invcov),1e-300)


def step_delta(param,which):
    s=STEPS[param][which]
    if param=='lnA_s': return s
    if STEPS[param]['kind']=='fractional': return BASE[param]*s
    return s


def derivative(ells,plus,minus,param,which):
    return vec_from_maps(ells,plus,minus,2.0*step_delta(param,which))


def orthonormalize(vectors,invcov):
    qs=[]; diagnostics=[]
    for name,v in vectors:
        w=v[:]; n0=wnorm(w,invcov)
        for _ in range(2):
            for qname,q in qs:
                c=inner(q,w,invcov); w=sub(w,scale(q,c))
        n=wnorm(w,invcov)
        ratio=n/max(n0,1e-300)
        diagnostics.append({'parameter':name,'input_norm':n0,'independent_fraction':ratio})
        if ratio>1e-8:
            qs.append((name,scale(w,1.0/n)))
    return qs,diagnostics


def project_out(s,qs,invcov):
    r=s[:]; coeff={}
    for _ in range(2):
        for name,q in qs:
            c=inner(q,r,invcov)
            coeff[name]=coeff.get(name,0.0)+c
            r=sub(r,scale(q,c))
    return r,coeff


def euclidean_peak_fraction(ells,base,s,r):
    peaks=[max(abs(base[l][j]) for l in ells) for j in range(3)]
    sn=[]; rn=[]
    for i,l in enumerate(ells):
        for j in range(3):
            p=max(peaks[j],1e-300)
            sn.append(s[3*i+j]/p); rn.append(r[3*i+j]/p)
    return norm2(rn)/max(norm2(sn),1e-300)


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('output_dir'); ap.add_argument('--json-out',default='results/v020_analysis.json'); args=ap.parse_args()
    out=Path(args.output_dir)
    labels=['force_l0','force_p300','force_m300','force_p1000','force_m1000']
    for p in PARAMS:
        for w in ('full','half'):
            labels += [f'{p}_{w}_p',f'{p}_{w}_m']
    maps={lab:load_cl(clpath(out,lab)) for lab in labels}
    ells=sorted(set.intersection(*(set(maps[k]) for k in maps)))
    if len(ells)<1000: raise RuntimeError(f'too few common multipoles: {len(ells)}')
    base=maps['force_l0']; invcov=make_invcov(ells,base)

    s300=vec_from_maps(ells,maps['force_p300'],maps['force_m300'],600.0)
    s1000=vec_from_maps(ells,maps['force_p1000'],maps['force_m1000'],2000.0)
    mem_control={'relative_CV_norm':wrel(s300,s1000,invcov),'cosine_CV':wcos(s300,s1000,invcov),
                 'norm300_CV':wnorm(s300,invcov),'norm1000_CV':wnorm(s1000,invcov)}

    deriv_full={}; deriv_half={}; stability={}; overlaps={}
    for p in PARAMS:
        deriv_full[p]=derivative(ells,maps[f'{p}_full_p'],maps[f'{p}_full_m'],p,'full')
        deriv_half[p]=derivative(ells,maps[f'{p}_half_p'],maps[f'{p}_half_m'],p,'half')
        stability[p]={'relative_CV_norm':wrel(deriv_full[p],deriv_half[p],invcov),
                      'cosine_CV':wcos(deriv_full[p],deriv_half[p],invcov)}
        overlaps[p]=wcos(s1000,deriv_half[p],invcov)

    qs,bdiag=orthonormalize([(p,deriv_half[p]) for p in PARAMS],invcov)
    residual,coeff=project_out(s1000,qs,invcov)
    raw=wnorm(s1000,invcov); marg=wnorm(residual,invcov); retained=marg/max(raw,1e-300)

    bands={'30-100':(30,100),'101-500':(101,500),'501-1000':(501,1000),'1001-2500':(1001,2500)}
    band_snr={}
    for name,(lo,hi) in bands.items():
        mask=[lo<=l<=hi for l in ells]
        band_snr[name]={'raw_per_eta':wnorm(s1000,invcov,mask),'marginalized_per_eta':wnorm(residual,invcov,mask)}

    nuisance_ok=all(x['relative_CV_norm']<0.05 and x['cosine_CV']>0.999 for x in stability.values())
    memory_ok=mem_control['relative_CV_norm']<0.05 and mem_control['cosine_CV']>0.999
    rank_ok=len(qs)>=5
    distinct=retained>=0.25
    partly_distinct=retained>=0.10
    cv_visible=marg>=1.0

    if nuisance_ok and memory_ok and rank_ok and distinct and cv_visible:
        classification='PASS_DISTINCT_MEMORY_FINGERPRINT_CV_VISIBLE_PER_UNIT_ETA'
    elif nuisance_ok and memory_ok and rank_ok and distinct:
        classification='PASS_DISTINCT_MEMORY_FINGERPRINT_LOW_UNIT_ETA_SIGNIFICANCE'
    elif nuisance_ok and memory_ok and rank_ok and partly_distinct:
        classification='PASS_PARTIALLY_DISTINCT_MEMORY_FINGERPRINT'
    elif nuisance_ok and memory_ok and rank_ok:
        classification='MEMORY_TANGENT_LARGELY_DEGENERATE_WITH_CORE_LCDM'
    else:
        classification='V020_NUMERICAL_OR_NUISANCE_BASIS_FOLLOWUP_REQUIRED'

    res={
        'model':'Exp','tauH0':1.0,'ell_range':[LMIN,LMAX],'channels':['TT','EE','TE'],'lensing':False,
        'metric':'full-sky cosmic-variance covariance of TT/EE/TE, no instrumental noise',
        'memory_tangent':'eta=0 variational forcing; lambda1000 primary, lambda300 control; lambda is numerical amplifier, not physical eta',
        'memory_control':mem_control,
        'nuisance_parameters':PARAMS,
        'nuisance_derivative_stability':stability,
        'memory_vs_parameter_CV_cosines':overlaps,
        'nuisance_basis_rank':len(qs),
        'nuisance_basis_independence':bdiag,
        'projection_coefficients_in_orthonormal_basis':coeff,
        'raw_CV_SNR_per_unit_eta':raw,
        'marginalized_CV_SNR_per_unit_eta':marg,
        'CV_retained_fraction_after_core_LCDM_projection':retained,
        'peak_normalized_Euclidean_retained_fraction':euclidean_peak_fraction(ells,base,s1000,residual),
        'eta_for_CV_SNR_1':(1.0/marg if marg>0 else None),
        'eta_for_CV_SNR_3':(3.0/marg if marg>0 else None),
        'band_SNR_per_unit_eta':band_snr,
        'gates':{'memory_tangent_control':memory_ok,'nuisance_derivative_stability':nuisance_ok,'nuisance_rank':rank_ok,
                 'distinct_fraction_ge_0p25':distinct,'marginalized_CV_SNR_per_unit_eta_ge_1':cv_visible},
        'classification':classification,
        'scope':'core six-parameter LambdaCDM projection only; unlensed CV-limited forecast; no experiment likelihood, lensing, foreground, or extended-parameter claim',
    }
    p=Path(args.json_out); p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(res,indent=2)); print(json.dumps(res,indent=2))

if __name__=='__main__': main()
