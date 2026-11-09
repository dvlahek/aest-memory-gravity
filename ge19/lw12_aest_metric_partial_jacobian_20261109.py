#!/usr/bin/env python3
"""GE19 LW12 — exact symbolic 5-state AeST+Phi direct Jacobian BLOCK.

Original Newtonian-gauge AeST fluid perturbations coupled to CLASS
Einstein psi,phi' expressions. Treat other-species shear/momentum S,M
as EXTERNAL DYNAMICAL INPUTS — NEVER claim full Einstein-AeST closure.

One SHA-frozen source-verified analytic calculation. No CLASS solver,
DES sky residuals, cosmological parameter fitting or physical history pair.
Requires sympy for symbolic algebra (only for this small offline audit).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PRE=ROOT/"ge19/lw12_aest_metric_partial_jacobian_protocol_r1_20261109.json"
PRE_BLOB="4490f60447ffc21204cad5763097a0fbc62c5904"
LW10_SHA256="10e8dd7f3eaa988a48966ce7892e1da653f4215c4ce09499a4c62981cf350851"
CLASS_HEAD="e85808324f51fc694d12e3ed7439552a3c3f9540"
CLASS_BLOB="c78fe4376d2eeebfbf4ff0cfca13b048d4513fa0"
PATCH_BLOBS={
    "v019/apply_patch_v019.py":
        "c78484eb916bfee2730759c0bdc813a706bf9a68",
    "v019j/apply_memory_patch.py":
        "14796a5ed9e6265ed6810c792a93d7328a109364",
    "v019w/apply_variational_forcing_patch.py":
        "00c3f5da5a1b7734c67c82aa9181a443736101bf",
}


def require(condition, gate):
    if not bool(condition):
        raise RuntimeError("GE19_LW12_"+gate)


def hash_file(p: Path) -> str:
    digest=hashlib.sha256()
    with p.open("rb") as f:
        for block in iter(lambda:f.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def git(*args: str) -> str:
    return subprocess.check_output(["git",*args], text=True).strip()


def symbolic_audit():
    try:
        import sympy as sp
    except ImportError as e:
        raise RuntimeError(
            "GE19_LW12_SYMPY_REQUIRED: python -m pip install sympy") from e

    a,Hconf,Hphys,rho,g,w,c2,KB,Q,KQ,k2=sp.symbols(
        "a Hconf Hphys rho g w c2 KB Q KQ k2", nonzero=True,real=True)
    delta,theta,alpha,E,Phi,S,M=sp.symbols(
        "delta theta alpha E Phi S M", real=True)
    y=sp.Matrix([delta,theta,alpha,E,Phi])
    e=sp.eye(5)
    ed,et,ea,eE,eP=[e.row(i) for i in range(5)]

    L=c2*k2/(3*a*a*rho)
    gamma=2-KB
    beta=sp.Rational(3,2)*a*a*rho*g/k2
    chi=Q*(a*theta/k2+alpha)
    Pi=c2*delta+L*(KB*E+gamma*chi)
    Psi=Phi-S
    Phip=-Hconf*Psi+beta*theta+M

    # Exact source equations in v019 + v019j; no finite eta bath coupling
    # inside these derivatives — the physical F_E enters as a source.
    deltadot=3*Hconf*(w*delta-Pi)-g*(theta-3*Phip)
    thetadot=(3*c2-1)*Hconf*theta+k2*Pi/g+k2*Psi
    alphadot=a*(E-Psi)
    Edot=(a/KB)*(KQ*chi-gamma*(
        Q*Pi/g+(Hphys+Q)*chi-3*c2*Hphys*Q*alpha))-Hconf*E
    equations=sp.Matrix([deltadot,thetadot,alphadot,Edot,Phip])
    A=equations.jacobian(y)
    V=equations.jacobian(sp.Matrix([S,M]))

    # Reconstruct using the FACTORIZED physical source/Jacobian rows.
    p=sp.Matrix([Pi]).jacobian(y)
    x=sp.Matrix([chi]).jacobian(y)
    rPhi=-Hconf*eP+beta*et
    expectedA=sp.Matrix.vstack(
        3*Hconf*w*ed-3*Hconf*p-g*et+3*g*rPhi,
        (3*c2-1)*Hconf*et+(k2/g)*p+k2*eP,
        a*eE-a*eP,
        (a/KB)*((KQ-gamma*(Hphys+Q))*x
            -gamma*Q*p/g+3*gamma*c2*Hphys*Q*ea)-Hconf*eE,
        rPhi,
    )
    expectedV=sp.Matrix([
        [3*g*Hconf,3*g],
        [-k2,0],
        [a,0],
        [0,0],
        [Hconf,1]
    ])
    C=eP
    inputE=eE.T
    C0=sp.simplify((C*inputE)[0])
    C1=sp.simplify((C*A*inputE)[0])
    C2=sp.factor((C*A*A*inputE)[0])
    target=sp.Rational(1,2)*c2*KB*k2
    G2=sp.factor(C2/2)
    physical=sp.factor(G2*(-a*Q/(2*KB)))

    checks={
        "exact_all_five_rows":
            all(sp.simplify(x)==0 for x in A-expectedA),
        "both_external_source_columns":
            all(sp.simplify(x)==0 for x in V-expectedV),
        "weyl_phi_plus_shear_observer":
            sp.simplify(sp.diff(Phi-S/2,Phi)-1)==0
            and sp.simplify(sp.diff(Phi-S/2,S)+sp.Rational(1,2))==0,
        "pressure_direct_E":
            sp.simplify(sp.diff(Pi,E)-c2*KB*k2/(3*a*a*rho))==0,
        "C_eE_equals_zero":C0==0,
        "C_A_eE_equals_zero":C1==0,
        "C_A2_eE_equals_c2KBk2_over_2":
            sp.simplify(C2-target)==0,
        "physical_source_coefficient_explicit_KB_cancels":
            sp.simplify(physical+a*Q*c2*k2/8)==0,
    }
    require(all(checks.values()),"SYMBOLIC_BLOCK_MISMATCH")
    return {
        "checks":checks,
        "basis":["delta_A","theta_A","alpha_A","E_A","Phi"],
        "source_column_eE":[0,0,0,1,0],
        "definitions":{
            "g":"1+w_A",
            "L":"c_a²*k²/(3*a²*rho_A)",
            "gamma":"2-K_B",
            "beta":"3*a²*rho_A*(1+w_A)/(2*k²)",
            "chi":"Q*(a*theta_A/k²+alpha_A)",
            "Pi":"c_a²*delta_A+L*(K_B*E_A+gamma*chi)",
            "Psi":"Phi-S",
            "S":"(9/2)*(a²/k²)*Sigma_shear_other",
            "M":"(3/2)*(a²/k²)*Sigma_momentum_other",
        },
        "AeST_metric_state_Jacobian_partial_5x5":
            [[str(sp.factor(A[i,j])) for j in range(5)]
              for i in range(5)],
        "external_stress_Jacobian_5x2":
            [[str(sp.factor(V[i,j])) for j in range(2)]
              for i in range(5)],
        "W_state_observer":[0,0,0,0,1],
        "W_external_shear_observer_coefficient":-0.5,
        "C_eE":str(C0),
        "C_A_eE":str(C1),
        "C_A2_eE":str(C2),
        "G_WE_impulse_leading_short_lag_coefficient_Delta2":
            str(G2),
        "physical_memory_Braw_to_W_local_convolution_Delta2":
            str(physical),
        "number_of_smooth_state_variables":5,
        "SymPy_version":sp.__version__,
    }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--self-test",action="store_true")
    ap.add_argument("--class-root",type=Path,
                    help="optional original patched CLASS dir (no solver)")
    ap.add_argument("--lw10",type=Path,default=ROOT/
        "results/ge19_lw10_source_to_weyl_constrained_green_static_audit_20261109.json")
    ap.add_argument("--out",type=Path,default=ROOT/
        "results/ge19_lw12_aest_metric_partial_jacobian_20261109.json")
    args=ap.parse_args()

    symbolic=symbolic_audit()
    if args.self_test:
        print("GE19_LW12_SYMBOLIC_BLOCK_SELFTEST_PASS",
              "gates",len(symbolic["checks"]),flush=True)
        return

    require(git("hash-object",str(PRE))==PRE_BLOB,
            "PREDATA_BLOB_CHANGED")
    pre=json.loads(PRE.read_text())
    require(pre["classification"]==
            "GE19_LW12_PARTIAL_CONSTRAINED_AEST_METRIC_JACOBIAN_FORMULA_LOCK",
            "PREDATA_CLASSIFICATION")
    require(args.lw10.is_file() and hash_file(args.lw10)==LW10_SHA256,
            "ORIGINAL_LW10_RESULT_SHA256")
    lw10=json.loads(args.lw10.read_text())
    require(lw10["classification"]==
            "GE19_LW10_IMPLEMENTED_E_TO_METRIC_STRUCTURAL_PATH_PASS_FULL_GREEN_UNCERTIFIED"
            and lw10["all_static_source_anchors_pass"]
            and all(lw10["static_exact_text_anchor_checks"].values()),
            "ORIGINAL_LW10_NOT_PASS")
    for path,wanted in PATCH_BLOBS.items():
        require(git("hash-object",str(ROOT/path))==wanted,
                "HISTORICAL_PATCH_BLOB_"+Path(path).name)
    if args.class_root is not None:
        cls=args.class_root.resolve()
        require(git("-C",str(cls),"rev-parse","HEAD")==CLASS_HEAD,
                "CLASS_PIN_CHANGED")
        require(git("-C",str(cls),"rev-parse",
                    "HEAD:source/perturbations.c")==CLASS_BLOB,
                "CLASS_ORIGINAL_SOURCE_BLOB_CHANGED")

    result={
        "classification":
            "GE19_LW12_EXACT_AEST_PHI_DIRECT_JACOBIAN_BLOCK_PASS_FULL_AEFF_OPEN",
        "predata_git_blob_sha1":PRE_BLOB,
        "LW10_sha256":hash_file(args.lw10),
        "original_CLASS_commit":CLASS_HEAD,
        "historical_patch_blobs":PATCH_BLOBS,
        **symbolic,
        "physical_scope":"Five-state EXACT partial AeST+Phi block with S,M external species stress. This is NOT a closed evolution because ordinary radiation, neutrino, baryon perturbations feed metric and are themselves metric-driven.",
        "source_perturbation":"F_E = -a Q B_chi_raw/(2K_B) in E' only at eta=0",
        "hypothetical_impulse_not_dynamically_admissible":True,
        "global_Aeff_closed":False,
        "other_species_A_AO_A_OA_A_OO_assembled":False,
        "Einstein_Hamiltonian_Noether_constraint_propagation_certified":False,
        "global_retarded_G_WE_evaluated":False,
        "two_physical_history_pair_certified":False,
        "DES_ACT_detection":False,
        "LW03_radial_quadrature_FAIL_preserved":True,
        "LW05_cosmic_shear_LOS_BLOCK_preserved":True,
        "LW08_antisymmetric_response_UNRESOLVED_preserved":True,
        "H4_Z21_certified":False,
    }
    out=args.out.resolve()
    require(out.parent.is_dir() and not out.exists(),
            "OUTPUT_EXISTS_OR_PARENT_MISSING")
    out.write_text(json.dumps(result,sort_keys=True,indent=2,
                              allow_nan=False)+"\n")
    print("GE19_LW12_CLASSIFICATION",result["classification"],flush=True)
    print("GE19_LW12_SYMBOLIC_GATES",len(symbolic["checks"]),
          "ALL_PASS",flush=True)
    print("GE19_LW12_FULL_AEFF_CLOSED",False,flush=True)
    print("GE19_LW12_OUTPUT",out,flush=True)


if __name__=="__main__":
    main()
