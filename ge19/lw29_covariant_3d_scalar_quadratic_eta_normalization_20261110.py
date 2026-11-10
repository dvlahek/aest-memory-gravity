#!/usr/bin/env python3
"""LW29: original NL0B + AeST 3D scalar quadratic Hessian audit.

Exactly the covariant model's *local scalar quadratic spatial block* in
arbitrary 3-vector k orientation. NOT a full Einstein/ADM constraint
reduction, a new finite-eta model, or a detection.  No CLASS runs.
"""
from __future__ import annotations
import argparse
import json
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PRE=ROOT/"ge19/lw29_covariant_scalar_quadratic_normalization_predata_20261110.json"
PRE_BLOB="53b4baf3484ddac7c272a4dd3b9d3eeee2388bd7"

def require(ok,why):
    if not bool(ok):
        raise RuntimeError("GE19_LW29_"+why)

def blob(p):
    return subprocess.check_output(
        ["git","hash-object",str(p)],cwd=ROOT,text=True
    ).strip()

def algebra():
    import sympy as s
    a,KB,C,Q,eta,wx,om,Y2=s.symbols(
        "a K_B C Q eta w omega Y2",positive=True)
    kx,ky,kz=s.symbols("kx ky kz",real=True)
    alpha,alphad,phi,Psi,q,qd=s.symbols(
        "alpha alpha_dot varphi Psi q q_dot",real=True)
    h,eps=s.symbols("h eps",real=True)
    ks=(kx,ky,kz)
    k2=sum(t*t for t in ks)
    k=s.sqrt(k2)
    chi=phi+Q*alpha
    EA=alphad+Psi
    Bchi=wx*chi-a*om*s.sqrt(wx)*q/k

    # Scalar gradient amplitudes are real Fourier cosine components.
    # Every k component contributes. The physical vector bath component
    # points along k, with q_i=(k_i/k)*q, on a selected retarded q branch.
    Ei=[ki*EA/a for ki in ks]
    Xi=[ki*chi/a for ki in ks]
    qi=[ki*q/k for ki in ks]
    qdi=[ki*qd/k for ki in ks]
    base=a**3*(KB*sum(e*e for e in Ei)
              +2*C*sum(e*x for e,x in zip(Ei,Xi))
              -C*sum(x*x for x in Xi))
    gradY=a**3*Y2*sum(x*x for x in Xi)
    bath=eta*a**3*s.Rational(1,4)*(
       sum(v*v for v in qdi)
       -sum((om*v-s.sqrt(wx)*x)**2 for v,x in zip(qi,Xi)))
    total=base+gradY+bath

    kinetic=s.diff(total,alphad,2)
    bath_alpha=s.diff(bath,alpha)
    bath_phi=s.diff(bath,phi)
    inferred=s.simplify(bath_alpha/kinetic)
    expected=-eta*Q*Bchi/(4*KB)
    half_core_inferred=s.simplify(bath_alpha/s.diff(base/2+gradY+bath,alphad,2))
    doubled_bath_inferred=s.simplify((2*bath_alpha)/kinetic)
    hess=s.hessian(bath,(phi,alpha))
    reducedbath=eta*a**3*s.Rational(1,4)*(
       qd*qd-(om*q-s.sqrt(wx)*k*chi/a)**2)

    # Since background X=q=0, direct bath stress about FLRW is zero:
    # evaluate a perturbation of the spatial metric (through a) and
    # perturb X and q simultaneously. First-order derivative vanishes.
    expanded_bath=bath.subs({
       a:a*(1+eps*h),phi:eps*phi,
       alpha:eps*alpha,q:eps*q,qd:eps*qd,
    })
    def zero(expr):
        return s.simplify(expr)==0
    checks={
      "3d_vector_bath_exactly_scalar_longitudinal":
          zero(bath-reducedbath),
      "3d_k_tensor_sum_exact":
          zero(sum(ki*ki for ki in ks)-k2),
      "full_AeST_aether_kinetic_Hessian_2KB":
          zero(kinetic-2*a*KB*k2),
      "bath_raw_alpha_Euler_source_minus_half":
          zero(bath_alpha+eta*a*k2*Q*Bchi/2),
      "bath_raw_scalar_Euler_source_minus_half":
          zero(bath_phi+eta*a*k2*Bchi/2),
      "rank_one_bath_phi_alpha_source":
          zero(bath_alpha-Q*bath_phi),
      "rank_one_bath_phi_alpha_Hessian":
          zero(hess.det()),
      "normalized_aether_eta_evolution_quarter":
          zero(inferred-expected),
      "arbitrary_k_orientation_swap":
          zero(inferred-inferred.xreplace({kx:ky,ky:kx})),
      "free_analytic_Y_quadratic_gradient_no_E_kinetic":
          zero(s.diff(gradY,alphad,2)),
      "eta_zero_bath_null":
          zero(bath.subs(eta,0)),
      "no_bath_linear_metric_Euler_source":
          zero(s.diff(s.diff(expanded_bath,h),eps).subs(eps,0)),
      "wrong_raw_half_as_evolution_detected":
          not zero(inferred+eta*Q*Bchi/(2*KB)),
      "negative_halve_AeST_kinetic_detected":
          zero(half_core_inferred-2*expected) and not zero(half_core_inferred-expected),
      "negative_double_bath_force_detected":
          zero(doubled_bath_inferred-2*expected) and not zero(doubled_bath_inferred-expected),
    }
    failed=[name for name,result in checks.items() if not bool(result)]
    if failed:
        print("GE19_LW29_SYMBOLIC_GATES_FAILED",failed,flush=True)
    require(not failed,"SYMBOLIC_PHYSICS_FAIL")
    return {key:bool(value) for key,value in checks.items()},{
      "original_AeST_kinetic":"a^3 K_B sum_i[(k_i/a)*(alpha_dot+Psi)]^2",
      "original_bath":"eta*a^3/4*(q_dot^2 - (omega*q-sqrt(w)*k*chi/a)^2)",
      "k_squared":"kx^2+ky^2+kz^2 (nonzero)",
      "raw_bath_aether_source":"-eta*a*k^2*Q*Bchi/2",
      "aether_kinetic_Hessian":"2*a*K_B*k^2",
      "full_normalized_local_Edot_eta_source":"-eta*Q*Bchi/(4*K_B)",
      "historical_CLASS_Edot_eta_source":"-eta*Q*Bchi/(2*K_B)",
      "relative_source_factor":"2",
      "original_scalar_source_rank":"1 (phi,alpha)",
      "Y_note":"Arbitrary quadratic Y2*X^2 changes gradient stiffness but not the E kinetic Hessian; the locked Y^(3/2) starts at cubic order",
      "math_scope":"3D isotropic scalar quadratic local action at relaxed FLRW, fixed retarded auxiliary branch; full constraints still open",
    }

def preflight():
    require(PRE.is_file() and blob(PRE)==PRE_BLOB,"PRELOCK_CHANGED")
    data=json.loads(PRE.read_text())
    require(data["classification"]==
      "GE19_LW29_COVARIANT_3D_SCALAR_QUADRATIC_ETA_NORMALIZATION_AUDIT_PRELOCK",
      "CLASSIFICATION_CHANGED")
    for p,want in data["source_git_blobs"].items():
        f=ROOT/p
        require(f.is_file() and blob(f)==want,"PARENT_CHANGED_"+f.name)
    # Audit the unchanged original assertions: historical source HALF
    # differs from the full normalized evolution QUARTER.
    original=(ROOT/"docs/nl0b_covariant_memory_completion_result.md").read_text()
    require("Delta E_" in original or "\\Delta E_" in original,
      "ORIGINAL_NL0B_SOURCE_ASSERTION_MISSING")
    patch=(ROOT/"v019j/apply_memory_patch.py").read_text()
    require("E_rhs_aest -= 0.5*Q_aest*Bchi_aest;" in patch,
      "ORIGINAL_PATCH_SOURCE_MISSING")
    return data

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--self-test",action="store_true")
    ap.add_argument("--out",type=Path,default=ROOT/
      "results/ge19_lw29_covariant_3d_scalar_quadratic_normalization_20261110_r1.json")
    args=ap.parse_args()
    checks,derived=algebra()
    print("GE19_LW29_3D_QUADRATIC_SYMBOLIC_PASS",len(checks),flush=True)
    if args.self_test:
        return
    data=preflight()
    print("GE19_LW29_ORIGINAL_SOURCE_LOCKS_PASS",
          len(data["source_git_blobs"]),flush=True)
    out=args.out.resolve()
    require(out.parent.is_dir() and not out.exists(),"OUTPUT_PREEXISTS_OR_PARENT_MISSING")
    report={
      "classification":
         "GE19_LW29_ORIGINAL_COVARIANT_3D_QUADRATIC_NORMALIZATION_QUARTER_PASS_FULL_ADM_BRIDGE_OPEN",
      "predata_git_blob":PRE_BLOB,
      "source_git_blobs":data["source_git_blobs"],
      "symbolic_checks":checks,
      "derived":derived,
      "historical_NL0B_raw_half_source_remains_true":True,
      "historical_NL0B_identity5_physical_evolution_claim_qualified":True,
      "historical_NL0B_identity7_full_mapping_not_certified":True,
      "original_CLASS_patch_changed":False,
      "original_LW01_LW08_reclassified":False,
      "physical_full_3plus1_constraints_and_unit_aether_mapping_certified":False,
      "physical_eta_matter_Weyl_derivative_certified":False,
      "DES_lensing_observation_found":False,
      "LW22_geometry_pass_preserved":True,
      "LW28_reduced_action_quarter_pass_preserved":True
    }
    out.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n")
    print("GE19_LW29_CLASSIFICATION",report["classification"],flush=True)
    print("GE19_LW29_PHYSICAL_OBSERVER_READY",False,flush=True)
    print("GE19_LW29_OUTPUT",out,flush=True)

if __name__=="__main__":
    main()
