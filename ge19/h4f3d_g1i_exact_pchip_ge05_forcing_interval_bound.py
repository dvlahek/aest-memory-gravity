#!/usr/bin/env python3
"""GE19 G1I: exact-input rational Bernstein bounds for frozen Repair32B GE05 forcing.

This IS a mathematical all-time-interval enclosure of the *declared
piecewise-cubic PCHIP polynomial* s_h(x), once its real/imaginary binary64
coefficient arrays have been computed. Source L_inf, derivative L_inf and
time-integrated L1 upper bounds are proved without temporal sampling.

This is NOT a validated enclosure of the true GE05 bath driving source,
nor a bound on original-action canonical M(x), F(x), numerical Z11 state,
algebraic rows, original H4 Ward or Z21. It does not run a Z11 solver.
Do not silently promote a PCHIP source-polynomial bound into G1 PASS.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import subprocess
from fractions import Fraction as Q
from pathlib import Path

import numpy as np
import scipy
from scipy.interpolate import PchipInterpolator

ROOT=Path(__file__).resolve().parents[1]
SCALE=10**30
TINY=Q(0)
MODES=(3,5,8,10,15,20)
C_TAGS=("C_min","C_star","C_max")
GRIDS={"primary":128,"control":64}
PINS={
  "ge19/repair32b_factor2_corrected_reduced_h2_z11_reconstruction.py":
    "6ece578e8a30f48faaded8808687a9bd5c114608",
  "ge19/repair07_window_retarded_reduced_h3_z20_particular.py":
    "e34d28a2062c748f48bc82fa928844b02631de25",
  "ge19/h4f3d_g1g_independent_action_z11_ivp.py":
    "3575a11e5d4bbddbce5bc8a052129c6c0c553808",
}
FROZEN_SHA="5d4a0a72c08d09d096a8de0b428b3c8443fc33e8ad442ed6d997d6bf2bc6e327"
FROZEN_NAME="ge19_repair32b_factor2_corrected_reduced_h2_z11_reconstruction.npz"

def need(test,msg):
    if not bool(test):raise RuntimeError("GE19_G1I_"+msg)

def sha256(p):
    h=hashlib.sha256()
    with Path(p).open("rb") as stream:
        for block in iter(lambda:stream.read(1<<20),b""):
            h.update(block)
    return h.hexdigest()

def source_pins():
    out={}
    for path,want in PINS.items():
        head=subprocess.check_output(["git","rev-parse","HEAD:"+path],
                                     cwd=ROOT,text=True).strip()
        work=subprocess.check_output(["git","hash-object",str(ROOT/path)],
                                     cwd=ROOT,text=True).strip()
        need(head==work==want,"SOURCE_CHANGED_"+path)
        out[path]=want
    script=(ROOT/"ge19/repair32b_factor2_corrected_reduced_h2_z11_reconstruction.py").read_text()
    need("RAW_RESIDUAL_DICTIONARY_SCALE=2.0" in script and
         "PchipInterpolator(x,arr.real,axis=-1,extrapolate=False)" in script and
         "PchipInterpolator(x,arr.imag,axis=-1,extrapolate=False)" in script,
         "FROZEN_SOURCE_PCHIP_PRESCRIPTION_CHANGED")
    return out

def scalar(z):
    v=float(z)
    need(math.isfinite(v),"NONFINITE_NUMERIC_INPUT")
    return Q.from_float(v)

def complexq(z):
    v=complex(z)
    return scalar(v.real),scalar(v.imag)

def add(a,b):
    return a[0]+b[0],a[1]+b[1]

def mul(v,a):
    return (v*a[0],v*a[1])

def ub_sqrt_fraction(q):
    """Smallest multiple of 1e-30 >= sqrt(q), exact rational comparisons."""
    need(q>=0,"NEGATIVE_MODULUS_SQUARE")
    if q==0:return Q(0)
    numer=q.numerator*SCALE*SCALE
    denom=q.denominator
    floor=math.isqrt(numer//denom)
    units=floor if floor*floor*denom>=numer else floor+1
    need(units*units*denom>=numer,"OUTWARD_SQRT_FAILED")
    return Q(units,SCALE)

def modulus_sq(v):
    return v[0]*v[0]+v[1]*v[1]

def vector_norm_upper(vec):
    return ub_sqrt_fraction(sum((modulus_sq(z) for z in vec),Q(0)))

def decimal_ceil(q,places=30):
    """Outward rounding UP to a human-readable decimal string."""
    need(q>=0,"NEGATIVE_CERT_BOUND")
    n=10**places
    units=(q.numerator*n+q.denominator-1)//q.denominator
    return str(units//n)+"."+str(units%n).zfill(places)

def bernstein(c,h):
    """Cubic in local coordinate t=x-x_j, coeff c=[t^3,t^2,t,1]."""
    c3,c2,c1,c0=(complexq(k) for k in c)
    a1=mul(h,c1);a2=mul(h*h,c2);a3=mul(h*h*h,c3)
    b0=c0
    b1=add(c0,mul(Q(1,3),a1))
    b2=add(add(c0,mul(Q(2,3),a1)),mul(Q(1,3),a2))
    b3=add(add(add(c0,a1),a2),a3)
    # derivative q'(x) quadratic in normalized u=(x-x_j)/h:
    d0=c1
    d1=add(c1,mul(h,c2))
    d2=add(add(c1,mul(2*h,c2)),mul(3*h*h,c3))
    return (b0,b1,b2,b3),(d0,d1,d2)

def evaluate_power(c,h,u):
    t=h*u
    z=complexq(0)
    for ck in (complexq(item) for item in c):
        z=add(mul(t,z),ck)
    return z

def evaluate_bernstein(b,u):
    v=Q(1)-u
    return add(add(add(mul(v*v*v,b[0]),mul(3*v*v*u,b[1])),
                   mul(3*v*u*u,b[2])),mul(u*u*u,b[3]))

def selftest():
    h=Q(7,13)
    coeffs=((complex(0.5,0.25),complex(-0.4,0.2),
             complex(0.1,-0.3),complex(1.2,-2.5)),
            (0j,0j,0j,0j))
    for c in coeffs:
        b,d=bernstein(c,h)
        for u in (Q(0),Q(1,7),Q(1,2),Q(9,11),Q(1)):
            need(evaluate_power(c,h,u)==evaluate_bernstein(b,u),
                 "POLYNOMIAL_BERNSTEIN_IDENTITY_FAIL")
            # derivative of power (wrt actual x)
            cc=tuple(complexq(x) for x in c)
            tt=h*u
            exact=add(add(mul(3*tt*tt,cc[0]),
                          mul(2*tt,cc[1])),cc[2])
            approximate=add(add(mul((Q(1)-u)**2,d[0]),
                          mul(2*u*(Q(1)-u),d[1])),mul(u*u,d[2]))
            need(exact==approximate,"DERIVATIVE_IDENTITY_FAIL")
        for vec in ((b[0],b[1]),(b[2],b[3]),(d[0],d[1])):
            norm_ub=vector_norm_upper(vec)
            need(norm_ub*norm_ub>=sum((modulus_sq(x) for x in vec),Q(0)),
                 "COMPLEX_NORM_BOUND_FAIL")
    return {"bernstein_power_and_derivative_exact_rational":True,
            "exact_integer_sqrt_outward_rounding":True,
            "zero_polynomial":True}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--results-dir",type=Path,default=ROOT/"results")
    ap.add_argument("--tag",choices=C_TAGS,default="C_star")
    ap.add_argument("--grid",choices=GRIDS.keys(),default="primary")
    ap.add_argument("--modes",default="20",
                    help="Comma-separated subset of original 3,5,8,10,15,20")
    ap.add_argument("--json-out",type=Path)
    ap.add_argument("--self-test",action="store_true")
    args=ap.parse_args()
    tested=selftest()
    if args.self_test:
        print("GE19_G1I_PCHIP_BERNSTEIN_SELFTEST_PASS",flush=True)
        return
    need(args.json_out is not None,"JSON_OUT_REQUIRED")
    need(not args.json_out.exists(),"REFUSE_OVERWRITE_REPORT")
    modes=tuple(int(s) for s in args.modes.split(","))
    need(len(set(modes))==len(modes) and
         len(modes)>0 and all(m in MODES for m in modes),
         "INVALID_ORIGINAL_MODE_SUBSET")
    pins=source_pins()
    parent=args.results_dir/FROZEN_NAME
    need(parent.is_file(),"MISSING_FROZEN_REPAIR32B_NPZ")
    got=sha256(parent)
    need(got==FROZEN_SHA,"FROZEN_REPAIR32B_NPZ_SHA_MISMATCH")
    nt=GRIDS[args.grid]
    modes_rows=[]
    with np.load(parent,allow_pickle=False) as z:
        x=np.asarray(z["x_"+args.grid],float)
        src=np.asarray(z[f"{args.tag}_M1_rhs_{args.grid}"],complex)
        need(x.shape==(nt,) and src.shape==(6,6,nt),
             "FROZEN_M1_SOURCE_SHAPE_CHANGED")
        need(np.isfinite(x).all() and np.all(np.diff(x)>0) and
             np.isfinite(src).all(),"NONFINITE_OR_NONMONOTONE_FROZEN_INPUT")
        need(np.array_equal(src[:,[0,1,4,5],:],np.zeros_like(src[:,[0,1,4,5],:])),
             "FROZEN_ORIGINAL_GE05_SOURCE_HAS_UNEXPECTED_ROWS")

        for m in modes:
            j=MODES.index(m)
            y=src[j]  # 6 original Euler main rows x Nt
            # EXACT ORIGINAL Repair32B source_interp implementation: separate
            # complex real/imag PCHIP, axis=-1, no extrapolation.
            re=PchipInterpolator(x,y.real,axis=-1,extrapolate=False)
            im=PchipInterpolator(x,y.imag,axis=-1,extrapolate=False)
            need(re.c.shape==im.c.shape==(4,nt-1,6),
                 "SCIPY_CUBIC_SOURCE_SHAPE_CHANGED")
            all_source_sup=Q(0)
            all_derivative_sup=Q(0)
            all_time_integral_upper=Q(0)
            max_per_row=[Q(0) for _ in range(6)]
            dominant={"interval":None,"Bernstein_control":None}
            per_interval=[]
            for interval in range(nt-1):
                # Endpoints are exact binary64 rational input values. The
                # physical coordinate domain is the exact interval between
                # the two represented binary64 x knot values, not the
                # rounded floating mesh delta returned by np.diff.
                h=scalar(x[interval+1])-scalar(x[interval])
                need(h>0,"DEGENERATE_TIME_INTERVAL")
                ctrls=[];dctrls=[]
                for row in range(6):
                    c=tuple(complex(re.c[p,interval,row],im.c[p,interval,row])
                            for p in range(4))
                    b,d=bernstein(c,h)
                    ctrls.append(b)
                    dctrls.append(d)
                    for control in b:
                        max_per_row[row]=max(max_per_row[row],
                                             vector_norm_upper((control,)))
                vectors=[tuple(ctrls[row][idx] for row in range(6))
                         for idx in range(4)]
                der_vectors=[tuple(dctrls[row][idx] for row in range(6))
                             for idx in range(3)]
                bound_controls=[vector_norm_upper(v) for v in vectors]
                dbounds=[vector_norm_upper(v) for v in der_vectors]
                source_upper=max(bound_controls)
                derivative_upper=max(dbounds)
                # ||sum_k beta_3,k(u) B_k||_2 <=
                # sum_k beta_3,k(u) ||B_k||_2 for u in [0,1].
                # Integral of each beta_3,k over u=0..1 is 1/4.
                integral_upper=h*sum(bound_controls,Q(0))/4
                if source_upper>all_source_sup:
                    all_source_sup=source_upper
                    dominant={"interval":interval,
                              "Bernstein_control":bound_controls.index(source_upper)}
                all_derivative_sup=max(all_derivative_sup,derivative_upper)
                all_time_integral_upper+=integral_upper
                per_interval.append({
                  "j":interval,
                  "source_vector_Linf_upper":decimal_ceil(source_upper),
                  "source_x_derivative_vector_Linf_upper":
                    decimal_ceil(derivative_upper),
                  "source_vector_L1_integral_upper":
                    decimal_ceil(integral_upper),
                })
            modes_rows.append({
              "m":m,
              "source_vector_Linf_x_upper":decimal_ceil(all_source_sup),
              "source_x_derivative_vector_Linf_x_upper":
                  decimal_ceil(all_derivative_sup),
              "source_vector_L1_x_upper":decimal_ceil(all_time_integral_upper),
              "source_row_Linf_upper":
                  {str(k):decimal_ceil(v) for k,v in enumerate(max_per_row)},
              "max_source_control":dominant,
              "continuous_intervals_covered":nt-1,
              "per_interval_certified_upper":per_interval,
            })
            print("GE19_G1I_GE05_PCHIP m=%s Linf=%s L1=%s dLinf=%s"%(
                    m,decimal_ceil(all_source_sup),
                    decimal_ceil(all_time_integral_upper),
                    decimal_ceil(all_derivative_sup)),flush=True)

    report={
      "classification":
        "GE19_G1I_EXACT_INPUT_BERNSTEIN_GE05_PCHIP_CONTINUOUS_FORCING_CERTIFIED_TRUE_GE05_AND_Z11_OPEN",
      "source_frozen_hash":got,
      "source_file":FROZEN_NAME,
      "source_source_git_blobs":pins,
      "scipy_version":scipy.__version__,
      "self_tests":tested,
      "scope":{"C":args.tag,"Nt":nt,"grid":args.grid,
               "modes":list(modes),
               "time_intervals":nt-1,
               "source_main_euler_row_order":
                 ["lapse","isotropic","aether","scalar",
                  "dust_potential","dust_density"],
               "clock":"x=ln a represented by exact float64 rational endpoints"},
      "per_mode":modes_rows,
      "proven_claim":"Continuum-in-x upper bounds on ||s_h(x)||_2, ||ds_h/dx||_2 and integral ||s_h||_2 dx for the explicitly defined SciPy PCHIP cubic source with each stored floating-point coefficient treated as an exact rational; Bernstein positivity/convexity and exact rational arithmetic with integer-square-root ceiling give upper rather than sampled values.",
      "coefficient_generation_roundoff_enclosed":False,
      "true_physical_GE05_source_error_enclosed":False,
      "original_action_canonical_M_F_interval_enclosed":False,
      "original_forced_Z11_8D_IVP_error_enclosed":False,
      "G1_PHYSICAL_CLOSED":False,
      "G3_B_total_frozen":False,
      "full_H4_Ward_certified":False,
      "Z21_certified":False,
      "lensing_licensed":False,
      "scientific_boundary":"Rigorous only for the explicitly defined frozen-input real/imag PCHIP SOURCE POLYNOMIAL s_h using exact arithmetic on the post-interpolation binary64 coefficients. The original Repair32B formula and NPZ are pinned, but coefficient generation in SciPy and the true GE05 bath are not interval-enclosed. No coefficient M/F or true-solution ODE error has been certified. Never compare this source bound to the original H4 shift threshold.",
    }
    args.json_out.parent.mkdir(parents=True,exist_ok=True)
    args.json_out.write_text(
        json.dumps(report,indent=2,sort_keys=True,allow_nan=False)+"\n")
    print(report["classification"],flush=True)

if __name__=="__main__":
    main()
