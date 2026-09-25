#!/usr/bin/env python3
"""GE19 H4F3d9: exact original FD4/FD8 stencil constants, NOT full error bound.

Source-read/AST-only compiler: does not import historical GE19 generators,
read physical parent binaries, adjust original derivatives or run H4/Z21.
"""
from __future__ import annotations

import argparse
import ast
from fractions import Fraction
import json
import math
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
PREDATA = "ge19/h4f3d9_predata_original_fd4_fd8_structural_error_budget.json"
PRE_BLOB = "98e6fd8835fdbe3bd169d062431eefe80a3e9232"
AMENDMENT = "ge19/h4f3d9_predata_amendment01_correct_d7_git_blob.json"
AMEND_BLOB = "34cea0c62ef2dc962bc43ef93b2fbbd70b9c2180"
PATHS = {
    "Repair07_original_FD4": "ge19/repair07_window_retarded_reduced_h3_z20_particular.py",
    "Repair37_original_FD8": "ge19/repair37_cancellation_safe_fd8_h4_z21_reclosure.py",
    "H4F2H_original_scheme_map": "ge19/h4f2h_physical_time_source_ward_bridge.py",
    "H4F3d1_original_canonical_operator": "ge19/h4f3d1_frozen_canonical_operator_ward.py",
    "H4F3d6_original_bath_Euler": "ge19/h4f3d6_actual_normalized_bath_parent_ward.py",
    "H4F3d7_original_interval_diagnostic": "ge19/h4f3d7_bath_fd4_vs_original_r1_interval_ode.py",
    "H4F3d8_independent_nonbath_compiler": "ge19/h4f3d8_independent_nonbath_euler_and_boundary.py",
    "NL0C_Y_original_action_flux": "ge19/h4_stagee_versioned_y_source_rows.py",
    "H4F3d_full_actual_predata": "ge19/h4f3d_predata_actual_operator_all_parent_ward_closure.json",
}
FD4_INDICES = (
    "D[0,0:5]", "D[1,0:5]", "D[i,i-2:i+3]",
    "D[-2,-5:]", "D[-1,-5:]",
)
FD8_INDICES = (
    "D[0,0:9]", "D[1,0:9]", "D[2,0:9]", "D[3,0:9]",
    "D[i,i-4:i+5]", "D[-4,-9:]", "D[-3,-9:]",
    "D[-2,-9:]", "D[-1,-9:]",
)


def blob(relative, worktree=False):
    cmd = (["git", "hash-object", str(ROOT/relative)] if worktree
           else ["git", "rev-parse", "HEAD:" + relative])
    return subprocess.check_output(cmd, cwd=ROOT, text=True).strip()


def source_lock():
    prereg = json.loads((ROOT/PREDATA).read_text())
    if (prereg.get("classification") !=
            "GE19_H4F3D9_PREDATA_ORIGINAL_FD4_FD8_STENCIL_CONSTANTS_AND_FULL_WARD_ERROR_BUDGET_PROTOCOL"
            or set(prereg["frozen_source_blobs"]) != set(PATHS)):
        raise RuntimeError("H4F3d9 frozen preregistration not recognized")
    amend = json.loads((ROOT/AMENDMENT).read_text())
    override = amend["one_allowed_override"]
    if not (
        amend["classification"] ==
        "GE19_H4F3D9_PREDATA_AMENDMENT01_CORRECT_FROZEN_D7_BLOB_ONLY"
        and amend["parent_predata"] == PREDATA
        and amend["parent_predata_git_blob"] == PRE_BLOB
        and override["label"] == "H4F3d7_original_interval_diagnostic"
        and override["path"] == PATHS[override["label"]]
        and prereg["frozen_source_blobs"][override["label"]] ==
            override["old_wrong_git_blob"]
        and override["correct_original_git_blob"] ==
            "b598a5cc49b3d87827b4758c55d3ce7f3a1198a8"
        and all(amend[key] is True for key in (
            "original_predata_unchanged",
            "all_other_source_pins_unchanged",
            "physical_dataset_unmodified",
            "registered_FD4_FD8_formulas_unchanged",
            "no_new_numeric_error_tolerance",
            "no_physical_test_executed",
            "no_relabel_of_historical_results"))
    ):
        raise RuntimeError("H4F3d9 immutable single-pin amendment not recognized")
    registered = dict(prereg["frozen_source_blobs"])
    registered[override["label"]] = override["correct_original_git_blob"]
    want = {"predata": (PREDATA, PRE_BLOB),
            "predata_amendment01": (AMENDMENT, AMEND_BLOB)}
    want.update({key:(PATHS[key],value)
                 for key,value in registered.items()})
    result = {}
    for key,(path,expected) in want.items():
        head,actual = blob(path),blob(path,True)
        result[key] = {
            "file":path,"expected":expected,"git_HEAD":head,
            "working_tree":actual,
            "exact":expected==head==actual
        }
    return result,prereg,amend


def exact_fraction(node):
    """Restricted AST evaluator for numeric SOURCE literals only."""
    if isinstance(node,ast.Constant) and type(node.value) is int:
        return Fraction(node.value)
    if isinstance(node,ast.UnaryOp) and isinstance(node.op,ast.USub):
        return -exact_fraction(node.operand)
    if isinstance(node,ast.UnaryOp) and isinstance(node.op,ast.UAdd):
        return exact_fraction(node.operand)
    if isinstance(node,ast.BinOp):
        left,right=exact_fraction(node.left),exact_fraction(node.right)
        if isinstance(node.op,ast.Add):return left+right
        if isinstance(node.op,ast.Sub):return left-right
        if isinstance(node.op,ast.Mult):return left*right
        if isinstance(node.op,ast.Div):return left/right
    raise ValueError("non-rational literal in original source stencil")


def fd4_original_rows():
    text=(ROOT/PATHS["Repair07_original_FD4"]).read_text()
    tree=ast.parse(text)
    functions=[n for n in tree.body if isinstance(n,ast.FunctionDef)
               and n.name=="fd4_matrix"]
    if len(functions)!=1:
        raise RuntimeError("frozen FD4 matrix function missing or duplicated")
    got={}
    for n in ast.walk(functions[0]):
        if not (isinstance(n,ast.Assign) and len(n.targets)==1
                and isinstance(n.value,ast.BinOp)
                and isinstance(n.value.op,ast.Div)
                and isinstance(n.value.left,ast.Call)):
            continue
        key="".join(ast.unparse(n.targets[0]).split())
        call=n.value.left
        if (key not in FD4_INDICES or
                "".join(ast.unparse(call.func).split())!="np.asarray"):
            continue
        if ("".join(ast.unparse(n.value.right).split())!="12*h"
                or len(call.args)<1
                or not isinstance(call.args[0],ast.List)):
            raise RuntimeError("changed original FD4 normalized denominator/list")
        if key in got:
            raise RuntimeError("duplicated original FD4 row "+key)
        got[key]=[exact_fraction(node)/12 for node in call.args[0].elts]
    if set(got)!=set(FD4_INDICES) or any(len(row)!=5 for row in got.values()):
        raise RuntimeError("all five original FD4 rows not extracted exactly")
    return [got[key] for key in FD4_INDICES]


def fd8_original_rows():
    text=(ROOT/PATHS["Repair37_original_FD8"]).read_text()
    tree=ast.parse(text)
    nodes=[node for node in tree.body
           if isinstance(node,ast.Assign)
           and len(node.targets)==1
           and isinstance(node.targets[0],ast.Name)
           and node.targets[0].id=="_FD8_W"]
    if len(nodes)!=1:
        raise RuntimeError("original nine-row FD8 weight constant missing")
    call=nodes[0].value
    if (not isinstance(call,ast.Call)
        or "".join(ast.unparse(call.func).split())!="np.asarray"
        or len(call.args)<1 or not isinstance(call.args[0],ast.List)):
        raise RuntimeError("original FD8 nine-row rational literal changed")
    rows=call.args[0].elts
    if len(rows)!=9 or not all(isinstance(z,ast.List)
                               and len(z.elts)==9 for z in rows):
        raise RuntimeError("original FD8 nine-by-nine weights changed")
    compact="".join(text.split())
    for i,key in enumerate(FD8_INDICES):
        if (key+"=_FD8_W["+str(i)+"]/h") not in compact:
            raise RuntimeError("FD8 frozen endpoint/interior row mapping changed: "+key)
    return [[exact_fraction(z) for z in row.elts] for row in rows]


def original_scheme_binding():
    text=(ROOT/PATHS["H4F2H_original_scheme_map"]).read_text()
    op=(ROOT/PATHS["H4F3d1_original_canonical_operator"]).read_text()
    d6=(ROOT/PATHS["H4F3d6_original_bath_Euler"]).read_text()
    d7=(ROOT/PATHS["H4F3d7_original_interval_diagnostic"]).read_text()
    return {
        "original_four_nonbath_source_families_use_FD8":
            all('"'+k+'":"fd8"' in text for k in (
                "2Q_GE06_cross","2Q_GE07_cross","2Q_Lambda_cross",
                "2DY2_action_complete_Y_u_and_phi")),
        "original_two_GE05_source_families_use_FD4":
            all('"'+k+'":"fd4"' in text for k in (
                "2M1_GE05_mapped","2M2_GE05_mapped")),
        "canonical_operator_original_complete_FD4_product":
            "H*D4_x(C14 w)" in op and
            "operator_ward_from_frozen_Cmat" in op,
        "physical_bath_uses_original_FD4":
            "def normalized_bath_euler" in d6
            and "current_d=fd4(current,xx)" in d6,
        "R1_both_one_sided_interval_H_preserved":
            'left=side(' in d7 and 'right=side(' in d7
            and 'hmid=np.sqrt(hh[:-1]*hh[1:])' in d7,
    }


def exact_stencil(rows,degree):
    if len(rows)!=degree+1:
        raise ValueError("invalid preregistered original edge/center rows")
    npoints=degree+1
    records=[]
    for i,row in enumerate(rows):
        offsets=tuple(j-i for j in range(npoints))
        moments=[sum((c*s**p for c,s in zip(row,offsets)),
                     Fraction(0)) for p in range(degree+1)]
        exact=all(m==(Fraction(1) if p==1 else Fraction(0))
                  for p,m in enumerate(moments))
        if not exact:raise RuntimeError("original FD"+str(degree)+" moment failure: "+str(i))
        k=sum((abs(c)*abs(s)**(degree+1)
               for c,s in zip(row,offsets)),Fraction(0))/math.factorial(degree+1)
        stability=sum(map(abs,row),Fraction(0))
        if k<=0 or stability<=0:
            raise RuntimeError("nonpositive original stencil remainder/stability")
        records.append({
            "original_row":i, "location":(
                "interior" if i==degree//2 else
                "left_one_sided" if i<degree//2 else "right_one_sided"),
            "offsets":list(offsets),
            "coefficients_exact":[str(c) for c in row],
            "moments_degree_0_to_p_exact":[str(m) for m in moments],
            "degree_p_polynomial_exact":exact,
            "Taylor_remainder_factor_exact":str(k),
            "Taylor_remainder_factor_float_report_only":float(k),
            "sum_absolute_coefficients_exact":str(stability),
        })
    max_k=max(Fraction(z["Taylor_remainder_factor_exact"]) for z in records)
    return {
        "p":degree,
        "original_row_count":len(records),
        "all_moment_and_positive_remainder_gates":True,
        "distinct_original_rows":records,
        "max_Taylor_remainder_factor_exact":str(max_k),
        "max_Taylor_remainder_factor_float_report_only":float(max_k),
        "predeclared_smooth_bound":
            "|D_p f_i-f'_i| <= h^p K_(p,i) sup_stencil |f^(p+1)|, IF smoothness proven",
    }


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--json-out",required=True)
    args=p.parse_args()
    locks,prereg,amend=source_lock()
    # Refuse to read the original source AST if any frozen source changed.
    if not all(item["exact"] for item in locks.values()):
        raise RuntimeError("H4F3d9 frozen source/predata blob mismatch")
    schemes=original_scheme_binding()
    fd4=exact_stencil(fd4_original_rows(),4)
    fd8=exact_stencil(fd8_original_rows(),8)
    passed=bool(all(schemes.values())
                and fd4["all_moment_and_positive_remainder_gates"]
                and fd8["all_moment_and_positive_remainder_gates"]
                and fd4["original_row_count"]==5
                and fd8["original_row_count"]==9)
    data={
        "classification":(
            "GE19_H4F3D9_EXACT_FD4_FD8_STENCIL_CONSTANTS_PASS_PHYSICAL_BUDGET_OPEN"
            if passed else "GE19_H4F3D9_STENCIL_COMPILER_FAIL"),
        "preregistration":prereg["classification"],
        "preregistration_amendment01":amend["classification"],
        "amendment01_single_original_d7_blob_pin_only":True,
        "frozen_source_blobs":locks,
        "original_operator_and_source_scheme_binding":schemes,
        "FD4_exact_original_stencil":fd4,
        "FD8_exact_original_stencil":fd8,
        "all_stencil_compiler_gates_pass":passed,
        "physical_M5_M9_envelopes_certified":False,
        "piecewise_R1_differentiability_bound_certified":False,
        "Y_zero_set_C9_regularization_bound_certified":False,
        "roundoff_propagation_bound_certified":False,
        "full_physical_FD4_FD8_structural_budget_complete":False,
        "actual_H4F3b_or_H4F3d6_physical_arrays_loaded":False,
        "full_H4_Noether_certified":False,
        "Z21_certified":False,
        "lensing_licensed":False,
        "claim_boundary":"Exact source-derived rational original FD4/FD8 edge/center polynomial moment and conditional C5/C9 Taylor-remainder factors ONLY. Missing physical derivative envelopes, R1/Y regularity and floating-point bounds are hard STOP before any integrated physical full Ward tolerance; no residual-fit and no science certification.",
    }
    out=Path(args.json_out).resolve()
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(data,indent=2,sort_keys=True,allow_nan=False)+"\n")
    print(json.dumps(data,indent=2,sort_keys=True,allow_nan=False))
    if not passed:raise SystemExit(3)


if __name__=="__main__":
    main()
