#!/usr/bin/env python3
"""H4F2h deterministic symbolic/FD4/FD8 physical clock source Ward audit.

No real H3F/H3G/Z11 parents are loaded and NO full Noether or H4 solve
is performed. H4F2g's source-only PASS remains untouched; its generic
np.gradient(time) expression is a negative control when time=ln(a).
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import sympy as sp

from ge19 import h4f2h_physical_time_source_ward_bridge as clock
from ge19 import h4f2g_action_completed_six_piece_source_ledger as ledger

def rel_l2(p,q):
    x=np.asarray(p);y=np.asarray(q)
    return float(np.linalg.norm(x-y)/max(
        np.linalg.norm(x),np.linalg.norm(y),1e-300
    ))

def chain_rule():
    t,z=sp.symbols("t z",real=True)
    a=sp.Function("a")(t)
    Sb=sp.Function("S_b")
    derived=sp.diff(Sb(sp.log(a)),t)
    exact=sp.diff(a,t)/a*sp.Subs(
        sp.Derivative(Sb(z),z),z,sp.log(a)
    )
    return bool(sp.simplify(derived-exact)==0)

def p(z):
    return .11+.28*z+.19*z*z+.13*z**5

def dp_dlog(z,length):
    return (.28+.38*z+.65*z**4)/length

def manufactured(nt,beta):
    x=np.linspace(np.log(.4),0.0,nt)
    z=(x-x[0])/(x[-1]-x[0])
    a=np.exp(x)
    H=.4+.09*z
    m=np.arange(41,dtype=float)
    weight=(1.0/(1.0+beta))/(1.0+m)
    phase=np.exp(1j*(m*.08))
    phase[0]=1.0
    amplitude=2e-5*weight*phase
    iso_amp=4e-7*weight*np.exp(1j*.12*m)
    aniso_amp=3e-7*weight*np.exp(-1j*.21*m)
    iso_amp[0]=iso_amp[0].real
    aniso_amp[0]=aniso_amp[0].real
    f=np.zeros((8,nt,41),complex)
    f[6]=p(z)[:,None]*amplitude[None,:]
    f[1]=(.25+.23*z*z)[:,None]*iso_amp[None,:]
    f[7]=(.17+.11*z**3)[:,None]*aniso_amp[None,:]
    kfund=.19
    k=kfund*m
    true=(H[:,None]*dp_dlog(z,x[-1]-x[0])[:,None]*amplitude[None,:]
          +1j*(a[:,None]*k[None,:]/3.)*(f[1]+2*f[7]))
    return f,x,a,H,kfund,true

def families(nt,beta):
    source,x,a,H,kfund,truth=manufactured(nt,beta)
    result={}
    for j,name in enumerate(ledger.PIECES):
        s=np.zeros_like(source)
        if name in (ledger.Y_PIECE,"2M1_GE05_mapped"):
            # No metric or constraint source, both physical u/phi rows retained.
            s[2]=2e-8*np.cos(x[:,None]*1.3+np.arange(41)[None,:]*.09)
            s[3]=1e-8*np.sin(x[:,None]*1.2+np.arange(41)[None,:]*.07)
            s[2,:,0]=s[2,:,0].real
            s[3,:,0]=s[3,:,0].real
        else:
            fac=(j+1)/12.
            s[6]=fac*source[6] if 6 in ledger.SUPPORT[name] else 0
            s[1]=fac*source[1] if 1 in ledger.SUPPORT[name] else 0
            s[7]=fac*source[7] if 7 in ledger.SUPPORT[name] else 0
            if 0 in ledger.SUPPORT[name]:
                s[0]=fac*1e-8*np.ones((nt,41))
            if 2 in ledger.SUPPORT[name]:
                s[2]=fac*1e-8*np.ones((nt,41))
            if 3 in ledger.SUPPORT[name]:
                s[3]=fac*1e-8*np.ones((nt,41))
            if 4 in ledger.SUPPORT[name]:
                s[4]=fac*1e-8*np.ones((nt,41))
            if 5 in ledger.SUPPORT[name]:
                s[5]=fac*1e-8*np.ones((nt,41))
        result[name]=s
    return result,x,a,H,kfund

def invalid_tests(f,x,a,H,k):
    bad={}
    cases={
        "nonuniform_ln_a":(f,x.copy(),a,H,k,"fd8"),
        "a_not_exp_ln_a":(f,x,a.copy(),H,k,"fd8"),
        "negative_H":(f,x,a,H.copy(),k,"fd8"),
        "missing_mode":(f[:,:,:-1],x,a,H,k,"fd8"),
        "unregistered_FD":(f,x,a,H,k,"gradient"),
    }
    xbad=cases["nonuniform_ln_a"][1]
    xbad[2]+=0.002
    cases["a_not_exp_ln_a"][2][2]+=0.01
    cases["negative_H"][3][3]=-0.2
    for label,args in cases.items():
        try:
            clock.physical_source_ward(*args)
        except ValueError:
            bad[label]=True
        else:
            bad[label]=False
    parts,x,a,H,k=families(64,1.0)
    parts.pop("2M2_GE05_mapped")
    try:
        clock.physical_six_piece_ward(parts,x,a,H,k)
    except ValueError:
        bad["missing_source_family"]=True
    else:
        bad["missing_source_family"]=False
    return bad

def case(nt,beta):
    f,x,a,H,k,truth=manufactured(nt,beta)
    fd8=clock.physical_source_ward(f,x,a,H,k,"fd8")
    fd4=clock.physical_source_ward(f,x,a,H,k,"fd4")
    wrong=ledger.signed_ward_source(f,x,a,k)
    e8=rel_l2(fd8,truth)
    e4=rel_l2(fd4,truth)
    ew=rel_l2(wrong,truth)
    parts,xp,ap,Hp,kp=families(nt,beta)
    pieces=clock.physical_six_piece_ward(parts,xp,ap,Hp,kp)
    summed=sum((pieces["per_piece"][name] for name in ledger.PIECES),
               np.zeros((nt,41),complex))
    aggregate=sum((parts[name] for name in ledger.PIECES),
                  np.zeros_like(f))
    wrong_all_fd8=clock.physical_source_ward(aggregate,xp,ap,Hp,kp,"fd8")
    mismatch=rel_l2(wrong_all_fd8,pieces["total_source_ward"])
    lambda_nonzero=bool(
        np.linalg.norm(pieces["per_piece"]["2Q_Lambda_cross"][:,1:])>0
    )
    zero_Y=bool(np.array_equal(
        pieces["per_piece"][ledger.Y_PIECE],np.zeros((nt,41),complex)
    ))
    zero_M1=bool(np.array_equal(
        pieces["per_piece"]["2M1_GE05_mapped"],np.zeros((nt,41),complex)
    ))
    pass_gate=bool(
        e8<=1e-9 and e4<=2e-5 and ew>1e-2
        and rel_l2(summed,pieces["total_source_ward"])<=1e-13
        and mismatch>1e-12 and zero_Y and zero_M1 and lambda_nonzero
        and np.isfinite(fd8).all() and np.isfinite(fd4).all()
        and np.isfinite(pieces["total_source_ward"]).all()
    )
    return {
        "Nt":nt,"beta":beta,
        "physical_FD8_vs_analytic_relative_L2":e8,
        "physical_FD4_vs_analytic_relative_L2":e4,
        "legacy_ln_a_gradient_vs_physical_relative_L2":ew,
        "separate_scheme_sum_relative_L2":
            rel_l2(summed,pieces["total_source_ward"]),
        "naive_all_FD8_vs_mixed_FD8_FD4_relative_L2_report_only":mismatch,
        "Y_source_Ward_exact_zero":zero_Y,
        "M1_source_Ward_exact_zero":zero_M1,
        "Lambda_isotropic_source_Ward_nonzero":lambda_nonzero,
        "pass":pass_gate
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--json-out",required=True)
    args=ap.parse_args()
    blobs=clock.frozen_blobs()
    chain=chain_rule()
    cases=[case(nt,beta)
           for nt in (64,128)
           for beta in (1.0,.5,.1)]
    f,x,a,H,k,_=manufactured(64,1.0)
    invalid=invalid_tests(f,x,a,H,k)
    good=bool(chain and all(v["exact"] for v in blobs.values())
              and all(c["pass"] for c in cases)
              and all(invalid.values()))
    report={
        "classification":(
            "GE19_H4F2H_PHYSICAL_CLOCK_DISCRETE_SOURCE_WARD_BRIDGE_PASS"
            if good else
            "GE19_H4F2H_PHYSICAL_CLOCK_OR_DISCRETE_SOURCE_WARD_FAIL"
        ),
        "predata_classification":
            "GE19_H4F2H_PREDATA_PHYSICAL_CLOCK_DISCRETE_WARD_BRIDGE",
        "frozen_blobs":blobs,
        "physical_chain_rule_exact":chain,
        "all_gates_pass":good,
        "cases":cases,
        "invalid_inputs_rejected":invalid,
        "H4F2g_legacy_source_only_result_unchanged":True,
        "real_corrected_parent_arrays_loaded":False,
        "full_all_sector_H4_Noether_derived":False,
        "H4_Z21_solve_performed":False,
        "Z21_certified":False,
        "lensing_licensed":False,
        "next_route":(
            "PREREGISTER_CORRECTED_PARENT_OPERATOR_PLUS_SOURCE_WARD_ON_COMMON_TIME"
            if good else
            "FREEZE_PHYSICAL_TIME_FD_SOURCE_WARD_FAILURE"
        ),
        "boundary":"Manufactured clock/scheme audit only. Does not demonstrate physical H3F/H3G/Z11 parent compatibility, full H4 Noether or discrete shift-constraint success."
    }
    p=Path(args.json_out)
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(report,indent=2,sort_keys=True,allow_nan=False)+"\n")
    print(json.dumps(report,indent=2,sort_keys=True,allow_nan=False))
    if not good:
        raise SystemExit(3)

if __name__=="__main__":
    main()
