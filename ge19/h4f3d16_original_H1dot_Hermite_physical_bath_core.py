#!/usr/bin/env python3
"""D16: exact frozen H1 endpoint jets -> conditional Hermite X10 and physical-clock bath.

Only H1 and H1dot endpoints are original certified parents. Cubic Hermite
is an independently tracked continuous surrogate, not the exact H1 solution.
The convergent bath propagator uses exact frozen Repair24 step_linear_nd with
substep *physical* time increments integrated from original Repair13 H(x).
State v=dz/d(t/tau) is carried continuously across every substep. Neither
an all-interval numerical error enclosure nor a true-X10 error is inferred.
"""
from __future__ import annotations
import numpy as np

MODES=np.array([3,5,8,10,15,20],int)
TINY=1e-300

def l2(a):
    return float(np.linalg.norm(np.asarray(a)))

def rel(a,b):
    return l2(np.asarray(a)-np.asarray(b))/max(l2(a),l2(b),TINY)

def frozen_endpoint_X_Xx(r7,bg,h1,h1dot):
    """Action-exact X_x at each frozen H3F on-shell H1 knot.

    X=Q*u+(ik/a)*phi. H1dot stores [Sdot,udot,phidot,Tdot]
    as cosmic-time derivatives. Scalar charge gives Q_x=-3*KQ/KQQ.
    """
    st=np.asarray(h1,complex); dt=np.asarray(h1dot,complex)
    x=np.asarray(bg['x'],float); a=np.asarray(bg['a'],float)
    H=np.asarray(bg['H'],float);Q=np.asarray(bg['Q_action'],float)
    KQ=np.asarray(bg['KQ_action'],float);KQQ=np.asarray(bg['KQQ_action'],float)
    if (st.shape!=(6,6,len(x)) or dt.shape!=(6,4,len(x)) or
        any(q.shape!=x.shape for q in (a,H,Q,KQ,KQQ)) or
        any(not np.isfinite(q).all() for q in (st,dt,x,a,H,Q,KQ,KQQ)) or
        np.any(a<=0) or np.any(H<=0) or np.any(KQQ<=0) or np.any(KQ<=0)):
        raise ValueError('D16 original H1/H1dot physical endpoint shape/source invalid')
    kfund=float(r7.g9.K_REQ[0]/r7.FOURIER_N[0])
    if not np.array_equal(np.asarray(r7.FOURIER_N,int),MODES):
        raise RuntimeError('D16 frozen six positive modes changed')
    ik=(1j*kfund*MODES[:,None])/a[None,:]
    X=Q[None,:]*st[:,2,:]+ik*st[:,3,:]
    Qx=-3.0*KQ/KQQ
    Xx=Qx[None,:]*st[:,2,:]+Q[None,:]*dt[:,1,:]/H[None,:]+ik*(dt[:,2,:]/H[None,:]-st[:,3,:])
    if any(not np.isfinite(z).all() for z in (X,Xx)):
        raise RuntimeError('D16 nonfinite original H1 X/Xx endpoint jets')
    return X,Xx

def evaluate_hermite(X,Xx,x,interval,theta):
    """Vectorized cubic Hermite at original intervals; interval, theta broadcast."""
    y=np.asarray(X,complex); dy=np.asarray(Xx,complex)
    xx=np.asarray(x,float);i=np.asarray(interval,int); t=np.asarray(theta,float)
    if (y.shape!=dy.shape or y.ndim!=2 or y.shape[1]!=len(xx) or
        not np.all(np.diff(xx)>0) or np.any(i<0) or np.any(i>=len(xx)-1) or
        np.any(t<0) or np.any(t>1) or not np.isfinite(t).all()):
        raise ValueError('D16 Hermite interpolation domain invalid')
    i,t=np.broadcast_arrays(i,t)
    h=(xx[i+1]-xx[i])[None,...]
    tt=t[None,...]
    H00=2*tt**3-3*tt**2+1
    H10=tt**3-2*tt**2+tt
    H01=-2*tt**3+3*tt**2
    H11=tt**3-tt**2
    yy=(H00*y[:,i]+H10*h*dy[:,i]+H01*y[:,i+1]+H11*h*dy[:,i+1])
    dydx=((6*tt**2-6*tt)/h*y[:,i]+(3*tt**2-4*tt+1)*dy[:,i]
           +(-6*tt**2+6*tt)/h*y[:,i+1]+(3*tt**2-2*tt)*dy[:,i+1])
    return yy,dydx

def subgrid_data(x,X,Xx,nsub,action_H,tau,legendre_n=16,drive='hermite'):
    """Gauss quadrature of original action physical dt/tau across each substep.

    h_eff = delta_x / integral dx/(tau H(x)); this is not an extra
    model parameter and its *endpoints* use the same physical clock.
    """
    xx=np.asarray(x,float);N=len(xx)-1
    if nsub<1 or legendre_n not in (8,16) or drive not in ('hermite','linear'):
        raise ValueError('D16 subgrid prereg scope changed')
    frac=np.arange(nsub,dtype=float)/nsub
    xsub=(xx[:-1,None]+np.diff(xx)[:,None]*frac[None,:]).reshape(-1)
    xsub=np.r_[xsub,xx[-1]]
    it=np.repeat(np.arange(N),nsub)
    theta=np.tile(frac,N)
    if drive=='hermite':
        xd,_=evaluate_hermite(X,Xx,xx,it,theta)
    else:
        xd=X[:,it]+theta[None,:]*(X[:,it+1]-X[:,it])
    xd=np.column_stack((xd,X[:,-1]))
    xm=(xsub[:-1]+xsub[1:])/2
    hd=np.diff(xsub)
    qnodes,qw=np.polynomial.legendre.leggauss(legendre_n)
    evalx=xm[:,None]+hd[:,None]*qnodes[None,:]/2
    H,_=action_H(evalx)
    if H.shape!=evalx.shape or not np.all(np.isfinite(H)) or np.any(H<=0):
        raise RuntimeError('D16 original action H invalid at Gauss nodes')
    ds=.5*hd*np.sum(qw[None,:]/(tau*H),axis=1)
    heff=hd/ds
    if not(np.all(np.isfinite(ds)) and np.all(ds>0) and np.all(heff>0)):
        raise RuntimeError('D16 nonphysical original action substep clock')
    return xsub,xd,ds,heff

def propagate_physical(x,X,Xx,bg_eval,z0,v0,r,tau,step,nsub,drive='hermite'):
    """Frozen original step propagator, integrated on true physical substep time.

    All node/r values are retained. Finite nsub remains a numerical
    approximation, including substep H and drive interpolation defects.
    """
    xx=np.asarray(x,float); rr=np.asarray(r,float)
    q=np.asarray(z0,complex).copy();v=np.asarray(v0,complex).copy()
    if q.shape!=v.shape or q.shape!=(rr.size,6) or not np.isfinite(q).all() or not np.isfinite(v).all():
        raise ValueError('D16 original R1 bath boundary invalid')
    xsub,xd,ds,heff=subgrid_data(xx,X,Xx,nsub,bg_eval,tau,16,drive)
    outq=np.empty((rr.size,6,len(xx)),complex)
    outv=np.empty_like(outq)
    outq[:,:,0]=q;outv[:,:,0]=v
    for j in range(len(ds)):
        q,v=step(q,v,rr,float(heff[j]),xd[:,j],xd[:,j+1],float(ds[j]))
        if (j+1)%nsub==0:
            k=(j+1)//nsub
            outq[:,:,k]=q;outv[:,:,k]=v
    if not np.isfinite(outq).all() or not np.isfinite(outv).all():
        raise RuntimeError('D16 nonfinite physical-clock bath propagation')
    # Return only the last/first substep clock data needed for one-sided
    # physical-action GE05 source at the ORIGINAL H3F time knots.
    return outq,outv,heff[nsub-1::nsub],heff[::nsub]

def signed_one_sided_endpoint_W(z,v,a,H,h_eff,r,w,tau,kfund,convolve,envelope,side):
    """One-sided smooth E_q source of finite-nsub physical-time approximation.

    Its actual original GE05 residual at a knot has the frozen-H difference;
    Xlin_sub equals Hermite X at each exact original knot. No impulse at the
    knot because the propagated physical-time v is carried continuously.
    """
    zz=np.asarray(z,complex);vv=np.asarray(v,complex)
    aa=np.asarray(a,float);HH=np.asarray(H,float);hh=np.asarray(h_eff,float)
    rr=np.asarray(r,float);ww=np.asarray(w,float)
    if side=='left':
        zz=zz[:,:,1:];vv=vv[:,:,1:];aa=aa[1:];HH=HH[1:]
    elif side=='right':
        zz=zz[:,:,:-1];vv=vv[:,:,:-1];aa=aa[:-1];HH=HH[:-1]
    else:
        raise ValueError('D16 one-sided clock source side invalid')
    if hh.shape!=aa.shape or zz.shape[-1]!=len(hh):
        raise ValueError('D16 one-sided clock source shape invalid')
    omega=rr[:,None,None]/tau;sqrtw=np.sqrt(ww)[:,None,None]
    R=3.0*aa[None,None,:]**3/tau*(HH-hh/tau)[None,None,:]*vv
    Eq=-sqrtw/(2.0*omega)*R
    qx=(sqrtw/omega)*(1j*kfund*MODES[None,:,None])*zz
    W=convolve(Eq,qx)
    U=envelope(Eq,qx)
    if np.any(np.abs(W)>U*(1+1e-10)+1e-25):
        raise RuntimeError('D16 signed endpoint bath envelope violated')
    return W,U
