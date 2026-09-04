#!/usr/bin/env python3
from pathlib import Path
import argparse,json,math,bisect

PARAMS=['H0','omega_b','omega_cdm','tau_reio','n_s','lnA_s']
BASE={'H0':67.32117,'omega_b':0.02238280,'omega_cdm':0.1201075,
      'tau_reio':0.05430842,'n_s':0.9660499,'A_s':2.100549e-09}
HALF={'H0':('fractional',0.0025),'omega_b':('fractional',0.005),
      'omega_cdm':('fractional',0.005),'tau_reio':('absolute',0.0015),
      'n_s':('absolute',0.003),'lnA_s':('log',0.01)}
LMIN,LMAX=30,2500

def load_cl(path):
    d={}
    with open(path,'r',errors='replace') as f:
        for line in f:
            t=line.strip()
            if not t or t.startswith('#'): continue
            p=t.split()
            if len(p)<4: continue
            try: ell=int(round(float(p[0]))); vals=(float(p[1]),float(p[2]),float(p[3]))
            except ValueError: continue
            if LMIN<=ell<=LMAX: d[ell]=vals
    if not d: raise RuntimeError(f'no Cl data in {path}')
    return d

def clpath(out,label):
    p=out/f'v021_{label}__cl.dat'
    if not p.exists(): raise RuntimeError(f'missing {p}')
    return p

def sub(a,b): return [x-y for x,y in zip(a,b)]
def scale(a,c): return [c*x for x in a]
def dot(a,b): return sum(x*y for x,y in zip(a,b))
def norm(a): return math.sqrt(max(dot(a,a),0.0))

def vec(ells,A,B=None,den=1.0):
    v=[]
    if B is None:
        for l in ells: v.extend(A[l])
    else:
        for l in ells: v.extend([(A[l][j]-B[l][j])/den for j in range(3)])
    return v

def inv3(A):
    M=[list(A[i])+[1.0 if i==j else 0.0 for j in range(3)] for i in range(3)]
    for c in range(3):
        p=max(range(c,3),key=lambda r:abs(M[r][c]))
        if abs(M[p][c])<1e-300: raise RuntimeError('singular covariance')
        if p!=c: M[c],M[p]=M[p],M[c]
        z=M[c][c]; M[c]=[x/z for x in M[c]]
        for r in range(3):
            if r==c: continue
            z=M[r][c]; M[r]=[M[r][j]-z*M[c][j] for j in range(6)]
    return [r[3:] for r in M]

def invcov(ells,base):
    out=[]
    for l in ells:
        tt,ee,te=base[l]; f=1.0/(2*l+1.0)
        C=[[2*f*tt*tt,2*f*te*te,2*f*tt*te],
           [2*f*te*te,2*f*ee*ee,2*f*ee*te],
           [2*f*tt*te,2*f*ee*te,f*(te*te+tt*ee)]]
        sc=max(abs(C[0][0]),abs(C[1][1]),abs(C[2][2]),1e-300); eps=sc*1e-14
        out.append(inv3([[C[i][j]+(eps if i==j else 0.0) for j in range(3)] for i in range(3)]))
    return out

def inner(a,b,W,mask=None):
    s=0.0
    for i,M in enumerate(W):
        if mask is not None and not mask[i]: continue
        x=a[3*i:3*i+3]; y=b[3*i:3*i+3]
        My=[sum(M[r][c]*y[c] for c in range(3)) for r in range(3)]
        s+=sum(x[r]*My[r] for r in range(3))
    return s

def wnorm(a,W,mask=None): return math.sqrt(max(inner(a,a,W,mask),0.0))
def wcos(a,b,W):
    na,nb=wnorm(a,W),wnorm(b,W)
    return inner(a,b,W)/(na*nb) if na>0 and nb>0 else 1.0
def wrel(a,b,W): return wnorm(sub(a,b),W)/max(wnorm(b,W),1e-300)

def delta(p):
    kind,h=HALF[p]
    if p=='lnA_s': return h
    if kind=='fractional': return BASE[p]*h
    return h

def orthonormalize(vectors,W):
    qs=[]; diag=[]
    for name,v in vectors:
        q=v[:]; n0=wnorm(q,W)
        for _ in range(2):
            for _,u in qs: q=sub(q,scale(u,inner(u,q,W)))
        n=wnorm(q,W); frac=n/max(n0,1e-300)
        diag.append({'parameter':name,'input_norm':n0,'independent_fraction':frac})
        if frac>1e-8: qs.append((name,scale(q,1.0/n)))
    return qs,diag

def project(s,qs,W):
    r=s[:]
    for _ in range(2):
        for _,q in qs: r=sub(r,scale(q,inner(q,r,W)))
    return r

def load_force(path):
    g={}
    with open(path) as f:
        for line in f:
            t=line.strip()
            if not t or t.startswith('#'): continue
            p=t.split()
            if len(p)<3: continue
            k,tt,ff=map(float,p[:3]); g.setdefault(k,[]).append((tt,ff))
    for k in g: g[k].sort()
    return g

def nearest_key(keys,k):
    i=bisect.bisect_left(keys,k); cand=[]
    if i<len(keys): cand.append(keys[i])
    if i>0: cand.append(keys[i-1])
    if not cand: return None
    q=min(cand,key=lambda x:abs(x-k))
    return q if abs(q-k)/max(abs(k),1e-300)<2e-10 else None

def interp(seq,t):
    ts=[x[0] for x in seq]; i=bisect.bisect_left(ts,t)
    if i==0: return seq[0][1]
    if i>=len(seq): return seq[-1][1]
    t0,f0=seq[i-1]; t1,f1=seq[i]
    if t1<=t0: return f0
    x=(t-t0)/(t1-t0); return f0+x*(f1-f0)

def force_control(p256,p512):
    a=load_force(p256); b=load_force(p512); ka=sorted(a)
    x=[]; y=[]
    for k,seq in b.items():
        q=nearest_key(ka,k)
        if q is None: continue
        for t,f in seq:
            x.append(interp(a[q],t)); y.append(f)
    if not y: raise RuntimeError('no common force-table samples')
    d=[u-v for u,v in zip(x,y)]
    rel=norm(d)/max(norm(y),1e-300)
    cos=dot(x,y)/max(norm(x)*norm(y),1e-300)
    return {'relative_L2':rel,'cosine':cos,'samples':len(y)}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('output_dir'); ap.add_argument('--tau',type=float,required=True); ap.add_argument('--tag',required=True)
    ap.add_argument('--force256',required=True); ap.add_argument('--force512',required=True)
    ap.add_argument('--json-out',required=True)
    args=ap.parse_args(); out=Path(args.output_dir)
    labels=['force_l0','force_p300','force_m300','force_p1000','force_m1000']
    for p in PARAMS: labels += [f'nuis_{p}_p',f'nuis_{p}_m']
    maps={lab:load_cl(clpath(out,lab)) for lab in labels}
    ells=sorted(set.intersection(*(set(m) for m in maps.values())))
    if len(ells)<1000: raise RuntimeError(f'too few common multipoles {len(ells)}')
    base=maps['force_l0']; W=invcov(ells,base)
    s300=vec(ells,maps['force_p300'],maps['force_m300'],600.0)
    s1000=vec(ells,maps['force_p1000'],maps['force_m1000'],2000.0)
    mem={'relative_CV_norm':wrel(s300,s1000,W),'cosine_CV':wcos(s300,s1000,W),
         'norm300_CV':wnorm(s300,W),'norm1000_CV':wnorm(s1000,W)}
    deriv={}; overlaps={}
    for p in PARAMS:
        deriv[p]=vec(ells,maps[f'nuis_{p}_p'],maps[f'nuis_{p}_m'],2.0*delta(p))
        overlaps[p]=wcos(s1000,deriv[p],W)
    qs,bdiag=orthonormalize([(p,deriv[p]) for p in PARAMS],W)
    residual=project(s1000,qs,W)
    raw=wnorm(s1000,W); marg=wnorm(residual,W); retained=marg/max(raw,1e-300)
    fc=force_control(args.force256,args.force512)
    bands={'30-100':(30,100),'101-500':(101,500),'501-1000':(501,1000),'1001-2500':(1001,2500)}
    bs={}
    for name,(lo,hi) in bands.items():
        mask=[lo<=l<=hi for l in ells]
        bs[name]={'raw_per_eta':wnorm(s1000,W,mask),'marginalized_per_eta':wnorm(residual,W,mask)}
    bath_ok=fc['relative_L2']<0.05 and fc['cosine']>0.999
    tangent_ok=mem['relative_CV_norm']<0.05 and mem['cosine_CV']>0.999
    rank_ok=len(qs)==6
    if bath_ok and tangent_ok and rank_ok:
        if marg>=1: classification='PASS_TAU_POINT_CV_VISIBLE_PER_UNIT_ETA'
        elif marg>=0.1: classification='PASS_TAU_POINT_STRONG_SUBUNIT_ETA_FORECAST'
        elif marg>=1e-3: classification='PASS_TAU_POINT_DISTINCT_LOW_SIGNIFICANCE'
        else: classification='PASS_TAU_POINT_DISTINCT_VERY_LOW_SIGNIFICANCE'
    else:
        classification='TAU_POINT_NUMERICAL_FOLLOWUP_REQUIRED'
    res={'model':'Exp','tauH0':args.tau,'tag':args.tag,'ell_range':[LMIN,LMAX],
         'channels':['TT','EE','TE'],'lensing':False,
         'bath':'direct positive tan-theta Drude quadrature; N512 primary, N256 control',
         'bath_force_convergence_N256_vs_N512':fc,
         'memory_tangent_control_lambda300_vs1000':mem,
         'nuisance_parameters':PARAMS,'nuisance_basis_rank':len(qs),
         'nuisance_basis_independence':bdiag,'memory_vs_parameter_CV_cosines':overlaps,
         'raw_CV_SNR_per_unit_eta':raw,'marginalized_CV_SNR_per_unit_eta':marg,
         'CV_retained_fraction_after_core_LCDM_projection':retained,
         'eta_for_CV_SNR_1':1.0/marg if marg>0 else None,
         'eta_for_CV_SNR_3':3.0/marg if marg>0 else None,
         'band_SNR_per_unit_eta':bs,
         'gates':{'bath_convergence':bath_ok,'tangent_extraction':tangent_ok,'nuisance_rank':rank_ok},
         'classification':classification,
         'scope':'unlensed full-sky CV TT/EE/TE; six core LambdaCDM nuisance directions; no instrumental noise/foregrounds/lensing'}
    q=Path(args.json_out); q.parent.mkdir(parents=True,exist_ok=True); q.write_text(json.dumps(res,indent=2))
    print(json.dumps(res,indent=2))

if __name__=='__main__': main()
