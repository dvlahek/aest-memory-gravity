#!/usr/bin/env python3
"""GE19 Repair09 exact symbolic rank audit for canonical constraint partitions.

The action is the frozen GE06 Einstein+AeST analytic action plus the frozen
GE07 dust action.  K(Q) is represented by its generic local quadratic jet,
which is sufficient for the complete first-order algebraic matrix.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sympy as sp


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--json-out",required=True)
    args=ap.parse_args()

    N,L,R,b,u,phi=sp.symbols("N L R b u phi", real=True)
    Lt,Lx,Rt,Rx,bx,ut,ux,pt,px,Nx=sp.symbols(
        "Lt Lx Rt Rx bx ut ux pt px Nx", real=True
    )
    KB,C=sp.symbols("KB C", nonzero=True, real=True)
    Qb=sp.symbols("Qb", real=True)
    K0,K1,KQQ=sp.symbols("K0 K1 KQQ", real=True)

    ch,sh=sp.cosh(u),sp.sinh(u)
    kL=(Lt-b*Lx-L*bx)/(N*L)
    kR=(Rt-b*Rx)/(N*R)
    sigma=(pt-b*px)/N
    Qinv=ch*sigma+sh*px/L
    Xinv=sh*sigma+ch*px/L
    E=ch*((ut-b*ux)/N+Nx/(N*L))+sh*(kL+ux/L)

    dq=Qinv-Qb
    Kfun=K0+K1*dq+sp.Rational(1,2)*KQQ*dq**2

    grav=(
        N*L*R**2*(-4*kL*kR-2*kR**2)
        +2*N*Rx**2/L
        +4*Nx*R*Rx/L
    )
    aest=N*L*R**2*(KB*E**2+2*C*E*Xinv-C*Xinv**2+2*Kfun)
    lag=sp.expand(grav+aest)

    partials={
        "N_f":sp.diff(lag,N),
        "N_x":sp.diff(lag,Nx),
        "L_f":sp.diff(lag,L),
        "L_t":sp.diff(lag,Lt),
        "L_x":sp.diff(lag,Lx),
        "R_f":sp.diff(lag,R),
        "R_t":sp.diff(lag,Rt),
        "R_x":sp.diff(lag,Rx),
        "b_f":sp.diff(lag,b),
        "b_x":sp.diff(lag,bx),
        "u_f":sp.diff(lag,u),
        "u_t":sp.diff(lag,ut),
        "u_x":sp.diff(lag,ux),
        "phi_t":sp.diff(lag,pt),
        "phi_x":sp.diff(lag,px),
    }

    varrho,Tt,Tx=sp.symbols("varrho Tt Tx", real=True)
    W=(Tt-b*Tx)/N
    V=Tx/L
    lagm=sp.expand(N*L*R**2*varrho*(W**2-V**2-1))
    pm={
        "N_f":sp.diff(lagm,N),
        "L_f":sp.diff(lagm,L),
        "R_f":sp.diff(lagm,R),
        "b_f":sp.diff(lagm,b),
        "rho_f":sp.diff(lagm,varrho),
        "T_t":sp.diff(lagm,Tt),
        "T_x":sp.diff(lagm,Tx),
    }

    eps=sp.symbols("eps", real=True)
    aa,adot,rhob,k=sp.symbols("a adot rhob k", nonzero=True, real=True)
    dN,dr,S,du,dphi,dT,Sdot,udot,phidot,Tdot=sp.symbols(
        "dN dr S du dphi dT Sdot udot phidot Tdot", real=True
    )
    I=sp.I

    subg={
        N:1+eps*dN,
        L:aa+eps*S,
        R:aa+eps*S,
        b:0,
        u:eps*du,
        Lt:adot+eps*Sdot,
        Lx:eps*I*k*S,
        Rt:adot+eps*Sdot,
        Rx:eps*I*k*S,
        bx:0,
        ut:eps*udot,
        ux:eps*I*k*du,
        pt:Qb+eps*phidot,
        px:eps*I*k*dphi,
        Nx:eps*I*k*dN,
    }
    subm={
        N:1+eps*dN,
        L:aa+eps*S,
        R:aa+eps*S,
        b:0,
        varrho:rhob+eps*dr,
        Tt:1+eps*Tdot,
        Tx:eps*I*k*dT,
    }

    c1={
        name:sp.expand(sp.diff(expr.subs(subg),eps).subs(eps,0))
        for name,expr in partials.items()
    }
    m1={
        name:sp.expand(sp.diff(expr.subs(subm),eps).subs(eps,0))
        for name,expr in pm.items()
    }

    pS=c1["L_t"]+c1["R_t"]
    pu=c1["u_t"]
    pphi=c1["phi_t"]
    pT=m1["T_t"]
    Erho=m1["rho_f"]
    shift=(c1["b_f"]-I*k*c1["b_x"])+m1["b_f"]
    aniso=(
        (c1["L_f"]-I*k*c1["L_x"])
        -sp.Rational(1,2)*(c1["R_f"]-I*k*c1["R_x"])
        +m1["L_f"]-sp.Rational(1,2)*m1["R_f"]
    )

    zvars=[dN,dr,Sdot,udot,phidot,Tdot]
    def matrix(rows):
        return sp.Matrix([[sp.diff(row,z) for z in zvars] for row in rows])

    common=[pS,pu,pphi,pT,Erho]
    Ashift=matrix(common+[shift])
    Aaniso=matrix(common+[aniso])

    rank_shift=int(Ashift.rank())
    det_shift=sp.factor(Ashift.det())
    rank_aniso=int(Aaniso.rank())
    det_aniso=sp.factor(Aaniso.det())

    expected_aniso=384*KB*KQQ*aa**13*k**2
    aniso_identity=bool(sp.simplify(det_aniso-expected_aniso)==0)

    K2,Z=sp.symbols("K2 Z", positive=True, real=True)
    KQQ_exp=4*K2*sp.exp(Z**2)*(1+2*Z**2)
    det_exp=sp.factor(expected_aniso.subs(KQQ,KQQ_exp))

    passed=bool(
        rank_shift==5
        and det_shift==0
        and rank_aniso==6
        and aniso_identity
    )

    result={
        "classification":(
            "GE19_REPAIR09_SHIFT_PARTITION_STRUCTURALLY_SINGULAR"
            if passed else
            "GE19_REPAIR09_SYMBOLIC_PARTITION_AUDIT_FAIL"
        ),
        "generic_K_jet_sufficient_for_first_order":True,
        "unknown_order":["N","delta_varrho","Sdot","udot","phidot","Tdot"],
        "common_rows":["pS","pu","pphi","pT","dust_density"],
        "shift_partition":{
            "sixth_row":"shift",
            "rank":rank_shift,
            "determinant":str(det_shift),
            "structurally_singular":bool(rank_shift<6 and det_shift==0),
        },
        "anisotropy_partition":{
            "sixth_row":"anisotropy",
            "rank":rank_aniso,
            "determinant":str(det_aniso),
            "expected_generic_determinant":str(expected_aniso),
            "identity_exact":aniso_identity,
            "Exp_branch_determinant":str(det_exp),
        },
        "routing":"reduced-background and omitted-vacuum-sector on-shell consistency",
        "claim_boundary":"Exact symbolic DAE partition diagnosis only; no evolution or H3/Z20 result."
    }

    out=Path(args.json_out)
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps(result,indent=2,sort_keys=True))
    if not passed:
        raise SystemExit(2)


if __name__=="__main__":
    main()
