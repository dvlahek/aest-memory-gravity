#!/usr/bin/env python3
"""H4F2a: off-shell GE07 dust spatial covariance, an H4F2 subset only."""
from __future__ import annotations
import argparse,json,subprocess
from pathlib import Path
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
BLOBS={
 "ge19/h4f2_predata_complete_mixed_h4_ward_parent_dictionary.json":"8097a4770ae8aed74cb4dd0721c1c9bd6907533c",
 "ge07/pressureless_matter_directional_source_generator.py":"cde8da77a80799cef00fc7c09c3633310fc9e3d4",
 "docs/ge19_h4f1_longitudinal_bath_ward_valid_freeze.md":"5aa99f10383a253e934c0c2833230fa714c3ef1d",
}
def iszero(expr):
    return bool(sp.factor(sp.cancel(sp.together(expr)))==0)
def prove():
    N,L,R,b,rho,Tt,Tx=sp.symbols("N L R b rho Tt Tx",real=True)
    Nx,Lx,Rx,bx,rhox,Ttx,Txx=sp.symbols(
        "Nx Lx Rx bx rhox Ttx Txx",real=True)
    xi,xix,xit=sp.symbols("xi xix xit",real=True)
    grad={N:Nx,L:Lx,R:Rx,b:bx,rho:rhox,Tt:Ttx,Tx:Txx}
    delta={N:xi*Nx,L:xi*Lx+L*xix,R:xi*Rx,
           b:xi*bx+xit-b*xix,rho:xi*rhox,
           Tt:xi*Ttx+xit*Tx,Tx:xi*Txx+xix*Tx}
    def d(expr,direction):
        return sum(sp.diff(expr,var)*v for var,v in direction.items())
    def scalar(expr):
        return iszero(d(expr,delta)-xi*d(expr,grad))
    def density(expr):
        return iszero(d(expr,delta)-xi*d(expr,grad)-xix*expr)
    W=(Tt-b*Tx)/N
    V=Tx/L
    volume=N*L*R**2
    dust_constraint=W**2-V**2-1
    lag=volume*rho*dust_constraint
    wrong=dict(delta);wrong[rho]=xi*rhox+xix*rho
    wrong_defect=d(lag,wrong)-xi*d(lag,grad)-xix*lag
    tests={
      "GE07_W_scalar":scalar(W),
      "GE07_V_scalar":scalar(V),
      "GE07_rho_scalar_off_shell":scalar(rho),
      "GE07_constraint_scalar":scalar(dust_constraint),
      "GE07_volume_density":density(volume),
      "GE07_full_lag_density_off_shell":density(lag),
      "wrong_rho_density_has_extra_lag":iszero(wrong_defect-xix*lag),
      "wrong_rho_density_not_off_shell":not iszero(wrong_defect),
    }
    source=(ROOT/"ge07/pressureless_matter_directional_source_generator.py").read_text()
    compact="".join(source.split())
    bindings={
      "frozen_GE07_lag":("lag=sp.expand(N*L*R**2*varrho*(W**2-V**2-1))" in compact),
      "frozen_GE07_W":("W=(Tt-b*Tx)/N" in compact),
      "frozen_GE07_V":("V=Tx/L" in compact),
      "frozen_GE07_rho_Euler":('"rho_f":sp.diff(lag,varrho)' in compact),
      "frozen_GE07_Tt_Tx_Euler":('"T_t":sp.diff(lag,Tt)' in compact
                                 and '"T_x":sp.diff(lag,Tx)' in compact),
    }
    return tests,bindings
def main():
    ap=argparse.ArgumentParser();ap.add_argument("--json-out",required=True)
    args=ap.parse_args()
    blobs={}
    for name,expected in BLOBS.items():
        got=subprocess.check_output(["git","rev-parse","HEAD:"+name],
                                    cwd=ROOT,text=True).strip()
        blobs[name]={"expected":expected,"observed":got,"exact":got==expected}
    tests,bindings=prove()
    ok=all(v["exact"] for v in blobs.values()) and all(tests.values()) and all(bindings.values())
    out={
      "classification":("GE19_H4F2A_DUST_OFFSHELL_WARD_DERIVED" if ok else
                        "GE19_H4F2A_DUST_WARD_UNRESOLVED"),
      "frozen_blobs":blobs,"GE07_action_bindings":bindings,
      "dust_offshell_spatial_covariance":tests,
      "dust_multiplier_transformation":"delta varrho=xi varrho_x (scalar, not spatial density)",
      "density_weight_one_rho_defect":"xi_x * L_dust; generally nonzero off shell",
      "dust_parent_contributions_to_formal_Ward":"E_T*T_x + E_varrho*varrho_x",
      "all_subset_gates_pass":bool(ok),
      "full_mixed_H4_source_Noether_derived":False,
      "H4_Z21_solve_performed":False,"Z21_certified":False,"lensing_licensed":False,
      "next_route":"DERIVE_SIGNED_MIXED_H4_WARD_COEFFICIENT_AND_SIX_PIECE_SOURCE_DICTIONARY",
    }
    p=Path(args.json_out);p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps(out,indent=2,sort_keys=True))
    if not ok:raise SystemExit(3)
if __name__=="__main__":main()
