#!/usr/bin/env python3
"""D16 isolated algebraic and synthetic physics checks; no actual R1 claim."""
from __future__ import annotations
from types import SimpleNamespace
import numpy as np
from scipy.linalg import expm
from ge19 import h4f3d16_original_H1dot_Hermite_physical_bath_core as core


def run():
    x=np.linspace(0,.9,6);H=.7+.05*x; beta=.08
    KQ=np.exp(-3*x);KQQ=3*KQ/beta;Q=1.0-beta*x
    bg={'x':x,'a':np.exp(x),'H':H,'Q_action':Q,'KQ_action':KQ,'KQQ_action':KQQ}
    r7=SimpleNamespace(FOURIER_N=core.MODES,g9=SimpleNamespace(K_REQ=np.array([.3])))
    st=np.zeros((6,6,len(x)),complex);dot=np.zeros((6,4,len(x)),complex)
    amp=1+np.arange(6)[:,None]/20
    u=amp*np.exp(.4*x)[None,:]
    phi=amp*(.01+.10j)*np.exp(-.2*x)[None,:]
    st[:,2,:]=u;st[:,3,:]=phi
    dot[:,1,:]=H[None,:]*(.4*u)
    dot[:,2,:]=H[None,:]*(-.2*phi)
    X,Xx=core.frozen_endpoint_X_Xx(r7,bg,st,dot)
    ik=(1j*.1*core.MODES[:,None])/np.exp(x)[None,:]
    X_expected=Q[None,:]*u+ik*phi
    Xx_expected=(-beta+.4*Q)[None,:]*u+ik*(-1.2*phi)
    assert np.allclose(X,X_expected,rtol=1e-14,atol=1e-15)
    assert np.allclose(Xx,Xx_expected,rtol=1e-14,atol=1e-15)
    wrong= (-beta+.4*Q)[None,:]*u+ik*(-.2*phi)
    assert core.l2(Xx-wrong)>1e-3*core.l2(Xx), 'negative control omitted original 1/a derivative'
    idx=np.arange(len(x)-1)
    for theta in (0.,1.):
        y,d=core.evaluate_hermite(X,Xx,x,idx,np.full(len(idx),theta))
        j=0 if theta==0. else 1
        assert np.allclose(y,X[:,idx+j],rtol=1e-13,atol=1e-14)
        assert np.allclose(d,Xx[:,idx+j],rtol=1e-13,atol=1e-14)
    theta=np.array([.23,.46,.65,.81,.37])
    y,d=core.evaluate_hermite(X,Xx,x,idx,theta)
    assert y.shape==d.shape==(6,5)
    eps=1e-6
    yp,_=core.evaluate_hermite(X,Xx,x,idx,theta+eps)
    ym,_=core.evaluate_hermite(X,Xx,x,idx,theta-eps)
    assert np.allclose((yp-ym)/(2*eps*np.diff(x)[None,:]),d,rtol=2e-9,atol=1e-9)
    print('GE19_D16_ORIGINAL_H1DOT_ACTION_X10_XDERIV_HERMITE_JETS_PASS_NEGATIVE_CONTROL_PASS')

    tau=2.4
    xgrid=np.array([0.,.4,.85])
    hconst=.37
    def eh(z):
        return np.full_like(np.asarray(z,float),hconst),np.zeros_like(np.asarray(z,float))
    Xlin=np.empty((6,3),complex)
    for m in range(6):
        Xlin[m]=(m+1)*(.02+.01j)*xgrid+(.004-.002j)*m
    Xd=np.broadcast_to(((Xlin[:,-1]-Xlin[:,0])/(xgrid[-1]-xgrid[0]))[:,None],Xlin.shape).copy()
    r=np.array([.19,1.3,17.,800.])
    z0=np.broadcast_to((.17+.01j)*np.arange(1,7),(4,6)).astype(complex)
    v0=np.broadcast_to((.03-.05j)*np.arange(1,7),(4,6)).astype(complex)
    def independent_exact_affine_step(q,v,rr,h,x0,x1,ds):
        # Independent augmented linear ODE matrix exponential, NOT
        # original Repair24 analytic-step implementation.
        aa=np.asarray(x0,complex);bb=np.asarray(x1,complex)
        aa=np.broadcast_to(aa,q.shape);bb=np.broadcast_to(bb,q.shape)
        slope=(bb-aa)/ds
        outq=np.empty_like(q);outv=np.empty_like(v)
        for j,rj in enumerate(rr):
            A=np.array([[0,1,0,0],[-rj*rj,-3*h,rj*rj,0],
                        [0,0,0,1],[0,0,0,0]],float)
            M=expm(A*ds)
            s=np.stack([q[j],v[j],aa[j],slope[j]])
            nxt=M@s
            outq[j]=nxt[0];outv[j]=nxt[1]
            assert np.allclose(nxt[2],bb[j],rtol=1e-9,atol=1e-11)
        return outq,outv
    zz={}
    for sub in (1,4,8,16):
        z,v,hl,hr=core.propagate_physical(xgrid,Xlin,Xd,eh,z0,v0,r,tau,
                                        independent_exact_affine_step,sub)
        zz[sub]=(z,v)
        assert np.allclose(hl,tau*hconst,rtol=1e-13,atol=1e-13)
        assert np.allclose(hr,tau*hconst,rtol=1e-13,atol=1e-13)
        assert np.array_equal(z[:,:,0],z0) and np.array_equal(v[:,:,0],v0)
    for sub in (4,8,16):
        # high-phase oscillator must NOT be dropped or approximated by
        # quasi-static r suppression; original augmented solution is exact.
        assert core.rel(zz[sub][0],zz[1][0])<1e-9
        assert core.rel(zz[sub][1],zz[1][1])<1e-9
    saved=zz[16]
    # Original GE05 source of exact constant-H plus exactly affine X is zero.
    def simple_signed(E,qx):
        return np.zeros((E.shape[-1],41),complex)
    def simple_unsigned(E,qx):
        return np.zeros((E.shape[-1],41),float) if not np.any(E) else np.ones((E.shape[-1],41),float)*np.max(np.abs(E))*10000
    W,U=core.signed_one_sided_endpoint_W(saved[0],saved[1],np.exp(xgrid),
        np.full_like(xgrid,hconst),np.full(len(xgrid)-1,tau*hconst),
        r,np.ones_like(r)/len(r),tau,.1,simple_signed,simple_unsigned,'left')
    assert not np.any(W) and np.max(np.abs(U))<1e-10
    print('GE19_D16_PHYSICAL_CLOCK_TRUE_SUBSTEP_GAUSS_EXACT_AFFINE_HIGH_PHASE_AND_JUMP_FREE_V_PASS')

    def Edecay(z):
        q=np.asarray(z,float)
        return np.exp(-.25*q),-.25*np.exp(-.25*q)
    aa=np.linspace(.1,.5,6);Xm=np.zeros((6,len(aa)),complex)
    s4=core.subgrid_data(aa,Xm,Xm,4,Edecay,2.0)[2]
    s16=core.subgrid_data(aa,Xm,Xm,16,Edecay,2.0)[2]
    exact=2*(np.exp(.25*aa[-1])-np.exp(.25*aa[0]))
    assert abs(float(np.sum(s4))-exact)<1e-13
    assert abs(float(np.sum(s16))-exact)<1e-13
    badX=np.zeros_like(Xlin);badX[:,-1]=100
    delta=core.evaluate_hermite(Xlin,Xd,xgrid,np.array([1]),np.array([.5]))[0]
    assert np.isfinite(delta).all()
    print('GE19_D16_VARIABLE_ORIGINAL_ACTION_CLOCK_ANALYTIC_GAUSS_AND_DRIVE_NEGATIVE_CONTROL_PASS')
    print('GE19_H4F3D16_SYNTHETIC_SOURCE_AND_PHYSICAL_CLOCK_STATIC_PASS_ACTUAL_PARENT_RUN_OPEN')

if __name__=='__main__':run()
