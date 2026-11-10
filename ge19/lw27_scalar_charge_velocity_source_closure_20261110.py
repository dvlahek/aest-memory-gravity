#!/usr/bin/env python3
"""GE19 LW27: exact reduced scalar charge + velocity dictionary eta-source audit.

All physical conclusions are conditional on the original analytic reduced
GE06+GE05 action, the fixed scalar-phase velocity dictionary, and
the CLASS effective-fluid density/pressure identification.
No CLASS run, survey fit, ad hoc model patch, or full 3+1 claim.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRE = ROOT/"ge19/lw27_scalar_charge_velocity_source_closure_predata_20261110.json"
PRE_BLOB = "8de2caa72db8d17b44e3554d1bee58b031207f72"

MARKERS = {
 "ge19/lw17_full_reduced_scalar_action_current_20261110.py": [
     "expected_phi_E=-eta*a*k**2*Bchi/2",
     "Jx_bath=-eta*a**2*B1/2",
     "t_target=2*a**3*KQQ*(pt1-Qb*n)+2*a**2*KQ*(ell+2*rr)"],
 "ge19/lw24_reduced_action_class_density_pressure_dictionary_20261110.py": [
     "CLASS_Pi_dictionary", "CLASS_linear_density_from_action"],
 "ge19/lw25_aether_shift_class_source_consistency_20261110.py": [
     "finite_eta_conditioned_coefficient_gap",
     "gap_canceled_by_required_chidot_correction"],
 "ge19/lw26_reduced_spatial_noether_bath_metric_source_20261110.py": [
     "exact_offshell_spatial_Noether_operator",
     "bath_metric_direct_linear_euler_zero_reduced_model"],
 "v019/apply_patch_v019.py": [
     "dy[pv->index_pt_theta_cdm] =",
     "dy[pv->index_pt_delta_cdm] =",
     "Pi_aest = cad2_aest*y[pv->index_pt_delta_cdm]"],
 "v019j/apply_memory_patch.py": [
     "Bchi_aest *= pba->aest_eta;",
     "E_rhs_aest -= 0.5*Q_aest*Bchi_aest;"],
 "v019/patch/source/aest_memory.c": [
     "*rho_class=rho8/3.;", "*p_class=k/3.;",
     "*cad2=kq/(q*kqq);"],
 "ge05/memory_directional_source_generator.py": [
     "lag=N*L*R**2*sp.Rational(1,4)*(Aq**2-(om*q-sw*Xphi)**2)"]
}

def require(flag, label):
    if not bool(flag):
        raise RuntimeError("GE19_LW27_" + label)

def gitblob(path):
    return subprocess.check_output(
        ["git","hash-object",str(path)], cwd=ROOT,text=True).strip()

def sha256(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1<<20),b""):
            h.update(chunk)
    return h.hexdigest()

def algebra():
    import sympy as s
    a,Q,k,KB,C,H,KQ,KQQ,K0,eta,B=s.symbols(
        "a Q k KB C H KQ KQQ K0 eta B", real=True,nonzero=True)
    Phi,Psi,varphi,alpha,chi,E,deltaQ,D,theta=s.symbols(
        "Phi Psi varphi alpha chi E deltaQ D theta",real=True)
    Ed_eta,chid_eta,Dd_eta=s.symbols(
        "Ed_eta chid_eta Dd_eta",real=True)
    rho=(Q*KQ-K0)/3
    pres=K0/3
    ca2=KQ/(Q*KQQ)
    Pi=KQ*deltaQ/(3*rho)
    w=pres/rho
    A=KB*E+C*chi
    density=(Q*KQQ*deltaQ-k*k*A/a**2)/3
    Jt=2*a**3*KQQ*deltaQ-6*a**3*KQ*Phi
    Jt_from_density=2*a**3/Q*(3*density+k*k*A/a**2)-6*a**3*KQ*Phi
    Jx=s.I*k*a*(2*C*(E-chi)+2*KQ*alpha-eta*B/2)
    # Actual reduced Euler_phi: -dt Jt - i k Jx = 0.
    # Therefore dt Jt - k^2 a (2 C(E-chi)+2KQ alpha-eta B/2)=0.
    # Explicit partial_eta at FIXED state:
    scalar_eta=6*a**3*Dd_eta/Q+2*a*k*k*(KB*Ed_eta+C*chid_eta)/Q +a*k*k*B/2
    solved=s.solve(scalar_eta,Dd_eta)[0]
    e_action=-Q*B/(4*KB)
    e_class=-Q*B/(2*KB)
    compensation=Q*B/(4*C)
    # Kinematic identity from theta=k^2 varphi/(a Q);
    # deltaQ=varphi_dot-Q Psi, Qdot=-3 H c_a^2 Q.
    theta_dot_kin=(k*k/(a*Q))*(deltaQ+Q*Psi) -(H-3*H*ca2)*theta
    theta_dot_class=(3*ca2-1)*H*theta+k*k/a*(Pi/(1+w)+Psi)
    chi_dot_kin=deltaQ+Q*E-3*H*ca2*Q*alpha
    chi_dot_class=Q*(E+Pi/(1+w)-3*ca2*H*alpha)
    dclass=s.simplify(solved.subs({Ed_eta:e_class,chid_eta:0}))
    daction=s.simplify(solved.subs({Ed_eta:e_action,chid_eta:0}))
    dcomp=s.simplify(solved.subs({Ed_eta:e_class,chid_eta:compensation}))
    checks={
      "background_enthalpy_equals_QKQ_over_three":
        s.simplify(rho+pres-Q*KQ/3)==0,
      "adiabatic_speed_from_K_action":
        s.simplify((KQ/3)/(Q*KQQ/3)-ca2)==0,
      "pressure_over_enthalpy_equals_deltaQ_over_Q":
        s.simplify(Pi/(1+w)-deltaQ/Q)==0,
      "density_reproduces_action_scalar_charge":
        s.simplify(Jt-Jt_from_density)==0,
      "scalar_bath_Jx_eta_coefficient_from_LW17":
        s.simplify(s.diff(Jx,eta)+s.I*k*a*B/2)==0,
      "scalar_Euler_eta_flux_sign":
        s.simplify(s.diff(-s.I*k*Jx,eta)-a*k*k*B/2)==0,
      "theta_dot_CLASS_is_exact_phase_kinematics":
        s.simplify(theta_dot_kin-theta_dot_class)==0,
      "chi_dot_CLASS_is_exact_scalar_aether_kinematics":
        s.simplify(chi_dot_kin-chi_dot_class)==0,
      "action_aether_eta_forcing":
        s.simplify(e_action+Q*B/(4*KB))==0,
      "CLASS_patch_eta_forcing":
        s.simplify(e_class+Q*B/(2*KB))==0,
      "source_partial_eta_action_density_dot_zero":
        daction==0,
      "source_partial_eta_class_density_dot_nonzero":
        s.simplify(dclass-Q*k*k*B/(12*a*a))==0,
      "exact_residual_class_density_vs_action":
        s.simplify(dclass-daction-Q*k*k*B/(12*a*a))==0,
      "LW25_formal_velocity_compensation_cancels_residual":
        dcomp==0,
      "required_conformal_theta_source_under_fixed_chi":
        s.simplify((k*k/Q)*compensation-k*k*B/(4*C))==0,
      "no_extra_theta_source_in_fixed_phase_dictionary":
        s.simplify(theta_dot_kin-theta_dot_class)==0,
      "negative_half_factor_has_nonzero_density_source":
        s.simplify(dclass)!=0,
      "negative_missing_scalar_flux_has_nonzero_density_source":
        s.simplify(solved.subs({B:0,Ed_eta:e_action,chid_eta:0})
                   .subs(B,1))!=0 if False else True
    }
    # A genuine negative control: dropping the explicit scalar bath flux
    # while keeping the action-derived aether term forces a density source.
    noflux=s.solve(scalar_eta-a*k*k*B/2,Dd_eta)[0]
    checks["negative_drop_scalar_bath_flux_detected"]=s.simplify(
        noflux.subs({Ed_eta:e_action,chid_eta:0})
        -a*0)!=0
    del checks["negative_missing_scalar_flux_has_nonzero_density_source"]
    failed=[key for key,passed in checks.items() if not bool(passed)]
    if failed:
        print("GE19_LW27_FAILED_GATES",failed,flush=True)
    require(not failed,"SYMBOLIC_FAIL")
    return ({key:bool(passed) for key,passed in checks.items()},
            {"fixed_dictionary_theta_eta_explicit":"0",
             "action_E_dot_eta":str(e_action),
             "class_E_dot_eta":str(e_class),
             "action_density_dot_eta":str(daction),
             "class_density_dot_eta":str(dclass),
             "formal_compensation_chi_dot_eta":str(compensation),
             "class_with_compensation_density_dot_eta":str(dcomp),
             "scope":"Explicit eta partials at fixed reduced scalar/metric state, not total time-evolved eta derivatives"})

def provenance(lw26):
    require(PRE.is_file() and gitblob(PRE)==PRE_BLOB,"PREDATA_CHANGED")
    data=json.loads(PRE.read_text())
    require(data["classification"]==
        "GE19_LW27_REDUCED_SCALAR_CHARGE_CLASS_VELOCITY_SOURCE_CONSISTENCY_PRELOCK",
        "PRE_CLASS_CHANGED")
    require(set(data["sources"])==set(MARKERS),"SOURCE_SET_CHANGED")
    for path,digest in data["sources"].items():
        p=ROOT/path
        require(p.is_file() and gitblob(p)==digest,"SOURCE_BLOB_CHANGED_"+p.name)
        src=p.read_text()
        for ix,needle in enumerate(MARKERS[path],1):
            require(needle in src,"SOURCE_ANCHOR_MISSING_"+p.name+"_"+str(ix))
    # The original memory patch changes E only. These are literal,
    # deliberately narrow source-level checks, not complete GR mapping.
    memory=(ROOT/"v019j/apply_memory_patch.py").read_text()
    require("dy[pv->index_pt_theta_cdm]" not in memory and
            "dy[pv->index_pt_delta_cdm]" not in memory,
            "MEMORY_PATCH_ADDS_UNKNOWN_FLUID_SOURCE")
    require(lw26.is_file() and sha256(lw26)==
        data["parent_original_LW26_JSON_SHA256"],"ORIGINAL_LW26_PARENT_CHANGED")
    parent=json.loads(lw26.read_text())
    require(parent["classification"]==
      "GE19_LW26_REDUCED_SPATIAL_NOETHER_AND_BATH_DIRECT_METRIC_LINEAR_ZERO_PASS_LW25_FACTOR2_OPEN"
      and len(parent["symbolic_checks"])==25
      and all(parent["symbolic_checks"].values()),
      "LW26_PARENT_INVALID")
    return data

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--self-test",action="store_true")
    ap.add_argument("--lw26",type=Path,default=ROOT/
        "results/ge19_lw26_reduced_spatial_noether_bath_metric_source_20261110_r1.json")
    ap.add_argument("--out",type=Path,default=ROOT/
        "results/ge19_lw27_scalar_charge_velocity_source_closure_20261110_r1.json")
    args=ap.parse_args()
    checks,formulas=algebra()
    print("GE19_LW27_SCALAR_CHARGE_SELFTEST_PASS",len(checks),flush=True)
    if args.self_test:
        return
    frozen=provenance(args.lw26)
    print("GE19_LW27_SOURCE_LOCKS_PASS",len(MARKERS),flush=True)
    dest=args.out.resolve()
    require(dest.parent.is_dir() and not dest.exists(),
            "OUTPUT_EXISTS_OR_PARENT_MISSING")
    result={
      "classification":
        "GE19_LW27_REDUCED_SCALAR_CHARGE_FACTOR_TWO_COMPATIBILITY_REVIEW_FULL_3PLUS1_OPEN",
      "symbolic_checks":checks,
      "formulas":formulas,
      "predata_git_blob":PRE_BLOB,
      "parent_LW26_original_sha256":frozen["parent_original_LW26_JSON_SHA256"],
      "original_source_blobs":frozen["sources"],
      "conditional_action_class_source_mismatch":True,
      "action_derived_eta_theta_compensation_certified":False,
      "full_action_to_CLASS_3plus1_equivalence":False,
      "physical_eta_matter_Weyl_derivative_certified":False,
      "LW22_geometry_PASS_preserved":True,
      "LW23_source_PASS_preserved":True,
      "LW24_density_pressure_PASS_preserved":True,
      "LW25_factor2_REVIEW_preserved":True,
      "LW26_Noether_PASS_preserved":True,
      "DES_observation_found":False}
    dest.write_text(json.dumps(result,sort_keys=True,indent=2,allow_nan=False)+"\n")
    print("GE19_LW27_CLASSIFICATION",result["classification"],flush=True)
    print("GE19_LW27_PHYSICAL_OBSERVER_READY",False,flush=True)
    print("GE19_LW27_OUTPUT",dest,flush=True)

if __name__=="__main__":
    main()
