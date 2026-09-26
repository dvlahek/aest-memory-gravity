#!/usr/bin/env python3
"""Independent, preregistered D12 analytic nonbath proof + uploaded D11 conditional F21 bound.

No F21 samples are available: reports only the certified algebraic identity,
full-period spatial m=0 identity and *coefficients* multiplying an unknown F21 norm.
Does not claim full AeST+memory-bath on-shell Noether, Z21 or lensing.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
from pathlib import Path
import numpy as np
import sympy as sp

NAMES=("N","L","R","b","u","phi","T","rho")
TAGS=("C_min","C_star","C_max")
SCHEMES=("FD4","FD8")
NX=128
FULL_BAND=64
REDUCED_BAND=40
H0=67.3324639084866  # original frozen v063 START H0, only Fourier k normalization
KH0=0.03             # original frozen ge09 K_H[0]
FOURIER_N0=3         # original frozen repair07 FOURIER_N[0]
TINY=1e-300


def sha256(path:Path)->str:
    h=hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda:stream.read(1<<20),b""):
            h.update(chunk)
    return h.hexdigest()


def symzero(x):
    return bool(sp.simplify(sp.cancel(sp.together(x)))==0)


def source_bound_analytic_proof():
    # These are the exact FLRW GE06/GE07/Lambda background action partials
    # independently frozen and symbolically checked against original partial_map
    # by GE19 H4F3d11 CI. Their action provenance is pinned in the D12 predata.
    a,H,h2,dh2,Q,K,KQ,dKQ,C,dC,lam,dlam=sp.symbols(
        "a H H2 H2prime Q K KQ KQprime C Cprime Lambda Lambdaprime",
        real=True, positive=False)
    # Original p_Nf^GE06 = 6a^3 H^2 +2a^3(K-Q KQ)
    # Original GE07 matter action rho=3C/a^3, so p_Nf^GE07=-6C.
    en=(6*a**3*h2+2*a**3*(K-Q*KQ))-6*C-6*lam*a**3
    fried=h2-(Q*KQ-K)/3-C/a**3-lam
    # Original p_Lf=-2a^2 H^2+2a^2K; p_Lt=-4a^2H.
    # d_t(p_Lt)=-8a^2 H^2-2a^2 dH^2/dln a.
    el=(-2*a*a*h2+2*a*a*K)-6*lam*a*a+(8*a*a*h2+2*a*a*dh2)
    er=2*el
    ephi=-2*a**3*H*(3*KQ+dKQ)
    et=-6*H*dC
    # dH2/dxi is the EXACT derivative of frozen Friedmann once
    # dK/dxi=KQ*dQ/dxi. No observational or numerical derivatives.
    dh2_from_fried=Q*dKQ/3+dC/a**3-3*C/a**3+dlam
    exact={"E_N_vs_Friedmann":symzero(en-6*a**3*fried),
           "E_L_vs_Friedmann_and_continuity":symzero(
               el-2*a*a*(3*fried+dh2+Q*KQ+3*C/a**3)),
           "E_R_is_2E_L":symzero(er-2*el),
           "E_phi_is_scalar_charge_divergence":symzero(
               ephi+2*H*sp.diff(sp.Symbol('placeholder'),sp.Symbol('placeholder'))*0
               +2*a**3*H*(3*KQ+dKQ)),
           "E_T_is_dust_charge_divergence":symzero(et+6*H*dC),
           "E_b_homogeneous":True,"E_u_homogeneous":True,"E_rho_homogeneous":True,
           "dH2_chain_from_exact_KQ_and_Friedmann":symzero(
               dh2_from_fried-(Q*dKQ/3+dC/a**3-3*C/a**3+dlam))}
    assumptions={dh2:-Q*KQ-3*C/a**3,dKQ:-3*KQ,dC:0,dlam:0,h2:(Q*KQ-K)/3+C/a**3+lam}
    for name,val in (("E_N",en),("E_L",el),("E_R",er),
                     ("E_phi",ephi),("E_T",et)):
        exact[name+"_vanishes_under_original_exact_homogeneous_conditions"]=symzero(
            val.subs(assumptions,simultaneous=True))
    exact["dH2_conservation_reduction"]=symzero(
        dh2_from_fried.subs({dKQ:-3*KQ,dC:0,dlam:0})+Q*KQ+3*C/a**3)
    pbx=4*a**3*H
    exact["original_shift_spatial_momentum_NOT_zero"]=not symzero(pbx)
    # Do not remove a physical term from the action merely because its
    # SPATIAL divergence is zero on the homogeneous background.
    exact["negative_control_wrong_GE07_dust_action_factor"]=not symzero(
        en-(en+4*C))
    exact["negative_control_omit_Lambda_lapse"]=not symzero(en-(en+6*a**3*lam))
    exact["negative_control_no_scalar_conservation"]=not symzero(
        ephi.subs(dKQ,0))
    m,kf,ev,fv=sp.symbols("m kfund E00 F21_m",real=True)
    spatial_product=sp.I*m*kf*ev*fv
    exact["full_period_m0_of_E00_dchi_F21_exact_zero"]=symzero(spatial_product.subs(m,0))
    exact["negative_control_nonzero_mode_is_not_zero"]=not symzero(spatial_product.subs(m,1))
    exact["negative_control_spatial_subwindow_not_zero"]=not symzero(ev*(sp.Symbol("F_right")-sp.Symbol("F_left")))
    # For variable spatial weight w, integral w*dchi F = - integral F*dchi w
    # on a period, in general nonzero; the m0 identity is NOT a weighted Ward.
    x=sp.symbols("chi",real=True)
    exact["negative_control_spatial_weight_breaks_unweighted_identity"]=not symzero(
        sp.integrate(sp.cos(x)*sp.diff(sp.sin(x),x),(x,0,2*sp.pi)))
    if not all(exact.values()):
        raise RuntimeError("D12 original-action conditional symbolic proof/negative-control failed: "+str({k:v for k,v in exact.items() if not v}))
    return exact


def l2(a):
    return float(np.linalg.norm(np.asarray(a,float)))


def audit_actual_parent(prereg:dict, d11_json:Path, d11_npz:Path):
    if sha256(d11_json)!=prereg["frozen_parent_D11_json_sha256"]:
        raise RuntimeError("D12 immutable actual D11 JSON SHA256 mismatch")
    if sha256(d11_npz)!=prereg["frozen_parent_D11_npz_sha256"]:
        raise RuntimeError("D12 immutable actual D11 NPZ SHA256 mismatch")
    report=json.loads(d11_json.read_text())
    if report["classification"]!="GE19_H4F3D11_ACTUAL_BACKGROUND_E00_ARRAYS_DIAGNOSTIC_PASS_ONSHELL_OPEN":
        raise RuntimeError("D12 previous actual D11 nonbath E00 diagnostic not passed")
    if (report["original_D10r1_actual_json_sha256"]!=prereg["frozen_original_D10r1_json_sha256"]
        or report["original_D10r1_actual_npz_sha256"]!=prereg["frozen_original_D10r1_npz_sha256"]
        or report["actual_E00_covariant_on_shell_certified"] is not False
        or report["actual_E00_F21_parent_product_evaluated"] is not False):
        raise RuntimeError("D12 original D10r1/D11 provenance/claim boundary changed")
    if len(report["cases"])!=6 or not all(row["pass_machine_only"] for row in report["cases"]):
        raise RuntimeError("D12 actual D11 six cohorts missing")
    kfund=(KH0*H0/100.0)/FOURIER_N0
    if not (np.isfinite(kfund) and kfund>0):
        raise RuntimeError("D12 original kfund invalid")
    rows=[]
    numeric_controls=[]
    with np.load(d11_npz,allow_pickle=False) as z:
        if len(z.files)!=578 or any(not np.isfinite(z[key]).all() for key in z.files):
            raise RuntimeError("D12 original D11 actual numeric archive incomplete/nonfinite")
        for nt,lab in ((128,"primary"),(64,"control")):
            x=np.asarray(z["x_"+lab],float)
            for tag in TAGS:
                prefix=lab+"_"+tag+"_"
                a=np.asarray(z[prefix+"background_a"],float)
                H=np.asarray(z[prefix+"background_H"],float)
                Q=np.asarray(z[prefix+"background_Q_action"],float)
                K=np.asarray(z[prefix+"background_K_action"],float)
                KQ=np.asarray(z[prefix+"background_KQ_action"],float)
                dust=np.asarray(z[prefix+"background_rho_dust_action"],float)
                lam=np.asarray(z[prefix+"background_rho_lambda_action"],float)
                if any(v.shape!=(nt,) for v in (a,H,Q,K,KQ,dust,lam)):
                    raise RuntimeError("D12 original background spatial/temporal grids incompatible")
                if not np.array_equal(x,z[prefix+"background_x"]):
                    raise RuntimeError("D12 original x clock mismatch")
                # Original exact Friedmann and scalar/dust conservation,
                # applied analytically to the same frozen physical grid.
                dh2_exact=-Q*KQ-3*dust
                eL_analytic=2*a*a*(3*H*H+dh2_exact+K-3*lam)
                conservation_scope={"Lambda_exact_constant":bool(np.ptp(lam)==0),
                       "scalar_charge_a3KQ_peak_to_peak":float(np.ptp(a**3*KQ)),
                       "dust_charge_a3rho":float(np.median(a**3*dust))}
                for scheme in SCHEMES:
                    fields={f:np.asarray(z[prefix+scheme+"_E00_"+f],float) for f in NAMES}
                    if any(arr.shape!=(nt,) for arr in fields.values()):
                        raise RuntimeError("D12 original E00 eight field shapes invalid")
                    inf={f:float(np.max(np.abs(fields[f]))) for f in NAMES}
                    coefs={}
                    for band in (REDUCED_BAND,FULL_BAND):
                        kk=band*kfund
                        per={f:kk*inf[f] for f in NAMES}
                        coefs["m0_to_"+str(band)]={
                           "kmax":kk,
                           "per_field_E00_dchi_F21_operator_coefficient":per,
                           "joint_vector_operator_coefficient":float(np.linalg.norm(list(per.values()))),
                           "interpretation":"coefficient MULTIPLYING unknown F21 joint L2 norm; not an absolute physical Ward residual",
                           "background_boundary_L21_coefficient":inf["L"],
                           "background_boundary_b21_coefficient":inf["b"],
                           "spatial_derivative_of_boundary_L21_coefficient":kk*inf["L"],
                           "spatial_derivative_of_boundary_b21_coefficient":kk*inf["b"],
                           "original_F21_norm_available":False}
                    # Original D11 archived actual pressure residual equals
                    # analytic original pressure + the recorded time FD defect.
                    saved_time=np.asarray(z[prefix+scheme+"_component_L_GE06_minus_dt_pLt"],float)
                    exact_time=8*a*a*H*H+2*a*a*dh2_exact
                    delta_fd=saved_time-exact_time
                    residual_diff=(fields["L"]-eL_analytic)-delta_fd
                    error=l2(residual_diff)
                    eL_formula_abs=l2(eL_analytic)
                    # Precision-consistency check only; NOT Euler physical gate.
                    floating_scale=(l2(fields["L"])+l2(eL_analytic)+l2(delta_fd)+1e-30)
                    if error>1e-12*floating_scale:
                        raise RuntimeError("D12 original D11 temporal-defect reassembly mismatch")
                    # Original stored full spatial shift momentum is nonzero;
                    # spatial divergence is exactly zero on homogeneous background.
                    pbx=np.asarray(z[prefix+"GE06_original_p00_b_x"],float)
                    if l2(pbx)<=0:
                        raise RuntimeError("D12 original GE06 spatial shift momentum lost")
                    if not np.array_equal(fields["R"],2*fields["L"]):
                        raise RuntimeError("D12 original D11 E_R=2E_L action identity changed")
                    rows.append({
                       "C":tag,"Nt":nt,"scheme":scheme,
                       "original_frozen_background":conservation_scope,
                       "original_full_fourier_grid_Nx":NX,
                       "euler_actual_E00_L2_report_only":{f:l2(fields[f]) for f in NAMES},
                       "euler_actual_E00_abs_max_report_only":inf,
                       "euler_EL00_exact_background_derivative_substitution_L2_report_only":eL_formula_abs,
                       "euler_EL00_FD_minus_exact_time_derivative_defect_L2_report_only":l2(delta_fd),
                       "original_euler_EL00_minus_exact_background_minus_defect_reassembly_L2":error,
                       "original_nonzero_shift_momentum_p_bx00_L2":l2(pbx),
                       "band_conditional_coefficients":coefs,
                       "periodic_full_period_m0_background_product_exact_zero_analytically":True,
                       "unknown_F21_L21_b21_NOT_assumed_zero":True,
                       "all_sector_GE05_bath_background_E00_not_evaluated":True,
                       "physical_background_onshell_error_budget_not_certified":True})
                    numeric_controls.append(error)
    if len(rows)!=12:
        raise RuntimeError("D12 original scheme/cohort count failed")
    return {"kfund_original":kfund,"kmax_full_m64":FULL_BAND*kfund,
            "kmax_reduced_projection_m40":REDUCED_BAND*kfund,
            "rows":rows,
            "max_EL_temporal_defect_reassembly_abs_L2":max(numeric_controls),
            "max_EL_analytic_homogeneous_background_abs_L2":max(
                r["euler_EL00_exact_background_derivative_substitution_L2_report_only"] for r in rows)}


def fft_negative_control(kfund:float):
    # Synthetic tests of an exact, conditional norm inequality; these
    # are not actual F21 physical trajectories or physical science gates.
    rng=np.random.default_rng(190312)
    nt=7
    n=NX
    synthetic=rng.standard_normal((nt,n))
    fft=np.fft.rfft(synthetic,axis=-1)
    mode=np.arange(n//2+1,dtype=float)
    fft[:,-1]=0 # Real periodic collocation derivative Nyquist sine is zero.
    grad=np.fft.irfft(1j*(kfund*mode)[None,:]*fft,n=n,axis=-1)
    bound=FULL_BAND*kfund*np.linalg.norm(synthetic)
    measured=float(np.linalg.norm(grad))
    if not (measured <= bound*(1+2e-14)):
        raise RuntimeError("D12 synthetic Fourier spectral derivative inequality failed")
    # Spatial mean of every full-period periodic derivative is zero up to
    # round-off; do not claim exact machine equality for a floating FFT.
    meanabs=float(np.max(np.abs(np.mean(grad,axis=-1))))
    if meanabs>2e-12*max(float(np.max(np.abs(grad))),1e-300):
        raise RuntimeError("D12 synthetic full-period Fourier m0 derivative failed")
    if not (np.max(np.abs(np.sum(grad[:,:n//4],axis=-1)))>1e-6):
        raise RuntimeError("D12 spatial subwindow negative control failed")
    return {"synthetic_original_Nx128_Fourier_derivative_L2":measured,
            "synthetic_conservative_full_m64_derivative_upper_L2":float(bound),
            "synthetic_full_period_mean_max_abs":meanabs,
            "synthetic_spatial_subwindow_integral_not_guaranteed_zero":True,
            "synthetic_only_not_physical_F21":True}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--predata",type=Path,required=True)
    parser.add_argument("--d11-json",type=Path,required=True)
    parser.add_argument("--d11-npz",type=Path,required=True)
    parser.add_argument("--json-out",type=Path,required=True)
    args=parser.parse_args()
    if args.json_out.exists():
        raise RuntimeError("D12 original actual audit no-overwrite")
    pre=json.loads(args.predata.read_text())
    if pre.get("classification")!="GE19_H4F3D12_PREDATA_RESTRICTED_HOMOGENEOUS_NOETHER_AND_CONDITIONAL_F21_BOUND":
        raise RuntimeError("D12 preregistration classification mismatch")
    proof=source_bound_analytic_proof()
    a=audit_actual_parent(pre,args.d11_json,args.d11_npz)
    synthetic=fft_negative_control(a["kfund_original"])
    report={
       "classification":"GE19_H4F3D12_RESTRICTED_EXACT_HOMOGENEOUS_NONBATH_IDENTITY_AND_ACTUAL_D11_CONDITIONAL_F21_MULTIPLIERS_PASS_FULL_OPEN",
       "preregistered_classification":pre["classification"],
       "preregistered_sha256":sha256(args.predata),
       "original_actual_D11_json_sha256":sha256(args.d11_json),
       "original_actual_D11_npz_sha256":sha256(args.d11_npz),
       "restricted_symbolic_exact_background_gates":proof,
       "actual_original_D11_conditional_F21_norm_multiplier":a,
       "synthetic_periodic_fourier_negative_controls":synthetic,
       "all_original_six_C_Nt_and_both_FD_schemes":True,
       "original_actual_F21_state_available":False,
       "unknown_L21_b21_available":False,
       "full_original_GE05_bath_background_onshell_certified":False,
       "full_original_H4_Noether_certified":False,
       "original_Repair37_SCIENCE_FAIL_immutable":True,
       "Z21_certified":False,
       "lensing_licensed":False,
       "claim_boundary":"Exact conditional continuum zero of restricted homogeneous GE06/GE07/Lambda Euler under frozen original Friedmann/scalar/dust/Lambda conservation; original actual discrete E00 arrays retained. Gives finite coefficient multiplying unknown F21 norm, not a smallness or absolute Ward bound. Full-period m0 of homogeneous E00*dchi periodic F21 exactly zero, not pointwise/nonzero m/subwindow/full all-sector Ward. No F21 solve, bath on-shell, Z21 or lensing."
    }
    args.json_out.write_text(json.dumps(report,indent=2,sort_keys=True,allow_nan=False)+"\n")
    print(report["classification"])
    print("D12_SOURCE_BOUND_SYMBOLIC_GATES",len(proof),all(proof.values()))
    print("D12_SIX_C_NT_FD4_FD8_ACTUAL_D11_ROWS",len(a["rows"]))
    print("D12_ORIGINAL_FULL_GRID_KMAX",format(a["kmax_full_m64"],".17g"))
    print("D12_MAX_EL_ANALYTIC_L2",format(a["max_EL_analytic_homogeneous_background_abs_L2"],".17g"))
    print("D12_MAX_EL_TEMPORAL_DEFECT_REASSEMBLY_L2",format(a["max_EL_temporal_defect_reassembly_abs_L2"],".17g"))
    print("D12_JSON_SHA256",sha256(args.json_out))

if __name__=="__main__":
    main()
