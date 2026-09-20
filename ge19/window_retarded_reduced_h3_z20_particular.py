#!/usr/bin/env python3
"""GE19 window-retarded reduced-H3 Z20 particular solve.

This is the first actual baseline H3 state solve in the controlled
plane-symmetric scalar sector:

    L_total Z20 = -Q_total(Z10,Z10) - 2 Y2[Z10].

It consumes the frozen GE15 R1 cancellation-free first-order metric/AeST
trace and the frozen GE18 Repair01 on-shell pressureless matter bridge.

The result is deliberately narrower than a cosmological second-order state:
it is the m=1..40 projection of one window-retarded particular solution on
0.2 <= z <= 1.5.  The homogeneous/primordial second-order solution is not
chosen here.
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
from scipy.interpolate import PchipInterpolator
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import splu

ROOT=Path(__file__).resolve().parents[1]
import sys
sys.path.insert(0,str(ROOT))

import ge09.repair01_dense_accepted_step_local_jet_bridge as g9
import nl1c4.expanding_memory_source_trajectory as c4

# Frozen theory/numerics.
KB=0.0665
CV=2.0-KB
K2=9500.0
Q0=1.0e-4
Z0=1.0e-17
A0_MPC_INV=4.1199352008117163e-5
BETAS=(1.0,0.5,0.1)
C_TAGS=("C_min","C_star","C_max")
C_VALUES={
    "C_min":2.566238549760586e-9,
    "C_star":2.568543329983919e-9,
    "C_max":2.5714842087496506e-9,
}
FOURIER_N=np.asarray([3,5,8,10,15,20],int)
PHASES=np.asarray([0.13,0.71,1.29,2.03,2.77,3.41],float)
M_SOLVE=np.arange(1,41,dtype=int)
NT_PRIMARY=64
NT_CONTROL=32
NX_PRIMARY=1024
NX_SPATIAL_CONTROL=2048
SOURCE_SPATIAL_MAX=5.0e-4
LINEAR_RES_MAX=1.0e-8
CONSTRAINT_MAX=1.0e-6
TIME_STATE_MAX=5.0e-3
GE15_GE18_METRIC_MAX=1.0e-10
GE18_NPZ_SHA="b6ccaf2257fbb09df701c43bc9a593a3f68238826277a510a0b3b531ea9fa6fe"
TINY=1.0e-300
FIELDS=("N20","S20","u20","phi20","T20","delta_varrho20")
EQS=("lapse","isotropic_spatial","aether_rapidity","scalar_phi","dust_potential","dust_density")
DYNAMIC_FIELD_INDEX=(1,2,3,4)  # S,u,phi,T
DYNAMIC_EQ_INDEX=(1,2,3,4)


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


def cosine(a,b)->float:
    aa=np.asarray(a).ravel(); bb=np.asarray(b).ravel()
    return float(np.real(np.vdot(aa,bb))/max(np.linalg.norm(aa)*np.linalg.norm(bb),TINY))


def load_frozen_generator(path:Path,name:str):
    """Load a frozen historical generator without touching repository results."""
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


def fd4_matrix(n:int,x0:float,x1:float)->np.ndarray:
    """Fourth-order first derivative on a uniform grid, including one-sided edges."""
    if n<6:
        raise ValueError("fd4 requires n>=6")
    h=(x1-x0)/(n-1)
    D=np.zeros((n,n),float)
    # Forward 5-point fourth-order.
    D[0,0:5]=np.asarray([-25,48,-36,16,-3],float)/(12*h)
    D[1,0:5]=np.asarray([-3,-10,18,-6,1],float)/(12*h)
    for i in range(2,n-2):
        D[i,i-2:i+3]=np.asarray([1,-8,0,8,-1],float)/(12*h)
    # Backward mirrors.
    D[-2,-5:]=np.asarray([-1,6,-18,10,3],float)/(12*h)
    D[-1,-5:]=np.asarray([3,-16,36,-48,25],float)/(12*h)
    return D


def interp_real(x0,y0,x):
    return np.asarray(PchipInterpolator(x0,np.asarray(y0,float),axis=-1,extrapolate=False)(x),float)


def interp_complex(x0,y0,x):
    yy=np.asarray(y0)
    re=PchipInterpolator(x0,yy.real,axis=-1,extrapolate=False)(x)
    im=PchipInterpolator(x0,yy.imag,axis=-1,extrapolate=False)(x)
    return np.asarray(re+1j*im,complex)


def reconstruct_modes(cos_coeff,sin_coeff,amplitudes,nx):
    """coeff shape [6,nt]; return [nt,nx] real field."""
    theta=2*np.pi*np.arange(nx,dtype=float)/nx
    out=np.zeros((cos_coeff.shape[1],nx),float)
    for i,m in enumerate(FOURIER_N):
        ph=m*theta+PHASES[i]
        out += amplitudes[i]*(cos_coeff[i,:,None]*np.cos(ph)[None,:]
                              +sin_coeff[i,:,None]*np.sin(ph)[None,:])
    return out


def spectral_dx(a,kfund):
    arr=np.asarray(a)
    nx=arr.shape[-1]
    m=np.fft.fftfreq(nx)*nx
    h=np.fft.fft(arr,axis=-1)
    return np.fft.ifft(1j*(kfund*m)[None,:]*h,axis=-1).real


def mask23(nx):
    m=np.fft.fftfreq(nx)*nx
    return (np.abs(m)<=nx/3.0+1e-12).astype(float)


def y2_source(chi,a,kfund,beta):
    """Full physical NL0C Y2 residual, shape [nt,nx]."""
    nt,nx=chi.shape
    h=np.fft.fft(chi,axis=1)
    mm=np.fft.fftfreq(nx)*nx
    gx=np.fft.ifft(1j*(kfund*mm)[None,:]*h,axis=1).real/a[:,None]
    flux=np.abs(gx)*gx
    fh=np.fft.fft(flux,axis=1)*mask23(nx)[None,:]
    div=np.fft.ifft(1j*(kfund*mm)[None,:]*fh,axis=1).real/a[:,None]
    return (2.0*(2.0-KB)/((1.0+beta)*A0_MPC_INV))*div


def fft_modes(arr,mmax=40):
    h=np.fft.fft(np.asarray(arr),axis=1)/arr.shape[1]
    return np.asarray(h[:,0:mmax+1],complex)


def build_ge15_reference(dense_path:Path,nt:int):
    rows=g9.read_table(dense_path)
    modes,kmiss=g9.group_modes(rows)
    interps=[g9.build_interps(m) for m in modes]
    x=np.linspace(math.log(g9.AMIN),math.log(g9.AMAX),nt)
    a=np.exp(x)
    state=[g9.eval_state(ip,x) for ip in interps]
    jets=[]
    for ik,k in enumerate(g9.K_REQ):
        c,s,d=g9.jet_from_state(state[ik],a,float(k))
        jets.append((c,s,d))
    # Background quantities should be common to all six mode traces.
    Hs=np.asarray([q["H_over_H0"] for q in state],float)
    Qs=np.asarray([q["Q"] for q in state],float)
    bg_mode_mismatch=max(aor(Hs[0],Hs[i]) for i in range(1,6))
    bg_mode_mismatch=max(bg_mode_mismatch,max(aor(Qs[0],Qs[i]) for i in range(1,6)))
    bg={
        "x":x,
        "a":a,
        "H":np.asarray(state[0]["H_over_H0"],float)*g9.H0_CLASS,
        "Q":np.asarray(state[0]["Q"],float),
        "bg_mode_mismatch":float(bg_mode_mismatch),
        "kmiss":float(kmiss),
    }
    return bg,state,jets


def jet_mode_arrays(jets,name):
    c=np.asarray([q[0][name] for q in jets],float)
    s=np.asarray([q[1][name] for q in jets],float)
    return c,s


def ge18_coeff(npz,tag,name,x):
    x0=np.asarray(npz["ln_a"],float)
    arr=np.asarray(npz[f"{tag}_{name}"],float)
    if np.array_equal(x,x0):
        return arr.copy()
    return interp_real(x0,arr,x)


def amplitudes():
    widths=c4.log_trap_weights(c4.K_H)
    PR=c4.AS*(g9.K_REQ/c4.KPIV_MPC)**(c4.NS-1.0)
    return np.sqrt(2.0*widths*PR),widths,PR


def build_first_order_real(bg,jets,npz,tag,nx):
    nt=len(bg["x"])
    amps,_,_=amplitudes()
    # Einstein+AeST local jet.
    ga={}
    for name in g9.JET_NAMES:
        cc,ss=jet_mode_arrays(jets,name)
        ga[name]=reconstruct_modes(cc,ss,amps,nx)

    # Matter directional local variables.
    zero=np.zeros((6,nt),float)
    matter={}
    cos_names=("dN","dL","dR","db","drho_action","dTt")
    for name in cos_names:
        cc=ge18_coeff(npz,tag,name,bg["x"])
        matter[name]=reconstruct_modes(cc,zero,amps,nx)
    ss=ge18_coeff(npz,tag,"dTx_sin",bg["x"])
    matter["dTx"]=reconstruct_modes(zero,ss,amps,nx)

    # chi is reconstructed from the certified GE06 jet:
    # px=-k varphi, u=-(k/a)alpha, chi=varphi+Q alpha.
    chi_cos=np.empty((6,nt),float)
    for ik,k in enumerate(g9.K_REQ):
        u_s=np.asarray(jets[ik][1]["u"],float)
        px_s=np.asarray(jets[ik][1]["px"],float)
        alpha=-bg["a"]*u_s/float(k)
        varphi=-px_s/float(k)
        chi_cos[ik]=varphi+bg["Q"]*alpha
    chi=reconstruct_modes(chi_cos,zero,amps,nx)
    return ga,matter,chi


def assemble_ga_local(pd,Dt,k=None,spatial_real=False,kfund=None):
    if spatial_real:
        dx=lambda q:spectral_dx(q,kfund)
    else:
        dx=lambda q:1j*k*q
    return {
        "N":pd["N_f"]-dx(pd["N_x"]),
        "L":pd["L_f"]-Dt@pd["L_t"]-dx(pd["L_x"]),
        "R":pd["R_f"]-Dt@pd["R_t"]-dx(pd["R_x"]),
        "b":pd["b_f"]-dx(pd["b_x"]),
        "u":pd["u_f"]-Dt@pd["u_t"]-dx(pd["u_x"]),
        "phi":-Dt@pd["phi_t"]-dx(pd["phi_x"]),
    }


def assemble_m_local(pd,Dt,k=None,spatial_real=False,kfund=None):
    if spatial_real:
        dx=lambda q:spectral_dx(q,kfund)
    else:
        dx=lambda q:1j*k*q
    return {
        "N":pd["N_f"],
        "L":pd["L_f"],
        "R":pd["R_f"],
        "b":pd["b_f"],
        "T":-Dt@pd["T_t"]-dx(pd["T_x"]),
        "rho":pd["rho_f"],
    }


def main_and_constraints(ga,ma):
    EN=ga["N"]+ma["N"]
    EL=ga["L"]+ma["L"]
    ER=ga["R"]+ma["R"]
    Eb=ga["b"]+ma["b"]
    main=np.stack([EN,EL+ER,ga["u"],ga["phi"],ma["T"],ma["rho"]],axis=0)
    con=np.stack([Eb,EL-0.5*ER],axis=0)
    return main,con


def source_real(mod6,mod7,bg,jets,npz,tag,beta,nx):
    nt=len(bg["x"])
    Dx=fd4_matrix(nt,bg["x"][0],bg["x"][-1])
    Dt=bg["H"][:,None]*Dx
    ga,matter,chi=build_first_order_real(bg,jets,npz,tag,nx)
    aa=bg["a"][:,None]
    adot=(bg["a"]*bg["H"])[:,None]
    Qb=bg["Q"][:,None]
    vals6=(aa,adot,Qb,
           ga["N"],ga["L"],ga["R"],ga["b"],ga["u"],
           ga["Lt"],ga["Lx"],ga["Rt"],ga["Rx"],ga["bx"],
           ga["ut"],ga["ux"],ga["pt"],ga["px"],ga["Nx"],
           KB,CV,K2,Q0,Z0)
    p6={name:fn(*vals6) for name,fn in mod6.f_c2.items()}
    q6=assemble_ga_local(p6,Dt,spatial_real=True,kfund=float(g9.K_REQ[0]/FOURIER_N[0]))

    rhob=(3.0*C_VALUES[tag]/bg["a"]**3)[:,None]
    vals7=(aa,rhob,matter["dN"],matter["dL"],matter["dR"],matter["db"],
           matter["drho_action"],matter["dTt"],matter["dTx"])
    p7={name:fn(*vals7) for name,fn in mod7.f_c2.items()}
    q7=assemble_m_local(p7,Dt,spatial_real=True,kfund=float(g9.K_REQ[0]/FOURIER_N[0]))

    qmain,qcon=main_and_constraints(q6,q7)
    y=y2_source(chi,bg["a"],float(g9.K_REQ[0]/FOURIER_N[0]),beta)
    rhs=-qmain
    rhs[3] += -2.0*y
    rhscon=-qcon

    # Separate source pieces for interpretation.
    zma={k:np.zeros_like(v) for k,v in q7.items()}
    zga={k:np.zeros_like(v) for k,v in q6.items()}
    qmain_ga,_=main_and_constraints(q6,zma)
    qmain_m,_=main_and_constraints(zga,q7)
    ypiece=np.zeros_like(qmain)
    ypiece[3]=-2.0*y
    return {
        "rhs":rhs,
        "rhs_constraint":rhscon,
        "Q_ga":-qmain_ga,
        "Q_matter":-qmain_m,
        "Y_H3":ypiece,
        "chi":chi,
    }


def linear_operator_batch(mod6,mod7,bg,tag,k,Y):
    """Apply gauge-fixed L_total to columns Y, shape [6,nt,ncol]."""
    nt=Y.shape[1]
    Dx=fd4_matrix(nt,bg["x"][0],bg["x"][-1])
    Dt=bg["H"][:,None]*Dx
    N,S,u,phi,T,drho=Y
    z=np.zeros_like(N)
    dS=Dt@S; du=Dt@u; dp=Dt@phi; dT=Dt@T
    ik=1j*k
    aa=bg["a"][:,None]
    adot=(bg["a"]*bg["H"])[:,None]
    Qb=bg["Q"][:,None]
    vals6=(aa,adot,Qb,
           N,S,S,z,u,
           dS,ik*S,dS,ik*S,z,
           du,ik*u,dp,ik*phi,ik*N,
           KB,CV,K2,Q0,Z0)
    p6={name:fn(*vals6) for name,fn in mod6.f_c1.items()}
    l6=assemble_ga_local(p6,Dt,k=k)

    rhob=(3.0*C_VALUES[tag]/bg["a"]**3)[:,None]
    vals7=(aa,rhob,N,S,S,z,drho,dT,ik*T)
    p7={name:fn(*vals7) for name,fn in mod7.f_c1.items()}
    l7=assemble_m_local(p7,Dt,k=k)
    return main_and_constraints(l6,l7)


def build_matrix(mod6,mod7,bg,tag,k):
    nt=len(bg["x"]); n=6*nt
    eye=np.eye(n,dtype=complex).reshape(6,nt,n)
    main,con=linear_operator_batch(mod6,mod7,bg,tag,k,eye)
    A=np.asarray(main,complex).reshape(n,n)
    C=np.asarray(con,complex).reshape(2*nt,n)

    Dx=fd4_matrix(nt,bg["x"][0],bg["x"][-1])
    Dt=bg["H"][:,None]*Dx
    # Replace the first two collocation rows of each dynamical equation by
    # value and first-cosmic-time-derivative homogeneous conditions.
    for vi,ei in zip(DYNAMIC_FIELD_INDEX,DYNAMIC_EQ_INDEX):
        r0=ei*nt+0
        r1=ei*nt+1
        A[r0,:]=0.0
        A[r0,vi*nt+0]=1.0
        A[r1,:]=0.0
        A[r1,vi*nt:(vi+1)*nt]=Dt[0,:]
    return csr_matrix(A),csr_matrix(C)


def rhs_fourier(source,mmax=40):
    out={}
    for key in ("rhs","rhs_constraint","Q_ga","Q_matter","Y_H3"):
        arr=np.asarray(source[key],float)  # [eq,nt,nx]
        hh=np.fft.fft(arr,axis=2)/arr.shape[2]
        out[key]=np.asarray(hh[:,:,0:mmax+1],complex)
    return out


def apply_bc_rhs(B,nt):
    out=np.asarray(B,complex).copy()
    for ei in DYNAMIC_EQ_INDEX:
        out[ei*nt+0,:]=0.0
        out[ei*nt+1,:]=0.0
    return out


def solve_case(mod6,mod7,bg,tag,sources_by_beta):
    """Solve all beta RHS for each m with one LU per (C,m)."""
    nt=len(bg["x"])
    nb=len(BETAS)
    states=np.zeros((nb,len(M_SOLVE),6,nt),complex)
    solve_res=np.zeros((nb,len(M_SOLVE)),float)
    con_res=np.zeros((nb,len(M_SOLVE),2),float)
    for jm,m in enumerate(M_SOLVE):
        k=float(m*g9.K_REQ[0]/FOURIER_N[0])
        A,Cmat=build_matrix(mod6,mod7,bg,tag,k)
        B=np.empty((6*nt,nb),complex)
        BC=np.empty((2*nt,nb),complex)
        for ib,beta in enumerate(BETAS):
            ff=sources_by_beta[beta]["rhs"][:,:,m]
            fc=sources_by_beta[beta]["rhs_constraint"][:,:,m]
            B[:,ib]=ff.reshape(6*nt)
            BC[:,ib]=fc.reshape(2*nt)
        Bbc=apply_bc_rhs(B,nt)
        try:
            lu=splu(A.tocsc())
            X=lu.solve(Bbc)
        except Exception as exc:
            raise RuntimeError(f"sparse solve failed tag={tag} m={m}: {exc}") from exc
        for ib in range(nb):
            y=X[:,ib].reshape(6,nt)
            states[ib,jm]=y
            rr=A@X[:,ib]-Bbc[:,ib]
            solve_res[ib,jm]=np.linalg.norm(rr)/max(np.linalg.norm(A@X[:,ib]),np.linalg.norm(Bbc[:,ib]),TINY)
            cr=Cmat@X[:,ib]-BC[:,ib]
            for ic in range(2):
                sl=slice(ic*nt,(ic+1)*nt)
                lhs=(Cmat@X[:,ib])[sl]
                rhs=BC[sl,ib]
                con_res[ib,jm,ic]=np.linalg.norm(cr[sl])/max(np.linalg.norm(lhs),np.linalg.norm(rhs),TINY)
    return states,solve_res,con_res


def source_bundle(mod6,mod7,bg,jets,npz,tag,nx):
    out={}
    for beta in BETAS:
        out[beta]=rhs_fourier(source_real(mod6,mod7,bg,jets,npz,tag,beta,nx))
    return out


def interpolate_state_to(x0,state,x):
    # [beta,m,field,time]
    sh=state.shape[:-1]+(len(x),)
    out=np.empty(sh,complex)
    it=np.ndindex(state.shape[:-1])
    for idx in it:
        out[idx]=interp_complex(x0,state[idx],x)
    return out


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--results-dir",default=str(ROOT/"results"))
    ap.add_argument("--json-out",required=True)
    ap.add_argument("--npz-out",required=True)
    args=ap.parse_args()
    rd=Path(args.results_dir)
    required=[
        rd/"ge15_R1_dense_accepted_step_trace.dat",
        rd/"ge15_cancellation_free_s_state_precision_closure.json",
        rd/"ge18_repair01_on_shell_matched_dust_first_order_bridge.json",
        rd/"ge18_repair01_on_shell_matched_dust_first_order_bridge.npz",
    ]
    missing=[str(p) for p in required if not p.exists()]
    if missing:
        raise RuntimeError("missing frozen local inputs: "+", ".join(missing))

    ge15=json.loads((rd/"ge15_cancellation_free_s_state_precision_closure.json").read_text())
    ge18=json.loads((rd/"ge18_repair01_on_shell_matched_dust_first_order_bridge.json").read_text())
    if ge15.get("classification")!="GE15_CANCELLATION_FREE_S_STATE_PRECISION_CLOSURE_PASS":
        raise RuntimeError("GE15 parent is not PASS")
    if ge18.get("classification")!="GE18_REPAIR01_ON_SHELL_MATCHED_DUST_FIRST_ORDER_BRIDGE_PASS":
        raise RuntimeError("GE18 Repair01 parent is not PASS")
    dense=rd/"ge15_R1_dense_accepted_step_trace.dat"
    dense_sha=sha256(dense)
    dense_expected=ge15["precision_binding"]["dense_trace_sha256"]["R1"]
    ge18_npz_path=rd/"ge18_repair01_on_shell_matched_dust_first_order_bridge.npz"
    ge18_npz_sha=sha256(ge18_npz_path)
    npz=np.load(ge18_npz_path)

    mod6=load_frozen_generator(ROOT/"ge06"/"analytic_aest_directional_source_generator.py","ge19_ge06")
    mod7=load_frozen_generator(ROOT/"ge07"/"pressureless_matter_directional_source_generator.py","ge19_ge07")

    bg64,state64,jets64=build_ge15_reference(dense,NT_PRIMARY)
    bg32,state32,jets32=build_ge15_reference(dense,NT_CONTROL)

    # GE15/GE18 metric bridge check on native 64-node representation.
    metric_err=0.0
    for name,jetname in (("dN","N"),("dL","L"),("dR","R"),("db","b"),("dTt","N")):
        jj=np.asarray([jets64[i][0][jetname] for i in range(6)],float)
        if name=="db":
            # b is zero in both representations.
            jj=np.asarray([jets64[i][0]["b"] for i in range(6)],float)
        gg=np.asarray(npz[f"C_star_{name}"],float)
        metric_err=max(metric_err,aor(jj,gg))

    # First-order common physical amplitudes.
    amps,widths,PR=amplitudes()
    kfund=float(g9.K_REQ[0]/FOURIER_N[0])

    # Primary source at both spatial resolutions, for every matter/beta case.
    src1024={}; src2048={}
    spatial_rows=[]
    spatial_max=0.0
    all_sources_finite=True
    zero_mode_rows=[]
    source_piece_norms=[]
    for tag in C_TAGS:
        src1024[tag]=source_bundle(mod6,mod7,bg64,jets64,npz,tag,NX_PRIMARY)
        src2048[tag]=source_bundle(mod6,mod7,bg64,jets64,npz,tag,NX_SPATIAL_CONTROL)
        for beta in BETAS:
            a=src1024[tag][beta]["rhs"][:,:,1:41]
            b=src2048[tag][beta]["rhs"][:,:,1:41]
            e=rel_l2(a,b)
            spatial_max=max(spatial_max,e)
            spatial_rows.append({"C":tag,"beta0":beta,"relative_L2_m1_40":e})
            all_sources_finite=bool(all_sources_finite and np.all(np.isfinite(a)) and np.all(np.isfinite(b)))
            z0=src1024[tag][beta]["rhs"][:,:,0]
            zero_mode_rows.append({
                "C":tag,"beta0":beta,
                "m0_source_global_L2":float(np.linalg.norm(z0)),
            })
            qga=src1024[tag][beta]["Q_ga"][:,:,1:41]
            qm=src1024[tag][beta]["Q_matter"][:,:,1:41]
            yy=src1024[tag][beta]["Y_H3"][:,:,1:41]
            source_piece_norms.append({
                "C":tag,"beta0":beta,
                "analytic_Einstein_AeST_Q_L2":float(np.linalg.norm(qga)),
                "dust_Q_L2":float(np.linalg.norm(qm)),
                "Y_H3_L2":float(np.linalg.norm(yy)),
                "Y_over_analytic_plus_dust":float(np.linalg.norm(yy)/max(np.linalg.norm(qga+qm),TINY)),
                "Y_cosine_analytic_plus_dust":cosine(yy,qga+qm),
            })

    # Solve primary Nt=64.
    state64_by_C={}
    solve_max=0.0
    shift_max=0.0
    aniso_max=0.0
    solve_rows=[]
    for tag in C_TAGS:
        st,res,con=solve_case(mod6,mod7,bg64,tag,src1024[tag])
        state64_by_C[tag]=st
        solve_max=max(solve_max,float(np.max(res)))
        shift_max=max(shift_max,float(np.max(con[:,:,0])))
        aniso_max=max(aniso_max,float(np.max(con[:,:,1])))
        solve_rows.append({
            "C":tag,
            "linear_system_relative_L2_max":float(np.max(res)),
            "shift_constraint_relative_L2_max":float(np.max(con[:,:,0])),
            "anisotropy_constraint_relative_L2_max":float(np.max(con[:,:,1])),
        })

    # Independent time-grid control Nt=32, same Nx=1024.
    src32={}
    state32_by_C={}
    time_rows=[]
    time_max=0.0
    for tag in C_TAGS:
        src32[tag]=source_bundle(mod6,mod7,bg32,jets32,npz,tag,NX_PRIMARY)
        st32,res32,con32=solve_case(mod6,mod7,bg32,tag,src32[tag])
        state32_by_C[tag]=st32
        p32=interpolate_state_to(bg64["x"],state64_by_C[tag],bg32["x"])
        by_field={}
        for iv,name in enumerate(FIELDS):
            e=rel_l2(p32[:,:,iv,:],st32[:,:,iv,:])
            by_field[name]=e
            time_max=max(time_max,e)
        time_rows.append({"C":tag,"by_field_relative_L2":by_field,"max":max(by_field.values())})

    # C-envelope around central state, separately for each beta.
    envelope=[]
    for ib,beta in enumerate(BETAS):
        cs=state64_by_C["C_star"][ib]
        envelope.append({
            "beta0":beta,
            "C_min_vs_C_star_global_relative_L2":rel_l2(state64_by_C["C_min"][ib],cs),
            "C_max_vs_C_star_global_relative_L2":rel_l2(state64_by_C["C_max"][ib],cs),
        })

    # beta response around beta=1, central C only, descriptive.
    beta_rows=[]
    central=state64_by_C["C_star"]
    for ib,beta in enumerate(BETAS):
        beta_rows.append({
            "beta0":beta,
            "state_global_L2":float(np.linalg.norm(central[ib])),
            "relative_to_beta1":rel_l2(central[ib],central[0]),
            "cosine_to_beta1":cosine(central[ib],central[0]),
        })

    all_state_finite=bool(
        all(np.all(np.isfinite(v)) for v in state64_by_C.values())
        and all(np.all(np.isfinite(v)) for v in state32_by_C.values())
    )

    provenance={
        "GE15_parent_PASS":True,
        "GE18_repair01_parent_PASS":True,
        "GE15_R1_dense_sha256":dense_sha,
        "GE15_R1_dense_expected_sha256":dense_expected,
        "GE15_R1_dense_hash_exact":dense_sha==dense_expected,
        "GE18_repair01_npz_sha256":ge18_npz_sha,
        "GE18_repair01_npz_expected_sha256":GE18_NPZ_SHA,
        "GE18_repair01_npz_hash_exact":ge18_npz_sha==GE18_NPZ_SHA,
        "GE15_GE18_metric_bridge_abs_or_rel_max":metric_err,
        "GE15_background_mode_mismatch_max":max(bg64["bg_mode_mismatch"],bg32["bg_mode_mismatch"]),
        "requested_k_relative_miss_max":max(bg64["kmiss"],bg32["kmiss"]),
    }

    gates={
        "frozen_input_provenance_exact":bool(
            provenance["GE15_R1_dense_hash_exact"]
            and provenance["GE18_repair01_npz_hash_exact"]
            and provenance["requested_k_relative_miss_max"]<=1e-12
            and provenance["GE15_background_mode_mismatch_max"]<=1e-10
        ),
        "GE15_GE18_metric_bridge_abs_or_rel_le_1e10":bool(metric_err<=GE15_GE18_METRIC_MAX),
        "all_sources_finite":bool(all_sources_finite),
        "spatial_N1024_vs_N2048_source_m1_40_global_relative_L2_le_5e4":bool(spatial_max<=SOURCE_SPATIAL_MAX),
        "primary_linear_system_relative_L2_residual_le_1e8":bool(solve_max<=LINEAR_RES_MAX),
        "shift_constraint_relative_L2_le_1e6":bool(shift_max<=CONSTRAINT_MAX),
        "anisotropy_constraint_relative_L2_le_1e6":bool(aniso_max<=CONSTRAINT_MAX),
        "primary64_vs_control32_state_global_relative_L2_le_5e3":bool(time_max<=TIME_STATE_MAX),
        "all_three_beta0_and_C_cases_complete":bool(len(state64_by_C)==3 and all(v.shape[0]==3 for v in state64_by_C.values())),
        "all_outputs_finite":bool(all_state_finite),
        "no_homogeneous_full_species_finite_eta_or_physical_amplitude_claim":True,
    }
    passed=bool(all(gates.values()))
    classification=(
        "GE19_WINDOW_RETARDED_REDUCED_H3_Z20_PARTICULAR_PASS"
        if passed else
        "GE19_WINDOW_RETARDED_REDUCED_H3_Z20_PARTICULAR_FAIL"
    )

    result={
        "classification":classification,
        "predata_classification":"GE19_PREDATA_WINDOW_RETARDED_REDUCED_H3_Z20_PARTICULAR",
        "scope":"m=1..40 projection of one window-retarded reduced-matter baseline H3 directional particular state. Formal epsilon->0 coefficient only.",
        "equation":"L_total Z20 = -Q_total(Z10,Z10) - 2 Y2[Z10]",
        "provenance":provenance,
        "frozen_direction":{
            "k_h_per_Mpc":g9.K_H.tolist(),
            "integer_modes":FOURIER_N.tolist(),
            "phases_rad":PHASES.tolist(),
            "amplitudes_sqrt_2wPR":amps.tolist(),
            "log_trapezoid_weights":widths.tolist(),
            "primordial_PR":PR.tolist(),
            "kfund_Mpc_inv":kfund,
        },
        "gauge":{
            "conditions":["b20=0","L20=R20=S20"],
            "fields":list(FIELDS),
            "main_equations":list(EQS),
            "constraint_monitors":["shift","E_L-E_R/2"],
        },
        "window_retarded_convention":{
            "z_start":1.5,"z_end":0.2,
            "dynamic_fields":["S20","u20","phi20","T20"],
            "initial_conditions":"value=0 and cosmic-time derivative=0 at z=1.5",
            "meaning":"one window-local particular solution; primordial/earlier-time response remains in omitted homogeneous solution",
        },
        "source_spatial_convergence":{
            "primary_Nx":NX_PRIMARY,
            "control_Nx":NX_SPATIAL_CONTROL,
            "relative_L2_max":spatial_max,
            "rows":spatial_rows,
        },
        "source_decomposition":source_piece_norms,
        "unsolved_m0_source":zero_mode_rows,
        "primary_solve_controls":{
            "max_linear_system_relative_L2":solve_max,
            "max_shift_constraint_relative_L2":shift_max,
            "max_anisotropy_constraint_relative_L2":aniso_max,
            "rows":solve_rows,
        },
        "time_grid_control":{
            "primary_Nt":NT_PRIMARY,
            "control_Nt":NT_CONTROL,
            "state_relative_L2_max":time_max,
            "rows":time_rows,
        },
        "matter_background_envelope":envelope,
        "beta0_state_dependence":beta_rows,
        "external_reduced_matter_systematic_from_GE18":{
            "density_global_relative_L2":0.0013765302104657398,
            "momentum_global_relative_L2":0.006891936293682233,
            "included_in_C_envelope":False,
            "propagation_status":"not representable by an on-shell pressureless C variation; retained as an external reduced-model systematic"
        },
        "gates":gates,
        "project_boundary":{
            "window_retarded_reduced_H3_particular_certified":passed,
            "homogeneous_primordial_Z20_certified":False,
            "full_species_Z20_certified":False,
            "physical_amplitude_nonlinear_state_certified":False,
            "q20_ready_after_Z20":passed,
            "Z21_licensed":False,
        },
        "claim_boundary":"PASS certifies only the frozen low-mode window-retarded reduced-H3 particular directional state. It does not certify the omitted homogeneous/primordial second-order mode, full standard species, finite eta, physical-amplitude nonlinear evolution, collapse, halo/lensing or observations."
    }

    outj=Path(args.json_out); outj.parent.mkdir(parents=True,exist_ok=True)
    outj.write_text(json.dumps(result,indent=2,allow_nan=False)+"\n")

    save={
        "beta0":np.asarray(BETAS,float),
        "m":M_SOLVE,
        "field_names":np.asarray(FIELDS,dtype="U32"),
        "ln_a_primary":bg64["x"],
        "a_primary":bg64["a"],
        "ln_a_control":bg32["x"],
        "a_control":bg32["a"],
    }
    for tag in C_TAGS:
        save[f"{tag}_Z20_primary"]=state64_by_C[tag]
        save[f"{tag}_Z20_control"]=state32_by_C[tag]
        for ib,beta in enumerate(BETAS):
            bt=str(beta).replace(".","p")
            save[f"{tag}_beta{bt}_rhs_primary_m0_40"]=src1024[tag][beta]["rhs"]
            save[f"{tag}_beta{bt}_Qga_primary_m0_40"]=src1024[tag][beta]["Q_ga"]
            save[f"{tag}_beta{bt}_Qmatter_primary_m0_40"]=src1024[tag][beta]["Q_matter"]
            save[f"{tag}_beta{bt}_YH3_primary_m0_40"]=src1024[tag][beta]["Y_H3"]
    np.savez_compressed(args.npz_out,**save)

    print(json.dumps(result,indent=2,allow_nan=False))
    if not passed:
        raise SystemExit(2)


if __name__=="__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as exc:
        # Keep implementation failures distinct from science FAIL.
        print(json.dumps({
            "classification":"GE19_WINDOW_RETARDED_REDUCED_H3_Z20_PARTICULAR_IMPLEMENTATION_FAIL",
            "error":repr(exc),
        },indent=2))
        raise
