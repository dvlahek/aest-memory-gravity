#!/usr/bin/env python3
"""Exact original GE05 c2[pt] current and physical-time chain-rule derivative.

For original L=NLR^2/4 [A_q^2-(omega*q-sqrt(w)*Xphi)^2],
with first-order normalized q=sqrt(w)/omega*z and longitudinal
X=Q*u+phi_x/a, the epsilon^2 coefficient (second derivative) of
partial L/partial phi_t is a^3*w*u*(z-X). No time finite difference
of the high-phase bath is used here. Derivatives are conditional on
z_t=v/tau and supplied first-order u_t and X_t (from action D17).
"""
from __future__ import annotations
import numpy as np

TINY=1.e-300

def rel(a,b):
    a=np.asarray(a);b=np.asarray(b)
    return float(np.linalg.norm(a-b)/max(np.linalg.norm(a),np.linalg.norm(b),TINY))

def current(a,u,z,X,w):
    """a[nt], u/X[nt,nx], z[node,nt,nx], w[node]."""
    a=np.asarray(a,float);u=np.asarray(u,float);z=np.asarray(z,float)
    X=np.asarray(X,float);w=np.asarray(w,float)
    if (a.ndim!=1 or u.ndim!=2 or X.shape!=u.shape or
        z.ndim!=3 or z.shape[1:]!=u.shape or a.shape!=(u.shape[0],) or
        w.shape!=(z.shape[0],) or np.any(a<=0) or np.any(w<=0) or
        not all(np.isfinite(v).all() for v in (a,u,z,X,w))):
        raise ValueError('D21 invalid GE05 c2[pt] current inputs')
    return a[None,:,None]**3*w[:,None,None]*u[None]*(z-X[None])

def current_dot(a,H,u,ut,z,zt,X,Xt,w):
    """Exact d/dt of c2[pt] given continuum first-order ODE jets."""
    a=np.asarray(a,float);H=np.asarray(H,float);u=np.asarray(u,float)
    ut=np.asarray(ut,float);z=np.asarray(z,float);zt=np.asarray(zt,float)
    X=np.asarray(X,float);Xt=np.asarray(Xt,float);w=np.asarray(w,float)
    if (H.shape!=a.shape or ut.shape!=u.shape or Xt.shape!=X.shape or
        zt.shape!=z.shape or np.any(H<=0) or
        not all(np.isfinite(v).all() for v in (H,ut,zt,Xt))):
        raise ValueError('D21 invalid action physical-time derivative inputs')
    _=current(a,u,z,X,w)  # exact shape/physical-domain validation
    return (a[None,:,None]**3*w[:,None,None]*
         (((3*H[:,None]*u+ut)[None])*(z-X[None])+
           u[None]*(zt-Xt[None])))

def fd4_uniform(y,x,H):
    """Diagnostic only: reproduce original FD4 time current at original knots."""
    x=np.asarray(x,float); H=np.asarray(H,float);y=np.asarray(y,float)
    if (x.ndim!=1 or y.shape[-2]!=len(x) or H.shape!=x.shape or len(x)<9 or
        not np.allclose(np.diff(x),x[1]-x[0],rtol=1e-9,atol=1e-13)):
        raise ValueError('D21 FD4 grid shape mismatch')
    h=float(x[1]-x[0]);r=np.empty_like(y)
    r[...,2:-2,:]=(y[...,:-4,:]-8*y[...,1:-3,:]+8*y[...,3:-1,:]-y[...,4:,:])/(12*h)
    r[...,0,:]=(-25*y[...,0,:]+48*y[...,1,:]-36*y[...,2,:]+16*y[...,3,:]-3*y[...,4,:])/(12*h)
    r[...,1,:]=(-3*y[...,0,:]-10*y[...,1,:]+18*y[...,2,:]-6*y[...,3,:]+y[...,4,:])/(12*h)
    r[...,-2,:]=(3*y[...,-1,:]+10*y[...,-2,:]-18*y[...,-3,:]+6*y[...,-4,:]-y[...,-5,:])/(12*h)
    r[...,-1,:]=(25*y[...,-1,:]-48*y[...,-2,:]+36*y[...,-3,:]-16*y[...,-4,:]+3*y[...,-5,:])/(12*h)
    return r*H[None,:,None]


def mapped_M2_scalar_delta(old_pt_dot,new_pt_dot,mapping_factor=2.):
    """Source rows are -2 * raw Euler; raw scalar=-dt pt-dx px."""
    if mapping_factor!=2.:
        raise ValueError('D21 original GE05->GE06 mapping factor must be +2')
    return 2.*(np.asarray(new_pt_dot)-np.asarray(old_pt_dot))
