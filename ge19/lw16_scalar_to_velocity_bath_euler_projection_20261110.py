#!/usr/bin/env python3
"""GE19 LW16: exact source-level NL0B bath Euler projection into theta_A.

The canonical reduced quadratic bath variation E_varphi is transformed
using the frozen AeST scalar/velocity definition varphi=Q a theta/k^2.
Its projected aether partner is compared to original CLASS E_rhs.

This is only the off-shell BATH PART of a field redefinition, and is NOT
the full AeST+NL0B scalar EOM -> fluid theta' map or a physical Ward
certificate. No CLASS runs or observational data are used.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PRE=ROOT/"ge19/lw16_scalar_to_velocity_bath_euler_projection_predata_20261110.json"
PRE_BLOB="d03d947f78b216834ca64926d369ba9c255f7fb2"
LW15_SHA256="7732d5bc13ea7ff5df2fcf9747862215954af53348d0083fe7d66c195cb527f1"

BLOBS={
  "docs/nl0b_covariant_memory_completion_result.md":
      "d005b1c135fead856510aa76b6174fb9051fa552",
  "docs/gravitational_elasticity_canonical_nl0b_interpretation.md":
      "d4a774074ad6c69142bb6f00f5426949e98ca67b",
  "v019/apply_patch_v019.py":
      "c78484eb916bfee2730759c0bdc813a706bf9a68",
  "v019j/apply_memory_patch.py":
      "14796a5ed9e6265ed6810c792a93d7328a109364",
}
ANCHORS={
 "docs/nl0b_covariant_memory_completion_result.md":[
   "**Identity 7: PASS.**",
   "\\chi\\equiv\\varphi+\\dot{\\bar\\phi}\\,\\alpha",
   "\\chi=Q(u_A+\\alpha)"],
 "v019/apply_patch_v019.py":[
   "double theta_potential_aest = a*theta_div_aest/k2;",
   "double chi_aest = Q_aest*(theta_potential_aest+alpha_aest);"],
 "v019j/apply_memory_patch.py":[
   "E_rhs_aest -= 0.5*Q_aest*Bchi_aest;",
   "Bchi_aest *= pba->aest_eta;"]
}

def require(ok,label):
    if not bool(ok):
        raise RuntimeError("GE19_LW16_"+label)

def sha(p):
    h=hashlib.sha256()
    with Path(p).open("rb") as f:
        for x in iter(lambda:f.read(1<<20),b""):
            h.update(x)
    return h.hexdigest()

def gitblob(p):
    return subprocess.check_output(["git","hash-object",str(p)],
                                   text=True).strip()

def symbolic():
    import sympy as sp
    a,k,Q,w,eta,omega,q=sp.symbols(
        "a k Q w eta omega q",positive=True,real=True)
    varphi,alpha,theta=sp.symbols("varphi alpha theta",real=True)
    kap=k/a
    chi=varphi+Q*alpha
    B=w*chi-omega*sp.sqrt(w)*q/kap
    L=-eta/sp.Integer(4)*(omega*q-sp.sqrt(w)*kap*chi)**2
    Ev=sp.factor(sp.diff(L,varphi))
    Ea=sp.factor(sp.diff(L,alpha))
    Ltheta=sp.factor(L.subs(varphi,Q*a*theta/k**2))
    Etheta=sp.factor(sp.diff(Ltheta,theta))
    projected=sp.factor((a*a/k**2)*Ea)
    projectedTheta=sp.factor(projected.subs(varphi,Q*a*theta/k**2))
    Btheta=sp.factor(B.subs(varphi,Q*a*theta/k**2))
    Hess=sp.hessian(Ltheta,[theta,alpha])
    null=sp.Matrix([k*k/a,-1])
    no_scalar=Ea
    wrong_projection=(a/k**2)*Ea
    checks={
      "E_varphi_action_variation":
         sp.simplify(Ev+eta*kap**2*B/2)==0,
      "E_alpha_equals_Q_E_varphi":
         sp.simplify(Ea-Q*Ev)==0,
      "field_redefinition_matches_CLASS_chi":
         sp.simplify(chi.subs(varphi,Q*a*theta/k**2)-
                     Q*(a*theta/k**2+alpha))==0,
      "Euler_theta_chain_rule":
         sp.simplify(Etheta-(Qa:=Q*a/k**2)*Ev.subs(
                     varphi,Q*a*theta/k**2))==0,
      "Euler_theta_equals_a_over_k2_Ealpha":
         sp.simplify(Etheta-(a/k**2)*Ea.subs(
                     varphi,Q*a*theta/k**2))==0,
      "projected_aether_source_matches_frozen_CLASS":
         sp.simplify(projected+eta*Q*B/2)==0,
      "Euler_theta_equals_projected_source_over_a":
         sp.simplify(Etheta-projectedTheta/a)==0,
      "theta_alpha_Hessian_rank_one":
         Hess.rank()==1,
      "theta_alpha_null_direction":
         all(sp.simplify(z)==0 for z in Hess*null),
      "negative_control_wrong_projection":
         sp.simplify(wrong_projection-projected)!=0,
      "negative_control_scalar_partner_missing":
         sp.simplify(no_scalar)!=0,
    }
    require(all(checks.values()),"SYMBOLIC_TEST_FAIL")
    return {
      "checks":checks,
      "sympy_version":sp.__version__,
      "action_reduced_potential":str(L),
      "varphi_Euler_source":str(Ev),
      "alpha_Euler_source":str(Ea),
      "theta_Euler_source":str(Etheta),
      "chi_in_CLASS_theta_variables":
          str(chi.subs(varphi,Q*a*theta/k**2)),
      "B_chi_in_CLASS_theta_variables":str(Btheta),
      "projected_aether_source":str(projected),
      "normalized_aether_source_in_theta":str(projectedTheta),
      "theoretical_identity":
          "E_theta=(Qa/k^2)E_varphi=(a/k^2)E_alpha=F_projected/a, F_projected=(a^2/k^2)E_alpha=-eta Q Bchi/2",
      "theta_alpha_Hessian":[[str(sp.factor(Hess[i,j]))
                              for j in range(2)] for i in range(2)],
      "theta_alpha_Hessian_rank":Hess.rank(),
      "theta_alpha_Hessian_null":["k^2/a","-1"],
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--self-test",action="store_true")
    ap.add_argument("--lw15",type=Path,default=ROOT/
        "results/ge19_lw15_effective_fluid_action_dictionary_audit_20261110.json")
    ap.add_argument("--out",type=Path,default=ROOT/
        "results/ge19_lw16_scalar_to_velocity_bath_euler_projection_20261110.json")
    args=ap.parse_args()
    result=symbolic()
    if args.self_test:
        print("GE19_LW16_REDUCED_BATH_SOURCE_PROJECTION_SELFTEST_PASS",
              len(result["checks"]),flush=True)
        return

    require(gitblob(PRE)==PRE_BLOB,"PRELOCK_HASH_CHANGED")
    pre=json.loads(PRE.read_text())
    require(pre["classification"]==
      "GE19_LW16_REDUCED_ACTION_SCALAR_TO_CLASS_VELOCITY_PROJECTION_PREDATA",
      "PREDATA_CLASS_CHANGED")
    for name,want in BLOBS.items():
        require(gitblob(ROOT/name)==want,"FROZEN_SOURCE_CHANGED_"+Path(name).name)
    anchor_status={}
    for name,needles in ANCHORS.items():
        text=(ROOT/name).read_text()
        for j,n in enumerate(needles):
            anchor_status[name+"#"+str(j+1)]=n in text
    require(all(anchor_status.values()),"ACTION_TO_CLASS_SOURCE_ANCHOR_NOT_FOUND")
    require(args.lw15.is_file() and sha(args.lw15)==LW15_SHA256,
            "ORIGINAL_WSL_LW15_CHANGED")
    j=json.loads(args.lw15.read_text())
    require(j["classification"]==
      "GE19_LW15_IMPLEMENTED_TOTAL_FLUID_JD_JT_IDENTICALLY_ZERO_ACTION_EQUIVALENCE_STILL_OPEN"
      and all(j["exact_gates"].values())
      and all(j["source_anchor_checks"].values()),"LW15_PARENT_FAIL")
    report={
      "classification":
        "GE19_LW16_BATH_SOURCE_PROJECTION_TO_THETA_PASS_FULL_ACTION_FLUID_DICTIONARY_OPEN",
      "frozen_protocol_git_blob_sha1":PRE_BLOB,
      "original_LW15_WSL_SHA256":LW15_SHA256,
      "original_source_git_blobs":BLOBS,
      "original_source_anchor_checks":anchor_status,
      **result,
      "scope":
        "Exact fixed-background one-mode bath contribution under instantaneous field redefinition only. E_theta is an Euler-source variation of the action, not the CLASS first-order theta' equation.",
      "full_AeST_scalar_Euler_action_variation":False,
      "full_covariant_metric_multiplier_auxiliary_variation":False,
      "scalar_partner_encoded_in_CLASS_fluid_independently_certified":False,
      "physical_total_action_Noether_JD_JT_verified":False,
      "full_Aeff_or_global_G_WE":False,
      "physically_admissible_two_history_Weyl_response":False,
      "DES_ACT_detection":False,
      "LW03_radial_FAIL":True,
      "LW05_LOS_BLOCK":True,
      "LW08_differential_source_UNRESOLVED":True,
      "H4_Z21_certified":False,
      "next_physical_gate":
        "Construct independent full AeST+NL0B scalar Euler-to-effective-fluid mapping including kinetic terms, aether norm and U-orthogonality multipliers, time-dependent Q,a, and constraints. Do not interpret nonzero E_theta as a missing explicit term in the conservation-form theta' equation."
    }
    out=args.out.resolve()
    require(out.parent.is_dir() and not out.exists(),
            "OUTPUT_PREEXISTS_OR_DIR_MISSING")
    out.write_text(json.dumps(report,indent=2,sort_keys=True,
                              allow_nan=False)+"\n")
    print("GE19_LW16_CLASSIFICATION",report["classification"],flush=True)
    print("GE19_LW16_REDUCED_ACTION_GATES",len(result["checks"]),flush=True)
    print("GE19_LW16_FULL_ACTION_CLOSURE",False,flush=True)
    print("GE19_LW16_OUTPUT",out,flush=True)

if __name__=="__main__":
    main()
