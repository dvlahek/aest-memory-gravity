#!/usr/bin/env python3
"""GE19 H4F2h: physically clocked, scheme-aware H4 SOURCE Ward projection.

GE19 time x=ln(a) is NOT physical proper time. The frozen Repair37
source differentiates in physical time as H(x)*FD8_x for GE06/GE07/Lambda;
the frozen Repair07/GE05 memory source uses H(x)*FD4_x. This new,
standalone adapter keeps the distinction explicit instead of silently
using np.gradient(source,ln(a)) as d/dt.

It computes the SOURCE projection only. Actual linear-operator Ward,
parent Euler residuals and full H4/Z21 remain untested.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

import numpy as np

from ge19 import h4f2g_action_completed_six_piece_source_ledger as ledger
from ge19 import repair07_window_retarded_reduced_h3_z20_particular as r7
from ge19 import repair37_cancellation_safe_fd8_h4_z21_reclosure as r37

ROOT=Path(__file__).resolve().parents[1]
BLOBS={
    "ge19/h4f2h_predata_physical_clock_discrete_ward_bridge.json":
        "dc5b29219d25c89d18b1bc37a7ce116f3818e349",
    "ge19/h4f2g_predata_six_piece_signed_source_ward_ledger.json":
        "70bee663a0f529a734b586dbc8b9f6e90bc8ed9f",
    "ge19/h4f2g_action_completed_six_piece_source_ledger.py":
        "d9778da0bb6cc52a15015238810c79978527ffc5",
    "docs/ge19_h4f2g_signed_six_piece_source_ledger_valid_freeze.md":
        "9bb8d66ee6f04ec893b6523a9ce8a44c9c0867b8",
    "docs/ge19_h4f2b_signed_mixed_ward_template_valid_freeze.md":
        "98693317485149898830eebd0f335db12024e6dc",
    "ge19/repair37_cancellation_safe_fd8_h4_z21_reclosure.py":
        "45d203a092f9ac71cc612b15df5f0c0c630f5898",
    "ge19/repair07_window_retarded_reduced_h3_z20_particular.py":
        "e34d28a2062c748f48bc82fa928844b02631de25",
}
SCHEMES={
    "2Q_GE06_cross":"fd8",
    "2Q_GE07_cross":"fd8",
    "2Q_Lambda_cross":"fd8",
    "2DY2_action_complete_Y_u_and_phi":"fd8",
    "2M1_GE05_mapped":"fd4",
    "2M2_GE05_mapped":"fd4",
}

def frozen_blobs():
    return {
        path:{"expected":want,
              "observed":(got:=subprocess.check_output(
                  ["git","rev-parse","HEAD:"+path],cwd=ROOT,text=True
              ).strip()),
              "exact":got==want}
        for path,want in BLOBS.items()
    }

def validate_clock_and_rows(rows,log_a,a,H,kfund):
    f=np.asarray(rows,complex)
    xx=np.asarray(log_a,float)
    aa=np.asarray(a,float)
    hh=np.asarray(H,float)
    if (xx.ndim!=1 or xx.size<9 or not np.isfinite(xx).all()
        or not np.all(np.diff(xx)>0)
        or aa.shape!=xx.shape or hh.shape!=xx.shape
        or not np.isfinite(aa).all() or not np.isfinite(hh).all()
        or not np.all(aa>0) or not np.all(hh>0)
        or f.shape!=(8,xx.size,41) or not np.isfinite(f).all()
        or not np.isfinite(kfund) or float(kfund)<=0):
        raise ValueError("invalid H4 source, ln(a), physical H, or 41-mode cohort")
    if not np.allclose(aa,np.exp(xx),rtol=1e-12,atol=1e-14):
        raise ValueError("a does not equal exp(log_a) on common GE19 time grid")
    h=float((xx[-1]-xx[0])/(xx.size-1))
    if not np.allclose(np.diff(xx),h,rtol=1e-9,atol=1e-13):
        raise ValueError("frozen GE19 FD4/FD8 requires uniform log(a) grid")
    return f,xx,aa,hh

def physical_source_ward(rows,log_a,a,H,kfund,scheme):
    """D_S=H*D_ln(a) S_b+(a/3)*i*k*(S_iso+2*S_aniso).

    No claim that the source projection is individually zero.
    This routine NEVER accepts the generic second-order np.gradient
    proxy of the historical H4F2g synthetic source-only test.
    """
    f,xx,aa,hh=validate_clock_and_rows(rows,log_a,a,H,kfund)
    if scheme=="fd8":
        derivative=r37.fd8_matrix(len(xx),float(xx[0]),float(xx[-1]))
    elif scheme=="fd4":
        derivative=r7.fd4_matrix(len(xx),float(xx[0]),float(xx[-1]))
    else:
        raise ValueError("unregistered H4 temporal differentiation scheme")
    k=float(kfund)*np.arange(f.shape[-1],dtype=float)
    return (hh[:,None]*(derivative@f[6])
            +1j*aa[:,None]*k[None,:]/3.0*(f[1]+2.0*f[7]))

def physical_six_piece_ward(parts,log_a,a,H,kfund):
    """Sum source-Ward pieces after EACH frozen family derivative scheme.

    FD8 and FD4 source families cannot be aggregated and differentiated
    with one arbitrary derivative operator without a separate error proof.
    """
    if not isinstance(parts,dict) or set(parts)!=set(ledger.PIECES):
        raise ValueError("require all and only six registered source families")
    xx=np.asarray(log_a,float)
    out={}
    for name in ledger.PIECES:
        arr=np.asarray(parts[name],complex)
        if arr.shape!=(8,len(xx),41):
            raise ValueError(f"{name}: common time, row or mode mismatch")
        # Preserve exact frozen H4F2g support and source signs.
        ledger._validate_piece((arr[:6],arr[6:]),name,len(xx),41)
        out[name]=physical_source_ward(
            arr,xx,a,H,kfund,SCHEMES[name]
        )
    total=sum((out[n] for n in ledger.PIECES),
              np.zeros((len(xx),41),complex))
    return {
        "per_piece":out,
        "total_source_ward":total,
        "schemes":dict(SCHEMES),
        "mixed_FD8_FD4_scheme_kept_explicit":True,
        "corrected_parent_and_operator_Ward_evaluated":False,
        "full_H4_Noether_derived":False,
        "Z21_solved":False,
    }

def main():
    print(json.dumps({
        "classification":"GE19_H4F2H_PHYSICAL_CLOCK_SOURCE_WARD_HELPER_ONLY",
        "blobs":frozen_blobs(),
        "schemes":SCHEMES,
        "derivative":"physical d_t=H(x)*D_x, x=ln(a)",
        "full_H4_Noether_derived":False,
        "Z21_certified":False,
    },indent=2,sort_keys=True))
if __name__=="__main__":
    main()
