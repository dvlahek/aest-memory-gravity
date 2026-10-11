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

from ge19 import \
    repair07_window_retarded_reduced_h3_z20_particular as r7
from ge19 import \
    repair31_repair30_h2_dictionary_monitor_audit as r31

ROOT=Path(__file__).resolve().parents[1]
RD=ROOT/"results"

PRE=ROOT/"ge19/h4f3d12r6_predata_matched_x10_physical_hermite_enclosure.json"

PRE_CLASS=(
    "GE19_H4F3D12R6_PREDATA_MATCHED_X10_PHYSICAL_HERMITE_ARB"
)

BITS=192
NSPLIT=64
TINY=1e-300

ctx.prec=BITS


def require(v,msg):
    if not v:
        raise RuntimeError(msg)


def sha256(p):
    h=hashlib.sha256()
    with Path(p).open("rb") as f:
        for b in iter(lambda:f.read(1<<20),b""):
            h.update(b)
    return h.hexdigest()


def git_blob(p):
    return subprocess.check_output(
        ["git","rev-parse","HEAD:"+p],
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
    return math.nextafter(
        float(v.upper()),
        math.inf
    )


def theta_ball(i,n):
    lo=fmpq(i,n)
    hi=fmpq(i+1,n)
    return arb(
        (lo+hi)/2,
        (hi-lo)/2
    )


def verify_predata(pre):
    require(
        pre["classification"]==PRE_CLASS,
        "wrong D12R6 predata"
    )

    require(
        subprocess.run(
            [
                "git","merge-base","--is-ancestor",
                pre["parent_HEAD"],"HEAD"
            ],
            cwd=ROOT
        ).returncode==0,
        "D12R6 parent not ancestor"
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
        "D12R6 frozen source changed"
    )

    art={}
    for name,item in pre["frozen_artifacts"].items():
        p=ROOT/item["path"]
        require(
            p.is_file(),
            f"missing D12R6 artifact {p}"
        )
        got=sha256(p)
        art[name]={
            "path":item["path"],
            "expected":item["sha256"],
            "observed":got,
            "exact":got==item["sha256"],
        }

    require(
        all(v["exact"] for v in art.values()),
        "D12R6 frozen artifact changed"
    )

    return src,art


def node_x10_and_dx(bg,st,dd,k):
    x=np.asarray(bg["x"],float)
    a=np.asarray(bg["a"],float)
    H=np.asarray(bg["H"],float)
    Q=np.asarray(bg["Q_action"],float)

    require(
        np.all(np.isfinite(H)) and np.all(H>0),
        "nonpositive/nonfinite H"
    )
    require(
        np.all(np.isfinite(a)) and np.all(a>0),
        "nonpositive/nonfinite a"
    )

    Qx=np.asarray(
        PchipInterpolator(
            x,Q,
            extrapolate=False
        ).derivative()(x),
        float
    )

    u=np.asarray(st[2],complex)
    phi=np.asarray(st[3],complex)

    udot=np.asarray(dd[1],complex)
    phidot=np.asarray(dd[2],complex)

    ik=1j*float(k)

    g=Q*u + ik*phi/a

    gx=(
        Qx*u
        + Q*(udot/H)
        + ik/a*(phidot/H - phi)
    )

    require(
        np.all(np.isfinite(g))
        and np.all(np.isfinite(gx)),
        "nonfinite X10 node data"
    )

    return g,gx,Qx


def hermite_mode_bound(x,g,gx):
    max_g=0.0
    max_gx=0.0

    worst_g=None
    worst_gx=None

    max_endpoint_identity=0.0
    max_derivative_identity=0.0

    for j in range(len(x)-1):
        xa=float(x[j])
        xb=float(x[j+1])
        h=float(xb-xa)

        require(
            h>0,
            "nonpositive H3F clock interval"
        )

        hA=Afloat(h)

        f0=Cfloat(g[j])
        f1=Cfloat(g[j+1])

        d0=Cfloat(gx[j])
        d1=Cfloat(gx[j+1])

        # Hermite polynomial in theta in [0,1]:
        # f=c0+c1*t+c2*t^2+c3*t^3
        c0=f0
        c1=hA*d0
        c2=-3*f0-2*hA*d0+3*f1-hA*d1
        c3=2*f0+hA*d0-2*f1+hA*d1

        # Binary64 report-only algebraic endpoint checks.
        ff0=complex(g[j])
        ff1=complex(g[j+1])
        dd0=complex(gx[j])
        dd1=complex(gx[j+1])

        cf0=ff0
        cf1=(
            ff0
            + h*dd0
            + (-3*ff0-2*h*dd0+3*ff1-h*dd1)
            + (2*ff0+h*dd0-2*ff1+h*dd1)
        )

        cd0=dd0
        cd1=(
            h*dd0
            + 2*(-3*ff0-2*h*dd0+3*ff1-h*dd1)
            + 3*(2*ff0+h*dd0-2*ff1+h*dd1)
        )/h

        max_endpoint_identity=max(
            max_endpoint_identity,
            abs(cf0-ff0),
            abs(cf1-ff1),
        )

        max_derivative_identity=max(
            max_derivative_identity,
            abs(cd0-dd0),
            abs(cd1-dd1),
        )

        for ii in range(NSPLIT):
            t=theta_ball(ii,NSPLIT)

            f=(
                c0
                + c1*t
                + c2*t*t
                + c3*t*t*t
            )

            fx=(
                c1
                + 2*c2*t
                + 3*c3*t*t
            )/hA

            fu=upper_float(abs(f))
            fxu=upper_float(abs(fx))

            if fu>max_g:
                max_g=fu
                worst_g={
                    "step":j,
                    "subsegment":ii,
                    "xa":
                        xa+(xb-xa)*ii/NSPLIT,
                    "xb":
                        xa+(xb-xa)*(ii+1)/NSPLIT,
                    "upper":fu,
                }

            if fxu>max_gx:
                max_gx=fxu
                worst_gx={
                    "step":j,
                    "subsegment":ii,
                    "xa":
                        xa+(xb-xa)*ii/NSPLIT,
                    "xb":
                        xa+(xb-xa)*(ii+1)/NSPLIT,
                    "upper":fxu,
                }

    require(
        max_endpoint_identity <= 1e-18,
        f"Hermite endpoint identity fail {max_endpoint_identity}"
    )

    # This is only binary64 construction verification.
    require(
        max_derivative_identity <= 1e-14,
        f"Hermite derivative identity fail {max_derivative_identity}"
    )

    return {
        "mode_M0_sup_abs_X10_upper":
            max_g,

        "mode_L0_sup_abs_dX10_dx_upper":
            max_gx,

        "max_binary64_endpoint_identity_abs":
            max_endpoint_identity,

        "max_binary64_derivative_identity_abs":
            max_derivative_identity,

        "worst_X10":
            worst_g,

        "worst_dX10_dx":
            worst_gx,
    }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--json-out",required=True)
    args=ap.parse_args()

    out=Path(args.json_out).resolve()

    require(
        not out.exists(),
        "D12R6 output exists; no overwrite"
    )

    pre=json.loads(PRE.read_text())

    src_audit,art_audit=verify_predata(pre)

    h3fj=json.loads(
        (
            RD /
            "ge19_h3f_corrected_y_z20_science_reclosure.json"
        ).read_text()
    )

    require(
        h3fj["classification"] ==
        "GE19_H3F_CORRECTED_Y_H3_Z20_CERTIFIED",
        "H3F parent not certified"
    )

    d4=json.loads(
        (
            RD /
            "ge19_h4f3d12r4r1_y_spatial_zeroset_structural_repair.json"
        ).read_text()
    )

    require(
        d4["Y_lower_regularity_route_selected"] is True,
        "D12R4R1 lower-regularity route missing"
    )

    d5=json.loads(
        (
            RD /
            "ge19_h4f3d12r5r1_continuous_x11_collocation_enclosure.json"
        ).read_text()
    )

    require(
        d5["Y_M1_L1_collocation_certified"] is True,
        "D12R5R1 M1/L1 missing"
    )

    bgs,bases,mod6,mod7,bgdiag = \
        r31.build_operator_context(RD)

    h3fn=(
        RD /
        "ge19_h3f_corrected_y_z20_science_reclosure.npz"
    )

    mode_rows=[]
    case_rows=[]

    global_M0=0.0
    global_L0=0.0

    with np.load(
        h3fn,
        allow_pickle=False
    ) as z:

        for nt,label in (
            (128,"primary"),
            (64,"control"),
        ):
            x=np.asarray(
                z["x_"+label],
                float
            )

            for tag in r7.C_TAGS:
                bg=bgs[(nt,tag)]

                require(
                    np.array_equal(
                        x,
                        np.asarray(bg["x"],float)
                    ),
                    f"H3F/background x mismatch "
                    f"{tag} {label}"
                )

                per=[]

                for im,m in enumerate(r7.FOURIER_N):
                    m=int(m)

                    k=float(
                        m*r7.g9.K_REQ[0] /
                        r7.FOURIER_N[0]
                    )

                    st=np.asarray(
                        z[f"{tag}_H1_{label}"][im],
                        complex
                    )

                    dd=np.asarray(
                        z[f"{tag}_H1dot_{label}"][im],
                        complex
                    )

                    require(
                        st.shape==(6,nt),
                        "bad H1 state shape"
                    )

                    require(
                        dd.shape==(4,nt),
                        "bad H1dot shape"
                    )

                    g,gx,Qx = node_x10_and_dx(
                        bg,st,dd,k
                    )

                    q=hermite_mode_bound(
                        x,g,gx
                    )

                    q.update({
                        "Nt":nt,
                        "grid":label,
                        "C":tag,
                        "mode":m,
                        "k_Mpc_inv":k,
                        "node_max_abs_X10_report_only":
                            float(np.max(np.abs(g))),
                        "node_max_abs_dX10_dx_report_only":
                            float(np.max(np.abs(gx))),
                        "node_max_abs_Qx_report_only":
                            float(np.max(np.abs(Qx))),
                    })

                    per.append(q)
                    mode_rows.append(q)

                # Real-valued field from positive modes + conjugates.
                M0=2.0*sum(
                    q["mode_M0_sup_abs_X10_upper"]
                    for q in per
                )

                L0=2.0*sum(
                    q["mode_L0_sup_abs_dX10_dx_upper"]
                    for q in per
                )

                case_rows.append({
                    "Nt":nt,
                    "grid":label,
                    "C":tag,
                    "positive_mode_count":len(per),
                    "realspace_M0_sup_abs_g10_upper":M0,
                    "realspace_L0_Lipschitz_dx_upper":L0,
                })

                global_M0=max(global_M0,M0)
                global_L0=max(global_L0,L0)

    require(
        len(mode_rows)==36,
        "expected 36 mode cases"
    )

    require(
        len(case_rows)==6,
        "expected six C x Nt cases"
    )

    require(
        math.isfinite(global_M0)
        and math.isfinite(global_L0)
        and global_M0>=0
        and global_L0>=0,
        "nonfinite global M0/L0"
    )

    M1=float(
        d5[
            "global_realspace_M1_sup_abs_g11_upper"
        ]
    )

    L1=float(
        d5[
            "global_realspace_L1_Lipschitz_dx_upper"
        ]
    )

    candidate_modulus = (
        2.0 * (
            M1*global_L0
            + global_M0*L1
        )
    )

    classification=(
        "GE19_H4F3D12R6_MATCHED_X10_PHYSICAL_HERMITE_ARB_PASS_"
        "Y_M0_L0_CERTIFIED_PHYSICAL_H1_CONTINUUM_ERROR_OPEN"
    )

    report={
        "classification":
            classification,

        "preregistration":
            PRE_CLASS,

        "execution_HEAD":
            subprocess.check_output(
                ["git","rev-parse","HEAD"],
                cwd=ROOT,text=True
            ).strip(),

        "frozen_source_audit":
            src_audit,

        "frozen_artifact_audit":
            art_audit,

        "arb_precision_bits":
            BITS,

        "subsegments_per_original_step":
            NSPLIT,

        "continuous_representation":
            "cubic physical Hermite interpolation of X10 "
            "using frozen H3F X10 and dX10/dx endpoints",

        "g10_definition":
            "g10 = Q_action*u10 + i*k*phi10/a",

        "dg10_dx_definition":
            "Q_x*u + Q*(udot/H) + "
            "i*k/a*(phidot/H-phi)",

        "realspace_bound_rule":
            "sup_chi |g| <= 2*sum_positive_modes |g_m|",

        "mode_rows":
            mode_rows,

        "case_rows":
            case_rows,

        "global_realspace_M0_sup_abs_g10_upper":
            global_M0,

        "global_realspace_L0_Lipschitz_dx_upper":
            global_L0,

        "inherited_M1_sup_abs_g11_upper":
            M1,

        "inherited_L1_Lipschitz_dx_upper":
            L1,

        "candidate_Y_lower_regularity_modulus_coefficient":
            candidate_modulus,

        "candidate_modulus_formula":
            "2*(M1*L0 + M0*L1)",

        "all_6_C_Nt_cases_certified":
            True,

        "all_18_C_beta_Nt_cohorts_covered_via_beta_invariance":
            True,

        "continuous_X10_physical_Hermite_representation_certified":
            True,

        "Y_M0_L0_numerical_representation_certified":
            True,

        "continuous_physical_H1_solution_error_enclosed":
            False,

        "Y_M1_L1_inherited_certified":
            True,

        "Y_full_M0_M1_L0_L1_modulus_frozen":
            False,

        "candidate_full_Ward_residual_read":
            False,

        "B_total_defined":
            False,

        "full_Ward_execution_licensed":
            False,

        "full_original_H4_Ward_certified":
            False,

        "Z21_certified":
            False,

        "lensing_licensed":
            False,

        "threshold_changed":
            False,

        "source_coefficients_changed":
            False,

        "observational_tuning":
            False,

        "next_route":
            "ARTIFACT_ONLY_FREEZE_Y_LOWER_REGULARITY_MODULUS_"
            "2_TIMES_M1L0_PLUS_M0L1",

        "claim_boundary":
            "D12R6 rigorously bounds the chosen continuous physical-Hermite "
            "representation of the already-certified frozen H1 parent and "
            "provides numerical-representation M0/L0 bounds for X10 over "
            "all C x Nt cases. It does not create a new rigorous error "
            "enclosure between frozen H1 and the exact continuum H1 solution. "
            "No full H4 Ward residual, B_total, Z21 or observation is read."
    }

    out.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    out.write_text(
        json.dumps(
            report,
            indent=2,
            sort_keys=True,
            allow_nan=False
        )+"\n"
    )

    print("CLASSIFICATION =",classification)
    print("CASES =",len(case_rows))
    print("MODE_CASES =",len(mode_rows))
    print("M0_G10 =",f"{global_M0:.16e}")
    print("L0_G10_DX =",f"{global_L0:.16e}")
    print("M1_G11 =",f"{M1:.16e}")
    print("L1_G11_DX =",f"{L1:.16e}")
    print(
        "Y_MODULUS_CANDIDATE =",
        f"{candidate_modulus:.16e}"
    )
    print("PHYSICAL_H1_ERROR_ENCLOSED = False")
    print("FULL_WARD = False")
    print(
        "GE19_H4F3D12R6_MATCHED_X10_PHYSICAL_HERMITE_ARB_PASS"
    )


if __name__=="__main__":
    main()
