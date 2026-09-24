#!/usr/bin/env python3
"""H3F source adapter: action-completed Y on frozen GE19 non-Y H3 source.

This is a new, versioned source wrapper. It does not modify Repair07,
Repair14, Repair21, Repair22 or their historical files and outputs.
It replaces (never adds on top of) the old scalar-only Y contribution
with the two nonzero action-derived Stage E raw Y rows.
"""
from __future__ import annotations

import numpy as np

from ge19 import h4_stagee_versioned_y_source_rows as stagee


def replace_y_only(legacy_by_beta,bg,u10,phi10_x,kb,a0,kfund,mmax=40):
    """Replace the complete old Y term in an existing frozen H3 bundle.

    legacy_by_beta[beta] contains the frozen Fourier source dictionary,
    with keys rhs, rhs_constraint, Q_ga, Q_matter, Q_lambda, Y_H3.
    u10 and phi10_x must be real [nt,nx] fields on exactly the same
    background/time/space representation as the legacy source.
    """
    aa=np.asarray(bg["a"],float)
    qq=np.asarray(bg["Q_action"],float)
    uu=np.asarray(u10,float)
    px=np.asarray(phi10_x,float)
    if uu.ndim!=2 or px.shape!=uu.shape or uu.shape[0]!=aa.size:
        raise ValueError("H3F source representation mismatch")
    nx=uu.shape[1]
    if not isinstance(mmax,int) or mmax<1 or mmax>=nx//3:
        raise ValueError("H3F retained mmax violates original 2/3 source scope")
    if tuple(float(k) for k in legacy_by_beta.keys())!=stagee.FROZEN_BETAS:
        raise ValueError("H3F source beta cohort mismatch or reordered")

    result={}
    for beta in stagee.FROZEN_BETAS:
        old=legacy_by_beta[beta]
        new=stagee.source_h3(
            aa,qq,uu,px,kb,a0,beta,kfund
        )
        main=np.fft.fft(new["main"],axis=-1)/nx
        con=np.fft.fft(new["constraint"],axis=-1)/nx
        low=np.asarray(main[:,:,:mmax+1],complex)
        clow=np.asarray(con[:,:,:mmax+1],complex)
        oldy=np.asarray(old["Y_H3"],complex)
        oldrhs=np.asarray(old["rhs"],complex)
        oldcon=np.asarray(old["rhs_constraint"],complex)
        if low.shape!=oldy.shape or clow.shape!=oldcon.shape:
            raise ValueError("H3F GE19 source row/mode shape mismatch")
        pieces=tuple(np.asarray(old[name],complex)
                     for name in ("Q_ga","Q_matter","Q_lambda"))
        if any(p.shape!=low.shape for p in pieces):
            raise ValueError("H3F analytic non-Y source layout mismatch")
        if not all(np.isfinite(p).all() for p in (*pieces,oldrhs,oldcon,oldy)):
            raise ValueError("H3F nonfinite legacy source")
        non_y=sum(pieces,np.zeros_like(low))
        # Prefer the independently preserved analytic non-Y decomposition.
        # The legacy total is an independent exact cross-check, not a
        # fallback that could silently carry any old scalar Y term.
        legacy_non_y=oldrhs-oldy
        defect=np.linalg.norm(legacy_non_y-non_y)/max(
            np.linalg.norm(legacy_non_y),np.linalg.norm(non_y),1e-300
        )
        if not np.isfinite(defect) or defect>1e-12:
            raise RuntimeError(
                f"frozen H3 non-Y decomposition mismatch beta={beta}: {defect}"
            )
        if np.any(clow):
            raise RuntimeError("Y sector generated a forbidden constraint row")
        item=dict(old)
        item["rhs"]=np.asarray(non_y+low,complex)
        item["rhs_constraint"]=oldcon.copy()
        item["Y_H3_legacy_report_only"]=oldy.copy()
        item["Y_H3"]=low.copy()
        item["Y_H3_new_aether"]=low[2].copy()
        item["Y_H3_new_scalar"]=low[3].copy()
        item["H3F_non_Y_reproduction_relative_L2"]=float(defect)
        item["H3F_Y_source_action_derived"]=True
        result[beta]=item
    return result


def source_bundle_reduced_lambda(
    r7,r14,mod6,mod7,bg,rho_lambda,tag,nx,state,dot,mmax=40
):
    """Production H3F wrapper over the unchanged Repair14 source builder.

    The old source is first constructed on this exact H1/time/spatial
    representation. Stage E then replaces its entire old Y term.
    """
    legacy=r14.source_bundle_reduced_lambda(
        r7,mod6,mod7,bg,rho_lambda,tag,nx,state,dot
    )
    real,_,spatial=r7.reduced_state_real(bg,state,nx,dot)
    return replace_y_only(
        legacy,bg,real["u20"],spatial["phi20"],
        r7.KB,r7.A0_MPC_INV,
        float(r7.g9.K_REQ[0]/r7.FOURIER_N[0]),
        mmax=mmax
    )
