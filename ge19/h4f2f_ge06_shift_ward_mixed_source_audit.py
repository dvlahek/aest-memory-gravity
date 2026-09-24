#!/usr/bin/env python3
"""GE19 H4F2f: exact frozen GE06 coframe Ward + mixed shift source subset.

No GE19 H4/Z21 integration or corrected-parent evaluation is performed.
Frozen generator module is loaded only through Repair07's isolated loader,
so historical results/ are not overwritten by generator import side effects.
"""
from __future__ import annotations
import argparse
import json
import subprocess
from pathlib import Path

import numpy as np
import sympy as sp
from ge19 import repair07_window_retarded_reduced_h3_z20_particular as r7

ROOT=Path(__file__).resolve().parents[1]
BLOBS={
 "ge19/h4f2f_predata_ge06_shift_ward_mixed_source.json":
   "551294c5763b086919c9f27076a922c29ca953e5",
 "ge19/h4f2_predata_complete_mixed_h4_ward_parent_dictionary.json":
   "8097a4770ae8aed74cb4dd0721c1c9bd6907533c",
 "ge06/analytic_aest_directional_source_generator.py":
   "a7afe0035054a9dca55d74a6497c081422114b4c",
 "ge19/repair07_window_retarded_reduced_h3_z20_particular.py":
   "e34d28a2062c748f48bc82fa928844b02631de25",
 "ge19/repair37_cancellation_safe_fd8_h4_z21_reclosure.py":
   "45d203a092f9ac71cc612b15df5f0c0c630f5898",
 "docs/ge19_h4f2b_signed_mixed_ward_template_valid_freeze.md":
   "98693317485149898830eebd0f335db12024e6dc",
 "docs/ge19_h4f2e_shift_action_subidentity_valid_freeze.md":
   "79c81ebffeca490b9dad74d812005086daa04c32",
}
def exact_blobs():
    out={}
    for p,want in BLOBS.items():
        got=subprocess.check_output(
            ["git","rev-parse","HEAD:"+p],cwd=ROOT,text=True
        ).strip()
        out[p]={"expected":want,"observed":got,"exact":got==want}
    return out

def iszero(expr):
    return bool(sp.simplify(sp.trigsimp(sp.cancel(expr)))==0)

def primitive_ward():
    names=("N L R b u Lt Lx Rt Rx bx ut ux pt px Nx "
           "Nxx Lxx Rxx bxx Ltx Rtx utx uxx ptx pxx "
           "xi xix xit xixx xitx")
    (N,L,R,b,u,Lt,Lx,Rt,Rx,bx,ut,ux,pt,px,Nx,
     Nxx,Lxx,Rxx,bxx,Ltx,Rtx,utx,uxx,ptx,pxx,
     xi,xix,xit,xixx,xitx)=sp.symbols(names,real=True)
    spatial={
        N:Nx,L:Lx,R:Rx,b:bx,u:ux,
        Lt:Ltx,Lx:Lxx,Rt:Rtx,Rx:Rxx,
        bx:bxx,ut:utx,ux:uxx,pt:ptx,px:pxx,Nx:Nxx
    }
    variation={
        N:xi*Nx,
        L:xi*Lx+L*xix,
        R:xi*Rx,
        b:xit+xi*bx-b*xix,
        u:xi*ux,
        Lt:xi*Ltx+xit*Lx+Lt*xix+L*xitx,
        Lx:xi*Lxx+2*xix*Lx+L*xixx,
        Rt:xi*Rtx+xit*Rx,
        Rx:xi*Rxx+xix*Rx,
        bx:xitx+xi*bxx-b*xixx,
        ut:xi*utx+xit*ux,
        ux:xi*uxx+xix*ux,
        pt:xi*ptx+xit*px,
        px:xi*pxx+xix*px,
        Nx:xi*Nxx+xix*Nx
    }
    def linear(expr,mapping):
        return sum((sp.diff(expr,k)*v for k,v in mapping.items()),sp.S.Zero)
    def scalar(expr):
        return iszero(linear(expr,variation)-xi*linear(expr,spatial))
    def density(expr):
        return iszero(linear(expr,variation)
                      -xi*linear(expr,spatial)-xix*expr)
    kL=(Lt-b*Lx-L*bx)/(N*L)
    kR=(Rt-b*Rx)/(N*R)
    sigma=(pt-b*px)/N
    ch,sh=sp.cosh(u),sp.sinh(u)
    Qinv=ch*sigma+sh*px/L
    Xinv=sh*sigma+ch*px/L
    E=ch*((ut-b*ux)/N+Nx/(N*L))+sh*(kL+ux/L)
    volume=N*L*R**2
    gplane=2*N*Rx**2/L+4*Nx*R*Rx/L
    checks={
      "kL_from_full_L_and_shift_jets_is_scalar":scalar(kL),
      "kR_from_full_R_and_shift_jets_is_scalar":scalar(kR),
      "sigma_from_shift_phi_jets_is_scalar":scalar(sigma),
      "Qinv_from_frozen_aether_and_phi_is_scalar":scalar(Qinv),
      "Xinv_from_frozen_aether_and_phi_is_scalar":scalar(Xinv),
      "aether_divergence_E_from_full_jets_is_scalar":scalar(E),
      "lapse_spatial_acceleration_Nx_over_NL_is_scalar":scalar(Nx/(N*L)),
      "Rx_over_L_is_scalar":scalar(Rx/L),
      "GE06_NLR2_is_spatial_density":density(volume),
      "GE06_plane_curvature_gradient_is_density":density(gplane),
    }
    return checks

def actual_ge06_and_mixed_shift():
    path=ROOT/"ge06/analytic_aest_directional_source_generator.py"
    generator=r7.load_frozen_generator(path,"ge06_h4f2f_isolated")
    src=path.read_text()
    code_bind={
      "exact_frozen_GE06_coframe":
        "theta0=N dt, theta1=L(dx+b dt)" in src,
      "exact_frozen_GR_plane_no_sphere":
        "grav=N*L*R**2*(-4*kL*kR-2*kR**2) + 2*N*Rx**2/L + 4*Nx*R*Rx/L" in src,
      "exact_frozen_analytic_AeST_action":
        "aest=N*L*R**2*(KB*E**2 + 2*C*E*Xinv - C*Xinv**2 + 2*Kfun)" in src,
      "original_exact_GEOS_b_f_and_b_x_partials":
        iszero(generator.partial_map["b_f"]-sp.diff(generator.lag,generator.b))
        and iszero(generator.partial_map["b_x"]-sp.diff(generator.lag,generator.bx)),
    }
    h4=(ROOT/"ge19/repair37_cancellation_safe_fd8_h4_z21_reclosure.py").read_text()
    code_bind["Repair37_shift_b_f_minus_dx_b_x_source_assembly"]=(
        '"b":pd["b_f"]-dx(pd["b_x"])' in
        (ROOT/"ge19/repair07_window_retarded_reduced_h3_z20_particular.py").read_text()
    )
    code_bind["Repair37_GE06_mixed_minus_two_unnormalized_source"]=(
        "qga_main=-2.0*fft_low(ga_m); qga_con=-2.0*fft_low(ga_c)" in h4)
    code_bind["Repair37_fft_over_nx"]=(
        "hh=np.fft.fft(aa,axis=-1)/aa.shape[-1]" in h4)
    dir0=tuple(generator.direction_args[3:18])
    assert len(dir0)==15
    etas=sp.symbols("ge06_h4f2f_eta0:15",real=True)
    symbolic={}
    numeric={}
    for key in ("b_f","b_x"):
        expr=generator.coeff2[key]
        physical_mixed=sp.Rational(1,2)*sum(
            (sp.diff(expr,d)*e for d,e in zip(dir0,etas)),sp.S.Zero
        )
        plus=expr.xreplace({d:d+e for d,e in zip(dir0,etas)})
        minus=expr.xreplace({d:d-e for d,e in zip(dir0,etas)})
        Qbil=sp.cancel(sp.expand((plus-minus)/4))
        reversed_expr=expr.xreplace(dict(zip(dir0,etas)))
        reverse=sp.Rational(1,2)*sum(
            (sp.diff(reversed_expr,e)*d for d,e in zip(dir0,etas)),
            sp.S.Zero
        )
        symbolic[key]={
          "original_Q_cross_half_gradient_matches_polarization":
            iszero(physical_mixed-Qbil),
          "mixed_direction_symmetry":iszero(physical_mixed-reverse),
          "original_minus_two_source_equals_negative_physical_mixed":
            iszero(-2*Qbil+physical_mixed),
          "directional_quadratic_zero_origin":
            iszero(expr.xreplace({d:0 for d in dir0})),
        }
        # Frozen f_c2 is already generated from the full action, not
        # an independently guessed source formula. Sample nonzero
        # directions through the actual frozen generator.
        args0=list(generator.direction_args)
        vals=[0.61,0.025,0.24]
        vals.extend([0.01*np.sin(0.37*(j+1)) for j in range(15)])
        vals.extend([0.1,1.9,0.4,0.2,0.7])
        if len(vals)!=len(args0):
            raise RuntimeError("GE06 frozen direction_args layout changed")
        ev=[0.012*np.cos(0.21*(j+1)) for j in range(15)]
        head=vals[:3];tail=vals[18:]
        q0=np.asarray(generator.f_c2[key](*vals),float)
        qp=np.asarray(generator.f_c2[key](
            *(head+[d+e for d,e in zip(vals[3:18],ev)]+tail)),float)
        qm=np.asarray(generator.f_c2[key](
            *(head+[d-e for d,e in zip(vals[3:18],ev)]+tail)),float)
        pol=(qp-qm)/4
        fun=sp.lambdify((*args0,*etas),physical_mixed,"numpy",cse=True)
        direct=np.asarray(fun(*vals,*ev),float)
        denom=max(float(np.linalg.norm(direct)),
                  float(np.linalg.norm(pol)),1e-300)
        diff=float(np.linalg.norm(direct-pol)/denom)
        numeric[key]={
          "actual_frozen_c2_minus_plus_Qbil_relative_L2":diff,
          "actual_frozen_c2_nonzero":bool(float(np.linalg.norm(q0))>0),
          "numeric_finite":bool(np.isfinite(q0).all()
                                and np.isfinite(direct).all()
                                and np.isfinite(pol).all()),
          "source_only_relative_L2_le_1e_minus_9":diff<=1e-9,
        }
    # Explain exact non-spherical action closure: kL,kR,E,Qinv,Xinv
    # and gradient ratios are proven scalars above, while NLR^2
    # and both plane curvature terms are proven densities.
    return code_bind,symbolic,numeric

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--json-out",required=True)
    args=ap.parse_args()
    blobs=exact_blobs()
    primitive=primitive_ward()
    bindings,symbolic,numeric=actual_ge06_and_mixed_shift()
    subset=bool(all(d["exact"] for d in blobs.values())
                and all(primitive.values()) and all(bindings.values())
                and all(all(g.values()) for g in symbolic.values())
                and all(all(g.values()) for g in numeric.values()))
    result={
      "classification":(
        "GE19_H4F2F_GE06_SPATIAL_WARD_SHIFT_SOURCE_SUBSET_PASS"
        if subset else "GE19_H4F2F_GE06_ACTION_SHIFT_SOURCE_SUBSET_FAIL"
      ),
      "frozen_blobs":blobs,
      "full_unreduced_coframe_jet_spatial_ward":primitive,
      "frozen_action_and_source_implementation_bindings":bindings,
      "exact_independent_shift_local_mixed_action_partials":symbolic,
      "source_only_frozen_generator_numeric":numeric,
      "GE06_full_offshell_spatial_action_covariance_from_primitives":
        bool(all(primitive.values()) and
             all(bindings[k] for k in (
               "exact_frozen_GE06_coframe",
               "exact_frozen_GR_plane_no_sphere",
               "exact_frozen_analytic_AeST_action"
             ))),
      "all_subset_gates_pass":subset,
      "full_six_piece_H4_source_parent_Noether_derived":False,
      "corrected_H3F_H3G_parent_time_evaluated":False,
      "H4_Z21_solve_performed":False,
      "Z21_certified":False,"lensing_licensed":False,
      "next_route":"COMPLETE_ALL_ROW_SOURCE_AND_SIGNED_PARENT_RESIDUAL_H4_WARD",
      "claim_boundary":"GE06 action/shift subset only; no complete all-sector mixed H4 source-parent Noether certification, numerical corrected-parent H4 source evaluation or H4/Z21 result."
    }
    dest=Path(args.json_out)
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(result,indent=2,sort_keys=True,allow_nan=False)+"\n")
    print(json.dumps(result,indent=2,sort_keys=True,allow_nan=False))
    if not subset:raise SystemExit(3)

if __name__=="__main__":
    main()
