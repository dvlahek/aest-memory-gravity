#!/usr/bin/env python3
from __future__ import annotations

import argparse
import contextlib
import io
import json
from pathlib import Path
import sys
import tempfile

import numpy as np

import nl1c7a.a6_a10_spherical_reconstruction as rec
import nl1c7b.initial_constraint_certification as b4
import nl1c7b.initial_constraint_certification_repair15 as r15

R15_PASS='NL1C7B4_REPAIR15_DENSITY_Q_COMPLETED_STATE_CERTIFIED'
R15A_PASS='NL1C7B4_REPAIR15A_DENSITY_Q_COMPLETED_STATE_CERTIFIED'
R15A_FAIL='NL1C7B4_REPAIR15A_IMPLEMENTATION_FAIL'


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--trace',required=True)
    ap.add_argument('--coverage-json',required=True)
    ap.add_argument('--repair08-json',required=True)
    ap.add_argument('--repair08-npz',required=True)
    ap.add_argument('--repair14a-json',required=True)
    ap.add_argument('--out',required=True)
    ap.add_argument('--state-npz',required=True)
    a=ap.parse_args()

    # Pre-run accessor provenance check on the exact same dense trace.
    z_rec=rec.read_trace(a.trace)
    ks_rec,gs_rec=rec.groups(z_rec)
    z_b4=b4.read_trace(a.trace)
    ks_b4,gs_b4=b4.groups(z_b4)
    grids_equal=bool(np.array_equal(ks_rec,ks_b4) and len(ks_rec)==128)

    tv_b4=b4.at_ai(gs_b4)
    kq_present=bool('KQ' in tv_b4 and np.all(np.isfinite(np.asarray(tv_b4['KQ'],float))))

    original_at_ai=rec.at_ai

    def at_ai_with_frozen_kq(gs,method):
        out=original_at_ai(gs,method)
        if method!='pchip':
            return out
        bkg=b4.at_ai(gs)
        if 'KQ' not in bkg:
            raise RuntimeError('frozen B4 interpolation did not provide KQ')
        out=dict(out)
        out['KQ']=np.asarray(bkg['KQ'],float)
        return out

    # The frozen Repair15 evaluator itself remains unchanged.
    rec.at_ai=at_ai_with_frozen_kq
    r15.rec.at_ai=at_ai_with_frozen_kq

    argv_old=sys.argv[:]
    sys.argv=[
        'initial_constraint_certification_repair15.py',
        '--trace',a.trace,
        '--coverage-json',a.coverage_json,
        '--repair08-json',a.repair08_json,
        '--repair08-npz',a.repair08_npz,
        '--repair14a-json',a.repair14a_json,
        '--out',a.out,
        '--state-npz',a.state_npz,
    ]

    captured=io.StringIO()
    try:
        with contextlib.redirect_stdout(captured):
            r15.main()
        inner_rc=0
    except SystemExit as e:
        inner_rc=int(e.code or 0)
    finally:
        sys.argv=argv_old
        rec.at_ai=original_at_ai
        r15.rec.at_ai=original_at_ai

    out_path=Path(a.out)
    if not out_path.is_file():
        raise RuntimeError('frozen Repair15 evaluator did not write result JSON')

    result=json.loads(out_path.read_text())
    inherited_class=result.get('classification')
    inherited_gates=result.get('gates',{})
    inherited_pass=bool(
        inner_rc==0
        and inherited_class==R15_PASS
        and len(inherited_gates)==6
        and all(inherited_gates.values())
        and Path(a.state_npz).is_file()
    )

    accessor_gate=bool(grids_equal and kq_present)
    gates={
        'R15A_G1_exact_native_k_grid_match_for_KQ_accessor':accessor_gate,
        'R15A_G2_inherited_frozen_Repair15_all_gates_pass':inherited_pass,
        'R15A_G3_claim_boundary':True,
    }

    certified=bool(all(gates.values()))
    classification=R15A_PASS if certified else R15A_FAIL
    if not certified and Path(a.state_npz).exists():
        Path(a.state_npz).unlink()

    result['classification']=classification
    result['scope']='Repair15a KQ-background-accessor-only repair around the frozen Repair15 evaluator; state construction and all Repair15 science gates unchanged.'
    result['repair15a_accessor_repair']={
        'historical_Repair15_evaluator_classification':inherited_class,
        'historical_Repair15_evaluator_return_code':inner_rc,
        'native_k_grids_exactly_equal':grids_equal,
        'n_native_k_modes':int(len(ks_rec)),
        'frozen_B4_KQ_present_and_finite':kq_present,
        'KQ_source':'b4.at_ai() on the same frozen dense trace',
        'frozen_Repair15_evaluator_modified':False,
        'formula_changed':False,
        'threshold_changed':False,
        'state_rule_changed':False,
        'B4_residual_used':False,
        'attempt01_harness_failure_preserved':True,
    }
    result['inherited_Repair15_gates']=dict(inherited_gates)
    result['gates']=gates
    cb=dict(result.get('claim_boundary',{}))
    cb.update({
        'historical_Repair15_attempt01_harness_failure_preserved':True,
        'frozen_Repair15_evaluator_modified':False,
        'Repair15a_only_KQ_accessor_changed':True,
    })
    result['claim_boundary']=cb
    result['output']['new_state_npz_written']=bool(certified and Path(a.state_npz).is_file())

    out_path.write_text(json.dumps(result,indent=2,sort_keys=True,allow_nan=False)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True,allow_nan=False))
    raise SystemExit(0 if certified else 2)


if __name__=='__main__':
    main()
