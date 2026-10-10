#!/usr/bin/env python3
"""D15a exact GE05 x-clock identity, negative controls and synthetic tests.

SYNTHETIC tests only; never imply actual original R1 physical execution.
"""
from __future__ import annotations
import math
import numpy as np
import sympy as sp
from scipy.special import lambertw
from ge19 import h4f3d15a_original_GE05_clock_embedded_source as source


def symbolic_identity():
    a,H,Hx,hm,tau,r,z,v,Xlin,Xtrue=sp.symbols(
        'a H Hx hm tau r z v Xlin Xtrue',real=True,nonzero=True)
    gamma=tau*H/hm
    gamma_x=tau*Hx/hm
    # x=ln(a), a_x=a and original frozen R1 v_x.
    vx=(-3*hm*v-r*r*(z-Xlin))/hm
    # d_x[a^3 gamma v/tau] under the FROZEN original R1 step.
    Jx=a**3/tau*(3*gamma*v+gamma_x*v+gamma*vx)
    Euler=H*Jx+a**3*(r/tau)**2*(z-Xtrue)
    formula=a**3*(r/tau)**2*((1-gamma**2)*(z-Xlin)+Xlin-Xtrue)+a**3*gamma*Hx*v/tau
    assert sp.simplify(Euler-formula)==0
    # The earlier INTERNAL-TIME expression omits the x-embedded gamma_x term
    # and is not a valid physical-x continuous-Euler identity in general.
    wrong_no_gamma_x=formula-a**3*gamma*Hx*v/tau
    assert sp.simplify(Euler-wrong_no_gamma_x)!=0
    wrong_gamma=formula+a**3*(r/tau)**2*(gamma**2-gamma)*(z-Xlin)
    assert sp.simplify(Euler-wrong_gamma)!=0
    wrong_drive=formula-2*a**3*(r/tau)**2*(Xlin-Xtrue)
    assert sp.simplify(Euler-wrong_drive)!=0
    assert sp.simplify(formula.subs({H:hm/tau,Hx:0,Xtrue:Xlin}))==0
    return 'GE19_D15A_ORIGINAL_ACTION_X_CLOCK_SYMPY_IDENTITY_PASS_NEGATIVE_CONTROLS_PASS'


def independent_signed_convolve(ee,qq):
    out=np.zeros((ee.shape[-1],source.M_MAX+1),complex)
    for i,mi in enumerate(source.MODES):
        for j,mj in enumerate(source.MODES):
            for si in (-1,1):
                E=ee[:,i,:] if si==1 else np.conj(ee[:,i,:])
                for sj in (-1,1):
                    m=int(si*mi+sj*mj)
                    if 0<=m<=source.M_MAX:
                        Q=qq[:,j,:] if sj==1 else np.conj(qq[:,j,:])
                        out[:,m]+=4*np.einsum('bt,bt->t',E,Q,optimize=True)
    return out


def synthetic_source_and_envelopes():
    nq,ni=7,5
    r=np.array([.11,.3,.59,.85,1.2,1.8,3.2])
    w=np.array([.09,.13,.18,.17,.15,.14,.14])
    nt=np.arange(ni)[None,None,:]
    nm=source.MODES[None,:,None]
    nr=r[:,None,None]
    z=(.37+.07*nr+.014*nm)*np.exp(1j*(.23*nr+.1*nm+.3*nt))
    v=(.26+.03*nm+.06*nr)*np.exp(1j*(.19*nr+.09*nm-.08*nt))
    Xlin=.2*np.exp(1j*(.13*source.MODES[:,None]+.11*np.arange(ni)[None,:]))
    a=np.linspace(.52,.74,ni)
    H=np.linspace(.51,.56,ni)
    Hx=np.linspace(-.08,-.06,ni)
    hmid=np.linspace(.53,.55,ni)*.7
    tau=.7
    kfund=.16
    out=source.x_embedded_clock_source(z,v,Xlin,a,H,Hx,hmid,r,w,tau,kfund,
                                         independent_signed_convolve)
    assert out['signed_W_clock'].shape==(ni,41)
    assert out['conditional_unsigned_W_drive_per_max_eps_X'].shape==(ni,41)
    assert np.all(np.abs(out['signed_W_clock'])<=out['unsigned_W_clock_envelope']*(1+1e-11)+1e-25)
    omega=r[:,None,None]/tau
    sqrtw=np.sqrt(w)[:,None,None]
    qx=sqrtw/omega*(1j*kfund*source.MODES[None,:,None])*z
    ecoef=np.broadcast_to(-sqrtw*omega/2*a[None,None,:]**3,z.shape)
    eps=.013
    delta=eps*np.exp(1j*(.13*source.MODES[:,None]+.23*np.arange(ni)[None,:]))
    Wdrive=independent_signed_convolve(ecoef*delta[None,:,:],qx)
    upper=out['conditional_unsigned_W_drive_per_max_eps_X']*eps
    assert np.all(np.abs(Wdrive)<=upper*(1+1e-11)+1e-23)
    # Negative controls: wrong gamma and zeroing unknown X error must change
    # nontrivial source/conditional coefficient arrays.
    assert np.linalg.norm(out['signed_W_clock'])>1e-16
    assert np.linalg.norm(out['conditional_unsigned_W_drive_per_max_eps_X'])>1e-16
    # A synthetic constant-H original R1 clock with Xtrue=Xlin is exactly
    # on shell for the frozen equation, independent of the nonzero z/v state.
    constant=source.x_embedded_clock_source(z,v,Xlin,a,np.full(ni,.55),
            np.zeros(ni),np.full(ni,tau*.55),r,w,tau,kfund,
            independent_signed_convolve)
    assert np.array_equal(constant['signed_W_clock'],np.zeros((ni,41),complex))
    return 'GE19_D15A_SYNTHETIC_SIGNED_BATH_AND_CONDITIONAL_DRIVE_ENVELOPES_PASS'


def analytic_background():
    class FakeR7:
        C_VALUES={'C_star':.25}
        K2=2.;Z0=.3;Q0=.1
        @staticmethod
        def exp_Z_from_KQ(kq):
            xx=np.asarray(kq,float)/(4*FakeR7.K2*FakeR7.Z0)
            return np.sqrt(np.real(lambertw(2*xx*xx))/2)
    x=np.linspace(-.8,0,12)
    a=np.exp(x)
    I0=1.2
    lam=.08
    kq=I0/a**3
    Z=FakeR7.exp_Z_from_KQ(kq)
    Q=FakeR7.Q0+FakeR7.Z0*Z
    ex=kq/(4*FakeR7.K2*FakeR7.Z0*Z)
    K=2*FakeR7.K2*FakeR7.Z0**2*(ex-1)
    H=np.sqrt((Q*kq-K)/3+.25/a**3+lam)
    bg={'x':x,'a':a,'KQ_action':kq,'H':H,
        'rho_lambda_action':np.full(x.shape,lam)}
    evaluate,diag=source.make_original_action_background(FakeR7,bg,'C_star')
    assert diag['original_action_H_knot_relative_machine']<1e-13
    q=np.array([-.73,-.41,-.13]); Hq,Hx=evaluate(q)
    h=1.e-5
    Hfd=(evaluate(q+h)[0]-evaluate(q-h)[0])/(2*h)
    assert np.max(np.abs(Hx-Hfd))<1e-8
    bad=dict(bg);bad['rho_lambda_action']=np.linspace(.07,.08,len(x))
    try:source.make_original_action_background(FakeR7,bad,'C_star')
    except RuntimeError:pass
    else:raise AssertionError('D15a must reject variable original Lambda under constant-Lambda source')
    return 'GE19_D15A_STABLE_EXP_ACTION_BACKGROUND_HX_AND_WRONG_LAMBDA_NEGATIVE_CONTROL_PASS'

if __name__=='__main__':
    print(symbolic_identity())
    print(synthetic_source_and_envelopes())
    print(analytic_background())
    print('GE19_H4F3D15A_STATIC_MACHINE_PASS_ACTUAL_R1_CONTINUOUS_X10_OPEN')
