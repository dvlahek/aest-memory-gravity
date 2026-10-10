#!/usr/bin/env python3
"""Offline original-action algebra, manufactured time-jet and alias negative controls."""
from __future__ import annotations
import numpy as np, sympy as sp
from ge19 import h4f3d21_GE05_phase_safe_M2_core as core

N,L,R,b,r=sp.symbols('N L R b r',real=True)
pt,px,qt,qx,q=sp.symbols('pt px qt qx q',real=True)
om,sw=sp.symbols('om sw',positive=True,real=True)
Aq=sp.cosh(r)/N*(qt-b*qx)+sp.sinh(r)/L*qx
Xp=sp.sinh(r)/N*(pt-b*px)+sp.cosh(r)/L*px
lag=N*L*R**2*sp.Rational(1,4)*(Aq**2-(om*q-sw*Xp)**2)
eps=sp.symbols('eps',real=True)
a,Q,dN,dL,dR,db,dr,dpt,dpx,dqt,dqx,dq=sp.symbols('a Q dN dL dR db dr dpt dpx dqt dqx dq',real=True)
sub={N:1+eps*dN,L:a+eps*dL,R:a+eps*dR,b:eps*db,r:eps*dr,
     pt:Q+eps*dpt,px:eps*dpx,qt:eps*dqt,qx:eps*dqx,q:eps*dq}
pt2=sp.simplify(sp.diff(sp.diff(lag,pt).subs(sub),eps,2).subs(eps,0))
z=sp.symbols('z',real=True)
want=a**3*sw**2*dr*(z-Q*dr-dpx/a)
assert sp.simplify(pt2.subs(dq,sw/om*z)-want)==0
assert sp.simplify(sp.diff(pt2,dqt))==0 and sp.simplify(sp.diff(pt2,dpt))==0
print('GE19_D21_ORIGINAL_GE05_C2_PT_SYMBOLIC_EXACT_IDENTITY_PASS',flush=True)

rng=np.random.default_rng(30)
t=np.linspace(.03,.17,12);weight=np.array([.17,.43]);H=.21;aa=np.exp(H*t)
omegas=np.array([1.2,380.])[:,None,None];T=t[None,:,None]
u=np.sin(2.3*t)[:,None]*np.ones((1,3))
ut=2.3*np.cos(2.3*t)[:,None]*np.ones((1,3))
X=.12*np.sin(1.3*t)[:,None]*np.ones((1,3));Xt=.156*np.cos(1.3*t)[:,None]*np.ones((1,3))
zstate=np.cos(omegas*T)*np.ones((1,1,3));zt=-omegas*np.sin(omegas*T)*np.ones((1,1,3))
calc=core.current_dot(aa,np.full_like(t,H),u,ut,zstate,zt,X,Xt,weight)
def f(tt):
 A=np.exp(H*tt);U=np.sin(2.3*tt);XX=.12*np.sin(1.3*tt)
 Z=np.cos(omegas*tt[None,:,None])*np.ones((1,1,3))
 return A[None,:,None]**3*weight[:,None,None]*U[None,:,None]*(Z-XX[None,:,None])
h=1.e-7
fd=(f(t+h)-f(t-h))/(2*h)
assert core.rel(calc,fd)<8e-10,core.rel(calc,fd)
wrong=core.current_dot(aa,np.full_like(t,H),u,ut,zstate,zt,X,np.zeros_like(Xt),weight)
assert core.rel(calc,wrong)>1.e-5
assert core.rel(core.mapped_M2_scalar_delta(np.ones((2,3)),np.ones((2,3))*3),
                np.ones((2,3))*4)<1e-15
print('GE19_D21_MANUFACTURED_FAST_PHASE_CURRENT_CHAIN_RULE_AND_NEGATIVE_CONTROL_PASS',flush=True)

x=np.linspace(0,1,129);high=np.sin(900.*x)[None,:,None]
fd4=core.fd4_uniform(high,x,np.ones_like(x))[0,:,0]
truth=900*np.cos(900*x)
assert np.linalg.norm(fd4-truth)/np.linalg.norm(truth)>.1
print('GE19_D21_ORIGINAL_KNOT_FD4_HIGH_PHASE_ALIAS_NEGATIVE_CONTROL_PASS',flush=True)
