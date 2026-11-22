#!/usr/bin/env python3
"""Original Exp + full Einstein/pressureful AeST + primordial radiation k^0,k^2.

A reusable *coefficient ODE operator*, NOT a solved primordial growing mode.
Newtonian gauge, conformal time, CLASS-normalized 8*pi*G/3=1.
Photon-baryon tight coupling; free-streaming massless neutrinos through
octupole; pressureful AeST w_A(a), c_A^2(a) from original Exp action.
No guessed initial vector, numeric cosmology, retarded bath reset or DES fit.

Y(k,tau)=Y0+k^2 Y2+O(k^4), theta_s=k^2(V_s0+k^2 V_s2),
sigma_nu=k^2(Z0+k^2 Z2), F_nu3=k^3 J3+O(k^5).
d_A=delta_A/(1+w_A). Under an *unproved* analytic physical branch
X,S_A=O(k^2), auxiliary forcing first enters Einstein matter at k^4.
"""
from __future__ import annotations
from dataclasses import dataclass
import math
from typing import Mapping

FIELDS=("Phi0","Phi2","dg0","dg2","dn0","dn2","db0","db2",
        "dA0","dA2","vg0","vg2","vn0","vn2","vA0","vA2",
        "zn0","zn2","jn3")

@dataclass(frozen=True)
class ExpParameters:
    Q0:float
    Z0:float
    K2:float
    I0:float  # calibrated positive shift charge K_Q*a^3
    def __post_init__(self):
        if not all(math.isfinite(x) and x>0
                   for x in (self.Q0,self.Z0,self.K2,self.I0)):
            raise ValueError("Exp Q0,Z0,K2,I0 must be finite and positive")

@dataclass(frozen=True)
class ExpState:
    a:float
    z:float
    Q:float
    KQ:float
    KQQ:float
    K:float
    rhoA:float
    wA:float
    cA2:float

def exp_state(a:float,p:ExpParameters)->ExpState:
    """Original positive Exp branch: K_Q(a)=I0/a^3, Z^2+ln Z=ln[K_Q/(4K2Z0)]."""
    if not (math.isfinite(a) and a>0):
        raise ValueError("positive finite scale factor required")
    target=math.log(p.I0)-math.log(4*p.K2*p.Z0)-3*math.log(a)
    def residual(z):return z*z+math.log(z)-target
    lo=1e-300
    hi=1.0
    while residual(hi)<0:
        hi*=2
        if hi>1e100:raise ValueError("Exp positive branch not bracketed")
    for _ in range(100):
        mid=(lo+hi)/2
        if residual(mid)>0:hi=mid
        else:lo=mid
    z=(lo+hi)/2
    Q=p.Q0+p.Z0*z
    KQ=p.I0/a**3
    KQQ=4*p.K2*math.exp(z*z)*(1+2*z*z)
    K=2*p.K2*p.Z0**2*math.expm1(z*z)
    rhoA=(Q*KQ-K)/3
    if not (math.isfinite(rhoA) and rhoA>0):
        raise ValueError("nonphysical Exp background energy density")
    return ExpState(a,z,Q,KQ,KQQ,K,rhoA,K/(3*rhoA),
                    p.Z0*z/(Q*(1+2*z*z)))

@dataclass(frozen=True)
class Background:
    a:float
    Hcal:float
    rho_g:float
    rho_nu:float
    rho_b:float
    rho_A:float
    w_A:float
    c_A2:float
    def __post_init__(self):
        if not all(math.isfinite(x) for x in
                   (self.a,self.Hcal,self.rho_g,self.rho_nu,self.rho_b,
                    self.rho_A,self.w_A,self.c_A2)):
            raise ValueError("nonfinite background value")
        if not (self.a>0 and self.Hcal>0 and self.rho_g>0
                and self.rho_nu>=0 and self.rho_b>=0 and self.rho_A>0):
            raise ValueError("unsupported primordial background sector")
        if not (self.w_A>-1 and self.c_A2>=0):
            raise ValueError("unsupported AeST equation of state")
    @property
    def R_A(self):return self.rho_A*(1+self.w_A)
    @property
    def R_nu(self):return 4*self.rho_nu/3
    @property
    def R_g(self):return 4*self.rho_g/3
    @property
    def baryon_loading(self):return 3*self.rho_b/(4*self.rho_g)

def radiation_baryon_exp_background(a:float,p:ExpParameters,
       rho_g_today:float,rho_nu_today:float,rho_b_today:float)->Background:
    """Exact homogeneous Exp+radiation+baryons in CLASS units; no Lambda at early time.

    Caller supplies all present density normalizations and calibrated I0;
    this function NEVER obtains parameters from observations or hidden data.
    """
    if (not all(math.isfinite(x) and x>=0
                for x in (rho_g_today,rho_nu_today,rho_b_today))
            or rho_g_today==0):
        raise ValueError("invalid supplied standard-species densities")
    e=exp_state(a,p)
    rg=rho_g_today/a**4
    rn=rho_nu_today/a**4
    rb=rho_b_today/a**3
    return Background(a,a*math.sqrt(rg+rn+rb+e.rhoA),
                      rg,rn,rb,e.rhoA,e.wA,e.cA2)

def rhs(y:Mapping[str,float],b:Background)->dict[str,float]:
    """Complete 19-variable k^0+k^2 pressureful, full-Einstein coefficient RHS.

    Cauchy initial vector and full-covariant equivalence are NOT certified.
    No k-dependent / observational templates are constructed here.
    """
    if set(y)!=set(FIELDS):
        raise ValueError("requires exactly the 19 named coefficient fields")
    if any(not math.isfinite(float(y[name])) for name in FIELDS):
        raise ValueError("nonfinite coefficient input")
    a,h=b.a,b.Hcal
    shear_factor=4.5*a*a*b.R_nu
    psi0=y["Phi0"]-shear_factor*y["zn0"]
    psi2=y["Phi2"]-shear_factor*y["zn2"]
    def momentum(i):
        return (b.R_g*y[f"vg{i}"]+b.R_nu*y[f"vn{i}"]
                +b.rho_b*y[f"vg{i}"]+b.R_A*y[f"vA{i}"])
    phi0p=-h*psi0+1.5*a*a*momentum(0)
    phi2p=-h*psi2+1.5*a*a*momentum(2)
    Rb=b.baryon_loading
    def vgprime(i,psi):
        return (-h*Rb*y[f"vg{i}"]+y[f"dg{i}"]/4)/(1+Rb)+psi
    def vAprime(i,psi):
        return -h*y[f"vA{i}"]+psi+b.c_A2*(y[f"dA{i}"]+3*h*y[f"vA{i}"])
    return {
      "Phi0":phi0p,"Phi2":phi2p,
      "dg0":4*phi0p,"dg2":-4*y["vg0"]/3+4*phi2p,
      "dn0":4*phi0p,"dn2":-4*y["vn0"]/3+4*phi2p,
      "db0":3*phi0p,"db2":-y["vg0"]+3*phi2p,
      "dA0":3*phi0p,"dA2":-y["vA0"]+3*phi2p,
      "vg0":vgprime(0,psi0),"vg2":vgprime(2,psi2),
      "vn0":y["dn0"]/4+psi0,
      "vn2":y["dn2"]/4+psi2-y["zn0"],
      "vA0":vAprime(0,psi0),"vA2":vAprime(2,psi2),
      "zn0":4*y["vn0"]/15,
      "zn2":4*y["vn2"]/15-3*y["jn3"]/10,
      "jn3":6*y["zn0"]/7,
    }

def constraints(y:Mapping[str,float],b:Background)->dict[str,float]:
    """Einstein Hamiltonian and comoving k^0+k^2 residuals.

    After imposing the momentum equation, these pairs are redundant:
    Hamiltonian_kN=(3/2)*a*a*comoving_kN, N=0 and 2.
    These are not independent physical consistency gates.
    """
    d=rhs(y,b)
    a,h=b.a,b.Hcal
    psi0=y["Phi0"]-4.5*a*a*b.R_nu*y["zn0"]
    psi2=y["Phi2"]-4.5*a*a*b.R_nu*y["zn2"]
    def density(i):
        return (b.rho_g*y[f"dg{i}"]+b.rho_nu*y[f"dn{i}"]
             +b.rho_b*y[f"db{i}"]+b.R_A*y[f"dA{i}"])
    def omega_s(i):
        return (b.rho_g*(y[f"dg{i}"]+4*h*y[f"vg{i}"])
             +b.rho_nu*(y[f"dn{i}"]+4*h*y[f"vn{i}"])
             +b.rho_b*(y[f"db{i}"]+3*h*y[f"vg{i}"]))
    return {
        "Hamiltonian_k0":3*h*(d["Phi0"]+h*psi0)+1.5*a*a*density(0),
        "Hamiltonian_k2":y["Phi0"]+3*h*(d["Phi2"]+h*psi2)
                        +1.5*a*a*density(2),
        "comoving_k0":omega_s(0)+b.R_A*(y["dA0"]+3*h*y["vA0"]),
        "comoving_k2":omega_s(2)+b.R_A*(y["dA2"]+3*h*y["vA2"])
                       +2*y["Phi0"]/(3*a*a),
    }

def driver_delta_A2(y:Mapping[str,float],b:Background)->float:
    """Constrained physical fluid-source coefficient (not a dust proxy)."""
    return y["dA2"]+3*b.Hcal*y["vA2"]

def entropy_rate_identities(y:Mapping[str,float],b:Background)->dict[str,float]:
    """Algebraic k^2 sources of relative entropy (residuals all zero)."""
    d=rhs(y,b)
    return {
        "AeST_photon_S0prime":d["dA0"]-0.75*d["dg0"],
        "AeST_photon_S2prime_minus_velocity_slip":
            d["dA2"]-0.75*d["dg2"]-(y["vg0"]-y["vA0"]),
        "baryon_photon_S0prime":d["db0"]-0.75*d["dg0"],
        "baryon_photon_S2prime":d["db2"]-0.75*d["dg2"],
        "neutrino_photon_S2prime_minus_velocity_slip":
            d["dn2"]-d["dg2"]-4*(y["vg0"]-y["vn0"])/3,
    }

def specification()->dict:
    return {
      "classification":"GE19_JOINT_EXP_PRESSUREFUL_K0_K2_COEFFICIENT_OPERATOR_ASSEMBLED_NOT_PRIMORDIAL_SELECTED",
      "n_fields":len(FIELDS),"fields":list(FIELDS),
      "expansion":"Y=Y0+k²Y2; theta=k²(V0+k²V2); sigma_nu=k²(Z0+k²Z2); F_nu3=k³J3",
      "gauge":"conformal Newtonian","time":"conformal tau",
      "background":"original Exp KQ=I0/a³, rhoA=(QKQ-K)/3, wA=K/(QKQ-K), cA²=KQ/(QKQQ); Friedmann includes all species",
      "species":"early tight-coupled photons+baryons, massless neutrino multipoles through F3, pressureful AeST fluid; full additive Einstein",
      "source":"Delta_A2=dA2+3 Hcal vA2; dA=deltaA/(1+wA)",
      "entropy_identity":"(dA2-3 dg2/4)'=v_gamma0-v_A0",
      "assumption":"analytic X,S_A=O(k²), zero direct linear bath stress at relaxed background; unproved full physical primordial branch",
      "constraint_redundancy":"Hamiltonian_kN=(3/2)a^2*comoving_kN, N=0,2, after momentum equation",
      "primordial_mode_selected":False,"evolved":False,"class_executed":False,
      "FULL_PHYSICS_GO":False,"DES_detection":False,
    }

if __name__=="__main__":
    import argparse,json
    from pathlib import Path
    p=argparse.ArgumentParser()
    p.add_argument("--spec",action="store_true")
    p.add_argument("--out",type=Path)
    args=p.parse_args()
    if not (args.spec or args.out):
        p.error("Requires --spec/--out: no unphysical default initial mode")
    doc=specification()
    if args.out:
        if args.out.exists():p.error("REFUSE_OVERWRITE "+str(args.out))
        args.out.parent.mkdir(parents=True,exist_ok=True)
        args.out.write_text(json.dumps(doc,indent=2,sort_keys=True)+"\n")
    if args.spec:print(json.dumps(doc,indent=2,sort_keys=True))
