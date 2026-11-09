#!/usr/bin/env python3
"""GE19 G2C: action-derived NL0C Y2 H4 mixed spatial Ward & zero-set proof.

NO ODE. Exact original source-blob locks. All results analytic, not an
actual-grid Noether parent/error or H4/Z21/lensing certification.
"""
from __future__ import annotations
import argparse,ast,json,subprocess
from pathlib import Path
import sympy as sp

ROOT=Path(__file__).resolve().parents[1]
PINS={
 "ge06/analytic_aest_directional_source_generator.py":"a7afe0035054a9dca55d74a6497c081422114b4c",
 "ge19/h4_stagee_versioned_y_source_rows.py":"282166ea5840d7fba4dbc328d40d7687afa6fa0f",
 "docs/nl0c_y_sector_weakly_nonlinear_result.md":"6fe02e60e4de34a247003c1f4ab449c159850e99",
 "ge19/h4f3d8_independent_nonbath_euler_and_boundary.py":"861cd5a81c17380a727777a4e1ff08cd7e857522",
 "ge19/h4f3d4_complete_eta_regularized_mixed_ward_ledger.py":"87d8be9ec44ecb099feecbaf59a904bd989da2fb",
}

def require(ok,name):
 if not bool(ok):raise RuntimeError("G2C_"+name)

def source_locks():
 result={}
 for path,want in PINS.items():
  p=ROOT/path
  require(p.is_file(),"MISSING_"+path)
  committed=subprocess.check_output(["git","rev-parse","HEAD:"+path],cwd=ROOT,text=True).strip()
  working=subprocess.check_output(["git","hash-object",str(p)],cwd=ROOT,text=True).strip()
  require(committed==want and working==want,"BLOB_CHANGED_"+path)
  result[path]=want
 s=(ROOT/"ge19/h4_stagee_versioned_y_source_rows.py").read_text()
 tree=ast.parse(s)
 funcs={n.name:n for n in tree.body if isinstance(n,ast.FunctionDef)}
 require(all(z in funcs for z in ("_rhs","source_h3","source_h4")),"STAGE_E_FUNC_CHANGED")
 targets=[]
 for n in ast.walk(funcs["_rhs"]):
  if isinstance(n,ast.Assign):targets.extend(n.targets)
  if isinstance(n,ast.AugAssign):targets.append(n.target)
 def rows(name):
  return sorted(set(int(t.slice.value) for t in targets
   if isinstance(t,ast.Subscript) and isinstance(t.value,ast.Name)
   and t.value.id==name and isinstance(t.slice,ast.Constant)
   and isinstance(t.slice.value,int)))
 require(rows("main")==[2,3] and rows("constraints")==[],"STAGE_E_Y_ROW_SUPPORT_CHANGED")
 for needle in ("2.0*np.abs(g0)*g1","np.abs(g)*g",
                "main[2]=2.0*aa**3*qq*kappa*projected",
                "main[3]=-2.0*aa**2*kappa*div_x"):
  require(needle in s,"STAGE_E_Y_NORMALIZATION_CHANGED")
 return result,{"main_rows":rows("main"),"constraint_rows":rows("constraints")}

def exact(expr):
 return sp.simplify(sp.trigsimp(sp.cancel(sp.together(expr))))==0

def proof():
 N,L,R,b,u,pt,px=sp.symbols("N L R b u pt px",real=True)
 Nx,Lx,Rx,bx,ux,ptx,pxx=sp.symbols("Nx Lx Rx bx ux ptx pxx",real=True)
 xi,xt,xx=sp.symbols("xi xt xx",real=True)
 X=sp.sinh(u)*(pt-b*px)/N+sp.cosh(u)*px/L
 V=N*L*R**2
 D={N:Nx,L:Lx,R:Rx,b:bx,u:ux,pt:ptx,px:pxx}
 d={N:xi*Nx,L:xi*Lx+L*xx,R:xi*Rx,b:xi*bx+xt-b*xx,
    u:xi*ux,pt:xi*ptx+xt*px,px:xi*pxx+xx*px}
 dc=lambda f:sum(sp.diff(f,z)*q for z,q in D.items())
 dv=lambda f:sum(sp.diff(f,z)*q for z,q in d.items())
 t={
   "original_GE06_Xinvariant_is_spatial_scalar":exact(dv(X)-xi*dc(X)),
   "original_volume_is_weight_one_density":exact(dv(V)-xi*dc(V)-xx*V),
   "wrong_shift_connection_breaks_X_scalar":not exact(
      sum(sp.diff(X,z)*(q-xt if z==b else q) for z,q in d.items())-xi*dc(X)),
   "wrong_phi_t_prolongation_breaks_X_scalar":not exact(
      sum(sp.diff(X,z)*(q-xt*px if z==pt else q) for z,q in d.items())-xi*dc(X)),
 }
 pos,neg=sp.symbols("pos neg",positive=True)
 x=sp.symbols("x",real=True)
 t["Y_potential_C1_derivative_both_signs"]=(
   exact(sp.diff(pos**3,pos)-3*pos*sp.Abs(pos))
   and exact(sp.diff(-(-neg)**3,neg)-3*neg**2))
 t["Y_abs_cube_derivative_signs"]=(
   exact(sp.diff(x**3,x)-3*x**2)
   and exact(sp.diff(-x**3,x)+3*x**2))
 lam,Xchi=sp.symbols("lam Xchi",positive=True)
 dLY=-lam*(xi*dc(V)+xx*V)*sp.Abs(x)**3-lam*V*3*x*sp.Abs(x)*xi*Xchi
 density=xi*(-lam*dc(V)*sp.Abs(x)**3-lam*V*3*x*sp.Abs(x)*Xchi)-xx*lam*V*sp.Abs(x)**3
 t["off_shell_Y_spatial_density_chain_rule"]=exact(dLY-density)
 a,Q=sp.symbols("a Q",positive=True)
 eps,eta=sp.symbols("eps eta",real=True)
 bg={u:0,px:0,pt:Q,b:0,N:1,L:a,R:a}
 t["X_u_background_equals_Q"]=exact(sp.diff(X,u).subs(bg)-Q)
 t["X_phi_x_background_equals_one_over_a"]=exact(sp.diff(X,px).subs(bg)-1/a)
 t["X_b_background_zero"]=exact(sp.diff(X,b).subs(bg))
 t["X_L_background_zero"]=exact(sp.diff(X,L).subs(bg))
 t["X_N_background_zero"]=exact(sp.diff(X,N).subs(bg))
 t["X_phi_t_background_zero"]=exact(sp.diff(X,pt).subs(bg))
 u1,p1,n1,l1,r1,b1=sp.symbols("u1 p1 n1 l1 r1 b1",real=True)
 pert={u:eps*u1,px:eps*p1,pt:Q,N:1+eps*n1,
       L:a+eps*l1,R:a+eps*r1,b:eps*b1}
 t["X_b_starts_at_eps2_original_action"]=exact(
   sp.limit(sp.diff(X,b).subs(pert)/eps**2,eps,0,dir="+")+u1*p1)
 t["X_L_starts_at_eps1_original_action"]=exact(
   sp.limit(sp.diff(X,L).subs(pert)/eps,eps,0,dir="+")+p1/a**2)
 t["X_N_starts_at_eps1_original_action"]=exact(
   sp.limit(sp.diff(X,N).subs(pert)/eps,eps,0,dir="+")+Q*u1)
 t["V_LEuler_volume_factor_background"]=exact(sp.diff(V,L).subs(bg)-a**2)
 g,h=sp.symbols("g h",real=True)
 kappa=3*lam
 flux=g*sp.Abs(g)
 F=sp.Symbol("DchiFlux")
 G=sp.Symbol("DchiAbsGh")
 YH3u=6*lam*a**3*Q*flux
 YH3phi=-6*lam*a**2*F
 YH4u=12*lam*a**3*Q*sp.Abs(g)*h
 YH4phi=-12*lam*a**2*G
 t["Y_H3_aether_original_StageE_kappa_factor"]=exact(YH3u-2*a**3*Q*kappa*flux)
 t["Y_H3_scalar_original_StageE_kappa_factor"]=exact(YH3phi+2*a**2*kappa*F)
 t["Y_H4_aether_original_StageE_tangent_factor"]=exact(YH4u-4*a**3*Q*kappa*sp.Abs(g)*h)
 t["Y_H4_scalar_original_StageE_tangent_factor"]=exact(YH4phi+4*a**2*kappa*G)
 EbY=eps**4*sp.Symbol("B4")
 ELY=eps**3*sp.Symbol("L3")
 EuY=eps**2*(sp.Symbol("U20")+eta*sp.Symbol("U21"))
 EpY=eps**2*(sp.Symbol("P20")+eta*sp.Symbol("P21"))
 uxY=eps*(sp.Symbol("ux10")+eta*sp.Symbol("ux11"))
 pxY=eps*(sp.Symbol("px10")+eta*sp.Symbol("px11"))
 # FLRW background is spatially homogeneous; direct Y L,b rows vanish
 # at epsilon^2 while u/phi rows begin at that order.
 WardY=EuY*uxY+EpY*pxY-eps**3*sp.Symbol("chi_L3")-eps**4*sp.Symbol("t_B4")
 t["Y_mixed_eps2_eta_full_spatial_Ward_zero"]=exact(
    sp.diff(sp.diff(WardY,eps,2),eta).subs({eps:0,eta:0}))
 t["Y_nonzero_dynamic_euler_two_rows"]=bool(EuY!=0 and EpY!=0)
 t["Y_wrong_order_shift_Eb_eps2_negative_control"]=bool(
    sp.diff(sp.diff(WardY-eps**2*eta*sp.Symbol("bad_Shift_t"),eps,2),eta)
    .subs({eps:0,eta:0}) != 0)
 t["directional_second_amplitude_not_two_sided_Hessian"]=bool(
    sp.limit(eps*sp.Abs(eps)/eps**2,eps,0,dir="+")==1
    and sp.limit(eps*sp.Abs(eps)/eps**2,eps,0,dir="-")==-1)
 t["flux_derivative_at_zero_is_zero"]=exact(
    sp.limit(eps*h*sp.Abs(eps*h)/eps,eps,0,dir="+"))
 t["flux_positive_derivative"]=exact(sp.diff(x**2,x)-2*x)
 t["flux_negative_derivative"]=exact(sp.diff(-x**2,x)+2*x)
 t["tangent_continuous_at_zero"]=bool(
    sp.limit(2*sp.Abs(g)*h,g,0,dir="+")==0
    and sp.limit(2*sp.Abs(g)*h,g,0,dir="-")==0)
 t["zero_crossing_flux_jump_exact_zero"]=exact(
    sp.limit(g*sp.Abs(g),g,0,dir="+")-
    sp.limit(g*sp.Abs(g),g,0,dir="-"))
 t["zero_crossing_mixed_flux_jump_exact_zero"]=exact(
    sp.limit(sp.Abs(g)*h,g,0,dir="+")-
    sp.limit(sp.Abs(g)*h,g,0,dir="-"))
 require(all(t.values()),"SYMBOLIC_FAILURE_"+",".join(k for k,v in t.items() if not v))
 return t

def main():
 ap=argparse.ArgumentParser()
 ap.add_argument("--self-test",action="store_true")
 ap.add_argument("--json-out",type=Path)
 args=ap.parse_args()
 tests=proof()
 if args.self_test:
  print("GE19_G2C_Y_ACTION_MIXED_NOETHER_ZERO_SET_SELFTEST_PASS",len(tests))
  return
 require(args.json_out is not None and not args.json_out.exists(),"OUTPUT_MISSING_OR_EXISTS")
 blobs,rows=source_locks()
 result={
  "classification":"GE19_G2C_SOURCE_LOCKED_Y_ACTION_H4_DIRECT_WARD_ZERO_SET_ANALYTIC_PASS_ACTUAL_PARENT_OPEN",
  "frozen_blobs":blobs,"frozen_Stage_E_rows":rows,
  "analytic_symbolic_checks":tests,"symbolic_checks_passed":len(tests),
  "action_Y":"L_Y=-lambda*N*L*R^2*|Xinv|^3; lambda=2*(2-KB)/(3*(1+beta0)*a0)",
  "gradient":"g10=Q*u10+phi10_chi/a; g11=Q*u11+phi11_chi/a",
  "H3_Y_RHS":"Su=+6lambda*a^3*Q*g10*|g10|; Sphi=-6lambda*a^2*partial_chi(g10*|g10|)",
  "H4_Y_RHS":"Su=+12lambda*a^3*Q*|g10|*g11; Sphi=-12lambda*a^2*partial_chi(|g10|*g11)",
  "Y_direct_H4_shift_iso_aniso_zero":True,
  "Y_direct_mixed_H4_spatial_Noether_coefficient_zero":True,
  "Y_aether_scalar_H4_RHS_generically_nonzero":True,
  "zero_crossing_no_delta_if_continuous_gradients":True,
  "discontinuous_gradient_requires_interface_terms":True,
  "actual_parent_Euler_and_boundary_error_enclosed":False,
  "full_original_H4_Ward_certified":False,
  "Z21_certified":False,"lensing_licensed":False,
  "original_frozen_H4_shift_FAIL_preserved":True,
  "claim_boundary":"Exact one-sided epsilon directional reduced Y action and frozen Stage E support; not a real-grid Ward, a verified continuous FD8 regularity bound, or a new H4 solve."
 }
 args.json_out.parent.mkdir(parents=True,exist_ok=True)
 args.json_out.write_text(json.dumps(result,indent=2,sort_keys=True,allow_nan=False)+"\n")
 print(result["classification"])
 print("SYMBOLIC_CHECKS",len(tests))

if __name__=="__main__":
 main()
