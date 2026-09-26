#!/usr/bin/env python3
"""GE19 H4F3d13: exact original R1 one-sided GE05 bath Euler/FD4 signed-Ward assembly.

Pure deterministic array helper. The physical driver supplies the FROZEN
Repair24 R1 (z,v,X,r,w,tau) parent and exact original FD4+signed convolution.
All outputs are report-only. This code never declares bath on-shell.
"""
from __future__ import annotations
import numpy as np

MODES=np.asarray([3,5,8,10,15,20],int)
M_MAX=40
TINY=1e-300

def l2(a):
    return float(np.linalg.norm(np.asarray(a)))

def rel(a,b):
    aa=np.asarray(a);bb=np.asarray(b)
    return l2(aa-bb)/max(l2(aa),l2(bb),TINY)

def interval_signed(z,v,X,a,H,x,r,w,tau,kfund,fd4,convolve):
    z=np.asarray(z,complex);v=np.asarray(v,complex)
    X=np.asarray(X,complex)
    a=np.asarray(a,float);H=np.asarray(H,float);x=np.asarray(x,float)
    r=np.asarray(r,float);w=np.asarray(w,float)
    if (z.ndim!=3 or z.shape!=v.shape or z.shape[1]!=len(MODES)
        or z.shape[2]!=len(x) or X.shape!=(len(MODES),len(x))
        or a.shape!=x.shape or H.shape!=x.shape
        or r.shape!=w.shape or z.shape[0]!=len(r)
        or not np.all(np.diff(x)>0) or np.any(r<=0)
        or np.any(w<=0) or np.any(a<=0) or np.any(H<=0)
        or not np.isfinite(tau) or tau<=0
        or not np.isfinite(kfund) or kfund<=0
        or any(not np.isfinite(q).all() for q in (z,v,X,a,H,x,r,w))):
        raise ValueError("D13 actual original R1 bath arrays or original mode/clock invalid")
    nb,nm,nt=z.shape
    omega=r[:,None,None]/tau
    ww=np.sqrt(w)[:,None,None]
    a3=a[None,None,:]**3
    rr2=r[:,None,None]**2
    current=a3*v/tau
    sampled_kinetic=H[None,None,:]*fd4(current,x)
    potential=a3*omega**2*(z-X[None,:,:])
    Rfd=sampled_kinetic+potential
    Efd=-ww/(2*omega)*Rfd
    qx=ww/omega*(1j*kfund*MODES[None,:,None])*z
    Wfd=convolve(Efd,qx)
    if Wfd.shape!=(nt,M_MAX+1):
        raise ValueError("D13 original FD4 signed bath array scope changed")
    hmid=np.sqrt(H[:-1]*H[1:])
    hinterval=tau*hmid
    phase=r[:,None]*np.diff(x)[None,:]/hinterval[None,:]
    if phase.shape!=(nb,nt-1) or not np.isfinite(phase).all():
        raise ValueError("D13 original R1 phase node/interval invalid")
    out={"FD4_original_signed_W":Wfd}
    row={}
    for side,sl,nh,ah,interval_H in (
         ("left",slice(1,None),H[1:],a3[:,:,1:],hinterval),
         ("right",slice(None,-1),H[:-1],a3[:,:,:-1],hinterval)):
        vs=v[:,:,sl];zs=z[:,:,sl];drive=X[None,:,sl]
        jt=(3*nh[None,None,:]*ah*vs/tau
            +ah*(-3*interval_H[None,None,:]*vs
                 -rr2*(zs-drive))/tau**2)
        pot=ah*(r[:,None,None]/tau)**2*(zs-drive)
        ode=jt+pot
        explicit=3*ah*(nh[None,None,:]-interval_H[None,None,:]/tau)*vs/tau
        defect=sampled_kinetic[:,:,sl]-jt
        eq_def=Rfd[:,:,sl]-ode-defect
        E_ode=-ww/(2*omega)*ode
        E_def=-ww/(2*omega)*defect
        wi=convolve(E_ode,qx[:,:,sl])
        wd=convolve(E_def,qx[:,:,sl])
        wfd=Wfd[sl,:]
        if any(q.shape!=(nt-1,M_MAX+1) for q in (wi,wd,wfd)):
            raise ValueError("D13 original one-sided signed Ward output shape invalid")
        denom=max(l2(wfd)+l2(wi)+l2(wd),TINY)
        norm_r=max(l2(sampled_kinetic[:,:,sl])+l2(pot),TINY)
        row[side]={
          "original_ODE_unsimplified_vs_explicit_interval_H_relative_natural":l2(ode-explicit)/norm_r,
          "original_FD4_equals_interval_ODE_plus_derivative_defect_relative_natural":l2(eq_def)/norm_r,
          "original_signed_FD4_equals_interval_plus_defect_relative_natural":l2(wfd-wi-wd)/denom,
          "one_sided_R_ODE_abs_L2":l2(ode),
          "one_sided_R_FD4_defect_abs_L2":l2(defect),
          "one_sided_signed_interval_W_abs_L2":l2(wi),
          "one_sided_signed_FD4_defect_W_abs_L2":l2(wd),
          "one_sided_signed_FD4_original_W_abs_L2":l2(wfd),
          "signed_interval_not_called_on_shell":True,
          "both_original_interval_ODE_and_FD4_preserved":True
        }
        out[side+"_signed_interval_W"]=wi
        out[side+"_signed_derivative_defect_W"]=wd
        out[side+"_original_R_ODE_mode_time_L2"]=np.linalg.norm(ode,axis=0)
        out[side+"_original_FD4_defect_mode_time_L2"]=np.linalg.norm(defect,axis=0)
        out[side+"_original_interval_phase"]=phase
    if any(not np.isfinite(q).all() for q in out.values()):
        raise RuntimeError("D13 nonfinite original signed bath output")
    return out,row

def signed_convolution_independent(E,qx):
    """Independent signed Fourier convolution, preserving +/- original modes."""
    ee=np.asarray(E,complex);qq=np.asarray(qx,complex)
    if ee.shape!=qq.shape or ee.ndim!=3 or ee.shape[1]!=len(MODES):
        raise ValueError("D13 signed convolution source shape changed")
    out=np.zeros((ee.shape[-1],M_MAX+1),complex)
    for i,pi in enumerate(MODES):
        for j,pj in enumerate(MODES):
            for si in (-1,1):
                for sj in (-1,1):
                    target=int(si*pi+sj*pj)
                    if 0<=target<=M_MAX:
                        e=ee[:,i,:] if si==1 else np.conj(ee[:,i,:])
                        q=qq[:,j,:] if sj==1 else np.conj(qq[:,j,:])
                        out[:,target]+=4*np.sum(e*q,axis=0)
    return out
