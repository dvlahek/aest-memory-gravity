#!/usr/bin/env python3
"""D18: analytic polynomial-surrogate H1 residual envelope, NOT action-H1 certification.

Given the original-action canonical M at both ends of each D17 fine interval,
interpolate M linearly, use an ODE-slope Hermite cubic for the saved D17 state,
and enclose the resulting QUARTIC residual by its five Bernstein control norms.
This is an algebraic convex-hull result in exact arithmetic on its inputs;
float64 arithmetic is NOT outward-rounded, and the unknown off-grid action
operator remainder is deliberately never set to zero in the physical claim.
"""
from __future__ import annotations
import math
import numpy as np

TINY=1.e-300

def norm(v):
    return float(np.linalg.norm(np.asarray(v,complex)))

def bernstein_ideal_float(x0,x1,y0,y1,m0,m1):
    """Return numerical Bernstein controls for y_h and y_h'-M_lin*y_h.

    For exact coefficients, the maxima of control-vector 2-norms bound the
    supremum on every t in [0,1], not just at sampled locations.
    """
    h=float(x1-x0)
    a=np.asarray(y0,complex);b=np.asarray(y1,complex)
    A=np.asarray(m0,complex);B=np.asarray(m1,complex)
    if not (h>0 and a.shape==(8,) and b.shape==(8,)
            and A.shape==(8,8) and B.shape==(8,8)):
        raise ValueError('D18 canonical Bernstein interval shape/domain changed')
    if not all(np.isfinite(z).all() for z in (a,b,A,B)):
        raise ValueError('D18 nonfinite canonical Bernstein inputs')
    d0=A@a; d1=B@b
    # y_h(t) = p0 + p1*t + p2*t**2 + p3*t**3, t=(x-x0)/h.
    p0=a;p1=h*d0;p2=3*(b-a)-h*(2*d0+d1)
    p3=2*(a-b)+h*(d0+d1)
    dy=B-A
    # r(t) = (1/h) dy_h/dt - (A+t*(B-A))*y_h, degree at most 4.
    powers=np.stack((p1/h-A@p0,
                     2*p2/h-A@p1-dy@p0,
                     3*p3/h-A@p2-dy@p1,
                     -A@p3-dy@p2,
                     -dy@p3),axis=0)
    controls=[]
    for j in range(5):
        controls.append(sum((math.comb(j,k)/math.comb(4,k))*powers[k]
                            for k in range(j+1)))
    rb=np.stack(controls)
    # Degree-3 Bernstein coefficients for y_h.
    yb=np.stack((p0,p0+p1/3.,p0+2.*p1/3.+p2/3.,p0+p1+p2+p3))
    rmax=max(map(norm,rb));ymax=max(map(norm,yb))
    lmax=max(float(np.linalg.norm(A,ord='fro')),
             float(np.linalg.norm(B,ord='fro')))
    if not np.isfinite([rmax,ymax,lmax]).all():
        raise RuntimeError('D18 nonfinite Bernstein envelope')
    return dict(h=h,r_bernstein=rb,y_bernstein=yb,
                residual_poly_sup_ideal_float=rmax,
                y_poly_sup_ideal_float=ymax,
                operator_affine_fro_sup_ideal_float=lmax,
                power=powers)

def exact_polynomial_residual_at(out,y0,m0,m1,t):
    """Independent explicit polynomial evaluation for tests only."""
    t=float(t);p=out['power'];h=out['h'];m0=np.asarray(m0,complex);m1=np.asarray(m1,complex)
    # Return quartic residual directly from its power coefficients.
    return sum(p[k]*t**k for k in range(5))

def gronwall_step(e0,h,l,r):
    """Conditional comparison solution for E'<=L E + R, exact-input ideal."""
    e0,h,l,r=map(float,(e0,h,l,r))
    if not all(math.isfinite(x) and x>=0 for x in (e0,h,l,r)):
        raise ValueError('D18 comparison negative/nonfinite input')
    z=h*l
    if z>700:raise RuntimeError('D18 comparison overflow: no admissible bound')
    amp=math.exp(z)
    integ=(math.expm1(z)/l) if l else h
    e1=amp*e0+integ*r
    if not math.isfinite(e1):raise RuntimeError('D18 nonfinite comparison')
    return e1

def gronwall_log_step(log_e0,h,l,r):
    """Return log(E) for the nonnegative comparison without overflow.

    log_e0=-inf denotes E0=0. A computed log-envelope is ONLY an affine
    operator scenario until independently validated M_action-M_affine bounds.
    """
    h,l,r=map(float,(h,l,r))
    if not all(math.isfinite(v) and v>=0 for v in (h,l,r)):
        raise ValueError('D18 log comparison nonnegative finite inputs required')
    if not (math.isfinite(log_e0) or log_e0==-math.inf):
        raise ValueError('D18 log comparison invalid starting log')
    z=h*l
    log_phi=(math.log(math.expm1(z))-math.log(l)) if l and z<700 and z>0 else (
             (z+math.log1p(-math.exp(-z))-math.log(l)) if l and z>=700 else
             math.log(h) if h else -math.inf)
    term_a=log_e0+z
    term_b=(math.log(r)+log_phi) if r else -math.inf
    result=float(np.logaddexp(term_a,term_b))
    if not (math.isfinite(result) or result==-math.inf):
        raise RuntimeError('D18 log comparison invalid result')
    return result

def log10_1plus_error(log_e):
    """Finite log10(1+E), even when E itself overflows binary64."""
    if log_e==-math.inf:return 0.
    v=float(np.logaddexp(0.,log_e)/math.log(10.))
    if not math.isfinite(v):raise RuntimeError('D18 log10 scenario failed')
    return v

def optional_action_remainder(B2,h):
    """Rigorous mathematical formula ONLY if B2 bounds sup ||M_action''||.

    A midpoint or mesh difference is not an admissible B2.
    """
    if B2 is None:return None
    v=float(B2)
    if not math.isfinite(v) or v<0:raise ValueError('D18 invalid certified action curvature')
    return h*h*v/8.

def conditional_step(e0,poly,B2=None):
    eps=optional_action_remainder(B2,poly['h'])
    if eps is None:return None
    L=poly['operator_affine_fro_sup_ideal_float']+eps
    R=(poly['residual_poly_sup_ideal_float']+
       eps*poly['y_poly_sup_ideal_float'])
    return gronwall_step(e0,poly['h'],L,R)
