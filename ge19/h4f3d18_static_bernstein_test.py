#!/usr/bin/env python3
"""Synthetic tests of exact polynomial algebra, convexity and negative controls."""
import numpy as np
from ge19 import h4f3d18_bernstein_affine_canonical_H1_core as c

def check():
    rng=np.random.default_rng(187001)
    h=.071
    for _ in range(16):
        y0=rng.normal(size=8)+1j*rng.normal(size=8)
        y1=rng.normal(size=8)+1j*rng.normal(size=8)
        M0=(rng.normal(size=(8,8))+1j*rng.normal(size=(8,8)))*.15
        M1=(rng.normal(size=(8,8))+1j*rng.normal(size=(8,8)))*.15
        v=c.bernstein_ideal_float(1.,1.+h,y0,y1,M0,M1)
        d0=M0@y0;d1=M1@y1
        p0=y0;p1=h*d0;p2=3*(y1-y0)-h*(2*d0+d1)
        p3=2*(y0-y1)+h*(d0+d1)
        for t in np.linspace(0,1,257):
            yy=p0+t*p1+t*t*p2+t**3*p3
            dyy=(p1+2*t*p2+3*t*t*p3)/h
            mm=M0+t*(M1-M0)
            residual=dyy-mm@yy
            from_power=c.exact_polynomial_residual_at(v,y0,M0,M1,t)
            assert np.linalg.norm(residual-from_power)<5.e-12
            assert np.linalg.norm(residual)<=v['residual_poly_sup_ideal_float']+4.e-12
            assert np.linalg.norm(yy)<=v['y_poly_sup_ideal_float']+4.e-12
        assert np.linalg.norm(v['r_bernstein'][0])<1.e-12
        assert np.linalg.norm(v['r_bernstein'][-1])<1.e-12
        assert c.conditional_step(0.,v) is None
        # Negative control: fabricated zero curvature must never be authorized
        # as a source-action certificate; only a *scenario* can be computed.
        ideal=c.conditional_step(0.,v,0.)
        assert ideal is not None and ideal>=0
        assert c.optional_action_remainder(2.,h)==h*h/4.
    assert abs(c.gronwall_step(.3,.2,0.,.4)-.38)<1.e-15
    assert abs(c.gronwall_log_step(-np.inf,.2,0.,.4)-np.log(.08))<1.e-13
    assert abs(c.log10_1plus_error(1100.) - 1100./np.log(10.))<1.e-12
    # Negative control: midpoint action curvature invisible at endpoints.
    # Affine residual is identically zero, yet a non-affine physical operator
    # produces a strictly nonzero genuine residual inside the same interval.
    y=np.ones(8,complex);zero=np.zeros((8,8),complex)
    flat=c.bernstein_ideal_float(0.,.1,y,y,zero,zero)
    assert flat['residual_poly_sup_ideal_float']==0.
    Mtrue_mid=.02*np.eye(8,dtype=complex)
    assert np.linalg.norm(Mtrue_mid@y)>0.
    assert c.conditional_step(0.,flat) is None
    for bad in (-1.,float('nan')):
        try:c.optional_action_remainder(bad,h)
        except ValueError:pass
        else:raise AssertionError('D18 invalid curvature negative control failed')
    print('GE19_D18_EXACT_DEGREE4_BERNSTEIN_AND_HERMITE_ENDPOINT_CONVEXITY_PASS')
    print('GE19_D18_UNKNOWN_ACTION_CURVATURE_CANNOT_CERTIFY_NEGATIVE_CONTROL_PASS')
if __name__=='__main__':check()
