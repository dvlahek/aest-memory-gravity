#!/usr/bin/env python3
"""GE19 LW14: exact reduced NL0B quadratic-source Ward re-audit.

This is an explicit formula-level recheck of already-published NL0B
Identity 7. It does NOT independently vary the entire covariant action,
derive the complete AeST effective-fluid dictionary or prove that the
modified CLASS approximations satisfy physical J_D=J_T=0.

No CLASS solver, DES data, H4 or numerical fitting.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PRE=ROOT/"ge19/lw14_linear_covariant_bath_scalar_aether_ward_predata_20261109.json"
PRE_BLOB="b81c6399ae18ef609a40043fcd946a4b101e9826"
SOURCE_BLOBS={
  "docs/nl0b_predata_covariant_memory_completion.md":
      "9b1c013153faeddbd2add3d80eb29f673bc7748f",
  "docs/nl0b_covariant_memory_completion_result.md":
      "d005b1c135fead856510aa76b6174fb9051fa552",
  "docs/gravitational_elasticity_canonical_nl0b_interpretation.md":
      "d4a774074ad6c69142bb6f00f5426949e98ca67b",
  "v019j/apply_memory_patch.py":
      "14796a5ed9e6265ed6810c792a93d7328a109364",
  "v019/apply_patch_v019.py":
      "c78484eb916bfee2730759c0bdc813a706bf9a68",
  "docs/ge19_lw13_conditional_hamiltonian_propagation_and_memory_ward_gap_2026-11-09.md":
      "19f51583aee9e2aedc2aa186c3eec37d68d7d1bc",
}
def require(condition,label):
    if not bool(condition):
        raise RuntimeError("GE19_LW14_"+label)

def exact_symbolics():
    try:
        import sympy as sp
    except ImportError as e:
        raise RuntimeError("GE19_LW14_SYMPY_REQUIRED") from e
    varphi,alpha,q,Q,kap,omega,weight,eta=sp.symbols(
        "varphi alpha q Q kappa omega w eta",
        positive=True,real=True)
    chi=varphi+Q*alpha
    x=kap*chi
    mismatch=omega*q-sp.sqrt(weight)*x
    # The physical U_j=sqrt(eta)q_j gives overall eta after
    # eliminating the normalization from the quadratic potential.
    Lpot=-eta*mismatch**2/sp.Integer(4)
    Bchi=weight*chi-omega*sp.sqrt(weight)*q/kap
    Evar=sp.diff(Lpot,varphi)
    Ealpha=sp.diff(Lpot,alpha)
    H=sp.hessian(Lpot,[varphi,alpha])
    null=sp.Matrix([-Q,1])
    null_result=H*null
    original_Evar=-eta*kap**2*Bchi/2
    # Deliberately wrong model: add aether source without required scalar
    # partner. This must NOT satisfy the source Ward identity.
    negative=sp.factor(Ealpha-Q*0)
    # Nontrivial one-mode bath source only (finite theta/eta etc).
    checks={
       "chi_only_invariant_direction":
         sp.simplify(sp.diff(chi,alpha)-Q*sp.diff(chi,varphi))==0,
       "exact_backreaction_variation":
         sp.simplify(Evar-original_Evar)==0,
       "aether_scalar_source_proportionality":
         sp.simplify(Ealpha-Q*Evar)==0,
       "Hessian_rank_one": H.rank()==1,
       "Hessian_null_vector_all_jets":
         all(sp.simplify(t)==0 for t in null_result),
       "negative_control_missing_scalar_partner":
         sp.simplify(negative)!=0,
       "potential_quadratic_no_linear_perturbation_term":
         sp.diff(Lpot.subs({varphi:sp.Symbol("t")*varphi,
                           alpha:sp.Symbol("t")*alpha,
                           q:sp.Symbol("t")*q}),
                 sp.Symbol("t")).subs(sp.Symbol("t"),0)==0
    }
    require(all(checks.values()),"REDUCED_SOURCE_IDENTITY_FAIL")
    return {
      "sympy_version":sp.__version__,
      "checks":checks,
      "symbols":{"chi":str(chi),"X_L":str(x),
                 "mismatch":str(mismatch),
                 "Bchi":str(Bchi)},
      "normalized_single_mode_L_potential":str(Lpot),
      "Euler_varphi":str(sp.factor(Evar)),
      "Euler_alpha":str(sp.factor(Ealpha)),
      "Euler_varphi_backreaction":
          "-eta*kappa**2*Bchi/2",
      "Euler_alpha_minus_Q_Euler_varphi":
          str(sp.simplify(Ealpha-Q*Evar)),
      "Hessian": [[str(H[i,j]) for j in range(2)]
                    for i in range(2)],
      "Hessian_rank":H.rank(),
      "Hessian_null_direction":["-Q","1"],
      "negative_control_aether_source_no_scalar":
          str(negative),
      "source_potential_projection_note":
          "The reduced spatial-mode potential variation includes kappa^2=(k/a)^2; the CLASS aether scalar-potential E_rhs uses the original field-equation spatial projection/normalization. Do not equate unnormalized Euler coefficients directly.",
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--self-test",action="store_true")
    ap.add_argument("--out",type=Path,default=
      ROOT/"results/ge19_lw14_linear_covariant_bath_scalar_aether_ward_20261109.json")
    a=ap.parse_args()
    algebra=exact_symbolics()
    if a.self_test:
        print("GE19_LW14_REDUCED_SOURCE_WARD_SELFTEST_PASS",
              len(algebra["checks"]),flush=True)
        return
    blob=subprocess.check_output(["git","hash-object",str(PRE)],
                                 text=True).strip()
    require(blob==PRE_BLOB,"PRELOCK_CHANGED")
    protocol=json.loads(PRE.read_text())
    require(protocol["classification"]==
      "GE19_LW14_OLD_NL0B_LINEAR_WARD_OBLIGATION_REVISIT_PRELOCK",
      "PROTOCOL_CHANGED")
    for path,b in SOURCE_BLOBS.items():
        actual=subprocess.check_output(
            ["git","hash-object",str(ROOT/path)],text=True).strip()
        require(actual==b,"SOURCE_BLOB_CHANGED_"+Path(path).name)
    prior=(ROOT/"docs/nl0b_covariant_memory_completion_result.md").read_text()
    patch=(ROOT/"v019j/apply_memory_patch.py").read_text()
    require("**Identity 7: PASS.**" in prior and
            "NL0B_COVARIANT_MEMORY_COMPLETION_PASS" in prior,
            "PREVIOUS_NL0B_PASS_NOT_PRESERVED")
    require("E_rhs_aest -= 0.5*Q_aest*Bchi_aest;" in patch,
            "CLASS_E_SOURCE_NOT_FOUND")
    result={
      "classification":
        "GE19_LW14_REDUCED_LINEAR_BATH_SCALAR_AETHER_WARD_PASS_TOTAL_ACTION_CLOSURE_OPEN",
      "prior_known_NL0B_identity7_pass":True,
      "novelty_claim":"none: checks and isolates already known frozen linear bath source redundancy",
      "protocol_git_blob_sha1":PRE_BLOB,
      "source_git_blobs":SOURCE_BLOBS,
      **algebra,
      "covariant_action_metric_variation_full_recomputed":False,
      "no_direct_linear_bath_stress_newly_certified":False,
      "no_direct_linear_bath_stress_existing_NL0B":True,
      "total_AeST_NL0B_Noether_map_to_CLASS_fluid_verified":False,
      "total_linear_J_D_J_T_measured_from_action":False,
      "linear_CLASS_E_and_scalar_partner_implementation_closure_verified":False,
      "Hamiltonian_Ward_conditional_LW13_preserved":True,
      "full_global_Aeff_closed":False,
      "full_metric_Green_evaluated":False,
      "physically_admissible_two_history_observer":False,
      "observational_memory_detection":False,
      "LW03_radial_FAIL":True,
      "LW05_full_LOS_BLOCK":True,
      "LW08_differential_source_UNRESOLVED":True,
      "H4_Z21_certified":False,
      "exact_remaining_task":
        "Audit original action-level scalar Euler-to-effective fluid dictionary, including the bath scalar partner and the exact total Einstein stress at linear order; derive J_D,J_T for the actual CLASS state variables rather than setting them zero because its Euler equations look conservative."
    }
    output=a.out.resolve()
    require(output.parent.is_dir() and not output.exists(),
            "OUTPUT_PREEXISTS_OR_DIR_MISSING")
    output.write_text(json.dumps(result,indent=2,sort_keys=True,
                                 allow_nan=False)+"\n")
    print("GE19_LW14_CLASSIFICATION",result["classification"],flush=True)
    print("GE19_LW14_REDUCED_WARD_GATES",len(algebra["checks"]),
          "PASS",flush=True)
    print("GE19_LW14_COMPLETE_ACTION_WARD_CERTIFIED",False,flush=True)
    print("GE19_LW14_OUTPUT",output,flush=True)

if __name__=="__main__":
    main()
