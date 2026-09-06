#!/usr/bin/env python3
from pathlib import Path
import argparse, json, math
import numpy as np
from scipy.io import FortranFile
from scipy.optimize import minimize_scalar
from getdist.inifile import IniFile

ETA_GRID=np.array([-10.,-7.5,-5.,-2.5,0.,2.5,5.,7.5,10.])
APL_SIGMA=0.0025
TCMB_UK=2.7255e6


def load_class_dl(path):
    arr=np.loadtxt(path)
    if arr.ndim!=2 or arr.shape[1] < 4: raise RuntimeError(f'bad CLASS cl file {path}: shape={arr.shape}')
    ell=arr[:,0].astype(int)
    # CLASS format for _cl.dat is D_l=l(l+1)C_l/(2pi), dimensionless.
    # Column order for tCl,pCl is TT EE TE (followed by possible lensing columns).
    conv=TCMB_UK**2
    tt=arr[:,1]*conv; ee=arr[:,2]*conv; te=arr[:,3]*conv
    return ell,tt,te,ee


def find_dataset(packages):
    cands=list(Path(packages).rglob('*.dataset'))
    good=[]
    for p in cands:
        try:
            ini=IniFile(str(p)); use=[x.lower() for x in ini.list('use_cl')]
            if all(x in use for x in ['tt','te','ee']) and ini.int('nbintt')>0 and ini.int('nbinte')>0 and ini.int('nbinee')>0:
                good.append(p)
        except Exception:
            pass
    if not good: raise RuntimeError(f'no TTTEEE Plik-lite dataset found under {packages}; candidates={len(cands)}')
    # Prefer the explicitly native 2018 plik-lite directory.
    good.sort(key=lambda p:(0 if 'pliklite' in str(p).lower() or 'plik_lite' in str(p).lower() else 1,len(str(p))))
    return good[0]


class PlikLite:
    def __init__(self,dataset):
        ini=IniFile(str(dataset)); self.dataset=str(dataset)
        self.use_cl=[c.lower() for c in ini.list('use_cl')]
        nbintt=ini.int('nbintt'); nbinte=ini.int('nbinte'); nbinee=ini.int('nbinee')
        data=np.loadtxt(ini.relativeFileName('data'))
        off=ini.int('bin_lmin_offset')
        self.blmin=np.loadtxt(ini.relativeFileName('blmin')).astype(int)+off
        self.blmax=np.loadtxt(ini.relativeFileName('blmax')).astype(int)+off
        lav=(self.blmin+self.blmax)//2
        weights=np.loadtxt(ini.relativeFileName('weights'))
        ls=np.arange(len(weights))+off
        weights=weights*2*np.pi/ls/(ls+1)
        self.weights=np.hstack((np.zeros(off),weights))
        self.nbins=nbintt+nbinte+nbinee
        bfile=ini.relativeFileName('cov_file_binary')
        if Path(bfile).exists():
            f=FortranFile(bfile,'r'); cov=f.read_reals(dtype=float).reshape((self.nbins,self.nbins)); cov=np.tril(cov)+np.tril(cov,-1).T
        else:
            cov=np.loadtxt(ini.relativeFileName('cov_file'))
        maxbin=max(nbintt,nbinte,nbinee); self.used_bins=[]; inds=[]; offset=0
        for cl,nbin in zip(['tt','te','ee'],[nbintt,nbinte,nbinee]):
            if cl in self.use_cl:
                u=np.arange(nbin,dtype=int); self.used_bins.append(u); inds.append(u+offset)
            else: self.used_bins.append(np.arange(0,dtype=int))
            offset += nbin
        self.used_indices=np.hstack(inds); self.X_data=data[self.used_indices,1]
        self.cov=cov[np.ix_(self.used_indices,self.used_indices)]; self.invcov=np.linalg.inv(self.cov)
        self.lmax=ini.int('lmax'); self.lav=lav[:maxbin]
    def chi2(self,L0,tt,te,ee,A=1.0):
        cl=np.empty(self.used_indices.shape); ix=0
        for tp,cell in enumerate([tt,te,ee]):
            for i in self.used_bins[tp]:
                cl[ix]=np.dot(cell[self.blmin[i]-L0:self.blmax[i]-L0+1], self.weights[self.blmin[i]:self.blmax[i]+1]); ix+=1
        cl/=A**2; d=self.X_data-cl
        return float(d@self.invcov@d)


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--base',required=True); ap.add_argument('--plus',required=True); ap.add_argument('--minus',required=True)
    ap.add_argument('--packages',required=True); ap.add_argument('--json-out',required=True); ap.add_argument('--meta',required=True)
    a=ap.parse_args(); meta=json.loads(Path(a.meta).read_text())
    eb,ttb,teb,eeb=load_class_dl(a.base); ep,ttp,tep,eep=load_class_dl(a.plus); em,ttm,tem,eem=load_class_dl(a.minus)
    if not (np.array_equal(eb,ep) and np.array_equal(eb,em)): raise RuntimeError('CLASS ell grids differ')
    if eb[0] > 2: raise RuntimeError(f'CLASS spectrum starts at ell={eb[0]}, expected <=2')
    # Centered response per unit eta from the locked numerical amplification lambda=10.
    dtt=(ttp-ttm)/20.; dte=(tep-tem)/20.; dee=(eep-eem)/20.
    like=PlikLite(find_dataset(a.packages))
    if eb[-1] < like.lmax: raise RuntimeError(f'CLASS lmax={eb[-1]} < Planck required {like.lmax}')
    L0=int(eb[0]); rows=[]
    for eta in ETA_GRID:
        tt=ttb+eta*dtt; te=teb+eta*dte; ee=eeb+eta*dee
        def obj(A): return like.chi2(L0,tt,te,ee,A)+((A-1.)/APL_SIGMA)**2
        opt=minimize_scalar(obj,bounds=(0.98,1.02),method='bounded',options={'xatol':1e-10})
        rows.append({'eta':float(eta),'chi2_profiled':float(opt.fun),'A_planck':float(opt.x),'planck_chi2':float(like.chi2(L0,tt,te,ee,opt.x))})
    best=min(rows,key=lambda r:r['chi2_profiled']); c0=next(r for r in rows if r['eta']==0.0)['chi2_profiled']
    for r in rows: r['delta_chi2_vs_eta0']=float(r['chi2_profiled']-c0)
    # Local quadratic diagnostic using the best grid point and neighbors, only if interior.
    etahat=sigma=None; qfit=None
    j=rows.index(best)
    if 0<j<len(rows)-1:
        xs=np.array([rows[j-1]['eta'],rows[j]['eta'],rows[j+1]['eta']]); ys=np.array([rows[j-1]['chi2_profiled'],rows[j]['chi2_profiled'],rows[j+1]['chi2_profiled'])
        co=np.polyfit(xs,ys,2); A2,B2,C2=co
        if A2>0:
            etahat=float(-B2/(2*A2)); sigma=float(1/math.sqrt(A2)); qfit={'a':float(A2),'b':float(B2),'c':float(C2)}
    res={
      'classification':'V054_PLANCK_HIGHL_FIXED_COSMOLOGY_PROFILE_COMPLETE',
      'likelihood_dataset':like.dataset,'planck_lmax':like.lmax,'eta_grid':rows,
      'best_grid_eta':best['eta'],'best_profiled_chi2':best['chi2_profiled'],'eta0_profiled_chi2':c0,
      'delta_chi2_best_vs_eta0':float(best['chi2_profiled']-c0),'quadratic_eta_hat':etahat,'quadratic_sigma_eta':sigma,'quadratic_fit':qfit,
      'locked_model':{'KB':meta['KB'],'tauH0':meta['tauH0'],'p':meta['p'],'lambda':meta['lambda'],'cosmology':meta['cosmology']},
      'scope':meta['scope'],
      'interpretation_rule':'This is the first real Planck high-l directional test at the pre-locked cosmology, with only A_planck profiled. It is not the final six-parameter marginalized eta posterior.',
      'anti_tuning':meta['anti_tuning']
    }
    Path(a.json_out).write_text(json.dumps(res,indent=2)); print(json.dumps(res,indent=2))

if __name__=='__main__': main()
