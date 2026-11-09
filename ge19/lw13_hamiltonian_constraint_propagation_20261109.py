#!/usr/bin/env python3
"""GE19 LW13: conditional flat-FLRW total-fluid Hamiltonian Ward identity.

Mathematically exact in the original CLASS Newtonian scalar sign and
normalization convention under CONSERVED TOTAL stress. Does NOT certify
action-level AeST+NL0B Noether/Ward identities, CLASS approximation
branches, numerical constraint residuals, physical paired histories,
or DES/ACT observations. No CLASS solver runs.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PRE=ROOT/"ge19/lw13_hamiltonian_constraint_propagation_protocol_20261109.json"
PRE_BLOB="859e2a2c2f65008987c342c2ed51437b7ebf5949"
INPUT_SHA={
    "lw10":"10e8dd7f3eaa988a48966ce7892e1da653f4215c4ce09499a4c62981cf350851",
    "lw12":"fdec5a67d0ba5a7f22fa9b59e22116b18e6b94dce8e18578a526c36164d0b00f",
}

def require(ok,label):
    if not bool(ok):
        raise RuntimeError("GE19_LW13_"+label)

def sha(p):
    h=hashlib.sha256()
    with Path(p).open("rb") as f:
        for b in iter(lambda:f.read(1<<20),b""):
            h.update(b)
    return h.hexdigest()

def symbolics():
    try:
        import sympy as sp
    except ImportError as e:
        raise RuntimeError("GE19_LW13_SYMPY_REQUIRED: pip install sympy") from e

    a,H,k2,D,P,T,R,Phi,S,JD,JT=sp.symbols(
        "a H k2 D P T R Phi S J_D J_T",real=True,nonzero=True)
    psi=Phi-sp.Rational(9,2)*a**2*S/k2
    phip=-H*psi+sp.Rational(3,2)*a**2*T/k2
    Dp=-3*H*(D+P)-T+3*R*phip+JD
    Tp=-4*H*T+k2*P+k2*R*psi-k2*S+JT
    Hp=H**2-sp.Rational(3,2)*a**2*R

    # Flat-FLRW Hamiltonian scalar constraint as directly present in
    # pinned CLASS perturbations.c Newtonian-gauge comment.
    C=k2*Phi+sp.Rational(3,2)*a**2*(D+3*H*T/k2)

    # Differentiate C without treating independent total-fluid fields
    # as time constants: a'=a*H, Phi'=phip, H'=Hp, etc.
    Cp=k2*phip + sp.Rational(3,2)*a**2 * (2*H*D+Dp)
    Cp+=sp.Rational(9,2)*a**2/k2 * ((2*H**2+Hp)*T+H*Tp)
    predicted=(
        sp.Rational(3,2)*a**2*JD+
        sp.Rational(9,2)*a**2*H*JT/k2
    )
    actual=sp.factor(sp.expand(Cp+H*C))
    residual=sp.simplify(actual-predicted)
    free=sp.simplify(actual.subs({JD:0,JT:0}))
    checks={
        "full_source_identity_exact":residual==0,
        "source_free_constraint_propagation_exact":free==0,
        "J_D_coefficient":sp.simplify(sp.diff(actual,JD)-
            sp.Rational(3,2)*a**2)==0,
        "J_T_coefficient":sp.simplify(sp.diff(actual,JT)-
            sp.Rational(9,2)*a**2*H/k2)==0,
        "pressure_cancels":sp.simplify(sp.diff(actual,P))==0,
        "anisotropic_shear_cancels":sp.simplify(sp.diff(actual,S))==0,
        "density_and_momentum_background_cancel":
            sp.simplify(actual-predicted)==0,
    }
    require(all(checks.values()),"SYMBOLIC_IDENTITY_FAIL")
    return {
        "checks":checks,
        "symbols":["a","H=a_prime/a","k2","D=delta_rho_total",
                   "P=delta_p_total","T=total_rho_plus_p_theta",
                   "S=total_rho_plus_p_shear","R=rho_plus_p",
                   "Phi","Psi","J_D","J_T"],
        "hamiltonian_constraint":
          "C=k2*Phi+(3/2)*a^2*(D+3*H*T/k2), K=0",
        "Einstein_psi":"Psi=Phi-(9/2)*a^2*S/k2",
        "Einstein_phi_prime":
          "Phi'=-H*Psi+(3/2)*a^2*T/k2",
        "background_H_prime":"H'=H^2-(3/2)*a^2*R",
        "total_D_prime":
          "D'=-3*H*(D+P)-T+3*R*Phi'+J_D",
        "total_T_prime":
          "T'=-4*H*T+k2*P+k2*R*Psi-k2*S+J_T",
        "exact_derived_identity":
          "C'=-H*C+(3/2)*a^2*J_D+(9/2)*a^2*H*J_T/k2",
        "free_conservation_solution":
          "if J_D=J_T=0, C(tau)=C(tau_i)*a(tau_i)/a(tau)",
        "computed_Cprime_plus_HC":str(actual),
        "SymPy_version":sp.__version__,
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--self-test",action="store_true")
    ap.add_argument("--lw10",type=Path,default=ROOT/
        "results/ge19_lw10_source_to_weyl_constrained_green_static_audit_20261109.json")
    ap.add_argument("--lw12",type=Path,default=ROOT/
        "results/ge19_lw12_aest_metric_partial_jacobian_20261109.json")
    ap.add_argument("--out",type=Path,default=ROOT/
        "results/ge19_lw13_hamiltonian_constraint_propagation_20261109.json")
    args=ap.parse_args()

    formal=symbolics()
    if args.self_test:
        print("GE19_LW13_TOTAL_FLUID_HAMILTONIAN_IDENTITY_SELFTEST_PASS",
              "gates",len(formal["checks"]),flush=True)
        return

    pre_git=subprocess.check_output(["git","hash-object",str(PRE)],
                                    text=True).strip()
    require(pre_git==PRE_BLOB,"PRE_LOCK_BLOB_CHANGED")
    pre=json.loads(PRE.read_text())
    require(pre["classification"]==
        "GE19_LW13_TOTAL_FLUID_HAMILTONIAN_CONSTRAINT_IDENTITY_FORMULA_FROZEN",
        "PRE_CLASSIFICATION_CHANGED")
    for key,p in (("lw10",args.lw10),("lw12",args.lw12)):
        require(p.exists() and sha(p)==INPUT_SHA[key],
                "PARENT_SHA_CHANGED_"+key)
    lw10=json.loads(args.lw10.read_text())
    lw12=json.loads(args.lw12.read_text())
    require(lw10["all_static_source_anchors_pass"] and
            not lw10["class_solver_executed"],"LW10_PARENT_INVALID")
    require(lw12["classification"]==
        "GE19_LW12_EXACT_AEST_PHI_DIRECT_JACOBIAN_BLOCK_PASS_FULL_AEFF_OPEN"
        and all(lw12["checks"].values())
        and not lw12["global_Aeff_closed"],
        "LW12_PARENT_INVALID")

    result={
        "classification":
          "GE19_LW13_CONDITIONAL_TOTAL_CONSERVATION_HAMILTONIAN_PROPAGATION_IDENTITY_PASS_ACTION_WARD_OPEN",
        "protocol_git_blob_sha1":PRE_BLOB,
        "input_SHA256":{x:sha(p) for x,p in
            [("lw10",args.lw10),("lw12",args.lw12)]},
        **formal,
        "conservation_requirement":
          "Total effective delta rho and momentum MUST satisfy the stated exact linear conservation laws and original flat-FLRW background. This is an assumption of this identity, not an action-level verification.",
        "modified_AeST_memory_equation_source":
          "E_aest' receives F_E; the original effective-fluid delta_A' and theta_A' are built as conservation equations with Pi_A and no independent direct J_D,J_T.",
        "action_level_Noether_identity_certified":False,
        "actual_memory_bath_linear_Einstein_stress_complete":False,
        "CLASS_branch_approximation_residuals_tested":False,
        "all_other_species_feedback_in_Aeff":False,
        "full_global_retarded_G_WE":False,
        "two_physical_histories_metric_difference":False,
        "DES_ACT_detection":False,
        "LW03_radial_FAIL_preserved":True,
        "LW05_LOS_BLOCK_preserved":True,
        "LW08_differential_response_UNRESOLVED_preserved":True,
        "H4_Z21_certified":False,
        "interpretation":
          "Conditional continuum constraint-propagation theorem. Does not independently certify physical NL0B Noether consistency, branch-by-branch numerical CLASS Ward conservation, or gravitational-memory observational discovery."
    }
    path=args.out.resolve()
    require(path.parent.is_dir() and not path.exists(),
            "OUTPUT_ALREADY_EXISTS_OR_PARENT_MISSING")
    path.write_text(json.dumps(result,sort_keys=True,indent=2,
                               allow_nan=False)+"\n")
    print("GE19_LW13_CLASSIFICATION",result["classification"],flush=True)
    print("GE19_LW13_GATES",len(formal["checks"]),"/",
          len(formal["checks"]),"PASS",flush=True)
    print("GE19_LW13_FULL_ACTION_WARD_CERTIFIED",False,flush=True)
    print("GE19_LW13_OUTPUT",str(path),flush=True)

if __name__=="__main__":
    main()
