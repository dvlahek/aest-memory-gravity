#!/usr/bin/env python3
"""GE19 H4F3d11 actual original homogeneous GE06/GE07/Lambda background Euler.

Evaluate E_i00 for all eight fields on exactly six frozen Repair13 x/C/Nt
backgrounds. Original H*FD4 and H*FD8 physical-time schemes are archived
SEPARATELY. No E00 on-shell assertion, E00*F21 removal or H4 Ward claim.
"""
from __future__ import annotations
import argparse,json,subprocess
from pathlib import Path
import numpy as np

from ge19 import h4f3d10_actual_nonbath_first_order_known_boundary as frozen
from ge19 import h4f3d11_source_bound_original_background_partials as source

ROOT=Path(__file__).resolve().parents[1]
SOURCE_PINS={
"ge19/h4f3d11_predata_actual_original_action_background_e00.json":
"deb4b35e6a147b48fe93d6c99d798572650000ac",
"ge19/h4f3d11_source_bound_original_background_partials.py":
"1f085efec4ea64b42822ddeaac566f532d9dccf1",
"ge19/h4f3d10r1_actual_physical_lossless_archive_independent_audit.json":
"2921f79dbb0ce99200418bfba924b699ff8cd67f",
"ge19/h4f3d10r1_lossless_fourier_physical_main.py":
"659ba72aafedc6f62d519f5fe09e47736074e90a",
"ge19/repair07_window_retarded_reduced_h3_z20_particular.py":
"e34d28a2062c748f48bc82fa928844b02631de25",
"ge19/repair11_lambda_inclusive_reduced_h1_reclosure.py":
"dbfa43ae11dbd3cfeeb1994a30237e9374dbb3e7",
"ge19/repair13_self_consistent_reduced_background_h1_reclosure.py":
"362d63d03d7b850fceae393f535353ded79aeea7",
"ge06/analytic_aest_directional_source_generator.py":
"a7afe0035054a9dca55d74a6497c081422114b4c",
"ge07/pressureless_matter_directional_source_generator.py":
"cde8da77a80799cef00fc7c09c3633310fc9e3d4"}
D10R1={
"json":"69eabf101a6ec1939b32323e25b207dc419fad57eb5b2cef0858874a50cfa1d2",
"npz":"85c0fbd8b56037aae98615926b70bd60739a1af2fa1ff666ffc2e95485c2749b"}
FIELDS=("N","L","R","b","u","phi","T","rho")
TINY=1e-300

def source_locks():
    locked={}
    for path,want in SOURCE_PINS.items():
        head=subprocess.check_output(["git","rev-parse","HEAD:"+path],
                cwd=ROOT,text=True).strip()
        work=subprocess.check_output(["git","hash-object",str(ROOT/path)],
                cwd=ROOT,text=True).strip()
        exact=head==work==want
        locked[path]={"expected":want,"head":head,
                      "worktree":work,"exact":exact}
        if not exact:
            raise RuntimeError("D11 source/parent Git SHA mismatch: "+path)
    return locked

def norm(q):
    return float(np.linalg.norm(np.asarray(q,float)))

def arrays(bg,tag,r7,compiled,fd_matrix):
    a=np.asarray(bg["a"],float)
    H=np.asarray(bg["H"],float)
    x=np.asarray(bg["x"],float)
    nt=len(x)
    if any(np.asarray(bg[k]).shape!=(nt,) for k in (
        "a","H","Z_action","Q_action","K_action","KQ_action",
        "rho_lambda_action","rho_dust_action")):
        raise RuntimeError("D11 incomplete original Repair13 physical grid")
    ga,du,consistency=source.physical_partials(compiled,bg,tag,r7)
    lam=np.asarray(bg["rho_lambda_action"],float)
    Dt=H[:,None]*np.asarray(fd_matrix,float)
    if Dt.shape!=(nt,nt) or not np.isfinite(Dt).all():
        raise RuntimeError("D11 original FD4/FD8 time operator invalid")
    lmb={
        "N":-6.0*lam*a**3,
        "L":-6.0*lam*a**2,
        "R":-12.0*lam*a**2}
    components={
        "N":{"GE06_local":ga["N_f"],"GE07_local":du["N_f"],
             "Lambda":lmb["N"]},
        "L":{"GE06_local":ga["L_f"],
             "GE06_minus_dt_pLt":-(Dt@ga["L_t"]),
             "GE07_local":du["L_f"],"Lambda":lmb["L"]},
        "R":{"GE06_local":ga["R_f"],
             "GE06_minus_dt_pRt":-(Dt@ga["R_t"]),
             "GE07_local":du["R_f"],"Lambda":lmb["R"]},
        "b":{"GE06_local":ga["b_f"],"GE07_local":du["b_f"]},
        "u":{"GE06_local":ga["u_f"],
             "GE06_minus_dt_put":-(Dt@ga["u_t"])},
        "phi":{"GE06_minus_dt_phi_current":-(Dt@ga["phi_t"])},
        "T":{"GE07_minus_dt_T_current":-(Dt@du["T_t"])},
        "rho":{"GE07_rho_constraint":du["rho_f"]}}
    e={name:sum((np.asarray(q,float) for q in terms.values()),
                np.zeros(nt,float)) for name,terms in components.items()}
    if (set(e)!=set(FIELDS)
        or any(q.shape!=(nt,) or not np.isfinite(q).all()
               for q in e.values())):
        raise RuntimeError("D11 incomplete/nonfinite actual eight-field E00")
    rho_dust=np.asarray(bg["rho_dust_action"],float)
    K=np.asarray(bg["K_action"],float)
    KQ=np.asarray(bg["KQ_action"],float)
    Q=np.asarray(bg["Q_action"],float)
    fried=H**2-(Q*KQ-K)/3.0-rho_dust-lam
    e_n_from_fried=6.0*a**3*fried
    saved={}
    for n,v in ga.items():saved["GE06_original_p00_"+n]=v
    for n,v in du.items():saved["GE07_original_p00_"+n]=v
    for n,v in lmb.items():saved["Lambda_E00_"+n]=v
    for n,v in e.items():saved["E00_"+n]=v
    for n,terms in components.items():
        for part,v in terms.items():
            saved["component_"+n+"_"+part]=v
    saved["EN_from_frozen_Repair13_Friedmann_report_only"]=e_n_from_fried
    saved["H2_Friedmann_difference_report_only"]=fried
    saved["original_rho_lambda_dxi_report_only"]=fd_matrix@lam
    saved["original_scalar_charge_a3_KQ_report_only"]=a**3*KQ
    saved["original_dust_charge_a3_rhob_report_only"]=(a**3*
             3.0*float(r7.C_VALUES[tag])/a**3)
    for n in ("x","a","H","Q_action","Z_action","K_action",
              "KQ_action","rho_lambda_action","rho_dust_action"):
        saved["background_"+n]=np.asarray(bg[n],float)
    if any(q.shape!=(nt,) or not np.isfinite(q).all()
           for q in saved.values()):
        raise RuntimeError("D11 incomplete/nonfinite raw physical background archive")
    scales={n:sum(norm(q) for q in terms.values())
            for n,terms in components.items()}
    diag={
        "C":tag,"Nt":nt,
        "original_source_consistency_machine_only":consistency,
        "original_eight_field_E00_L2_report_only":{
             n:norm(q) for n,q in e.items()},
        "original_eight_field_E00_natural_relative_report_only":{
             n:norm(e[n])/max(scales[n],TINY) for n in FIELDS},
        "original_eight_field_E00_component_natural_scale_L2_report_only":scales,
        "Friedmann_EN_source_minus_reduced_identity_abs_L2_report_only":
             norm(e["N"]-e_n_from_fried),
        "Friedmann_reduced_identity_L2_report_only":norm(fried),
        "GE06_original_shift_bx00_momentum_L2_report_only":norm(ga["b_x"]),
        "GE06_scalar_current_minus_stable_charge_L2_report_only":
             norm(ga["phi_t"]-2.0*a**3*KQ),
        "GE07_T_current_minus_exact_charge_L2_report_only":
             norm(du["T_t"]-6.0*float(r7.C_VALUES[tag])),
        "rho_lambda_a_grid_span_report_only":
             float(np.max(lam)-np.min(lam)),
        "rho_lambda_dxi_L2_report_only":norm(fd_matrix@lam),
        "E00_source_and_archive_finite":True,
        "no_E00_on_shell_smallness_gate_applied":True,
        "no_E00_F21_or_L21_background_term_eliminated":True,
        "full_H4_Noether_not_tested":True}
    return saved,diag

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--results-dir",required=True)
    p.add_argument("--repair26-trace",required=True)
    p.add_argument("--json-out",required=True)
    p.add_argument("--npz-out",required=True)
    args=p.parse_args()
    rd=Path(args.results_dir).resolve()
    outj=Path(args.json_out).resolve()
    outn=Path(args.npz_out).resolve()
    trace=Path(args.repair26_trace).resolve()
    if outj.exists() or outn.exists():
        raise RuntimeError("D11 no-overwrite actual physical output policy")
    prereg=json.loads((ROOT/"ge19/h4f3d11_predata_actual_original_action_background_e00.json").read_text())
    if (prereg["classification"]!=
        "GE19_H4F3D11_PREDATA_ORIGINAL_ACTION_SOURCE_BOUND_ACTUAL_BACKGROUND_E00_ALL_EIGHT_FIELDS"
        or prereg["preregistered_machine_only_controls"][
                "source_vs_explicit_numeric_closed_forms_rtol"]!=source.RTOL):
        raise RuntimeError("D11 immutable predata classification/control mismatch")
    code=source_locks()
    parent_code=frozen.locks()
    physical=frozen.physical_paths(rd,trace)
    parent_paths,parents=frozen.s.frozen_inputs(rd,trace)
    if not all(parents[k]["exact"] for k in frozen.s.REQUIRED):
        raise RuntimeError("D11 frozen H3F/H3G/Repair13/Z11/trace mismatch")
    old_json=rd/"ge19_h4f3d10r1_lossless_fourier_known_boundary.json"
    old_npz=rd/"ge19_h4f3d10r1_lossless_fourier_known_boundary.npz"
    if (frozen.digest(old_json)!=D10R1["json"]
        or frozen.digest(old_npz)!=D10R1["npz"]):
        raise RuntimeError("D11 actual frozen known first-order nonbath inputs changed")
    old_report=json.loads(old_json.read_text())
    if (old_report["classification"]!=
        "GE19_H4F3D10R1_LOSSLESS_ARCHIVE_KNOWN_NONBATH_DIAGNOSTIC_PASS_FULL_OPEN"
        or not old_report["lossless_full_Nyquist_archive_only_checks_pass"]
        or not old_report["all_original_D10_low_mode_arrays_bitwise_reproduced"]):
        raise RuntimeError("D11 D10r1 original physical-parent diagnostic not PASS")
    save={}
    rows=[]
    with (np.load(parent_paths["r13"],allow_pickle=False) as r13,
          np.load(parent_paths["h3fn"],allow_pickle=False) as h3f,
          np.load(parent_paths["z11"],allow_pickle=False) as z11,
          np.load(old_npz,allow_pickle=False) as original10):
        bgs,_,_,mod7,_,_,_,_,_=frozen.old.build_context(rd,r13)
        mod6_frozen=frozen.old.r7.load_frozen_generator(
            ROOT/"ge06/analytic_aest_directional_source_generator.py",
            "GE19_D11_original_GE06_exact_homogeneous")
        compiled=source.compile_exact_source(mod6_frozen,mod7)
        for nt,label in ((128,"primary"),(64,"control")):
            x=np.asarray(original10["x_"+label],float)
            if x.shape!=(nt,):
                raise RuntimeError("D11 original D10r1 clock is not original cohort")
            for parent in (h3f,z11):
                if not np.array_equal(x,np.asarray(parent["x_"+label],float)):
                    raise RuntimeError("D11 original H3F/Z11 parent clock mismatch")
            save["x_"+label]=x
            for tag in frozen.old.r7.C_TAGS:
                bg=bgs[(nt,tag)]
                if not np.array_equal(np.asarray(bg["x"],float),x):
                    raise RuntimeError("D11 Repair13 original clock mismatch")
                outputs={}
                diags={}
                for scheme,mat in (
                    ("FD4",frozen.old.r7.fd4_matrix(
                        nt,float(x[0]),float(x[-1]))),
                    ("FD8",frozen.old.fd8_matrix(
                        nt,float(x[0]),float(x[-1])))):
                    arrays_,diag=arrays(bg,tag,frozen.old.r7,compiled,mat)
                    for name,q in arrays_.items():
                        key=name
                        if name.startswith("background_") or name.startswith("GE06_original_p00_") or name.startswith("GE07_original_p00_") or name.startswith("Lambda_E00_"):
                            if key in outputs:
                                if not np.array_equal(outputs[key],q):
                                    raise RuntimeError("D11 source p00 or bg changed across original FD schemes")
                            else:
                                outputs[key]=q
                        else: outputs[scheme+"_"+key]=q
                    diags[scheme]=diag
                for name,q in outputs.items():
                    save[label+"_"+tag+"_"+name]=q
                rows.append({"C":tag,"Nt":nt,
                    "all_8_original_nonbath_background_E00_rows_saved":True,
                    "original_fd4_and_fd8_separate":True,
                    "original_R1_bath_2048_nodes_unchanged":True,
                    "source_bound_GE06_GE07_symbolic_gates":compiled[-1],
                    "schemes":diags,
                    "all_E00_on_shell_conditions_evaluated_with_valid_error_budget":False,
                    "original_unknown_F21_and_L21_background_preserved":True,
                    "pass_machine_only":True})
    ok=bool(len(rows)==6 and all(row["pass_machine_only"] for row in rows)
            and all(np.isfinite(q).all() for q in save.values()))
    result={
        "classification":(
            "GE19_H4F3D11_ACTUAL_BACKGROUND_E00_ARRAYS_DIAGNOSTIC_PASS_ONSHELL_OPEN"
            if ok else "GE19_H4F3D11_ACTUAL_SOURCE_OR_PARENT_INCONSISTENT"),
        "original_preregistered_scope":prereg["classification"],
        "source_and_parent_code_exact_blobs":code,
        "frozen_parent_code_locks":parent_code,
        "original_parent_input_hashes":parents,
        "original_H4F3b_d6_d7r1_input_sha256":{
            k:frozen.digest(p) for k,p in physical.items()},
        "original_D10r1_actual_json_sha256":frozen.digest(old_json),
        "original_D10r1_actual_npz_sha256":frozen.digest(old_npz),
        "all_six_original_C_Nt_backgrounds_evaluated":len(rows)==6,
        "all_original_E00_arrays_source_bound_finite":ok,
        "cases":rows,
        "actual_E00_evaluated":ok,
        "actual_E00_covariant_on_shell_certified":False,
        "actual_E00_F21_parent_product_evaluated":False,
        "actual_L21_EL00_minus_b21_Eb00_evaluated":False,
        "actual_all_sector_integrated_H4_Ward_evaluated":False,
        "actual_full_FD4_FD8_error_bound_certified":False,
        "Z21_certified":False,"lensing_licensed":False,
        "original_D10_unresolved_immutable":True,
        "original_Repair37_SCIENCE_FAIL_immutable":True,
        "claim_boundary":"Original-source exact GE06 GE07 Lambda and analytically zero-background NL0C/Y homogeneous all-eight nonbath Euler arrays evaluated on original Repair13 physical grids, with original H*FD4/H*FD8 divergences independently saved as report only. No validated physical derivative error bound or E00 on-shell gate. Unknown E00*F21 and L21*EL00-b21*Eb00 not deleted, full H4 Ward and Z21 OPEN."
    }
    outj.parent.mkdir(parents=True,exist_ok=True)
    outn.parent.mkdir(parents=True,exist_ok=True)
    outj.write_text(json.dumps(result,indent=2,sort_keys=True,allow_nan=False)+"\n")
    np.savez_compressed(outn,**save)
    print(json.dumps(result,indent=2,sort_keys=True,allow_nan=False))
    if not ok:raise SystemExit(2)

if __name__=="__main__":main()
