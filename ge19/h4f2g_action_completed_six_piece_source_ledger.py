#!/usr/bin/env python3
"""GE19 H4F2g: separately versioned six-piece signed source-row ledger.

The five external source families must ALREADY be in frozen GE19 raw RHS
units and fft/nx convention. The sixth, full NL0C Y u+phi family, is built
HERE from the blob-pinned Stage E action-derived implementation, replacing
the historical scalar-only Repair37 DY2. The only derived Ward quantity is
the signed *source* projection; all parent and linear-operator Ward terms
remain explicitly unresolved. No H4/Z21 solver or corrected parent is run.
"""
from __future__ import annotations

import argparse
import ast
import json
import subprocess
from pathlib import Path

import numpy as np
from ge19 import h4_stagee_versioned_y_source_rows as stagee

ROOT=Path(__file__).resolve().parents[1]
BLOBS={
    "ge19/h4f2g_predata_six_piece_signed_source_ward_ledger.json":
        "70bee663a0f529a734b586dbc8b9f6e90bc8ed9f",
    "ge19/h4f2_predata_complete_mixed_h4_ward_parent_dictionary.json":
        "8097a4770ae8aed74cb4dd0721c1c9bd6907533c",
    "ge19/repair37_cancellation_safe_fd8_h4_z21_reclosure.py":
        "45d203a092f9ac71cc612b15df5f0c0c630f5898",
    "ge19/repair07_window_retarded_reduced_h3_z20_particular.py":
        "e34d28a2062c748f48bc82fa928844b02631de25",
    "ge19/h4_stagee_versioned_y_source_rows.py":
        "282166ea5840d7fba4dbc328d40d7687afa6fa0f",
    "docs/ge19_h4f2b_signed_mixed_ward_template_valid_freeze.md":
        "98693317485149898830eebd0f335db12024e6dc",
    "docs/ge19_h4f2d_y_m1_action_flux_valid_freeze.md":
        "647d3a8cf207fbf18fef7e0cbdb23c9bfbfc5de8",
    "docs/ge19_h4f2e_shift_action_subidentity_valid_freeze.md":
        "79c81ebffeca490b9dad74d812005086daa04c32",
    "docs/ge19_h4f2f_ge06_ward_shift_valid_freeze.md":
        "3ea436c1f535d9477847bb690c7b5fc7652951d2",
}
GE19_ROWS=("N","L_plus_R","u","phi","T","rho","b",
           "L_minus_R_over2")
PIECES=(
    "2Q_GE06_cross",
    "2Q_GE07_cross",
    "2Q_Lambda_cross",
    "2DY2_action_complete_Y_u_and_phi",
    "2M1_GE05_mapped",
    "2M2_GE05_mapped",
)
Y_PIECE=PIECES[3]
NON_Y=(PIECES[0],PIECES[1],PIECES[2],PIECES[4],PIECES[5])
SUPPORT={
    PIECES[0]:(0,1,2,3,6,7),
    PIECES[1]:(0,1,4,5,6,7),
    PIECES[2]:(0,1),
    PIECES[3]:(2,3),
    PIECES[4]:(2,3),
    PIECES[5]:(0,1,2,3,6,7),
}

def exact_blobs():
    return {
        path:{"expected":want,
              "observed":(got:=subprocess.check_output(
                  ["git","rev-parse","HEAD:"+path],
                  cwd=ROOT,text=True
              ).strip()),
              "exact":got==want}
        for path,want in BLOBS.items()
    }

def frozen_source_bindings():
    old=(ROOT/"ge19/repair37_cancellation_safe_fd8_h4_z21_reclosure.py").read_text()
    y=(ROOT/"ge19/h4_stagee_versioned_y_source_rows.py").read_text()
    static=(ROOT/"ge19/h4f2_predata_complete_mixed_h4_ward_parent_dictionary.json").read_text()
    return {
        "six_original_piece_names_retained":all(
            ('"'+name+'"') in old for name in (
                "2Q_GE06_cross","2Q_GE07_cross","2Q_Lambda_cross",
                "2DY2","2M1_GE05_mapped","2M2_GE05_mapped")
        ),
        "frozen_GE06_negative_two_cross":
            "qga_main=-2.0*fft_low(ga_m); qga_con=-2.0*fft_low(ga_c)" in old,
        "frozen_GE07_negative_two_cross":
            "qm_main=-2.0*fft_low(ma_m); qm_con=-2.0*fft_low(ma_c)" in old,
        "frozen_Lambda_direct_negative_two":
            "ql_main=-2.0*fft_low(lam_m); ql_con=-2.0*fft_low(lam_c)" in old,
        "frozen_GE05_M2_factor_two":
            "return -GE05_TO_GE06*fft_low(raw_main),-GE05_TO_GE06*fft_low(raw_con),z10,v10" in old
            and "GE05_TO_GE06=2.0" in old,
        "frozen_M1_uses_weighted_B20":
            'm1_main,m1_con=m1_mapped_fourier(bg,bathcfg[tag]["B20_linear"])' in old,
        "frozen_fft_over_nx":
            "hh=np.fft.fft(aa,axis=-1)/aa.shape[-1]" in old,
        "historical_DY2_scalar_only_requires_replacement":
            "main[3]=-2.0*fm" in old
            and 'pieces={' in old,
        "StageE_H4_has_both_action_derived_rows":
            "main[2]=2.0*aa**3*qq*kappa*projected" in y
            and "main[3]=-2.0*aa**2*kappa*div_x" in y
            and "2.0*np.abs(g0)*g1" in y,
        "StageE_second_order_beta_cohorts":
            stagee.FROZEN_BETAS==(1.0,0.5,0.1),
        "frozen_six_piece_predata_exact":
            len(json.loads(static)["fixed_source_dictionary"]["six_pieces"])==6,
    }

def _validate_piece(item,name,nt,nm):
    if not isinstance(item,(tuple,list)) or len(item)!=2:
        raise ValueError(f"{name}: supply (main[6,nt,nm],constraint[2,nt,nm])")
    ma=np.asarray(item[0],dtype=complex)
    co=np.asarray(item[1],dtype=complex)
    if ma.shape!=(6,nt,nm) or co.shape!=(2,nt,nm):
        raise ValueError(f"{name}: GE19 row or shared-grid/mode mismatch")
    if not (np.isfinite(ma).all() and np.isfinite(co).all()):
        raise ValueError(f"{name}: nonfinite GE19 source")
    allrows=np.concatenate((ma,co),axis=0)
    zero_rows=tuple(i for i in range(8) if i not in SUPPORT[name])
    if any(np.any(allrows[i]) for i in zero_rows):
        raise ValueError(f"{name}: forbidden row support {zero_rows}")
    return ma.copy(),co.copy()

def signed_ward_source(full8,time,a,kfund):
    """Compute D_S=d_t(S_b)+(a/3)*ik*(S_iso+2 S_aniso).

    No assertion that this equals zero: it must cancel the signed
    all-sector parent+linear-operator Ward expression, not itself.
    """
    f=np.asarray(full8,dtype=complex)
    tt=np.asarray(time,float)
    aa=np.asarray(a,float)
    if (f.ndim!=3 or f.shape[0]!=8 or f.shape[1]!=len(tt)
        or tt.ndim!=1 or len(tt)<3 or aa.shape!=tt.shape
        or not np.all(np.diff(tt)>0) or not np.isfinite(f).all()
        or not np.isfinite(tt).all() or not np.isfinite(aa).all()
        or not np.all(aa>0)
        or not np.isfinite(kfund) or float(kfund)<=0):
        raise ValueError("invalid H4 source Ward grid or complex source")
    k=float(kfund)*np.arange(f.shape[-1],dtype=float)
    dt_shift=np.gradient(f[6],tt,axis=0,edge_order=2)
    return dt_shift+1j*(aa[:,None]*k[None,:]/3.0)*(f[1]+2.0*f[7])

def assemble_six(external,a,Q,u10,phi10_x,u11,phi11_x,
                 KB,a0,beta,kfund,time,mmax=40):
    """Assemble only source rows; keep corrected parents outside this stage.

    All five external inputs are already GE19 RHS (NOT raw Euler,
    NOT Q without -2). Legacy scalar-only Y is NEVER accepted.
    """
    if not isinstance(external,dict) or set(external)!=set(NON_Y):
        raise ValueError("exactly five fixed non-Y GE19 RHS families required; old DY2 forbidden")
    aa=np.asarray(a,float)
    tt=np.asarray(time,float)
    if aa.ndim!=1 or tt.shape!=aa.shape or aa.size<3 or not (1<=mmax):
        raise ValueError("invalid shared time or mode representation")
    nx=np.asarray(u10).shape[-1]
    if not isinstance(mmax,int) or nx<3*(mmax+1):
        raise ValueError("underresolved Y flux 2/3 band or invalid mmax")
    y=stagee.source_h4(
        aa,Q,u10,phi10_x,u11,phi11_x,KB,a0,beta,kfund
    )
    fy=np.fft.fft(y["main"],axis=-1)[:,:,:mmax+1]/nx
    cy=np.fft.fft(y["constraint"],axis=-1)[:,:,:mmax+1]/nx
    nt,nm=aa.size,mmax+1
    pieces={name:_validate_piece(external[name],name,nt,nm)
            for name in NON_Y}
    pieces[Y_PIECE]=_validate_piece((fy,cy),Y_PIECE,nt,nm)
    parts={
        name:np.concatenate(pieces[name],axis=0)
        for name in PIECES
    }
    total=sum((parts[name] for name in PIECES),
              np.zeros((8,nt,nm),dtype=complex))
    ward_by_piece={
        name:signed_ward_source(parts[name],tt,aa,kfund)
        for name in PIECES
    }
    ward_total=signed_ward_source(total,tt,aa,kfund)
    if not np.isfinite(ward_total).all():
        raise FloatingPointError("nonfinite six-piece source Ward projection")
    return {
        "piece_rows":parts,
        "total_rows":total,
        "source_ward_by_piece":ward_by_piece,
        "total_source_ward":ward_total,
        "Y_from_StageE":True,
        "historical_scalar_only_Y_replaced":True,
        "full_six_piece_parent_Noether_certified":False,
        "linear_operator_Ward_evaluated":False,
        "background_H1_Z11_Z20_q20_dust_bath_parent_residuals_evaluated":False,
        "Z21_solved":False,
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--show-contract",action="store_true")
    args=p.parse_args()
    d={"classification":"GE19_H4F2G_SIX_PIECE_SIGNED_SOURCE_LEDGER_ONLY",
       "blob_gates":exact_blobs(),
       "source_bindings":frozen_source_bindings(),
       "row_order":GE19_ROWS,"pieces":PIECES,
       "support":{k:list(v) for k,v in SUPPORT.items()},
       "full_H4_Noether_derived":False,"Z21_certified":False}
    if args.show_contract:
        print(json.dumps(d,indent=2,sort_keys=True))
if __name__=="__main__":
    main()
