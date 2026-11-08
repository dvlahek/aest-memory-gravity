#!/usr/bin/env python3
"""GE19 G1K: first true all-subinterval defect upper bound for frozen Z11 surrogate.

Rigorous exact-input residual enclosure on the declared x interval for the
*explicitly defined cubic-Hermite canonical polynomial* y_h(x) reconstructed
from frozen Repair32B nodal fields, original-action momenta, and nodal Euler
slopes. The source s_h is the frozen Repair32B PCHIP polynomial as in G1I.

Original GE06+GE07+Lambda operator M,F is interval-enclosed by the G1J
source-derived action Cmat and a verified Neumann preconditioned block solve.
For each subdivided interval, use EXACT Fraction Bernstein controls of both
y_h and s_h, and interval M,F, to bound
   r(x) = y_h'(x) - M(x)y_h(x) - F(x)s_h(x)
for EVERY x in that subinterval (NOT just three offclock samples).

NOTE: y_h slopes at nodes are constructed using Euler equations, so nodal
residual cancellation is not independent evidence. Even a small verified
defect is NOT a true-solution error certificate without stability, initial
error, and original GE05 source-error enclosures. M,F and source parameter
uncertainties outside specified exact binary64 action inputs not covered.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import subprocess
from fractions import Fraction
from pathlib import Path

import numpy as np
from mpmath import iv
from scipy.interpolate import PchipInterpolator

from ge19 import h4f3d_g1j_verified_action_operator_interval as g1j
from ge19 import h4f3d_g1i_exact_pchip_ge05_forcing_interval_bound as g1i
from ge19 import h4f3d_g1e_z11_original_action_euler_offclock as g1e
from ge19 import h4f3d17_actual_original_action_dense_canonical_H1 as d17
from ge19 import repair32b_factor2_corrected_reduced_h2_z11_reconstruction as r32b

ROOT=Path(__file__).resolve().parents[1]
PINS={
 "ge19/h4f3d_g1j_verified_action_operator_interval.py":
     "16480e44542c8a9bda7d64790bbe99dff4d45890",
 "ge19/h4f3d_g1i_exact_pchip_ge05_forcing_interval_bound.py":
     "d33f70509f8e710157cd57423350d2dd84ff1a25",
 "ge19/repair32b_factor2_corrected_reduced_h2_z11_reconstruction.py":
     "6ece578e8a30f48faaded8808687a9bd5c114608",
}
SOURCE_SHA="5d4a0a72c08d09d096a8de0b428b3c8443fc33e8ad442ed6d997d6bf2bc6e327"
Q=Fraction
ZERO=(Q(0),Q(0))
ONE=(Q(1),Q(0))

def need(ok,why):
    if not bool(ok):raise RuntimeError("GE19_G1K_"+why)

def sha256(path):
    h=hashlib.sha256()
    with Path(path).open("rb") as f:
        for b in iter(lambda:f.read(1<<20),b""):h.update(b)
    return h.hexdigest()

def complex_add(a,b):
    return a[0]+b[0],a[1]+b[1]

def complex_sub(a,b):
    return a[0]-b[0],a[1]-b[1]

def complex_mul_real(r,z):
    return r*z[0],r*z[1]

def fnum(z):
    z=complex(z)
    return Q.from_float(z.real),Q.from_float(z.imag)

def bernstein_split(ctrl,t):
    """Exact de Casteljau split of degree-n rational complex Bernstein."""
    left=[ctrl[0]];right=[ctrl[-1]]
    level=list(ctrl)
    while len(level)>1:
        level=[complex_add(complex_mul_real(1-t,level[i]),
                            complex_mul_real(t,level[i+1]))
               for i in range(len(level)-1)]
        left.append(level[0])
        right.append(level[-1])
    return tuple(left),tuple(reversed(right))

def restrict(ctrl,aa,bb):
    """Return exact Bernstein controls of polynomial restricted to [aa,bb]."""
    need(Q(0)<=aa<bb<=Q(1),"BAD_NORMALIZED_SUBINTERVAL")
    if bb==1:
        left=ctrl
    else:
        left,_=bernstein_split(ctrl,bb)
    if aa==0:return left
    _,right=bernstein_split(left,aa/bb)
    return right

def make_hermite(y0,y1,d0,d1,h):
    """Exactly define cubic Hermite polynomial with binary64 endpoints/slopes."""
    z0=fnum(y0);z1=fnum(y1);s0=fnum(d0);s1=fnum(d1)
    b0=z0
    b1=complex_add(z0,complex_mul_real(h/3,s0))
    b2=complex_sub(z1,complex_mul_real(h/3,s1))
    b3=z1
    b=(b0,b1,b2,b3)
    db=tuple(complex_mul_real(Q(3)/h,complex_sub(b[i+1],b[i]))
             for i in range(3))
    need(db[0]==s0 and db[2]==s1,"HERMITE_ENDPOINT_SLOPE_IDENTITY")
    return b,db

def rational_iv(r):
    return iv.mpf(r.numerator)/iv.mpf(r.denominator)

def hull_controls(controls):
    """Each control convex hull encloses the polynomial at ALL u in [0,1]."""
    re_lo=min(z[0] for z in controls)
    re_hi=max(z[0] for z in controls)
    im_lo=min(z[1] for z in controls)
    im_hi=max(z[1] for z in controls)
    lo_re=rational_iv(re_lo);hi_re=rational_iv(re_hi)
    lo_im=rational_iv(im_lo);hi_im=rational_iv(im_hi)
    return iv.mpc(iv.mpf([lo_re.a,hi_re.b]),
                  iv.mpf([lo_im.a,hi_im.b]))

def complex_matrix_product(A,B):
    return g1j.matmul(A,B)

def solve_iv_columns(A,R,b_column_matrix,centers):
    """Preconditioner proof: ||z-z0||inf<=||R(b-Az0)||inf/(1-q)."""
    aiv=A
    riv=g1j.as_iv_matrix(R)
    inv,q=g1j.neumann_test(aiv,riv)
    need(inv is not None,"INTERVAL_AZ_INCONCLUSIVE")
    q_hi=g1j.ub(q)
    need(0<=q_hi<1,"NO_CONTRACTION")
    n=len(A);nc=len(b_column_matrix[0])
    actual=[]
    corrections=[]
    for col in range(nc):
        z0=[g1j.fc(centers[k,col]) for k in range(n)]
        residual=[
          b_column_matrix[i][col]-
          sum((aiv[i][k]*z0[k] for k in range(n)),iv.mpc(0))
          for i in range(n)]
        rr=[
          sum((riv[i][k]*residual[k] for k in range(n)),iv.mpc(0))
          for i in range(n)]
        maxrr=max(g1j.ub(abs(z).b) for z in rr)
        radius=math.nextafter(maxrr/(1-q_hi),math.inf)
        need(math.isfinite(radius) and radius>=0,
             "NONFINITE_NEUMANN_CORRECTION")
        wide=g1j.fi(radius)
        enclosed=[]
        for v in z0:
            c_re=v.real;c_im=v.imag
            enclosed.append(
                iv.mpc(iv.mpf([(c_re-wide).a,(c_re+wide).b]),
                       iv.mpf([(c_im-wide).a,(c_im+wide).b])))
        actual.append(enclosed)
        corrections.append(radius)
    return [[actual[col][i] for col in range(nc)] for i in range(n)],q_hi,max(corrections)

def original_interval_MF(C,box,Cmid):
    # EXACT source-locked R07 canonical row structure.
    alg=C[:4]+[C[5]]+[
       [C[12][j]+C[13][j] for j in range(10)]]
    A=[[alg[i][j] for j in g1j.ZIDX] for i in range(6)]
    Aq=[[alg[i][j] for j in g1j.QIDX] for i in range(6)]
    Am=np.vstack([
        Cmid[:4],Cmid[5:6],Cmid[12:13]+Cmid[13:14]
    ])[:,g1j.ZIDX]
    R=np.linalg.inv(Am)
    # b=Ry*y+Rr*source, 16 columns in one validated correction pass.
    B=[[iv.mpc(0) for _ in range(16)] for _ in range(6)]
    for i in range(6):
        for j in range(4):
            B[i][j]=-Aq[i][j]
    for i in range(4):B[i][i+4]+=iv.mpc(1)
    B[4][8+5]=iv.mpc(1)
    B[5][8+7]=iv.mpc(1)
    zcent=np.zeros((6,16),complex)
    # Numeric midpoint is permitted to choose any z0; only the interval
    # residual and contraction q certify its error enclosure.
    Y=np.zeros((6,16),complex)
    Y[:,:4]=-Cmid[:0].reshape(0,10) if False else 0  # overwritten below
    A_qmid=np.vstack([Cmid[:4],Cmid[5:6],
                       Cmid[12:13]+Cmid[13:14]])[:,g1j.QIDX]
    Y[:,:4]=-A_qmid
    Y[:4,4:8]=np.eye(4)
    Y[4,8+5]=1
    Y[5,8+7]=1
    zcent=R@Y
    Z,q,rad=solve_iv_columns(A,R,B,zcent)
    WY=[[iv.mpc(0) for _ in range(8)] for _ in range(10)]
    WR=[[iv.mpc(0) for _ in range(8)] for _ in range(10)]
    for i in range(4):WY[g1j.QIDX[i]][i]=iv.mpc(1)
    for i,row in enumerate(g1j.ZIDX):
        for col in range(8):
            WY[row][col]=Z[i][col]
            WR[row][col]=Z[i][8+col]
    H=box["H"]
    need(H.a>0,"NONPOSITIVE_H_INTERVAL")
    M=[[iv.mpc(0) for _ in range(8)] for _ in range(8)]
    F=[[iv.mpc(0) for _ in range(8)] for _ in range(8)]
    for i in range(4):
        for j in range(8):
            M[i][j]=Z[i+2][j]/H
            F[i][j]=Z[i+2][j+8]/H
    for i in range(4):
        for j in range(8):
            M[4+i][j]=sum((C[6+i][k]*WY[k][j]
                           for k in range(10)),iv.mpc(0))/H
            v=sum((C[6+i][k]*WR[k][j]
                   for k in range(10)),iv.mpc(0))
            if j==i+1:v-=iv.mpc(1)
            F[4+i][j]=v/H
    return M,F,q,rad

def validated_defect(M,F,y,ydot,s):
    maxabs=0.
    rows=[]
    for i in range(8):
        res=ydot[i]-sum((M[i][k]*y[k] for k in range(8)),iv.mpc(0))\
             -sum((F[i][k]*s[k] for k in range(8)),iv.mpc(0))
        v=g1j.ub(abs(res).b)
        need(math.isfinite(v) and v>=0,"NONFINITE_RESIDUAL_BOUND")
        rows.append(v)
        maxabs=max(maxabs,v)
    return maxabs,rows

def selftest():
    b=(ZERO,(Q(1,3),Q(0)),(Q(2,3),Q(0)),ONE)
    left=restrict(b,Q(1,4),Q(1,2))
    need(left[0]==(Q(1,4),Q(0)) and
         left[-1]==(Q(1,2),Q(0)),
         "EXACT_DECASTELJAU_ENDPOINTS_FAILED")
    y,dy=make_hermite(1+2j,3+4j,0.25-0.5j,0.75+0.5j,Q(1,8))
    need(y[0]==fnum(1+2j) and y[-1]==fnum(3+4j),
         "EXACT_HERMITE_ENDPOINT_FAILED")
    check=hull_controls(restrict(b,Q(1,4),Q(1,2)))
    need(check.real.a<=iv.mpf(Q(1,4).numerator)/iv.mpf(Q(1,4).denominator)
         and check.real.b>=iv.mpf(Q(1,2).numerator)/iv.mpf(Q(1,2).denominator),
         "INTERVAL_BERNSTEIN_HULL_FAILED")
    return {"exact_bernstein_restriction":True,
            "exact_hermite_endpoints_derivatives":True,
            "outward_bernstein_complex_hull":True}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--results-dir",type=Path,default=ROOT/"results")
    ap.add_argument("--tag",default="C_star",choices=g1e.TAGS)
    ap.add_argument("--grid",default="primary",choices=g1e.GRIDS.keys())
    ap.add_argument("--mode",type=int,default=20,choices=g1e.MODES)
    ap.add_argument("--interval",type=int,default=0)
    ap.add_argument("--subdivisions",type=int,default=4)
    ap.add_argument("--dps",type=int,default=60)
    ap.add_argument("--json-out",type=Path)
    ap.add_argument("--self-test",action="store_true")
    args=ap.parse_args()
    need(40<=args.dps<=200 and 1<=args.subdivisions<=32,
         "INTERVAL_PRECISION_OR_SUBDIVISIONS")
    iv.dps=args.dps
    tests=selftest()
    if args.self_test:
        print("GE19_G1K_INTERVAL_BERNSTEIN_DEFECT_SELFTEST_PASS")
        return
    need(args.json_out is not None and not args.json_out.exists(),
         "OUTPUT_PATH_MISSING_OR_EXISTS")
    pins=g1j.locks(args.results_dir.resolve())
    for path,want in PINS.items():
        commit=subprocess.check_output(["git","rev-parse","HEAD:"+path],
                                         cwd=ROOT,text=True).strip()
        work=subprocess.check_output(["git","hash-object",str(ROOT/path)],
                                        cwd=ROOT,text=True).strip()
        need(commit==work==want,"SOURCE_GIT_BLOB_CHANGED_"+path)
        pins[path]=want
    paths=g1e.files(args.results_dir)
    need(sha256(paths["z11"])==SOURCE_SHA,"FROZEN_Z11_NPZ_CHANGED")
    nt=g1e.GRIDS[args.grid]
    need(0<=args.interval<nt-1,"BAD_INTERVAL_INDEX")
    old=d17.d16r1.d15.d13.old
    d15=d17.d16r1.d15
    r7=old.r7
    index=g1e.MODES.index(args.mode)
    k=float(args.mode*r7.g9.K_REQ[0]/r7.FOURIER_N[0])
    results=[]
    with np.load(paths["r13"],allow_pickle=False) as z13,\
         np.load(paths["z11"],allow_pickle=False) as data:
        bgs,_,mod6,mod7,_,_,_,_,_=old.build_context(
            args.results_dir,z13)
        bg=bgs[(nt,args.tag)]
        x=np.asarray(bg["x"],float)
        need(np.array_equal(x,np.asarray(data["x_"+args.grid],float)),
             "Z11_BACKGROUND_CLOCK_CHANGED")
        j=args.interval
        state=np.asarray(data[f"{args.tag}_Z11_{args.grid}"],complex)[index]
        dot=np.asarray(data[f"{args.tag}_Z11dot_{args.grid}"],complex)[index]
        sourceall=np.asarray(data[f"{args.tag}_M1_rhs_{args.grid}"],complex)
        need(np.isfinite(state).all() and np.isfinite(dot).all() and
             np.isfinite(sourceall).all(),"NONFINITE_FROZEN_INPUT")
        all_b=np.asarray(data[f"{args.tag}_B10_{args.grid}"],complex)
        need(np.array_equal(sourceall,r32b.source_from_B(bg,all_b)),
             "FROZEN_GE05_SOURCE_NOT_IDENTICAL")
        raw=sourceall[index]
        real=PchipInterpolator(x,raw.real,axis=-1,extrapolate=False)
        imag=PchipInterpolator(x,raw.imag,axis=-1,extrapolate=False)
        funcs6,funcs7=g1j.expr_compilers(mod6,mod7)
        action_H,_=d15.clk.make_original_action_background(
            r7,bg,args.tag)
        action=d17.core.ActionBackground(r7,bg,action_H)
        saved_callback=r7._bg_point
        saved_cache=r7._CANONICAL_LOCAL_CACHE
        r7._CANONICAL_LOCAL_CACHE={}
        r7._bg_point=lambda background,t:action(background,float(t))
        try:
            action.knot_check()
            h=Q.from_float(float(x[j+1]))-Q.from_float(float(x[j]))
            need(h>0,"BAD_POSITIVE_PHYSICAL_INTERVAL")
            ypair=[]
            dpair=[]
            for node in (j,j+1):
                w=np.empty(10,complex)
                w[0]=state[0,node]
                w[1]=state[5,node]
                w[2:6]=state[1:5,node]
                w[6:10]=dot[:,node]
                M,F,ZY,ZR,WY,WR,Cmat,bp,_=(
                    r7._canonical_operator_matrices(
                        mod6,mod7,bg,args.tag,k,float(x[node])))
                p=Cmat[0:4]@w
                yy=np.r_[w[2:6],p]
                src=np.r_[raw[:,node],np.zeros(2,complex)]
                yd=M@yy+F@src
                ypair.append(yy)
                dpair.append(yd)
            yctrl=[];dctrl=[]
            for row in range(8):
                bs,db=make_hermite(ypair[0][row],ypair[1][row],
                                  dpair[0][row],dpair[1][row],h)
                yctrl.append(bs)
                dctrl.append(db)
            sctrl=[]
            for row in range(6):
                coeffs=tuple(complex(real.c[p,j,row],imag.c[p,j,row])
                            for p in range(4))
                bs,_=g1i.bernstein(coeffs,h)
                sctrl.append(bs)
            for row in range(2):sctrl.append((ZERO,ZERO,ZERO,ZERO))
            largest=0.;integral_up=0.;q_max=0.;correction_max=0.
            for step in range(args.subdivisions):
                aa=Q(step,args.subdivisions)
                bb=Q(step+1,args.subdivisions)
                xa=float(x[j])+float(h)*float(aa)
                xb=float(x[j])+float(h)*float(bb)
                # Ensure interval encloses exact dyadic sub-endpoints:
                # a rounded x coordinate can be slightly inside; expand
                # outward by one float ulp (inside original interval).
                xa=max(float(x[j]),math.nextafter(xa,-math.inf))
                xb=min(float(x[j+1]),math.nextafter(xb,math.inf))
                box=g1j.bg_box(r7,bg,args.tag,xa,xb)
                CI=g1j.interval_C(funcs6,funcs7,r7,args.tag,k,box)
                xm=(xa+xb)*.5
                Cmid,_,_=r7._local_linear_matrix(
                    mod6,mod7,bg,args.tag,k,xm)
                M,F,q,correction=original_interval_MF(CI,box,Cmid)
                ybox=[hull_controls(restrict(c,aa,bb)) for c in yctrl]
                dybox=[hull_controls(restrict(c,aa,bb)) for c in dctrl]
                sbox=[hull_controls(restrict(c,aa,bb)) for c in sctrl]
                defect,byrow=validated_defect(M,F,ybox,dybox,sbox)
                dx=h*(bb-aa)
                integral_up+=math.nextafter(float(dx)*defect,math.inf)
                largest=max(largest,defect)
                q_max=max(q_max,q)
                correction_max=max(correction_max,correction)
                results.append({
                  "subinterval":step,
                  "u_lo_exact_rational":str(aa),
                  "u_hi_exact_rational":str(bb),
                  "x_lo_cover_float64":xa,
                  "x_hi_cover_float64":xb,
                  "q_neumann_upper":q,
                  "max_column_Az_solution_correction_abs_upper":correction,
                  "canonical_defect_vector_Linf_upper":defect,
                  "canonical_defect_each_row_abs_upper":byrow,
                  "source_polynomial_and_y_hermite_bernstein_full_subinterval":True
                })
                print("GE19_G1K j=%d subdiv=%d q=%.7g ||r||inf<=%.9g"%(
                     j,step,q,defect),flush=True)
                r7._CANONICAL_LOCAL_CACHE.clear()
        finally:
            r7._bg_point=saved_callback
            r7._CANONICAL_LOCAL_CACHE=saved_cache
    report={
      "classification":
        "GE19_G1K_EXACT_INPUT_FULL_SUBINTERVAL_CANONICAL_Z11_POLYNOMIAL_DEFECT_ENCLOSED_TRUE_Z11_ERROR_OPEN",
      "scope":{"tag":args.tag,"grid":args.grid,"Nt":nt,
               "m":args.mode,"j":args.interval,
               "subdivisions":args.subdivisions,
               "precision_decimal_digits":args.dps,
               "x_lo":float(x[j]),"x_hi":float(x[j+1])},
      "source_locks":pins,
      "parent_sha256":{key:sha256(p) for key,p in paths.items()},
      "selftests":tests,
      "all_subintervals_verified":len(results)==args.subdivisions and
                                    all(z["q_neumann_upper"]<1 for z in results),
      "max_continuous_canonical_residual_infinity_norm_upper":largest,
      "integral_continuous_canonical_residual_infinity_norm_upper":integral_up,
      "max_Az_Neumann_q_upper":q_max,
      "max_verified_linear_solution_correction_upper":correction_max,
      "per_subinterval":results,
      "mathematical_scope":"For each exact-input frozen coefficient and explicitly constructed binary64-node canonical Hermite polynomial y_h, all x subsegments are enclosed via exact rational Bernstein hulls, original GE06/GE07/Lambda interval Cmat and Neumann-validated algebraic linear solves. M,F reconstructed entry-wise by original Noether canonical formulas. The residual inequality is for this DECLARED POLYNOMIAL and the declared frozen GE05 SciPy PCHIP polynomial, not for an independently true solution.",
      "source_generation_float_roundoff_certified":False,
      "true_GE05_source_error_enclosed":False,
      "global_Z11_IVP_error_enclosed":False,
      "original_H4_Euler_Ward_certified":False,
      "G1_PHYSICAL_CLOSED":False,
      "G3_B_total_frozen":False,
      "Z21_certified":False,
      "lensing_licensed":False
    }
    args.json_out.parent.mkdir(parents=True,exist_ok=True)
    args.json_out.write_text(json.dumps(report,indent=2,
                                      sort_keys=True,allow_nan=False)+"\n")
    print(report["classification"],flush=True)

if __name__=="__main__":
    main()
