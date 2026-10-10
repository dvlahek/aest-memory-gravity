#!/usr/bin/env python3
"""D17 independent source-action dense H1 numerical reconstruction (NOT certification).

Uses the original frozen GE06/GE07 canonical operator with an explicit,
source-identical original action H,Q,Z background override. The frozen
PCHIP off-knot implementation is independently compared and never changed.
The 2-stage Radau IIA step uses original Repair07 coefficients and solver.
All sampled defects and mesh differences are empirical, NOT error bounds.
"""
from __future__ import annotations
import math
import numpy as np

C1=1.0/3.0
A11,A12,A21,A22=5./12.,-1./12.,3./4.,1./4.
B1,B2=3./4.,1./4.
TINY=1e-300

def rel(a,b):
    aa=np.asarray(a);bb=np.asarray(b)
    return float(np.linalg.norm(aa-bb)/max(np.linalg.norm(aa),np.linalg.norm(bb),TINY))

def aor(a,b):
    aa=np.asarray(a);bb=np.asarray(b)
    ae=np.abs(aa-bb)
    return float(np.max(np.minimum(ae,ae/np.maximum(np.maximum(np.abs(aa),np.abs(bb)),TINY))))

def action_Qx_from_Z(Z,Z0):
    """For original K_Q=4*K2*Z0*Z*exp(Z**2) and Q=Q0+Z0*Z."""
    zz=np.asarray(Z,float)
    return -3.*float(Z0)*zz/(1.+2.*zz**2)

def radau2_step(y,xa,xb,M_at,solve):
    """Exact original two-stage Radau IIA algebra, zero H1 sources."""
    y=np.asarray(y,complex)
    if y.shape!=(8,) or not (xb>xa) or not np.isfinite(y).all():
        raise ValueError('D17 canonical step input invalid')
    h=float(xb-xa)
    M1=np.asarray(M_at(xa+C1*h),complex)
    M2=np.asarray(M_at(xb),complex)
    I=np.eye(8,dtype=complex)
    K=np.block([[I-h*A11*M1,-h*A12*M2],[-h*A21*M1,I-h*A22*M2]])
    Y,diag=solve(K,np.r_[y,y])
    Y=np.asarray(Y,complex)
    if Y.shape!=(16,) or not np.isfinite(Y).all():
        raise RuntimeError('D17 nonfinite Radau stage')
    yn=y+h*(B1*(M1@Y[:8])+B2*(M2@Y[8:]))
    if not np.isfinite(yn).all():
        raise RuntimeError('D17 nonfinite canonical state')
    return yn,diag

def integrate_original_grid(x,y0,nsub,M_at,solve):
    """Retains all original knots and all interior substep nodes."""
    xx=np.asarray(x,float)
    if xx.ndim!=1 or len(xx)<3 or not np.all(np.diff(xx)>0) or nsub not in (1,2,4):
        raise ValueError('D17 original-grid integration domain invalid')
    fine=np.empty((len(xx)-1)*nsub+1,float)
    state=np.empty((8,len(fine)),complex)
    fine[0]=xx[0];state[:,0]=y0
    diagnostics=[];index=0
    for j in range(len(xx)-1):
        x0=float(xx[j]);delta=float(xx[j+1]-xx[j])
        for sub in range(nsub):
            xa=float(x0+delta*sub/nsub)
            xb=float(xx[j+1]) if sub==nsub-1 else float(x0+delta*(sub+1)/nsub)
            yn,d=radau2_step(state[:,index],xa,xb,M_at,solve)
            index+=1;fine[index]=xb;state[:,index]=yn
            diagnostics.append(float(d.get('scaled_relative_L2_residual_max',np.nan)))
    if not np.array_equal(fine[::nsub],xx):
        raise RuntimeError('D17 exact original canonical parent knots lost')
    if not(np.isfinite(state).all() and np.isfinite(diagnostics).all()):
        raise RuntimeError('D17 nonfinite original canonical integrated state')
    return fine,state,float(max(diagnostics,default=0.))

def sampled_hermite_ode_defect(xfine,yfine,M_at):
    """One midpoint per fine substep; sampled residual is NOT an enclosure."""
    xx=np.asarray(xfine,float);Y=np.asarray(yfine,complex)
    if Y.shape!=(8,len(xx)) or not np.all(np.diff(xx)>0):
        raise ValueError('D17 dense H1 residual array invalid')
    absmax=0.;relmax=0.;integrated=0.
    for j in range(len(xx)-1):
        xa=float(xx[j]);xb=float(xx[j+1]);h=xb-xa
        ya=Y[:,j];yb=Y[:,j+1]
        dy0=M_at(xa)@ya;dy1=M_at(xb)@yb
        ym=.5*(ya+yb)+h/8.*(dy0-dy1)
        dym=1.5/h*(yb-ya)-.25*(dy0+dy1)
        mm=M_at(.5*(xa+xb))@ym
        defect=dym-mm
        val=float(np.linalg.norm(defect))
        absmax=max(absmax,val)
        relmax=max(relmax,val/max(float(np.linalg.norm(dym)),float(np.linalg.norm(mm)),TINY))
        integrated+=h*val
    return {'midpoint_canonical_ODE_defect_absolute_L2_max_sampled_not_bound':absmax,
            'midpoint_canonical_ODE_defect_relative_L2_max_sampled_not_bound':relmax,
            'midpoint_abs_defect_rectangle_integral_diagnostic_not_bound':float(integrated)}

class ActionBackground:
    """Independent original GE15/Repair13 charge/Exp and Lambda extension.

    Caller supplies the source-bound original continuous H function from D15a.
    All off-knot Q,Z values derive from scalar charge, not PCHIP.
    """
    def __init__(self,r7,bg,evalH):
        self.r7=r7;self.bg=bg;self.evalH=evalH
        xx=np.asarray(bg['x'],float);aa=np.asarray(bg['a'],float)
        kq=np.asarray(bg['KQ_action'],float)
        self.i0=float(np.median(aa**3*kq))
        self.x0,self.x1=float(xx[0]),float(xx[-1])
        self.cache={}
        self.max_frozen_pchip_relative={q:0. for q in ('H','Q_action','Z_action')}
    def __call__(self,bg,xq):
        xx=float(xq)
        if id(bg)!=id(self.bg) or not (self.x0-1e-13<=xx<=self.x1+1e-13):
            raise RuntimeError('D17 original action background identity/domain changed')
        key=round(xx,15)
        if key not in self.cache:
            aa=math.exp(xx);kq=self.i0*math.exp(-3.*xx)
            Z=float(self.r7.exp_Z_from_KQ(np.asarray([kq],float))[0])
            Q=float(self.r7.Q0+self.r7.Z0*Z)
            H=float(np.asarray(self.evalH(np.asarray([xx],float))[0],float)[0])
            if not(np.isfinite([H,Q,Z,kq]).all() and H>0 and Z>0 and kq>0):
                raise RuntimeError('D17 nonphysical original positive Exp action background')
            self.cache[key]={'x':xx,'a':aa,'H':H,'Q_action':Q,'Z_action':Z}
        return self.cache[key]
    def knot_check(self):
        bg=self.bg
        for i,xq in enumerate(np.asarray(bg['x'],float)):
            point=self(bg,float(xq))
            for key,reference in (('H',bg['H'][i]),('Q_action',bg['Q_action'][i]),('Z_action',bg['Z_action'][i])):
                if abs(point[key]-float(reference))>1e-10*max(abs(point[key]),abs(float(reference)),1e-30):
                    raise RuntimeError('D17 original action knot differs from frozen Repair13: '+key)
