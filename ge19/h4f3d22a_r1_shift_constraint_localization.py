#!/usr/bin/env python3
"""D22A-R1: localize failed frozen shift gates from archived states, without new solves.

Compare original-action vs frozen-background canonical shift row, new vs old
Z11 on their own archived source sign, and every beta/mode/time of new Z20.
No gate relaxation, q20 or H4/Z21 calculation. D22A SCIENCE FAIL immutable.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
from contextlib import ExitStack
from pathlib import Path

import numpy as np

ROOT=Path(__file__).resolve().parents[1]
D22J_SHA="158207d747e9fa617c335f4a30d860c011264b2da1dcde34870bad762ec5bbf4"
D22N_SHA="6952a2cde9a39367d29b75b63aca53a97a8feb622e7cbe7b33a468ae2b9a1632"
TINY=1e-300

def sha(path):
    h=hashlib.sha256()
    with Path(path).open("rb") as fh:
        for block in iter(lambda:fh.read(1<<20),b""):
            h.update(block)
    return h.hexdigest()

def backward(row,w,source):
    row=np.asarray(row,complex);w=np.asarray(w,complex)
    lhs=complex(row@w);src=complex(source)
    numerator=abs(lhs-src)
    contributions=float(np.sum(np.abs(row*w)))
    scale=max(abs(lhs),abs(src),contributions,TINY)
    return float(numerator/scale),float(numerator),float(scale),lhs,src,float(contributions)

def packed_w(st,dot,it):
    """Frozen r7 order: N,rho,S,u,phi,T,Sdot,udot,phidot,Tdot."""
    w=np.empty(10,complex)
    w[:2]=st[[0,5],it]
    w[2:6]=st[[1,2,3,4],it]
    w[6:10]=dot[:,it]
    return w

def show(z):
    return [float(np.real(z)),float(np.imag(z))]

def location(metric,num,scale,lhs,src,component,x,scope,beta_values=None):
    i=np.unravel_index(int(np.argmax(metric)),metric.shape)
    if scope=="Z11":
        mode=[3,5,8,10,15,20][i[0]]
        beta=None;t=i[1]
    else:
        mode=i[1]+1;beta=float(beta_values[i[0]]);t=i[2]
    return dict(mode=mode,beta=beta,t_index=int(t),x=float(x[t]),
        relative_backward=float(metric[i]),absolute_residual=float(num[i]),
        backward_scale=float(scale[i]),lhs=show(lhs[i]),source=show(src[i]),
        row_component_scale=float(component[i]))

def array_pack(shape):
    return tuple(np.empty(shape,dtype=d) for d in (float,float,float,complex,complex,float))

def assign(out,index,v):
    for arr,x in zip(out,v):arr[index]=x

def summarize(pack,x,scope,beta_values=None):
    metric,num,scale,lhs,src,component=pack
    if any(not np.isfinite(q).all() for q in pack):
        raise RuntimeError("nonfinite shift forensic arrays")
    return dict(
        worst_relative=location(metric,num,scale,lhs,src,component,x,scope,beta_values),
        max_absolute=float(num.max()),
        max_scale=float(scale.max()),
        global_residual_over_global_component_scale=float(
            np.linalg.norm(num.ravel())/max(np.linalg.norm(component.ravel()),TINY)),
        global_residual_over_global_backward_scale=float(
            np.linalg.norm(num.ravel())/max(np.linalg.norm(scale.ravel()),TINY)),
        worst_absolute_index=list(map(int,np.unravel_index(int(np.argmax(num)),num.shape)))
    )

def manufactured():
    row=np.array([1+0j,1j]);w=np.array([1+2j,2-1j])
    rhs=row@w
    assert backward(row,w,rhs)[0]==0
    assert backward(row,w,-rhs)[0]>.01
    st=np.zeros((6,2),complex);dots=np.zeros((4,2),complex)
    st[0,0]=3;st[5,0]=5;st[1:5,0]=[7,11,13,17]
    dots[:,0]=[19,23,29,31]
    assert np.array_equal(packed_w(st,dots,0),[3,5,7,11,13,17,19,23,29,31])
    print("GE19_D22AR1_BACKWARD_METRIC_SIGN_AND_CANONICAL_ORDER_NEGATIVE_CONTROL_PASS",flush=True)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--results-dir",type=Path,required=True)
    ap.add_argument("--repair26-trace",type=Path,required=True)
    ap.add_argument("--json-out",type=Path,required=True)
    ap.add_argument("--npz-out",type=Path,required=True)
    args=ap.parse_args()
    manufactured()
    from ge19 import h4f3d22a_action_parent_reclosure as d22
    from ge19 import h4f3d20r1_recompute_five_sources_and_bath_ward as d20
    from ge19 import h4f3d17_actual_original_action_dense_canonical_H1 as d17driver
    from ge19 import h4f3d17_original_action_dense_H1_core as d17core
    rd=args.results_dir.resolve();trace=args.repair26_trace.resolve()
    jpath=rd/"ge19_h4f3d22a_actual_Cstar_action_B10_Z11_Z20_parent_candidates.json"
    npath=jpath.with_suffix(".npz")
    if sha(jpath)!=D22J_SHA or sha(npath)!=D22N_SHA:
        raise RuntimeError("D22A failed archive changed; never silently accept replacement")
    parent=json.loads(jpath.read_text())
    if parent["classification"]!="GE19_D22A_CSTAR_PARENT_NUMERICAL_CANDIDATE_FAIL_Q20_AND_FULL_H4_OPEN":
        raise RuntimeError("D22A failure provenance has changed")
    pre=json.loads(d22.PRE.read_text())
    files,inputs,locks=d22.verify(rd,trace,pre)
    old=d20.source.old;r7=old.r7
    if not (np.array_equal(r7._QIDX,[2,3,4,5]) and
            np.array_equal(r7._ZIDX,[0,1,6,7,8,9])):
        raise RuntimeError("frozen canonical slot definitions changed")

    results={}
    with ExitStack() as stack:
        old13=stack.enter_context(np.load(inputs["r13"],allow_pickle=False))
        oldz11=stack.enter_context(np.load(inputs["z11"],allow_pickle=False))
        archive=stack.enter_context(np.load(npath,allow_pickle=False))
        bgs,_,mod6,mod7,_,_,_,_,_=old.build_context(rd,old13)
        tag="C_star";bg=bgs[(128,tag)]
        x=np.asarray(archive["x_primary"],float)
        if not np.array_equal(x,np.asarray(bg["x"],float)):raise RuntimeError("background grid changed")
        z11=np.asarray(archive["Z11_D17_D19_candidate_primary"],complex)
        d11=np.asarray(archive["Z11dot_D17_D19_candidate_primary"],complex)
        zz=np.asarray(archive["Z20_D17_H3F_candidate_primary"],complex)
        dz=np.asarray(archive["Z20dot_D17_H3F_candidate_primary"],complex)
        z11old=np.asarray(oldz11["C_star_Z11_primary"],complex)
        d11old=np.asarray(oldz11["C_star_Z11dot_primary"],complex)
        if z11.shape!=(6,6,128) or d11.shape!=(6,4,128) or zz.shape!=(3,40,6,128) or dz.shape!=(3,40,4,128):
            raise RuntimeError("D22A state/physical jet dimensions changed")
        srcshift=np.asarray([archive[f"beta{ib}_H3F_D17_source_constraints"][0]
                             for ib in range(3)],complex)
        if srcshift.shape!=(3,128,41):raise RuntimeError("Z20 source constraints changed")
        if not (np.isfinite(z11).all() and np.isfinite(d11).all()
            and np.isfinite(zz).all() and np.isfinite(dz).all() and np.isfinite(srcshift).all()):
            raise RuntimeError("nonfinite D22A stored state or source")
        new11=array_pack((6,128));old11=array_pack((6,128))
        new20=array_pack((3,40,128))
        oldbg=r7._bg_point;oldcache=r7._CANONICAL_LOCAL_CACHE
        r7._CANONICAL_LOCAL_CACHE={}
        try:
            ev,_=d17driver.d16r1.d15.clk.make_original_action_background(r7,bg,tag)
            ctx=d17core.ActionBackground(r7,bg,ev);ctx.knot_check()
            r7._bg_point=lambda bgarg,xq:ctx(bgarg,xq)
            for im,m in enumerate(r7.FOURIER_N):
                k=float(m*r7.g9.K_REQ[0]/r7.FOURIER_N[0])
                for it,t in enumerate(x):
                    *_,cm,_,_=r7._canonical_operator_matrices(
                        mod6,mod7,bg,tag,k,float(t))
                    row=cm[10]+cm[11]
                    assign(new11,(im,it),backward(row,packed_w(z11[im],d11[im],it),0))
                    assign(old11,(im,it),backward(row,packed_w(z11old[im],d11old[im],it),0))
                print(f"GE19_D22AR1_SHIFT_Z11_ACTION_ROW mode={int(m)} / 6",flush=True)
            for jm,m in enumerate(r7.M_SOLVE):
                k=float(m*r7.g9.K_REQ[0]/r7.FOURIER_N[0])
                for it,t in enumerate(x):
                    *_,cm,_,_=r7._canonical_operator_matrices(
                        mod6,mod7,bg,tag,k,float(t))
                    row=cm[10]+cm[11]
                    for ib in range(3):
                        assign(new20,(ib,jm,it),backward(
                            row,packed_w(zz[ib,jm],dz[ib,jm],it),
                            srcshift[ib,it,int(m)]))
                if jm%5==0 or jm==39:
                    print(f"GE19_D22AR1_SHIFT_Z20_ACTION_ROW mode={jm+1}/40",flush=True)
        finally:
            r7._bg_point=oldbg
            r7._CANONICAL_LOCAL_CACHE=oldcache

        s11=summarize(new11,x,"Z11")
        s11old=summarize(old11,x,"Z11")
        s20=summarize(new20,x,"Z20",r7.BETAS)
        # Compare the identical stored states/jets and sources with the original
        # frozen interpolation at the worst original-action nodes only.
        legacy={}
        for name,summary in (("new_Z11",s11),("old_frozen_Z11",s11old),("new_Z20",s20)):
            loc=summary["worst_relative"];it=loc["t_index"];m=loc["mode"]
            if name=="new_Z11":
                im=int(np.where(r7.FOURIER_N==m)[0][0])
                w=packed_w(z11[im],d11[im],it);src=0j
            elif name=="old_frozen_Z11":
                im=int(np.where(r7.FOURIER_N==m)[0][0])
                w=packed_w(z11old[im],d11old[im],it);src=0j
            else:
                ib=int(np.where(np.asarray(r7.BETAS)==loc["beta"])[0][0])
                w=packed_w(zz[ib,m-1],dz[ib,m-1],it)
                src=srcshift[ib,it,m]
            k=float(m*r7.g9.K_REQ[0]/r7.FOURIER_N[0])
            # Restore frozen original background and isolate cache.
            oldcache2=r7._CANONICAL_LOCAL_CACHE
            r7._CANONICAL_LOCAL_CACHE={}
            try:
                *_,cm,_,_=r7._canonical_operator_matrices(
                    mod6,mod7,bg,tag,k,float(x[it]))
                met,num,scale,lhs,rhs,components=backward(cm[10]+cm[11],w,src)
            finally:
                r7._CANONICAL_LOCAL_CACHE=oldcache2
            legacy[name]=dict(relative_backward=met,absolute_residual=num,
                backward_scale=scale,lhs=show(lhs),source=show(rhs),
                row_component_scale=components)

        report=dict(
            classification="GE19_D22AR1_ARCHIVED_SHIFT_CONSTRAINT_LOCALIZATION_D22A_FAIL_UNCHANGED",
            D22A_failure_archive_json_sha256=D22J_SHA,D22A_failure_archive_npz_sha256=D22N_SHA,
            claim_boundary="Localizes archived D22A failed shift row using its saved states, jets and RHS. No new integration, no gate changes, no q20, no H4 Ward/Z21, no lensing. Original and legacy operator comparisons are diagnostics only.",
            D22A_science_fail_immutable=True,
            all_interval_GE05_on_shell_certified=False,
            Z11_certified=False,Z20_certified=False,
            q20_B20_recomputed=False,full_H4_Ward_certified=False,Z21_certified=False,lensing_licensed=False,
            stored_D22A_max_shift_Z11=parent["Z11_numerical"]["shift_constraint_relative_L2_max"],
            stored_D22A_max_shift_Z20=parent["Z20_numerical"]["shift_constraint_relative_max"],
            original_action_new_Z11=s11,
            original_action_frozen_Z11=s11old,
            original_action_new_Z20=s20,
            frozen_interpolation_at_action_worst_nodes=legacy,
            original_action_D22A_shift_max_reproduced=bool(
                abs(s11["worst_relative"]["relative_backward"]-
                    parent["Z11_numerical"]["shift_constraint_relative_L2_max"])<1e-6
                and abs(s20["worst_relative"]["relative_backward"]-
                    parent["Z20_numerical"]["shift_constraint_relative_max"])<1e-6),
            sources_verified=locks,
        )
        out={}
        for prefix,pack in (("new_Z11",new11),("frozen_Z11_action_matrix",old11),("new_Z20",new20)):
            for suffix,arr in zip(("metric","absolute","scale","lhs","source","row_component_scale"),pack):
                out[prefix+"_"+suffix]=arr
        out["x_primary"]=x
    jp=args.json_out.resolve();npz=args.npz_out.resolve()
    if jp.exists() or npz.exists():raise RuntimeError("D22A-R1 refuses to overwrite")
    jp.parent.mkdir(parents=True,exist_ok=True)
    jp.write_text(json.dumps(report,indent=2,sort_keys=True,allow_nan=False)+"\n")
    np.savez_compressed(npz,**out)
    print("GE19_D22AR1_FAILED_SHIFT_LOCALIZATION_JSON",json.dumps({
        k:report[k] for k in ("classification","original_action_D22A_shift_max_reproduced",
          "original_action_new_Z11","original_action_frozen_Z11",
          "original_action_new_Z20","frozen_interpolation_at_action_worst_nodes")},
        sort_keys=True),flush=True)
    if not report["original_action_D22A_shift_max_reproduced"]:
        raise SystemExit("D22A-R1 archived shift metric not independently reproduced")

if __name__=="__main__":
    main()
