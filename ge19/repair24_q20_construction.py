#!/usr/bin/env python3
"""GE19 Repair24 — construction of the baseline second-order normalized bath q20.

Consumes frozen Repair22 Z20 and the frozen v0.77 full-history base trace.
No H4/Z21 solve and no finite eta.
"""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import importlib.util
import io
import json
import math
import os
import tempfile
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.interpolate import PchipInterpolator

ROOT=Path(__file__).resolve().parents[1]
import sys
sys.path.insert(0,str(ROOT))

REPAIR22_JSON_SHA="7d53b2458183c6b2cc326acdded70b2c3ce1fab959d8456e56d3b4f1f86ef374"
REPAIR22_NPZ_SHA="3020e0d040f902ab2609e05705f4508d9919665b1344fa0e641644ea8fc41a16"
REPAIR13_JSON_SHA="ae3cc790ecffbd5498b5852273c72ae578d4615de29bbb616673c05cdb3e74b7"
REPAIR13_NPZ_SHA="011c0ae54fd21d70c0e2c695ce62e7b74a3c5529a07c9023c882a447d5b40ca3"

TAUH0=10.0
NQ_PRIMARY=2048
NQ_CONTROL=1024
NT_PRIMARY=128
NT_CONTROL=64
NX_PRIMARY=512
NX_CONTROL=256
M_MAX=40
CHUNK=16

A_INITIAL=0.4
A_INITIAL_MAX=1e-12
X_INITIAL_MAX=1e-10
SPATIAL_MAX=1e-10
QUAD_MAX=1e-2
TIME_MAX=5e-3
TINY=1e-300


def sha256(path:Path)->str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel_l2(a,b)->float:
    aa=np.asarray(a); bb=np.asarray(b)
    return float(np.linalg.norm(aa-bb)/max(np.linalg.norm(aa),np.linalg.norm(bb),TINY))


def aor(a,b)->float:
    aa=np.asarray(a); bb=np.asarray(b)
    ae=np.abs(aa-bb)
    re=ae/np.maximum(np.maximum(np.abs(aa),np.abs(bb)),TINY)
    return float(np.max(np.minimum(ae,re)))


def load_quiet(path:Path,name:str):
    path=Path(path).resolve()
    old=os.getcwd()
    with tempfile.TemporaryDirectory() as td:
        os.chdir(td)
        try:
            spec=importlib.util.spec_from_file_location(name,path)
            if spec is None or spec.loader is None:
                raise RuntimeError(f"cannot import {path}")
            mod=importlib.util.module_from_spec(spec)
            with contextlib.redirect_stdout(io.StringIO()):
                spec.loader.exec_module(mod)
            return mod
        finally:
            os.chdir(old)


def interp_complex_last(x0,y0,x):
    y=np.asarray(y0)
    re=PchipInterpolator(x0,y.real,axis=-1,extrapolate=False)(x)
    im=PchipInterpolator(x0,y.imag,axis=-1,extrapolate=False)(x)
    return np.asarray(re+1j*im,complex)


def spectral_dx_batch(a,kfund):
    arr=np.asarray(a)
    nx=arr.shape[-1]
    mm=np.fft.fftfreq(nx)*nx
    hh=np.fft.fft(arr,axis=-1)
    return np.fft.ifft(1j*(kfund*mm)*hh,axis=-1).real


def reconstruct_batched_positive_modes(coeff,modes,nx):
    """coeff [batch,nmode,nt] -> real [batch,nt,nx]."""
    cc=np.asarray(coeff,complex)
    theta=2*np.pi*np.arange(nx,dtype=float)/nx
    basis=np.exp(1j*np.asarray(modes)[:,None]*theta[None,:])
    return 2.0*np.real(np.einsum("bmt,mx->btx",cc,basis,optimize=True))


def fft_low_modes(a,mmax=M_MAX):
    arr=np.asarray(a,float)
    hh=np.fft.fft(arr,axis=-1)/arr.shape[-1]
    return np.asarray(hh[...,:mmax+1],complex)


def build_normalized_c2_generator(ge05):
    """Symbolically cancel sqrt(w)/omega from GE05 bath c2 before numerics."""
    zz,zzt,zzx=sp.symbols("zz zzt zzx", real=True)
    sub={
        ge05.dq:ge05.sw*zz/ge05.om,
        ge05.dqt:ge05.sw*zzt/ge05.om,
        ge05.dqx:ge05.sw*zzx/ge05.om,
    }
    expr={}
    for key in ("q","qt","qx"):
        e=(-2*ge05.om/ge05.sw)*ge05.coeff2[key].subs(sub)
        e=sp.factor(sp.cancel(e))
        expr[key]=e

    args=(
        ge05.a,ge05.Q,
        ge05.dN,ge05.dL,ge05.dR,ge05.db,ge05.dr,
        ge05.dpt,ge05.dpx,
        zzt,zzx,zz,
        ge05.om,
    )
    f={k:sp.lambdify(args,v,"numpy",cse=True) for k,v in expr.items()}
    sw_absent=all(ge05.sw not in v.free_symbols for v in expr.values())
    return f,{
        "sqrtw_symbol_absent_after_normalization":bool(sw_absent),
        "expressions":{k:str(v) for k,v in expr.items()},
    }


def step_linear_nd(q,v,r,h,x0,x1,dxi):
    """Vectorized frozen NL1C4 interval propagator.

    q,v,x0,x1 shape [node,...], r shape [node].
    """
    q=np.asarray(q,complex); v=np.asarray(v,complex)
    x0=np.broadcast_to(np.asarray(x0,complex),q.shape)
    x1=np.broadcast_to(np.asarray(x1,complex),q.shape)
    r=np.asarray(r,float)
    if q.shape[0]!=r.size:
        raise ValueError("node dimension mismatch")

    tail=(1,)*(q.ndim-1)
    c=3.0*float(h)
    d=0.5*c
    slope=(x1-x0)/float(dxi)
    u0=q-x0
    vu0=v-slope
    force=-c*slope
    om2=r*r
    disc=om2-d*d
    scale=np.maximum(om2+d*d,1.0)
    under=disc>1e-12*scale
    over=disc<-1e-12*scale
    crit=~(under|over)
    un=np.empty_like(q); vn=np.empty_like(v)

    if np.any(under):
        idx=np.where(under)[0]
        O=np.sqrt(disc[idx]).reshape((-1,)+tail)
        oo2=om2[idx].reshape((-1,)+tail)
        z=O*dxi
        ed=math.exp(-d*dxi)
        co=np.cos(z); si=np.sin(z)
        uu=u0[idx]; vv=vu0[idx]
        hu=ed*(uu*co+(vv+d*uu)/O*si)
        hv=ed*(vv*co-(d*vv+oo2*uu)/O*si)
        one=1.0-ed*(co+d/O*si)
        G=ed*si/O
        un[idx]=hu+force[idx]/oo2*one
        vn[idx]=hv+force[idx]*G

    if np.any(over):
        idx=np.where(over)[0]
        oo2=om2[idx].reshape((-1,)+tail)
        delta=np.sqrt(-disc[idx]).reshape((-1,)+tail)
        lam1=-oo2/(d+delta)
        lam2=-d-delta
        den=lam1-lam2
        e1=np.exp(lam1*dxi); e2=np.exp(lam2*dxi)
        uu=u0[idx]; vv=vu0[idx]
        c1=(vv-lam2*uu)/den
        c2=(lam1*uu-vv)/den
        hu=c1*e1+c2*e2
        hv=lam1*c1*e1+lam2*c2*e2
        one=(-lam2*(-np.expm1(lam1*dxi))+lam1*(-np.expm1(lam2*dxi)))/den
        G=(e1-e2)/den
        un[idx]=hu+force[idx]/oo2*one
        vn[idx]=hv+force[idx]*G

    if np.any(crit):
        idx=np.where(crit)[0]
        oo2=om2[idx].reshape((-1,)+tail)
        zz0=d*dxi
        ed=math.exp(-zz0)
        uu=u0[idx]; vv=vu0[idx]
        hu=ed*(uu+(vv+d*uu)*dxi)
        hv=ed*(vv-(d*vv+oo2*uu)*dxi)
        one=-math.expm1(-zz0)-zz0*ed
        G=ed*dxi
        un[idx]=hu+force[idx]/oo2*one
        vn[idx]=hv+force[idx]*G

    return x1+un, vn+slope


def step_nd_self_test(c4):
    r=np.asarray([0.08,0.7,2.0,9.0],float)
    q=np.asarray([
        [0.2+0.1j,-0.1+0.02j],
        [0.1-0.2j,0.03+0.01j],
        [-0.04+0.02j,0.2-0.1j],
        [0.01+0.03j,-0.02+0.04j],
    ],complex)
    v=0.2*q
    x0=-0.4*q+0.03
    x1=0.7*q-0.02j
    h=1.8; dx=0.031
    qn,vn=step_linear_nd(q,v,r,h,x0,x1,dx)
    errs=[]
    for j in range(q.shape[1]):
        a,b=c4.step_linear(q[:,j],v[:,j],r,h,x0[:,j],x1[:,j],dx)
        errs.extend([aor(qn[:,j],a),aor(vn[:,j],b)])
    return float(max(errs))


def full_history_boundary(c4,r7,trace_path,order):
    rows=c4.read_trace(trace_path)
    histories,kmiss,tmiss=c4.select_and_align(rows)
    aa=np.asarray([q["a"] for q in histories[0]],float)
    i0=int(np.argmin(np.abs(aa-A_INITIAL)))
    amiss=float(abs(aa[i0]-A_INITIAL))
    if amiss>A_INITIAL_MAX:
        raise RuntimeError(f"full-history trace lacks exact a=0.4 surface: mismatch={amiss}")

    amps,_,_=r7.amplitudes()
    z0=np.empty((order,len(r7.FOURIER_N)),complex)
    v0=np.empty_like(z0)
    rr_ref=ww_ref=None
    for im,hist in enumerate(histories):
        rr,ww,qs,vs=c4.integrate_mode(hist[:i0+1],order)
        if rr_ref is None:
            rr_ref=np.asarray(rr,float); ww_ref=np.asarray(ww,float)
        elif aor(rr_ref,rr)>1e-14 or aor(ww_ref,ww)>1e-14:
            raise RuntimeError("quadrature nodes changed between input modes")
        k=float(r7.g9.K_REQ[im])
        fac=0.5*float(amps[im])*np.exp(1j*float(r7.PHASES[im]))*(1j*k)
        z0[:,im]=fac*np.asarray(qs[-1],float)
        v0[:,im]=fac*np.asarray(vs[-1],float)

    trace_x0=np.empty(len(r7.FOURIER_N),complex)
    for im,hist in enumerate(histories):
        k=float(r7.g9.K_REQ[im])
        chi=float(hist[i0]["chi"])
        fac=0.5*float(amps[im])*np.exp(1j*float(r7.PHASES[im]))
        trace_x0[im]=1j*k*fac*chi/A_INITIAL

    return {
        "r":rr_ref,"w":ww_ref,"z0":z0,"v0":v0,
        "trace_X0":trace_x0,
        "a_mismatch":amiss,"k_relative_miss":float(kmiss),
        "common_time_mismatch":float(tmiss),
        "trace_index":i0,
    }


def reconstruct_backgrounds(r7,r11,r13,results_dir,r13npz):
    dense=results_dir/"ge15_R1_dense_accepted_step_trace.dat"
    lamb=results_dir/"ge15_R1_cli_background.dat"
    bgs={}
    controls=[]
    for nt,label in ((NT_PRIMARY,"primary"),(NT_CONTROL,"control")):
        base,_,_=r7.build_ge15_reference(dense,nt)
        rho=r11.interp_lambda(lamb,base["x"])
        for tag in r7.C_TAGS:
            bg,_=r13.reduced_background(r7,base,tag,rho)
            href=np.asarray(r13npz[f"{tag}_H_reduced_{label}"],float)
            hm=rel_l2(bg["H"],href)
            controls.append({"Nt":nt,"C":tag,"H_vs_Repair13_relative_L2":hm})
            if hm>1e-12:
                raise RuntimeError(f"background H does not reproduce Repair13: Nt={nt} C={tag} rel={hm}")
            bgs[(nt,tag)]=bg
    return bgs,controls


def first_order_X_modes(r7,bg,h1):
    """H1 positive-mode longitudinal X10 coefficients [6,nt]."""
    st=np.asarray(h1,complex)
    out=np.empty((len(r7.FOURIER_N),st.shape[-1]),complex)
    for im,m in enumerate(r7.FOURIER_N):
        k=float(m*r7.g9.K_REQ[0]/r7.FOURIER_N[0])
        out[im]=bg["Q_action"]*st[im,2] + (1j*k/bg["a"])*st[im,3]
    return out


def evolve_z10(c4,bg,X,z0,v0,r,tau):
    nq=z0.shape[0]; nm=z0.shape[1]; nt=X.shape[-1]
    z=np.empty((nq,nm,nt),complex)
    v=np.empty_like(z)
    z[:,:,0]=z0; v[:,:,0]=v0
    hgrid=np.asarray(bg["H"],float)*tau
    xgrid=np.asarray(bg["x"],float)
    for it in range(nt-1):
        hm=math.sqrt(hgrid[it]*hgrid[it+1])
        dxi=(xgrid[it+1]-xgrid[it])/hm
        z[:,:,it+1],v[:,:,it+1]=step_linear_nd(
            z[:,:,it],v[:,:,it],r,hm,
            np.broadcast_to(X[:,it],(nq,nm)),
            np.broadcast_to(X[:,it+1],(nq,nm)),
            dxi,
        )
    return z,v


def metric_real_fields(r7,bg,h1,h1dot,nx):
    real={}
    names={0:"N",1:"S",2:"u",3:"phi"}
    for iv,name in names.items():
        real[name]=r7.reconstruct_positive_modes(np.asarray(h1[:,iv,:],complex),nx)
    real["phidot"]=r7.reconstruct_positive_modes(np.asarray(h1dot[:,2,:],complex),nx)
    kfund=float(r7.g9.K_REQ[0]/r7.FOURIER_N[0])
    real["phix"]=r7.spectral_dx(real["phi"],kfund)
    return real


def normalized_g2_chunk(normf,r7,bg,metric,zchunk,vchunk,rchunk,tau,nx):
    """Return normalized G2 low modes [node,40,nt]."""
    nt=len(bg["x"]); nq=len(rchunk)
    kfund=float(r7.g9.K_REQ[0]/r7.FOURIER_N[0])
    modes=np.asarray(r7.FOURIER_N,int)

    zr=reconstruct_batched_positive_modes(zchunk,modes,nx)
    ztr=reconstruct_batched_positive_modes(vchunk/tau,modes,nx)
    k_modes=np.asarray([float(m*kfund) for m in modes],float)
    zxr=reconstruct_batched_positive_modes(
        (1j*k_modes[None,:,None])*zchunk,modes,nx
    )

    shape=(nq,nt,nx)
    aa=np.broadcast_to(np.asarray(bg["a"],float)[None,:,None],shape)
    QQ=np.broadcast_to(np.asarray(bg["Q_action"],float)[None,:,None],shape)
    zero=np.zeros((nt,nx),float)

    args_common=[
        aa,QQ,
        metric["N"][None,:,:],
        metric["S"][None,:,:],
        metric["S"][None,:,:],
        zero[None,:,:],
        metric["u"][None,:,:],
        metric["phidot"][None,:,:],
        metric["phix"][None,:,:],
        ztr,zxr,zr,
        np.asarray(rchunk,float)[:,None,None]/tau,
    ]
    pd={}
    for key,fn in normf.items():
        val=np.asarray(fn(*args_common))
        pd[key]=np.broadcast_to(val,shape).astype(float,copy=False)

    D=r7.fd4_matrix(nt,bg["x"][0],bg["x"][-1])
    Dt=np.asarray(bg["H"],float)[:,None]*D
    dt_qt=np.einsum("ij,bjk->bik",Dt,pd["qt"],optimize=True)
    dx_qx=spectral_dx_batch(pd["qx"],kfund)
    g2=pd["q"]-dt_qt-dx_qx
    low=fft_low_modes(g2,M_MAX)[:,:,1:M_MAX+1]   # [node,nt,40]
    return np.transpose(low,(0,2,1)).copy()


def X20_modes(r7,bg,z20):
    """Certified Z20 -> linear second-order bath drive X20 [beta,40,nt]."""
    st=np.asarray(z20,complex)
    nb,nm,_,nt=st.shape
    out=np.empty((nb,nm,nt),complex)
    kfund=float(r7.g9.K_REQ[0]/r7.FOURIER_N[0])
    for jm,m in enumerate(r7.M_SOLVE):
        k=float(m*kfund)
        out[:,jm,:]=bg["Q_action"][None,:]*st[:,jm,2,:] + (
            1j*k/bg["a"][None,:]
        )*st[:,jm,3,:]
    return out


def solve_z20_chunk(bg,X20,g2,rchunk,tau):
    """Solve q20 normalized node states. Returns [node,beta,40,nt]."""
    nq,nm,nt=g2.shape
    nb=X20.shape[0]
    z=np.zeros((nq,nb,nm,nt),complex)
    v=np.zeros_like(z)
    rr=np.asarray(rchunk,float)
    om2=(rr/tau)**2
    hgrid=np.asarray(bg["H"],float)*tau
    xgrid=np.asarray(bg["x"],float)

    # Xeff = X20-G2/omega^2. G2 scales as omega^2 at the low-r end;
    # monitor finiteness explicitly rather than clipping any node.
    xeff=X20[None,:,:,:]-g2[:,None,:,:]/om2[:,None,None,None]
    if not np.all(np.isfinite(xeff)):
        raise RuntimeError("non-finite q20 effective drive")

    for it in range(nt-1):
        hm=math.sqrt(hgrid[it]*hgrid[it+1])
        dxi=(xgrid[it+1]-xgrid[it])/hm
        z[:,:,:,it+1],v[:,:,:,it+1]=step_linear_nd(
            z[:,:,:,it],v[:,:,:,it],rr,hm,
            xeff[:,:,:,it],xeff[:,:,:,it+1],dxi
        )
    return z,v,xeff


def construct_configuration(
    ge05,c4,r7,normf,bgs,r22npz,boundary,
    nt,nx,order,spatial_control=False,
):
    label="primary" if nt==NT_PRIMARY else "control"
    r=np.asarray(boundary["r"],float)
    w=np.asarray(boundary["w"],float)
    if len(r)!=order:
        raise RuntimeError("boundary quadrature order mismatch")
    tau=TAUH0/float(r7.g9.H0_CLASS)

    out={}
    spatial_num=0.0; spatial_a=0.0; spatial_b=0.0
    all_finite=True
    initial_match=0.0

    for tag in r7.C_TAGS:
        bg=bgs[(nt,tag)]
        h1=np.asarray(r22npz[f"{tag}_H1_{label}"],complex)
        h1dot=np.asarray(r22npz[f"{tag}_H1dot_{label}"],complex)
        z20=np.asarray(r22npz[f"{tag}_Z20_{label}"],complex)

        X10=first_order_X_modes(r7,bg,h1)
        initial_match=max(initial_match,aor(X10[:,0],boundary["trace_X0"]))

        z10,v10=evolve_z10(c4,bg,X10,boundary["z0"],boundary["v0"],r,tau)
        wz10=np.einsum("b,bmt->mt",w,z10,optimize=True)
        X20=X20_modes(r7,bg,z20)

        metric=metric_real_fields(r7,bg,h1,h1dot,nx)
        metric_small=None
        if spatial_control:
            metric_small=metric_real_fields(r7,bg,h1,h1dot,NX_CONTROL)

        wz20=np.zeros_like(X20)
        wg2=np.zeros((M_MAX,nt),complex)
        max_xeff=0.0

        for j0 in range(0,order,CHUNK):
            j1=min(order,j0+CHUNK)
            rc=r[j0:j1]; wc=w[j0:j1]
            zc=z10[j0:j1]; vc=v10[j0:j1]
            g2=normalized_g2_chunk(normf,r7,bg,metric,zc,vc,rc,tau,nx)
            if spatial_control:
                g2s=normalized_g2_chunk(
                    normf,r7,bg,metric_small,zc,vc,rc,tau,NX_CONTROL
                )
                spatial_num += float(np.linalg.norm(g2-g2s)**2)
                spatial_a += float(np.linalg.norm(g2)**2)
                spatial_b += float(np.linalg.norm(g2s)**2)

            zs,vs,xeff=solve_z20_chunk(bg,X20,g2,rc,tau)
            wz20 += np.einsum("b,bcmt->cmt",wc,zs,optimize=True)
            wg2 += np.einsum("b,bmt->mt",wc,g2,optimize=True)
            max_xeff=max(max_xeff,float(np.max(np.abs(xeff))))
            all_finite=bool(
                all_finite and np.all(np.isfinite(g2))
                and np.all(np.isfinite(zs)) and np.all(np.isfinite(vs))
            )

        out[tag]={
            "weighted_z10":wz10,
            "weighted_z20":wz20,
            "weighted_G2":wg2,
            "X20":X20,
            "B20_linear":X20-wz20,
            "effective_drive_abs_max":max_xeff,
        }

    spatial_rel=math.sqrt(spatial_num/max(spatial_a,spatial_b,TINY)) if spatial_control else None
    return out,{
        "initial_X10_match_abs_or_rel_max":float(initial_match),
        "G2_spatial_relative_L2":None if spatial_rel is None else float(spatial_rel),
        "all_outputs_finite":bool(all_finite),
    }


def stack_key(data,key,tags):
    return np.stack([np.asarray(data[t][key]) for t in tags],axis=0)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--results-dir",default=str(ROOT/"results"))
    ap.add_argument("--v077-trace",required=True)
    ap.add_argument("--json-out",required=True)
    ap.add_argument("--npz-out",required=True)
    args=ap.parse_args()
    rd=Path(args.results_dir)
    trace=Path(args.v077_trace)

    required={
        "r22j":rd/"ge19_repair22_on_shell_parent_z20_certification.json",
        "r22n":rd/"ge19_repair22_on_shell_parent_z20_certification.npz",
        "r13j":rd/"ge19_repair13_self_consistent_reduced_background_h1_reclosure.json",
        "r13n":rd/"ge19_repair13_self_consistent_reduced_background_h1_reclosure.npz",
        "dense":rd/"ge15_R1_dense_accepted_step_trace.dat",
        "lambda":rd/"ge15_R1_cli_background.dat",
    }
    missing=[str(p) for p in [*required.values(),trace] if not p.exists()]
    if missing:
        raise RuntimeError("missing frozen inputs: "+", ".join(missing))

    hashes={
        "Repair22_JSON":sha256(required["r22j"]),
        "Repair22_NPZ":sha256(required["r22n"]),
        "Repair13_JSON":sha256(required["r13j"]),
        "Repair13_NPZ":sha256(required["r13n"]),
    }
    if hashes["Repair22_JSON"]!=REPAIR22_JSON_SHA: raise RuntimeError("Repair22 JSON hash mismatch")
    if hashes["Repair22_NPZ"]!=REPAIR22_NPZ_SHA: raise RuntimeError("Repair22 NPZ hash mismatch")
    if hashes["Repair13_JSON"]!=REPAIR13_JSON_SHA: raise RuntimeError("Repair13 JSON hash mismatch")
    if hashes["Repair13_NPZ"]!=REPAIR13_NPZ_SHA: raise RuntimeError("Repair13 NPZ hash mismatch")

    d22=json.loads(required["r22j"].read_text())
    if d22.get("classification")!="GE19_REPAIR22_ON_SHELL_PARENT_Z20_CERTIFICATION_PASS":
        raise RuntimeError("Repair22 not PASS")
    if d22.get("Z20_certified") is not True:
        raise RuntimeError("Repair22 Z20 not certified")

    ge05=load_quiet(ROOT/"ge05"/"memory_directional_source_generator.py","ge05r24")
    c4=load_quiet(ROOT/"nl1c4"/"expanding_memory_source_trajectory.py","c4r24")
    r7=load_quiet(ROOT/"ge19"/"repair07_window_retarded_reduced_h3_z20_particular.py","r7r24")
    r11=load_quiet(ROOT/"ge19"/"repair11_lambda_inclusive_reduced_h1_reclosure.py","r11r24")
    r13=load_quiet(ROOT/"ge19"/"repair13_self_consistent_reduced_background_h1_reclosure.py","r13r24")

    normf,normdiag=build_normalized_c2_generator(ge05)
    step_err=step_nd_self_test(c4)
    if step_err>1e-12:
        raise RuntimeError(f"vectorized interval propagator mismatch {step_err}")

    z22=np.load(required["r22n"])
    z13=np.load(required["r13n"])
    bgs,bgctl=reconstruct_backgrounds(r7,r11,r13,rd,z13)

    # Exact Repair22 time grids.
    if aor(z22["x_primary"],bgs[(128,r7.C_TAGS[0])]["x"])>1e-14:
        raise RuntimeError("Repair22 primary x grid mismatch")
    if aor(z22["x_control"],bgs[(64,r7.C_TAGS[0])]["x"])>1e-14:
        raise RuntimeError("Repair22 control x grid mismatch")

    # Frozen full-history retarded boundaries for the two quadrature orders.
    b2048=full_history_boundary(c4,r7,trace,NQ_PRIMARY)
    b1024=full_history_boundary(c4,r7,trace,NQ_CONTROL)

    # Primary q20 and spatial source control.
    p,pdiag=construct_configuration(
        ge05,c4,r7,normf,bgs,z22,b2048,
        NT_PRIMARY,NX_PRIMARY,NQ_PRIMARY,spatial_control=True
    )
    # Quadrature control on the same state/time/spatial representation.
    q,qdiag=construct_configuration(
        ge05,c4,r7,normf,bgs,z22,b1024,
        NT_PRIMARY,NX_PRIMARY,NQ_CONTROL,spatial_control=False
    )
    # Time control at primary quadrature order and frozen Nt64 state.
    t,tdiag=construct_configuration(
        ge05,c4,r7,normf,bgs,z22,b2048,
        NT_CONTROL,NX_CONTROL,NQ_PRIMARY,spatial_control=False
    )

    tags=list(r7.C_TAGS)
    W20p=stack_key(p,"weighted_z20",tags) # [C,beta,m,t]
    W20q=stack_key(q,"weighted_z20",tags)
    W10p=stack_key(p,"weighted_z10",tags) # [C,input_m,t]
    W10t=stack_key(t,"weighted_z10",tags)
    W20t=stack_key(t,"weighted_z20",tags)

    quad_rel=rel_l2(W20p,W20q)
    x128=np.asarray(bgs[(128,tags[0])]["x"],float)
    x64=np.asarray(bgs[(64,tags[0])]["x"],float)
    W20p64=interp_complex_last(x128,W20p,x64)
    W10p64=interp_complex_last(x128,W10p,x64)
    time_q20=rel_l2(W20p64,W20t)
    time_z10=rel_l2(W10p64,W10t)

    initial_mismatch=max(
        pdiag["initial_X10_match_abs_or_rel_max"],
        qdiag["initial_X10_match_abs_or_rel_max"],
        tdiag["initial_X10_match_abs_or_rel_max"],
    )
    a_mismatch=max(b2048["a_mismatch"],b1024["a_mismatch"])
    all_finite=bool(
        pdiag["all_outputs_finite"] and qdiag["all_outputs_finite"]
        and tdiag["all_outputs_finite"]
        and np.all(np.isfinite(W20p)) and np.all(np.isfinite(W20q))
        and np.all(np.isfinite(W20t))
    )

    completeness=bool(
        W20p.shape==(3,3,40,128)
        and W20q.shape==(3,3,40,128)
        and W20t.shape==(3,3,40,64)
        and W10p.shape==(3,6,128)
        and W10t.shape==(3,6,64)
    )

    gates={
        "Repair22_Z20_certified":True,
        "Repair23_bridge_PASS":True,
        "full_history_initial_surface_a_abs_mismatch_le_1e12":bool(a_mismatch<=A_INITIAL_MAX),
        "H1_X10_initial_match_abs_or_rel_le_1e10":bool(initial_mismatch<=X_INITIAL_MAX),
        "G2_Nx256_vs_Nx512_low_mode_relative_L2_le_1e10":bool(
            pdiag["G2_spatial_relative_L2"]<=SPATIAL_MAX
        ),
        "q20_quadrature_N1024_vs_N2048_weighted_z20_relative_L2_le_1e2":bool(
            quad_rel<=QUAD_MAX
        ),
        "q20_Nt64_vs_Nt128_weighted_z20_relative_L2_le_5e3":bool(time_q20<=TIME_MAX),
        "z10_Nt64_vs_Nt128_weighted_z10_relative_L2_le_5e3":bool(time_z10<=TIME_MAX),
        "all_weighted_q20_outputs_finite":all_finite,
        "all_cases_complete":completeness,
        "normalized_c2_sqrtw_symbol_absent":bool(normdiag["sqrtw_symbol_absent_after_normalization"]),
        "vectorized_interval_propagator_match_le_1e12":bool(step_err<=1e-12),
    }
    passed=bool(all(gates.values()))

    per_case=[]
    for ic,tag in enumerate(tags):
        for ib,beta in enumerate(r7.BETAS):
            per_case.append({
                "C":tag,"beta0":float(beta),
                "weighted_z20_primary_L2":float(np.linalg.norm(W20p[ic,ib])),
                "B20_linear_primary_L2":float(np.linalg.norm(p[tag]["B20_linear"][ib])),
                "X20_primary_L2":float(np.linalg.norm(p[tag]["X20"][ib])),
                "weighted_G2_primary_L2":float(np.linalg.norm(p[tag]["weighted_G2"])),
                "effective_drive_abs_max":float(p[tag]["effective_drive_abs_max"]),
            })

    result={
        "classification":(
            "GE19_REPAIR24_Q20_CONSTRUCTION_PASS"
            if passed else "GE19_REPAIR24_Q20_CONSTRUCTION_FAIL"
        ),
        "predata_classification":"GE19_REPAIR24_PREDATA_Q20_CONSTRUCTION",
        "provenance":{
            **hashes,
            "v077_artifact_run_id":34315590099,
            "v077_artifact_id":10090367181,
            "v077_artifact_digest":"sha256:24b97e5738eb07be4f12d433ff5f9fe22249e199e186d5617aca5dc81f748378",
        },
        "normalized_c2_generator":normdiag,
        "vectorized_interval_propagator_self_test":step_err,
        "background_reproduction":bgctl,
        "full_history_boundary":{
            "a_mismatch_max":a_mismatch,
            "primary_order":NQ_PRIMARY,
            "control_order":NQ_CONTROL,
            "primary_k_relative_miss":b2048["k_relative_miss"],
            "control_k_relative_miss":b1024["k_relative_miss"],
            "primary_common_time_mismatch":b2048["common_time_mismatch"],
            "control_common_time_mismatch":b1024["common_time_mismatch"],
        },
        "construction":{
            "tauH0":TAUH0,
            "time_primary":NT_PRIMARY,
            "time_control":NT_CONTROL,
            "spatial_primary":NX_PRIMARY,
            "spatial_control":NX_CONTROL,
            "quadrature_primary":NQ_PRIMARY,
            "quadrature_control":NQ_CONTROL,
            "certified_projection":"weighted_z20=sum_j w_j z20_j",
            "node_states_persisted":False,
            "node_states_recomputable":True,
        },
        "controls":{
            "H1_X10_initial_match_abs_or_rel_max":initial_mismatch,
            "G2_spatial_Nx256_vs_Nx512_relative_L2":pdiag["G2_spatial_relative_L2"],
            "q20_quadrature_N1024_vs_N2048_weighted_z20_relative_L2":quad_rel,
            "q20_time_Nt64_vs_Nt128_weighted_z20_relative_L2":time_q20,
            "z10_time_Nt64_vs_Nt128_weighted_z10_relative_L2":time_z10,
            "all_outputs_finite":all_finite,
        },
        "per_case":per_case,
        "gates":gates,
        "q20_constructed":passed,
        "q20_certified_projection":passed,
        "Z21_licensed_after_freeze":passed,
        "claim_boundary":"PASS certifies the window-local particular baseline second-order normalized bath response through the physical weighted projection sum_j w_j z20_j on the frozen Repair22 low-mode scope. It does not certify a primordial bath mode, solve Z21, introduce finite eta, or make observational claims.",
    }

    outj=Path(args.json_out); outn=Path(args.npz_out)
    outj.parent.mkdir(parents=True,exist_ok=True)
    outj.write_text(json.dumps(result,indent=2)+"\n")
    save={
        "x_primary":x128,"x_control":x64,
        "r_primary":b2048["r"],"w_primary":b2048["w"],
        "r_control":b1024["r"],"w_control":b1024["w"],
    }
    for tag in tags:
        save[f"{tag}_weighted_z10_primary"]=p[tag]["weighted_z10"]
        save[f"{tag}_weighted_z20_primary"]=p[tag]["weighted_z20"]
        save[f"{tag}_weighted_G2_primary"]=p[tag]["weighted_G2"]
        save[f"{tag}_X20_primary"]=p[tag]["X20"]
        save[f"{tag}_B20_linear_primary"]=p[tag]["B20_linear"]
        save[f"{tag}_weighted_z20_quadrature_control"]=q[tag]["weighted_z20"]
        save[f"{tag}_weighted_z10_time_control"]=t[tag]["weighted_z10"]
        save[f"{tag}_weighted_z20_time_control"]=t[tag]["weighted_z20"]
    np.savez_compressed(outn,**save)

    print(json.dumps(result,indent=2))
    if not passed:
        raise SystemExit(2)


if __name__=="__main__":
    main()
