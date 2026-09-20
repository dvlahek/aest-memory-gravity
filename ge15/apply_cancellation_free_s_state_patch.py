#!/usr/bin/env python3
"""GE15 exact cancellation-free AeST state reparameterization.

Apply after the validated v0.19/v0.19i/memory/trace patch chain.
The legacy index_pt_alpha_aest slot is reused internally for

    s = chi/Q = a theta/k^2 + alpha.

Physical alpha is reconstructed algebraically. No state dimension or
physical equation is changed.
"""
from pathlib import Path
import argparse, json


def replace_once(path, old, new, label):
    p=Path(path)
    s=p.read_text()
    n=s.count(old)
    if n!=1:
        raise RuntimeError(f"{label}: expected exactly one anchor, found {n}")
    p.write_text(s.replace(old,new,1))


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("class_root")
    args=ap.parse_args()
    root=Path(args.class_root).resolve()
    repo=Path(__file__).resolve().parents[1]
    pert=root/"source"/"perturbations.c"

    # 1. Leading adiabatic IC: store s=chi/Q exactly as zero instead of
    # separately storing alpha=-a theta/k^2 and later subtracting.
    old_ic='''      ppw->pv->y[ppw->pv->index_pt_alpha_aest] =
        -ppw->pvecback[pba->index_bg_a]*ppw->pv->y[ppw->pv->index_pt_theta_cdm]/(k*k);
'''
    new_ic='''      /* GE15 cancellation-free state: this legacy slot stores
         s_aest = chi/Q = a*theta/k^2 + alpha. */
      ppw->pv->y[ppw->pv->index_pt_alpha_aest] = 0.;
'''
    replace_once(pert,old_ic,new_ic,"GE15 s-state initial condition")

    # 2. Stress-energy closure: chi is now Q*s directly.
    old_stress='''        double theta_potential = a*y[ppw->pv->index_pt_theta_cdm]/k2;
        double chi_aest = Q_aest*(theta_potential+y[ppw->pv->index_pt_alpha_aest]);
'''
    new_stress='''        double theta_potential = a*y[ppw->pv->index_pt_theta_cdm]/k2;
        double chi_aest = Q_aest*y[ppw->pv->index_pt_alpha_aest];
'''
    replace_once(pert,old_stress,new_stress,"GE15 stress chi state")

    # 3. Physical derivative block: reconstruct alpha from s-v, and evolve s
    # with the exact transformed equation.
    old_vars='''        double theta_potential_aest = a*theta_div_aest/k2;
        double alpha_aest = y[pv->index_pt_alpha_aest];
        double E_aest = y[pv->index_pt_E_aest];
        double chi_aest = Q_aest*(theta_potential_aest+alpha_aest);
'''
    new_vars='''        double theta_potential_aest = a*theta_div_aest/k2;
        double s_aest = y[pv->index_pt_alpha_aest];
        double alpha_aest = s_aest-theta_potential_aest;
        double E_aest = y[pv->index_pt_E_aest];
        double chi_aest = Q_aest*s_aest;
'''
    replace_once(pert,old_vars,new_vars,"GE15 derivative state reconstruction")

    old_alpha_rhs='''        dy[pv->index_pt_alpha_aest] = a*(E_aest-psi_aest);
'''
    new_s_rhs='''        /* Exact transformed equation for s=chi/Q.
           Q'/Q=-3*c_ad^2*(aH) follows from K_Q=I0/a^3. */
        dy[pv->index_pt_alpha_aest] =
          a*(E_aest+Pi_aest/(1.+w_aest))
          +3.*cad2_aest*a_prime_over_a*theta_potential_aest;
'''
    replace_once(pert,old_alpha_rhs,new_s_rhs,"GE15 exact s derivative")

    # 4. Native tangent forcing trace must use chi=Q*s directly.
    old_force='''    double Q_aest=pvecback[pba->index_bg_Q_aest];
    double theta_aest=y[ppw->pv->index_pt_theta_cdm];
    double alpha_aest=y[ppw->pv->index_pt_alpha_aest];
    double chi_aest=Q_aest*(a*theta_aest/(k*k)+alpha_aest);
'''
    new_force='''    double Q_aest=pvecback[pba->index_bg_Q_aest];
    double theta_aest=y[ppw->pv->index_pt_theta_cdm];
    double s_aest=y[ppw->pv->index_pt_alpha_aest];
    double chi_aest=Q_aest*s_aest;
'''
    replace_once(pert,old_force,new_force,"GE15 tangent forcing chi")

    # 5. Historical accepted source-grid chi trace remains the same physical
    # observable but is now read directly from s.
    old_trace='''    double Q_trace = pvecback[pba->index_bg_Q_aest];
    double theta_trace = y[ppw->pv->index_pt_theta_cdm];
    double alpha_trace = y[ppw->pv->index_pt_alpha_aest];
    double chi_trace = Q_trace*(a*theta_trace/(k*k)+alpha_trace);
'''
    new_trace='''    double Q_trace = pvecback[pba->index_bg_Q_aest];
    double theta_trace = y[ppw->pv->index_pt_theta_cdm];
    double s_trace = y[ppw->pv->index_pt_alpha_aest];
    double chi_trace = Q_trace*s_trace;
'''
    replace_once(pert,old_trace,new_trace,"GE15 accepted-grid chi trace")

    # 6. GE08 source trace schema remains physical alpha/alpha-prime even
    # though the internal state slot now stores s.
    old_ge08='''        y[ppw->pv->index_pt_delta_cdm],
        y[ppw->pv->index_pt_theta_cdm],
        y[ppw->pv->index_pt_alpha_aest],
        y[ppw->pv->index_pt_E_aest],
        dy[ppw->pv->index_pt_alpha_aest],
        y[ppw->pv->index_pt_delta_b],
'''
    new_ge08='''        y[ppw->pv->index_pt_delta_cdm],
        y[ppw->pv->index_pt_theta_cdm],
        y[ppw->pv->index_pt_alpha_aest]-a*y[ppw->pv->index_pt_theta_cdm]/(k*k),
        y[ppw->pv->index_pt_E_aest],
        a*(y[ppw->pv->index_pt_E_aest]-pvecmetric[ppw->index_mt_psi]),
        y[ppw->pv->index_pt_delta_b],
'''
    replace_once(pert,old_ge08,new_ge08,"GE15 GE08 physical alpha trace")

    # 7. GE09 successful-step trace also remains in physical alpha variables.
    old_ge09='''      y[ppw->pv->index_pt_delta_cdm],
      dy[ppw->pv->index_pt_delta_cdm],
      y[ppw->pv->index_pt_theta_cdm],
      dy[ppw->pv->index_pt_theta_cdm],
      y[ppw->pv->index_pt_alpha_aest],
      dy[ppw->pv->index_pt_alpha_aest],
      y[ppw->pv->index_pt_E_aest],
      dy[ppw->pv->index_pt_E_aest]);
'''
    new_ge09='''      y[ppw->pv->index_pt_delta_cdm],
      dy[ppw->pv->index_pt_delta_cdm],
      y[ppw->pv->index_pt_theta_cdm],
      dy[ppw->pv->index_pt_theta_cdm],
      y[ppw->pv->index_pt_alpha_aest]-a*y[ppw->pv->index_pt_theta_cdm]/(k*k),
      a*(y[ppw->pv->index_pt_E_aest]-pvecmetric[ppw->index_mt_psi]),
      y[ppw->pv->index_pt_E_aest],
      dy[ppw->pv->index_pt_E_aest]);
'''
    replace_once(pert,old_ge09,new_ge09,"GE15 GE09 physical alpha trace")

    txt=pert.read_text()
    checks={
        "s_ic_exact_zero":"GE15 cancellation-free state" in txt,
        "s_derivative_exact":"a*(E_aest+Pi_aest/(1.+w_aest))" in txt,
        "chi_direct_from_s":"double chi_aest = Q_aest*s_aest;" in txt,
        "physical_alpha_reconstructed":"double alpha_aest = s_aest-theta_potential_aest;" in txt,
        "legacy_stress_cancellation_absent":"Q_aest*(theta_potential+y[ppw->pv->index_pt_alpha_aest])" not in txt,
        "legacy_derivative_cancellation_absent":"Q_aest*(theta_potential_aest+alpha_aest)" not in txt,
        "legacy_alpha_rhs_absent":"dy[pv->index_pt_alpha_aest] = a*(E_aest-psi_aest);" not in txt,
        "accepted_chi_trace_direct":"double chi_trace = Q_trace*s_trace;" in txt,
        "dense_trace_physical_alpha":"y[ppw->pv->index_pt_alpha_aest]-a*y[ppw->pv->index_pt_theta_cdm]/(k*k)" in txt,
        "memory_closure_preserved":"E_rhs_aest -= 0.5*Q_aest*Bchi_aest" in txt,
    }
    if not all(checks.values()):
        raise RuntimeError(checks)

    out={
        "classification":"GE15_CANCELLATION_FREE_S_STATE_PATCH_PASS",
        "physics_modified":False,
        "state_dimension_modified":False,
        "legacy_slot_semantics":"index_pt_alpha_aest stores s=chi/Q internally",
        "physical_alpha":"s-a theta/k^2",
        "initial_s":0.0,
        "checks":checks,
    }
    (repo/"results").mkdir(exist_ok=True)
    (repo/"results"/"ge15_s_state_patch.json").write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps(out,indent=2))


if __name__=="__main__":
    main()
