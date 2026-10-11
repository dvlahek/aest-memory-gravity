#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import math
import subprocess
from pathlib import Path

import numpy as np
from scipy.interpolate import PchipInterpolator
from flint import arb, acb, ctx, fmpq

from ge19 import repair07_window_retarded_reduced_h3_z20_particular as r7
from ge19 import repair31_repair30_h2_dictionary_monitor_audit as r31
from ge19 import repair32b_factor2_corrected_reduced_h2_z11_reconstruction as r32b

ROOT=Path(__file__).resolve().parents[1]
RD=ROOT/"results"

PRE=ROOT/"ge19/h4f3d12r5_predata_continuous_x11_collocation_enclosure.json"

PRE_CLASS=(
    "GE19_H4F3D12R5_PREDATA_CONTINUOUS_X11_COLLOCATION_ARB_ENCLOSURE"
)

CTX_BITS=192
NSPLIT=64
REPLAY_MAX=5e-13
TINY=1e-300

ctx.prec=CTX_BITS


def require(v,msg):
    if not v:
        raise RuntimeError(msg)


def sha256(p):
    h=hashlib.sha256()
    with Path(p).open("rb") as f:
        for b in iter(lambda:f.read(1<<20),b""):
            h.update(b)
    return h.hexdigest()


def git_blob(path):
    return subprocess.check_output(
        ["git","rev-parse","HEAD:"+path],
        cwd=ROOT,text=True
    ).strip()


def exact_q(v):
    n,d=float(v).as_integer_ratio()
    return fmpq(n,d)


def Afloat(v):
    return arb(exact_q(float(v)))


def Cfloat(v):
    z=complex(v)
    return acb(Afloat(z.real),Afloat(z.imag))


def upper_float(v):
    return math.nextafter(float(v.upper()),math.inf)


def theta_ball(i,n):
    lo=fmpq(i,n)
    hi=fmpq(i+1,n)
    return arb((lo+hi)/2,(hi-lo)/2)


def rel_l2(a,b):
    aa=np.asarray(a)
    bb=np.asarray(b)
    return float(
        np.linalg.norm(aa-bb) /
        max(np.linalg.norm(aa),np.linalg.norm(bb),TINY)
    )


def pchip_ball(c,dx):
    c0,c1,c2,c3=[Afloat(v) for v in c]
    val=((c0*dx+c1)*dx+c2)*dx+c3
    der=(3*c0*dx+2*c1)*dx+c2
    return val,der


def verify_predata(pre):
    require(pre["classification"]==PRE_CLASS,"wrong D12R5 predata")

    branch=subprocess.check_output(
        ["git","branch","--show-current"],
        cwd=ROOT,text=True
    ).strip()

    require(
        branch=="physics-first-gravitational-elasticity",
        "wrong branch"
    )

    require(
        subprocess.run(
            ["git","merge-base","--is-ancestor",
             pre["parent_HEAD"],"HEAD"],
            cwd=ROOT
        ).returncode==0,
        "D12R5 prereg parent is not ancestor"
    )

    src={}
    for name,item in pre["frozen_git_blobs"].items():
        got=git_blob(item["path"])
        src[name]={
            "path":item["path"],
            "expected":item["blob"],
            "observed":got,
            "exact":got==item["blob"],
        }

    require(
        all(v["exact"] for v in src.values()),
        "D12R5 frozen source changed"
    )

    art={}
    for name,item in pre["frozen_artifacts"].items():
        p=ROOT/item["path"]
        require(p.is_file(),f"missing artifact {p}")
        got=sha256(p)
        art[name]={
            "path":item["path"],
            "expected":item["sha256"],
            "observed":got,
            "exact":got==item["sha256"],
        }

    require(
        all(v["exact"] for v in art.values()),
        "D12R5 frozen artifact changed"
    )

    return src,art


def canonical_nodes(z,tag,label,im):
    st=np.asarray(z[f"{tag}_Z11_{label}"][im],complex)
    dd=np.asarray(z[f"{tag}_Z11dot_{label}"][im],complex)

    require(st.shape[0]==6,"bad Z11 field shape")
    require(dd.shape[0]==4,"bad Z11dot shape")
    require(st.shape[1]==dd.shape[1],"Z11 clock mismatch")

    return np.vstack([st[1:5],dd])


def radau_step(mod6,mod7,bg,tag,k,x,source_mode,yn,j):
    a11=5.0/12.0
    a12=-1.0/12.0
    a21=3.0/4.0
    a22=1.0/4.0
    b1=3.0/4.0
    b2=1.0/4.0
    c1=1.0/3.0

    xa=float(x[j])
    xb=float(x[j+1])
    h=float(xb-xa)

    x1=float(xa+c1*h)
    x2=xb

    M1,Fmap1,*_=r7._canonical_operator_matrices(
        mod6,mod7,bg,tag,k,x1
    )
    M2,Fmap2,*_=r7._canonical_operator_matrices(
        mod6,mod7,bg,tag,k,x2
    )

    rhsfun,confun=r32b.source_interp(x,source_mode)

    R1=np.asarray(rhsfun(x1),complex)
    R2=np.asarray(rhsfun(x2),complex)
    C1=np.asarray(confun(x1),complex)
    C2=np.asarray(confun(x2),complex)

    if R1.ndim==1: R1=R1[:,None]
    if R2.ndim==1: R2=R2[:,None]
    if C1.ndim==1: C1=C1[:,None]
    if C2.ndim==1: C2=C2[:,None]

    F1=Fmap1@np.vstack([R1,C1])
    F2=Fmap2@np.vstack([R2,C2])

    ya=np.asarray(yn[:,j],complex)[:,None]

    I=np.eye(8,dtype=complex)

    K=np.block([
        [I-h*a11*M1,-h*a12*M2],
        [-h*a21*M1,I-h*a22*M2],
    ])

    RHS=np.vstack([
        ya+h*(a11*F1+a12*F2),
        ya+h*(a21*F1+a22*F2),
    ])

    stages,diag=r7._dense_equilibrated_solve(K,RHS)
    stages=np.asarray(stages,complex)

    Y1=stages[:8]
    Y2=stages[8:]

    G1=M1@Y1+F1
    G2=M2@Y2+F2

    P0=ya[:,0]
    P1=h*(1.5*G1[:,0]-0.5*G2[:,0])
    P2=h*(-0.75*G1[:,0]+0.75*G2[:,0])

    yraw=P0+P1+P2
    yb=np.asarray(yn[:,j+1],complex)

    replay=rel_l2(yraw,yb)

    return (
        P0,P1,P2,yb,replay,
        float(diag["scaled_relative_L2_residual_max"])
    )


def mode_bounds(mod6,mod7,bg,tag,x,source_mode,yn,k):
    qp=PchipInterpolator(
        x,np.asarray(bg["Q_action"],float),
        extrapolate=False
    )
    ap=PchipInterpolator(
        x,np.asarray(bg["a"],float),
        extrapolate=False
    )

    require(np.array_equal(np.asarray(qp.x,float),x),"Q PCHIP grid mismatch")
    require(np.array_equal(np.asarray(ap.x,float),x),"a PCHIP grid mismatch")

    gmax=0.0
    gxmax=0.0
    replay_max=0.0
    stage_max=0.0
    stitch_max=0.0

    worst_g=None
    worst_gx=None

    for j in range(len(x)-1):
        P0,P1,P2,yb,replay,stage_res=radau_step(
            mod6,mod7,bg,tag,k,x,source_mode,yn,j
        )

        replay_max=max(replay_max,replay)
        stage_max=max(stage_max,stage_res)

        require(
            replay<=REPLAY_MAX,
            f"Radau endpoint replay fail C={tag} k={k} "
            f"step={j} replay={replay}"
        )

        xa=float(x[j])
        xb=float(x[j+1])

        xaA=Afloat(xa)
        xbA=Afloat(xb)
        widthA=xbA-xaA

        require(widthA>0,"nonpositive clock interval")

        p0=[Cfloat(v) for v in P0]
        p1=[Cfloat(v) for v in P1]
        p2=[Cfloat(v) for v in P2]

        # Exact Arb endpoint stitch:
        # pc(0)=archived left node and pc(1)=archived right node.
        jump=[
            Cfloat(yb[r])-p0[r]-p1[r]-p2[r]
            for r in range(8)
        ]
        p1c=[p1[r]+jump[r] for r in range(8)]

        stitch_max=max(
            stitch_max,
            max(upper_float(abs(v)) for v in jump)
        )

        ik=acb(0,Afloat(k))

        for ii in range(NSPLIT):
            th=theta_ball(ii,NSPLIT)
            dx=widthA*th

            QI,QxI=pchip_ball(qp.c[:,j],dx)
            aI,axI=pchip_ball(ap.c[:,j],dx)

            require(
                aI.lower()>0,
                f"a interval contains nonpositive value C={tag} step={j}"
            )

            u=(
                p0[1] +
                p1c[1]*th +
                p2[1]*th*th
            )
            phi=(
                p0[2] +
                p1c[2]*th +
                p2[2]*th*th
            )

            ux=(p1c[1]+2*p2[1]*th)/widthA
            phix=(p1c[2]+2*p2[2]*th)/widthA

            g=acb(QI)*u + ik*phi/aI

            gx=(
                acb(QxI)*u +
                acb(QI)*ux +
                ik*(
                    phix/aI -
                    phi*axI/(aI*aI)
                )
            )

            gu=upper_float(abs(g))
            gxu=upper_float(abs(gx))

            if gu>gmax:
                gmax=gu
                worst_g={
                    "step":j,
                    "subsegment":ii,
                    "xa":xa+(xb-xa)*ii/NSPLIT,
                    "xb":xa+(xb-xa)*(ii+1)/NSPLIT,
                    "upper":gu,
                }

            if gxu>gxmax:
                gxmax=gxu
                worst_gx={
                    "step":j,
                    "subsegment":ii,
                    "xa":xa+(xb-xa)*ii/NSPLIT,
                    "xb":xa+(xb-xa)*(ii+1)/NSPLIT,
                    "upper":gxu,
                }

    return {
        "mode_g11_abs_upper":gmax,
        "mode_dg11_dx_abs_upper":gxmax,
        "max_endpoint_replay_relative":replay_max,
        "max_Radau_stage_scaled_relative_L2_residual":stage_max,
        "max_endpoint_stitch_abs":stitch_max,
        "worst_g11":worst_g,
        "worst_dg11_dx":worst_gx,
    }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--json-out",required=True)
    args=ap.parse_args()

    out=Path(args.json_out).resolve()

    require(not out.exists(),"D12R5 output exists; no overwrite")

    pre=json.loads(PRE.read_text())
    src_audit,art_audit=verify_predata(pre)

    cert=json.loads(
        (RD/"ge19_repair32c_artifact_only_reduced_z11_certification.json")
        .read_text()
    )

    require(
        cert["classification"] ==
        "GE19_REPAIR32C_ARTIFACT_ONLY_REDUCED_Z11_CERTIFICATION_PASS",
        "Repair32C Z11 certificate missing"
    )
    require(cert["Z11_certified"] is True,"Z11 not certified")

    d4=json.loads(
        (RD/"ge19_h4f3d12r4r1_y_spatial_zeroset_structural_repair.json")
        .read_text()
    )

    require(
        d4["classification"] ==
        "GE19_H4F3D12R4R1_Y_SPATIAL_ZEROSET_"
        "STRUCTURAL_PASS_LOWER_REGULARITY_REQUIRED",
        "D12R4R1 lower-regularity route missing"
    )
    require(
        d4["Y_lower_regularity_route_selected"] is True,
        "D12R4R1 did not select lower regularity"
    )

    bgs,bases,mod6,mod7,bgdiag=r31.build_operator_context(RD)

    zpath=RD/"ge19_repair32b_factor2_corrected_reduced_h2_z11_reconstruction.npz"

    rows=[]
    case_rows=[]

    global_M1=0.0
    global_L1=0.0
    global_replay=0.0
    global_stitch=0.0
    global_stage=0.0

    with np.load(zpath,allow_pickle=False) as z:
        for nt,label in ((128,"primary"),(64,"control")):
            x=np.asarray(z["x_"+label],float)

            for tag in r7.C_TAGS:
                bg=bgs[(nt,tag)]

                require(
                    np.array_equal(x,np.asarray(bg["x"],float)),
                    f"clock mismatch Nt={nt} C={tag}"
                )

                per_mode=[]

                for im,m in enumerate(r7.FOURIER_N):
                    m=int(m)
                    k=float(
                        m*r7.g9.K_REQ[0] /
                        r7.FOURIER_N[0]
                    )

                    yn=canonical_nodes(z,tag,label,im)

                    source_mode=np.asarray(
                        z[f"{tag}_M1_rhs_{label}"][im],
                        complex
                    )

                    q=mode_bounds(
                        mod6,mod7,bg,tag,x,
                        source_mode,yn,k
                    )

                    q.update({
                        "Nt":nt,
                        "grid":label,
                        "C":tag,
                        "mode":m,
                        "k_Mpc_inv":k,
                    })

                    per_mode.append(q)
                    rows.append(q)

                    global_replay=max(
                        global_replay,
                        q["max_endpoint_replay_relative"]
                    )
                    global_stitch=max(
                        global_stitch,
                        q["max_endpoint_stitch_abs"]
                    )
                    global_stage=max(
                        global_stage,
                        q["max_Radau_stage_scaled_relative_L2_residual"]
                    )

                # Real field reconstructed from positive modes plus conjugates.
                M1=2.0*sum(
                    q["mode_g11_abs_upper"]
                    for q in per_mode
                )

                L1=2.0*sum(
                    q["mode_dg11_dx_abs_upper"]
                    for q in per_mode
                )

                case={
                    "Nt":nt,
                    "grid":label,
                    "C":tag,
                    "positive_mode_count":len(per_mode),
                    "realspace_M1_sup_abs_g11_upper":M1,
                    "realspace_L1_Lipschitz_dx_upper":L1,
                }

                case_rows.append(case)
                global_M1=max(global_M1,M1)
                global_L1=max(global_L1,L1)

    require(len(case_rows)==6,"expected six C x Nt cases")
    require(len(rows)==36,"expected 36 mode cases")

    finite=all(
        math.isfinite(v) and v>=0
        for v in (
            global_M1,
            global_L1,
            global_replay,
            global_stitch,
            global_stage,
        )
    )

    passed=bool(
        finite and
        global_replay<=REPLAY_MAX
    )

    classification=(
        "GE19_H4F3D12R5_CONTINUOUS_X11_COLLOCATION_ARB_PASS_"
        "Y_M1_L1_CERTIFIED_PHYSICAL_H2_ERROR_OPEN"
        if passed else
        "GE19_H4F3D12R5_CONTINUOUS_X11_COLLOCATION_ARB_FAIL"
    )

    report={
        "classification":classification,
        "preregistration":PRE_CLASS,
        "execution_HEAD":subprocess.check_output(
            ["git","rev-parse","HEAD"],
            cwd=ROOT,text=True
        ).strip(),

        "frozen_source_audit":src_audit,
        "frozen_artifact_audit":art_audit,

        "arb_precision_bits":CTX_BITS,
        "subsegments_per_Radau_step":NSPLIT,
        "endpoint_replay_gate":REPLAY_MAX,

        "canonical_state":
            "y=(S,u,phi,T,Sdot,udot,phidot,Tdot)",

        "continuous_representation":
            "endpoint-stitched quadratic Radau-2 polynomial "
            "on each original Repair32B step",

        "background_representation":
            "exact Arb evaluation of frozen binary64 PCHIP "
            "Q_action and a coefficients",

        "g11_definition":
            "g11 = Q_action*u11 + i*k*phi11/a",

        "dg11_dx_definition":
            "Q_x*u + Q*u_x + i*k*(phi_x/a-phi*a_x/a^2)",

        "realspace_bound_rule":
            "For positive Fourier modes with conjugate completion, "
            "sup_chi |g| <= 2*sum_m |g_m|.",

        "mode_rows":rows,
        "case_rows":case_rows,

        "global_realspace_M1_sup_abs_g11_upper":
            global_M1,

        "global_realspace_L1_Lipschitz_dx_upper":
            global_L1,

        "max_endpoint_replay_relative":
            global_replay,

        "max_endpoint_stitch_abs":
            global_stitch,

        "max_Radau_stage_scaled_relative_L2_residual":
            global_stage,

        "all_6_C_Nt_cases_certified":passed,
        "all_18_C_beta_Nt_cohorts_covered_via_beta_invariance":passed,

        "continuous_X11_collocation_representation_certified":passed,
        "Y_M1_L1_collocation_certified":passed,

        "continuous_physical_H2_solution_error_enclosed":False,

        "Y_M0_L0_certified":False,
        "Y_full_M0_M1_L0_L1_modulus_certified":False,

        "candidate_full_Ward_residual_read":False,
        "B_total_defined":False,
        "full_Ward_execution_licensed":False,
        "full_original_H4_Ward_certified":False,
        "Z21_certified":False,
        "lensing_licensed":False,

        "threshold_changed":False,
        "source_coefficients_changed":False,
        "observational_tuning":False,

        "next_route":
            "CERTIFY_MATCHED_X10_M0_L0_THEN_FORM_"
            "Y_LOWER_REGULARITY_MODULUS_AND_KEEP_"
            "PHYSICAL_H2_ERROR_AS_SEPARATE_PARENT_UNCERTAINTY",

        "claim_boundary":
            "D12R5 rigorously encloses the continuous endpoint-stitched "
            "Radau representation of the already-certified frozen Z11 "
            "parent and provides real-space M1/L1 bounds for g11. "
            "It does not claim a new rigorous error bound between the "
            "Repair32B numerical state and the exact continuum H2 solution. "
            "No full Ward residual, B_total, Z21 or observation is evaluated."
    }

    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(
        json.dumps(report,indent=2,sort_keys=True,allow_nan=False)+"\n"
    )

    print("CLASSIFICATION =",classification)
    print("CASES =",len(case_rows))
    print("MODE_CASES =",len(rows))
    print("M1_G11 =",f"{global_M1:.16e}")
    print("L1_G11_DX =",f"{global_L1:.16e}")
    print("MAX_REPLAY =",f"{global_replay:.16e}")
    print("MAX_STITCH =",f"{global_stitch:.16e}")
    print("PHYSICAL_H2_ERROR_ENCLOSED = False")
    print("FULL_WARD = False")
    print("NEXT =",report["next_route"])

    if not passed:
        raise SystemExit(2)

    print("GE19_H4F3D12R5_CONTINUOUS_X11_COLLOCATION_ARB_PASS")


if __name__=="__main__":
    main()
