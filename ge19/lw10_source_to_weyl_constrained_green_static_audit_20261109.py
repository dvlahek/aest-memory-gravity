#!/usr/bin/env python3
"""GE19 LW10 — pinned read-only source audit of AeST E -> Weyl pathway.

Reconstructs the *structural* Einstein+AeST linear source/observer map from
the original AeST patch source plus the official CLASS original at its pinned
commit. It does NOT calculate the retarded Green matrix, solve ODEs, prove
two physically admissible histories, or inspect observational residuals.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PRE=ROOT/"ge19/lw10_source_to_weyl_constrained_green_predata_20261109.json"
PRE_BLOB="ace64f2f8d60186ee1c261e83474ecfb38dd7918"

PIN="e85808324f51fc694d12e3ed7439552a3c3f9540"
OFFICIAL_PERTURBATIONS_BLOB="c78fe4376d2eeebfbf4ff0cfca13b048d4513fa0"
PATCH_BLOBS={
    "v019/apply_patch_v019.py":
        "c78484eb916bfee2730759c0bdc813a706bf9a68",
    "v019j/apply_memory_patch.py":
        "14796a5ed9e6265ed6810c792a93d7328a109364",
    "v019w/apply_variational_forcing_patch.py":
        "00c3f5da5a1b7734c67c82aa9181a443736101bf",
}

SOURCE_ANCHORS={
    "Einstein_psi_phi_anisotropic_shear":
      "ppw->pvecmetric[ppw->index_mt_psi] = y[ppw->pv->index_pt_phi] - 4.5 * (a2/k2) * ppw->rho_plus_p_shear;",
    "Einstein_phi_prime_momentum":
      "ppw->pvecmetric[ppw->index_mt_phi_prime] = -a_prime_over_a * ppw->pvecmetric[ppw->index_mt_psi] + 1.5 * (a2/k2) * ppw->rho_plus_p_theta;",
    "Einstein_phi_state_ODE":
      "dy[pv->index_pt_phi] = pvecmetric[ppw->index_mt_phi_prime];",
}
AE_PATCH_ANCHORS={
    "AeST_pressure_closure_E":
      "pba->aest_KB*E_aest+(2.-pba->aest_KB)*chi_aest",
    "AeST_pressure_in_Einstein_stress":
      "ppw->delta_p += rho_dark*Pi_aest;",
    "AeST_theta_prime_pressure":
      "+k2*Pi_aest/(1.+w_aest)+metric_euler;",
    "AeST_delta_prime_pressure":
      "3.*a_prime_over_a*(w_aest*y[pv->index_pt_delta_cdm]-Pi_aest)",
    "AeST_alpha_prime_E":
      "dy[pv->index_pt_alpha_aest] = a*(E_aest-psi_aest);",
    "AeST_Pi_prefactor":
      "cad2_aest*k2/(3.*a*a*rho_aest)",
    "AeST_chi_dictionary":
      "double chi_aest = Q_aest*(theta_potential_aest+alpha_aest);",
}
MEM_PATCH_ANCHORS={
    "physical_E_source":
      "E_rhs_aest -= 0.5*Q_aest*Bchi_aest;",
}
VAR_PATCH_ANCHORS={
    "physical_eta_tangent_trace":
      "aest_tangent_trace_force(k,tau,-0.5*a*Q_aest*Braw_aest/pba->aest_KB);",
    "actual_external_source_in_Eprime":
      "dy[pv->index_pt_E_aest] += aest_tangent_external_force(k,tau);",
}


def run(*argv):
    return subprocess.check_output(argv,text=True).strip()


def checked(text, anchors, prefix):
    return {prefix+name: (text.count(needle)>=1)
            for name,needle in anchors.items()}


def selftest():
    # Pure algebra tests of the correct code-implemented partial derivatives.
    a,k,rho,ca2,KB,w,Hconf=0.8,0.09,1.7,0.012,0.0665,0.03,0.04
    dPi=ca2*KB*k*k/(3*a*a*rho)
    dtheta=k*k*dPi/(1+w)
    ddelta=-3*Hconf*dPi
    assert dPi>0 and dtheta>0 and ddelta<0
    assert abs(dtheta-(ca2*KB*k**4/(3*a*a*rho*(1+w))))<1e-16
    assert abs(ddelta+(Hconf*ca2*KB*k*k/(a*a*rho)))<1e-16
    print("GE19_LW10_JACOBIAN_CHAIN_SYNTHETIC_SELFTEST_PASS",flush=True)


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--self-test",action="store_true")
    p.add_argument("--class-root",type=Path)
    p.add_argument("--out",type=Path,default=
       ROOT/"results/ge19_lw10_source_to_weyl_constrained_green_static_audit_20261109.json")
    args=p.parse_args()
    if args.self_test:
        selftest()
        return
    if args.class_root is None:
        raise RuntimeError("GE19_LW10_CLASS_ROOT_REQUIRED")
    class_root=args.class_root.resolve()
    assert run("git","hash-object",str(PRE))==PRE_BLOB, "PRELOCK_CHANGED"
    pre=json.loads(PRE.read_text())
    assert pre["classification"]=="GE19_LW10_ACTION_BRIDGE_E_SOURCE_TO_WEYL_STRUCTURAL_PRELOCK"
    head=run("git","-C",str(class_root),"rev-parse","HEAD")
    assert head==PIN, "CLASS_HEAD_CHANGED"
    orig_blob=run("git","-C",str(class_root),"rev-parse",
                  "HEAD:source/perturbations.c")
    assert orig_blob==OFFICIAL_PERTURBATIONS_BLOB, "ORIGINAL_CLASS_BLOB_CHANGED"

    paths={r:ROOT/r for r in PATCH_BLOBS}
    for name,path in paths.items():
        assert run("git","hash-object",str(path))==PATCH_BLOBS[name],(
            "AeST historical patch changed: "+name)

    official=run("git","-C",str(class_root),"show",
                 "HEAD:source/perturbations.c")
    first=paths["v019/apply_patch_v019.py"].read_text()
    memory=paths["v019j/apply_memory_patch.py"].read_text()
    tangent=paths["v019w/apply_variational_forcing_patch.py"].read_text()
    patched=(class_root/"source/perturbations.c").read_text()
    checks={}
    checks.update(checked(official,SOURCE_ANCHORS,"pinned_official_"))
    checks.update(checked(first,AE_PATCH_ANCHORS,"original_AeST_patch_"))
    checks.update(checked(memory,MEM_PATCH_ANCHORS,"positive_bath_patch_"))
    checks.update(checked(tangent,VAR_PATCH_ANCHORS,"external_source_patch_"))
    checks.update(checked(patched,AE_PATCH_ANCHORS,"actual_worktree_"))
    checks.update(checked(patched,MEM_PATCH_ANCHORS,"actual_worktree_"))
    checks.update(checked(patched,VAR_PATCH_ANCHORS,"actual_worktree_"))
    checks.update(checked(patched,SOURCE_ANCHORS,"actual_worktree_"))
    passed=bool(checks) and all(checks.values())
    verdict=(pre["outcome_labels"]["structural_pass"] if passed
             else pre["outcome_labels"]["structural_fail"])
    report={
        "classification":verdict,
        "predata_git_blob_sha1":PRE_BLOB,
        "class_git_HEAD":head,
        "official_pinned_perturbations_git_blob_sha1":orig_blob,
        "patch_git_blob_sha1":PATCH_BLOBS,
        "static_exact_text_anchor_checks":checks,
        "all_static_source_anchors_pass":passed,
        "source_entry":"E'_eta|0 = -a*Q*Bchi_raw/(2*K_B)",
        "direct_pressure_to_E_derivative":
            "dPi/dE=c_a^2*K_B*k^2/(3*a^2*rho_A)",
        "direct_AeST_theta_prime_to_E_derivative":
            "dtheta_A'/dE=c_a^2*K_B*k^4/[3*a^2*rho_A*(1+w_A)]",
        "direct_AeST_delta_prime_to_E_derivative":
            "ddelta_A'/dE=-Hconf*c_a^2*K_B*k^2/(a^2*rho_A)",
        "direct_alpha_prime_to_E_derivative":"dalpha_A'/dE=a",
        "metric_constraints":
            ["Psi=Phi-(9/2)*a^2/k^2*Sigma_shear",
             "Phi'=-Hconf*Psi+(3/2)*a^2/k^2*Sigma_momentum"],
        "formal_source_to_weyl_Green":
            "G_WE(k;t,s) = C_W(k,t)*Texp[integral_s^t A_eff(k,u) du]*e_E",
        "A_eff_Jacobian_assembled_from_actual_CLASS":False,
        "full_Einstein_AeST_observer_green_evaluated":False,
        "two_history_full_dynamical_admissibility_certified":False,
        "nonzero_W_difference_for_history_pair_certified":False,
        "original_LW01_native_W_tangent_PASS_preserved":True,
        "original_LW03_radial_FAIL_preserved":True,
        "original_LW05_cosmic_shear_LOS_BLOCK_preserved":True,
        "original_LW08_differential_tangent_UNRESOLVED_preserved":True,
        "H4_Z21_certified":False,
        "observational_detection":False,
        "class_solver_executed":False,
        "interpretation":
            "Only implemented equation-source structural pathway. Does not prove retarded observer kernel nonzero for arbitrary histories or physically admissible paired cosmologies.",
    }
    out=args.out.resolve()
    assert out.parent.is_dir() and not out.exists(), "OUTPUT_EXISTS_OR_DIRECTORY_MISSING"
    out.write_text(json.dumps(report,sort_keys=True,indent=2)+"\n")
    print("GE19_LW10_CLASSIFICATION",verdict,flush=True)
    print("GE19_LW10_STATIC_ANCHORS",
          sum(checks.values()),"/",len(checks),flush=True)
    print("GE19_LW10_FULL_GREEN_CERTIFIED",False,flush=True)
    print("GE19_LW10_OUTPUT",out,flush=True)


if __name__=="__main__":
    main()
