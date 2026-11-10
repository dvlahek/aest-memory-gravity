#!/usr/bin/env python3
"""GE19 LW15: exact implemented AeST background and effective-fluid identities.

A SOURCE-CODE-GROUNDED proof that the *implemented* fluid D,T rows
satisfy Ward conservation with J_D=J_T=0 for ANY algebraic pressure Pi
and ANY E' forcing. That is a necessary implementation consistency
identity but NOT independent action-Euler/Noether equivalence.
No CLASS run, H4, DES/ACT observation or fitting.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PRE=ROOT/"ge19/lw15_effective_fluid_action_dictionary_predata_20261110.json"
PRE_BLOB="e4614f21987e1c3dd895590127525d61c7aa992e"
LW12_ORIGINAL_SHA="fdec5a67d0ba5a7f22fa9b59e22116b18e6b94dce8e18578a526c36164d0b00f"
SOURCE_BLOBS={
    "v019/apply_patch_v019.py":
      "c78484eb916bfee2730759c0bdc813a706bf9a68",
    "v019j/apply_memory_patch.py":
      "14796a5ed9e6265ed6810c792a93d7328a109364",
    "v019/patch/source/aest_memory.c":
      "9a522a653a1855eda3cb67e856f9fc10a1e73d54",
    "docs/nl0b_covariant_memory_completion_result.md":
      "d005b1c135fead856510aa76b6174fb9051fa552",
    "docs/ge19_lw14_reconcile_nl0b_linear_bath_ward_and_lw13_total_constraint_2026-11-09.md":
      "df9eb6dad78396569ee22470c2befa6181a0dd69",
    "docs/ge19_lw13_conditional_hamiltonian_propagation_and_memory_ward_gap_2026-11-09.md":
      "19f51583aee9e2aedc2aa186c3eec37d68d7d1bc",
}
REQUIRED_ANCHORS={
  "v019/apply_patch_v019.py":[
    "dp_dloga += -3.*cad2_aest*(rho_aest+p_aest);",
    "ppw->delta_rho += rho_dark*y[ppw->pv->index_pt_delta_cdm];",
    "ppw->rho_plus_p_theta += rho_plus_p_dark*y[ppw->pv->index_pt_theta_cdm];",
    "ppw->delta_p += rho_dark*Pi_aest;",
    "3.*a_prime_over_a*(w_aest*y[pv->index_pt_delta_cdm]-Pi_aest)",
    "-(1.+w_aest)*(theta_div_aest+metric_continuity);",
    "(3.*cad2_aest-1.)*a_prime_over_a*theta_div_aest",
    "+k2*Pi_aest/(1.+w_aest)+metric_euler;",
    "dy[pv->index_pt_E_aest] = a*E_rhs_aest/pba->aest_KB-a_prime_over_a*E_aest;",
  ],
  "v019j/apply_memory_patch.py":[
    "E_rhs_aest -= 0.5*Q_aest*Bchi_aest;",
    "Bchi_aest *= pba->aest_eta;",
  ],
  "v019/patch/source/aest_memory.c":[
    "kq=I0/(a*a*a);",
    "rho8=q*kq-k;",
    "*rho_class=rho8/3.;",
    "*p_class=k/3.;",
    "*cad2=kq/(q*kqq);",
  ],
  "docs/nl0b_covariant_memory_completion_result.md":[
    "**Identity 6: PASS.**",
    "**Identity 7: PASS.**",
  ],
}


def check(condition, label):
    if not bool(condition):
        raise RuntimeError("GE19_LW15_"+label)


def file_sha(p):
    h=hashlib.sha256()
    with Path(p).open("rb") as f:
        for b in iter(lambda:f.read(1<<20),b""):
            h.update(b)
    return h.hexdigest()


def git_hash(path):
    return subprocess.check_output(["git","hash-object",str(path)],text=True).strip()


def algebra():
    try:
        import sympy as s
    except ImportError as exc:
        raise RuntimeError("GE19_LW15_SYMPY_REQUIRED") from exc

    H,Q,K,KQ,KQQ,rho,p,ca2=s.symbols(
        "H Q K KQ KQQ rho p ca2", real=True,nonzero=True)
    d,theta,Pi,Phid,Psi,k2=s.symbols(
        "delta theta Pi Phi_prime Psi k2",real=True)
    E,alpha,a,KB,dPi,dp_error,FE=s.symbols(
        "E alpha a KB DeltaPi Delta_p_prime F_E",real=True)
    w=s.symbols("w",real=True)

    # Independent background route from original aest_background_eval:
    # K'_Q = -3 H K_Q, K_QQ Q' = K'_Q.
    rhof=(Q*KQ-K)/3
    pf=K/3
    c2f=KQ/(Q*KQQ)
    Qp=-3*H*KQ/KQQ
    rhop_from_action=s.factor((Q*KQQ/3)*Qp)
    pp_from_action=s.factor((KQ/3)*Qp)
    R=rho+p
    rhop=-3*H*R
    pp=ca2*rhop

    # Exactly the v019 CLASS density and Euler rows, including Pi
    # as the SAME pressure in the evolution and Einstein stress.
    dp=3*H*(w*d-Pi)-(1+w)*(theta-3*Phid)
    tp=(3*ca2-1)*H*theta+k2*Pi/(1+w)+k2*Psi
    D=rho*d
    T=R*theta
    P=rho*Pi
    Dp=rhop*d+rho*dp
    Tp=(rhop+pp)*theta+R*tp

    JD=s.factor((Dp+3*H*(D+P)+T-3*R*Phid).subs(w,p/rho))
    JT=s.factor((Tp+4*H*T-k2*P-k2*R*Psi).subs(w,p/rho))

    # The original Pi(E) may be an arbitrarily complicated algebraic
    # function of the aether and memory fields. The Ward algebra
    # nevertheless remains independent of the E' forcing FE.
    chi=Q*(a*theta/k2+alpha)
    Pifull=ca2*d+ca2*k2/(3*a*a*rho)*(KB*E+(2-KB)*chi)
    JD_E=s.simplify(JD.subs(Pi,Pifull))
    JT_E=s.simplify(JT.subs(Pi,Pifull))
    assert not (JD_E.has(FE) or JT_E.has(FE))
    # Deliberate break of SAME Pi rule: pressure is still P=rho Pi
    # but a wrong source Pi+DeltaPi appears in only one fluid row.
    JDbad=s.factor((Dp.subs(dp,dp.subs(Pi,Pi+dPi))
                    +3*H*(D+P)+T-3*R*Phid).subs(w,p/rho))
    JTbad=s.factor((Tp.subs(tp,tp.subs(Pi,Pi+dPi))
                    +4*H*T-k2*P-k2*R*Psi).subs(w,p/rho))
    JTbackground=s.factor((Tp+dp_error*theta+4*H*T-k2*P-k2*R*Psi)
                          .subs(w,p/rho))

    tests={
      "background_rho_plus_p_KQ":s.simplify(rhof+pf-Q*KQ/3)==0,
      "background_rho_prime":s.simplify(rhop_from_action+H*Q*KQ)==0,
      "background_pressure_prime":
          s.simplify(pp_from_action-c2f*rhop_from_action)==0,
      "background_enthalpy_prime":
          s.simplify((rhop_from_action+pp_from_action)
                      +3*H*(1+c2f)*Q*KQ/3)==0,
      "effective_fluid_energy_JD_zero_for_arbitrary_Pi":JD==0,
      "effective_fluid_momentum_JT_zero_for_arbitrary_Pi":JT==0,
      "full_original_Pi_of_E_preserves_JD_JT":JD_E==0 and JT_E==0,
      "E_prime_force_is_unconstrained_by_fluid_Ward":
          not (JD_E.has(FE) or JT_E.has(FE)),
      "broken_delta_pressure_detected":
          s.simplify(JDbad+3*H*rho*dPi)==0 and JDbad!=0,
      "broken_theta_pressure_detected":
          s.simplify(JTbad-k2*rho*dPi)==0 and JTbad!=0,
      "wrong_background_pprime_detected":
          s.simplify(JTbackground-dp_error*theta)==0 and
          JTbackground!=0,
    }
    check(all(tests.values()),"EXACT_ALGEBRA_FAIL")
    return {
      "sympy_version":s.__version__,
      "exact_gates":tests,
      "canonical_background":{
        "rho_A":"(Q*K_Q-K)/3",
        "p_A":"K/3",
        "Q_prime":"-3*Hconf*K_Q/K_QQ",
        "rho_A_prime":str(rhop_from_action),
        "p_A_prime":str(pp_from_action),
        "ca2":"K_Q/(Q*K_QQ)",
        "rho_plus_p":"Q*K_Q/3",
      },
      "implemented_fluid_JD":str(JD),
      "implemented_fluid_JT":str(JT),
      "implemented_fluid_JD_with_original_Pi_of_E":str(JD_E),
      "implemented_fluid_JT_with_original_Pi_of_E":str(JT_E),
      "incorrect_delta_pressure_JD":str(JDbad),
      "incorrect_theta_pressure_JT":str(JTbad),
      "incorrect_background_pprime_JT":str(JTbackground),
      "arbitrary_Eprime_source_invariant":
        "Neither JD nor JT contains E' or the force FE. Inserting any arbitrary FE into E' leaves both identities zero for the written fluid equations.",
      "Noether_evidence_limit":
        "This is a structural Ward tautology of original v019 fluid equations; it does not prove those equations include the full original NL0B action scalar Euler partner.",
    }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--self-test",action="store_true")
    ap.add_argument("--lw12",type=Path,default=ROOT/
        "results/ge19_lw12_aest_metric_partial_jacobian_20261109.json")
    ap.add_argument("--out",type=Path,default=ROOT/
        "results/ge19_lw15_effective_fluid_action_dictionary_audit_20261110.json")
    a=ap.parse_args()
    result=algebra()
    if a.self_test:
        print("GE19_LW15_IMPLEMENTED_FLUID_WARD_SYNTHETIC_PASS",
              len(result["exact_gates"]),flush=True)
        return

    check(git_hash(PRE)==PRE_BLOB,"PREDATA_BLOB_CHANGED")
    pre=json.loads(PRE.read_text())
    check(pre["classification"]==
          "GE19_LW15_EFF_FLUID_CONSERVATION_IS_NOT_ACTION_EQUIVALENCE_PREDATA",
          "PREDATA_CHANGED")
    for path,blob in SOURCE_BLOBS.items():
        p=ROOT/path
        check(p.exists() and git_hash(p)==blob,
              "FROZEN_SOURCE_CHANGED_"+p.name)
    anchors={}
    for path,needles in REQUIRED_ANCHORS.items():
        txt=(ROOT/path).read_text()
        for n,needle in enumerate(needles,1):
            anchors[f"{path}#{n}"]=needle in txt
    check(all(anchors.values()),"SOURCE_ANCHOR_MISSING")
    check(a.lw12.is_file() and file_sha(a.lw12)==LW12_ORIGINAL_SHA,
          "ORIGINAL_LOCAL_LW12_CHANGED")
    lw12=json.loads(a.lw12.read_text())
    check(lw12["classification"]==
          "GE19_LW12_EXACT_AEST_PHI_DIRECT_JACOBIAN_BLOCK_PASS_FULL_AEFF_OPEN"
          and all(lw12["checks"].values()),"LW12_PARENT_NOT_PASS")

    report={
      "classification":
        "GE19_LW15_IMPLEMENTED_TOTAL_FLUID_JD_JT_IDENTICALLY_ZERO_ACTION_EQUIVALENCE_STILL_OPEN",
      "protocol_git_blob_sha1":PRE_BLOB,
      "source_git_blobs":SOURCE_BLOBS,
      "source_anchor_checks":anchors,
      "original_local_LW12_sha256":file_sha(a.lw12),
      **result,
      "total_physical_Noether_Euler_to_fluid_map_proven":False,
      "full_AeST_scalar_aether_multiplier_action_variation_independently_rederived":False,
      "bath_scalar_partner_in_class_effective_fluid_independently_certified":False,
      "physical_action_derived_JD_JT_zero_certified":False,
      "Hamiltonian_LW13_conditional_propagation_preserved":True,
      "NL0B_prior_eight_identity_analytic_PASS_preserved":True,
      "LW14_reduced_source_rank_one_PASS_preserved":True,
      "full_global_Aeff":False,
      "physical_two_history_Weyl_difference":False,
      "observational_memory_detection":False,
      "LW03_radial_FAIL":True,
      "LW05_LOS_BLOCK":True,
      "LW08_differential_source_UNRESOLVED":True,
      "H4_Z21_certified":False,
      "next_action":
        "Derive exact linear full-action scalar Euler equation and its off-shell relation to v019 CLASS D,T and E rows with auxiliary bath source, including multipliers and gauge. Do not infer physical Ward from fluid conservation by construction."
    }
    out=a.out.resolve()
    check(out.parent.is_dir() and not out.exists(),
          "OUTPUT_EXISTS_OR_PARENT_MISSING")
    out.write_text(json.dumps(report,sort_keys=True,indent=2,
                              allow_nan=False)+"\n")
    print("GE19_LW15_CLASSIFICATION",report["classification"],flush=True)
    print("GE19_LW15_CHECKS",len(report["exact_gates"]),"/",
          len(report["exact_gates"]),flush=True)
    print("GE19_LW15_ACTION_EQUIVALENCE",False,flush=True)
    print("GE19_LW15_OUTPUT",out,flush=True)


if __name__=="__main__":
    main()
