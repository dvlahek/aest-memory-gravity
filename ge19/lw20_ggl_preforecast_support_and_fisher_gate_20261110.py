#!/usr/bin/env python3
"""GE19 LW20 — DES Y3 MagLim4 galaxy-galaxy lensing PRE-forecast gate.

Reads only archived DES Y3 lens n(z)-mass coverage and LW08 native
source-response reliability; does NOT read sky shear, fit parameters,
extrapolate missing k/z, invent a source n(z), or output significance.

A true GGL observable needs physical P_deltaW derivative, lens/source
kernels and bias, theta/bandpower windows, covariance and nuisance
marginalization. Cosmic-shear full LOS BLOCK remains unchanged.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PRE=ROOT/"ge19/lw20_ggl_observer_preforecast_predata_20261110.json"
PRE_BLOB="f3915e650e044433a4cec18efd3381848bdb7ec1"
SOURCES={
  "results/ge19_lw07b_des_y3_nz_only_audit_20261109.json":
    "5323b8457cbe7e7426c3e6eb4345183c3660cbff",
  "results/ge19_lw08_density_weyl_relative_tangent_20261109_archive_replay.json":
    "f3039640de268cd2136474f1ac716a80695b3713",
}
LW19_SHA="7a13c89f7387299f3ce20bc92716004c8096ea0f170ac7cd0739fcc50d44207e"

def require(ok,name):
    if not bool(ok):
        raise RuntimeError("GE19_LW20_"+name)

def gitblob(p):
    return subprocess.check_output(
        ["git","hash-object",str(p)],text=True).strip()

def sha256(p):
    d=hashlib.sha256()
    with Path(p).open("rb") as stream:
        for c in iter(lambda:stream.read(1<<20),b""):
            d.update(c)
    return d.hexdigest()

def fisher_schur(t, covariance, nuisance, prior_precision):
    """General Asimov marginalized Fisher for ONE physical signal eta.

    A numerical forecast from the actual survey can only be run after
    all real physical and survey inputs are independently certified.
    Used HERE exclusively for algebraic selftests, never observations.
    """
    import numpy as np
    t=np.asarray(t,dtype=float).reshape(-1)
    C=np.asarray(covariance,dtype=float)
    D=np.asarray(nuisance,dtype=float)
    P=np.asarray(prior_precision,dtype=float)
    require(C.shape==(t.size,t.size),"FISHER_COVARIANCE_SHAPE")
    require(D.ndim==2 and D.shape[0]==t.size,"FISHER_NUISANCE_SHAPE")
    n=D.shape[1]
    require(P.shape==(n,n),"FISHER_PRIOR_SHAPE")
    require(np.all(np.isfinite(C)) and np.all(np.isfinite(D)) and
            np.all(np.isfinite(P)) and np.all(np.isfinite(t)),
            "FISHER_NONFINITE")
    require(np.allclose(C,C.T,rtol=0,atol=1.e-12) and
            np.allclose(P,P.T,rtol=0,atol=1.e-12),
            "FISHER_NOT_SYMMETRIC")
    require(np.min(np.linalg.eigvalsh(C))>0 and
            np.min(np.linalg.eigvalsh(P))>=-1.e-12,
            "FISHER_NON_PSD_INPUTS")
    Ct=np.linalg.solve(C,t)
    if n==0:
        return float(t@Ct)
    CD=np.linalg.solve(C,D)
    M=D.T@CD+P
    require(np.min(np.linalg.eigvalsh(M))>0,
            "FISHER_UNIDENTIFIABLE_NUISANCE_BLOCK")
    F=float(t@Ct-(D.T@Ct)@np.linalg.solve(M,D.T@Ct))
    require(F>=-1.e-10*max(1.,abs(float(t@Ct))),
            "FISHER_NEGATIVE")
    return max(F,0.)

def selftest():
    import numpy as np
    C=np.eye(2)
    t=np.array([1.,0.])
    require(abs(fisher_schur(t,C,np.zeros((2,0)),np.zeros((0,0)))-1.)<1.e-12,
            "FISHER_NO_NUISANCE")
    require(fisher_schur(t,C,np.array([[1.],[0.]]),
                         np.zeros((1,1)))<1.e-12,
            "FISHER_SIGNAL_NUISANCE_DEGENERACY")
    require(abs(fisher_schur(t,C,np.array([[0.],[1.]]),
                            np.zeros((1,1)))-1.)<1.e-12,
            "FISHER_ORTHOGONAL_NUISANCE")
    # Finite prior restores some mathematical information; not real data.
    require(abs(fisher_schur(t,C,np.array([[1.],[0.]]),
                            np.array([[1.]]))-.5)<1.e-12,
            "FISHER_FINITE_NUISANCE_PRIOR")
    print("GE19_LW20_ASIMOV_FISHER_SYNTHETIC_SELFTEST_PASS 4",flush=True)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--self-test",action="store_true")
    ap.add_argument("--out",type=Path,default=ROOT/
        "results/ge19_lw20_ggl_preforecast_support_20261110.json")
    opts=ap.parse_args()
    if opts.self_test:
        selftest()
        return
    require(gitblob(PRE)==PRE_BLOB,"PROTOCOL_CHANGED")
    pre=json.loads(PRE.read_text())
    require(pre["classification"]==
        "GE19_LW20_PHYSICS_FIRST_GGL_PREOBSERVATION_SELECTION_LOCK",
        "PROTOCOL_CLASS_CHANGED")
    for name,want in SOURCES.items():
        require(gitblob(ROOT/name)==want,"SOURCE_CHANGED_"+Path(name).name)
    p=ROOT/"results/ge19_lw19_reduced_full_action_temporal_invariance_20261110_r1.json"
    require(p.is_file() and sha256(p)==LW19_SHA,"ORIGINAL_WSL_LW19_CHANGED")
    lw19=json.loads(p.read_text())
    require(lw19["classification"]==
      "GE19_LW19_FULL_REDUCED_GE06_GE05_TEMPORAL_ACTION_COVARIANCE_PASS_CLASS_MAP_OPEN"
      and len(lw19["checks"])==16
      and all(lw19["checks"].values()),"LW19_PARENT_INVALID")
    seven=json.loads((ROOT/"results/ge19_lw07b_des_y3_nz_only_audit_20261109.json").read_text())
    eight=json.loads((ROOT/"results/ge19_lw08_density_weyl_relative_tangent_20261109_archive_replay.json").read_text())
    require(seven["classification"]==
      "GE19_LW07B_TRUE_NZ_SUPPORT_MEASURED_OBSERVATION_STILL_BLOCKED",
      "LW07B_PARENT_CHANGED")
    require(eight["classification"]==
      "GE19_LW08_RELATIVE_SOURCE_TANGENT_REPLAY_PASS_NOT_AN_OBSERVABLE"
      and eight["antisymmetric_physical_response_numerically_certified"] is False,
      "LW08_UNRESOLVED_PARENT_CHANGED")
    require(seven["observational_likelihood_authorized"] is False
      and seven["full_angular_window_forward_model_certified"] is False
      and seven["physical_eta_calibrated"] is False
      and seven["observed_shear_or_covariance_read"] is False,
      "LW07B_SCOPE_CHANGED")
    target=pre["target"]
    rows=[r for r in seven["rows"] if
          r["sample"]==target["lens_sample"] and
          r["bin_1based"]==target["lens_bin_1based"]]
    require(len(rows)==1,"LENS_TARGET_NOT_UNIQUE")
    row=rows[0]
    by_ell={p["ell"]:p for p in row["per_ell"]}
    ell=target["candidate_ell"]
    require(len(ell)==3 and all(e in by_ell for e in ell) and
            target["excluded_ell_control"] in by_ell,
            "ELL_PRESELECTION_CHANGED")
    threshold=target["information_screen_threshold_nz_mass"]
    coverage=[{"ell":e,
               "lens_nz_mass_fraction_only":
                 by_ell[e]["fraction_of_calibrated_nz_mass_inside_kz_domain"],
               "mass_outside_unquantified_observable":
                 1-by_ell[e]["fraction_of_calibrated_nz_mass_inside_kz_domain"]}
              for e in ell]
    require(all(x["lens_nz_mass_fraction_only"]>=threshold for x in coverage),
            "CANDIDATE_LENS_NZ_SCREEN_FAIL")
    control=by_ell[target["excluded_ell_control"]]
    require(control["fraction_of_calibrated_nz_mass_inside_kz_domain"]<threshold,
            "ELL300_NEGATIVE_COVERAGE_CONTROL_FAIL")
    # No DES gamma_t/covariance data or physical eta-signal is read or
    # synthesized. Any forecast value here would be fabricated.
    report={
      "classification":
        "GE19_LW20_MAGLIM4_LENS_ONLY_SUPPORT_SCREEN_PASS_GGL_FORWARD_AND_FORECAST_BLOCKED",
      "frozen_protocol_git_blob_sha1":PRE_BLOB,
      "original_parent_blobs":SOURCES,
      "original_LW19_WSL_SHA256":LW19_SHA,
      "survey":"DES Y3",
      "observable_candidate":"MagLim bin 4 g x kappa (galaxy-galaxy lensing)",
      "ell_candidates":ell,
      "native_k_h":[float(v) for v in seven["native_k_h_window"]],
      "native_z":[float(v) for v in seven["native_z_window"]],
      "lens_nz_mass_coverage_info":coverage,
      "lens_ell300_negative_coverage_control":{
        "ell":target["excluded_ell_control"],
        "mass_fraction":
          control["fraction_of_calibrated_nz_mass_inside_kz_domain"],
      },
      "lens_nz_screen_gates":{
        "original_LW07b_not_observation":True,
        "original_LW08_antisymmetric_unresolved":True,
        "fixed_lens_selection":True,
        "three_candidate_ell_above_info_threshold":True,
        "excluded_ell300_below_info_threshold":True,
        "LW19_original_WSL_provenance":True,
      },
      "physics_forward_equation":
        "C_ell_gkappa = ell*(ell+1) int dchi n_L(chi)*b_L(chi)*q_s(chi)/chi^3 * P_deltaW(k=(ell+.5)/chi,z(chi)) (sign convention fixed consistently), q_s=int_chi^inf dchi_s n_s(chi_s)(chi_s-chi)/chi_s",
      "derivative_target":
        "dC_ell_gkappa/deta at frozen FLRW background, physical eta=0 forcing from original NL0B, with tracer bias/nuisance responses",
      "fisher_schur_formula":
        "F_eta_marg = t^T C^-1 t - t^T C^-1 D (D^T C^-1 D + P_prior)^-1 D^T C^-1 t",
      "fisher_synthetic_selftests_available":True,
      "physical_eta_finite_calibration":False,
      "full_lens_kz_support_and_quadrature_certified":False,
      "source_nz_and_lensing_efficiency_kernel_validated":False,
      "galaxy_bias_magnification_IA_model_validated":False,
      "DES_theta_ell_window_and_scale_cut_validated":False,
      "real_covariance_and_nuisance_derivatives_validated":False,
      "Asimov_sensitivity_computed":False,
      "observed_shear_read":False,
      "physical_two_history_metric_observer_certified":False,
      "full_action_to_CLASS_fluid_map_certified":False,
      "DES_ACT_memory_detection":False,
      "LW05_cosmic_shear_FULL_LOS_BLOCK_preserved":True,
      "LW08_antisymmetric_response_UNRESOLVED_preserved":True,
      "H4_Z21_certified":False,
      "scientific_decision":
        "Candidate DES Y3 GGL avoids imposing the cosmic-shear all-chi-to-source transfer requirement. Lens n(z) mass is >99% at three selected ell, but this is NOT a GGL forward or likelihood certification. Next physics gate is genuine full-coupled P_deltaW physical eta derivative in calibrated lens bins and source/bandpower kernels; do not report forecast significance without real covariance.",
    }
    out=opts.out.resolve()
    require(out.parent.is_dir() and not out.exists(),
            "OUTPUT_EXISTS_OR_DIR_MISSING")
    out.write_text(json.dumps(report,sort_keys=True,indent=2,
                              allow_nan=False)+"\n")
    print("GE19_LW20_CLASSIFICATION",report["classification"],flush=True)
    for x in coverage:
        print("GE19_LW20_LENS_NZ_SCREEN",
              x["ell"],f'{x["lens_nz_mass_fraction_only"]:.9f}',flush=True)
    print("GE19_LW20_PHYSICAL_FORECAST_READY",False,flush=True)
    print("GE19_LW20_OUTPUT",out,flush=True)

if __name__=="__main__":
    main()
