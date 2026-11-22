#!/usr/bin/env python3
"""GE19 invariant adiabatic k0, k2 Einstein--Exp--matter source reduction.

Exactly reduces the PREVIOUS source-verified 19-variable primordial
tight-coupling/fluid coefficient operator on a selected non-isocurvature
adiabatic manifold. 9 dynamical variables + constant curvature; not a
full scalar/aether primordial Ward selection, bath history or DES signal.

Requires Newtonian gauge, positive Exp expanding background, and analytic
X,S_A=O(k^2) of the *unproved* original full covariant physical mode.
"""
from __future__ import annotations

import argparse
import json
import math
import subprocess
from pathlib import Path
from typing import Mapping

from ge19.physics_gate.primordial_exp_pressureful_joint_k2_system_20261122 import (
    Background, FIELDS, rhs as full_rhs, constraints as full_constraints
)

SOURCE_LOCKS = {
 "ge19/physics_gate/primordial_exp_pressureful_joint_k2_system_20261122.py":
  "716ba23eaeb683c48a0f2fdcae52663b8d4bfe70",
 "ge19/physics_gate/coupled_mixed_y_k2_photon_baryon_neutrino_20261121.py":
  "1a5736e05eb6c02dc3a05dc8334014088adef16d",
 "ge19/physics_gate/primordial_k2_XS_retarded_bath_hierarchy_20261122.py":
  "a7fa9069fb2670a0231ed8374d09ebd0b684d192",
}

# Curvature is an integration constant, rather than another evolving mode.
STATE=("calR","V0","Znu0","Phi2","dg2","Vg2","Vnu2","VA2","Znu2","Jnu3")

def leading_adiabatic_state(z:Mapping[str,float],b:Background)->dict[str,float]:
    """Reconstruct the complete 19 state on the adiabatic k0/k2 subspace.

    U_s0=delta_s0+3Hcal(1+w_s)V_s0=0, all V_s0=V0;
    no primordial relative entropy at k0 OR k2, so
    dA2=db2=3*dg2/4 and dn2=dg2.

    This is a physically MOTIVATED SELECTION, not a proof that the
    original full covariant scalar/aether Noether/Ward eigenvector
    or NL0B bath selects the same branch.
    """
    if set(z)!=set(STATE):
        raise ValueError("expected precisely 10 fields: calR + nine evolving values")
    if any(not math.isfinite(float(z[key])) for key in STATE):
        raise ValueError("nonfinite reduced state")
    h=b.Hcal
    v=z["V0"]
    phi0=z["calR"]-h*v
    dg0=-4*h*v
    dust0=-3*h*v
    d2=z["dg2"]
    y={
      "Phi0":phi0,"Phi2":z["Phi2"],
      "dg0":dg0,"dg2":d2,
      "dn0":dg0,"dn2":d2,
      "db0":dust0,"db2":3*d2/4,
      "dA0":dust0,"dA2":3*d2/4,
      "vg0":v,"vg2":z["Vg2"],
      "vn0":v,"vn2":z["Vnu2"],
      "vA0":v,"vA2":z["VA2"],
      "zn0":z["Znu0"],"zn2":z["Znu2"],"jn3":z["Jnu3"],
    }
    assert set(y)==set(FIELDS)
    return y

def reduced_rhs(z:Mapping[str,float],b:Background)->dict[str,float]:
    """Exact 9-dimensional ODE plus calR'=0. Actual full Exp h(a) supplied."""
    y=leading_adiabatic_state(z,b)
    a,h=b.a,b.Hcal
    psi0=y["Phi0"]-4.5*a*a*b.R_nu*z["Znu0"]
    psi2=z["Phi2"]-4.5*a*a*b.R_nu*z["Znu2"]
    p2prime=-h*psi2+1.5*a*a*(
      (b.R_g+b.rho_b)*z["Vg2"]+b.R_nu*z["Vnu2"]+b.R_A*z["VA2"])
    rb=b.baryon_loading
    return {
        "calR":0.0,
        "V0":psi0-h*z["V0"],
        "Znu0":4*z["V0"]/15,
        "Phi2":p2prime,
        "dg2":-4*z["V0"]/3+4*p2prime,
        "Vg2":(-h*rb*z["Vg2"]+z["dg2"]/4)/(1+rb)+psi2,
        "Vnu2":z["dg2"]/4+psi2-z["Znu0"],
        "VA2":-h*z["VA2"]+psi2+
              b.c_A2*(3*z["dg2"]/4+3*h*z["VA2"]),
        "Znu2":4*z["Vnu2"]/15-3*z["Jnu3"]/10,
        "Jnu3":6*z["Znu0"]/7,
    }

def initial_comoving_k2(z:Mapping[str,float],b:Background)->float:
    """The ONE independent k2 Einstein Cauchy constraint (not a fit)."""
    y=leading_adiabatic_state(z,b)
    return full_constraints(y,b)["comoving_k2"]

def driving_delta_A2(z:Mapping[str,float],b:Background)->float:
    """What the original quarter-action X2/S2 system must actually receive."""
    return 0.75*z["dg2"]+3*b.Hcal*z["VA2"]

def full_operator_reconstruction_residuals(
        z:Mapping[str,float],b:Background)->dict[str,float]:
    """Directly reconstruct derivatives of all 19 fields and compare.

    Uses the FULL provided Exp pressureful/homogeneous background
    derivative h' = h^2-(3/2)a^2 sum(rho+p); no cosmological integration.
    """
    y=leading_adiabatic_state(z,b)
    dr=reduced_rhs(z,b)
    reference=full_rhs(y,b)
    h=b.Hcal
    hp=h*h-1.5*b.a*b.a*(b.R_g+b.R_nu+b.rho_b+b.R_A)
    vp=dr["V0"]
    phi0p=-(hp*z["V0"]+h*vp)  # calR'=0
    dg0p=-4*(hp*z["V0"]+h*vp)
    d0p=-3*(hp*z["V0"]+h*vp)
    dg2p=dr["dg2"]
    explicit={
      "Phi0":phi0p,"Phi2":dr["Phi2"],
      "dg0":dg0p,"dg2":dg2p,
      "dn0":dg0p,"dn2":dg2p,
      "db0":d0p,"db2":0.75*dg2p,
      "dA0":d0p,"dA2":0.75*dg2p,
      "vg0":vp,"vg2":dr["Vg2"],
      "vn0":vp,"vn2":dr["Vnu2"],
      "vA0":vp,"vA2":dr["VA2"],
      "zn0":dr["Znu0"],"zn2":dr["Znu2"],
      "jn3":dr["Jnu3"],
    }
    return {k:explicit[k]-reference[k] for k in FIELDS}

def regular_radiation_normalization(Rnu_fraction:float,curv:float)->dict[str,float]:
    """Strict a~tau, rho_m/rho_r->0 Frobenius leading mode per calR.

    The regular radiation growing mode has V0~v*tau, Znu0~2v*tau^2/15.
    Non-regular homogeneous exponents obey (p+1)(p+2)+8Rnu/5=0.
    No k2 seed or Q-bath value is prescribed here.
    """
    if not (0<=Rnu_fraction<=1 and math.isfinite(curv)):
        raise ValueError("invalid radiation fraction or curvature")
    v=curv/(3+4*Rnu_fraction/5)
    psi=2*v
    return {
       "V0_over_tau":v,"Znu0_over_tau2":2*v/15,
       "Psi0":psi,"Phi0":curv-v,
       "calR":curv,
       "indicial_polynomial":"(p+1)(p+2)+8Rnu/5=0",
       "all_homogeneous_velocity_exponents_have_negative_real_part":True,
       "full_X2_S2_primordial_selected":False,
    }

def specification()->dict:
    return {
      "classification":"GE19_EXACT_ADIABATIC_K0_INVARIANT_MANIFOLD_AND_K2_7ROW_REDUCTION_NOT_FULL_PRIMORDIAL",
      "input_operator_locked":"primordial_exp_pressureful_joint_k2_system_20261122",
      "state_fields":list(STATE),"number_evolving_fields":9,
      "curvature_conserved":"calR=Phi0+Hcal V0",
      "k0_conditions":"V_gamma0=V_nu0=V_A0=V; delta_gamma0=delta_nu0=-4Hcal V; delta_b0=d_A0=-3Hcal V",
      "k2_adiabatic_density":"delta_nu2=delta_gamma2, delta_b2=d_A2=3 delta_gamma2/4; zero relative entropy initial state",
      "one_independent_k2_constraint":"C2=Omega_s2+R_A Delta_A2+2Phi0/(3a^2)=0",
      "physical_AeST_driver":"Delta_A2=3 delta_gamma2/4+3 Hcal V_A2",
      "radiation_indicial":"(p+1)(p+2)+8Rnu/5=0 for free k0 V, both Re p<0",
      "Volterra":"V0(tau)=a^-2 int_0^tau a^2 [calR-(9/2)a^2 R_nu Znu0] ds; Znu0=4/15 int_0^tau V0 ds",
      "required_next":"select k2 growing Frobenius eigenvector jointly with original scalar/aether Ward and retarded bath",
      "covariant_action_full_Ward":False,"complete_physical_growing_mode":False,
      "cosmology_run":False,"DES_detection":False,"FULL_PHYSICS_GO":False,
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--repo-root",type=Path,default=Path(__file__).resolve().parents[2])
    p.add_argument("--spec",action="store_true")
    p.add_argument("--out",type=Path)
    p.add_argument("--no-source-lock",action="store_true")
    args=p.parse_args()
    if not (args.out or args.spec):
        p.error("requires --spec or --out; no guessed primordial numerical initial data")
    if not args.no_source_lock:
        for source,blob in SOURCE_LOCKS.items():
            path=args.repo_root/source
            if not path.is_file():
                raise RuntimeError("MISSING_PROJECT_SOURCE "+source)
            actual=subprocess.check_output(["git","hash-object",str(path)],
                            cwd=args.repo_root,text=True).strip()
            if actual!=blob:
                raise RuntimeError("PROJECT_SOURCE_CHANGED "+source+" "+actual)
        print("GE19_ADIABATIC_K0_K2_SOURCE_LOCKS_PASS",len(SOURCE_LOCKS))
    report=specification()
    if args.out:
        dest=args.out
        if dest.exists():raise RuntimeError("REFUSE_OVERWRITE "+str(dest))
        dest.parent.mkdir(parents=True,exist_ok=True)
        dest.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n")
        print("GE19_ADIABATIC_K2_OPERATOR_REPORT",str(dest))
    if args.spec:print(json.dumps(report,indent=2,sort_keys=True))
    print("GE19_FULL_PHYSICS_GO False")
if __name__=="__main__":
    main()
