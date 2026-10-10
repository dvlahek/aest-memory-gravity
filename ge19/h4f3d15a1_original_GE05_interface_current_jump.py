#!/usr/bin/env python3
"""D15a1 source-first ORIGINAL GE05 distributional interior-interface audit.

For the ORIGINAL Repair24 R1 state embedded on the physical x=ln(a)
background, z is continuous but z_t=gamma*v/tau need not be continuous
across adjacent frozen-hmid steps. We save the signed coefficient of
its delta(t-t_i) Euler term; do not add its knot-vector L2 to the smooth
interval Euler L2 or treat it as a physically allowed impulsive source.
"""
from __future__ import annotations
import numpy as np
from ge19 import h4f3d15a_original_GE05_clock_embedded_source as smooth


def original_GE05_interior_current_jump(z,v,a,H,hmid,r,w,tau,kfund,convolve):
    zz=np.asarray(z,complex);vv=np.asarray(v,complex)
    aa=np.asarray(a,float);HH=np.asarray(H,float)
    hh=np.asarray(hmid,float);rr=np.asarray(r,float);ww=np.asarray(w,float)
    if (zz.ndim!=3 or zz.shape!=vv.shape or zz.shape[1]!=len(smooth.MODES)
        or zz.shape[-1]<3 or aa.shape!=HH.shape or aa.shape!=(zz.shape[-1],)
        or hh.shape!=(zz.shape[-1]-1,) or rr.shape!=(zz.shape[0],)
        or ww.shape!=rr.shape or np.any(aa<=0) or np.any(HH<=0)
        or np.any(hh<=0) or np.any(rr<=0) or np.any(ww<=0)
        or tau<=0 or kfund<=0
        or any(not np.isfinite(t).all() for t in (zz,vv,aa,HH,hh,rr,ww))):
        raise ValueError('D15a1 invalid original R1 interior action interface')
    omega=rr[:,None,None]/tau
    sqrtw=np.sqrt(ww)[:,None,None]
    gamma_minus=tau*HH[1:-1]/hh[:-1]
    gamma_plus=tau*HH[1:-1]/hh[1:]
    jump_gamma=gamma_plus-gamma_minus
    # Coefficient of delta(t-t_i) in d_t(a^3*z_t).
    jump_J=(aa[1:-1][None,None,:]**3)*(jump_gamma[None,None,:])*vv[:,:,1:-1]/tau
    eq_impulse=-sqrtw/(2.0*omega)*jump_J
    qx=(sqrtw/omega)*(1j*kfund*smooth.MODES[None,:,None])*zz[:,:,1:-1]
    Wimp=convolve(eq_impulse,qx)
    unsigned=smooth.unsigned_signed_pair_envelope(eq_impulse,qx)
    if Wimp.shape!=(len(aa)-2,smooth.M_MAX+1):
        raise RuntimeError('D15a1 original signed interface mode scope changed')
    if np.any(np.abs(Wimp)>unsigned*(1+1e-11)+1e-25):
        raise RuntimeError('D15a1 original GE05 interface unsigned bound violated')
    if any(not np.isfinite(q).all() for q in (jump_gamma,jump_J,Wimp,unsigned)):
        raise RuntimeError('D15a1 nonfinite original GE05 interior interface source')
    return {
      'interior_gamma_plus_minus_jump':jump_gamma,
      'interior_original_J_jump_node_mode_L2':np.linalg.norm(jump_J,axis=0),
      'interior_original_GE05_Eq_impulse_signed_W_coeff':Wimp,
      'interior_original_GE05_Eq_impulse_unsigned_W_coeff_envelope':unsigned,
      'interior_interface_coeff_multiplies_delta_t_not_smooth_W':True,
      'external_original_action_boundary_not_evaluated':True,
      'GE05_continuous_on_shell_not_certified':True}
