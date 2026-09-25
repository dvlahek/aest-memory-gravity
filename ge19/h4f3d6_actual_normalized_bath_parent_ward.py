#!/usr/bin/env python3
"""H4F3d6: physical, per-node GE05 normalized bath Ward SUBSET only.

Read exact certified local H4F3b source and H3F/H3G/Repair32B/Repair26
parents. Reconstruct the unchanged first-order R1 bath (z10,v10),
compute action-derived E_q10 using frozen FD4_x and sum the real-space
physical Ward product +4 E_q10 q10,x through exact signed-mode
convolution. Does not assume any Ward term is small. Does NOT compute
nonbath parent/boundary or full canonical operator Ward; no Z21 solve.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

import numpy as np

ROOT=Path(__file__).resolve().parents[1]
PRE_BLOB="PREDATA_BLOB_TO_PIN"
PINNED={
 "ge19/h4f3d6_predata_actual_normalized_bath_parent_ward.json":PRE_BLOB,
 "ge19/h4f3d_predata_actual_operator_all_parent_ward_closure.json":
   "f1bd4eb52b7da96ac2d50ed9136e3e1a74635f51",
 "ge19/h4f3d5_normalized_bath_parent_residual_compiler.py":
   "62cbd02902ccb514c535213ff9801a9abcd46ffb",
 "ge19/h4f3d4_complete_eta_regularized_mixed_ward_ledger.py":
   "87d8be9ec44ecb099feecbaf59a904bd989da2fb",
 "ge19/h4f3b_actual_corrected_six_piece_source.py":
   "0423cbc64f6cda3b2a9aeb67c734935ef3ae7f9c",
 "ge19/repair37_cancellation_safe_fd8_h4_z21_reclosure.py":
   "45d203a092f9ac71cc612b15df5f0c0c630f5898",
 "ge19/repair24_q20_construction.py":
   "fc271987d1bddcd023cc9c057ddcad036b1d72fb",
}

SOURCE_JSON_SHA="1ec88fd3fd6b81bf30614b0cb78d722a02dd4f745e1f22cb9b8f956a44bac6c1"
SOURCE_NPZ_SHA="787d5d177838b05078057aa932f379dd529449ce203f5664c36cf723acb0116b"
TINY=1e-300
MODES=np.array([3,5,8,10,15,20],dtype=int)
M_MAX=40


def sha256(path):
    h=hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda:stream.read(1<<20),b""):
            h.update(chunk)
    return h.hexdigest()


def check_code_lock():
    out={}
    for rel,want in PINNED.items():
        got=subprocess.check_output(
            ["git","rev-parse","HEAD:"+rel],cwd=ROOT,text=True
        ).strip()
        out[rel]={"expected":want,"observed":got,"exact":want==got}
    if not all(v["exact"] for v in out.values()):
        raise RuntimeError("H4F3d6 frozen source/predata blobs changed")
    return out


def rel_l2(a,b):
    x=np.asarray(a);y=np.asarray(b)
    return float(np.linalg.norm(x-y)/max(
        np.linalg.norm(x),np.linalg.norm(y),TINY
    ))


def fd4(y,x):
    """Frozen uniform x=ln(a) five-node fourth-order finite difference."""
    xx=np.asarray(x,float)
    arr=np.asarray(y,complex)
    if xx.ndim!=1 or arr.shape[-1]!=len(xx) or len(xx)<9:
        raise ValueError("H4F3d6 FD4 shape mismatch")
    h=float((xx[-1]-xx[0])/(len(xx)-1))
    if not h>0 or not np.allclose(np.diff(xx),h,rtol=1e-9,atol=1e-13):
        raise ValueError("H4F3d6 requires original uniform ln(a)")
    dst=np.empty_like(arr,complex)
    dst[...,2:-2]=(arr[...,:-4]-8*arr[...,1:-3]
                    +8*arr[...,3:-1]-arr[...,4:])/(12*h)
    dst[...,0]=(-25*arr[...,0]+48*arr[...,1]-36*arr[...,2]
                 +16*arr[...,3]-3*arr[...,4])/(12*h)
    dst[...,1]=(-3*arr[...,0]-10*arr[...,1]+18*arr[...,2]
                 -6*arr[...,3]+arr[...,4])/(12*h)
    dst[...,-2]=(3*arr[...,-1]+10*arr[...,-2]
                  -18*arr[...,-3]+6*arr[...,-4]-arr[...,-5])/(12*h)
    dst[...,-1]=(25*arr[...,-1]-48*arr[...,-2]
                  +36*arr[...,-3]-16*arr[...,-4]+3*arr[...,-5])/(12*h)
    return dst


def normalized_bath_euler(z,v,X,a,H,x,r,w,tau):
    """Original GE05 raw E_q10; all arrays on exact common physical grid."""
    z=np.asarray(z,complex)
    v=np.asarray(v,complex)
    X=np.asarray(X,complex)
    aa=np.asarray(a,float)
    hh=np.asarray(H,float)
    rr=np.asarray(r,float)
    ww=np.asarray(w,float)
    xx=np.asarray(x,float)
    nt=len(xx)
    if (z.ndim!=3 or z.shape!=v.shape or z.shape[1:]!=(len(MODES),nt)
        or X.shape!=(len(MODES),nt) or aa.shape!=(nt,)
        or hh.shape!=(nt,) or rr.shape!=(z.shape[0],)
        or ww.shape!=rr.shape or np.any(rr<=0) or np.any(ww<=0)
        or np.any(aa<=0) or np.any(hh<=0) or tau<=0
        or not np.allclose(aa,np.exp(xx),rtol=1e-12,atol=1e-14)):
        raise ValueError("H4F3d6 invalid frozen bath state, quadrature or clock")
    if not all(np.isfinite(a).all() for a in (z,v,X,aa,hh,rr,ww)):
        raise ValueError("nonfinite frozen bath parent")
    omega=rr[:,None,None]/tau
    omega2=omega**2
    a3=aa[None,None,:]**3
    current=a3*v/tau
    current_d=fd4(current,xx)
    kinetic=hh[None,None,:]*current_d
    potential=a3*omega2*(z-X[None,:,:])
    residual=kinetic+potential
    euler=-np.sqrt(ww)[:,None,None]/(2*omega)*residual
    natural=float(np.linalg.norm(kinetic)+np.linalg.norm(potential))
    if not np.isfinite(euler).all():
        raise FloatingPointError("nonfinite GE05 E_q10")
    return euler,residual,{
        "R_z10_absolute_L2":float(np.linalg.norm(residual)),
        "R_z10_relative_natural_L2_report_only":
            float(np.linalg.norm(residual)/max(natural,TINY)),
        "all_node_rows_finite":True,
        "frozen_action_current":"a**3*v10/tau",
        "frozen_physical_clock":"H*FD4_ln(a)",
    }


def ward_signed_convolution(euler,qx,modes=MODES,mmax=M_MAX):
    """4 sum_nodes E_q10(x) q10,x(x) including +/- mode cross-products.

    Fourier arrays [nodes, six POSITIVE modes, Nt]; negative coefficient
    of each real field is its complex conjugate. No FFT grid alias,
    no product of only equal positive Fourier coefficients.
    """
    ee=np.asarray(euler,complex)
    q=np.asarray(qx,complex)
    mm=np.asarray(modes,int)
    if (ee.ndim!=3 or ee.shape!=q.shape or ee.shape[1]!=len(mm)
        or not np.array_equal(np.sort(mm),mm) or np.any(mm<=0)
        or mmax<2*int(mm.max())
        or not np.isfinite(ee).all() or not np.isfinite(q).all()):
        raise ValueError("invalid exact first-order signed-mode convolution")
    out=np.zeros((ee.shape[-1],mmax+1),complex)
    for i,p in enumerate(mm):
        for j,k in enumerate(mm):
            for sp in (1,-1):
                E=ee[:,i,:] if sp==1 else np.conj(ee[:,i,:])
                for sq in (1,-1):
                    target=int(sp*p+sq*k)
                    if 0<=target<=mmax:
                        Q=q[:,j,:] if sq==1 else np.conj(q[:,j,:])
                        out[:,target]+=4*np.einsum(
                            "bt,bt->t",E,Q,optimize=True
                        )
    return out


def physical_bath_ward(z,v,X,a,H,x,r,w,tau,kfund):
    euler,residual,diagnostic=normalized_bath_euler(
        z,v,X,a,H,x,r,w,tau
    )
    qx=(np.sqrt(w)[:,None,None]/
        (r[:,None,None]/tau))*(
            1j*kfund*MODES[None,:,None]
        )*z
    W=ward_signed_convolution(euler,qx)
    return W,diagnostic


def real_modes(coeff,nx,modes=MODES):
    theta=2*np.pi*np.arange(nx)/nx
    basis=np.exp(1j*np.asarray(modes)[:,None]*theta[None,:])
    return 2*np.real(np.einsum(
        "bmt,mx->btx",np.asarray(coeff,complex),
        basis,optimize=True
    ))


def manufactured(nt):
    """Independent real-space FFT vs exact convolution, no physical parent."""
    x=np.linspace(np.log(.4),0.,nt)
    a=np.exp(x)
    H=np.full(nt,.71)
    tau=7.0
    r=np.array([.37,.73,1.09,1.57,2.11])
    w=np.array([.09,.16,.31,.25,.19])
    m=MODES[None,:,None]
    omega=r[:,None,None]/tau
    x3=x[None,None,:]
    amp=(1+.11*r[:,None,None]+.06*m)*np.exp(
        1j*(.17*r[:,None,None]+.13*m))
    P=.53+.17*x3-.039*x3**2+.012*x3**3+.006*x3**4
    P1=.17-.078*x3+.036*x3**2+.024*x3**3
    P2=-.078+.072*x3+.072*x3**2
    z=amp*np.exp(-3*x3)*P
    dz=amp*np.exp(-3*x3)*(P1-3*P)
    v=tau*H[None,None,:]*dz
    Jx=H[None,None,:]*amp*(P2-3*P1)
    # Deliberately leave a smooth nonzero exact Euler remainder.
    # X must be a COMMON node-independent drive for the frozen bath.
    # For real-space product test only choose common X=0; the exact
    # relative Euler numerical value is report-only, not a smallness gate.
    X=np.zeros((len(MODES),nt),complex)
    E,R,diag=normalized_bath_euler(z,v,X,a,H,x,r,w,tau)
    kfund=.13
    qx=np.sqrt(w)[:,None,None]/omega*(1j*kfund*m)*z
    conv=ward_signed_convolution(E,qx)
    nx=256
    actual=4*np.einsum("btx,btx->tx",
        real_modes(E,nx),real_modes(qx,nx),optimize=True)
    fft=np.fft.fft(actual,axis=-1)[:,:M_MAX+1]/nx
    test=rel_l2(conv,fft)
    polynomial=fd4(a[None,None,:]**3*v/tau,x)
    exact=H[None,None,:]*amp*(P2-3*P1)
    current_err=rel_l2(polynomial,exact/H[None,None,:])
    bad=ward_signed_convolution(E,qx*0+1e-3j)
    negative=float(np.linalg.norm(conv-bad)/max(
        np.linalg.norm(conv),np.linalg.norm(bad),TINY))
    return {
      "Nt":nt,
      "real_space_FFT_vs_exact_signed_convolution_relative_L2":test,
      "FD4_current_manufactured_relative_L2":current_err,
      "negative_wrong_spatial_gradient_relative_defect":negative,
      "all_outputs_finite":bool(
          np.isfinite(conv).all() and np.isfinite(E).all()
          and np.isfinite(R).all()),
      "actual_physical_parent_loaded":False,
      "pass":bool(test<=1e-12 and current_err<=1e-9
                  and negative>=.001 and np.isfinite(conv).all()),
    }


def actual_run(results_dir,trace,source_npz,source_json,json_out,npz_out):
    # Delay importing frozen historical generators until after the
    # local runner changes CWD to an isolated temporary directory.
    from ge19 import h4f3b_actual_corrected_six_piece_source as s
    from ge19 import repair37_cancellation_safe_fd8_h4_z21_reclosure as old
    rd=Path(results_dir).resolve()
    trace=Path(trace).resolve()
    sn=Path(source_npz).resolve()
    sj=Path(source_json).resolve()
    if (not sn.is_file() or not sj.is_file()
        or sha256(sn)!=SOURCE_NPZ_SHA or sha256(sj)!=SOURCE_JSON_SHA):
        raise RuntimeError("exact real H4F3b source JSON/NPZ missing or hash mismatched")
    report=json.loads(sj.read_text())
    if (report.get("classification")!=
        "GE19_H4F3B_ACTUAL_CORRECTED_SIX_SOURCE_PASS_FULL_WARD_OPEN"
        or not report.get("gates")
        or not all(v is True for v in report["gates"].values())):
        raise RuntimeError("actual H4F3b source not certified")
    code=s.code_lock()
    files,parents=s.frozen_inputs(rd,trace)
    if not (np.array_equal(MODES,old.r7.FOURIER_N)
            and old.M_MAX==M_MAX):
        raise RuntimeError("H4F3d6 original GE19 first-order mode scope changed")
    result={}
    entries=[]
    with np.load(files["r13"],allow_pickle=False) as r13,         np.load(files["h3fn"],allow_pickle=False) as h3f,         np.load(files["h3gn"],allow_pickle=False) as h3g,         np.load(files["z11"],allow_pickle=False) as z11,         np.load(sn,allow_pickle=False) as physical:
        bgs,_,_,_,_,_,_,_,_=old.build_context(rd,r13)
        boundary=old.r24.full_history_boundary(
            old.c4,old.r7,trace,2048
        )
        r=np.asarray(boundary["r"],float)
        w=np.asarray(boundary["w"],float)
        tau=old.r24.TAUH0/float(old.r7.g9.H0_CLASS)
        kfund=float(old.r7.g9.K_REQ[0]/old.r7.FOURIER_N[0])
        for nt,label in ((128,"primary"),(64,"control")):
            x=np.asarray(physical["x_"+label],float)
            if not np.array_equal(x,np.asarray(h3f["x_"+label],float)):
                raise RuntimeError("H4F3d6 H4F3b/H3F common x grid mismatch")
            for tag in old.r7.C_TAGS:
                bg=bgs[(nt,tag)]
                if not np.array_equal(x,np.asarray(bg["x"],float)):
                    raise RuntimeError("actual background differs from H4F3b saved grid")
                for parent in (h3g,z11):
                    if not np.array_equal(x,np.asarray(parent["x_"+label],float)):
                        raise RuntimeError("H4F3d6 H3G/Z11 common x grid mismatch")
                H=np.asarray(bg["H"],float)
                a=np.asarray(bg["a"],float)
                h1=np.asarray(h3f[f"{tag}_H1_{label}"],complex)
                X10=old.r24.first_order_X_modes(old.r7,bg,h1)
                z10,v10=old.r24.evolve_z10(
                    old.c4,bg,X10,boundary["z0"],
                    boundary["v0"],r,tau
                )
                wz10=np.einsum("b,bmt->mt",w,z10,optimize=True)
                oldw=np.asarray(h3g[f"{tag}_weighted_z10_{'primary' if nt==128 else 'time_control'}"],complex)
                r1rel=rel_l2(wz10,oldw)
                if r1rel>1e-10:
                    raise RuntimeError(f"frozen R1 bath reproduction FAIL {tag} {nt}: {r1rel}")
                bath,diag=physical_bath_ward(
                    z10,v10,X10,a,H,x,r,w,tau,kfund
                )
                key=f"{label}_{tag}"
                result[f"{key}_bath_parent_ward_physical"]=bath
                result[f"{key}_x"]=x
                for ib,beta in enumerate(old.r7.BETAS):
                    name=f"{key}_beta{ib}"
                    source=np.asarray(physical[
                        f"{name}_source_ward_physical"],complex)
                    if source.shape!=bath.shape:
                        raise RuntimeError("physical H4F3b source/bath shape mismatch")
                    result[f"{name}_source_plus_bath_report_only"]=source+bath
                    entries.append({
                       "C":tag,"Nt":nt,"beta":float(beta),
                       "frozen_R1_weighted_z10_relative_L2":r1rel,
                       "normalized_bath_Euler":diag,
                       "W_bath_max_abs_report_only":float(np.max(np.abs(bath))),
                       "W_source_max_abs_report_only":float(np.max(np.abs(source))),
                       "W_source_plus_bath_max_abs_report_only":
                           float(np.max(np.abs(source+bath))),
                       "W_source_plus_bath_zero_not_a_gate":True,
                       "all_outputs_finite":bool(
                           np.isfinite(bath).all()
                           and np.isfinite(source).all()),
                    })
        result["x_primary"]=np.asarray(physical["x_primary"],float)
        result["x_control"]=np.asarray(physical["x_control"],float)
    passes={
      "exact_source_parent_hash_and_classification":True,
      "common_corrected_H3F_H3G_Z11_R13_R1_grids":True,
      "all_C_Nt_beta_cases":len(entries)==18,
      "R1_weighted_z10_reproduction_le_1e10":
          all(q["frozen_R1_weighted_z10_relative_L2"]<=1e-10
              for q in entries),
      "per_node_normalized_GE05_and_Fourier_source_finite":
          all(q["all_outputs_finite"] for q in entries),
      "no_source_or_source_plus_bath_smallness_gate":
          all(q["W_source_plus_bath_zero_not_a_gate"] for q in entries),
    }
    passed=all(passes.values())
    result_json={
      "classification":(
        "GE19_H4F3D6_ACTUAL_BATH_PARENT_WARD_SUBSET_PASS_FULL_OPEN"
        if passed else
        "GE19_H4F3D6_ACTUAL_BATH_PARENT_WARD_SUBSET_FAIL"
      ),
      "parent_predata":"GE19_H4F3D_PREDATA_OPERATOR_PLUS_ALL_PARENT_WARD_ON_ACTUAL_SIX_SOURCE",
      "source_sha256":{"JSON":SOURCE_JSON_SHA,"NPZ":SOURCE_NPZ_SHA},
      "parent_input_sha256":parents,"source_blobs":code,
      "cases":entries,"gates":passes,
      "failed_gates":[k for k,v in passes.items() if not v],
      "full_actual_operator_and_all_nonbath_parent_Ward_derived":False,
      "full_all_sector_H4_Noether_certified":False,
      "new_structural_tolerance_preregistered":False,
      "H4_Z21_solve_performed":False,
      "Z21_certified":False,"lensing_licensed":False,
      "next_route":(
        "DERIVE_REMAINING_NONBATH_PARENT_BOUNDARY_PLUS_OPERATOR_COMMON_GRID_WARD"
        if passed else "FREEZE_PHYSICAL_BATH_SUBSET_FAILURE"
      ),
      "claim_boundary":"Physical normalized first-order R1 bath Euler Ward SUBSET on real H4F3b corrected-parent grids. Source+bath not constrained to zero. No independent nonbath background/H1/Z11 Euler, action boundary or canonical operator Ward evaluated; no all-sector structural or H4/Z21 certification.",
    }
    jp=Path(json_out).resolve();npz=Path(npz_out).resolve()
    jp.parent.mkdir(parents=True,exist_ok=True)
    jp.write_text(json.dumps(result_json,indent=2,sort_keys=True,allow_nan=False)+"\n")
    np.savez_compressed(npz,**result)
    print(json.dumps(result_json,indent=2,sort_keys=True,allow_nan=False))
    if not passed:
        raise SystemExit(2)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--manufactured",action="store_true")
    ap.add_argument("--results-dir")
    ap.add_argument("--repair26-trace")
    ap.add_argument("--source-json")
    ap.add_argument("--source-npz")
    ap.add_argument("--json-out",required=True)
    ap.add_argument("--npz-out")
    args=ap.parse_args()
    locks=check_code_lock()
    if args.manufactured:
        tests=[manufactured(n) for n in (64,128)]
        passed=all(t["pass"] for t in tests)
        data={
          "classification":(
            "GE19_H4F3D6_BATH_CONVOLUTION_COMPILER_PASS_ACTUAL_OPEN"
            if passed else "GE19_H4F3D6_BATH_CONVOLUTION_COMPILER_FAIL"
          ),
          "frozen_blobs":locks,"manufactured_cases":tests,
          "all_manufactured_gates_pass":passed,
          "actual_physical_parent_loaded":False,
          "full_all_sector_H4_Noether_certified":False,
          "Z21_certified":False,
          "lensing_licensed":False,
        }
        dest=Path(args.json_out)
        dest.parent.mkdir(parents=True,exist_ok=True)
        dest.write_text(json.dumps(data,indent=2,sort_keys=True,allow_nan=False)+"\n")
        print(json.dumps(data,indent=2,sort_keys=True,allow_nan=False))
        if not passed:
            raise SystemExit(3)
    else:
        if not all((args.results_dir,args.repair26_trace,
                    args.source_json,args.source_npz,args.npz_out)):
            ap.error("physical run requires all frozen parent/source paths and --npz-out")
        actual_run(args.results_dir,args.repair26_trace,
                   args.source_npz,args.source_json,
                   args.json_out,args.npz_out)


if __name__=="__main__":
    main()
