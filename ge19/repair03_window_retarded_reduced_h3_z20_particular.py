#!/usr/bin/env python3
"""GE19 Repair03 window-retarded reduced-H3 Z20 particular solve.

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
from types import SimpleNamespace

import sympy as sp

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




def canonicalize_exp_products(expr):
    """Combine only multiplicative exp factors, then normalize exponents exactly."""
    def norm_exp(node):
        if node.func is sp.exp:
            return sp.exp(sp.cancel(sp.expand(node.args[0])))
        return node

    out=[]
    for term in sp.Add.make_args(expr):
        t=sp.powsimp(term,force=True,combine="exp")
        t=t.replace(lambda z:z.func is sp.exp,norm_exp)
        t=sp.powsimp(t,force=True,combine="exp")
        t=t.replace(lambda z:z.func is sp.exp,norm_exp)
        out.append(t)
    return sp.Add(*out)


def symbolic_exp_audit(exprs,Zb,Q0_sym,Z0_sym):
    args=[]
    bad=[]
    for label,expr in exprs.items():
        for ex in sorted(expr.atoms(sp.exp),key=str):
            arg=sp.cancel(sp.expand(ex.args[0]))
            args.append((label,str(arg)))
            equivalent=bool(sp.cancel(sp.expand(arg-Zb**2))==0)
            q0_free=not arg.has(Q0_sym)
            z0_free=not arg.has(Z0_sym)
            if not (equivalent and q0_free and z0_free):
                bad.append({
                    "label":label,
                    "arg":str(arg),
                    "equivalent_to_Zb_squared":equivalent,
                    "contains_Q0":bool(arg.has(Q0_sym)),
                    "contains_Z0":bool(arg.has(Z0_sym)),
                })
    return {
        "exp_atom_count":len(args),
        "all_exp_args_equivalent_to_Zb_squared":len(bad)==0,
        "all_exp_args_Q0_free":all(not q0 for _,q0 in [(x["arg"],x["contains_Q0"]) for x in bad]) if bad else True,
        "all_exp_args_Z0_free":all(not z0 for _,z0 in [(x["arg"],x["contains_Z0"]) for x in bad]) if bad else True,
        "bad_exp_args":bad,
        "sample_exp_args":args[:20],
    }


def build_stable_ge06_generator(mod6):
    """Stable GE06 re-lambdification with frozen symbols and canonical Exp products."""
    frozen_args=tuple(mod6.direction_args)
    if len(frozen_args)!=23:
        raise RuntimeError(f"GE06 frozen direction_args length {len(frozen_args)} != 23")
    if not all(isinstance(s,sp.Symbol) for s in frozen_args):
        bad=[(i,type(s).__name__,repr(s)[:120]) for i,s in enumerate(frozen_args)
             if not isinstance(s,sp.Symbol)]
        raise RuntimeError(f"GE06 frozen direction_args contains non-symbols: {bad}")
    if len(set(frozen_args))!=len(frozen_args):
        raise RuntimeError("GE06 frozen direction_args contains duplicate symbols")

    Zb=sp.symbols("Zb",positive=True,real=True)
    stable_args=(frozen_args[0],frozen_args[1],Zb,*frozen_args[3:])
    if len(stable_args)!=23:
        raise RuntimeError(f"stable direction_args length {len(stable_args)} != 23")
    if not all(isinstance(s,sp.Symbol) for s in stable_args):
        bad=[(i,type(s).__name__,repr(s)[:120]) for i,s in enumerate(stable_args)
             if not isinstance(s,sp.Symbol)]
        raise RuntimeError(f"stable direction_args contains non-symbols: {bad}")
    if len(set(stable_args))!=len(stable_args):
        raise RuntimeError("stable direction_args contains duplicate symbols")

    eps=mod6.eps
    if not isinstance(eps,sp.Symbol):
        raise RuntimeError(f"GE06 eps is not symbolic: {type(eps).__name__}")

    dpt_sym=frozen_args[15]
    Q0_sym=frozen_args[21]
    Z0_sym=frozen_args[22]

    expansion=dict(mod6.expansion)
    pt_keys=[k for k in expansion if isinstance(k,sp.Symbol) and k.name=="pt"]
    if len(pt_keys)!=1:
        raise RuntimeError(f"expected exactly one symbolic pt key in frozen expansion, found {len(pt_keys)}")
    expansion[pt_keys[0]]=Q0_sym+Z0_sym*Zb+eps*dpt_sym

    coeff1={}
    coeff2={}
    for key,expr in mod6.partial_map.items():
        ee=expr.subs(expansion)
        raw1=sp.diff(ee,eps).subs(eps,0)
        raw2=sp.diff(ee,eps,2).subs(eps,0)
        coeff1[key]=canonicalize_exp_products(raw1)
        coeff2[key]=canonicalize_exp_products(raw2)

    audit1=symbolic_exp_audit(coeff1,Zb,Q0_sym,Z0_sym)
    audit2=symbolic_exp_audit(coeff2,Zb,Q0_sym,Z0_sym)
    if not (
        audit1["all_exp_args_equivalent_to_Zb_squared"]
        and audit1["all_exp_args_Q0_free"]
        and audit1["all_exp_args_Z0_free"]
        and audit2["all_exp_args_equivalent_to_Zb_squared"]
        and audit2["all_exp_args_Q0_free"]
        and audit2["all_exp_args_Z0_free"]
    ):
        raise RuntimeError(f"stable GE06 exponential canonicalization audit failed: c1={audit1} c2={audit2}")

    f1={k:sp.lambdify(stable_args,v,"numpy",cse=False) for k,v in coeff1.items()}
    f2={k:sp.lambdify(stable_args,v,"numpy",cse=False) for k,v in coeff2.items()}
    return SimpleNamespace(
        f_c1=f1,
        f_c2=f2,
        coeff1_expr=coeff1,
        coeff2_expr=coeff2,
        Zb_symbol=Zb,
        frozen_symbol_contract={
            "frozen_args_length":len(frozen_args),
            "stable_args_length":len(stable_args),
            "all_frozen_args_symbols":True,
            "all_stable_args_symbols":True,
            "frozen_args_unique":True,
            "stable_args_unique":True,
            "frozen_arg_names":[s.name for s in frozen_args],
            "stable_arg_names":[s.name for s in stable_args],
        },
        symbolic_exp_audit={"c1":audit1,"c2":audit2},
    )


def ge06_physical_parameter_probe(stable):
    """Overflow-only probe at the frozen physical parameter scales."""
    aa=np.asarray([0.4,0.55,0.7,1.0/1.2],float)
    adot=np.asarray([1.0e-4,9.0e-5,8.0e-5,7.0e-5],float)
    Zb=np.asarray([0.01,0.1,0.5,1.0],float)
    base=np.asarray([2.0e-3,-1.5e-3,1.0e-3,-5.0e-4],float)
    vals=(
        aa,adot,Zb,
        1.0*base,0.8*base,0.7*base,0.3*base,1.2*base,
        2.0e-7*base,3.0e-4*base,1.8e-7*base,2.5e-4*base,2.0e-4*base,
        1.1e-7*base,2.2e-4*base,
        0.2*Z0*base,2.5e-4*base,2.0e-4*base,
        KB,CV,K2,Q0,Z0,
    )
    out={}
    for label,fnmap in (("c1",stable.f_c1),("c2",stable.f_c2)):
        bad=[]
        maxabs=0.0
        for name,fn in fnmap.items():
            v=np.asarray(fn(*vals),float)
            if not np.all(np.isfinite(v)):
                bad.append(name)
            if v.size and np.any(np.isfinite(v)):
                maxabs=max(maxabs,float(np.nanmax(np.abs(v[np.isfinite(v)]))))
        out[label]={
            "all_partials_finite":len(bad)==0,
            "nonfinite_partials":bad,
            "finite_max_abs":maxabs,
        }
    return out

def ge06_stable_benign_equivalence(mod6,stable):
    """Compare stable re-expression to the frozen GE06 benign audit regime."""
    T,X,dt,dx,a,adot,qb,direction=mod6.deterministic_grid()
    loc=mod6.direction_locals(direction,dt,dx)
    Zb=(np.asarray(qb,float)-mod6.Q0V)/mod6.Z0V
    vals=(
        a,adot,Zb,*loc,
        mod6.KBV,mod6.CV,mod6.K2V,mod6.Q0V,mod6.Z0V,
    )
    p1={k:fn(*vals) for k,fn in stable.f_c1.items()}
    p2={k:fn(*vals) for k,fn in stable.f_c2.items()}
    s1=mod6.assemble(p1,dt,dx,direction["N"].shape)
    s2=mod6.assemble(p2,dt,dx,direction["N"].shape)
    f1,f2=mod6.analytic_sources(a,adot,qb,direction,dt,dx)
    names=mod6.SOURCE_NAMES
    v1=np.concatenate([np.asarray(s1[k],float).ravel() for k in names])
    w1=np.concatenate([np.asarray(f1[k],float).ravel() for k in names])
    v2=np.concatenate([np.asarray(s2[k],float).ravel() for k in names])
    w2=np.concatenate([np.asarray(f2[k],float).ravel() for k in names])
    return {
        "coeff1_source_global_relative_L2":rel_l2(v1,w1),
        "coeff2_source_global_relative_L2":rel_l2(v2,w2),
        "all_stable_outputs_finite":bool(np.all(np.isfinite(v1)) and np.all(np.isfinite(v2))),
    }


def eval_stable_partials(fnmap,vals,shape,label):
    out={}
    for name,fn in fnmap.items():
        v=np.broadcast_to(np.asarray(fn(*vals)),shape).copy()
        if not np.all(np.isfinite(v)):
            raise RuntimeError(f"non-finite stable GE06 partial {label}:{name}")
        out[name]=v
    return out


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



def positive_mode_coeff(cos_coeff,sin_coeff,amp,phase):
    """FFT +m coefficient for amp[c cos(m theta+phase)+s sin(...)]."""
    return 0.5*float(amp)*(np.asarray(cos_coeff)-1j*np.asarray(sin_coeff))*np.exp(1j*float(phase))


def reconstruct_positive_modes(coeff,nx):
    """coeff shape [6,nt] for positive modes; return real [nt,nx]."""
    coeff=np.asarray(coeff,complex)
    theta=2*np.pi*np.arange(nx,dtype=float)/nx
    out=np.zeros((coeff.shape[1],nx),float)
    for i,m in enumerate(FOURIER_N):
        out += 2.0*np.real(coeff[i,:,None]*np.exp(1j*m*theta)[None,:])
    return out


def ge15_frozen_npz_jet_error(npz_path,bg,jets):
    """Compare reconstructed GE15 R1 64-node jet against its frozen NPZ."""
    d=np.load(npz_path)
    x=np.asarray(d["ln_a"],float)
    if x.shape!=bg["x"].shape or aor(x,bg["x"])>1e-14:
        return math.inf
    err=0.0
    for name in g9.JET_NAMES:
        cc,ss=jet_mode_arrays(jets,name)
        err=max(err,aor(cc,np.asarray(d[f"R1_cos_{name}"],float)))
        err=max(err,aor(ss,np.asarray(d[f"R1_sin_{name}"],float)))
    return float(err)


def reference_reduced_mode_state(bg,jets,npz,tag):
    """Frozen mixed GE15+GE18 first-order reference in +m Fourier coefficients.

    Returns state [input_mode,field,time] and dynamic cosmic-time derivatives
    [input_mode,dynamic_field,time] for S,u,phi,T.
    """
    nt=len(bg["x"])
    amps,_,_=amplitudes()
    state=np.zeros((len(FOURIER_N),6,nt),complex)
    dot=np.zeros((len(FOURIER_N),4,nt),complex)
    z=np.zeros(nt,float)

    Tcos=ge18_coeff(npz,tag,"T_cos",bg["x"])
    drcos=ge18_coeff(npz,tag,"drho_action",bg["x"])
    Ttcos=ge18_coeff(npz,tag,"dTt",bg["x"])

    for ik in range(len(FOURIER_N)):
        amp=amps[ik]; ph=PHASES[ik]
        jc,js,diag=jets[ik]

        state[ik,0]=positive_mode_coeff(jc["N"],js["N"],amp,ph)
        state[ik,1]=positive_mode_coeff(jc["L"],js["L"],amp,ph)
        state[ik,2]=positive_mode_coeff(jc["u"],js["u"],amp,ph)
        state[ik,3]=positive_mode_coeff(np.asarray(diag["varphi"],float),z,amp,ph)
        state[ik,4]=positive_mode_coeff(Tcos[ik],z,amp,ph)
        state[ik,5]=positive_mode_coeff(drcos[ik],z,amp,ph)

        dot[ik,0]=positive_mode_coeff(jc["Lt"],js["Lt"],amp,ph)
        dot[ik,1]=positive_mode_coeff(jc["ut"],js["ut"],amp,ph)
        dot[ik,2]=positive_mode_coeff(jc["pt"],js["pt"],amp,ph)
        dot[ik,3]=positive_mode_coeff(Ttcos[ik],z,amp,ph)

    return state,dot


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



def exp_Z_from_KQ(KQ):
    """Stable positive Exp coordinate solving KQ/(4 K2 Z0)=Z exp(Z^2).

    This is the same y=Z^2 Newton equation used by pinned CLASS.
    """
    arr=np.asarray(KQ,float)
    out=np.empty_like(arr)
    it=np.nditer(arr,flags=["multi_index"])
    while not it.finished:
        kval=float(it[0])
        x=kval/(4.0*K2*Z0)
        if not (x>0.0 and math.isfinite(x)):
            raise RuntimeError(f"invalid Exp KQ coordinate x={x}")
        L=math.log(x)
        if x<1.0e-4:
            y=x*x
        else:
            y=L if L>1.0 else x*x
            y=max(y,1.0e-30)
        for _ in range(50):
            f=y+0.5*math.log(y)-L
            fp=1.0+0.5/y
            yn=y-f/fp
            if not (yn>0.0 and math.isfinite(yn)):
                yn=0.5*y
            if abs(yn-y)<2.0e-14*(1.0+y):
                y=yn
                break
            y=yn
        out[it.multi_index]=math.sqrt(y)
        it.iternext()
    return out


def stable_exp_background_from_native(modes,a_grid):
    """Reconstruct the physical Exp background from native accepted rows.

    CLASS conserves K_Q a^3=I0.  We infer I0 from the frozen native
    background state, then evaluate the same positive Exp branch without
    subtracting nearly equal Q and Q0 values.
    """
    native=[
        r for r in modes[0]
        if g9.AMIN-1e-14<=r["a"]<=g9.AMAX+1e-14
    ]
    if len(native)<8:
        raise RuntimeError("insufficient native GE15 background rows for stable Exp reconstruction")

    an=np.asarray([r["a"] for r in native],float)
    qn=np.asarray([r["Q"] for r in native],float)
    rn=np.asarray([r["rho_dark"] for r in native],float)
    pn=np.asarray([r["p_dark"] for r in native],float)
    cn=np.asarray([r["cad2_dark"] for r in native],float)

    kqn=3.0*(rn+pn)/qn
    i0_samples=an**3*kqn
    i0=float(np.median(i0_samples))
    i0_rel=float(np.linalg.norm(i0_samples-i0)/max(np.linalg.norm(i0_samples),TINY))

    def evaluate(a):
        a=np.asarray(a,float)
        kq=i0/a**3
        Z=exp_Z_from_KQ(kq)
        y=Z*Z
        x=kq/(4.0*K2*Z0)
        ex=x/Z
        q=Q0+Z0*Z
        kval=2.0*K2*Z0*Z0*(ex-1.0)
        kqq=4.0*K2*ex*(1.0+2.0*y)
        rho=(q*kq-kval)/3.0
        p=kval/3.0
        cad2=kq/(q*kqq)
        return {
            "Z":Z,"Q":q,"KQ":kq,"K":kval,"KQQ":kqq,
            "rho":rho,"p":p,"cad2":cad2,
        }

    nat=evaluate(an)
    native_diag={
        "native_rows":len(native),
        "I0_median":i0,
        "I0_samples_global_relative_L2_about_median":i0_rel,
        "rho_dark_reconstruction_global_relative_L2":rel_l2(nat["rho"],rn),
        "p_dark_reconstruction_global_relative_L2":rel_l2(nat["p"],pn),
        "cad2_dark_reconstruction_global_relative_L2":rel_l2(nat["cad2"],cn),
        "Q_trace_vs_action_abs_max":float(np.max(np.abs(qn-nat["Q"]))),
        "naive_trace_Z_abs_max":float(np.max(np.abs((qn-Q0)/Z0))),
        "stable_Z_min":float(np.min(nat["Z"])),
        "stable_Z_max":float(np.max(nat["Z"])),
    }
    native_gates={
        "all_stable_background_values_finite":bool(
            all(np.all(np.isfinite(v)) for v in nat.values())
        ),
        "Z_positive":bool(np.all(nat["Z"]>0.0)),
        "I0_samples_global_relative_L2_about_median_le_1e10":bool(i0_rel<=1e-10),
        "rho_dark_native_reconstruction_global_relative_L2_le_1e10":bool(
            native_diag["rho_dark_reconstruction_global_relative_L2"]<=1e-10
        ),
        "p_dark_native_reconstruction_global_relative_L2_le_1e8":bool(
            native_diag["p_dark_reconstruction_global_relative_L2"]<=1e-8
        ),
        "cad2_dark_native_reconstruction_global_relative_L2_le_1e8":bool(
            native_diag["cad2_dark_reconstruction_global_relative_L2"]<=1e-8
        ),
    }
    grid=evaluate(np.asarray(a_grid,float))
    if not all(np.all(np.isfinite(v)) for v in grid.values()):
        raise RuntimeError("non-finite stable Exp background on collocation grid")
    return grid,native_diag,native_gates


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

    stable,native_diag,native_gates=stable_exp_background_from_native(modes,a)
    bg={
        "x":x,
        "a":a,
        "H":np.asarray(state[0]["H_over_H0"],float)*g9.H0_CLASS,
        "Q":np.asarray(state[0]["Q"],float),
        "Q_action":np.asarray(stable["Q"],float),
        "KQ_action":np.asarray(stable["KQ"],float),
        "KQQ_action":np.asarray(stable["KQQ"],float),
        "Z_action":np.asarray(stable["Z"],float),
        "stable_exp_native_diagnostic":native_diag,
        "stable_exp_native_gates":native_gates,
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


def broadcast_partials(pd,shape):
    return {k:np.broadcast_to(np.asarray(v),shape).copy() for k,v in pd.items()}


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



def solve_reduced_h1_case(mod6,mod7,bg,tag,reference,reference_dot):
    """Solve L_total Z10_reduced=0 on the six frozen input modes."""
    nt=len(bg["x"])
    Dx=fd4_matrix(nt,bg["x"][0],bg["x"][-1])
    Dt=bg["H"][:,None]*Dx
    state=np.zeros((len(FOURIER_N),6,nt),complex)
    sys_res=[]
    shift_res=[]
    aniso_res=[]
    initial_err=[]

    for ik,m in enumerate(FOURIER_N):
        k=float(m*g9.K_REQ[0]/FOURIER_N[0])
        A,_=build_matrix(mod6,mod7,bg,tag,k)
        B=np.zeros(6*nt,complex)

        # build_matrix already replaced these rows with value / dt conditions.
        for jd,(vi,ei) in enumerate(zip(DYNAMIC_FIELD_INDEX,DYNAMIC_EQ_INDEX)):
            B[ei*nt+0]=reference[ik,vi,0]
            B[ei*nt+1]=reference_dot[ik,jd,0]

        try:
            lu=splu(A.tocsc())
            X=lu.solve(B)
        except Exception as exc:
            raise RuntimeError(f"reduced H1 sparse solve failed C={tag} m={m}: {exc}") from exc

        y=X.reshape(6,nt)
        state[ik]=y
        rr=A@X-B
        sys_res.append(
            np.linalg.norm(rr)/max(np.linalg.norm(A@X),np.linalg.norm(B),TINY)
        )

        # Native main/constraint operator, with separate blocks for a
        # cancellation-safe constraint normalization.
        main,con,mga,cga,mm,cm=linear_operator_batch(
            mod6,mod7,bg,tag,k,y[:,:,None],return_parts=True
        )
        for ic,store in ((0,shift_res),(1,aniso_res)):
            num=np.linalg.norm(con[ic,:,0])
            den=max(
                np.linalg.norm(cga[ic,:,0]),
                np.linalg.norm(cm[ic,:,0]),
                TINY,
            )
            store.append(float(num/den))

        for jd,vi in enumerate(DYNAMIC_FIELD_INDEX):
            initial_err.append(aor([y[vi,0]],[reference[ik,vi,0]]))
            dyi=Dt@y[vi]
            initial_err.append(aor([dyi[0]],[reference_dot[ik,jd,0]]))

    return state,{
        "linear_system_relative_L2_max":float(max(sys_res,default=math.inf)),
        "shift_constraint_relative_L2_max":float(max(shift_res,default=math.inf)),
        "anisotropy_constraint_relative_L2_max":float(max(aniso_res,default=math.inf)),
        "initial_dynamic_match_abs_or_rel_max":float(max(initial_err,default=math.inf)),
        "all_outputs_finite":bool(np.all(np.isfinite(state))),
    }


def reduced_h1_time_control(x64,state64,x32,state32):
    p64=interpolate_state_to(x64,state64,x32)
    by_field={}
    mx=0.0
    for iv,name in enumerate(FIELDS):
        e=rel_l2(p64[:,iv,:],state32[:,iv,:])
        by_field[name]=e
        mx=max(mx,e)
    return {"by_field_relative_L2":by_field,"max":float(mx)}


def mixed_reference_comparison(reduced,reference):
    by={}
    for iv,name in enumerate(FIELDS):
        by[name]=rel_l2(reduced[:,iv,:],reference[:,iv,:])
    return {"by_field_relative_L2":by,"max":float(max(by.values()))}


def reduced_state_real(bg,state,nx):
    """Reconstruct reduced Z10 and its local derivatives in real space."""
    nt=len(bg["x"])
    Dx=fd4_matrix(nt,bg["x"][0],bg["x"][-1])
    Dt=bg["H"][:,None]*Dx

    real={}
    dot={}
    for iv,name in enumerate(FIELDS):
        coeff=np.asarray(state[:,iv,:],complex)
        real[name]=reconstruct_positive_modes(coeff,nx)
        dcoeff=np.asarray([Dt@coeff[ik] for ik in range(len(FOURIER_N))],complex)
        dot[name]=reconstruct_positive_modes(dcoeff,nx)

    kfund=float(g9.K_REQ[0]/FOURIER_N[0])
    spatial={name:spectral_dx(real[name],kfund) for name in FIELDS}
    return real,dot,spatial


def y2_source_from_reduced(bg,real,spatial,beta):
    """Exact directional NL0C source from X1=Q u1 + (partial_x phi1)/a."""
    a=bg["a"][:,None]
    X=bg["Q_action"][:,None]*real["u20"] + spatial["phi20"]/a
    flux=np.abs(X)*X
    kfund=float(g9.K_REQ[0]/FOURIER_N[0])
    div=spectral_dx(flux,kfund)/a
    return (2.0*(2.0-KB)/((1.0+beta)*A0_MPC_INV))*div


def source_real_reduced(mod6,mod7,bg,tag,beta,nx,reduced_state):
    """H3 source evaluated on the internally reclosed reduced H1 state."""
    nt=len(bg["x"])
    Dx=fd4_matrix(nt,bg["x"][0],bg["x"][-1])
    Dt=bg["H"][:,None]*Dx
    real,dot,spatial=reduced_state_real(bg,reduced_state,nx)

    N=real["N20"]; S=real["S20"]; u=real["u20"]; ph=real["phi20"]
    T=real["T20"]; dr=real["delta_varrho20"]
    z=np.zeros_like(N)
    aa=bg["a"][:,None]
    adot=(bg["a"]*bg["H"])[:,None]
    Zb=bg["Z_action"][:,None]

    vals6=(
        aa,adot,Zb,
        N,S,S,z,u,
        dot["S20"],spatial["S20"],
        dot["S20"],spatial["S20"],z,
        dot["u20"],spatial["u20"],
        dot["phi20"],spatial["phi20"],spatial["N20"],
        KB,CV,K2,Q0,Z0,
    )
    p6=eval_stable_partials(mod6.f_c2,vals6,N.shape,"c2")
    q6=assemble_ga_local(
        p6,Dt,spatial_real=True,
        kfund=float(g9.K_REQ[0]/FOURIER_N[0])
    )

    rhob=(3.0*C_VALUES[tag]/bg["a"]**3)[:,None]
    vals7=(
        aa,rhob,N,S,S,z,dr,dot["T20"],spatial["T20"]
    )
    p7={name:fn(*vals7) for name,fn in mod7.f_c2.items()}
    p7=broadcast_partials(p7,N.shape)
    q7=assemble_m_local(
        p7,Dt,spatial_real=True,
        kfund=float(g9.K_REQ[0]/FOURIER_N[0])
    )

    qmain,qcon=main_and_constraints(q6,q7)
    y=y2_source_from_reduced(bg,real,spatial,beta)
    rhs=-qmain
    rhs[3] += -2.0*y
    rhscon=-qcon

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
        "X1":bg["Q_action"][:,None]*real["u20"]+spatial["phi20"]/bg["a"][:,None],
    }


def source_real(mod6,mod7,bg,jets,npz,tag,beta,nx):
    nt=len(bg["x"])
    Dx=fd4_matrix(nt,bg["x"][0],bg["x"][-1])
    Dt=bg["H"][:,None]*Dx
    ga,matter,chi=build_first_order_real(bg,jets,npz,tag,nx)
    aa=bg["a"][:,None]
    adot=(bg["a"]*bg["H"])[:,None]
    Zb=bg["Z_action"][:,None]
    vals6=(aa,adot,Zb,
           ga["N"],ga["L"],ga["R"],ga["b"],ga["u"],
           ga["Lt"],ga["Lx"],ga["Rt"],ga["Rx"],ga["bx"],
           ga["ut"],ga["ux"],ga["pt"],ga["px"],ga["Nx"],
           KB,CV,K2,Q0,Z0)
    p6={name:fn(*vals6) for name,fn in mod6.f_c2.items()}
    p6=broadcast_partials(p6,ga["N"].shape)
    q6=assemble_ga_local(p6,Dt,spatial_real=True,kfund=float(g9.K_REQ[0]/FOURIER_N[0]))

    rhob=(3.0*C_VALUES[tag]/bg["a"]**3)[:,None]
    vals7=(aa,rhob,matter["dN"],matter["dL"],matter["dR"],matter["db"],
           matter["drho_action"],matter["dTt"],matter["dTx"])
    p7={name:fn(*vals7) for name,fn in mod7.f_c2.items()}
    p7=broadcast_partials(p7,matter["dN"].shape)
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


def linear_operator_batch(mod6,mod7,bg,tag,k,Y,return_parts=False):
    """Apply gauge-fixed L_total to columns Y, shape [6,nt,ncol].

    If return_parts=True, also return separately assembled Einstein+AeST and
    dust main/constraint blocks for cancellation diagnostics.
    """
    nt=Y.shape[1]
    Dx=fd4_matrix(nt,bg["x"][0],bg["x"][-1])
    Dt=bg["H"][:,None]*Dx
    N,S,u,phi,T,drho=Y
    z=np.zeros_like(N)
    dS=Dt@S; du=Dt@u; dp=Dt@phi; dT=Dt@T
    ik=1j*k
    aa=bg["a"][:,None]
    adot=(bg["a"]*bg["H"])[:,None]
    Qb=bg["Q_action"][:,None]
    vals6=(aa,adot,Qb,
           N,S,S,z,u,
           dS,ik*S,dS,ik*S,z,
           du,ik*u,dp,ik*phi,ik*N,
           KB,CV,K2,Q0,Z0)
    p6=eval_stable_partials(mod6.f_c1,vals6,N.shape,"c1")
    l6=assemble_ga_local(p6,Dt,k=k)

    rhob=(3.0*C_VALUES[tag]/bg["a"]**3)[:,None]
    vals7=(aa,rhob,N,S,S,z,drho,dT,ik*T)
    p7={name:fn(*vals7) for name,fn in mod7.f_c1.items()}
    p7=broadcast_partials(p7,N.shape)
    l7=assemble_m_local(p7,Dt,k=k)
    main,con=main_and_constraints(l6,l7)
    if return_parts:
        zma={kk:np.zeros_like(vv) for kk,vv in l7.items()}
        zga={kk:np.zeros_like(vv) for kk,vv in l6.items()}
        mga,cga=main_and_constraints(l6,zma)
        mm,cm=main_and_constraints(zga,l7)
        return main,con,mga,cga,mm,cm
    return main,con


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
                con_scale=max(np.linalg.norm(B[:,ib]),np.linalg.norm(lhs),np.linalg.norm(rhs),TINY)
                con_res[ib,jm,ic]=np.linalg.norm(cr[sl])/con_scale
    return states,solve_res,con_res


def source_bundle(mod6,mod7,bg,jets,npz,tag,nx):
    out={}
    for beta in BETAS:
        out[beta]=rhs_fourier(source_real(mod6,mod7,bg,jets,npz,tag,beta,nx))
    return out



def source_bundle_reduced(mod6,mod7,bg,tag,nx,reduced_state):
    out={}
    for beta in BETAS:
        out[beta]=rhs_fourier(
            source_real_reduced(mod6,mod7,bg,tag,beta,nx,reduced_state)
        )
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
        rd/"ge15_cancellation_free_s_state_precision_closure.npz",
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

    mod6_frozen=load_frozen_generator(ROOT/"ge06"/"analytic_aest_directional_source_generator.py","ge19_ge06")
    mod6=build_stable_ge06_generator(mod6_frozen)
    ge06_equivalence=ge06_stable_benign_equivalence(mod6_frozen,mod6)
    ge06_physical_probe=ge06_physical_parameter_probe(mod6)
    mod7=load_frozen_generator(ROOT/"ge07"/"pressureless_matter_directional_source_generator.py","ge19_ge07")

    bg64,state64,jets64=build_ge15_reference(dense,NT_PRIMARY)
    bg32,state32,jets32=build_ge15_reference(dense,NT_CONTROL)

    ge15_npz_path=rd/"ge15_cancellation_free_s_state_precision_closure.npz"
    ge15_jet_err=ge15_frozen_npz_jet_error(ge15_npz_path,bg64,jets64)

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

    # ------------------------------------------------------------------
    # Stage A: mandatory internally coupled reduced H1 reclosure.
    # ------------------------------------------------------------------
    ref64={}; refdot64={}; ref32={}; refdot32={}
    h1_64={}; h1_32={}
    h1_rows=[]
    h1_time_rows=[]
    h1_reference_rows=[]
    h1_sys_max=0.0
    h1_shift_max=0.0
    h1_aniso_max=0.0
    h1_init_max=0.0
    h1_time_max=0.0
    h1_finite=True

    for tag in C_TAGS:
        ref64[tag],refdot64[tag]=reference_reduced_mode_state(bg64,jets64,npz,tag)
        ref32[tag],refdot32[tag]=reference_reduced_mode_state(bg32,jets32,npz,tag)

        st64,ctl64=solve_reduced_h1_case(
            mod6,mod7,bg64,tag,ref64[tag],refdot64[tag]
        )
        st32,ctl32=solve_reduced_h1_case(
            mod6,mod7,bg32,tag,ref32[tag],refdot32[tag]
        )
        h1_64[tag]=st64
        h1_32[tag]=st32

        tc=reduced_h1_time_control(bg64["x"],st64,bg32["x"],st32)
        cmp=mixed_reference_comparison(st64,ref64[tag])
        h1_rows.append({"C":tag,"primary":ctl64,"control":ctl32})
        h1_time_rows.append({"C":tag,**tc})
        h1_reference_rows.append({"C":tag,**cmp})

        h1_sys_max=max(h1_sys_max,ctl64["linear_system_relative_L2_max"],ctl32["linear_system_relative_L2_max"])
        h1_shift_max=max(h1_shift_max,ctl64["shift_constraint_relative_L2_max"],ctl32["shift_constraint_relative_L2_max"])
        h1_aniso_max=max(h1_aniso_max,ctl64["anisotropy_constraint_relative_L2_max"],ctl32["anisotropy_constraint_relative_L2_max"])
        h1_init_max=max(h1_init_max,ctl64["initial_dynamic_match_abs_or_rel_max"],ctl32["initial_dynamic_match_abs_or_rel_max"])
        h1_time_max=max(h1_time_max,tc["max"])
        h1_finite=bool(h1_finite and ctl64["all_outputs_finite"] and ctl32["all_outputs_finite"])

    stage_A_gates={
        "linear_system_relative_L2_residual_le_1e8":bool(h1_sys_max<=1e-8),
        "shift_constraint_relative_L2_le_1e6":bool(h1_shift_max<=1e-6),
        "anisotropy_constraint_relative_L2_le_1e6":bool(h1_aniso_max<=1e-6),
        "primary64_vs_control32_state_global_relative_L2_le_5e3":bool(h1_time_max<=5e-3),
        "initial_dynamic_match_abs_or_rel_le_1e10":bool(h1_init_max<=1e-10),
        "all_outputs_finite":bool(h1_finite),
    }
    stage_A_pass=bool(all(stage_A_gates.values()))

    provenance={
        "GE15_parent_PASS":True,
        "GE18_repair01_parent_PASS":True,
        "GE15_R1_dense_sha256":dense_sha,
        "GE15_R1_dense_expected_sha256":dense_expected,
        "GE15_R1_dense_hash_exact":dense_sha==dense_expected,
        "GE15_R1_frozen_64node_jet_abs_or_rel_max":ge15_jet_err,
        "stable_exp_background_native_diagnostic":bg64["stable_exp_native_diagnostic"],
        "stable_exp_background_native_gates":bg64["stable_exp_native_gates"],
        "stable_GE06_benign_equivalence":ge06_equivalence,
        "stable_GE06_symbol_contract":mod6.frozen_symbol_contract,
        "stable_GE06_symbolic_exp_audit":mod6.symbolic_exp_audit,
        "stable_GE06_physical_parameter_probe":ge06_physical_probe,
        "GE18_repair01_npz_sha256":ge18_npz_sha,
        "GE18_repair01_npz_expected_sha256":GE18_NPZ_SHA,
        "GE18_repair01_npz_hash_exact":ge18_npz_sha==GE18_NPZ_SHA,
        "GE15_GE18_metric_bridge_abs_or_rel_max":metric_err,
        "GE15_background_mode_mismatch_max":max(bg64["bg_mode_mismatch"],bg32["bg_mode_mismatch"]),
        "requested_k_relative_miss_max":max(bg64["kmiss"],bg32["kmiss"]),
    }

    provenance_pass=bool(
        provenance["GE15_R1_dense_hash_exact"]
        and provenance["GE18_repair01_npz_hash_exact"]
        and provenance["requested_k_relative_miss_max"]<=1e-12
        and provenance["GE15_background_mode_mismatch_max"]<=1e-10
        and ge15_jet_err<=1e-10
        and metric_err<=GE15_GE18_METRIC_MAX
        and all(bg64["stable_exp_native_gates"].values())
        and all(bg32["stable_exp_native_gates"].values())
        and ge06_equivalence["all_stable_outputs_finite"]
        and ge06_equivalence["coeff1_source_global_relative_L2"]<=1e-10
        and ge06_equivalence["coeff2_source_global_relative_L2"]<=1e-10
        and ge06_physical_probe["c1"]["all_partials_finite"]
        and ge06_physical_probe["c2"]["all_partials_finite"]
    )

    # Amendment01 stop rule: do not construct or interpret H3 if reduced H1
    # is not internally on shell.
    if not (provenance_pass and stage_A_pass):
        result={
            "classification":"GE19_REPAIR03_WINDOW_RETARDED_REDUCED_H3_Z20_PARTICULAR_FAIL",
            "predata_classification":"GE19_PREDATA_WINDOW_RETARDED_REDUCED_H3_Z20_PARTICULAR",
            "predata_amendment":"GE19_PREDATA_AMENDMENT01_REDUCED_H1_RECLOSURE",
        "repair01_predata":"GE19_REPAIR01_PREDATA_STABLE_EXP_BACKGROUND_COORDINATE",
        "repair01_predata_amendment":"GE19_REPAIR01_PREDATA_AMENDMENT01_NATIVE_I0_RECONSTRUCTION",
        "repair01_predata_amendment02":"GE19_REPAIR01_PREDATA_AMENDMENT02_STABLE_SYMBOLIC_RELAMBDIFICATION",
        "repair02_predata":"GE19_REPAIR02_PREDATA_FROZEN_SYMBOL_TUPLE_CAPTURE",
        "repair03_predata":"GE19_REPAIR03_PREDATA_CANONICAL_EXP_PRODUCT_EVALUATION",
            "failure_stage":"Stage_A_reduced_H1_reclosure",
            "provenance":provenance,
            "stage_A_reduced_H1":{
                "controls":{
                    "max_linear_system_relative_L2":h1_sys_max,
                    "max_shift_constraint_relative_L2":h1_shift_max,
                    "max_anisotropy_constraint_relative_L2":h1_aniso_max,
                    "max_initial_dynamic_match_abs_or_rel":h1_init_max,
                    "primary64_vs_control32_state_global_relative_L2_max":h1_time_max,
                    "rows":h1_rows,
                    "time_grid_rows":h1_time_rows,
                    "reduced_vs_mixed_reference_descriptive":h1_reference_rows,
                },
                "gates":stage_A_gates,
                "pass":False,
            },
            "stop_rule_applied":True,
            "Z20_constructed":False,
            "claim_boundary":"Stage A failed or provenance failed, so amendment01 forbids construction or interpretation of Z20. No H3 threshold or model choice is changed."
        }
        outj=Path(args.json_out); outj.parent.mkdir(parents=True,exist_ok=True)
        outj.write_text(json.dumps(result,indent=2,allow_nan=False)+"\n")
        print(json.dumps(result,indent=2,allow_nan=False))
        raise SystemExit(2)

    # ------------------------------------------------------------------
    # Stage B: H3 source on Z10_reduced, then window-retarded Z20.
    # ------------------------------------------------------------------
    src1024={}; src2048={}
    spatial_rows=[]
    spatial_max=0.0
    all_sources_finite=True
    zero_mode_rows=[]
    source_piece_norms=[]
    for tag in C_TAGS:
        src1024[tag]=source_bundle_reduced(
            mod6,mod7,bg64,tag,NX_PRIMARY,h1_64[tag]
        )
        src2048[tag]=source_bundle_reduced(
            mod6,mod7,bg64,tag,NX_SPATIAL_CONTROL,h1_64[tag]
        )
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

    src32={}
    state32_by_C={}
    time_rows=[]
    time_max=0.0
    for tag in C_TAGS:
        src32[tag]=source_bundle_reduced(
            mod6,mod7,bg32,tag,NX_PRIMARY,h1_32[tag]
        )
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

    gates={
        "frozen_input_provenance_exact":bool(provenance_pass),
        "stable_Exp_background_native_reconstruction_all_gates":bool(
            all(bg64["stable_exp_native_gates"].values())
            and all(bg32["stable_exp_native_gates"].values())
        ),
        "stable_GE06_benign_coeff1_equivalence_global_relative_L2_le_1e10":bool(
            ge06_equivalence["coeff1_source_global_relative_L2"]<=1e-10
        ),
        "stable_GE06_benign_coeff2_equivalence_global_relative_L2_le_1e10":bool(
            ge06_equivalence["coeff2_source_global_relative_L2"]<=1e-10
        ),
        "stable_GE06_benign_outputs_finite":bool(
            ge06_equivalence["all_stable_outputs_finite"]
        ),
        "stable_GE06_symbolic_exp_c1_canonical":bool(
            mod6.symbolic_exp_audit["c1"]["all_exp_args_equivalent_to_Zb_squared"]
            and mod6.symbolic_exp_audit["c1"]["all_exp_args_Q0_free"]
            and mod6.symbolic_exp_audit["c1"]["all_exp_args_Z0_free"]
        ),
        "stable_GE06_symbolic_exp_c2_canonical":bool(
            mod6.symbolic_exp_audit["c2"]["all_exp_args_equivalent_to_Zb_squared"]
            and mod6.symbolic_exp_audit["c2"]["all_exp_args_Q0_free"]
            and mod6.symbolic_exp_audit["c2"]["all_exp_args_Z0_free"]
        ),
        "stable_GE06_physical_probe_c1_all_partials_finite":bool(
            ge06_physical_probe["c1"]["all_partials_finite"]
        ),
        "stable_GE06_physical_probe_c2_all_partials_finite":bool(
            ge06_physical_probe["c2"]["all_partials_finite"]
        ),
        "GE15_R1_reconstructed_jet_vs_frozen_64node_representation_abs_or_rel_le_1e10":bool(ge15_jet_err<=1e-10),
        "GE15_GE18_metric_bridge_abs_or_rel_le_1e10":bool(metric_err<=GE15_GE18_METRIC_MAX),
        "reduced_H1_stage_A_all_gates":bool(stage_A_pass),
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
        "GE19_REPAIR03_WINDOW_RETARDED_REDUCED_H3_Z20_PARTICULAR_PASS"
        if passed else
        "GE19_REPAIR03_WINDOW_RETARDED_REDUCED_H3_Z20_PARTICULAR_FAIL"
    )

    result={
        "classification":classification,
        "predata_classification":"GE19_PREDATA_WINDOW_RETARDED_REDUCED_H3_Z20_PARTICULAR",
        "predata_amendment":"GE19_PREDATA_AMENDMENT01_REDUCED_H1_RECLOSURE",
        "scope":"m=1..40 projection of one window-retarded reduced-matter baseline H3 directional particular state. Formal epsilon->0 coefficient only.",
        "equation":"L_total Z20 = -Q_total(Z10,Z10) - 2 Y2[Z10]",
        "provenance":provenance,
        "stage_A_reduced_H1":{
            "pass":stage_A_pass,
            "controls":{
                "max_linear_system_relative_L2":h1_sys_max,
                "max_shift_constraint_relative_L2":h1_shift_max,
                "max_anisotropy_constraint_relative_L2":h1_aniso_max,
                "max_initial_dynamic_match_abs_or_rel":h1_init_max,
                "primary64_vs_control32_state_global_relative_L2_max":h1_time_max,
                "rows":h1_rows,
                "time_grid_rows":h1_time_rows,
                "reduced_vs_mixed_reference_descriptive":h1_reference_rows,
            },
            "gates":stage_A_gates,
        },
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
            "reduced_H1_reclosure_certified":stage_A_pass,
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
        save[f"{tag}_Z10_reduced_primary"]=h1_64[tag]
        save[f"{tag}_Z10_reduced_control"]=h1_32[tag]
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
        # Keep Repair03 implementation failures distinct from science FAIL.
        print(json.dumps({
            "classification":"GE19_REPAIR03_WINDOW_RETARDED_REDUCED_H3_Z20_PARTICULAR_IMPLEMENTATION_FAIL",
            "error":repr(exc),
        },indent=2))
        raise
