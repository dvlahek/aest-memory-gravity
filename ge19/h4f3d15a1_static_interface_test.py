#!/usr/bin/env python3
"""D15a1 ORIGINAL GE05 x-embedded R1 internal current jump static tests."""
from __future__ import annotations
import numpy as np
import sympy as sp
from ge19 import h4f3d15a1_original_GE05_interface_current_jump as interface
from ge19.h4f3d15a_static_clock_source_test import independent_signed_convolve


def symbolic_interface():
    a,v,tau,minus,plus=sp.symbols('a v tau gamma_minus gamma_plus',nonzero=True,real=True)
    Jminus=a**3*minus*v/tau
    Jplus=a**3*plus*v/tau
    jump=a**3*v/tau*(plus-minus)
    assert sp.simplify(Jplus-Jminus-jump)==0
    assert sp.simplify(Jminus-Jplus-jump)!=0
    assert sp.simplify(jump.subs(plus,minus))==0
    return 'GE19_D15A1_ORIGINAL_GE05_DISTRIBUTIONAL_INTERFACE_JUMP_SYMPY_PASS'


def signed_original_interface():
    nq,nt=9,13
    r=np.linspace(.11,2.,nq);w=np.ones(nq)/nq
    m=np.array([3,5,8,10,15,20]);idx=np.arange(nt)
    z=(.8+.01*r[:,None,None]+.002*m[None,:,None])*np.exp(1j*(
        .3*r[:,None,None]+.12*m[None,:,None]+.04*idx[None,None,:]))
    v=.3*z
    x=np.linspace(-.8,0,nt);a=np.exp(x);H=np.linspace(.5,.55,nt)
    tau=.6;hm=np.sqrt(H[:-1]*H[1:])*tau
    out=interface.original_GE05_interior_current_jump(
        z,v,a,H,hm,r,w,tau,.12,independent_signed_convolve)
    signed=out['interior_original_GE05_Eq_impulse_signed_W_coeff']
    upper=out['interior_original_GE05_Eq_impulse_unsigned_W_coeff_envelope']
    assert signed.shape==(nt-2,41) and upper.shape==signed.shape
    assert np.linalg.norm(signed)>1e-16
    assert np.all(np.abs(signed)<=upper*(1+1e-11)+1e-25)
    assert out['interior_interface_coeff_multiplies_delta_t_not_smooth_W'] is True
    constant=interface.original_GE05_interior_current_jump(
        z,v,a,np.full(nt,.52),np.full(nt-1,tau*.52),
        r,w,tau,.12,independent_signed_convolve)
    assert np.array_equal(constant['interior_original_GE05_Eq_impulse_signed_W_coeff'],
                          np.zeros((nt-2,41),complex))
    assert np.all(constant['interior_gamma_plus_minus_jump']==0)
    return 'GE19_D15A1_SIGNED_INTERFACE_AND_CONSERVATIVE_ENVELOPE_PASS_CONSTANT_H_NEGATIVE_CONTROL_PASS'

if __name__=='__main__':
    print(symbolic_interface())
    print(signed_original_interface())
    print('GE19_H4F3D15A1_INTERFACE_STATIC_PASS_ACTUAL_R1_PHYSICAL_OPEN')
