#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import subprocess
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in __import__('sys').path:
    __import__('sys').path.insert(0, str(ROOT))

from memory_gravity import mcmg_r1_causal_first_moment as r1

PROTOCOL_LOCK = "9d5163251b8bead62ff62bcf008bc2e5001ab5e2"
R1_JSON = ROOT / "results/mcmg_r1_causal_first_moment.json"

U_VALUES = (0.005, 0.01, 0.02, 0.04)
ETA_FINITE = (-0.50, -0.25, 0.0, 0.25, 0.50)
ETA_TAN = 0.01
U_ZERO = 1.0e-5
N_EVAL = 8193

PASS = "MCMG_SELF_CONSISTENT_GROWTH_WEYL_MEMORY_PASS"
NUM_FAIL = "MCMG_SELF_CONSISTENT_NUMERICAL_CONTROL_FAIL"
TAN_FAIL = "MCMG_SELF_CONSISTENT_TANGENT_CONTROL_FAIL"
CONS_FAIL = "MCMG_GROWTH_WEYL_CONSISTENCY_FAIL"
MOM_FAIL = "MCMG_FIRST_MOMENT_SELF_CONSISTENCY_FAIL"
STAB_FAIL = "MCMG_FINITE_AMPLITUDE_STABILITY_FAIL"


def is_ancestor(sha: str) -> bool:
    return subprocess.run(["git","merge-base","--is-ancestor",sha,"HEAD"], cwd=ROOT,
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0


def rel_l2(a, b):
    aa=np.asarray(a,float); bb=np.asarray(b,float)
    return float(np.linalg.norm(aa-bb)/max(np.linalg.norm(aa),np.linalg.norm(bb),1e-300))


def solve_system(eval_growth, u: float, eta: float, N):
    a_ini=r1.A_INI
    d0,v0=eval_growth(np.asarray([a_ini],float))
    y0=[float(d0[0]),float(v0[0]),float(d0[0]/a_ini)]

    def rhs(n,y):
        a=math.exp(n)
        om=float(r1.omega_m(a))
        ee=float(r1.E_of_a(a))
        D,V,M=y
        drive=(1.0-eta)*D + eta*a*M
        return [V, -(2.0-1.5*om)*V + 1.5*om*drive, (D/a-M)/(u*ee)]

    sol=solve_ivp(rhs,(float(N[0]),float(N[-1])),y0,t_eval=N,method="Radau",
                  rtol=2e-10,atol=2e-12,max_step=0.02)
    if not sol.success:
        raise RuntimeError(f"integration failed u={u} eta={eta}: {sol.message}")
    return np.asarray(sol.y,float)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--json-out",default="results/mcmg_r2_self_consistent_growth_weyl.json")
    ap.add_argument("--npz-out",default="results/mcmg_r2_self_consistent_growth_weyl.npz")
    args=ap.parse_args()

    if not is_ancestor(PROTOCOL_LOCK):
        raise SystemExit("MCMG_R2_PROTOCOL_LOCK_FAIL")
    if not R1_JSON.exists():
        raise SystemExit("MCMG_R2_R1_RESULT_MISSING")
    r1j=json.loads(R1_JSON.read_text())
    if r1j.get("classification")!="MCMG_CAUSAL_FIRST_MOMENT_UNIVERSALITY_PASS":
        raise SystemExit("MCMG_R2_R1_PARENT_NOT_PASS")

    print("MCMG_R2_START",flush=True)
    eval_growth=r1.solve_gr_growth()
    N=np.linspace(math.log(r1.A_INI),0.0,N_EVAL)
    a=np.exp(N)
    z=1.0/a-1.0
    win=z<=2.0+1e-12
    D0,V0=eval_growth(a)
    P0=D0/a
    dPdx=r1.E_of_a(a)*(V0-D0)/a
    T=-dPdx/P0

    runs={}
    finite_all=True
    positive_all=True
    etas=sorted(set(ETA_FINITE+(-ETA_TAN,ETA_TAN)))
    for u in U_VALUES:
        for eta in etas:
            y=solve_system(eval_growth,u,eta,N)
            D,V,M=y
            Peff=(1.0-eta)*D/a+eta*M
            ok=bool(np.all(np.isfinite(y)) and np.all(np.isfinite(Peff)))
            pos=bool(np.all(D>0))
            finite_all &= ok
            positive_all &= pos
            runs[(u,eta)]={"D":D,"V":V,"M":M,"P":Peff}
            print(f"MCMG_R2_RUN u={u:.6f} eta={eta:+.3f} D0resp={D[-1]/D0[-1]-1:+.8e} W0resp={Peff[-1]/P0[-1]-1:+.8e}",flush=True)

    # G1
    g1=bool(finite_all and positive_all)

    # G2 eta=0 nested GR
    gr_errs={}
    for u in U_VALUES:
        rr=runs[(u,0.0)]
        gr_errs[str(u)]={"D":rel_l2(rr["D"][win],D0[win]),"P":rel_l2(rr["P"][win],P0[win])}
    g2=bool(max(max(v.values()) for v in gr_errs.values())<=1e-8)

    # G3 zero-memory limit at eta +/-0.5
    zero_errs={}
    for eta in (-0.5,0.5):
        y=solve_system(eval_growth,U_ZERO,eta,N)
        D,V,M=y; P=(1.0-eta)*D/a+eta*M
        zero_errs[str(eta)]={"D":rel_l2(D[win],D0[win]),"P":rel_l2(P[win],P0[win])}
    g3=bool(max(max(v.values()) for v in zero_errs.values())<=2e-5)

    # G4 tangent odd symmetry
    tangent_sym={}
    tangent_C={}
    lag0={}
    first_moment={}
    for u in U_VALUES:
        rp=runs[(u,ETA_TAN)]; rm=runs[(u,-ETA_TAN)]; rz=runs[(u,0.0)]
        gp=rp["D"]/D0-1.0; gm=rm["D"]/D0-1.0
        wp=rp["P"]/P0-1.0; wm=rm["P"]/P0-1.0
        eg=float(np.linalg.norm((gp+gm)[win])/max(np.linalg.norm((gp-gm)[win]),1e-300))
        ew=float(np.linalg.norm((wp+wm)[win])/max(np.linalg.norm((wp-wm)[win]),1e-300))
        tangent_sym[str(u)]={"growth_even_to_odd":eg,"weyl_even_to_odd":ew}
        C=((wp-gp)-(wm-gm))/(2.0*ETA_TAN)
        L=(rz["M"]-P0)/P0
        tangent_C[u]=C; lag0[u]=L
        first_moment[str(u)]={
            "tangent_vs_passive_lag":rel_l2(C[win],L[win]),
            "scaled_vs_first_moment":rel_l2((C/u)[win],T[win]),
        }
    g4=bool(max(max(v.values()) for v in tangent_sym.values())<=0.02)

    # G5 exact tangent consistency
    g5=bool(max(v["tangent_vs_passive_lag"] for v in first_moment.values())<=0.005)

    # G6 first-moment consistency
    e005=first_moment[str(0.005)]["scaled_vs_first_moment"]
    e001=first_moment[str(0.01)]["scaled_vs_first_moment"]
    e002=first_moment[str(0.02)]["scaled_vs_first_moment"]
    g6=bool(e005<=0.02 and e001<=0.03 and e005<e002)

    # G7 finite-amplitude stability/sign
    finite_summary={}
    g7=True
    for u in U_VALUES:
        finite_summary[str(u)]={}
        for eta in (-0.5,-0.25,0.25,0.5):
            rr=runs[(u,eta)]
            g=rr["D"]/D0-1.0; w=rr["P"]/P0-1.0
            rec={"growth_today":float(g[-1]),"weyl_today":float(w[-1]),
                 "max_abs_growth":float(np.max(np.abs(g[win]))),
                 "max_abs_weyl":float(np.max(np.abs(w[win])))}
            finite_summary[str(u)][str(eta)]=rec
            if not (np.sign(rec["growth_today"])==np.sign(eta) and np.sign(rec["weyl_today"])==np.sign(eta)
                    and rec["max_abs_growth"]<0.05 and rec["max_abs_weyl"]<0.05):
                g7=False

    gates={
        "R2_G1_finite_self_consistent_evolution":g1,
        "R2_G2_nested_GR_amplitude_limit":g2,
        "R2_G3_zero_memory_GR_limit":g3,
        "R2_G4_tangent_odd_symmetry_control":g4,
        "R2_G5_growth_weyl_tangent_consistency":g5,
        "R2_G6_first_moment_causal_consistency":g6,
        "R2_G7_finite_amplitude_sign_stability":bool(g7),
    }

    if not all((g1,g2,g3)):
        cls=NUM_FAIL
    elif not g4:
        cls=TAN_FAIL
    elif not g5:
        cls=CONS_FAIL
    elif not g6:
        cls=MOM_FAIL
    elif not g7:
        cls=STAB_FAIL
    else:
        cls=PASS

    summary={
        "classification":cls,
        "max_nested_GR_relative_L2":float(max(max(v.values()) for v in gr_errs.values())),
        "max_zero_memory_relative_L2":float(max(max(v.values()) for v in zero_errs.values())),
        "max_tangent_even_to_odd":float(max(max(v.values()) for v in tangent_sym.values())),
        "max_tangent_vs_passive_lag_relative_L2":float(max(v["tangent_vs_passive_lag"] for v in first_moment.values())),
        "first_moment_error_u0p005":float(e005),
        "first_moment_error_u0p01":float(e001),
        "first_moment_error_u0p02":float(e002),
    }
    out={
        "classification":cls,"diagnostic_complete":True,"protocol_lock":PROTOCOL_LOCK,
        "parent_R1_classification":r1j.get("classification"),"gates":gates,"summary":summary,
        "nested_GR_errors":gr_errs,"zero_memory_errors":zero_errs,"tangent_symmetry":tangent_sym,
        "tangent_consistency":first_moment,"finite_amplitude":finite_summary,
        "interpretation":{"licenses_R3_heldout_generality":bool(cls==PASS),"new_physics_claim_licensed":False,
                          "observational_claim_licensed":False,"Nature_claim_licensed":False},
    }
    Path(args.json_out).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")

    arrays={"N":N,"a":a,"z":z,"D_GR":D0,"P_GR":P0,"first_moment_target":T}
    for u in U_VALUES:
        utag=str(u).replace('.','p')
        arrays[f"C_u{utag}"]=tangent_C[u]
        arrays[f"lag0_u{utag}"]=lag0[u]
        for eta in etas:
            etag=("m" if eta<0 else "p")+str(abs(eta)).replace('.','p')
            rr=runs[(u,eta)]
            arrays[f"D_u{utag}_eta{etag}"]=rr["D"]
            arrays[f"M_u{utag}_eta{etag}"]=rr["M"]
            arrays[f"P_u{utag}_eta{etag}"]=rr["P"]
    np.savez_compressed(args.npz_out,**arrays)

    print("MCMG_R2_GATES="+json.dumps(gates,sort_keys=True),flush=True)
    print("MCMG_R2_SUMMARY="+json.dumps(summary,sort_keys=True),flush=True)
    print("MCMG_R2_CLASSIFICATION="+cls,flush=True)
    return 0 if cls==PASS else 1

if __name__=="__main__":
    raise SystemExit(main())
