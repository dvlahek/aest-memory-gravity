#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import math
import subprocess
from pathlib import Path

import numpy as np

from ge19 import repair07_window_retarded_reduced_h3_z20_particular as r7
from ge19 import repair11_lambda_inclusive_reduced_h1_reclosure as r11
from ge19 import repair13_self_consistent_reduced_background_h1_reclosure as r13
from ge19 import repair24_q20_construction as r24
from ge19 import repair27_cancellation_free_parent_q20_reconstruction as r27
from nl1c4 import expanding_memory_source_trajectory as c4

ROOT=Path.home()/"aest-memory-gravity"
RD=ROOT/"results"
OUT=RD/"failure_aware_defect"
OUT.mkdir(parents=True,exist_ok=True)

BASE_SCIENCE_HEAD="6282ed54e35d4db6b58fcd13d1c7403419f8afb7"
EXPECTED_BRANCH="numerics/failure-aware-defect-certification"

R13=RD/"ge19_repair13_self_consistent_reduced_background_h1_reclosure.npz"
R22=RD/"ge19_repair22_on_shell_parent_z20_certification.npz"
R13_SHA="011c0ae54fd21d70c0e2c695ce62e7b74a3c5529a07c9023c882a447d5b40ca3"
R22_SHA="3020e0d040f902ab2609e05705f4508d9919665b1344fa0e641644ea8fc41a16"

NT=64
TAG="C_min"
MODE=20
NQ=1024
TSTAR=255.0/256.0
RSTAR=math.tan(0.5*math.pi*TSTAR)

JOUT=OUT/"ge19_d12r12b2c2a_regularized_b10x_uv_boundary_diagnostic.json"
NOUT=OUT/"ge19_d12r12b2c2a_regularized_b10x_uv_boundary_diagnostic.npz"


def sha256(p):
    h=hashlib.sha256()
    with Path(p).open("rb") as f:
        for b in iter(lambda:f.read(1<<20),b""):
            h.update(b)
    return h.hexdigest()


def git(*args):
    return subprocess.check_output(["git",*args],cwd=ROOT,text=True).strip()


def require(cond,msg):
    if not cond:
        raise RuntimeError(msg)


def find_trace():
    for p in RD.rglob("ge19_repair26_R1_full_history_trace.dat"):
        if p.is_file() and p.stat().st_size==int(r27.REPAIR26_R1_TRACE_BYTES) and sha256(p)==r27.REPAIR26_R1_TRACE_SHA:
            return p
    for p in RD.rglob("*repair26*trace*.dat"):
        if p.is_file() and p.stat().st_size==int(r27.REPAIR26_R1_TRACE_BYTES) and sha256(p)==r27.REPAIR26_R1_TRACE_SHA:
            return p
    raise RuntimeError("FROZEN_REPAIR26_TRACE_NOT_FOUND")


head=git("rev-parse","HEAD")
branch=git("branch","--show-current")
require(
    subprocess.call(["git","merge-base","--is-ancestor",BASE_SCIENCE_HEAD,head],cwd=ROOT)==0,
    f"BASE_SCIENCE_HEAD_NOT_ANCESTOR {BASE_SCIENCE_HEAD} {head}",
)
require(branch==EXPECTED_BRANCH,f"BRANCH_FAIL {branch}")

for p,h in ((R13,R13_SHA),(R22,R22_SHA)):
    require(p.is_file(),f"MISSING {p}")
    got=sha256(p)
    require(got==h,f"SHA_FAIL {p.name} {got}")

r24.TRACE_LO_A=float(r27.REPAIR26_TRACE_LO_A)
r24.TRACE_HI_A=float(r27.REPAIR26_TRACE_HI_A)
trace=find_trace()

with np.load(R13,allow_pickle=False) as r13n, np.load(R22,allow_pickle=False) as r22:
    bgs,_=r24.reconstruct_backgrounds(r7,r11,r13,RD,r13n)
    bg=bgs[(NT,TAG)]
    h1=np.asarray(r22[f"{TAG}_H1_control"],complex)
    require(h1.shape==(6,6,NT),f"H1_SHAPE_FAIL {h1.shape}")
    Xall=r24.first_order_X_modes(r7,bg,h1)

boundary=r24.full_history_boundary(c4,r7,trace,NQ)
r=np.asarray(boundary["r"],float)
w=np.asarray(boundary["w"],float)
z0all=np.asarray(boundary["z0"],complex)
v0all=np.asarray(boundary["v0"],complex)
require(z0all.shape==(NQ,6),f"Z0_SHAPE_FAIL {z0all.shape}")
require(v0all.shape==(NQ,6),f"V0_SHAPE_FAIL {v0all.shape}")

modes=list(map(int,r7.FOURIER_N))
im=modes.index(MODE)
X=np.asarray(Xall[im],complex)
x=np.asarray(bg["x"],float)
hgrid=np.asarray(bg["H"],float)*float(r24.TAUH0/r7.g9.H0_CLASS)

dx=float(x[1]-x[0])
hm=math.sqrt(float(hgrid[0]*hgrid[1]))
dxi=dx/hm
Xs=complex((X[1]-X[0])/dxi)

z0=np.asarray(z0all[:,im],complex)
v0=np.asarray(v0all[:,im],complex)

# Regularized variables.
u0=z0-complex(X[0])
us0=v0-Xs
p0=v0/(r*r)
q0=us0/(r*r)
Eq=(r*r)*np.abs(u0)**2+(r**4)*np.abs(q0)**2
sqrtEq=np.sqrt(Eq)

uv=(r>=RSTAR)
require(np.any(uv),"UV_EMPTY")
ruv=r[uv]
wuv=w[uv]
uuv=np.abs(u0[uv])
usuv=np.abs(us0[uv])
puv=np.abs(p0[uv])
quv=np.abs(q0[uv])
Euv=sqrtEq[uv]

tail_count=min(64,len(ruv))
rt=ruv[-tail_count:]

def slope(y):
    y=np.asarray(y[-tail_count:],float)
    mask=np.isfinite(y)&(y>0)&np.isfinite(rt)&(rt>0)
    if np.sum(mask)<4:
        return math.nan
    return float(np.polyfit(np.log(rt[mask]),np.log(y[mask]),1)[0])

slope_u=slope(uuv)
slope_us=slope(usuv)
slope_p=slope(puv)
slope_q=slope(quv)
slope_E=slope(Euv)

abs_B10x_uv_finite_proxy=float(np.sum(np.abs(wuv)*usuv/hm))
naive_v_max=float(np.max(np.abs(v0[uv])))
regularized_us_max=float(np.max(usuv))

last_rows=[]
for j in range(max(0,len(ruv)-12),len(ruv)):
    last_rows.append({
        "r":float(ruv[j]),
        "weight":float(wuv[j]),
        "abs_u":float(uuv[j]),
        "abs_v":float(abs(v0[uv][j])),
        "abs_u_s_v_minus_Xs":float(usuv[j]),
        "abs_p":float(puv[j]),
        "abs_q":float(quv[j]),
        "sqrt_Eq":float(Euv[j]),
    })

finite=bool(np.all(np.isfinite(Euv)) and np.all(np.isfinite(usuv)) and math.isfinite(abs_B10x_uv_finite_proxy))
regularized_route_promising=bool(
    finite and math.isfinite(slope_us) and math.isfinite(slope_E) and slope_us<0.75 and slope_E<0.75
)

classification=(
    "GE19_D12R12B2C2A_REGULARIZED_B10X_UV_BOUNDARY_DIAGNOSTIC_PASS_RIGOROUS_BOUNDARY_ENCLOSURE_REQUIRED"
    if finite else
    "GE19_D12R12B2C2A_REGULARIZED_B10X_UV_BOUNDARY_DIAGNOSTIC_FAIL"
)

report={
    "classification":classification,
    "git_HEAD":head,
    "base_science_HEAD":BASE_SCIENCE_HEAD,
    "branch":branch,
    "scope":"Nt64/C_min/m20 Nq1024 frozen Repair26 full-history boundary diagnostic",
    "Repair13_NPZ_SHA256":sha256(R13),
    "Repair22_NPZ_SHA256":sha256(R22),
    "Repair26_trace_SHA256":sha256(trace),
    "Nt":NT,
    "C":TAG,
    "mode":MODE,
    "Nq":NQ,
    "D55_t_star":TSTAR,
    "D55_r_star":RSTAR,
    "X0_abs":float(abs(X[0])),
    "first_step_Xs_abs":float(abs(Xs)),
    "first_step_h_mid":hm,
    "UV_node_count":int(np.sum(uv)),
    "UV_r_min":float(np.min(ruv)),
    "UV_r_max":float(np.max(ruv)),
    "high_r_tail_fit_count":tail_count,
    "high_r_loglog_slope_abs_u":slope_u,
    "high_r_loglog_slope_abs_us":slope_us,
    "high_r_loglog_slope_abs_p":slope_p,
    "high_r_loglog_slope_abs_q":slope_q,
    "high_r_loglog_slope_sqrt_Eq":slope_E,
    "UV_max_abs_v":naive_v_max,
    "UV_max_abs_v_minus_Xs":regularized_us_max,
    "UV_max_sqrt_Eq":float(np.max(Euv)),
    "finite_quadrature_absolute_B10x_UV_proxy":abs_B10x_uv_finite_proxy,
    "regularized_route_promising_report_only":regularized_route_promising,
    "all_outputs_finite":finite,
    "rigorous_continuum_boundary_enclosure":False,
    "B10_x_certified":False,
    "Z11_order2_certified":False,
    "GE06_direct_FD8_defect_certified":False,
    "GE07_direct_FD8_defect_certified":False,
    "B_total_defined":False,
    "full_H4_Ward_execution_licensed":False,
    "Z21_certified":False,
    "science_threshold_changed":False,
    "observational_tuning":False,
    "identity":{
        "u":"z-X",
        "q":"p-X_s/r^2",
        "u_s":"r^2 q = v-X_s",
        "q_s":"-3 h q-u-(X_ss+3 h X_s)/r^2",
        "energy":"E_q=r^2|u|^2+r^4|q|^2",
        "energy_inequality":"d sqrt(E_q)/ds <= |X_ss+3 h X_s|",
    },
    "claim_boundary":(
        "Finite Repair24 quadrature diagnostic only. It does not infer a continuum bound from quadrature "
        "convergence and does not certify B10_x. Extreme-UV growth of r|u| must be handled explicitly "
        "before any uniform-E_q promotion."
    ),
    "last_UV_nodes":last_rows,
}

np.savez_compressed(NOUT,r=r,w=w,uv_mask=uv,u0=u0,us0=us0,p0=p0,q0=q0,sqrt_Eq=sqrtEq)
report["NPZ_SHA256"]=sha256(NOUT)
JOUT.write_text(json.dumps(report,indent=2,sort_keys=True,allow_nan=False)+"\n")

print("B2C2A_CLASSIFICATION =",classification)
print("B2C2A_SLOPE_U =",f"{slope_u:.17e}")
print("B2C2A_SLOPE_US =",f"{slope_us:.17e}")
print("B2C2A_SLOPE_P =",f"{slope_p:.17e}")
print("B2C2A_SLOPE_Q =",f"{slope_q:.17e}")
print("B2C2A_SLOPE_SQRT_EQ =",f"{slope_E:.17e}")
print("B2C2A_FINITE_QUAD_ABS_B10X_UV_PROXY =",f"{abs_B10x_uv_finite_proxy:.17e}")
print("B2C2A_REGULARIZED_ROUTE_PROMISING_REPORT_ONLY =",regularized_route_promising)
print("B2C2A_JSON_SHA256 =",sha256(JOUT))
print("B2C2A_NPZ_SHA256 =",sha256(NOUT))

if not finite:
    raise SystemExit(2)
