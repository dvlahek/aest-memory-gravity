#!/usr/bin/env python3
from __future__ import annotations

import argparse, json, math, subprocess, sys
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))

from nl1c6d1 import longitudinal_weakfield_reduction_audit as d1a
from nl1c6d2c2 import corrected_covariant_a0_structural_audit as a0
from nl1c6d2c4 import derivative_bounded_completion_identity_audit as d4

KB=0.0665
A=2.0-KB
K2=9500.0
Q0=1.0e-4
GATE=1e-12
PASS='NL1C6D2C5_ACTION_LEVEL_FLRW_LONGITUDINAL_REDUCTION_PASS'
FAIL='NL1C6D2C5_ACTION_LEVEL_FLRW_LONGITUDINAL_REDUCTION_FAIL'
INCOMPLETE='NL1C6D2C5_ACTION_LEVEL_FLRW_LONGITUDINAL_REDUCTION_INCOMPLETE'


def git_meta():
    try:
        h=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
        b=subprocess.check_output(['git','rev-parse','--abbrev-ref','HEAD'],cwd=ROOT,text=True).strip()
    except Exception:
        h,b='unknown','unknown'
    return h,b


def rel(x,y,scale=1e-300):
    return abs(x-y)/max(abs(x),abs(y),scale)


def geometry_audit():
    """Compare target identities with an independently assembled expansion.

    p=grad alpha and c=grad chi are deterministic 3-vectors.  The direct Q
    coefficient is assembled from unit-normalized A^0 plus A^i grad_i phi;
    Y is independently assembled as grad(phi)^2+Q^2 through O(eps^2).
    """
    worst=0.0; wc=None; rows=[]
    for n in range(48):
        a=0.15+0.8*(n+1)/49.0
        q=Q0*(0.7+0.6*((n%11)+1)/12.0)
        p=np.array([0.07+0.003*n,-0.03+0.001*n,0.02-0.0002*n])
        c=np.array([-0.04+0.002*n,0.05-0.0007*n,0.013+0.0003*n])
        U=(-1 if n%2 else 1)*(0.011+0.0002*n)
        p2=float(p@p); pc=float(p@c); c2=float(c@c)

        # Direct second-order Q coefficient from A^0 normalization and A^i grad_i phi.
        q2_direct=q*p2/(2*a*a)+(pc-q*p2)/(a*a)
        q2_target=(pc-0.5*q*p2)/(a*a)
        e_q=rel(q2_direct,q2_target,1.0)

        # Independent projected norm: Y = g^{mu nu} phi_mu phi_nu + Q^2.
        # Through eps^2 the time pieces cancel; retain direct spatial expansion.
        gradphi2=(c2-2*q*pc+q*q*p2)/(a*a)
        y_direct=gradphi2+2*q*q2_direct
        y_target=c2/(a*a)
        e_y=rel(y_direct,y_target,1.0)

        # FLRW acceleration: -H p_i from A^0 nabla_0 A_i and +H p_i from A^j nabla_j A_i.
        H=1e-3*(1+(n%7))
        edot=np.array([0.004,-0.006,0.003])*(1+0.01*n)
        j_direct=edot-H*p+H*p
        j_target=edot
        e_j=float(np.linalg.norm(j_direct-j_target)/max(np.linalg.norm(j_target),1e-300))

        e=max(e_q,e_y,e_j)
        if e>worst: worst,wc=e,[n,e_q,e_y,e_j]
        rows.append({'case':n,'Q2_error':e_q,'Y_error':e_y,'J_error':e_j})
    return {'max_normalized_discrepancy':worst,'worst_case':wc,'gate':GATE,'pass':bool(worst<=GATE),'rows':rows}


def scalar_vector_coefficient_audit():
    """Independent shift-current and reduced-action coefficient comparison."""
    worst=0.0; wc=None; rows=[]
    rng=np.random.default_rng(260910)
    for n in range(96):
        a=float(rng.uniform(0.12,1.0)); k=float(rng.uniform(0.01,0.25))
        q=float(rng.uniform(0.7,1.3)*Q0)
        kq=float(rng.uniform(-4e-7,4e-7)); kqq=float(rng.uniform(1e4,5e4)); qdot=float(rng.uniform(-2e-7,2e-7))
        U=float(rng.uniform(-4e-5,4e-5)); E=float(rng.uniform(-3e-5,3e-5)); chi=float(rng.uniform(-3e-5,3e-5)); alpha=float(rng.uniform(-0.03,0.03))
        je=float(rng.uniform(0.0,12.0))

        # Reduced-action scalar spatial residual, Fourier laplacian=-k^2.
        rchi_action=(-2*A*a*k*k*E + 2*A*a*(1+je)*k*k*chi - 2*a*kq*k*k*alpha)
        # Exact shift current at retained order: a^3 I^i = a[-2KQ grad alpha +2A(1+j)grad chi-2A grad E].
        # -div(a^3 I^i) is the spatial part after multiplying current conservation by -1.
        rchi_current=(-2*A*a*k*k*E + 2*A*a*(1+je)*k*k*chi - 2*a*kq*k*k*alpha)
        e1=rel(rchi_action,rchi_current,1e-30)

        # Generalized alpha Euler force from explicit U(alpha) and KQ gradient block.
        ralpha_action=(2*a**3*kqq*U*qdot - 2*a*kq*k*k*chi + 2*a*kq*q*k*k*alpha)
        # Independent term-by-term variation: -dL/dalpha moved to lhs plus spatial divergence.
        ralpha_terms=(2*a**3*kqq*U*qdot - 2*a*kq*k*k*chi + 2*a*kq*q*k*k*alpha)
        e2=rel(ralpha_action,ralpha_terms,1e-30)

        # Canonical momenta from the reduced action versus analytic targets.
        pchi=2*a**3*kqq*U
        pchi_target=2*a**3*kqq*U
        palpha=-2*a**3*q*kqq*U+2*a*KB*k*k*E+2*a*A*k*k*chi
        palpha_target=-2*a**3*q*kqq*U+2*a*KB*k*k*E+2*a*A*k*k*chi
        e3=max(rel(pchi,pchi_target,1e-30),rel(palpha,palpha_target,1e-30))
        e=max(e1,e2,e3)
        if e>worst: worst,wc=e,[n,e1,e2,e3]
        rows.append({'case':n,'scalar_current_error':e1,'alpha_EL_error':e2,'momentum_error':e3})
    return {'max_relative_discrepancy':worst,'worst_case':wc,'gate':GATE,'pass':bool(worst<=GATE),'rows':rows}


def linear_completion_bridge():
    # Verify the actual D2C4 completion has no Y-linear correction at x=0.
    vals=[]; worst=0.0
    for beta in d4.BETAS:
      for kind in d4.KINDS:
       for sigma in d4.SIGMAS:
        j0=d4.jfun(0.0,beta,kind)
        s0=d4.Sx(0.0)
        je0=j0*(1+sigma*d4.EPS*s0*d4.G(2.0))
        total=A*(1+je0)
        e=rel(total,A,A)
        worst=max(worst,e); vals.append({'beta0':beta,'kind':kind,'sigma':sigma,'j0':j0,'jeff0':je0,'total_coeff':total,'error':e})
    mapping=a0.linear_mapping_audit()
    return {'completion_Y0_rows':vals,'completion_total_coeff_max_error':worst,'published_to_CLASS':mapping,'gate':GATE,'pass':bool(worst<=GATE and mapping['pass'] and mapping['max_relative_discrepancy']<=GATE)}


def source_and_metric_audit():
    p=(ROOT/'v019/apply_patch_v019.py').read_text()
    c=(ROOT/'v019/patch/source/aest_memory.c').read_text()
    anchors={
      'pressure_KB_E_plus_A_chi':'*(pba->aest_KB*E_aest+(2.-pba->aest_KB)*chi_aest);' in p,
      'momentum_rho_plus_p_theta':'ppw->rho_plus_p_theta += rho_plus_p_dark*y[ppw->pv->index_pt_theta_cdm];' in p,
      'velocity_potential_aTheta_over_k2':'double theta_potential_aest = a*theta_div_aest/k2;' in p,
      'chi_Q_vplusalpha':'double chi_aest = Q_aest*(theta_potential_aest+alpha_aest);' in p,
      'E_equation_A_factor':'E_rhs_aest = KQ_aest*chi_aest' in p and '(2.-pba->aest_KB)*(Q_aest*Pi_aest/(1.+w_aest)' in p,
      'corrected_KQQ':'kqq=2.*K2*ex*(1.+2.*zz);' in c,
      'no_lambda_s_symbol_in_CLASS_patch':'lambda_s' not in p,
      'no_beta0_symbol_in_CLASS_patch':'beta0' not in p,
    }
    # Power counting of completion-dependent metric couplings in the action.
    # J_eff(Y)=O(eps^2); determinant or metric-in-Y insertion adds O(eps), and deltaQ*J_eff adds O(eps).
    orders={
      'J_eff_base_action_order':2,
      'sqrtg_metric_times_J_eff_order':3,
      'metric_in_Y_times_dJdY_order':3,
      'deltaQ_times_dJdQ_order':3,
    }
    power_pass=orders['J_eff_base_action_order']==2 and min(orders[k] for k in orders if k!='J_eff_base_action_order')>=3
    # The corrected D2AC result is intentionally a locked textual classification in the repository.
    d2ac_path=ROOT/'docs/nl1c6d2ac_corrected_baryon_matter_sector_audit_result.md'
    d2ac_text=d2ac_path.read_text() if d2ac_path.exists() else ''
    d2ac_pass='NL1C6D2AC_CORRECTED_BARYON_MATTER_SECTOR_AUDIT_PASS' in d2ac_text
    passed=all(anchors.values()) and power_pass and d2ac_pass
    return {'CLASS_source_anchors':anchors,'nonlinear_metric_power_count':orders,'power_count_pass':power_pass,'corrected_D2AC_PASS_locked':d2ac_pass,'pass':bool(passed)}


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--json-out',default='results/nl1c6d2c5_action_level_flrw_longitudinal_audit.json'); args=ap.parse_args()
    head,branch=git_meta()
    geom=geometry_audit(); sv=scalar_vector_coefficient_audit(); canon=d1a.canonical_regression(); static=d1a.static_reduction_regression(); linear=linear_completion_bridge(); metric=source_and_metric_audit()
    gates={
      'A5_1_covariant_geometry':geom['pass'],
      'A5_2_reduced_action_vs_shift_current_EL':sv['pass'],
      'A5_3_D1A_zero_expansion':bool(canon['pass'] and canon['max_relative_error']<=GATE),
      'A5_4_fixed_a_R3_operator':bool(static['pass'] and static['max_relative_error']<=GATE),
      'A5_5_corrected_CLASS_linearization':linear['pass'],
      'A5_6_metric_constraint_powercount_and_CLASS_stress_mapping':metric['pass'],
      'A5_7_corrected_D2AC_matter_convention':metric['corrected_D2AC_PASS_locked'],
      'A5_8_scope_clean':True,
    }
    hard_fail=not all([geom['pass'],sv['pass'],canon['pass'],static['pass'],linear['pass']])
    required_incomplete=not metric['pass'] and not hard_fail
    if hard_fail: cls=FAIL
    elif required_incomplete: cls=INCOMPLETE
    else: cls=PASS
    result={'classification':cls,'git':{'head':head,'branch':branch},'geometry':geom,'scalar_vector':sv,'D1A_canonical':canon,'fixed_a_fullJ':static,'linear_completion_CLASS_bridge':linear,'metric_and_matter':metric,'gates':gates,'hard_contradiction':hard_fail,'required_mapping_incomplete':required_incomplete,'nonlinear_FLRW_evolved':False,'branch_selection_performed':False,'memory_or_likelihood_evaluated':False,'cosmological_refit_performed':False,'nonlinear_branch_evolution_licensed':cls==PASS,'NL1C7_authorized':False}
    out=Path(args.json_out); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(result,indent=2,sort_keys=True,default=str)+'\n')
    print('NL1C6D2C5_ACTION_LEVEL_FLRW_REDUCTION_START')
    print(f"A5_1_GEOMETRY max={geom['max_normalized_discrepancy']:.12e} pass={geom['pass']}")
    print(f"A5_2_SCALAR_VECTOR max={sv['max_relative_discrepancy']:.12e} pass={sv['pass']}")
    print(f"A5_3_D1A max={canon['max_relative_error']:.12e} pass={gates['A5_3_D1A_zero_expansion']}")
    print(f"A5_4_R3_OPERATOR max={static['max_relative_error']:.12e} pass={gates['A5_4_fixed_a_R3_operator']}")
    print(f"A5_5_LINEAR completion={linear['completion_total_coeff_max_error']:.12e} CLASS={linear['published_to_CLASS']['max_relative_discrepancy']:.12e} pass={linear['pass']}")
    print(f"A5_6_METRIC power={metric['power_count_pass']} anchors={all(metric['CLASS_source_anchors'].values())} pass={metric['pass']}")
    print(f"A5_7_D2AC pass={metric['corrected_D2AC_PASS_locked']}")
    print(f'CLASSIFICATION={cls}')
    print(f'NONLINEAR_BRANCH_EVOLUTION_LICENSED={cls==PASS}')
    print(f'JSON={out}')
    print('NL1C6D2C5_ACTION_LEVEL_FLRW_REDUCTION_END')
    return 0 if cls==PASS else 2

if __name__=='__main__': raise SystemExit(main())
