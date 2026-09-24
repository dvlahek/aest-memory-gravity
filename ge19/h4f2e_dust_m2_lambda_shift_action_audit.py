#!/usr/bin/env python3
"""H4F2e: exact shift-action subset for GE07 dust, GE05 M2 and Lambda.

Independent analytic source-row audit only. No corrected-parent sampling,
no full six-piece H4 Noether/source identity, no Z21 solve.
"""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

import numpy as np
import sympy as sp

from ge05 import memory_directional_source_generator as ge05
from ge07 import pressureless_matter_directional_source_generator as ge07
from ge19 import repair37_cancellation_safe_fd8_h4_z21_reclosure as r37

ROOT=Path(__file__).resolve().parents[1]
BLOBS={
 "ge19/h4f2e_predata_dust_m2_lambda_shift_action.json":"H4F2E_PRE_BLOB",
 "ge19/h4f2_predata_complete_mixed_h4_ward_parent_dictionary.json":"8097a4770ae8aed74cb4dd0721c1c9bd6907533c",
 "ge07/pressureless_matter_directional_source_generator.py":"cde8da77a80799cef00fc7c09c3633310fc9e3d4",
 "ge05/memory_directional_source_generator.py":"40837d77f89028da30c28899e2d0530a4401844e",
 "ge19/repair37_cancellation_safe_fd8_h4_z21_reclosure.py":"45d203a092f9ac71cc612b15df5f0c0c630f5898",
 "ge19/repair14_self_consistent_reduced_h3_z20_particular.py":"06c5ced952c2370cfa4aaadb6ef8f72d2d7221de",
 "docs/ge19_h4f2a_dust_offshell_ward_valid_freeze.md":"ca21c65ce2da8d760aa12018aefd849b3b67adf9",
 "docs/ge19_h4f2d_y_m1_action_flux_valid_freeze.md":"647d3a8cf207fbf18fef7e0cbdb23c9bfbfc5de8",
 "docs/ge19_h4_structural_stage_a_source_row_ledger.md":"44d4f01a05aba26926d6a8e13a2b7aac995258d5",
}


def exact(expr):
    return bool(sp.simplify(sp.factor(sp.cancel(expr)))==0)


def frozen_blobs():
    d={}
    for path,want in BLOBS.items():
        got=subprocess.check_output(
            ["git","rev-parse","HEAD:"+path],
            cwd=ROOT,text=True
        ).strip()
        d[path]={"expected":want,"observed":got,"exact":got==want}
    return d


def exact_action():
    # Read the actual frozen source actions, not a reconstructed
    # guessed normalization or independent Lagrangian substitution.
    W=ge07.W
    dust_expected=-2*ge07.L*ge07.R**2*ge07.varrho*W*ge07.Tx
    dust_source=ge07.partial_map["b_f"]
    dust_exact=exact(dust_source-dust_expected)

    C=ge05.om*ge05.q-ge05.sw*ge05.Xphi
    ge05_expected=-(ge05.L*ge05.R**2)/2*(
        ge05.Aq*sp.cosh(ge05.r)*ge05.qx
        +C*ge05.sw*sp.sinh(ge05.r)*ge05.px
    )
    mem_exact=exact(ge05.partials["b"]-ge05_expected)
    # The frozen physical epsilon-second derivative is a full
    # second derivative, not the coefficient divided by 2.
    mem_eps2=exact(
        ge05.coeff2["b"]+ge05.a**3*ge05.dqt*ge05.dqx
    )
    mem_first=exact(ge05.coeff1["b"])
    r24=(ROOT/"ge19/repair14_self_consistent_reduced_h3_z20_particular.py").read_text()
    r37src=(ROOT/"ge19/repair37_cancellation_safe_fd8_h4_z21_reclosure.py").read_text()
    lambda_bind=("L_lambda = -6 rho_lambda N L R^2" in r24)
    lambda_shift=exact(sp.diff(
        -6*sp.Symbol("rho_lambda")*sp.Symbol("N")*
        sp.Symbol("L")*sp.Symbol("R")**2,sp.Symbol("b")
    ))
    source_bindings={
        "GE07_action_shift_partial":dust_exact,
        "GE05_action_shift_partial":mem_exact,
        "GE05_M1_shift_exact_zero":mem_first,
        "GE05_M2_shift_eps2_equals_minus_a3_qt_qx":mem_eps2,
        "Lambda_frozen_action_bound":lambda_bind,
        "Lambda_exact_no_shift_coupling":lambda_shift,
        "Repair37_GE05_raw_shift_row_in_constraint_index0":
            'con=np.stack([shift,LL-0.5*RR],axis=0)' in r37src,
        "Repair37_GE05_factor2_and_H4_minus_sign":
            'return -GE05_TO_GE06*fft_low(raw_main),-GE05_TO_GE06*fft_low(raw_con),z10,v10' in r37src
            and r37.GE05_TO_GE06==2.0,
        "Repair37_GE07_negative_twice_bilinear":
            'qm_con=-2.0*fft_low(ma_c)' in r37src,
    }

    # Exact GE07 mixed H4 coefficient of the shift Euler row from
    # the frozen action, independently compared to the frozen c2
    # polarization. The frozen q_cross_direct returns half of this
    # directional derivative, so the -2 RHS map is its negative.
    eps,eta=sp.symbols("eps eta",real=True)
    a,rhob=sp.symbols("a rhob",positive=True,real=True)
    da=tuple(sp.symbols("dN0 dL0 dR0 db0 drho0 dTt0 dTx0",real=True))
    db=tuple(sp.symbols("dN1 dL1 dR1 db1 drho1 dTt1 dTx1",real=True))
    ordered=(ge07.N,ge07.L,ge07.R,ge07.b,
             ge07.varrho,ge07.Tt,ge07.Tx)
    background=(sp.Integer(1),a,a,sp.Integer(0),rhob,
                sp.Integer(1),sp.Integer(0))
    substituted=dust_source.subs({
        field:zero+eps*(left+eta*right)
        for field,zero,left,right in zip(
            ordered,background,da,db)
    }, simultaneous=True)
    mixed=sp.diff(substituted,eps,2).subs(eps,0)
    mixed=sp.diff(mixed,eta).subs(eta,0)
    args0=(a,rhob,*da)
    args1=(a,rhob,*(left+right for left,right in zip(da,db)))
    argsm=(a,rhob,*(left-right for left,right in zip(da,db)))
    c2=ge07.coeff2["b_f"]
    polarization=sp.Rational(1,2)*(
        c2.subs(dict(zip(ge07.direction_args,args1)),simultaneous=True)
        -c2.subs(dict(zip(ge07.direction_args,argsm)),simultaneous=True)
    )
    geo={
        "GE07_raw_mixed_shift_deta_deps2_matches_c2_polarization":
            exact(mixed-polarization),
        "GE07_direct_mixed_shift_is_negative_of_original_RHS":
            exact(-mixed+2*polarization/2),
    }
    # The source is -2*Qbil with Qbil=polarization/2.
    # -mixed == -2*(polarization/2) because mixed=polarization.
    geo["GE07_original_negative_two_bilinear_sign"]=exact(
        -mixed-(-2*polarization/2)
    )
    return source_bindings,geo,{
        "GE07_shift_Euler":"-2 L R^2 varrho W T_x",
        "GE07_mixed_H4_RHS":"-d_eta d_epsilon^2 E_b,GE07|0 = -2 Q_bilinear,GE07",
        "GE05_raw_M2_shift":"-a^3 dqt dqx per node",
        "GE05_mapped_H4_M2_shift":"+2 a^3 sum_nodes dqt dqx (then fft_low)",
        "Lambda_shift":"0 identically",
    }


def finite_fourier():
    nt,nx,nn=5,256,3
    tt=np.arange(nt)[:,None,None]
    xx=2*np.pi*np.arange(nx)[None,None,:]/nx
    jj=np.arange(nn)[:,None,None]
    phase=(jj+1)*xx+0.17*tt+0.2*jj
    amp=1e-4*(jj+1)
    q=amp*np.sin(phase)
    qt=amp*0.17*np.cos(phase)
    qx=amp*(jj+1)*np.cos(phase)
    aa=0.53+0.04*np.arange(nt)[:,None]
    Q=1.0e-4+1e-5*np.arange(nt)[:,None]
    shape=q.shape
    bb=lambda x:np.broadcast_to(np.asarray(x,float),shape)
    a=bb(aa[None,:,:])
    Qv=bb(Q[None,:,:])
    zeros=np.zeros(shape,float)
    du=bb(2e-4*np.cos(phase))
    dpt=bb(6e-5*np.sin(phase))
    dpx=bb(7e-5*np.cos(phase))
    sw=bb(0.6+0.1*jj)
    om=bb(1.2+0.2*jj)
    raw=ge05.f_c2["b"](
        a,Qv,zeros,zeros,zeros,zeros,du,
        dpt,dpx,qt,qx,q,om,sw
    )
    raw=np.broadcast_to(np.asarray(raw,float),shape)
    expected=-a**3*qt*qx
    if not (np.isfinite(raw).all() and np.isfinite(expected).all()):
        raise RuntimeError("nonfinite GE05 M2 local shift comparison")
    numerator=np.linalg.norm(raw-expected)
    denominator=max(np.linalg.norm(raw),np.linalg.norm(expected),1e-300)
    sample_error=float(numerator/denominator)
    low_implemented=-r37.GE05_TO_GE06*r37.fft_low(raw.sum(axis=0))
    low_action=r37.fft_low((2*a**3*qt*qx).sum(axis=0))
    err_low=float(np.linalg.norm(low_implemented-low_action)/max(
        np.linalg.norm(low_implemented),np.linalg.norm(low_action),1e-300
    ))
    return {
        "node_count":nn,"Nt":nt,"Nx":nx,
        "GE05_c2_b_vs_action_node_relative_L2":sample_error,
        "mapped_M2_shift_fourier_lowmode_relative_L2":err_low,
        "GE05_M2_shift_nonzero":bool(np.linalg.norm(low_action)>0),
        "all_outputs_finite":True,
        "gates_pass":bool(sample_error<=1e-12 and err_low<=1e-12
                          and np.linalg.norm(low_action)>0),
    }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--json-out",required=True)
    args=ap.parse_args()
    blobs=frozen_blobs()
    bind,geo,expr=exact_action()
    deterministic=finite_fourier()
    passed=bool(
        all(x["exact"] for x in blobs.values())
        and all(bind.values())
        and geo["GE07_raw_mixed_shift_deta_deps2_matches_c2_polarization"]
        and geo["GE07_original_negative_two_bilinear_sign"]
        and deterministic["gates_pass"]
    )
    d={
        "classification":(
            "GE19_H4F2E_SHIFT_ACTION_SUBIDENTITY_PASS"
            if passed else "GE19_H4F2E_SHIFT_ACTION_SUBIDENTITY_FAIL"
        ),
        "frozen_blobs":blobs,"exact_source_action_bindings":bind,
        "GE07_mixed_shift_polarization":geo,
        "GE07_GE05_Lambda_exact_row_dictionary":expr,
        "deterministic_frozen_GE05_M2_shift":deterministic,
        "all_subset_gates_pass":passed,
        "full_six_piece_H4_source_parent_Noether_derived":False,
        "corrected_parent_common_grid_evaluated":False,
        "H4_Z21_solve_performed":False,
        "Z21_certified":False,"lensing_licensed":False,
        "next_route":"DERIVE_GE06_SHIFT_AND_REMAINING_FULL_SOURCE_PARENT_WARD",
    }
    out=Path(args.json_out)
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(d,indent=2,sort_keys=True,allow_nan=False)+"\n")
    print(json.dumps(d,indent=2,sort_keys=True,allow_nan=False))
    if not passed:
        raise SystemExit(3)


if __name__=="__main__":
    main()
