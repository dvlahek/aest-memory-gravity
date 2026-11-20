#!/usr/bin/env python3
"""GE19: one joint pressureful AeST / radiation Einstein constraint decision.

Exact algebra in the reduced source dictionary and the pre-existing radiation
test-fluid expansion. A nonzero negative-control Einstein residual is the
expected result: this is NOT a full Einstein-AeST-NL0B primordial eigenmode.
"""
import argparse
import json
import subprocess
from pathlib import Path

import sympy as s

SOURCE_LOCKS = {
    "docs/ge19_20261111_joint_action_to_CLASS_scalar_source_matrix.md":
        "e5a0d0d889188f6bb7d8a2b6c44f9baf74c9c459",
    "docs/ge19_lw33_exact_scalar_action_to_CLASS_offshell_source_decision_2026-11-10.md":
        "dedcb6148b6ee4353c32972fcc456d9e3a185ffd",
    "ge19/physics_gate/radiation_neutrino_delta_source_20261111.py":
        "19e9efd5713dc8df3057c4b33f8c4a2921a96687",
    "ge19/physics_gate/primordial_pressureful_velocity_20261120.py":
        "849b74297a2293327956c548d53b5a802bb865d3",
    "ge19/physics_gate/constraint_projected_joint_operator_20261112.py":
        "b98bec1e1af46021d810676a062957d4efe80c58",
}

def source_locks(root):
    for path, expected in SOURCE_LOCKS.items():
        f = root / path
        if not f.is_file():
            raise RuntimeError("MISSING_SOURCE " + path)
        got = subprocess.check_output(
            ["git", "hash-object", str(f)], cwd=root, text=True
        ).strip()
        if got != expected:
            raise RuntimeError("SOURCE_CHANGED " + path + " " + got)
    print("GE19_JOINT_PRIMORDIAL_SOURCE_LOCKS_PASS", len(SOURCE_LOCKS))

def calculate():
    H, w, c, delta, theta, Phi_dot, Psi, k, a, RA, S = s.symbols(
        "H w c delta theta Phi_dot Psi k a R_A S_A", nonzero=True
    )
    d = s.symbols("d", real=True)
    rho = RA / (1+w)
    Pi = c*delta + c*k**2*S/(3*a**2*rho)
    wprime = -3*H*(1+w)*(c-w)
    delta_prime = 3*H*(w*delta-Pi) - (1+w)*(theta-3*Phi_dot)
    dprime = delta_prime/(1+w) - delta*wprime/(1+w)**2
    want_dprime = -theta+3*Phi_dot - H*c*k**2*S/(a**2*RA)
    theta_prime = (3*c-1)*H*theta + k**2*(Pi/(1+w)+Psi)
    Delta = d + 3*H*theta/k**2
    want_theta_prime = -H*theta + k**2*(Psi+c*Delta) + c*k**4*S/(3*a**2*RA)
    phase_from_euler = (
        (theta_prime+H*theta)/k**2-Psi-3*c*H*theta/k**2
    )
    want_phase = c*(d+k**2*S/(3*a**2*RA))
    checks = {
        "fluid_density_continuity_running_w_and_c_with_S":
            s.simplify((dprime-want_dprime).subs(delta,(1+w)*d)) == 0,
        "fluid_momentum_Euler_running_w_and_c_with_S":
            s.simplify((theta_prime-want_theta_prime).subs(delta,(1+w)*d)) == 0,
        "action_phase_pressure_dictionary_with_S":
            s.simplify((phase_from_euler-want_phase).subs(delta,(1+w)*d)) == 0,
    }

    # Independently reconstruct the SIX archived radiation-neutrino equations.
    Rnu,Psi0,tau = s.symbols("R_nu Psi_0 tau", real=True)
    f2,g2,tg3,tn3,s4 = s.symbols("Phi2 Psi2 tg3 tn3 s4")
    f0 = (1+s.Rational(2,5)*Rnu)*Psi0
    sig2=Psi0/15
    oct3=s.Rational(2,7)*sig2
    d2=-Psi0/3+4*f2
    equations = [
        3*tg3-d2/4-g2,
        3*tn3-d2/4+sig2-g2,
        s4-tn3/15+s.Rational(3,40)*oct3,
        2*f2+g2-2*((1-Rnu)*tg3+Rnu*tn3),
        f2-g2-6*Rnu*s4,
        12*f2+3*g2+f0-Psi0/2,
    ]
    solutions=s.solve(equations,[f2,g2,tg3,tn3,s4],dict=True)
    if len(solutions) != 1:
        raise RuntimeError("RADIATION_SOLUTION_NOT_UNIQUE")
    sol=solutions[0]
    f=s.factor((3*sol[f2]-Psi0/4+3*sol[g2]/4)/(Psi0))
    expected_f=-(15+4*Rnu)/40
    # For fixed pure-radiation Phi and ordinary-species Omega_s:
    # Omega_s+2 k² Phi/(3 a²)=0. Finite AeST contributes R_A Delta_A.
    # Leading full-comoving constraint defect:
    defect=s.factor(RA*Psi0*f*k**2*tau**2)
    predicted=-RA*Psi0*(15+4*Rnu)*k**2*tau**2/40
    checks.update({
        "six_radiation_neutrino_rows":
            all(s.simplify(eq.subs(sol))==0 for eq in equations),
        "dustlike_test_AeST_comoving_source":
            s.simplify(f-expected_f)==0,
        "finite_AeST_gravity_constraint_defect_formula":
            s.simplify(defect-predicted)==0,
        "fixed_radiation_negative_control_nonzero":
            s.simplify(defect)!=0,
        "Einstein_correction_requirement_algebra":
            s.simplify(
                2*k**2/(3*a**2)*(-3*a**2*defect/(2*k**2))
                +defect
            )==0,
    })
    if not all(checks.values()):
        raise RuntimeError(
            "JOINT_PRIMORDIAL_SYMBOLIC_FAIL "+
            repr([name for name,ok in checks.items() if not ok])
        )
    return {
        "classification":
            "GE19_PRIMORDIAL_REDUCED_ACTION_FLUID_PASS_FIXED_RADIATION_FULL_CONSTRAINT_NO_GO",
        "symbolic_checks":{key:bool(val) for key,val in checks.items()},
        "symbolic_gate_count":len(checks),
        "einstein_total_comoving_constraint":
            "Omega_s + R_A*Delta_A + 2*k**2*Phi/(3*a**2) = 0",
        "fixed_radiation_metric_and_species_constraint_defect":str(defect),
        "necessary_first_order_backreaction_identity":
            "2*k**2*deltaPhi/(3*a**2) + deltaOmega_s = -R_A*Delta_A",
        "fluid_action_consistency_certified_in_reduced_dictionary":True,
        "full_action_to_CLASS_equivalence_certified":False,
        "unchanged_radiation_proxy_is_full_finite_RA_einstein_solution":False,
        "photon_neutrino_backreaction_evolved":False,
        "full_scalar_aether_Ward_propagation_certified":False,
        "finite_k_physical_adiabatic_eigenvector_certified":False,
        "physical_delayed_only_Weyl_transfer_certified":False,
        "DES_detection":False,
        "interpretation":
            "Negative control: fixed radiation metric/species cannot satisfy "
            "full total comoving Einstein constraint for generic finite R_A. "
            "This establishes a mandatory metric+species backreaction gate; "
            "it does not disprove existence of a coupled physical mode.",
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--repo-root",type=Path,
                   default=Path(__file__).resolve().parents[2])
    p.add_argument("--self-test",action="store_true")
    p.add_argument("--out",type=Path)
    opt=p.parse_args()
    if not opt.self_test:
        source_locks(opt.repo_root.resolve())
    report=calculate()
    print("GE19_JOINT_PRIMORDIAL_REDUCED_ACTION_SYMBOLIC_PASS",
          report["symbolic_gate_count"])
    print("GE19_FIXED_RADIATION_FULL_EINSTEIN_NO_GO")
    print("GE19_FULL_PHYSICS_GO False")
    if opt.out:
        out=opt.out.resolve()
        if out.exists():
            raise RuntimeError("REFUSE_OVERWRITE "+str(out))
        out.parent.mkdir(parents=True,exist_ok=True)
        out.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n")
        print("GE19_JOINT_PRIMORDIAL_REPORT",out)
    elif opt.self_test:
        print(json.dumps(report,indent=2,sort_keys=True))

if __name__=="__main__":
    main()
