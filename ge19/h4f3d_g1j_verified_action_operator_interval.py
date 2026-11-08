#!/usr/bin/env python3
"""GE19 G1J: rigorous fixed-binary64-input interval Az invertibility and M/F norm gate.

For the unmodified GE06/GE07/Λ symbolic first-order action, use mpmath
directed interval arithmetic on the *whole x interval*, not selected x
samples. Original Repair13/D15a analytic action background is enclosed:
KQ=I0 exp(-3x); KQ=4 K2 Z0 Z exp(Z^2), inverted by certified monotone
bracketing; H^2=(Q KQ-K)/3 + C exp(-3x)+rho_lambda.

GE06/GE07 symbolic linear directional coefficients are evaluated in the
interval background to construct the ORIGINAL 16x10 Cmat and the ORIGINAL
Noether-regularized 6x6 Az. A numeric inverse R of a midpoint Az is used
ONLY as an exact-input preconditioner. ||I-R Az(I)||_infty < 1, computed
with interval arithmetic, then certifies invertibility of every Az(x)
throughout I, even if R was numerically inaccurate. From this we derive
valid, potentially conservative M/F/WY/WR norm bounds.

Scope is the mathematical exact-input analytic action operator defined
by the stored float64 physical constants; floating-point uncertainty
in original parent generation, source action, and SciPy is NOT enclosed.
This script does NOT certify any GE05 bath true-source error or any Z11
trajectory/IVP residual; it does NOT license physical G1, H4 or lensing.
No source coefficients, original NPZ data or physics thresholds changed.
"""
from __future__ import annotations
import argparse, hashlib, json, math, subprocess
from fractions import Fraction
from pathlib import Path

import numpy as np
import sympy as sp
from mpmath import iv
from ge19 import h4f3d17_actual_original_action_dense_canonical_H1 as d17

ROOT=Path(__file__).resolve().parents[1]
PINS={
 "ge19/repair07_window_retarded_reduced_h3_z20_particular.py":
    "e34d28a2062c748f48bc82fa928844b02631de25",
 "ge19/h4f3d17_actual_original_action_dense_canonical_H1.py":
    "813c350d1d1860515997ce43f223b9b6bc2091e9",
 "ge19/h4f3d15a_original_GE05_clock_embedded_source.py":
    "6af45e30a9719741d54360702d733374f78a0c52",
 "ge06/analytic_aest_directional_source_generator.py":
    "a7afe0035054a9dca55d74a6497c081422114b4c",
 "ge07/pressureless_matter_directional_source_generator.py":
    "cde8da77a80799cef00fc7c09c3633310fc9e3d4",
}
R13_NAME="ge19_repair13_self_consistent_reduced_background_h1_reclosure.npz"
R13_SHA="011c0ae54fd21d70c0e2c695ce62e7b74a3c5529a07c9023c882a447d5b40ca3"
GE15_NAME="ge15_R1_dense_accepted_step_trace.dat"
GE15_SHA="7f57ab676f2a31cf0abf93ff0f8b0f1f2f80bb9a58d7cf1e47e10a158c57c69f"
TINY=1e-300
ZIDX=(0,1,6,7,8,9)
QIDX=(2,3,4,5)
MODES=(3,5,8,10,15,20)
NT={"primary":128,"control":64}

def need(v,msg):
    if not bool(v): raise RuntimeError("GE19_G1J_"+msg)

def sha(path):
    h=hashlib.sha256()
    with Path(path).open("rb") as f:
        for b in iter(lambda:f.read(1<<20),b""):h.update(b)
    return h.hexdigest()

def locks(rd):
    out={}
    for name,want in PINS.items():
        git=subprocess.check_output(["git","rev-parse","HEAD:"+name],
                cwd=ROOT,text=True).strip()
        work=subprocess.check_output(["git","hash-object",str(ROOT/name)],
                cwd=ROOT,text=True).strip()
        need(git==work==want,"ORIGINAL_GIT_SOURCE_CHANGED_"+name)
        out[name]=want
    for name,want in ((R13_NAME,R13_SHA),(GE15_NAME,GE15_SHA)):
        file=rd/name
        need(file.is_file() and sha(file)==want,"ORIGINAL_PARENT_CHANGED_"+name)
        out["SHA256:"+name]=want
    return out

def fi(value):
    """Exact represented binary64 value as mpmath directed point interval."""
    x=float(value)
    need(math.isfinite(x),"NONFINITE_FLOAT_INPUT")
    n,d=x.as_integer_ratio()
    return iv.mpf(n)/iv.mpf(d)

def fc(value):
    z=complex(value)
    return iv.mpc(fi(z.real),fi(z.imag))

def ci(v):
    if hasattr(v,"_mpci_"):return v
    if isinstance(v,complex):return fc(v)
    return iv.mpc(v,iv.mpf(0))

def ub(v):
    """Outward-rounded binary64 value used only for serializing interval upper."""
    if hasattr(v,"_mpi_"):
        v=v.b
    f=float(v)
    need(math.isfinite(f),"INFINITE_VERIFIED_UPPER")
    return math.nextafter(f,math.inf)

def norminf_upper(A):
    best=iv.mpf(0)
    for row in A:
        rr=iv.mpf(0)
        for z in row: rr+=abs(ci(z)).b
        if rr.b>best.b:best=rr.b
    return best.b

def matmul(A,B):
    n=len(A);p=len(B);m=len(B[0])
    need(all(len(row)==p for row in A),"BAD_COMPLEX_INTERVAL_MATMUL")
    return [[sum((A[i][k]*B[k][j] for k in range(p)),
                 iv.mpc(0)) for j in range(m)] for i in range(n)]

def as_iv_matrix(A):
    return [[fc(v) for v in row] for row in np.asarray(A,complex)]

def neumann_test(A,R):
    """R arbitrary exact complex matrix, so q<1 rigorously proves A invertible."""
    v=matmul(R,A)
    E=[[(iv.mpc(1) if i==j else iv.mpc(0))-v[i][j]
         for j in range(len(A))] for i in range(len(A))]
    q=norminf_upper(E)
    if not q<iv.mpf(1):return None,q
    rnorm=norminf_upper(R)
    return (rnorm/(iv.mpf(1)-q)).b,q

def selftest():
    # For all t in [0,1], A(t)=diag(2+t,3) is invertible.
    A=[[iv.mpc(iv.mpf([2,3])),iv.mpc(0)],
       [iv.mpc(0),iv.mpc(3)]]
    R=as_iv_matrix(np.diag([0.4,1/3]))
    inv,q=neumann_test(A,R)
    need(inv is not None and q<iv.mpf(1) and inv>iv.mpf(0),
         "NONSINGULAR_WHOLE_INTERVAL_TEST_FAILED")
    # The same test must NOT certify diag(t,1) with t in [-1,1].
    B=[[iv.mpc(iv.mpf([-1,1])),iv.mpc(0)],
       [iv.mpc(0),iv.mpc(1)]]
    bad,qbad=neumann_test(B,as_iv_matrix(np.eye(2)))
    need(bad is None and qbad>=iv.mpf(1),
         "SINGULAR_INTERVAL_INCORRECTLY_CERTIFIED")
    # Test the actual hyperbolic interval replacements, rather than merely
    # testing the independent inverse bound: symbolic lambdify must retain
    # interval inputs and enclose both endpoint values.
    z=sp.symbols("z",real=True)
    eval_hyper=sp.lambdify(
        (z,),sp.cosh(z)+sp.sinh(z),
        modules=[{"cosh":iv_cosh,"sinh":iv_sinh,"exp":iv.exp},
                 "mpmath"],cse=True)
    test_range=iv.mpf([-1,1])
    y=eval_hyper(test_range)
    need(y.a<=iv.exp(iv.mpf(-1)).a and
         y.b>=iv.exp(iv.mpf(1)).b,
         "HYPERBOLIC_INTERVAL_LAMBDIFY_ENCLOSURE_FAILED")
    return {"interval_neumann_nonsingular_pass":True,
            "interval_neumann_singular_rejected":True,
            "interval_hyperbolic_lambdify_endpoint_enclosure":True}

def iv_cosh(z):
    """Cosh enclosure via directed interval exp; mpmath.iv has no .cosh."""
    return (iv.exp(z)+iv.exp(-z))/iv.mpf(2)


def iv_sinh(z):
    """Sinh enclosure via directed interval exp; mpmath.iv has no .sinh."""
    return (iv.exp(z)-iv.exp(-z))/iv.mpf(2)


def expr_compilers(mod6,mod7):
    # Original Repair07 builds a source-locked GE06 stable-Z symbolic c1.
    # Lambdify with iv.mpf so rational constants remain outward rounded,
    # and with iv.exp so the Exp branch is genuinely interval evaluated.
    expr6=mod6.coeff1_expr
    symbols=set().union(*(e.free_symbols for e in expr6.values()))
    byname={s.name:s for s in symbols}
    names=list(mod6.frozen_symbol_contract["frozen_arg_names"])
    need(len(names)==23,"GE06_FROZEN_SYMBOL_CONTRACT_CHANGED")
    names[2]="Zb"
    args6=tuple(byname.get(name,sp.Symbol(name)) for name in names)
    need(all(e.free_symbols.issubset(set(args6)) for e in expr6.values()),
         "GE06_UNRECOGNIZED_SYMBOLS")
    # Interval context deliberately lacks sinh/cosh methods in several
    # released mpmath versions. Build them from certified interval exp,
    # never fall back to scalar mpmath functions on interval arguments.
    use={"mpf":iv.mpf,"exp":iv.exp,"sqrt":iv.sqrt,
         "cosh":iv_cosh,"sinh":iv_sinh}
    six={name:sp.lambdify(args6,ex,modules=[use,"mpmath"],cse=True)
         for name,ex in expr6.items()}
    seven={name:sp.lambdify(mod7.direction_args,ex,
                 modules=[use,"mpmath"],cse=True)
           for name,ex in mod7.coeff1.items()}
    need(all(k in six for k in ("L_t","R_t","u_t","phi_t",
                   "L_f","R_f","L_x","R_x","u_f","u_x",
                   "phi_x","b_f","b_x","N_f","N_x")),
         "GE06_MISSING_LINEAR_OPERATOR_PARTIAL")
    need(all(k in seven for k in ("N_f","L_f","R_f","b_f",
                   "rho_f","T_t","T_x")),
         "GE07_MISSING_LINEAR_OPERATOR_PARTIAL")
    return six,seven

def dyadic_iv(fr):
    return iv.mpf(fr.numerator)/iv.mpf(fr.denominator)

def z_bracket(kq,K2,Z0,steps=68):
    """Certified root box using monotonic KQ=4*K2*Z0*Z*exp(Z^2)."""
    const=iv.mpf(4)*fi(K2)*fi(Z0)
    def f(z):
        t=dyadic_iv(z)
        return const*t*iv.exp(t*t)
    hi=Fraction(1,1)
    for _ in range(16):
        if f(hi).a>=kq.b:break
        hi*=2
    else:raise RuntimeError("GE19_G1J_NO_CERTIFIED_UPPER_Z")
    lower=Fraction(0);right=hi
    for _ in range(steps):
        mid=(lower+right)/2
        if f(mid).b<=kq.a:lower=mid
        else:right=mid
    left=Fraction(0);upper=hi
    for _ in range(steps):
        mid=(left+upper)/2
        if f(mid).a>=kq.b:upper=mid
        else:left=mid
    need(f(lower).b<=kq.a and f(upper).a>=kq.b,
         "ROOT_MONOTONE_BRACKET_VALIDATION_FAILED")
    return iv.mpf([dyadic_iv(lower).a,dyadic_iv(upper).b])

def bg_box(r7,bg,tag,xa,xb):
    x=iv.mpf([fi(xa).a,fi(xb).b])
    a=iv.exp(x)
    charge=float(np.median(np.asarray(bg["a"],float)**3*
                           np.asarray(bg["KQ_action"],float)))
    lam=float(np.median(np.asarray(bg["rho_lambda_action"],float)))
    kq=fi(charge)*iv.exp(-3*x)
    need(kq.a>0,"BAD_ACTION_SCALAR_CHARGE_INTERVAL")
    Z=z_bracket(kq,r7.K2,r7.Z0)
    Q=fi(r7.Q0)+fi(r7.Z0)*Z
    K=iv.mpf(2)*fi(r7.K2)*fi(r7.Z0)**2*(iv.exp(Z*Z)-iv.mpf(1))
    dust=fi(r7.C_VALUES[tag])*iv.exp(-3*x)
    H2=(Q*kq-K)/iv.mpf(3)+dust+fi(lam)
    need(H2.a>0,"NONPOSITIVE_ACTION_H2_INTERVAL")
    H=iv.sqrt(H2)
    rho=iv.mpf(3)*fi(r7.C_VALUES[tag])/(a**3)
    need(H.a>0 and Z.a>0 and a.a>0,"NONPOSITIVE_ACTION_BACKGROUND")
    return {"x":x,"a":a,"H":H,"Z":Z,"Q":Q,"rho":rho,
            "charge_median_f64":charge,"lambda_median_f64":lam}

def raw_interval(mod6,mod7,r7,tag,k,box,w):
    N,dr,S,u,phi,T,Sdot,udot,phidot,Tdot=w
    a,H,Z,rho=(box[k] for k in ("a","H","Z","rho"))
    zero=iv.mpc(0)
    ik=iv.mpc(iv.mpf(0),fi(k))
    vals6=(a,a*H,Z,N,S,S,zero,u,Sdot,ik*S,Sdot,ik*S,
           zero,udot,ik*u,phidot,ik*phi,ik*N,
           fi(r7.KB),fi(r7.CV),fi(r7.K2),fi(r7.Q0),fi(r7.Z0))
    vals7=(a,rho,N,S,S,zero,dr,Tdot,ik*T)
    p6={name:ci(fn(*vals6)) for name,fn in mod6.items()}
    p7={name:ci(fn(*vals7)) for name,fn in mod7.items()}
    return [
      p6["L_t"]+p6["R_t"],p6["u_t"],p6["phi_t"],p7["T_t"],
      p6["N_f"]-ik*p6["N_x"]+p7["N_f"],p7["rho_f"],
      p6["L_f"]+p6["R_f"]-ik*(p6["L_x"]+p6["R_x"])+p7["L_f"]+p7["R_f"],
      p6["u_f"]-ik*p6["u_x"],-ik*p6["phi_x"],-ik*p7["T_x"],
      p6["b_f"]-ik*p6["b_x"],p7["b_f"],
      p6["L_f"]-ik*p6["L_x"]-iv.mpf("0.5")*(p6["R_f"]-ik*p6["R_x"]),
      p7["L_f"]-iv.mpf("0.5")*p7["R_f"],
      p6["L_t"],p6["R_t"],
    ]

def interval_C(mod6,mod7,r7,tag,k,box):
    z=[iv.mpc(0) for _ in range(10)]
    zero=raw_interval(mod6,mod7,r7,tag,k,box,z)
    # c1 operator is homogeneous linear by action perturbation definition.
    # Check zero offset interval algebraically contains 0 and is negligible
    # as a symbolic expression; do NOT use numeric samples as proof.
    for i,v in enumerate(zero):
        if not (v.real.a<=0<=v.real.b and v.imag.a<=0<=v.imag.b):
            raise RuntimeError("GE19_G1J_NONZERO_SYMBOLIC_ZERO_ROW_"+str(i))
    C=[[None for _ in range(10)] for _ in range(16)]
    for j in range(10):
        e=[iv.mpc(0) for _ in range(10)];e[j]=iv.mpc(1)
        row=raw_interval(mod6,mod7,r7,tag,k,box,e)
        for i in range(16):C[i][j]=row[i]-zero[i]
    return C

def max_iv(a,b):
    return a if a.b>=b.b else b

def certify_interval(C,box,preconditioner):
    # Original _canonical_operator_matrices Noether partition:
    # Calg = vstack(Cmat[0:4], Cmat[5], Cmat[12]+Cmat[13]).
    alg=C[0:4]+[C[5]]+[
        [C[12][j]+C[13][j] for j in range(10)]]
    Az=[[alg[i][j] for j in ZIDX] for i in range(6)]
    Aq=[[alg[i][j] for j in QIDX] for i in range(6)]
    R=as_iv_matrix(preconditioner)
    inv,q=neumann_test(Az,R)
    out={"q_neumann_upper":ub(q),"Az_continuous_invertible":inv is not None}
    if inv is None:return out
    aq=norminf_upper(Aq)
    dyn=norminf_upper(C[6:10])
    one=iv.mpf(1)
    zy=inv*(one+aq)
    zr=inv
    wy=max_iv(one,zy)
    wr=zr
    hmin=box["H"].a
    M=max_iv(zy/hmin,dyn*wy/hmin)
    F=max_iv(zr/hmin,(dyn*wr+one)/hmin)
    out.update({
      "Az_inverse_norm_inf_upper":ub(inv),
      "Aq_norm_inf_upper":ub(aq),
      "C_dynamic_rows_norm_inf_upper":ub(dyn),
      "WY_norm_inf_upper":ub(wy),
      "WR_norm_inf_upper":ub(wr),
      "M_norm_inf_upper":ub(M),
      "F_norm_inf_upper":ub(F),
      "H_lower_positive_conservative":math.nextafter(float(hmin),-math.inf),
      "operator_componentwise_absolute_upper":ub(max_iv(M,F)),
    })
    return out

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--results-dir",type=Path,default=ROOT/"results")
    ap.add_argument("--tag",choices=("C_min","C_star","C_max"),default="C_star")
    ap.add_argument("--grid",choices=NT.keys(),default="primary")
    ap.add_argument("--mode",type=int,choices=MODES,default=20)
    ap.add_argument("--start-interval",type=int,default=0)
    ap.add_argument("--interval-count",type=int,default=1)
    ap.add_argument("--dps",type=int,default=60)
    ap.add_argument("--json-out",type=Path)
    ap.add_argument("--self-test",action="store_true")
    args=ap.parse_args()
    need(40<=args.dps<=200,"BAD_INTERVAL_PRECISION")
    iv.dps=args.dps
    tests=selftest()
    if args.self_test:
        print("GE19_G1J_INTERVAL_INVERSE_SELFTEST_PASS",flush=True)
        return
    need(args.json_out is not None and not args.json_out.exists(),
         "REQUIRE_UNWRITTEN_JSON_OUTPUT")
    rd=args.results_dir.resolve()
    pins=locks(rd)
    d15=d17.d16r1.d15
    old=d15.d13.old
    r7=old.r7
    need(tuple(map(int,r7.FOURIER_N))==MODES,
         "ORIGINAL_FOURIER_MODE_SET_CHANGED")
    nt=NT[args.grid]
    need(0<=args.start_interval<nt-1 and
         1<=args.interval_count<=nt-1-args.start_interval,
         "INTERVAL_SUBDOMAIN_INVALID")
    with np.load(rd/R13_NAME,allow_pickle=False) as z13:
        bgs,_,mod6,mod7,_,_,_,_,_=old.build_context(rd,z13)
        bg=bgs[(nt,args.tag)]
        x=np.asarray(bg["x"],float)
        need(x.shape==(nt,) and np.all(np.diff(x)>0),
             "ORIGINAL_ACTION_CLOCK_INVALID")
        funcs6,funcs7=expr_compilers(mod6,mod7)
        k=float(args.mode*r7.g9.K_REQ[0]/r7.FOURIER_N[0])
        evalH,_=d15.clk.make_original_action_background(r7,bg,args.tag)
        action=d17.core.ActionBackground(r7,bg,evalH)
        action.knot_check()
        orig_cb=r7._bg_point;orig_cache=r7._CANONICAL_LOCAL_CACHE
        r7._CANONICAL_LOCAL_CACHE={}
        r7._bg_point=lambda bg0,t:action(bg0,float(t))
        records=[]
        try:
            for j in range(args.start_interval,
                           args.start_interval+args.interval_count):
                a=float(x[j]);b=float(x[j+1])
                # Midpoint is used ONLY to choose an arbitrary numeric R.
                # The proof tests interval I-R Az([a,b]); no midpoint sampling
                # is ever substituted for the interval operator.
                xm=a+0.5*(b-a)
                Cmid,_,_=r7._local_linear_matrix(
                    mod6,mod7,bg,args.tag,k,xm)
                Am=np.vstack([Cmid[0:4],Cmid[5:6],
                              Cmid[12:13]+Cmid[13:14]])[:,ZIDX]
                R=np.linalg.inv(Am)
                box=bg_box(r7,bg,args.tag,a,b)
                CI=interval_C(funcs6,funcs7,r7,args.tag,k,box)
                row=certify_interval(CI,box,R)
                row.update({"j":j,"x_lo_binary64":a,"x_hi_binary64":b,
                            "action_charge_lambda_frozen_binary64":True,
                            "numeric_midpoint_condition_diagnostic_only":
                                float(np.linalg.cond(Am))})
                records.append(row)
                print("GE19_G1J m=%d j=%d certified=%s q_ub=%.8g"%(
                    args.mode,j,row["Az_continuous_invertible"],
                    row["q_neumann_upper"]),flush=True)
                r7._CANONICAL_LOCAL_CACHE.clear()
        finally:
            r7._bg_point=orig_cb
            r7._CANONICAL_LOCAL_CACHE=orig_cache
    complete=all(r["Az_continuous_invertible"] for r in records)
    full=(complete and args.start_interval==0 and
          args.interval_count==nt-1)
    report={
      "classification":(
        "GE19_G1J_FIXED_INPUT_ACTION_OPERATOR_FULL_INTERVAL_AZ_NEUMANN_ENCLOSURE_PASS_Z11_OPEN"
        if full else
        "GE19_G1J_FIXED_INPUT_ACTION_OPERATOR_SUBDOMAIN_NEUMANN_PASS_FULL_G1_OPEN"
        if complete else
        "GE19_G1J_AZ_INTERVAL_NEUMANN_INCONCLUSIVE_SUBDOMAIN_G1_OPEN"),
      "scope":{"tag":args.tag,"grid":args.grid,"Nt":nt,"m":args.mode,
               "k_binary64":k,"interval_start":args.start_interval,
               "interval_count":args.interval_count,
               "total_required_original_intervals":nt-1,
               "precision_decimal_digits":args.dps,
               "source":"unchanged original GE06+GE07+Lambda plus analytic Repair13 D15a continuation",
               "source_background_constants":"original stored float64 median I0 and Lambda treated as exact input constants",
               "Noether_Az_columns_original":list(ZIDX),
               "Noether_Az_rows_original":"pS,pu,pphi,pT,dust density, anisotropy GE06+GE07"},
      "input_source_locks":pins,"selftest":tests,
      "all_selected_intervals_Az_invertible":complete,
      "all_original_intervals_Az_invertible":full,
      "interval_records":records,
      "proof":"Outward-rounded mpmath.iv on complete x boxes in the exact original c1 symbolic action partials; scalar-charge Exp branch bracketed by monotone dyadic bisection; fixed approximate R treated as an exact complex binary64 preconditioner, q=||I-R Az(I)||inf<1 implies invertibility at every x and ||Az^-1||inf<=||R||inf/(1-q). Derived WY, WR, M and F induced inf-norm upper bounds follow from the original canonical block formulas, not from pointwise samples.",
      "physics_scope_limits":"Algebraic action proof for fixed binary64 background physical parameters and exact symbolic coefficients only. Actual source-generation/bath error, floating parent uncertainty and true IVP trajectory error not enclosed. No full first-order Euler residual/boundary audit; no original G3 budget or H4 Ward.",
      "GE05_true_source_error_enclosed":False,
      "original_Z11_continuous_numerical_error_enclosed":False,
      "G1_PHYSICAL_CLOSED":False,"G3_B_total_frozen":False,
      "full_H4_Ward_certified":False,"Z21_certified":False,
      "lensing_licensed":False}
    args.json_out.parent.mkdir(parents=True,exist_ok=True)
    args.json_out.write_text(json.dumps(report,indent=2,sort_keys=True,
                                        allow_nan=False)+"\n")
    print(report["classification"],flush=True)

if __name__=="__main__":
    main()
