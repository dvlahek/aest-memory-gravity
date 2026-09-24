#!/usr/bin/env python3
"""Standalone H3F exact source-adapter audit; no H3 parent solve."""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from types import SimpleNamespace

import numpy as np

from ge19 import h3f_corrected_y_source_adapter as h3f
from ge19 import h4_stagee_versioned_y_source_rows as stagee
from ge19 import repair07_window_retarded_reduced_h3_z20_particular as r7

ROOT=Path(__file__).resolve().parents[1]
BLOBS={
 "ge19/h3f_predata_action_completed_y_z20_parent_reclosure.json":
   "6ae1dd8c27ee1f94d85831cd5ae7b5ec21e3794e",
 "ge19/h3f_corrected_y_source_adapter.py":
   "395294868191111b9b01201315cd2e6a30e47578",
 "ge19/h4_stagee_versioned_y_source_rows.py":
   "282166ea5840d7fba4dbc328d40d7687afa6fa0f",
 "ge19/repair14_self_consistent_reduced_h3_z20_particular.py":
   "06c5ced952c2370cfa4aaadb6ef8f72d2d7221de",
 "ge19/repair07_window_retarded_reduced_h3_z20_particular.py":
   "e34d28a2062c748f48bc82fa928844b02631de25",
}


def rel_l2(a,b):
    u=np.asarray(a)
    v=np.asarray(b)
    return float(np.linalg.norm(u-v)/max(
        np.linalg.norm(u),np.linalg.norm(v),1e-300
    ))


def exact_blobs():
    return {
        path:{
            "expected":want,
            "observed":(got:=subprocess.check_output(
                ["git","rev-parse","HEAD:"+path],cwd=ROOT,text=True
            ).strip()),
            "exact":bool(got==want),
        }
        for path,want in BLOBS.items()
    }


def deterministic():
    nt,nx=5,256
    x=np.arange(nx)*2*np.pi/nx
    t=np.arange(nt)[:,None]
    aa=0.51+0.04*np.arange(nt)
    Q=1e-4+2e-6*np.arange(nt)
    u=0.0001*np.cos(x[None,:]+t*0.2)
    g=1e-6*np.sin(x[None,:]+t*0.1)+2e-7*np.cos(3*x[None,:]+t*0.4)
    px=aa[:,None]*(g-Q[:,None]*u)
    bg={"a":aa,"Q_action":Q}
    kfund=float(r7.g9.K_REQ[0]/r7.FOURIER_N[0])
    nm=41
    shape=(6,nt,nm)
    ar=np.arange(np.prod(shape),dtype=float).reshape(shape)
    ga=(np.cos(ar/17.0)+1j*np.sin(ar/13.0))*1e-2
    matter=(np.sin(ar/21.0)+1j*np.cos(ar/19.0))*1e-4
    lamb=(np.cos(ar/11.0)+1j*np.sin(ar/7.0))*1e-8
    legacy={}
    for beta in stagee.FROZEN_BETAS:
        oldY=np.zeros(shape,complex)
        old_reduced=r7.y2_source_from_reduced(
            bg,{"u20":u},{"phi20":px},beta
        )
        oldY[3]=np.fft.fft(-2*old_reduced,axis=-1)[:,:nm]/nx
        legacy[beta]={
            "rhs":ga+matter+lamb+oldY,
            "rhs_constraint":np.zeros((2,nt,nm),complex),
            "Q_ga":ga.copy(),"Q_matter":matter.copy(),
            "Q_lambda":lamb.copy(),"Y_H3":oldY,
        }
    out=h3f.replace_y_only(
        legacy,bg,u,px,r7.KB,r7.A0_MPC_INV,kfund
    )
    rows=[]
    for beta in stagee.FROZEN_BETAS:
        item=out[beta]
        direct=stagee.source_h3(
            aa,Q,u,px,r7.KB,r7.A0_MPC_INV,beta,kfund
        )
        newfft=np.fft.fft(direct["main"],axis=-1)[:,:,:nm]/nx
        nonY=ga+matter+lamb
        check={
            "beta":beta,
            "full_new_Y_exact":bool(np.array_equal(
                item["Y_H3"],newfft
            )),
            "new_RHS_nonY_plus_full_Y_exact":bool(np.array_equal(
                item["rhs"],nonY+newfft
            )),
            "old_Y_unchanged_report_only":bool(np.array_equal(
                item["Y_H3_legacy_report_only"],legacy[beta]["Y_H3"]
            )),
            "non_Y_pieces_unchanged":bool(all(
                np.array_equal(item[k],legacy[beta][k])
                for k in ("Q_ga","Q_matter","Q_lambda")
            )),
            "non_Y_reproduction_relative_L2":
                item["H3F_non_Y_reproduction_relative_L2"],
            "constraints_exactly_unchanged":bool(np.array_equal(
                item["rhs_constraint"],legacy[beta]["rhs_constraint"]
            )),
            "H3F_aether_row_present":bool(
                np.linalg.norm(item["Y_H3"][2])>0
            ),
            "Y_non_u_phi_rows_zero":bool(np.array_equal(
                item["Y_H3"][[0,1,4,5]],
                np.zeros((4,nt,nm),complex)
            )),
        }
        check["pass"]=bool(
            all(v for k,v in check.items()
                if k not in ("beta","pass","non_Y_reproduction_relative_L2"))
            and check["non_Y_reproduction_relative_L2"]<=1e-12
        )
        rows.append(check)

    # Verify production wrapper does not implicitly mix spatial grids
    # or add the legacy scalar source. Use the exact same synthetic
    # legacy bundle and an injected stub of the frozen generator.
    observed=[]
    def gen_stub(r7arg,m6,m7,bgarg,rho,tag,nxarg,state,dot):
        observed.append((bgarg is bg,nxarg==nx,state is u,dot is px))
        return legacy
    fake_r14=SimpleNamespace(source_bundle_reduced_lambda=gen_stub)
    fake_r7=SimpleNamespace(
        reduced_state_real=lambda background,state,nxarg,dot:
            ({"u20":state},None,{"phi20":dot}),
        KB=r7.KB,A0_MPC_INV=r7.A0_MPC_INV,
        g9=r7.g9,FOURIER_N=r7.FOURIER_N
    )
    prod=h3f.source_bundle_reduced_lambda(
        fake_r7,fake_r14,None,None,bg,None,"C_star",nx,u,px
    )
    production_exact=bool(
        all(np.array_equal(prod[beta]["rhs"],out[beta]["rhs"])
            for beta in stagee.FROZEN_BETAS)
        and observed==[(True,True,True,True)]
    )
    invalid=[]
    for legacy_bad,aa_bad,uu_bad,mmax in (
        (dict((beta,legacy[beta]) for beta in (0.1,0.5,1.0)),bg,u,40),
        (legacy,{"a":aa,"Q_action":Q[:-1]},u,40),
        (legacy,bg,u[:3],40),
        (legacy,bg,u,128),
    ):
        try:
            h3f.replace_y_only(
                legacy_bad,aa_bad,uu_bad,px,r7.KB,r7.A0_MPC_INV,kfund,
                mmax=mmax
            )
            invalid.append(False)
        except (ValueError,RuntimeError):
            invalid.append(True)
    return rows,production_exact,bool(all(invalid))


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--json-out",required=True)
    args=ap.parse_args()
    blobs=exact_blobs()
    rows,production,invalid=deterministic()
    ok=bool(
        all(v["exact"] for v in blobs.values())
        and all(r["pass"] for r in rows)
        and production and invalid
    )
    report={
        "classification":(
            "GE19_H3F_COMPLETE_Y_SOURCE_ADAPTER_PASS"
            if ok else "GE19_H3F_COMPLETE_Y_SOURCE_ADAPTER_FAIL"
        ),
        "predata_classification":
            "GE19_H3F_PREDATA_ACTION_COMPLETED_Y_Z20_PARENT_RECLOSURE",
        "audit_scope":"Source adapter only: old non-Y GE06/GE07/Lambda preserved, old scalar-only Y replaced by Stage E complete u+phi Y; H3 state is not solved.",
        "frozen_blobs":blobs,
        "beta_cases":rows,
        "production_wrapper_exact":production,
        "invalid_cases_rejected":invalid,
        "all_gates_pass":ok,
        "old_H3_H4_modules_modified":False,
        "H3F_Z20_reclosure_performed":False,
        "new_q20_computed":False,
        "full_H4_Noether_derived":False,
        "Z21_certified":False,
        "lensing_licensed":False,
        "next_route":(
            "IMPLEMENT_SEPARATE_H3F_ON_SHELL_PARENT_AND_REPROJECT_BOUNDARY"
            if ok else
            "FREEZE_H3F_SOURCE_ADAPTER_FAILURE"
        ),
    }
    p=Path(args.json_out)
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(report,indent=2,sort_keys=True,allow_nan=False)+"\n")
    print(json.dumps(report,indent=2,sort_keys=True,allow_nan=False))
    if not ok:
        raise SystemExit(3)


if __name__=="__main__":
    main()
