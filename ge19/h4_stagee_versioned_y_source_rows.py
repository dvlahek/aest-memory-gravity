#!/usr/bin/env python3
"""GE19 Stage E: versioned, action-derived NL0C Y-only H3/H4 raw RHS rows.

Standalone source constructor. This module MUST NOT patch, import, or
execute the frozen Repair07 / Repair37 state solvers. The complete Y-only
dictionary is derived in frozen Stage D; this file implements its real-space
flux and common spectral projection for a separately versioned parent.

Source ordering is GE19 [N, L+R, u, phi, T, rho] plus [shift, anisotropy].
The background Q and beta have zero eta derivative in the frozen hierarchy.
No field-independent global F2 kernel is introduced at zero gradient.
"""
from __future__ import annotations

import numpy as np

SOURCE_ORDER=("N","L_plus_R","u","phi","T","rho")
CONSTRAINT_ORDER=("shift_b","anisotropy_L_minus_R_over2")
FROZEN_BETAS=(1.0,0.5,0.1)


def _inputs(a,Q,u,phi_x,KB,a0,beta,kfund):
    aa=np.asarray(a,float)
    qq=np.asarray(Q,float)
    uu=np.asarray(u,float)
    pp=np.asarray(phi_x,float)
    if aa.ndim!=1 or qq.shape!=aa.shape:
        raise ValueError("a and Q must be same-shape time vectors")
    if uu.ndim!=2 or pp.shape!=uu.shape or uu.shape[0]!=aa.size:
        raise ValueError("u and phi_x must be same-shape [nt,nx] arrays")
    if aa.size==0 or uu.shape[1]<6:
        raise ValueError("nonempty time and nx >= 6 required")
    if not all(np.isfinite(x).all() for x in (aa,qq,uu,pp)):
        raise ValueError("nonfinite background or first-order field")
    if not np.all(aa>0):
        raise ValueError("scale factor must be positive")
    vals=(float(KB),float(a0),float(beta),float(kfund))
    if not all(np.isfinite(x) for x in vals):
        raise ValueError("nonfinite physical coefficient or wavenumber")
    kb,a0v,bet,kk=vals
    if not (0.0<kb<2.0 and a0v>0.0 and kk>0.0):
        raise ValueError("invalid frozen AeST coupling or units")
    if bet not in FROZEN_BETAS:
        raise ValueError("beta is outside frozen co-primary cohort")
    kappa=2.0*(2.0-kb)/((1.0+bet)*a0v)
    return aa,qq,uu,pp,kappa,kk


def _project_flux_and_dx(flux,kfund):
    raw=np.asarray(flux,float)
    nx=raw.shape[-1]
    modes=np.fft.fftfreq(nx)*nx
    keep=np.abs(modes)<=nx/3.0+1e-12
    spectral=np.fft.fft(raw,axis=-1)*keep[None,:]
    return (
        np.fft.ifft(spectral,axis=-1).real,
        np.fft.ifft(1j*(kfund*modes)[None,:]*spectral,axis=-1).real
    )


def _rhs(a,Q,kappa,kfund,flux):
    projected,div_x=_project_flux_and_dx(flux,kfund)
    aa=a[:,None]
    qq=Q[:,None]
    main=np.zeros((6,flux.shape[0],flux.shape[1]),float)
    constraints=np.zeros((2,flux.shape[0],flux.shape[1]),float)
    main[2]=2.0*aa**3*qq*kappa*projected
    main[3]=-2.0*aa**2*kappa*div_x
    if not np.isfinite(main).all():
        raise FloatingPointError("nonfinite action-derived Y source")
    return {
        "main":main,
        "constraint":constraints,
        "raw_flux":np.asarray(flux,float),
        "projected_flux":projected,
        "spatial_flux_derivative":div_x,
        "kappa":float(kappa),
    }


def source_h3(a,Q,u10,phi10_x,KB,a0,beta,kfund):
    """Return all 6 main and 2 constraint Y-only H3 raw GE19 RHS rows.

    The H3 coefficient is the second physical epsilon derivative.
    Equations: S_u=+2 a^3 Q kappa P(|g|g),
    S_phi=-2 a^2 kappa partial_x P(|g|g).
    """
    aa,qq,uu,pp,kappa,kk=_inputs(
        a,Q,u10,phi10_x,KB,a0,beta,kfund
    )
    g=qq[:,None]*uu+pp/aa[:,None]
    if not np.isfinite(g).all():
        raise FloatingPointError("nonfinite directional Y gradient")
    out=_rhs(aa,qq,kappa,kk,np.abs(g)*g)
    out["gradient"]=g
    return out


def source_h4(a,Q,u10,phi10_x,u11,phi11_x,KB,a0,beta,kfund):
    """Return Y-only H4 raw GE19 RHS rows, exact eta tangent of H3.

    With fixed background Q and beta: flux21=2 |g10| g11.
    At g10=0, this derivative is continuously zero for any g11.
    """
    aa,qq,u0,p0,kappa,kk=_inputs(
        a,Q,u10,phi10_x,KB,a0,beta,kfund
    )
    a2,q2,u1,p1,kappa2,kk2=_inputs(
        a,Q,u11,phi11_x,KB,a0,beta,kfund
    )
    if not (np.array_equal(aa,a2) and np.array_equal(qq,q2)
            and kappa==kappa2 and kk==kk2):
        raise RuntimeError("eta tangent changed frozen background")
    g0=qq[:,None]*u0+p0/aa[:,None]
    g1=qq[:,None]*u1+p1/aa[:,None]
    if not (np.isfinite(g0).all() and np.isfinite(g1).all()):
        raise FloatingPointError("nonfinite Y gradient tangent")
    out=_rhs(aa,qq,kappa,kk,2.0*np.abs(g0)*g1)
    out["gradient10"]=g0
    out["gradient11"]=g1
    return out
