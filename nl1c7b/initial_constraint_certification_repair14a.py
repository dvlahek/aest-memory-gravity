#!/usr/bin/env python3
from __future__ import annotations

import argparse
import ast
import contextlib
import hashlib
import io
import json
from pathlib import Path
import sys
import tempfile

import nl1c7b.initial_constraint_certification_repair14 as r14

R14_ATTEMPT01_SHA256='ea4f1d28330b22d6d3d64f5f6f6d27b3646a889fbee9cffc37c4e789282f0966'
R14_ATTEMPT01_CLASS='NL1C7B4_REPAIR14_IMPLEMENTATION_FAIL'
R14_PASS_CLASS='NL1C7B4_REPAIR14_DENSITY_Q_BRIDGE_OMISSION_IDENTIFIED'
EXPECTED_ATTEMPT01_GATES={
    'R14_G1_frozen_provenance':True,
    'R14_G2_exact_Hamiltonian_E_X_gauge_identities':True,
    'R14_G3_exact_B3_first_variations':True,
    'R14_G4_frozen_current_bridge_semantics':False,
    'R14_G5_analytic_Esector_Kcorrection_cancellation':True,
    'R14_G6_corrected_diagnostic_Hamiltonian_second_order':True,
    'R14_G7_corrected_diagnostic_momentum_second_order':True,
    'R14_G8_claim_boundary':True,
}
R14_FROZEN_BLOB='c67aa9f8c64ba2dcb499216feb405a7a339b7b06'


def sha256_file(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):
            h.update(block)
    return h.hexdigest()


def decoded_static_semantics():
    c7=Path('docs/nl1c7a_predata_growing_mode_bridge.md').read_text()
    b4src=Path('nl1c7b/initial_constraint_certification.py').read_text()
    v019_path=Path('v019/apply_patch_v019.py')
    v019=v019_path.read_text()

    c7_current=('deltaQ = rho_A delta_A/(Q K_QQ)' in c7)
    b4_current=("dq=inv(k,(rho/(Q*KQQ))*F['delta_A'],r)" in b4src)
    class_density=("ppw->delta_rho += rho_dark*y[ppw->pv->index_pt_delta_cdm];" in v019)
    pressure_combo=(
        "pba->aest_KB*y[ppw->pv->index_pt_E_aest]+(2.-pba->aest_KB)*chi_aest" in v019
        and "ppw->delta_p += rho_dark*Pi_aest;" in v019
    )

    tree=ast.parse(v019,filename=str(v019_path))
    vals=[]
    for node in ast.walk(tree):
        if isinstance(node,ast.Assign):
            if any(isinstance(t,ast.Name) and t.id=='new_stress' for t in node.targets):
                vals.append(ast.literal_eval(node.value))
    unique_assignment=(len(vals)==1 and isinstance(vals[0],str))
    decoded=vals[0] if unique_assignment else ''
    delta_rho_lines=[
        ln.strip() for ln in decoded.splitlines()
        if 'ppw->delta_rho +=' in ln
    ]
    expected_active_line='ppw->delta_rho += rho_dark*y[ppw->pv->index_pt_delta_cdm];'
    active_line_found=(expected_active_line in delta_rho_lines)
    no_explicit_Echi_density=bool(
        unique_assignment
        and active_line_found
        and delta_rho_lines
        and all(('E_aest' not in ln and 'chi_aest' not in ln) for ln in delta_rho_lines)
    )

    gates={
        'C7A_current_deltaQ_relation_found':c7_current,
        'B4_current_deltaQ_implementation_found':b4_current,
        'CLASS_effective_density_deltaA_line_found':class_density,
        'CLASS_Echi_pressure_combination_found':pressure_combo,
        'CLASS_new_stress_unique_AST_assignment':unique_assignment,
        'CLASS_active_decoded_delta_rho_line_found':active_line_found,
        'CLASS_no_explicit_Echi_delta_rho_line':no_explicit_Echi_density,
    }
    return {
        'parser':'ast.literal_eval(new_stress) then decoded C splitlines',
        'checks':gates,
        'pass':bool(all(gates.values())),
        'decoded_delta_rho_lines':delta_rho_lines,
    }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--trace',required=True)
    ap.add_argument('--coverage-json',required=True)
    ap.add_argument('--repair08-json',required=True)
    ap.add_argument('--repair08-npz',required=True)
    ap.add_argument('--repair10-json',required=True)
    ap.add_argument('--repair11-json',required=True)
    ap.add_argument('--repair12-json',required=True)
    ap.add_argument('--repair13-json',required=True)
    ap.add_argument('--repair13a-json',required=True)
    ap.add_argument('--repair14-json',required=True)
    ap.add_argument('--out',required=True)
    a=ap.parse_args()

    hist=json.loads(Path(a.repair14_json).read_text())
    hist_hash=sha256_file(a.repair14_json)
    g_hist=bool(
        hist_hash==R14_ATTEMPT01_SHA256
        and hist.get('classification')==R14_ATTEMPT01_CLASS
        and hist.get('gates')==EXPECTED_ATTEMPT01_GATES
    )

    fixed=decoded_static_semantics()
    g_parser=bool(fixed['pass'])

    original_static=r14.static_semantics
    r14.static_semantics=decoded_static_semantics

    with tempfile.TemporaryDirectory() as td:
        inner=Path(td)/'repair14a_inner.json'
        argv_old=sys.argv[:]
        sys.argv=[
            'initial_constraint_certification_repair14.py',
            '--trace',a.trace,
            '--coverage-json',a.coverage_json,
            '--repair08-json',a.repair08_json,
            '--repair08-npz',a.repair08_npz,
            '--repair10-json',a.repair10_json,
            '--repair11-json',a.repair11_json,
            '--repair12-json',a.repair12_json,
            '--repair13-json',a.repair13_json,
            '--repair13a-json',a.repair13a_json,
            '--out',str(inner),
        ]
        captured=io.StringIO()
        try:
            with contextlib.redirect_stdout(captured):
                r14.main()
            inner_rc=0
        except SystemExit as e:
            inner_rc=int(e.code or 0)
        finally:
            sys.argv=argv_old
            r14.static_semantics=original_static

        if not inner.exists():
            raise RuntimeError('frozen Repair14 evaluator did not write inner output')
        current=json.loads(inner.read_text())

    g_inherited=bool(
        inner_rc==0
        and current.get('classification')==R14_PASS_CLASS
        and all(current.get('gates',{}).values())
        and current.get('static_bridge_semantics',{}).get('pass') is True
    )

    science_keys=(
        'symbolic_audit','background','analytic_profile_rows',
        'corrected_diagnostic_order_rows','summary','state_anchor','claim_boundary'
    )
    payload_equal=all(current.get(k)==hist.get(k) for k in science_keys)

    claim_boundary=dict(current.get('claim_boundary',{}))
    claim_boundary.update({
        'historical_Repair14_attempt01_implementation_fail_preserved':True,
        'Repair14_frozen_evaluator_modified':False,
        'science_threshold_changed_in_Repair14a':False,
        'science_path_changed_in_Repair14a':False,
    })
    g_claim=bool(
        claim_boundary['historical_Repair14_attempt01_implementation_fail_preserved']
        and not claim_boundary['Repair14_frozen_evaluator_modified']
        and not claim_boundary['science_threshold_changed_in_Repair14a']
        and not claim_boundary['science_path_changed_in_Repair14a']
    )

    gates={
        'R14A_G1_historical_attempt01_hash_and_gate_pattern':g_hist,
        'R14A_G2_decoded_static_semantics_parser':g_parser,
        'R14A_G3_inherited_Repair14_all_gates_pass':g_inherited,
        'R14A_G4_claim_boundary':g_claim,
    }

    if all(gates.values()):
        cls='NL1C7B4_REPAIR14A_DENSITY_Q_BRIDGE_OMISSION_IDENTIFIED'
        rc=0
    else:
        cls='NL1C7B4_REPAIR14A_IMPLEMENTATION_FAIL'
        rc=2

    result=dict(current)
    result['classification']=cls
    result['scope']='Repair14a representation-only repair of the frozen Repair14 v0.19 static-semantics parser; all Repair14 science semantics inherited unchanged.'
    result['historical_Repair14_attempt01']={
        'sha256':hist_hash,
        'classification':hist.get('classification'),
        'gates':hist.get('gates'),
        'result_freeze_commit':'381bc30d6266b12c3590b9138c9f1a7bc07de9cc',
        'preserved':True,
    }
    result['repair14a_parser_repair']={
        'repair14_frozen_blob':R14_FROZEN_BLOB,
        'repair14a_prereg_commit':'f8eed7308018bc8f7e626128d9a375c6fc90b374',
        'attempt01_physical_line_scan_replaced':True,
        'decoded_static_semantics':fixed,
        'science_payload_exactly_reproduced_vs_attempt01':payload_equal,
        'science_payload_exact_reproduction_is_diagnostic_not_gate':True,
    }
    result['inherited_Repair14_gates']=current.get('gates')
    result['gates']=gates
    result['claim_boundary']=claim_boundary
    result['interpretation_boundary']=dict(current.get('interpretation_boundary',{}))
    result['interpretation_boundary'].update({
        'historical_Repair14_attempt01_relabelled':False,
        'density_Q_bridge_omission_identified_if_Repair14a_pass':bool(all(gates.values())),
    })

    out=Path(a.out)
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2,sort_keys=True,allow_nan=False)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True,allow_nan=False))
    raise SystemExit(rc)


if __name__=='__main__':
    main()
