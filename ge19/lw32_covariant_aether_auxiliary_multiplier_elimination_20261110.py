#!/usr/bin/env python3
"""GE19 LW32 — exact algebraic constraint/multiplier elimination in covariant AeST+NL0B.

For unit timelike A^mu and A^mu U_mu=0, compute the complete local
Euler chain rule for field/metric tangent variables on the regular
FLRW branch. No assertion of full physical CLASS eta-Weyl closure.
No CLASS simulations, data fit, source coefficient patch, or H4 run.
"""
from __future__ import annotations
import argparse,hashlib,json,subprocess
from pathlib import Path
import sympy as s

ROOT=Path(__file__).resolve().parents[1]
PRE=ROOT/"ge19/lw32_covariant_aether_auxiliary_multiplier_elimination_predata_20261110.json"
PRE_BLOB="c62f92aa33eba2257210f9da3adb0b238ec8e50b"

def need(ok, label):
    if not bool(ok):
        raise RuntimeError("GE19_LW32_"+label)

def blob(p):
    return subprocess.check_output(["git","hash-object",str(p)],cwd=ROOT,text=True).strip()

def sha256(p):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda:f.read(1<<20),b""):h.update(b)
    return h.hexdigest()

def symbolic():
    N,a,A0,U0=s.symbols("N a A0 U0",nonzero=True,real=True)
    Ai=s.symbols("A1:4",real=True)
    Ui=s.symbols("U1:4",real=True)
    EA0,EU0,EN,Ea=s.symbols("EA0 EU0 EN Ea",real=True)
    EAi=s.symbols("EA1:4",real=True)
    EUi=s.symbols("EU1:4",real=True)
    # The metric is diag(-N^2,a^2,a^2,a^2) only after taking
    # regular covariant constraints. A^i contravariant, U_i covariant.
    C=-N*N*A0*A0+a*a*sum(x*x for x in Ai)+1
    D=A0*U0+sum(x*y for x,y in zip(Ai,Ui))
    c0=s.diff(C,A0);d0=s.diff(D,A0);du0=s.diff(D,U0)
    J=s.Matrix([[c0,s.diff(C,U0)],[d0,du0]])
    solveA=s.sqrt(1+a*a*sum(x*x for x in Ai))/N
    solveU=-sum(x*y for x,y in zip(Ai,Ui))/solveA
    variables=(N,a,*Ai,*Ui)
    da={x:s.simplify(-s.diff(C,x)/c0) for x in variables}
    du={x:s.simplify(-(s.diff(D,x)+d0*da[x])/du0) for x in variables}
    multiplier_mu=-EU0/du0
    multiplier_lambda=s.simplify(-(EA0+multiplier_mu*d0)/c0)
    reduced={}
    constrained={}
    for z,base in tuple(zip(Ai,EAi))+tuple(zip(Ui,EUi))+((N,EN),(a,Ea)):
        reduced[z]=s.simplify(base+EA0*da[z]+EU0*du[z])
        constrained[z]=s.simplify(base+
             multiplier_lambda*s.diff(C,z)+multiplier_mu*s.diff(D,z))
    eps,Psi,Phi,a_bg=s.symbols("eps Psi Phi a_bg",real=True,nonzero=True)
    va=s.symbols("vA1:4",real=True)
    vu=s.symbols("vU1:4",real=True)
    perturb={N:1+eps*Psi,a:a_bg*(1-eps*Phi)}
    perturb.update(dict(zip(Ai,(eps*x for x in va))))
    perturb.update(dict(zip(Ui,(eps*x for x in vu))))
    Aexpr=solveA.subs(perturb)
    Uexpr=solveU.subs(perturb)
    chi,phi,alpha,Q,k,w,omega,q,qd,eta,KB=s.symbols(
       "chi phi alpha Q k w omega q qd eta KB",real=True,nonzero=True)
    χ=phi+Q*alpha
    B=w*χ-a*omega*s.sqrt(w)*q/k
    bath=eta*a**3*s.Rational(1,4)*(
         qd**2-(omega*q-s.sqrt(w)*k*χ/a)**2)
    alpha_bath=s.simplify(s.diff(bath,alpha))
    phi_bath=s.simplify(s.diff(bath,phi))
    # Isolated local alpha-E kinetic Hessian, NOT the full ADM-reduced
    # physical kinetic matrix.
    Ed=s.symbols("Ed",real=True)
    kinetic=a*KB*k*k*Ed*Ed
    checks={
       "exact_unit_norm_constraint":s.simplify(C.subs(A0,solveA))==0,
       "exact_aux_orthogonality":s.simplify(D.subs({A0:solveA,U0:solveU}))==0,
       "rank2_constraint_implicit_Jacobian":
          s.simplify(J.det()+2*N*N*A0*A0)==0,
       "aether_background_time_perturbation_minus_Psi":
          s.simplify(s.diff(Aexpr,eps).subs(eps,0)+Psi)==0,
       "aux_time_component_linear_zero":
          s.simplify(s.diff(Uexpr,eps).subs(eps,0))==0,
       "aux_time_component_first_nonzero_quadratic":
          s.simplify(s.diff(Uexpr,eps,2).subs(eps,0)/2+
                     sum(x*y for x,y in zip(va,vu)))==0,
       "negative_wrong_aux_temporal_sign_detected":
          s.simplify(D.subs({A0:solveA,U0:-solveU}))!=0,
       "negative_omit_unit_metric_N_chain_detected":
          s.simplify(EN-reduced[N])!=0,
       "negative_omit_aux_multiplier_in_aether_normal_detected":
          s.simplify(
              EAi[0]-EA0*s.diff(C,Ai[0])/c0+
              multiplier_mu*s.diff(D,Ai[0])-reduced[Ai[0]])!=0,
       "bath_rank_one_source":s.simplify(alpha_bath-Q*phi_bath)==0,
       "bath_raw_euler_has_half":s.simplify(
          alpha_bath+eta*a*k*k*Q*B/2)==0,
       "local_kinetic_hessian_2KB":s.simplify(
          s.diff(kinetic,Ed,2)-2*a*KB*k*k)==0,
    }
    for z in variables:
        checks["constraint_reduced_Euler_equals_full_"+str(z)]=(
           s.simplify(reduced[z]-constrained[z])==0)
    bad=[k for k,ok in checks.items() if not bool(ok)]
    if bad:
        print("GE19_LW32_FAILED_SYMBOLIC_GATES",bad,flush=True)
    need(not bad,"SYMBOLIC_CONSTRAINT_ELIMINATION_FAIL")
    return {k:bool(v) for k,v in checks.items()},{
       "constraints":"g_mu_nu A^mu A^nu=-1, A^mu U_mu=0",
       "jacobian_det":"-2*N^2*(A^0)^2 near regular FLRW",
       "normal_mode_solutions":"A^0=sqrt(1+a^2 sum_i (A^i)^2)/N; U_0=-sum_i A^i U_i/A^0",
       "FLRW_linear":"delta A^0=-Psi; delta U_0=0",
       "EL_tangent":"E_z^red=E_z^0+E_A0^0 partial_z A0+E_U0^0 partial_z U0",
       "EL_full":"E_z^full=E_z^0+lambda partial_z C+mu partial_z D; lambda,mu fixed by normal field Euler rows",
       "bath_alpha_raw":"-eta*a*k^2*Q*Bchi/2",
       "independent_eta_source_from_multipliers":
         "No extra independent scalar degree of freedom from these TWO algebraic constraints; their existing Euler/metric terms are included exactly by chain rule",
       "full_CLASS_eta_evolution_claim":"NOT certified by this algebra alone",
    }

def provenance(parent):
    need(PRE.is_file() and blob(PRE)==PRE_BLOB,"PREDATA_CHANGED")
    lock=json.loads(PRE.read_text())
    need(lock["classification"]==
      "GE19_LW32_FULL_COVARIANT_UNIT_AETHER_AUXILIARY_ORTHOGONALITY_ELIMINATION_PRELOCK",
      "PREDATA_CLASS_CHANGED")
    for p,sha in lock["source_blobs"].items():
        f=ROOT/p
        need(f.is_file() and blob(f)==sha,"ORIGINAL_SOURCE_CHANGED_"+f.name)
    src=(ROOT/"docs/nl0b_predata_covariant_memory_completion.md").read_text()
    need("A^\\mu U_{j\\mu}=0" in src and
         "h_{\\mu\\nu}=g_{\\mu\\nu}+A_\\mu A_\\nu" in src,
         "ORIGINAL_NL0B_UNIT_AUX_ANCHOR_CHANGED")
    need(parent.is_file() and sha256(parent)==
         lock["original_LW31_WSL_JSON_SHA256"],"LW31_PARENT_SHA_CHANGED")
    p=json.loads(parent.read_text())
    need(p["classification"]==
     "GE19_LW31_REDUCED_GE06_GR_AEST_NL0B_TRACeless_SHEAR_PASS_FULL_ACTION_BRIDGE_OPEN"
     and len(p["symbolic_checks"])==15
     and all(p["symbolic_checks"].values()),"LW31_PARENT_CHECK_CHANGED")
    return lock

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--self-test",action="store_true")
    ap.add_argument("--lw31",type=Path,default=ROOT/
       "results/ge19_lw31_action_spatial_traceless_shear_20261110_r1.json")
    ap.add_argument("--out",type=Path,default=ROOT/
       "results/ge19_lw32_covariant_aether_auxiliary_multiplier_elimination_20261110_r1.json")
    args=ap.parse_args()
    checks,formulas=symbolic()
    print("GE19_LW32_CONSTRAINED_VARIATION_SYMBOLIC_PASS",len(checks),flush=True)
    if args.self_test:return
    lock=provenance(args.lw31)
    print("GE19_LW32_SOURCE_LOCKS_PASS",len(lock["source_blobs"]),flush=True)
    out=args.out.resolve()
    need(out.parent.is_dir() and not out.exists(),"OUTPUT_EXISTING_OR_PARENT_MISSING")
    result={
       "classification":
          "GE19_LW32_COVARIANT_MULTIPLIER_ELIMINATION_EXACT_PASS_CLASS_ETA_EVOLUTION_OPEN",
       "gates":checks,"formulas":formulas,
       "parent_LW31_SHA256":lock["original_LW31_WSL_JSON_SHA256"],
       "source_blobs":lock["source_blobs"],"predata_blob":PRE_BLOB,
       "multiplier_independent_linear_mode_added":False,
       "full_original_covariant_3plus1_Euler_to_CLASS_normalization_closed":False,
       "LW25_LW29_factor_two_discrepancy_resolved":False,
       "LW30_LW31_reduced_metric_constraints_preserved":True,
       "physical_eta_Weyl_response_found":False,
       "observed_gravitational_memory":False,
       "original_CLASS_modified":False
    }
    out.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print("GE19_LW32_CLASSIFICATION",result["classification"],flush=True)
    print("GE19_LW32_PHYSICAL_FORWARD_READY",False,flush=True)
    print("GE19_LW32_OUTPUT",out,flush=True)

if __name__=="__main__":
    main()
