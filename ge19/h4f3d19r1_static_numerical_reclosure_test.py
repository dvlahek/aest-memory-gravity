#!/usr/bin/env python3
"""Independent manufactured high-phase oscillator for D19R1 bridge, no physical claims."""
import numpy as np
from ge19 import h4f3d19r1_physical_bath_numerical_core as c

def step_undamped_linear(q,v,r,h,X0,X1,ds):
    # Independent exact solution of z''+r^2(z-X_linear)=0, high-phase included.
    rr=np.asarray(r)[:,None];slope=(X1-X0)/ds
    z0=q-X0;u0=v-slope
    co=np.cos(rr*ds);si=np.sin(rr*ds)
    return X1+z0*co+u0*(si/rr),slope-rr*z0*si+u0*co

def H(x):
    q=np.asarray(x,float)
    return np.zeros_like(q)+.7,np.zeros_like(q)

def run():
    orig=np.array([0.,.4,.8]);fine=np.linspace(0.,.8,9)
    r=np.array([.2,3.,500.]);rr=r[:,None]
    X=np.tile(np.linspace(.001,.006,6)[:,None],(1,9)).astype(complex)
    DX=np.zeros_like(X);init=np.tile(np.linspace(.01,.06,6)[None,:],(3,1))
    z0=X[:,0][None,:]+init;v0=np.zeros_like(z0)
    for nsub in (16,32,64):
        sol=c.propagate(fine,X,DX,H,z0,v0,r,1.,step_undamped_linear,nsub,orig)
        time=(orig-orig[0])/.7
        expected=X[:,0][None,:,None]+init[:,:,None]*np.cos(r[:,None,None]*time[None,None,:])
        vel=-r[:,None,None]*init[:,:,None]*np.sin(r[:,None,None]*time[None,None,:])
        assert c.rel(sol['z'],expected)<3.e-11,(nsub,c.rel(sol['z'],expected))
        assert c.rel(sol['v'],vel)<3.e-11,(nsub,c.rel(sol['v'],vel))
        assert sol['sample_Rs'].shape==(3,6,4)
        assert c.norm(sol['sample_Rs'])<2.e-9, (nsub,c.norm(sol['sample_Rs']))
        assert c.high_phase_mask(r,np.diff(orig)/.7,1.)[-1].all()
    changed=DX.copy();changed[0,1]=.04
    sol=c.propagate(fine,X,changed,H,z0,v0,r,1.,step_undamped_linear,16,orig)
    assert c.norm(sol['sample_Rs'])>1.e-5,'D19R1 wrong H1 jets negative control did not register GE05 defect'
    print('GE19_D19R1_MANUFACTURED_EXACT_HIGH_PHASE_AND_TRUE_CLOCK_SOURCE_PASS',flush=True)
    print('GE19_D19R1_WRONG_D17_SOURCE_JET_NEGATIVE_CONTROL_PASS',flush=True)
if __name__=='__main__':run()
