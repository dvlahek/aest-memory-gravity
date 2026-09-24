#!/usr/bin/env python3
"""H4F2c: complete reduced action spatial density, NOT six-piece H4 sources.

Build all frozen GE06 Einstein/AeST, NL0C Y, GE07 dust, NL0B GE05
longitudinal-node and Lambda action-density sectors from source-bound
scalar/volume primitives. Prove the density transformation, including
the plane GR integrated-curvature terms and both one-sided Y branches.

The independent invariant transformations are certified by earlier
Stage B, H4F1 and H4F2a frozen source-bound proofs. A formal action
Ward identity follows, but its actual mixed six-piece source/parent
coefficient and common-grid implementation are not computed here.
"""
from __future__ import annotations
import argparse,json,subprocess
from pathlib import Path
import sympy as sp

ROOT=Path(__file__).resolve().parents[1]
BLOBS={
 "ge19/h4f2_predata_complete_mixed_h4_ward_parent_dictionary.json":"8097a4770ae8aed74cb4dd0721c1c9bd6907533c",
 "ge06/analytic_aest_directional_source_generator.py":"a7afe0035054a9dca55d74a6497c081422114b4c",
 "ge07/pressureless_matter_directional_source_generator.py":"cde8da77a80799cef00fc7c09c3633310fc9e3d4",
 "ge05/memory_directional_source_generator.py":"40837d77f89028da30c28899e2d0530a4401844e",
 "ge19/repair14_self_consistent_reduced_h3_z20_particular.py":"06c5ced952c2370cfa4aaadb6ef8f72d2d7221de",
 "docs/ge19_h4_staged_common_y_action_rows_valid_freeze.md":"7d140a608d91a39106c34565cd50e4aa729ec30b",
 "docs/ge19_h4f1_longitudinal_bath_ward_valid_freeze.md":"5aa99f10383a253e934c0c2833230fa714c3ef1d",
 "docs/ge19_h4f2a_dust_offshell_ward_valid_freeze.md":"ca21c65ce2da8d760aa12018aefd849b3b67adf9",
 "docs/ge19_h4f2b_signed_mixed_ward_template_valid_freeze.md":"98693317485149898830eebd0f335db12024e6dc",
 "ge19/h4_structural_stage_b_geometric_ward_primitives.py":"5695cf064dcc32bf4385687cbe6052521f2e36b4",
}
def pinned():
    d={}
    for path,expected in BLOBS.items():
        observed=subprocess.check_output(
            ["git","rev-parse","HEAD:"+path],cwd=ROOT,text=True).strip()
        d[path]={"expected":expected,"observed":observed,"exact":observed==expected}
    return d

def bind():
    g=(ROOT/"ge06/analytic_aest_directional_source_generator.py").read_text()
    d=(ROOT/"ge07/pressureless_matter_directional_source_generator.py").read_text()
    m=(ROOT/"ge05/memory_directional_source_generator.py").read_text()
    l=(ROOT/"ge19/repair14_self_consistent_reduced_h3_z20_particular.py").read_text()
    y=(ROOT/"docs/ge19_h4_staged_common_y_action_rows_valid_freeze.md").read_text()
    compact=lambda s:"".join(s.split())
    return {
      "GE06_raw_GR_kinetic_and_plane_curvature":
        "grav=N*L*R**2*(-4*kL*kR-2*kR**2)+2*N*Rx**2/L+4*Nx*R*Rx/L" in compact(g),
      "GE06_raw_AeST_scalar_invariants":
        "aest=N*L*R**2*(KB*E**2+2*C*E*Xinv-C*Xinv**2+2*Kfun)" in compact(g),
      "GE07_exact_offshell_dust":
        "lag=sp.expand(N*L*R**2*varrho*(W**2-V**2-1))" in compact(d),
      "GE05_actual_per_node_reduced_action":
        "lag=N*L*R**2*sp.Rational(1,4)*(Aq**2-(om*q-sw*Xphi)**2)" in compact(m),
      "frozen_Lambda_density":"L_lambda=-6rho_lambdaNLR^2" in compact(l),
      "NL0C_Y_relative_action_factor_bound":
        "relative NL0C-to-GE06 raw action factor is **1**" in y,
    }

def exact_density():
    N,L,R,Nx,Rx=sp.symbols("N L R Nx Rx",real=True)
    Nxx,Rxx,Lx,Rgrad=sp.symbols("Nxx Rxx Lx Rgrad",real=True)
    kn,kr,E,X,Q,kB,C,rho,TW,TV,Aq,q=sp.symbols(
        "kn kr E X Q kB C rho TW TV Aq q",real=True)
    knx,krx,Ex,Xx,Qx,kBx,Cx,rhox,TWx,TVx,Aqx,qx=sp.symbols(
        "knx krx Ex Xx Qx kBx Cx rhox TWx TVx Aqx qx",real=True)
    xi,xix=sp.symbols("xi xix",real=True)
    K=sp.Function("K")(Q)
    J=sp.Function("J")(X)
    omega,sw,rl=sp.symbols("omega sw rho_lambda",real=True)
    volume=N*L*R**2
    gradient={N:Nx,L:Lx,R:Rx,Nx:Nxx,Rx:Rxx,
              kn:knx,kr:krx,E:Ex,X:Xx,Q:Qx,kB:kBx,
              C:Cx,rho:rhox,TW:TWx,TV:TVx,Aq:Aqx,q:qx}
    delta={N:xi*Nx,L:xi*Lx+L*xix,R:xi*Rx,
           Nx:xi*Nxx+xix*Nx,Rx:xi*Rxx+xix*Rx,
           kn:xi*knx,kr:xi*krx,E:xi*Ex,
           X:xi*Xx,Q:xi*Qx,kB:xi*kBx,C:xi*Cx,
           rho:xi*rhox,TW:xi*TWx,TV:xi*TVx,
           Aq:xi*Aqx,q:xi*qx}
    def directional(expr,mapping):
        return sum((sp.diff(expr,v)*w for v,w in mapping.items()),sp.S.Zero)
    def test(expr):
        return bool(sp.simplify(directional(expr,delta)-
            xi*directional(expr,gradient)-xix*expr)==0)
    grav_kin=volume*(-4*kn*kr-2*kr**2)
    grav_plane=2*N*Rx**2/L+4*Nx*R*Rx/L
    aest=volume*(kB*E**2+2*C*E*X-C*X**2+2*K)
    ysector=-volume*C*J
    dust=volume*rho*(TW**2-TV**2-1)
    memory=volume*sp.Rational(1,4)*(Aq**2-(omega*q-sw*X)**2)
    lamb=-6*rl*volume
    pieces={
        "GR_ADM_kinetic":grav_kin,
        "GR_plane_integrated_curvature":grav_plane,
        "GE06_analytic_AeST":aest,
        "NL0C_nonanalytic_Y_as_C1_function_of_X":ysector,
        "GE07_dust_off_shell":dust,
        "GE05_NL0B_per_node_bath":memory,
        "Lambda_density":lamb,
    }
    checks={name:test(expr) for name,expr in pieces.items()}
    total=sum(pieces.values(),sp.S.Zero)
    checks["complete_reduced_action_spatial_density"]=test(total)
    # J(X)=c|X|^3: branch signs must not change its spatial density.
    checks["Y_positive_strict_branch"]=test(ysector.subs(J,X**3))
    checks["Y_negative_strict_branch"]=test(ysector.subs(J,-X**3))
    zero_set=sp.symbols("h",real=True)
    checks["Y_flux_directional_zero_set_continuity"]=bool(
        sp.limit(2*sp.Abs(X)*zero_set,X,0,dir="+")==0
        and sp.limit(2*sp.Abs(X)*zero_set,X,0,dir="-")==0)
    checks["plane_GR_curvature_uses_Nx_Rx_gradients"]=bool(
        test(grav_plane) and test(2*N*Rx**2/L) and test(4*Nx*R*Rx/L))
    return {
      "checks":checks,
      "underlying_geometry":"theta0=N dt; theta1=L(dx+b dt); plane GR, no sphere +2NL",
      "actual_sector_normalization":"GE06 raw grav+aest; NL0C raw -C*volume*J; GE05 mapped factor 2 is separate Euler normalization; Lambda -6rho_lambda*volume",
      "off_shell_total_action_variation":"delta L_total=partial_x(xi L_total) for arbitrary xi(t,x); bath node sum/integral commutes with delta",
      "physical_one_sided_nonanalytic_rule":"J(X) proportional Abs(X)^3 is C2 at X=0; D(Abs(g)*g)[h]=2Abs(g)h",
      "action_level_full_spatial_ward_derived":True,
      "actual_six_piece_H4_source_coefficients_instantiated":False,
      "full_mixed_H4_source_parent_identity_derived":False,
    }

def main():
    p=argparse.ArgumentParser();p.add_argument("--json-out",required=True)
    args=p.parse_args()
    blobs=pinned();bindings=bind();result=exact_density()
    ok=bool(all(v["exact"] for v in blobs.values())
            and all(bindings.values()) and all(result["checks"].values()))
    out={
      "classification":("GE19_H4F2C_COMPLETE_REDUCED_ACTION_COVARIANCE_DERIVED_SIX_SOURCE_OPEN"
                        if ok else "GE19_H4F2C_REDUCED_ACTION_COVARIANCE_UNRESOLVED"),
      "preregistration":"GE19_H4F2_PREDATA_COMPLETE_MIXED_H4_WARD_SOURCE_PARENT_DICTIONARY",
      "frozen_blobs":blobs,"actual_action_bindings":bindings,
      "all_sector_reduced_action_covariance":result,
      "all_restricted_gates_pass":ok,
      "full_six_piece_H4_source_parent_dictionary_derived":False,
      "corrected_parent_common_time_source_evaluated":False,
      "H4_Z21_solve_performed":False,"Z21_certified":False,
      "lensing_licensed":False,
      "next_route":"INSTANTIATE_ALL_SIX_ACTION_DERIVED_MIXED_H4_SOURCE_ROWS_AND_PARENT_TERMS",
    }
    dest=Path(args.json_out);dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps(out,indent=2,sort_keys=True))
    if not ok:raise SystemExit(3)
if __name__=="__main__":main()
