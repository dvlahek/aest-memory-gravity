#!/usr/bin/env python3
"""GE19 D15a: original GE05 action on the x-embedded frozen R1 state.

The R1 step's internal clock dx/ds=hmid is not physical dx/ds=tau*H(x).
Here the physical x=ln(a) derivative of the original R1 z_step(x) is
z_t=gamma*v_step/tau, gamma=tau*H(x)/hmid. The result is an exact
conditional algebraic source, not a certified continuous bath solution.
"""
from __future__ import annotations
import numpy as np

MODES=np.array([3,5,8,10,15,20],int)
M_MAX=40
TINY=1.e-300

def l2(a):
    return float(np.linalg.norm(np.asarray(a)))

def relative(a,b):
    return l2(np.asarray(a)-np.asarray(b))/max(l2(a),l2(b),TINY)

def make_original_action_background(r7,bg,tag):
    """Original Repair13/Repair07 stable Exp action H(x), H_x(x).

    Scalar charge I0=a^3 KQ and Lambda are checked on the immutable
    original knots; this is a source/identity check, not an independent
    continuous solution/error enclosure for the numerical first-order H1.
    """
    x=np.asarray(bg['x'],float)
    a=np.asarray(bg['a'],float)
    kq=np.asarray(bg['KQ_action'],float)
    original_H=np.asarray(bg['H'],float)
    rho_l=np.asarray(bg['rho_lambda_action'],float)
    if not (x.ndim==a.ndim==kq.ndim==original_H.ndim==rho_l.ndim==1
            and x.size==a.size==kq.size==original_H.size==rho_l.size
            and x.size>=9 and np.all(np.diff(x)>0)
            and np.all(a>0) and np.all(kq>0)
            and np.all(original_H>0)
            and all(np.isfinite(q).all() for q in (x,a,kq,original_H,rho_l))):
        raise ValueError('D15a invalid original Repair13 action background')
    if not np.allclose(a,np.exp(x),rtol=1e-13,atol=1e-14):
        raise RuntimeError('D15a original a=exp(x) action clock changed')
    i0_samples=a**3*kq
    i0=float(np.median(i0_samples))
    charge_rel=float(np.max(np.abs(i0_samples-i0))/max(np.max(np.abs(i0_samples)),TINY))
    lam=float(np.median(rho_l))
    lambda_rel=float(np.max(np.abs(rho_l-lam))/max(np.max(np.abs(rho_l)),1.0))
    # Original positive stable Exp source and original homogeneous Lambda
    # are exact background identities, NOT adjustable physical tolerances.
    if charge_rel>1e-10 or lambda_rel>1e-13:
        raise RuntimeError('D15a original scalar charge or Lambda background changed')
    C=float(r7.C_VALUES[tag])

    def evaluate(xq):
        xx=np.asarray(xq,float)
        if np.any(xx<x[0]-1e-13) or np.any(xx>x[-1]+1e-13):
            raise ValueError('D15a would extrapolate original action window')
        kq_eval=i0*np.exp(-3.0*xx)
        Z=np.asarray(r7.exp_Z_from_KQ(kq_eval),float)
        Q=r7.Q0+r7.Z0*Z
        ex=kq_eval/(4.0*r7.K2*r7.Z0*Z)
        K=2.0*r7.K2*r7.Z0**2*(ex-1.0)
        dust=C*np.exp(-3.0*xx)
        H2=(Q*kq_eval-K)/3.0+dust+lam
        if not np.all(np.isfinite(H2)) or np.any(H2<=0):
            raise RuntimeError('D15a action-source H2 nonpositive/nonfinite')
        H=np.sqrt(H2)
        Hx=(-Q*kq_eval-3.0*dust)/(2.0*H)
        if not np.all(np.isfinite(Hx)):
            raise RuntimeError('D15a original action H_x nonfinite')
        return H,Hx

    reconstructed,_=evaluate(x)
    H_relative=relative(reconstructed,original_H)
    H_max=float(np.max(np.abs(reconstructed-original_H)))
    if H_relative>1e-10:
        raise RuntimeError('D15a original action H differs from frozen Repair13 H knots')
    return evaluate,{
        'original_action_I0':i0,'original_action_rho_lambda':lam,
        'scalar_charge_knot_max_relative_machine':charge_rel,
        'rho_lambda_knot_max_relative_machine':lambda_rel,
        'original_action_H_knot_relative_machine':H_relative,
        'original_action_H_knot_max_absolute_machine':H_max,
        'original_source_action_H_and_Hx_but_not_true_H1_drive':True}

def unsigned_signed_pair_envelope(E,qx,mask=None):
    """Original +/- six-mode, all-node noncancelling Fourier upper bound.

    |W[m,t]|<=U[m,t] for the signed original +4 E_q10 partial_chi q10
    convolution when E and qx are the actual coefficient arrays.
    """
    ee=np.asarray(E,complex);qq=np.asarray(qx,complex)
    if ee.ndim!=3 or ee.shape!=qq.shape or ee.shape[1]!=len(MODES):
        raise ValueError('D15a original signed source array shapes changed')
    nq,nm,nt=ee.shape
    if mask is None:
        keep=np.ones((nq,nt),bool)
    else:
        keep=np.asarray(mask,bool)
        if keep.shape!=(nq,nt):
            raise ValueError('D15a original R1 phase mask invalid')
    out=np.zeros((nt,M_MAX+1),float)
    for i,mi in enumerate(MODES):
        ei=np.abs(ee[:,i,:])*keep
        for j,mj in enumerate(MODES):
            contribution=4.0*np.einsum('bt,bt->t',ei,np.abs(qq[:,j,:]),optimize=True)
            for si in (-1,1):
                for sj in (-1,1):
                    m=int(si*mi+sj*mj)
                    if 0<=m<=M_MAX:
                        out[:,m]+=contribution
    if not np.all(np.isfinite(out)) or np.any(out<0):
        raise RuntimeError('D15a original signed source unsigned envelope nonfinite')
    return out

def x_embedded_clock_source(z,v,Xlin,a,H,Hx,hmid,r,w,tau,kfund,convolve):
    """Actual original R1 field z_step(x): conditional original GE05 source.

    All arrays at the SAME physical x collocation points on original R1
    intervals. Actual true drive Xtrue is unspecified: returned U_X is a
    rigorous sampled signed-W bound COEFFICIENT for eps_X per input mode,
    not a numerical value for the unknown original continuous drive error.
    """
    zz=np.asarray(z,complex);vv=np.asarray(v,complex)
    xx=np.asarray(Xlin,complex);aa=np.asarray(a,float)
    HH=np.asarray(H,float);Hx=np.asarray(Hx,float)
    hmid=np.asarray(hmid,float);rr=np.asarray(r,float);ww=np.asarray(w,float)
    if (zz.ndim!=3 or zz.shape!=vv.shape or zz.shape[1]!=len(MODES)
        or xx.shape!=zz.shape[1:] or aa.shape!=HH.shape or aa.shape!=Hx.shape
        or aa.shape!=hmid.shape or aa.shape!=(zz.shape[-1],)
        or rr.shape!=(zz.shape[0],) or ww.shape!=rr.shape
        or np.any(aa<=0) or np.any(HH<=0) or np.any(hmid<=0)
        or np.any(rr<=0) or np.any(ww<=0) or tau<=0 or kfund<=0
        or any(not np.isfinite(q).all() for q in (zz,vv,xx,aa,HH,Hx,hmid,rr,ww))):
        raise ValueError('D15a invalid original clock-embedded source arrays')
    nq,nm,nt=zz.shape
    omega=rr[:,None,None]/tau
    sqrtw=np.sqrt(ww)[:,None,None]
    gamma=tau*HH/hmid
    a3=aa[None,None,:]**3
    pot=a3*omega**2*(1.0-gamma[None,None,:]**2)*(zz-xx[None,:,:])
    clock_der=a3*(gamma*Hx)[None,None,:]*vv/tau
    Rclock=pot+clock_der
    Eclock=-sqrtw/(2.0*omega)*Rclock
    qx=(sqrtw/omega)*(1j*kfund*MODES[None,:,None])*zz
    Wclock=convolve(Eclock,qx)
    if Wclock.shape!=(nt,M_MAX+1):
        raise RuntimeError('D15a original signed m0..40 mode support changed')
    unsigned_clock=unsigned_signed_pair_envelope(Eclock,qx)
    ecoef=np.broadcast_to(-sqrtw*omega/2.0*a3,(nq,nm,nt))
    U_X=unsigned_signed_pair_envelope(ecoef,qx)
    if np.any(np.abs(Wclock)>unsigned_clock*(1+1e-11)+1e-25):
        raise RuntimeError('D15a clock source unsigned envelope violated')
    if not all(np.isfinite(q).all() for q in (gamma,Rclock,Wclock,unsigned_clock,U_X)):
        raise RuntimeError('D15a nonfinite original clock source')
    return {
      'gamma':gamma,
      'signed_W_clock':Wclock,
      'unsigned_W_clock_envelope':unsigned_clock,
      'conditional_unsigned_W_drive_per_max_eps_X':U_X,
      'clock_R_node_mode_L2':np.linalg.norm(Rclock,axis=0),
      'no_original_continuous_Xtrue_error_enclosure':True,
      'no_continuous_time_bath_onshell_claim':True}
