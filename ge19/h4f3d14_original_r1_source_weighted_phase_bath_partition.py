#!/usr/bin/env python3
"""GE19 D14: original GE05 R1 source-weighted phase bins, signed and unsigned.

Same original R1 z,v,X,r,w,tau, same D13 one-sided interval expression,
same original GE05 normalized E_q10, q_chi10 and signed +/- mode convolution.
This module applies phase masks to ORIGINAL source terms, never to a
post-convolution W, and retains cancellation-sensitive FD4 bin totals.
This is a diagnostic of frozen input, not bath on-shell certification.
"""
from __future__ import annotations
import numpy as np
from ge19 import h4f3d13_original_r1_interval_signed_bath_assembly as prior

EDGES=(0.,.25,.5,1.,float(np.pi),float("inf"))
LABELS=("lt025","025_05","05_1","1_pi","ge_pi")
TINY=1.e-300

def norm(a):
    return float(np.linalg.norm(np.asarray(a)))

def rel(a,b):
    return norm(np.asarray(a)-np.asarray(b))/max(norm(a),norm(b),TINY)

def original_phase(z,v,X,a,H,x,r,w,tau,kfund,fd4,convolve):
    prior_out,prior_diag=prior.interval_signed(
        z,v,X,a,H,x,r,w,tau,kfund,fd4,convolve)
    z=np.asarray(z,complex); v=np.asarray(v,complex)
    X=np.asarray(X,complex); a=np.asarray(a,float)
    H=np.asarray(H,float); x=np.asarray(x,float)
    r=np.asarray(r,float); w=np.asarray(w,float)
    nb,nm,nt=z.shape
    omega=r[:,None,None]/tau
    ww=np.sqrt(w)[:,None,None]
    a3=a[None,None,:]**3
    rr2=r[:,None,None]**2
    current=a3*v/tau
    sampled_kinetic=H[None,None,:]*fd4(current,x)
    potential=a3*omega**2*(z-X[None,:,:])
    Rfd=sampled_kinetic+potential
    Efd=-ww/(2*omega)*Rfd
    qx=ww/omega*(1j*kfund*prior.MODES[None,:,None])*z
    hmid=np.sqrt(H[:-1]*H[1:])
    hinterval=tau*hmid
    phase=r[:,None]*np.diff(x)[None,:]/hinterval[None,:]
    return prior_out,prior_diag,dict(
        z=z,v=v,X=X,a=a,H=H,x=x,r=r,w=w,tau=tau,
        nb=nb,nt=nt,omega=omega,ww=ww,a3=a3,rr2=rr2,
        sampled_kinetic=sampled_kinetic,potential=potential,
        Efd=Efd,qx=qx,hinterval=hinterval,phase=phase)

def unsigned_envelope(E,qx,mask):
    """Valid componentwise bound for original signed +/- Fourier convolution.

    Each mode receives the absolute node sum for ALL original signed
    mode pairings; masks are per original frequency node and interval.
    It is deliberately conservative, and not a physics acceptance gate.
    """
    E=np.asarray(E,complex); qx=np.asarray(qx,complex)
    mask=np.asarray(mask,bool)
    nb,nm,ni=E.shape
    if (E.shape!=qx.shape or nm!=len(prior.MODES)
        or mask.shape!=(nb,ni)):
        raise ValueError("D14 source bound phase-bin dimensions invalid")
    out=np.zeros((ni,prior.M_MAX+1),float)
    for i,mi in enumerate(prior.MODES):
        for j,mj in enumerate(prior.MODES):
            signed_pairs=sum(
                int(0<=si*mi+sj*mj<=prior.M_MAX)
                for si in (-1,1) for sj in (-1,1))
            if signed_pairs==0:continue
            contribution=4*np.sum(
                np.abs(E[:,i,:])*np.abs(qx[:,j,:])*mask,
                axis=0)
            for si in (-1,1):
                for sj in (-1,1):
                    m=int(si*mi+sj*mj)
                    if 0<=m<=prior.M_MAX:
                        out[:,m]+=contribution
    if not np.isfinite(out).all() or np.any(out<0):
        raise RuntimeError("D14 nonfinite conservative GE05 unsigned envelope")
    return out

def phase_partition(z,v,X,a,H,x,r,w,tau,kfund,fd4,convolve):
    baseline,diagnostic,ctx=original_phase(
        z,v,X,a,H,x,r,w,tau,kfund,fd4,convolve)
    phase=ctx["phase"]
    if (phase.shape!=(ctx["nb"],ctx["nt"]-1)
        or not np.isfinite(phase).all() or np.any(phase<0)):
        raise ValueError("D14 invalid frozen original R1 phase")
    masks=[(phase>=low)&(phase<high)
           for low,high in zip(EDGES[:-1],EDGES[1:])]
    if not np.all(sum(mask.astype(int) for mask in masks)==1):
        raise RuntimeError("D14 original phase bins must exactly partition R1 nodes")
    out={"original_interval_phase":phase,
         "original_FD4_signed_W":baseline["FD4_original_signed_W"]}
    rows={}
    for side,sl,nh,ah in (
        ("left",slice(1,None),ctx["H"][1:],ctx["a3"][:,:,1:]),
        ("right",slice(None,-1),ctx["H"][:-1],ctx["a3"][:,:,:-1])):
        vs=ctx["v"][:,:,sl]; zs=ctx["z"][:,:,sl]
        drive=ctx["X"][None,:,sl]
        jt=(3*nh[None,None,:]*ah*vs/tau
            +ah*(-3*ctx["hinterval"][None,None,:]*vs
                  -ctx["rr2"]*(zs-drive))/tau**2)
        pot=ah*(ctx["r"][:,None,None]/tau)**2*(zs-drive)
        ode=jt+pot
        defect=ctx["sampled_kinetic"][:,:,sl]-jt
        e_ode=-ctx["ww"]/(2*ctx["omega"])*ode
        e_def=-ctx["ww"]/(2*ctx["omega"])*defect
        e_fd=ctx["Efd"][:,:,sl]
        qx=ctx["qx"][:,:,sl]
        whole_o=convolve(e_ode,qx)
        whole_d=convolve(e_def,qx)
        whole_fd=baseline["FD4_original_signed_W"][sl,:]
        if max(rel(whole_o,baseline[side+"_signed_interval_W"]),
               rel(whole_d,baseline[side+"_signed_derivative_defect_W"]))>1e-11:
            raise RuntimeError("D14 no longer matches exact original D13 one-sided GE05 source")
        sums={"ODE":np.zeros_like(whole_o),
              "defect":np.zeros_like(whole_d),
              "FD4":np.zeros_like(whole_fd)}
        phase_rows=[]
        for label,mask in zip(LABELS,masks):
            bmask=mask[:,None,:]
            wo=convolve(e_ode*bmask,qx)
            wd=convolve(e_def*bmask,qx)
            wf=convolve(e_fd*bmask,qx)
            bo=unsigned_envelope(e_ode,qx,mask)
            bd=unsigned_envelope(e_def,qx,mask)
            bf=unsigned_envelope(e_fd,qx,mask)
            bounds={}
            for part,wat,ub in (("ODE",wo,bo),
                                 ("defect",wd,bd),("FD4",wf,bf)):
                ratio=float(np.max(np.abs(wat)/(ub+TINY)))
                if not np.isfinite(ratio) or ratio>1+1e-11:
                    raise RuntimeError("D14 source-weighted bin absolute envelope invalid")
                bounds[part]=ratio
                sums[part]+=wat
                out[side+"_"+label+"_"+part+"_signed_W"]=wat
                out[side+"_"+label+"_"+part+"_unsigned_envelope"]=ub
            identity=rel(wf,wo+wd)
            if identity>1e-11:
                raise RuntimeError("D14 phase-bin signed original FD4 source identity invalid")
            phase_rows.append({
              "phase_bin":label,
              "node_interval_count":int(np.count_nonzero(mask)),
              "ODE_signed_L2_report_only":norm(wo),
              "defect_signed_L2_report_only":norm(wd),
              "FD4_signed_L2_report_only":norm(wf),
              "ODE_unsigned_envelope_L2_report_only":norm(bo),
              "defect_unsigned_envelope_L2_report_only":norm(bd),
              "FD4_unsigned_envelope_L2_report_only":norm(bf),
              "FD4_equals_ODE_plus_defect_identity_only":identity,
              "componentwise_original_unsigned_bounds_max_ratio_identity_only":bounds})
        residuals={
          "ODE_bins_sum_to_original_D13":rel(sums["ODE"],baseline[side+"_signed_interval_W"]),
          "defect_bins_sum_to_original_D13":rel(sums["defect"],baseline[side+"_signed_derivative_defect_W"]),
          "FD4_bins_sum_to_original_D13":rel(sums["FD4"],whole_fd),
          "source_original_FD4_equals_ODE_plus_defect":rel(whole_fd,whole_o+whole_d)}
        if max(residuals.values())>1e-11:
            raise RuntimeError("D14 source-weighted bins do not reproduce original D13 physical archive")
        rows[side]={"phase_bins":phase_rows,"signed_exact_machine_identity_only":residuals,
                    "all_source_weighted_bins_finite":True,
                    "GE05_bath_on_shell_certified":False}
    if any(not np.isfinite(arr).all() for arr in out.values()):
        raise RuntimeError("D14 nonfinite source-weighted actual signed bath archive")
    return out,rows
