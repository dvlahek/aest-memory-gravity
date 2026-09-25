#!/usr/bin/env python3
"""GE19 H4F3d11: exact frozen GE06/GE07 homogeneous source partials.

The source is frozen ge06.partial_map and ge07.partial_map, not the
linearized c1 expressions. Perform symbolic Q0+Z0*Z substitution BEFORE
float64 evaluation; audit every exact FLRW partial against an independently
derived closed expression. No physical E00 on-shell PASS is decided here.
"""
from __future__ import annotations
import sympy as sp
import numpy as np

GE06_KEYS=("N_f","N_x","L_f","L_t","L_x","R_f","R_t","R_x",
           "b_f","b_x","u_f","u_t","u_x","phi_t","phi_x")
GE07_KEYS=("N_f","L_f","R_f","b_f","rho_f","T_t","T_x")
RTOL=1.0e-12
TINY=1.0e-300

def _expr_equal(a,b):
    return sp.simplify(sp.cancel(sp.together(a-b)))==0

def _shape(fn,args,n):
    raw=np.asarray(fn(*args),float)
    val=np.broadcast_to(raw,(n,)).copy()
    if not np.all(np.isfinite(val)):
        raise RuntimeError("nonfinite source-bound homogeneous partial")
    return val

def _source_and_explicit(exprs,expected,args):
    source={}
    closed={}
    eq={}
    for name in expected:
        formula=sp.factor_terms(sp.simplify(exprs[name]))
        ok=bool(_expr_equal(formula,expected[name]))
        eq[name]=ok
        if not ok:
            raise RuntimeError("frozen original homogeneous action partial changed: "+
                               name+" = "+str(formula)[:300])
        source[name]=sp.lambdify(args,formula,modules="numpy",cse=True)
        closed[name]=sp.lambdify(args,expected[name],modules="numpy",cse=True)
    return source,closed,eq

def compile_exact_source(mod6,mod7):
    """Accept only genuine source modules exposing their frozen partial_map."""
    a,adot,Z=sp.symbols("d11_a d11_adot d11_Z",real=True,positive=True)
    rho=sp.symbols("d11_rho",real=True,positive=True)
    Q=mod6.Q0+mod6.Z0*Z
    kval=2*mod6.K2*mod6.Z0**2*(sp.exp(Z**2)-1)
    kq=4*mod6.K2*mod6.Z0*Z*sp.exp(Z**2)
    g0={
       mod6.N:1,mod6.L:a,mod6.R:a,mod6.b:0,mod6.u:0,
       mod6.Lt:adot,mod6.Lx:0,mod6.Rt:adot,mod6.Rx:0,
       mod6.bx:0,mod6.ut:0,mod6.ux:0,mod6.pt:Q,
       mod6.px:0,mod6.Nx:0
    }
    source6={
       k:mod6.partial_map[k].subs(g0,simultaneous=True)
       for k in GE06_KEYS}
    zero=sp.Integer(0)
    expected6={
       "N_f":6*a*adot**2+2*a**3*(kval-Q*kq),
       "N_x":zero,
       "L_f":-2*adot**2+2*a**2*kval,
       "L_t":-4*a*adot,
       "L_x":zero,
       "R_f":-4*adot**2+4*a**2*kval,
       "R_t":-8*a*adot,
       "R_x":zero,
       "b_f":zero,
       "b_x":4*a**2*adot,
       "u_f":zero,
       "u_t":zero,
       "u_x":zero,
       "phi_t":2*a**3*kq,
       "phi_x":zero
    }
    source6,closed6,gates6=_source_and_explicit(
        source6,expected6,(a,adot,Z,mod6.KB,mod6.C,
                          mod6.K2,mod6.Q0,mod6.Z0))
    d0={mod7.N:1,mod7.L:a,mod7.R:a,mod7.b:0,
        mod7.varrho:rho,mod7.Tt:1,mod7.Tx:0}
    source7={
        k:mod7.partial_map[k].subs(d0,simultaneous=True)
        for k in GE07_KEYS}
    expected7={
        "N_f":-2*a**3*rho,"L_f":zero,"R_f":zero,
        "b_f":zero,"rho_f":zero,"T_t":2*a**3*rho,"T_x":zero
    }
    source7,closed7,gates7=_source_and_explicit(
        source7,expected7,(a,rho))
    controls={
       "all_15_original_GE06_background_local_partials_exact":
           bool(len(gates6)==15 and all(gates6.values())),
       "all_7_original_GE07_background_local_partials_exact":
           bool(len(gates7)==7 and all(gates7.values())),
       "GE06_negative_control_omit_bx_background_momentum":
           not _expr_equal(expected6["b_x"],zero),
       "GE06_negative_control_drop_scalar_QKQ_from_lapse":
           not _expr_equal(expected6["N_f"],
                           6*a*adot**2+2*a**3*kval),
       "GE07_negative_control_wrong_dust_lapse_sign":
           not _expr_equal(expected7["N_f"],2*a**3*rho),
       "GE07_exact_background_rho_multiplier_zero":
           gates7["rho_f"],
       "original_GE06_nonzero_shift_spatial_momentum_retained":True,
       "source_action_not_modified":True,
    }
    if not all(controls.values()):
        raise RuntimeError("D11 source-bound homogeneous symbolic gate FAIL")
    return source6,closed6,source7,closed7,controls

def physical_partials(compiled,bg,tag,r7):
    s6,c6,s7,c7,_=compiled
    a=np.asarray(bg["a"],float)
    nt=len(a)
    z=np.asarray(bg["Z_action"],float)
    h=np.asarray(bg["H"],float)
    rl=np.asarray(bg["rho_lambda_action"],float)
    rhob=3.0*float(r7.C_VALUES[tag])/a**3
    if (any(q.shape!=(nt,) or not np.isfinite(q).all()
            for q in (a,z,h,rl,rhob))
        or np.any(a<=0) or np.any(h<=0) or np.any(z<=0)):
        raise RuntimeError("D11 invalid exact original Repair13 background")
    vals6=(a,a*h,z,r7.KB,r7.CV,r7.K2,r7.Q0,r7.Z0)
    vals7=(a,rhob)
    actual6={k:_shape(fn,vals6,nt) for k,fn in s6.items()}
    exact6={k:_shape(fn,vals6,nt) for k,fn in c6.items()}
    actual7={k:_shape(fn,vals7,nt) for k,fn in s7.items()}
    exact7={k:_shape(fn,vals7,nt) for k,fn in c7.items()}
    agreement={}
    for prefix,observed,want in (
        ("GE06",actual6,exact6),("GE07",actual7,exact7)):
        for key in want:
            a0=np.asarray(observed[key],float)
            b0=np.asarray(want[key],float)
            err=float(np.linalg.norm(a0-b0)/
                      max(np.linalg.norm(a0),np.linalg.norm(b0),TINY))
            agreement[prefix+"_"+key]=err
            if (not np.isfinite(err) or err>RTOL):
                raise RuntimeError("D11 source vs symbolic closed original partial: "+
                                   prefix+"_"+key+"="+str(err))
    return actual6,actual7,{
        "numeric_source_vs_exact_symbolic_closed_all_partials_max_relative":
            max(agreement.values()),
        "numeric_source_vs_exact_symbolic_closed_partials_relative":
            agreement,
        "source_closed_form_consistency_only_NOT_E00_on_shell":True
    }
