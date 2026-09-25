#!/usr/bin/env python3
"""GE19 H4F3d5: independent normalized first-order GE05 bath Euler compiler.

Bind the actual frozen GE05 node action and the eta-regularized mixed
H4 Ward parent. Compile R_z10=H D_xi(a^3 v/tau)+a^3 omega^2(z-X10)
and E_q10=-sqrt(w)/(2 omega) R_z10. Check the +4 E_q10 q10,x
physical-mixed Ward coefficient, not a product of independent
Fourier coefficients on physical grids.

The Actions fixtures are manufactured polynomial kinematics only.
They are NOT the actual H1/Z11/H3F/H3G parent, a physical H4 Ward
structural result, an H4/Z21 solve or any observation.
"""
from __future__ import annotations

import argparse
import ast
import json
import subprocess
from pathlib import Path

import numpy as np
import sympy as sp

ROOT=Path(__file__).resolve().parents[1]
BLOBS={
 "ge19/h4f3d5_predata_normalized_bath_parent_residual_compiler.json":
    "6b7519b48ace8900c8a2879f13c70db3524b366e",
 "ge19/h4f3d4_predata_complete_eta_regularized_mixed_ward_ledger.json":
    "cc921c4086d914274738a29f2b7b5c6961ab56b0",
 "ge19/h4f3d4_complete_eta_regularized_mixed_ward_ledger.py":
    "87d8be9ec44ecb099feecbaf59a904bd989da2fb",
 "ge19/h4f3d3_eta_regularized_bath_ward_parent.py":
    "fb340b957c31e34d35f1ebd9404a53b59d29c102",
 "ge19/h4f3d2_dust_bath_parent_euler_currents.py":
    "42b2405759402195ffb371056d9e48b70dcded71",
 "ge19/repair24_q20_construction.py":
    "fc271987d1bddcd023cc9c057ddcad036b1d72fb",
 "ge19/repair07_window_retarded_reduced_h3_z20_particular.py":
    "e34d28a2062c748f48bc82fa928844b02631de25",
 "ge19/h4f3d_predata_actual_operator_all_parent_ward_closure.json":
    "f1bd4eb52b7da96ac2d50ed9136e3e1a74635f51",
 "ge05/memory_directional_source_generator.py":
    "40837d77f89028da30c28899e2d0530a4401844e",
}

def source_blobs():
    result={}
    for path,expected in BLOBS.items():
        got=subprocess.check_output(
            ["git","rev-parse","HEAD:"+path],cwd=ROOT,text=True
        ).strip()
        result[path]={"expected":expected,"observed":got,"exact":got==expected}
    return result

def normalized_symbolic():
    original=(ROOT/"ge05/memory_directional_source_generator.py").read_text()
    d2=(ROOT/"ge19/h4f3d2_dust_bath_parent_euler_currents.py").read_text()
    d3=(ROOT/"ge19/h4f3d3_eta_regularized_bath_ward_parent.py").read_text()
    norm=lambda s:"".join(s.split())
    binds={
      "frozen_GE05_per_node_action":
        "lag=N*L*R**2*sp.Rational(1,4)*(Aq**2-(om*q-sw*Xphi)**2)"
        in norm(original),
      "frozen_GE05_first_order_raw_Eq10":
        '"E_q10":"-a**3*omega*(omega*dq-sqrt(w)*(Q*du+dphi_x/a))/2-d_t(a**3*dqt/2)"'
        in norm(d2),
      "physical_eta_mixed_parent_factor_plus_four":
        "bath_parent=4*eq10*sp.diff(q10,x)" in (
            ROOT/"ge19/h4f3d4_complete_eta_regularized_mixed_ward_ledger.py"
        ).read_text(),
      "physical_eta_bath_factor_from_original_action":
        "physical_mapped_ward=2*eta*E*qx" in d3,
    }
    a,H,tau,omega,sw,z,v,X,DJ,k,zx=sp.symbols(
        "a H tau omega sw z v X DJ k zx",
        real=True
    )
    w=sp.symbols("w",positive=True,real=True)
    A3=a**3
    q=sw*z/omega
    qt=sw*v/(omega*tau)
    q_local,qt_local=sp.symbols("q_local qt_local",real=True)
    lag_raw=A3*(qt_local**2-(omega*q_local-sw*X)**2)/4
    J=A3*v/tau
    R=H*DJ+A3*omega**2*(z-X)
    E_action=-A3*omega*(omega*q-sw*X)/2-H*sw*DJ/(2*omega)
    Eq_expected=-sw*R/(2*omega)
    qx=sw*sp.I*k*z/omega
    Wphys=4*Eq_expected*qx
    Wmode=-2*w*R*sp.I*k*z/omega**2
    tests={
        "GE05_Euler_current_exact_normalization":
            sp.simplify(E_action-Eq_expected)==0,
        "GE05_raw_time_current_from_action":
            sp.simplify(
               sp.diff(lag_raw,qt_local).subs(qt_local,qt)
               -A3*qt/2
            )==0,
        "GE05_raw_local_Euler_from_action":
            sp.simplify(
               sp.diff(lag_raw,q_local).subs(q_local,q)
               +A3*omega*(omega*q-sw*X)/2
            )==0,
        "GE05_mode_Ward_pair_factor_plus_four":
            sp.simplify(Wphys.subs(sw,sp.sqrt(w))-Wmode)==0,
        "negative_wrong_euler_sign":
            sp.simplify(Wphys.subs(sw,sp.sqrt(w))-(-Wmode))!=0,
        "negative_missing_factor_two":
            sp.simplify(Wphys.subs(sw,sp.sqrt(w))-Wmode/2)!=0,
        "positive_quadrature_frequency_domain":
            sp.simplify((w/omega**2).subs(omega,k/tau)
                        -w*tau**2/k**2)==0,
    }
    # Verify the unchanged normalized variable is the q->z map.
    tests["normalized_definition_z_omega_q_over_sqrtw"]=(
        sp.simplify((omega*q/sw)-z)==0
    )
    tests["normalized_derivative_qt_from_v"]=(
        sp.simplify(qt-sw*v/(omega*tau))==0
    )
    return binds,tests,{
      "GE05_first_order_normalized_Euler":
         "E_q10=-sqrt(w)/(2omega)*[H D_xi(a^3 v/tau)+a^3 omega^2(z-X10)]",
      "physical_eta_mixed_bath_parent":
         "+4 Sum_j E_qj10*q_j10,x",
      "mode_pair_analytic_not_physical_convolution":
         "-2 Sum_j (w_j/omega_j^2) R_zj10*(i k)z_j10",
      "physical_products_require_real_space_convolution":True,
      "normalized_action_and_GE05_to_GE06_scale_fitted":False,
    }

def fd4(y,dx):
    """Frozen-order 5-point FD4 derivative, including both boundaries."""
    values=np.asarray(y)
    if values.shape[-1]<5 or not dx>0:
        raise ValueError("FD4 requires >=5 nodes and positive step")
    result=np.empty_like(values,dtype=np.result_type(values,complex))
    result[...,2:-2]=(
         values[...,:-4]-8*values[...,1:-3]
         +8*values[...,3:-1]-values[...,4:]
    )/(12*dx)
    result[...,0]=(
        -25*values[...,0]+48*values[...,1]-36*values[...,2]
        +16*values[...,3]-3*values[...,4]
    )/(12*dx)
    result[...,1]=(
        -3*values[...,0]-10*values[...,1]+18*values[...,2]
        -6*values[...,3]+values[...,4]
    )/(12*dx)
    result[...,-2]=(
        3*values[...,-1]+10*values[...,-2]-18*values[...,-3]
        +6*values[...,-4]-values[...,-5]
    )/(12*dx)
    result[...,-1]=(
        25*values[...,-1]-48*values[...,-2]+36*values[...,-3]
        -16*values[...,-4]+3*values[...,-5]
    )/(12*dx)
    return result

def ratio(a,b):
    a=np.asarray(a);b=np.asarray(b)
    return float(np.linalg.norm(a-b)/max(
        np.linalg.norm(a),np.linalg.norm(b),1e-300
    ))

def fixture(Nt):
    x=np.linspace(np.log(.4),0.,Nt)
    dx=float(x[1]-x[0])
    a=np.exp(x)[None,None,:]
    H=.71;tau=7.
    r=np.array([.37,.73,1.09,1.57,2.11])[:,None,None]
    w=np.array([.09,.16,.31,.25,.19])[:,None,None]
    modes=np.array([3,5,8])[None,:,None]
    omega=r/tau
    kfund=.11
    k=kfund*modes
    amp=(1+.11*r+.06*modes)*np.exp(1j*(.17*r+.13*modes))
    x3=x[None,None,:]
    P=.53+.17*x3-.039*x3**2+.012*x3**3+.006*x3**4
    P1=.17-.078*x3+.036*x3**2+.024*x3**3
    P2=-.078+.072*x3+.072*x3**2
    J=H*amp*(P1-3*P)
    Jx=H*amp*(P2-3*P1)
    z=amp*np.exp(-3*x3)*P
    zx=amp*np.exp(-3*x3)*(P1-3*P)
    v=tau*H*zx
    X=z+H*Jx/(a**3*omega**2)
    Jfrom=a**3*v/tau
    DJ=fd4(Jfrom,dx)
    R=H*DJ+a**3*omega**2*(z-X)
    Eq=-np.sqrt(w)/(2*omega)*R
    qt=np.sqrt(w)*v/(omega*tau)
    qt_exact=np.sqrt(w)*H*zx/omega
    qx=np.sqrt(w)*1j*k*z/omega
    forced_X=z
    forced_R=H*DJ+a**3*omega**2*(z-forced_X)
    forced_E=-np.sqrt(w)/(2*omega)*forced_R
    forced_qx=qx
    actual_mixed=4*forced_E*forced_qx
    analytic_pair=-2*w/omega**2*forced_R*(1j*k)*z
    wrong_sign=-4*forced_E*forced_qx
    wrong_H=DJ+a**3*omega**2*(z-X)
    natural=np.linalg.norm(H*DJ)+np.linalg.norm(a**3*omega**2*(z-X))
    result={
      "Nt":Nt,
      "nodes":5,
      "modes":[3,5,8],
      "FD4_degree4_current_relative_L2":ratio(DJ,Jx),
      "kinematic_manufactured_relative_L2":ratio(qt,qt_exact),
      "manufactured_Eq10_relative_L2_over_natural_scale":
          float(np.linalg.norm(R)/max(natural,1e-300)),
      "analytic_mode_pair_identity_relative_L2":
          ratio(actual_mixed,analytic_pair),
      "negative_omit_H_relative_defect":
          float(np.linalg.norm(wrong_H)/max(natural,1e-300)),
      "negative_wrong_Euler_sign_relative_defect":
          ratio(wrong_sign,actual_mixed),
      "all_outputs_finite":bool(all(np.isfinite(a).all()
          for a in (DJ,R,Eq,qt,qx,actual_mixed,analytic_pair))),
      "zero_node_or_weight_used":bool(np.any(r<=0) or np.any(w<=0)),
      "actual_physical_corrected_parent_loaded":False,
      "physical_fourier_convolution_performed":False,
    }
    limits={
      "FD4_degree4_current_relative_L2":1e-9,
      "kinematic_manufactured_relative_L2":1e-12,
      "manufactured_Eq10_relative_L2_over_natural_scale":1e-9,
      "analytic_mode_pair_identity_relative_L2":1e-12,
    }
    gates={name+"_within_preregistered_max":result[name]<=limit
           for name,limit in limits.items()}
    gates["negative_omit_H_control"]=(
        result["negative_omit_H_relative_defect"]>=.001)
    gates["negative_wrong_Euler_sign_control"]=(
        result["negative_wrong_Euler_sign_relative_defect"]>=.001)
    gates["no_invalid_r_or_w"]=not result["zero_node_or_weight_used"]
    gates["all_outputs_finite"]=result["all_outputs_finite"]
    result["gates"]=gates
    return result

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--json-out",required=True)
    args=ap.parse_args()
    blobs=source_blobs()
    binds,formulas,dictionary=normalized_symbolic()
    cases=[fixture(n) for n in (64,128)]
    passed=bool(
        all(x["exact"] for x in blobs.values())
        and all(binds.values()) and all(formulas.values())
        and all(all(v for v in c["gates"].values()) for c in cases)
    )
    report={
      "classification":(
        "GE19_H4F3D5_NORMALIZED_BATH_PARENT_RESIDUAL_COMPILER_PASS"
        if passed else
        "GE19_H4F3D5_NORMALIZED_BATH_PARENT_RESIDUAL_COMPILER_FAIL"
      ),
      "predata_classification":
        "GE19_H4F3D5_PREDATA_NORMALIZED_PER_NODE_BATH_PARENT_RESIDUAL_COMPILER",
      "frozen_source_blobs":blobs,
      "actual_frozen_action_bindings":binds,
      "exact_normalization_and_sign_gates":formulas,
      "compiled_normalized_parent_dictionary":dictionary,
      "manufactured_Nt64_Nt128":cases,
      "all_restricted_analytic_and_manufactured_gates_pass":passed,
      "actual_corrected_parent_arrays_loaded":False,
      "all_sector_actual_physical_Ward_derived":False,
      "H4_Z21_solve_performed":False,
      "Z21_certified":False,
      "lensing_licensed":False,
      "next_route":(
        "FREEZE_COMPILER_THEN_PREREGISTER_EXACT_PHYSICAL_PARENT_GRID_AUDIT"
        if passed else
        "FREEZE_H4F3D5_SYMBOLIC_OR_MANUFACTURED_FAILURE"
      ),
    }
    out=Path(args.json_out)
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(report,indent=2,sort_keys=True,allow_nan=False)+"\n")
    print(json.dumps(report,indent=2,sort_keys=True,allow_nan=False))
    if not passed:
        raise SystemExit(3)

if __name__=="__main__":
    main()
